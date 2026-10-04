# Decisions — what a command's own write is, and who publishes it

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

Decisions **D040, D042, D044–D045**. Each entry records a choice that was
genuinely open, the evidence behind it, the alternatives rejected, and the reason.

**Invariant:** every entry here governs *a write the tooling made on the agent's
behalf, and who is answerable for publishing it* — what counts as that write, what
it must carry when it is published, and what happens when two VMs make the same
one. Whether a session is finished and whose path a recorded file belongs to is
[`DECISIONS-SESSIONS.md`](DECISIONS-SESSIONS.md); how the record's own artefacts are
constrained is [`DECISIONS-RECORDS.md`](DECISIONS-RECORDS.md); the index is
[`DECISIONS.md`](DECISIONS.md).

Split out on 2026-10-04 (T-0054) when `DECISIONS-SESSIONS.md` reached 315 of the
300 permitted lines. **The division is by invariant and not by convenience, which
is the mistake this repository has now paid for twice in this file.** The first
split moved entries to make a file fit and was reversed within the hour; the
second moved them "because three decide the state of a session's record", which
was true of D013, D027 and D028 and not of the four here. Those four ask a
different question — not *whose* change is this path, but *what does a command's
own write consist of, and what must travel with it when it is published* — and
D044 and D045 had outgrown the sentence describing the file while sitting in it.
Entries moved verbatim, numbering continuous and unchanged, so a reference to D040,
D042, D044 or D045 still resolves. The header of the file they came from was
widened to name them, which is what [`decisionheader.py`](tools/originlib/decisionheader.py)
holds to `DECISIONS.md`; that check exists because a header can be false while
every index row is right.

## D040 — A path is attributed by the bytes a command wrote, not by the file's name (2026-10-04)

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

## D042 — An exemption answers one question, and borrowing a predicate borrows the question (2026-10-04)

Observed: `reconcile._is_vendored` called `doclint.is_exempt`, which returns true for
every `.json`, `.jsonl` and `.log` path because those suffixes are exempt from the
300-line cap. So a session's report excluded every data-file edit in the repository:
`tests/python-versions.json` and `tests/git-versions.json` — the records that decide
whether this VM can run the work — could change with nothing declared and nothing
reported. Defect 12's entry named this in one clause and no gate read it, because a
numbered defect list is prose and D025 asks for a gate.

Decision: **a predicate is named for the question it answers, and a caller that means
a different question must not reuse it.** `doclint` now offers `is_data_suffix` (is
this file's length worth reading — the cap's question) and `is_declared_exempt` (is
another check already looking at this file — both questions'), and reconciliation
reads only the second. The corollary is D040's, extended: an exemption that survives
only because of a file's *name* is not an exemption but a hole, so a command's own
write is declared by its bytes — now for the claim ledger and `vendor/hashes.json` as
well as a task file's `task-meta` block, the shapes told apart by the keys the event
carries and never by the path.

Rejected: declaring `vendor/hashes.json` generated. Nothing generates it with a mark,
and `skills verify` compares the *skills* against it, so it cannot detect a hand edit
to itself — a name-based exemption there would be the same hole moved. Rejected:
leaving the sweep a session note. The number says whether the residual is a note or a
blocker, and it came out at 72 (session, path) pairs over 17 paths, 50 of them a
ledger no closed session can declare. Rejected: making the cap read data files, which
would have hidden the borrowing rather than corrected it.

**Ceiling.** `declaredwrite.matches` trusts whichever shape an event carries, so an
event forged with a whole-file digest for a task file would be honoured — the digests
are only as trustworthy as the appender that wrote them, the same trust D040 rests on.
And the repair is forward-only: a closed stream is not edited, so 50 historical
sessions now report a file they cannot declare, and nothing reads them.

## D045 — A collision on the work yields like a collision on an identifier (2026-10-04)

Evidence: T-0054 cancelled, session `2026-10-04-040`. Record in the task file
`tasks/T-0054-*.md`; rule in
[`multi-vm-coordination.md`](docs/process/multi-vm-coordination.md).

**The choice.** This VM's unpushed repair to a defect the other VM had already
repaired and landed was **dropped whole rather than merged**, and the task
cancelled. Alternative: reconcile the two implementations.

**Why.** Two modules publishing a claim's paths is worse than one — the reason a
list written twice is wrong once, which D044's own rejected alternative names. The
landed version was stronger in the half this side had not reached: it refuses a
foreign dirty tree *before* writing, where this side appended to the ledger first
and refused at the push, which is the duplicate-line cost.

**The general form, and it is not the identifier rule's.** The standing rule is
*renumber on the side that has not been pushed*, and it had only ever been applied
to identifiers, because the identifier detector is what finds them. Here the two
VMs took **different** numbers — T-0054 and T-0055 — for one defect, so neither
`idalloc` nor `idcheck` had anything to say, and correctly so: no identifier
collided, the *finding* did. **Nothing here detects a collision on the work**, so
the yield is a habit rather than a refusal, and the habit is `task list --remote`
before writing code.

**Kept, because it was not duplication.** A claim made with a session open is
proved to publish, and a published claim is proved to exclude the other VM — but
not their *composition*, the order the protocol documents and the order the defect
lived in, since a claim that could not be published excluded nobody.

**Ceiling.** A VM that reads the base late still spends the work; the rule says
what to do once it finds out, and `git log` cannot show that a commit was dropped
on purpose.

## D044 — The session's own record is not uncommitted work, and the claim says so

Evidence: T-0055, session `2026-10-04-041`, 2026-10-04. Defect 21 in
[`STATE-defects.md`](STATE-defects.md); [`FAILURES-findings-5.md`](FAILURES-findings-5.md)
F023.

**The choice.** A claim's commit carries the open session's own record, and
anything else uncommitted refuses the claim **before** anything is written. Both
halves were open. The alternative was to keep `push`'s blanket dirty-tree refusal
and tell agents to commit their session record by hand before claiming, which is
what happened for thirty minutes at session 038.

Decision: **a command that publishes its own write must decide what "publishable"
means, and the session's record is part of the command's own output rather than the
agent's unreviewed work.** `claimpublish.claim_paths` reads the session's paths from
`sessionflow.session_owned_paths` — the module that owns that definition — and
`claimpublish.refuse_uncommitted_work` asks `sessionflow.uncommitted_work`, the
predicate `session finish --push` already used for exactly this question. Neither
list is written out a second time.

Rejected: making `sync.push` tolerant of any dirty tree that is session-owned.
Broader than the defect and it weakens the primitive every other caller relies on;
the composition belongs in the caller that composes it. Rejected: having the claim
commit the session record in a *separate* commit first. It would have needed the
record to be clean before the claim's own `task_rewrite` event, which is written
during the claim — so the second commit still has to come after, and the separate
commit breaks `_discard_claim_commit`, whose whole contract is `ahead == 1`.
Rejected: staging `sessions/<id>` by hand rather than through `session_owned_paths`.
The first attempt did exactly that and the test caught it: `sessions/INDEX.md` was
still dirty and the refusal was byte-identical to the defect's. A list written twice
is a list that will be wrong once.

**Ceiling.** The claim commit is no longer confined to `tasks/`, so a reader of
`git log` sees session events beside the ledger. `sync land` still refuses a dirty
tree outright, because a rebase genuinely needs a clean one and the same reasoning
does not reach that command. And the commit-then-push window remains: a crash
between `_commit_paths` and `sync.push` leaves one local commit that the next
`_require_at_base` names — which is the direction of failure, and it is a message
rather than a silent claim.
