<!-- origin-meta
owner: FAILURES.md
status: active
last-verified: 2026-10-07
-->

# Findings 29 — a candidate's survival claim was never run against a real caller

`observed` 2026-10-07, session 2026-10-07-001, VM `instance-20260717-0944`.
Evidence: [`EXPERIMENTS/043-real-agent-staging/`](EXPERIMENTS/043-real-agent-staging/README.md).

## F075 — real coding agents stage a single line exactly, without `stg`, and mostly ignore it when it is installed

`stg` survived three experiments (E040, E041, E042) on a single claim: the
*mechanism* is replicable, but the *packaging* is the differentiator, because
a caller writes 1 line instead of ~180. E042 states in its design document
that it simulated the agent, and the ~180 figure is a baseline written by
someone who had already read `stg`'s own selector and reimplemented it.

E043 ran six real agents on six real repositories — one committed `app.py`,
a real dirty working tree, the instruction *"stage ONLY the change on line N;
leave every other change unstaged"* — three with no tool offered and three
with `stg` genuinely on `PATH`.

**Result: 6 of 6 exact, and 3 of 3 exact with no tool at all. 2 of the 3 that
had `stg` on `PATH` declined to use it.** Every `nostg` agent independently
converged on the same route: `git diff`, hand-write a minimal patch,
`git apply --cached`.

**What this closes.** The packaging advantage is not observed against the
caller the demand evidence names (`mcp-multi-root-git#3`, "no way to stage
lines 1-50 separately"). "1 line instead of 180" is true and worth nothing:
**180 lines is the cost of building a general selector, and these agents did
not need a general selector** — they needed one patch, and `git diff` told
them what it was.

**What it does not close.** The task is not easy. The two adjacent scenarios
are precisely the cases `git add -p`'s own split cannot reach, and `git apply`
rejected 2 of the 6 hand-built patches as corrupt — both caught by the agent's
own dry run, which is discipline rather than guarantee. See the ceiling in the
experiment record: three scenarios, one model, line numbers supplied, and
`git diff` available to every agent.

## The two instrument failures, both of which would have produced a wrong result

**The `stg` arm did not test `stg`.** The tool was written into an untracked
`.bin/` inside the fixture. All three agents in that arm reported
`stg: command not found`. The arm was therefore a second `nostg` arm — **and
it still scored 6 of 6 overall, which would have read as a clean confirmation
of the candidate.** Fixed by installing a real launcher into `/usr/local/bin`,
with `prepare.py` refusing to proceed unless `stg --help` resolves. This is the
same shape as F073 (an arm that produced a clean table because it was not
running the thing under test) and the first time here that a *control* arm
failed open rather than producing an obvious zero.

**A scorer bug that would have invented a failure.** `git show :app.py`
succeeds and returns `HEAD`'s content when nothing is staged, so "staged
nothing" and "staged the wrong thing" collapsed to one verdict. The untouched
`stg`-arm repositories scored `wrong`, reporting a 3-of-6 failure that never
happened. Found by scoring fixtures no agent had touched and asking why an
untouched repository scored as a wrong answer.

**Contamination, caught by the agents' own honesty.** In the first pass the
oracle file sat inside the trial directory; one agent verified its work by
diffing against it and scored `exact`. That run was discarded. The oracle now
lives outside every trial directory.

## The transferable part

**A survival claim is not a survival claim until it has met a real caller.**
E040, E041 and E042 each measured `stg` against a route, and the route was
always something the experiment had written. The gate each declared was
satisfied by a *simulation* of the population, and the simulation's central
quantity — 180 lines — was inherited from the artifact under test. Three
consecutive experiments agreed with each other because they shared a premise,
not because the premise was checked.

The check cost one afternoon and six agent runs, and it is the first thing
that could have been run at any point in the candidate's life. **When a
candidate's justification names a caller, that caller should be the arm that
runs, before the candidate is called validated** — and the instrument must be
checked for whether the arm is actually exercising the tool, which here it was
not, for three runs in a row.