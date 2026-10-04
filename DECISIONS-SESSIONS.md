# Decisions — is this session finished, and whose change is this path?

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

Decisions **D013, D027, D028, D037**. Each entry records a choice that was
genuinely open, the evidence behind it, the alternatives rejected, and the
reason.

**Invariant:** every entry here governs *the state of a session's own record* —
whether an unfinished session is in flight or provably abandoned, and which
machine a recorded path belongs to. How a **gate** is designed and run belongs in
[`DECISIONS-GATING.md`](DECISIONS-GATING.md); how work is recorded, moved, and
published in [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md); what *passes* in
[`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md). The index is
[`DECISIONS.md`](DECISIONS.md).

Split out on 2026-10-04, after two other splits of the same three entries were
tried and reversed in the same hour: into `DECISIONS-PRACTICE.md`, which then
reached 323 lines because the other VM had just appended D031 there, and into
`DECISIONS-GATING.md`, which reached 356. **The failure was the split's premise,
not its arithmetic** — both attempts moved entries to make a file fit, and neither
had an invariant that said why the entries belonged where they were put. This one
does: these three decide the state of a session's record, which is neither a gate
nor a publication. Entries moved whole, not retyped; numbering is continuous and
unchanged, so a reference to D013, D027 or D028 still resolves.

## D013 — Local verification tolerates an in-flight session; CI does not (2026-10-03)

Observed: `origin preflight` failed whenever it was run during a session, because
the current session has no `session_end` yet. A gate that cannot be run while
working is a gate that gets skipped.

Decision: `session verify` and `preflight` report the session in flight as
"in progress" and exit `0`. Both accept `--strict`, which fails for it; CI uses
`session verify --strict`, since on a pushed commit nothing is in flight and an
unfinished session genuinely is a failure.

Rejected: dropping the check for unfinished sessions entirely, because then a
crashed run would be indistinguishable from a completed one. Making strictness the
only mode, because it would make local use useless.

## D027 — An unfinished session fails CI only when it is provably abandoned (2026-10-03)

Observed: D013's premise does not hold for this fleet. `task claim` requires
HEAD to equal the remote base before it publishes a claim, so a VM that claims a
task must push its `session_start` first — measured on 2026-10-03 as `dfa6eb9`
(session 030's start) immediately followed by `4791ed3` (its claim). The
unfinished session is therefore *structurally required* to be on the shared base
branch, and `session verify --strict` failed on every push of every VM for as
long as any session was open. Run `37157528596`: four gates green, one red, and
the red one was reporting correct behaviour against an impossible premise.

Decision: strict verification asks whether an unfinished session is still **in
flight**, derived from the tree alone by `tools/originlib/inflight.py` — its
`session_start` names a task; that task is `claimed`; the claim identifies this
session by `claim-session`, or failing that by `claim-agent` plus `claim-vm`;
the last ledger entry for that task still opens a claim; and the claim is
younger than `--lease-hours` (default 12). An unfinished session failing any
clause is **abandoned** and fails the gate with the clause named. An in-flight
one is a note printing task, holder, and claim age, which CI re-emits as a
`::warning::` annotation. D013 is unchanged for the session running in the
working tree being checked.

Rejected: (a) dropping `--strict` entirely, which loses every unfinished-session
signal including the ones this keeps; (b) making the whole check a warning,
which leaves a crashed session indistinguishable from a live one forever; (c) a
bare staleness window on the last event with no claim check, which cannot tell
one long honest session from a dead VM's while the record already carries the
thing that can; (d) keeping in-flight sessions off the base branch by publishing
claims on a separate ref, which would hide the claim from `sync land` and from a
reader browsing the base branch — trading a cosmetic problem for the real one.

**Cost, stated plainly.** A crash *inside* the lease window is not detected by
this gate: the claim stays in force for up to `--lease-hours`, so a dead VM's
session keeps CI green for that long. Bounded detection comes from `task list
--remote`, which names the holder and the claim time, and the lease is a flag so
an operator can shorten it. No lease at all was rejected because "in flight"
with no upper bound is precisely the hiding place this replaces.

**Ceiling.** One gate made truthful. It says nothing about whether the claims it
trusts are true, and a session that crashes after `task complete` still looks
finished. Those are different problems, not solved ones.

**Clause 1 relaxed by observation, not by design.** The first implementation
required the `session_start` to name a task. Run against the live record it
immediately produced a false red: `instance-20260717-0944` started session
`2026-10-03-037-repair-the-three-mission-records-corrupt` without `--task` and
then claimed T-0021, so the predicate read a demonstrably live session as
abandoned. A claim in the ledger that *names the session* is now accepted in
place of the `task` field, under the same opening-action and lease clauses.
`--task` should still be passed; the fallback exists because the predicate met
reality, not because omitting it was right.

Consequence: `tools/origin session verify --strict` exits `0` in this repository
while a session on either VM is in flight; `tests/test_inflight_session.py`
fails if any clause is removed (verified by mutating each clause and re-running);
`docs/operations/ci.md` states what the gate now catches and what it does not.

Split on 2026-10-03 (T-0020): D019–D023 moved verbatim to
[`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md), because adding D024–D027 took
the gating file past the 300-line cap. D025 and D026 were written on
`instance-20260717-0944` while this branch was unpublished, so the session-gate
decision drafted as D025 is D027. Numbering is unchanged.

## D028 — Reconciliation attributes by the recorded base move, not by authorship (2026-10-04)

Observed: session 029 (T-0016) closed with exit `4` and nine `unlogged_change`
events, every one naming a file that session never touched —
`EXPERIMENTS/007-build-timestamps/*`, `tasks/T-0013-*`, `tasks/T-0017-*`,
`HYPOTHESES*.md`, `RESEARCH.md`, `DECISIONS-PRACTICE.md`. The reflog shows the
cause: `sync land` rebased the branch onto the other VM's commits at 22:04:28 and
22:06:08, reconciliation ran at 22:10:23, and a diff against the session's
*starting* commit cannot tell a landed commit from one the session made. Four
false `doc_update` events and a `documentation_gaps` report came from the same
comparison. `observed`, `instance-20260717-0947`, now replayed by
`tests/test_landed_work.py`.

Decision: the evidence is recorded while the branch moves. `sync pull` and
`sync land` append a `base_advance` event naming the commits that arrived. A path
is *not* this session's change when the newest thing to touch it is one of those
commits, and *is* this session's change again when the newest thing is one of its
own commits or an uncommitted edit. One change set feeds `unlogged_change`,
`doc_update` and `documentation_gaps`, and `session finish` prints what it
excluded, so an excluded path is never silently dropped.

Rejected: **git authorship** (`--author`, `%an`), which needs no new record and is
therefore the strongest baseline available. Falsified by evidence, not argument:
every commit in session 029's range is authored `Ihsan Ai Server Bot` on both
VMs, so it separates nothing. Rejected: **exclude whatever another session
declared**, which cannot say which of two edits to `STATE.md` was the undeclared
one, and would hide real work. Rejected: **infer from commit timestamps**, which
require the two machines' clocks to agree.

The asymmetry is the safety property: a base move the tooling did not perform
records nothing, so its paths stay reported. The tooling never silences a file it
cannot prove belongs to someone else.

**Ceiling.** Attribution knows only about base moves `tools/origin` performed. It
reads git's history to decide which commit touched a path last, so a session that
rewrites history after landing leaves the rule matching shas that no longer
exist, and those paths are reported again — conservative, not wrong, but a real
limit. Neither the defect nor its repair says anything about a candidate; this is
bookkeeping hygiene with a measured cost.

**Falsified against its own defect.** The new tests ran against the pre-change
code first: 4 failures and 1 error, naming the very paths session 029
mis-attributed. With the exclusion removed again, 3 of the 6 fail; the 3 that
still pass are the negative controls, which must not change. Both runs are in this
session's `commands.log`.

## D037 — A path is attributed by the bytes a command wrote, not by the file's name (2026-10-04)

Observed: `task claim`, `task complete` and `task release` rewrite the task file
they manage, and reconciliation reports every file this session changed without
declaring it. So every one of those commands closed its session with exit 4
naming the tooling's own write. The record understated it: defect 12 counted
"three such events in two sessions", because it was read from two sessions, and
a sweep of every closed session's stream finds **37 reports naming a task file,
across 21 sessions** (`observed` 2026-10-04, by reading each
`sessions/*/events.jsonl` out of git). Session `2026-10-04-019` is the clean
instance: it declared seven artifacts, ran `task complete`, and closed `worked`
with `unlogged_changes: 1` naming `tasks/T-0039-*.md`.

Decision: **the tooling declares its own writes, and the declaration names the
bytes rather than the file.** `_set_meta` is the only function that rewrites a
task file's meta block, so it — and not the four commands that call it — appends a
`task_rewrite` event carrying the path, the task, the status, and two SHA-256
digests: one of the meta block and one of everything outside it.
`reconcile.command_rewrites` honours a path only while both digests still match.
Two consequences follow, and the second is the point. The command's write is not
reported. And an agent's *next* edit to the same file changes one of the two
digests and is reported, so ticking an acceptance checkbox is still a declared
change or a reported gap. The path is also printed on a `REWRITTEN by task
commands` line at finish, because an excluded path an operator cannot see is an
excluded path they cannot check — the reason D028 prints what it excluded.

Rejected: **exclude `tasks/*.md`**, the cheapest form and the one the defect's own
note called the trade-off. It silences every later edit to every task file, which
is the signal rather than the noise. Rejected: **let the agent declare the task
file by hand**, which is what was happening and what produced 37 false reports; it
also asks the agent to remember a second command immediately after running one,
which is the state in which remembering is least likely. Rejected: **drop the
status from the task file and read it from the ledger alone** — the one design
with no second copy of the truth, and a much larger change to the task model than
a bookkeeping defect justifies. Rejected: **write the declaration into
`tasks/CLAIMS.jsonl`**, where the command already writes, because attribution then
has to decide which VM appended a line, and the session's own stream answers that
without a rule.

**Falsified in both directions, and the first attempt falsified nothing.** With
the clause in `reconcile` removed, 4 of the 14 new tests fail, one of them the
defect's own shape. With only the digest bound removed, 3 fail, and they are
exactly the two hand-edit controls plus the digest unit test. The first attempt at
the first mutation *passed all 14*: the patch script's `str.replace` pattern did
not match the file's real indentation, so nothing was mutated and a green run was
read as a control. The pattern is now asserted before the run — **a mutation that
does not check it landed cannot fail, which makes it the weakest link in a
falsification rather than the strongest.**

**Ceiling.** The declaration is per path and per byte-range: it covers the meta
block and the body as they were, so a task file that later gained a third region
is not covered, and one with a second `task-meta` block is compared against the
first. A command run with no session open records nothing, so the next session
reports the file — the intended direction of failure, and the same asymmetry D028
is built on. Nothing here changes what the ledger or the indexes say; this decides
whose change a recorded path is, and nothing else. Defect 12 measured the false
positives; it says nothing about the false negative recorded beside it, which is
a separate question and an open one.
