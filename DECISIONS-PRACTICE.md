# Decisions — recording, verifying, publishing, and gating work

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

Decisions **D011 onwards**. Each entry records a choice that was genuinely open,
the evidence behind it, the alternatives rejected, and the reason. Decisions that
constrain later work belong here; ordinary edits do not.

**Invariant:** every entry in this file governs *how work is recorded, checked,
published, or gated* — the tooling and the rules a session must satisfy. If a
decision can be restated as "what the mission is, what the workspace is, or what
counts as evidence", it belongs in
[`DECISIONS-FOUNDATION.md`](DECISIONS-FOUNDATION.md) instead. The index is
[`DECISIONS.md`](DECISIONS.md).

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

## D019 — A candidate may not be implemented until its witness is run (2026-10-03)

Observed: `HYPOTHESES.md` carried "information-sufficiency witness" prose for
three candidates but none had been executed, while the A1 masking experiment was
already being deepened.

Decision: run the witness for every held candidate before any implementation.
A passive candidate that cannot separate two realities with identical inputs and
different outputs is information-insufficient and must narrow its input or permit
refusal; an active candidate fails only when *no* permitted observation
separates the pair. Results are recorded per candidate in `HYPOTHESES.md`, and a
disproved input set is recorded in `FAILURES.md`.

Rejected: treating the witness as a formality after the fact, because a gate
written after seeing results is a rationalisation; and applying it only to the
candidate then in focus, because the two others were cheap to screen in the same
session and one (knitting) failed.

Consequence: the knitting candidate's input set must add loop orientation or
refuse (F007); the sidewalk and ventilation candidates may proceed to their
behavioural experiments under their stated scope conditions.

## D020 — Screen candidates by whether a surviving result changes a build decision (2026-10-03)

Observed: `STATE.md` asked for the six sealed investigations to be compared with
E's and F's criteria as a screen. Applying them literally produced nothing — F's
C1–C6 describe a built repository (a runnable README, one-command install, CI
coverage) and score **not applicable** against six unimplemented candidates, so
they discriminate nothing. Applying E's entry criterion alone also failed to
separate the software candidates: E1 and E3 both have killing experiments much
smaller than the argument for them.

Decision: screen on three questions in order, and require all three before an
experiment is scheduled. (1) Is the experiment that could kill the candidate
smaller than the argument for keeping it (E)? (2) What does a user receive, in
how many steps, and at what comprehension cost (F's time-to-first-value, not its
checklist)? (3) **If the gate passes, what gets built** — a nameable mechanism
with a nameable owner, or nothing? Question 3 is the discriminator E and F left
out, and it is the one that killed E1: jitter is in every modern client library,
so a passing simulator would confirm a 2015 blog post and change no build
decision.

Consequence: F's C1–C6 stay a **gate at stage D**, applied to a repository that
exists, and are not cited as a candidate screen. E1 is not run despite being the
cheapest experiment in the repository. The screen itself, with the full
per-candidate tables and the ranked next actions, is
[`RESEARCH/SYNTHESIS.md`](RESEARCH/SYNTHESIS.md).

Rejected: applying C1–C6 as written and reporting six "not applicable" rows as
the result, because that is a screen that cannot fail and therefore teaches
nothing; and ranking by cheapness alone, because the cheapest experiment here
(E1) is also the one whose outcome changes nothing.

## D021 — An experiment is judged by the setting that can fail, not the best one (2026-10-03)

Observed: the interrupted T-0011 draft defined its "bounded" planner by taking the
product of every per-neighbourhood candidate. Measured, that product equals the
oracle's `2**|errors|` on every T-0010 case, so its `all_optimal = true` was a
tautology of the decomposition rather than a result. The replacement planner
produces two settings that are also optimal — and two of them (`cap=1, beam=2`,
`cap=2, beam=4`) turn out to evaluate exactly the oracle's `2**|errors|`
combinations, because keeping a second candidate per chunk is exhaustive search
wearing the planner's clothes.

Decision: report the whole sweep, name the setting that fails and the settings
that only look good, and count work as patch subsets enumerated **plus**
combinations evaluated, because the combination phase is where the cost hides.
A kill gate must name the setting it applies to. Settings that turn out to
enumerate the baseline's own search space are labelled as such in the results and
never counted as evidence for the planner under test.

Rejected: reporting only the headline setting, because a reader would then take
the best number as the planner's quality and never learn that the cheap settings
fail; and "the planner is optimal, so it works", because optimality that follows
from the model's structure is a check on the implementation, not a discovery.

Consequence: `EXPERIMENTS/005-knitting-bounded-search/README.md` states the cap
and beam sweep, the family-by-family work ratios (1.28x *worse* than the oracle
on T-0010's own cases), and the explicit verdict that "bounded neighbourhood" is
not an efficiency claim at this scale. The chunk cap is recorded as the failure
boundary: whole neighbourhoods are exact, per-error chunks are not.

## D022 — A kill-gate condition naming "prior art" must name which claim it gates (2026-10-03)

Observed: the knitting candidate's kill gate read "abandon the
algorithmic-advantage claim if existing graph tooling already supplies equivalent
intervention sequences". One sentence, two different claims: whether a *knitting*
tool already does this, and whether the *algorithm* is new. T-0015 answered both,
in opposite directions — no tool was found, and the mechanism has been published
since 2007 — so a single verdict would have been wrong whichever way it went, and
a later session reading only the verdict could not tell which claim died.

Decision: when a kill gate's condition contains the words prior art, no novelty,
or differentiated, the report must answer **one row per claim inside the
condition**, each with its own result and its own confidence label. A condition
whose reading is ambiguous is split in the record, not resolved silently by the
agent running it.

Rejected: picking the reading that made the candidate look best, because that is
the failure the gate exists to prevent; and rewriting the kill gate after seeing
the result, which turns a predeclared gate into a rationalisation (the D020
reasoning in a new place).

Consequence: `RESEARCH/PRIOR-ART-KNITTING.md` carries the two-row verdict table,
the algorithmic-advantage claim is recorded as `FAILURES.md` F009, and the
surviving physical question (Stage B) is stated as the only thing left for the
candidate. Any future kill gate that gates on prior art should be written with
its claims separated in the first place.

## D023 — Honour the declared gate metric; record that it cannot fail separately (2026-10-03)

Observed: E3's predeclared kill gate is "below 5% non-normalized wheel
timestamps, E3 is a weak lead". `EXPERIMENTS/007-build-timestamps/` measured
0.965 on that metric (T-0013), and the same run computed two stricter fractions
— 0.670 of wheels with disagreeing entry dates, 0.145 spanning an hour or more —
which the earlier interrupted run had printed first. 1980-01-01 appears in a wheel
only when the builder pins the DOS epoch, which almost nothing does, so the
declared metric is met by any ecosystem that does not pin, whether or not it is
reproducible. Zero of 200 wheels carried a unix-epoch string in `METADATA` or
`RECORD`, so the mechanism's stated assumption is half false as well.

Decision: the verdict is taken on the metric the report declared, not on the
stricter one the code happened to compute first, and the stricter fractions are
reported beside it as lower bounds that cannot overrule it. A gate whose metric
cannot fail is recorded as its own finding (`FAILURES.md` F010) with the
follow-up measurement that could decide the claim (T-0017), rather than fixed by
silently swapping in a metric chosen after seeing the data.

Rejected: (a) ruling on the stricter metric, because a gate is a commitment made
before the data and choosing the metric once the numbers exist makes the gate a
rationalisation; (b) ruling the gate invalid and declaring the experiment
uninformative, which discards a real prevalence measurement because the stated
metric is weak; (c) reporting only the favourable 0.965, which is the failure this
decision exists to prevent — the same shape of near-vacuous gate as F008.

Consequence: the census reports `lead-survives` and F010 explains why that
verdict licenses nothing yet. The attribution measurement is T-0017
(`EXPERIMENTS/008-build-timestamp-attribution/`).
