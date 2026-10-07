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

## F083 — the discovery population doesn't need the tool either, and the agent's self-report is not the compliance record

`observed` 2026-10-07, session 2026-10-07-002. Evidence:
[`EXPERIMENTS/044-discover-staging/`](EXPERIMENTS/044-discover-staging/README.md).

E043's ceiling named the one population where a line-addressed interface could
still pay: an agent that must *discover* which line changed, with no line number
and no `git diff`. E044 reran E043's harness with exactly those two changes —
a semantic description of the target change, and a logging policy shim that
refuses `git diff`. Kill gate declared before the runs: `nostg` ≥ 2 of 3 exact
kills the claim.

**Result: 6 of 6 exact, and the `nostg` arm went 3 of 3.** Every agent in both
arms opened with the same move — `git show HEAD:app.py` against `cat -n
app.py`, compared by eye, correct line on the first attempt — so the work the
surviving claim said needed an interface was done by hand, in both arms, in
about twenty seconds. In the `stg` arm all three agents used the tool this
time (E043: 1 of 3), and all three reports describe `stg list` as
*confirming* a line they had already identified: the coordinate listing
answered a question they had already answered. The `nostg` arm also produced
a route no experiment here had seen: `git hash-object -w` +
`git update-index --cacheinfo`, staging the intended blob directly with **no
patch at all** — the second no-tool route in two experiments, found
independently.

**The candidate is closed.** `stg` is a correct tool — exact whenever used,
30 of 30 on E038's matrix, honest exits on E039's boundary cases — and every
population the demand evidence or any experiment's ceiling named is now
tested and negative: not agents told a line (E043), not agents who must
discover it without diff (E044). The untested cells (weaker models, no-shell
harnesses, files too large for discovery-by-eye) have no named requester in
F064's demand evidence.

**The instrument finding, and it generalises.** Compliance with the no-diff
constraint was enforced and logged at a shim on `PATH`. The log shows one
agent-facing `git diff --cached --stat`, refused, in one trial; the run
stayed valid because no diff output was produced. **That attempt appears in
no agent's self-report.** Six reports were otherwise accurate command-by
command — and still the one policy-relevant event survived only in the log.
When a constraint is part of the treatment, the enforcement point is where
compliance is measured; the subject's account of its own compliance is not
evidence of it (D078).