# Decisions — recording, verifying, publishing, and gating work

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

Decisions **D011–D018, D027–D028**. Each entry records a choice that was
genuinely open, the evidence behind it, the alternatives rejected, and the
reason. Decisions that constrain later work belong here; ordinary edits do not.

**Invariant:** every entry in this file governs *how work is recorded, moved, or
published* — the tooling and the mechanics a session must satisfy. If a decision
can be restated as "what the mission is, what the workspace is, or what counts
as evidence", it belongs in
[`DECISIONS-FOUNDATION.md`](DECISIONS-FOUNDATION.md) instead; if it governs how
work is verified, screened, or judged, it belongs in
[`DECISIONS-GATING.md`](DECISIONS-GATING.md). The index is
[`DECISIONS.md`](DECISIONS.md).

Split on 2026-10-03 (T-0018) when this file reached 297 of the 300 permitted
lines: D013 and D019–D023 moved verbatim to `DECISIONS-GATING.md`; D019–D021 then
moved again to `DECISIONS-SCREENING.md` (T-0020). Numbering is
continuous and unchanged.

D013 came back on 2026-10-04 (T-0030) with D027 and D028, because the three
together decide whether a session is finished, in flight, or abandoned, and whose
change a recorded path is — the mechanics of a session's own record, which is
this file's invariant. They left `DECISIONS-GATING.md` because D030 had reached
289 of its 300 permitted lines. Entries moved verbatim; numbering is continuous
and unchanged, so a reference to D013, D027 or D028 still resolves.

## D011 — Artifact declaration takes several paths and a directory (2026-10-03)

Observed: session 002 declared 57 artifacts in a single hand-written list at the
end of the session and omitted 55 committed files. `session finish` reported every
one and exited `4`. Recorded in `FAILURES.md` F003.

Decision: `origin session artifact` accepts multiple paths and a repeatable
`--dir`, which declares every file beneath a directory. Each file still receives
its own SHA-256, because a hash of a directory says nothing about its contents.

Rejected: leaving the command single-file and relying on discipline, because the
failure was a foreseeable consequence of the interface, not of carelessness.
Allowing a directory to be declared as one artifact, because it would remove the
per-file verifiability that makes the record worth having.

## D012 — Secret scanning can be waived per file, by name, and only visibly (2026-10-03)

Observed: a scanner's own test fixtures must contain credentials that look real.
The scanner correctly refused to record such a file as an artifact, which left no
way to declare a test file at all.

Decision: a file may declare `# origin-allow-secret-patterns: <names>` within its
first 40 lines. It suppresses exactly the patterns named, applies to that file
only, and is recorded as a `note` event when the file is declared. Suppressing a
specific pattern also silences the generic `assigned-credential` rule when that
rule merely re-reported the same span, so one name is enough.

Reasoning: the alternative was to weaken the scanner, which protects a git history
that cannot be rewritten. A named, per-file, logged waiver keeps the default safe
while making the legitimate case expressible. A waiver for a real credential is
still wrong; it is only narrower, not endorsed.

## D014 — Gitignored paths are never artifacts (2026-10-03)

Observed: a `--dir tools` sweep declared 13 `__pycache__/*.pyc` files, which then
appeared in a generated session report as deliverables. `FAILURES.md` F004.

Decision: `origin session artifact` refuses a named file that git ignores, and a
directory sweep skips ignored files while printing what it skipped.

Reasoning: build output is reproducible from the source that is being declared, so
recording it adds noise without evidence. This is the same rule already applied to
vendored content, which is hash-verified rather than declared. It should have been
applied when `--dir` was introduced; it was found by reading a report instead.
## D015 — A claim is published, or it is not a claim (2026-10-03)

Observed: `origin task claim` mutated only the local task file, so two VMs could
both believe they held one task (`FAILURES.md` F005).

Decision: a claim is committed and pushed to the shared base branch, and git's
ref update is the lock. The claim commit must be the only thing between the
branch and the base, so a claim can never carry unreviewed work onto the shared
branch. A rejected push means another VM won: the claim commit is discarded, the
winner is named, and the loser changes nothing. Taking a dead VM's task requires
`--takeover "reason"`, which is written to the ledger with the superseded holder.

Rejected: a lock file in the repository, because two VMs writing one file is the
same lost-update problem one level down. A claim queue service, because the point
of this repository is that it works with only git. Advisory claims with a
convention attached, because that is the arrangement that just failed.

Consequence: claiming a task requires the branch to be at the base, so a VM with
unlanded work is told to land it first instead of quietly publishing it.

## D016 — One worktree and branch per task, not one shared tree (2026-10-03)

Observed: every VM worked in its own clone, so within one machine two agents —
or one agent and one background run — shared one index, one
`sessions/active.json` pointer, and one set of uncommitted changes. `session
start` refuses a second session, so the second agent has nowhere to record
itself, and `git add -A` cannot tell whose change it is staging.

Decision: `origin worktree add --task T-NNNN` creates `.worktrees/T-NNNN-<vm>`
on branch `task/T-NNNN-<vm>` from `origin/<base>`. The tooling adds
`.worktrees/` to `.gitignore` if it is missing, so the isolation mechanism cannot
commit itself. A worktree is refused when the task is claimed elsewhere, when this
VM already has one for that task, or when the branch name is taken.

Rejected: relying on agents to `cd` into separate clones, because nothing recorded
which directory belonged to which task. Nested worktrees inside the repository
tree, because the parent would then see the child's files.

## D017 — Sessions fetch on the way in; only the record is committed on the way out (2026-10-03)

Observed: a session could start from a tree that was behind the shared base, and
finish with its record sitting only on that VM.

Decision: `session start` fetches and fast-forwards by default, refuses a dirty
tree when the remote has moved, and records which remote commit it synced to;
`--no-sync` is the explicit opt-out for an offline machine. `session finish
--push` commits the session's own files — its directory and the three generated
indexes — and pushes the branch, refusing while unrelated edits are uncommitted.
`origin sync land` rebases a work branch onto the base and pushes it, resolving
conflicts in generated indexes by regenerating them and stopping on every other
conflict. Nothing is ever force-pushed.

Rejected: auto-committing the agent's work with a generated message, because a
commit message is the place where a human-readable claim about the work lives,
and a generated one would be a claim nobody made. Force-pushing to resolve a
diverged branch, because it destroys the other VM's work silently.

Consequence: `land` is the only operation that moves work onto the shared branch,
so it is the place where a real merge conflict becomes visible to a person.

## D018 — The App JWT generator lives under `~/.config`, not `/tmp` (2026-10-03)

Observed: on `instance-20260717-0947` the git credential helper invoked
`/tmp/github-app-jwt.sh`. `/tmp` was cleared, so every push failed with
`could not read Username` even though the private key and the helper survived.
The App ID itself was not stored anywhere durable and had to be recovered.

Decision: the JWT generator is a small script at
`~/.config/github-app/jwt.py`; the App ID is a `0600` file at
`~/.config/github-app/app-id`; the credential helper references the script in
`~/.config` rather than `/tmp`. The App ID (5173845) was recovered from the
bot's public avatar URL, which for GitHub Apps embeds the app id.

Rejected: recreating the script in `/tmp` on every session, because an ephemeral
path silently removes the ability to push and the failure looks like an auth
error rather than a missing file. Storing the App ID in the repository, because
it is credential-adjacent configuration and the private key must stay per-VM.

Consequence: a VM's ability to push no longer depends on `/tmp` surviving.
The helper still reads the private key at the moment of use and never copies it.

## D031 — An identifier is allocated from the shared base, and the record of that is printed (2026-10-04)

Observed: `tasks.next_task_id` listed this VM's `tasks/` directory and added one.
Between 2026-10-03 and 2026-10-04, two VMs took the same identifier twelve times
— `observed` from the history, not from a report about it: `83aa9a4` and `569a7ce`
each added a different `tasks/T-0024-*.md`, commit `e6eb992` carries two `## F010`
definitions, and one task on this VM was renumbered through T-0026, T-0027, T-0028
and T-0029 in four separate commits before it could be published. A working tree
is one VM's opinion of the ledger; nothing recorded how old that opinion was.

Decision: **an F, D or T number is allocated from `origin/<base>` plus this
working tree, and every command that hands out a number prints the record it was
read from.** `tools/originlib/idalloc.py` fetches, reads the numbered records at
the base — task files, the claim ledger, findings definitions and index rows,
decision definitions and spans — takes one above the highest either side defines,
and returns that together with `local_highest`, `remote_highest`, `fetched` and
the ref and commit it read. Three states are distinguishable and each is printed
differently: the base was read and is current; it was read but a fetch failed, so
the number may already be stale; or no base was readable at all.

Falsified before it was trusted, per D025: with the old allocator a clone whose
tree is behind the base allocated `T-0002` where the base already defined it, and
after the repair `T-0003`. A withdrawn task's number is no longer recycled,
because the ledger still names it. A withdrawn *finding* is not recycled either —
a row with no definition is an allocated number too, which is the state a
half-finished renumbering leaves behind.

Rejected: a lock or a reservation service, because git is the only shared state
here and a second source of truth is a new way to disagree with it. Rejecting a
commit whose number the base already holds, because that is a detector and
detectors cannot stop a race — they only make it visible afterwards, and that
half is T-0030. Numbering only tasks and leaving F and D to memory, which is how
eight of the twelve collisions happened. Treating a prose mention of a number as
an allocation, because the allocator would then drift upward with every citation.

Consequence: [`docs/reference/identifier-allocation.md`](docs/reference/identifier-allocation.md)
states the rule and the ceiling, and the three printed states are distinguished
in [`cli-reference.md`](docs/reference/cli-reference.md). **The ceiling is
unchanged in kind:** two VMs allocating between their own fetches still collide,
and an unpushed number reserves nothing. What changed is that a stale tree — the
condition behind all twelve — no longer decides anything.

## D033 — An exercised-environment record states what nobody has run, and its test checks honesty (2026-10-04)

Observed: `docs/operations/vm-execution.md` said plainly that no gate pinned a
Python range while [`tests/git-versions.json`](tests/git-versions.json)
pinned git, and T-0023 had already had to repair a mission record demanding a
3.11+ floor invented from one machine's 3.14.6 — a claim about interpreters the
fleet has never run. A floor asserted in prose is a claim about what someone
believes.

Decision: **the exercised interpreters live in
[`tests/python-versions.json`](tests/python-versions.json) (schema
`origin.python-versions/1`), and the test that validates it checks honesty
clauses rather than schema alone.** Every entry carries the scope it has actually
run — 3.8.10 has run all 335 tests, the standalone 3.12.15 only the 173 that
existed when T-0016 recorded it, CI's `'3.12'` only the minor version, because
the run log needs repository admin rights. `not_exercised` names 3.9 through 3.11,
3.13 and newer, and any non-CPython or non-Linux target. The record's `floor`
must be a minor version some entry ran; the test compares minor versions, so
"3.8 or newer" is supported by 3.8.10 and a record that had never run 3.8 fails.

**Renumbered from D032 on 2026-10-04:** `instance-20260717-0947` published its
own D032 (the collision detector, T-0030) while this session was resolving a
rebase, and the two mean different things. This side is the one not pushed, so
it moved — D033. Recorded here because the collision was found by the rebase
itself and because the other VM's D032 is a real decision, not a mistake.

Falsified four ways before it was trusted, per D025: a floor claiming 3.10, an
entry with no `scope`, CI credited with the unreadable patch `3.12.7`, and an
emptied `not_exercised` list each fail the test, and the restored record passes.
A schema check passes just as happily on a record that lies, which is why those
four are the clauses.

Rejected: recording only the versions that work, on the grounds that the others
are noise — that is the record that produced the invented 3.11 floor. Having
`doctor` compare this VM's interpreter, which is the *reading* half of defect 6
and a separate change: it would make a VM warn, and this task is about making the
claim true. Listing a supported range such as "3.8–3.12", which no run supports.

Consequence: defect 6 is twice-partly closed — the claim exists and is checked,
and what remains is that nothing reads it at run time.
[`vm-execution.md`](docs/operations/vm-execution.md) says so instead of calling the
work unclaimed, and [`ci.md`](docs/operations/ci.md) states that pinning 3.12 is a
recorded decision rather than evidence about the fleet.

## D034 — An environment record is read at run time, and "could not look" is its own answer (2026-10-04)

Observed: `tests/git-versions.json` (T-0018) and `tests/python-versions.json`
(T-0032) recorded what the suite has run on, and `doctor` printed
`tool python3 Python 3.8.10` beside a git version without ever consulting
either. A VM on Python 3.9 was indistinguishable in the report from one on
3.8.10, and the only way to learn the difference was to open a JSON file by hand —
the same class of failure T-0025 found in this report when it printed
`credentials none present` for three different machines (D025, D030).

Decision: **a record of what has been exercised is read by the diagnostic that
reports the environment, and the comparison distinguishes four states.** `doctor`
now prints `exercised` with the matched entry's own `scope` attached, `NOT
exercised` for a version no entry names, `record unreadable` for a record that is
missing or does not parse, and `no record` for the three probed tools no record
covers. Matching is by dotted prefix with the longest entry first, because the
records mix patch-level entries (`3.8.10`) with a minor-level one (`3.12`, CI's
pin, whose run log needs admin rights) and a VM on `3.12.7` must find it.

Rejected: a bare yes/no. It collapses "the suite has never run here" and "we
could not check", which is the exact confusion D030 was written about, and it is
the confusion this very report had already made once. Rejected: treating a missing
record as an unexercised VM, because it would blame a machine for a missing file.
Rejected: dropping the entry's `scope`, which makes a version that ran 173 tests
look identical to one that has run all 373. Rejected: making `doctor` *fail* on
an unexercised version — a VM with an unusual interpreter can still do the work,
and `doctor`'s job is to report, not to refuse.

Falsified four ways before it was trusted, per D025: a comparison that always
said `exercised` (3 failures), a missing record read as `unexercised` (5), a
summary dropping the record name (2), and `doctor` not reporting the comparison
at all (1). The fourth is the instructive one: removing the single line in
`summarize` left every unit test of the comparison green, because the tests
exercised the module rather than the report a reader sees.

Consequence: [`doctor.md`](docs/operations/doctor.md) states the four states and
their ceilings, and the two records' scopes were updated to name the tests they
have now run — a stale scope is the same defect in the opposite direction. The
ceiling is written down rather than implied: `exercised` means a run happened,
not that the version is supported, and no interpreter between 3.8 and 3.12 has
ever run this suite.
