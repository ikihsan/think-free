<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Decision log

Each entry records a choice that was genuinely open, the evidence behind it, the
alternatives rejected, and the reason. Decisions that constrain later work
belong here; ordinary edits do not.

## D001 — Clean research workspace (2026-10-03)

Observed: `/home/ihsan/Works/think-free` was empty and outside any Git
repository. Initialize a dedicated repository there; no worktree of an unrelated
project is needed. No prior personal or project memories are consulted.

## D002 — Independent investigations before commitment (2026-10-03)

Use six isolated reports in two waves of three workers, with fresh contexts and
separate files. Do not share hypotheses until all initial reports are complete.
This provides procedural independence, not independence of model training or
real-world validation.

## D003 — Autonomous research authority (2026-10-03)

The user explicitly delegates local design, coding, testing, research, and
reversible experimentation and asks not to choose among weak concepts.
Therefore routine design approval gates in generic workflow skills are
superseded by this mission. Designs and falsification criteria are still
documented and reviewed. Purchases, secret exposure, destructive external
actions, and commitments beyond actual permissions remain gated.

## D004 — One repository, zoned, with a public manifest (2026-10-03)

Observed: the mission's durable records and any future product would share one
repository. Alternatives considered: two repositories from the start; a single
flat repository with everything public.

Decision: one repository, zoned by directory, with `RELEASE-MANIFEST.md`
declaring an explicit allowlist of public paths. No wildcard: a path not listed
as public is not published.

Rejected: two repositories, because session and task state would then need
duplicating or syncing across two trees for no benefit at this stage. A flat
public repository, because the front door would be dominated by operational
history that is interesting to auditors and noise to users.

Consequence: `sessions/`, `tasks/`, `RESEARCH/`, and `EXPERIMENTS/` stay internal
by default. The manifest is the single authority, so promoting a path later is
one edit rather than a restructure.

## D005 — Skills vendored in-repo, canonical in `.agents/skills` (2026-10-03)

Observed: `.agents/skills/` is the cross-agent convention read by Codex, Gemini,
Cursor, and OpenCode. Claude Code reads only `.claude/skills/`, and its
documentation states that a skill folder may be a symlink to a directory
elsewhere on disk. OpenCode reads both locations.

Decision: canonical skill files live in `.agents/skills/<name>/SKILL.md`;
`.claude/skills/<name>` is a per-skill symlink to `../../.agents/skills/<name>`.
No agent installation step is required, so a fresh clone works in every
supported agent.

Rejected: symlinking the whole `skills/` directory, because Codex writes internal
files there. Duplicating real files in both trees, because the two copies would
drift silently. Relying on a plugin marketplace, because that reintroduces the
install step the user asked to remove.

## D006 — Vendored content exempt from the line cap, but reported (2026-10-03)

Observed: superpowers v6.2.0 contains five Markdown files over 300 lines, up to
1150. Splitting them would break byte-identity with upstream and make updates
manual.

Decision: vendored skills are exempt from the 300-line cap, declared per path in
`vendor/MANIFEST.md`, and every exempt file is reported by `origin doc lint` as an
`info` line with its line count. All repository-authored files remain capped.

Rejected: splitting vendored files, because diffability against upstream matters
more than a uniform rule. Silently exempting them, because an invisible exception
becomes an invisible norm.

## D007 — One event file per session, not a global log (2026-10-03)

Observed: the intended execution model is several VMs claiming tasks from the same
git repository. A single append-only `sessions/events.jsonl` would produce a merge
conflict on every concurrent run, because append-only lines conflict as soon as
two branches both append.

Decision: each session writes `sessions/<id>/events.jsonl` inside its own
directory. `sessions/INDEX.md` is generated and may need rebuilding after a
merge, which is expected rather than corruption.

Rejected: a global log, which is the obvious design and the wrong one here. One
file per agent rather than per session, because a session is the unit that is
recovered and reconciled.

## D008 — Two secret policies, by exposure type (2026-10-03)

Decision: an artifact matching a credential pattern is **refused** and the command
fails, because the file itself is the exposure and redacting it would corrupt the
artifact. Captured command output is **redacted** before it reaches disk, because
losing evidence is worse than masking a token, and the redaction is recorded as an
event. Terminal output is not redacted, because suppressing it would hide command
failures.

Reasoning: the two cases have opposite failure costs. One risks a permanent
secret in git history; the other risks losing the only record of what a command
printed.

## D009 — Documentation gates enforced by lint, not by review (2026-10-03)

Observed: 113 lint violations appeared the first time the rules were applied to
this repository, including broken links written by hand, missing metadata on
pre-existing documents, and three source modules over the cap.

Decision: enforce the cap, metadata, link resolution, orphan status, and generated
freshness in `origin doc lint`, wired into `preflight` and CI. Documented
exemptions are declared in `vendor/MANIFEST.md`, never inline.

Reasoning: a rule an agent can forget is not a rule. The first lint run found more
real defects than review had, which is the argument for automating the check rather
than trusting prose.

## D010 — State folding: E001's outcome recorded, not deferred (2026-10-03)

Observed: the interrupted session left `EXPERIMENTS/001-photo-baseline/results.json`
with a passing run and a `first-failure.json` marked "diagnosis in progress", and no
decision written to `HYPOTHESES.md` or `FAILURES.md`.

Decision: record the E001 result, classify the earlier parser failure as an
implementation failure rather than a hypothesis failure, and write both into the
mission records now, rather than leaving them for a later session.

Reasoning: an experiment whose result is not in the record will be re-run or
misread, and the cost of writing it down is minutes.

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
