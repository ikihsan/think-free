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