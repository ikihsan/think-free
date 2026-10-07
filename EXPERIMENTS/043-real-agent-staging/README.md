<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-07
-->

# E043 — real coding agents on real staging tasks

`observed` 2026-10-07, session 2026-10-07-001, VM `instance-20260717-0944`, git 2.25.1,
Python 3.8.10. Harness in this directory: `build.py`, `check_oracle.py`,
`prepare.py`, `score.py`. Six real agent runs, no simulation.

**Verdict: real coding agents solve line-addressable partial staging correctly
and without `stg`, 3 of 3 with no tool present and 3 of 3 with `stg` on PATH —
and 2 of the 3 that had it declined to use it. The candidate's
agent-usability advantage is not observed in the population the demand
evidence names.**

## What this was for

E041 and E042 both concluded that `stg`'s differentiator is *packaging*: a
callable CLI instead of ~180 lines of git plumbing a caller must write and
maintain. E042 says in its own design document, line 38:

> Since we can't run a real coding agent, we simulate the agent's decision process.

That simulation is where the surviving justification came from, and it also
is where the "~180 lines" figure came from: a baseline written by someone who
had already read `stg`'s selector and reimplemented it. So the load-bearing
claim had never met an agent. This experiment runs the agents.

## Question, arms, and oracle

**Question:** given a real repository with a real dirty working tree and the
instruction *"stage ONLY the change on line N; leave every other change
unstaged"*, what does a coding agent actually do, and does `stg` change the
outcome?

- **Arm `nostg`** — no tool offered. Three scenarios.
- **Arm `stg`** — `stg` genuinely on `PATH`, named in the prompt as available
  and not required. Three scenarios.

Scenarios, each a fresh `git init` repository over one committed `app.py`:

| scenario | working tree | requested |
|---|---|---|
| adjacent-modifications | lines 6 **and** 7 both modified, one hunk | stage line 7 only |
| two-line-insertion | lines 3 **and** 4 both inserted, one hunk | stage line 3 only |
| one-edit-among-three | edits at lines 1, 15, 19 | stage line 19 only |

The oracle is `.expected_index`, written **by hand** in `build.py` from the
scenario description. It is hoisted into `oracle/` and removed from every
trial directory, so an agent cannot diff against it. Scored by byte
comparison of `git show :app.py` against that file.

**The oracle was checked before any agent ran** (`check_oracle.py`, 4 routes ×
3 scenarios): `stage-all` → `wrong`, `stage-none` → `wrong`, `diff-filter` →
`wrong` on both adjacent cases and `exact` on the easy one, `stg` → `exact`
on all three. A scorer that cannot separate these cannot report a result.

## Observed

| arm | scenario | verdict | used `stg` |
|---|---|---|---|
| nostg | adjacent-modifications | **exact** | n/a |
| nostg | two-line-insertion | **exact** | n/a |
| nostg | one-edit-among-three | **exact** | n/a |
| stg | adjacent-modifications | **exact** | yes |
| stg | two-line-insertion | **exact** | **no** |
| stg | one-edit-among-three | **exact** | **no** |

**6 of 6 exact. 3 of 3 exact in the arm with no tool at all.** No trial left a
stray file behind, none committed, all left the other changes unstaged.

Every `nostg` agent arrived at the same route independently, without being
told it: read `git diff`, **hand-write a minimal patch**, and
`git apply --cached`. Three of the six did the dry run first
(`--check` / dry-run-then-apply); two of the three that built a patch file hit
patch-malformedness first and were caught by their own check.

Two agents independently flagged the same hazard unprompted: `git apply` is
all-or-nothing, so a malformed hunk header is a hard error rather than a
silent partial stage. One noted the index state is not independently
runnable — staging half of a pair leaves a tree that would break if committed
alone.

## What this closes

**F075.** The packaging advantage that kept `stg` alive after its mechanism
was falsified is not observed against the caller the demand evidence names.
The population had a non-interactive route available to it and used it, at 3
of 3, in one tool call each and no code written. "1 line instead of 180" is
true and worth nothing: the 180-line figure is the cost of building a
*general* selector, and these agents did not need a general selector, they
needed one patch, which they could write because `git diff` told them what it
was.

**This does not say the task is easy.** Two things held it up. The two
adjacent scenarios are exactly the cases `git add -p`'s own split cannot
reach — an agent that had defaulted to `git add -p` would have had to fall
back anyway. And `git apply` rejected two of the six hand-built patches as
corrupt; both agents caught it with a check first, which is discipline, not
guarantee.

## Ceiling

- **Three scenarios, six runs, one agent model, one session.** This is a
  small sample of *this* population. It does not establish that agents never
  need `stg`; it establishes that the advantage is not visible here.
- All six agents are the same model with the same capabilities. Agent
  heterogeneity — weaker models, or harnesses that forbid shell heredocs — is
  untested, and is the most plausible place `stg` still wins.
- Every agent could read `git diff`. An agent that only has an edit tool and
  no diff access is a different population and is untested.
- Line numbers were handed to the agent in the prompt. An agent that has to
  *discover* which line changed is untested, and that is harder.
- The scenarios are synthetic Python; real files may be messier. `stg` is
  unaffected by that in principle, but these agents were not tested on them.
- Scored against a hand-written oracle, verified to discriminate on four
  routes. It was not checked against a second independent reader.

## The instrument, including its two failures

Both are recorded because both would have produced a wrong result.

**Contamination.** In the first pass the oracle file `.expected_index` sat
inside the trial directory. One agent read it and verified its own work
against it — `git show :app.py | diff -u .expected_index -`. That run scored
`exact` and was not evidence. Fixed by quarantining the oracle outside every
trial directory; all six reported runs are post-fix.

**The `stg` arm was not testing `stg`.** `stg` was written into an untracked
`.bin/` inside the fixture. All three agents in that arm reported
`stg: command not found`, so the arm was a second `nostg` arm — and it still
scored 6 of 6, which would have read as a clean confirmation. Fixed by
installing a real launcher into `/usr/local/bin`, with `prepare.py` now
refusing to proceed unless `stg --help` resolves. The third run of that arm
is the one that has `stg` genuinely available.

**A scorer bug that would have invented a failure.** `git show :app.py`
succeeds and returns `HEAD`'s content when nothing is staged, so
"staged nothing" and "staged the wrong thing" were the same verdict. The
untouched `stg`-arm repositories were scored `wrong`, which would have
reported a 3-of-6 failure that did not happen. Found by scoring fixtures no
agent had touched and asking why an untouched repo scored as a wrong answer.

## Next action

The candidate decision changes: **`stg` is no longer a candidate for release
on the strength of agent usability**, because that advantage was not observed
against real agents. It remains a working, correct tool — 30 of 30 on E038,
byte-identical to a hand-built index — and that is the whole claim now.

The single most useful next measurement is the one this experiment's ceiling
names first: **an agent that must discover which line changed, without being
told a line number, and with `git diff` unavailable.** That is the population
where a line-addressed interface could still pay, and it is a two-arm rerun of
this harness, not a new line of work.