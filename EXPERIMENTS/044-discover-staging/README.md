<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-07
-->

# E044 — must the agent discover the line, without `git diff`?

`observed` 2026-10-07, session 2026-10-07-002, VM `instance-20260717-0944`,
git 2.25.1, Python 3.8.10. Harness in this directory: `build.py`,
`check_oracle.py`, `prepare.py`, `score.py`. Six real agent runs, no
simulation. Fixtures are byte-identical scenarios to E043 (`build.py`
carries the same BASE and edits, and re-derives the requested line from an
anchor asserted against git's own `diff -U0`).

**Verdict: 6 of 6 exact — and the `nostg` arm went 3 of 3 under the harder
condition, crossing the pre-declared kill gate. Every agent in both arms did
the discovery by hand (read HEAD, read the working copy, compare) before any
tool was touched; in the `stg` arm `stg list` was a *confirmation* of a line
the agent had already identified, and `stg stage` was only the mechanism.
The population E043's ceiling named — an agent that must discover the line
with no diff access — does not need `stg` either, at this scale. `stg` is a
correct tool with no observed population that needs it.**

## What this was for

E043 killed `stg`'s packaging advantage for agents that are *told* a line
number and can read `git diff`: 3 of 3 solved it with no tool at all. Its
ceiling named the one population where a line-addressed interface could
still pay — **an agent that must discover which line changed, with no line
number and no diff access** (a harness that exposes file contents but not
diffs). This experiment reruns E043's harness with exactly those two
changes. It is item 0a of `STATE-next-actions.md`: the result decides
whether `stg` has any agent population left, or is a correct tool with none.

## Question, arms, and oracle

**Question:** given a real repository with a dirty working tree, a
*semantic* description of one change ("the addition of
`.decode("utf-8")`"), no line number, and `git diff` disabled, what does a
coding agent actually do — and does `stg` change the outcome?

- **Arm `nostg`** — no tool offered, `stg` asserted absent from PATH.
  Three scenarios.
- **Arm `stg`** — `stg` genuinely on `PATH` (launcher in `/usr/local/bin`,
  verified resolvable at prepare time), named in the prompt as available
  and not required. Three scenarios.

Scenarios (identical to E043): adjacent-modifications (stage line 7 of an
adjacent 6–7 modification pair), two-line-insertion (stage only
`import json` of an adjacent import pair), one-edit-among-three (stage the
`sys.argv[-1]` edit among three scattered edits).

The oracle is hand-written in `build.py`, quarantined in `oracle/` —
**outside** the fixture directories, which now contain only `app.py` and
`.git` (E043 left the answer one `ls ..` away from the trial; `prepare.py`
asserts a trial holds nothing else). Scored by byte comparison of
`git show :app.py` against the oracle.

**The oracle was checked before any agent ran** (`check_oracle.py`, raw in
`raw/oracle-check.txt`): stage-all → `wrong` 3/3, stage-none →
`nothing_staged` 3/3, `stg` → `exact` 3/3, and a **no-diff route** —
difflib alignment of HEAD vs worktree, one hand-emitted `-U0` hunk,
`git apply --cached --unidiff-zero` — → `exact` 3/3. The last route proves
each fixture is solvable from file contents plus a line coordinate without
diff output, so an agent failure is the agent's, not the fixture's.

## The no-diff simulation and its limits

`git diff` is disabled by a policy shim (`gitbin/<trial>/git`) that refuses
any `diff` argument and logs every call with cwd, exit status, and a marker
for `stg`'s internal plumbing (the launcher sets `STG_INTERNAL=1`; the
tool's own diffing is not the agent reading a diff — that is the harness
restriction being simulated, and the candidate's exemption from it is
exactly the hypothesis under test). The agent is told not to bypass the
wrapper; the shim log is the compliance record — an agent reporting git
commands the log does not show went around it, and that run is not
evidence. This is a cooperative-agent simulation of a restricted harness,
not an adversarial sandbox: `git stash show -p`-style routes exist and are
not blocked, only logged.

## Kill gate, declared before the runs

- **Claim dead** — `stg` has no remaining agent population worth a
  release — if the `nostg` arm scores `exact` on **≥ 2 of 3** scenarios:
  agents recover the line and stage it without diff and without the tool,
  at E043-like rates, under the harder condition.
- **Claim survives, narrower** — the discovery-and-no-diff population is
  real — if `nostg` scores `exact` on **≤ 1 of 3** AND `stg` scores
  `exact` on **≥ 2 of 3** with the tool genuinely exercised (shim log or
  report shows `stg` invocations; D074 requires the treatment arm to be
  checked to have exercised the tool).
- Anything else (both arms fail, or `stg` wins without being used) is an
  instrument suspicion, not a verdict: inspect first.

Secondary measures: git-call counts and nonzero exits from the shim log,
and discovery accuracy (did the agent name the right line even when staging
failed).

## Observed

| arm | scenario | verdict | git calls | failed calls | used `stg` |
|---|---|---|---|---|---|
| nostg | adjacent-modifications | **exact** | 7 | 0 | n/a |
| nostg | two-line-insertion | **exact** | 12 | 2 | n/a |
| nostg | one-edit-among-three | **exact** | 10 | 0 | n/a |
| stg | adjacent-modifications | **exact** | 12 (6 internal) | 0 | yes |
| stg | two-line-insertion | **exact** | 11 (6 internal) | 0 | yes |
| stg | one-edit-among-three | **exact** | 11 (6 internal) | 0 | yes |

Raw: `raw/final-scores.json`, per-trial agent reports in
`raw/<scenario>-<arm>.report.md`, shim logs in `oracle/shim-*.log`.

**6 of 6 exact; 3 of 3 with no tool, no line number, and no diff.** Every
one of the six agents opened with the same discovery move: `git show
HEAD:app.py` against `cat -n app.py`, compared by eye, and named the correct
line on the first attempt, in all three scenarios. Discovery — the work the
surviving claim said needed an interface — was done by hand in 20 seconds in
both arms. In the `stg` arm all three agents then ran `stg list` and
reported it *confirmed* the line they had already identified; the tool's
coordinate listing answered a question they had already answered.

The `nostg` arm split into two routes again, and added one E043 did not
see: two agents hand-built context patches (one failed first — git 2.25.1
would not anchor a leading-context-only hunk — diagnosed with `--check`,
then succeeded), and the third **never wrote a patch at all**: it built the
intended staged content with `sed` over `git show HEAD:app.py`, wrote it as
a blob with `git hash-object -w`, and pointed the index at it with
`git update-index --cacheinfo`. That agent also declined `git add -p`
deliberately, because its UI displays diff hunks and would have broken the
policy.

Compliance held in all six runs: the shim log shows **one** agent-facing
`git diff --cached --stat`, refused, in `adjacent-modifications-stg`; the
agent produced no diff output and complied afterwards. That attempt is
absent from the agent's own report — **the shim log, not the self-report,
is the complete compliance record.**

## What this closes

**The last named population.** E043 closed agents that are *told* a line;
this closes agents that must *discover* the line without diff access, at
this scale. Both arms at 3 of 3 is not a marginal call: the gap the tool
fills was performed for free, by hand, by every agent, including the three
that had the tool. `stg` remains a correct tool — exact whenever used here,
30 of 30 on E038's matrix — and that is now the whole claim, with every
population the demand evidence or the experiment ceilings named tested and
negative.

## Ceiling

- **Scale is the honest boundary of this result.** The scenarios are
  20-line files with 2–3 edits; discovery-by-eye is free at that size. A
  2,000-line file with 40 scattered edits is a different task, and no
  requester in the demand evidence (F064's named issues) describes it. A
  negative result here closes the small-file discover population only.
- One model, one VM, one session — agent heterogeneity (weaker models,
  harnesses without shell heredocs) remains untested, as in E043.
- The no-diff simulation is cooperative, not adversarial: `git stash show
  -p`-style routes exist and are only logged, not blocked. No agent probed
  them.
- `stg`'s own internal `git diff` passed the shim by design
  (`STG_INTERNAL`) — the tool's exemption from the agent's restriction is
  the hypothesis under test, not a leak.
