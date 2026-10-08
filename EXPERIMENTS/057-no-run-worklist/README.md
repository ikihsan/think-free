<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E057 — the population gate for the "no-run worklist" idea

`observed` 2026-10-08, session 2026-10-08-005, VM `instance-20260717-0944`,
Python 3.8.10. Public unauthenticated GitHub issue search, 10 requests,
`raw/requests.jsonl` and `raw/requests-2.jsonl` hold every request, its HTTP
status and its body. Scripts: [`harvest.py`](harvest.py),
[`harvest2.py`](harvest2.py). Reproduce:

```bash
python3 EXPERIMENTS/057-no-run-worklist/harvest.py
python3 EXPERIMENTS/057-no-run-worklist/harvest2.py
```

## Question

The session's declared goal was: *measure whether a project's own tests, read
statically, locate the code a real test run reports unexercised, and build a
no-run worklist prototype if they agree.* Two separate things have to be true
before a prototype is worth writing — a requester must want the substitute for
running the suite, and a static read must be able to substitute. D077 orders the
first to be read out of the evidence before anything is built to measure the
second, so this experiment is the first gate and the mechanism gate was not run.

**Declared kill gate, before any row was read:** if 0 of the 30 rows in each of
the two trackers that own this vocabulary (`coveragepy/coveragepy` and
`jendrikseipp/vulture`) state the declared need — *tell me which code no test
exercises, without running the suite* — the population is not observed and no
prototype is built.

## Result: the gate fired. 0 of 30, 0 of 1, 0 of 13, 0 of 30.

| arm | query | HTTP | `total_count` | rows read | rows stating the need |
|---|---|---|---|---|---|
| inc:coveragepy | `repo:coveragepy/coveragepy is:issue "without running"` | 200 | 32 | 30 of 32 | **0** |
| inc:vulture | `repo:jendrikseipp/vulture is:issue "without running"` | 200 | 1 | 1 of 1 | **0** |
| inc:pytest-cov | `repo:pytest-dev/pytest-cov is:issue "without running"` | 200 | 13 | 13 of 13 | **0** |
| inc:coveragepy (part 1, misspelled) | `repo:nedbat/coveragepy …` | **422** | — | **0** | no observation |
| inc:vulture (part 1, misspelled) | `repo:jendriksegers/vulture …` | **422** | — | **0** | no observation |
| voc:static-untested | `is:issue "without running the tests" untested` | 200 | 177 | 30 of 177 | **0** |
| voc:coverage-no-run | `is:issue "coverage" "without running the tests"` | 200 | 1217 | 30 of 1217 | **0** |
| voc:never-called | `is:issue "never called" "statically"` | 200 | 1683 | 30 of 1683 | **0** |
| voc:static-dead-code | `is:issue "find" "dead code" "statically"` | 200 | 1483 | 30 of 1483 | **0** |
| voc:no-executed-tests | disjunction, see below | 200 | 202343 | discarded | — |

## What the 30 `coveragepy` rows actually are

Every one is about coverage **at a moment when it ran**: lines that were
executed and recorded as missed (redis/asyncio #1853450777, aiohttp on 3.14
#3686569189, `concurrency=multiprocessing` and coroutines #1625344395, #335128585,
multiline comprehensions under pytest rewriting #335128664, dotted `--source`
#5703691955, #396287038, #2523798729), performance (5× #2789795029, 20× on PyPy
#4232599782, 77× with `Decimal` #1163067308, 13 s startup #2550030930,
#1065935311, #1518806667, #335128316), crashes and compatibility
(#3133996501, #877597472, #475545874, #1065441940, #393765327), and one
scoping request (#2211282948).

**#2211282948 is the closest row in the population and it is answered.** *Want
to get coverage for 3rd party dependencies' code used by my project* — 10
comments. The requester wants to know which lines of a dependency their own code
reaches. The answer is to run coverage with `--source` pointed at site-packages:
they *do* run the suite, and the missing piece is a config flag. That is the
opposite of the declared need and it is served.

`vulture`'s single row (#5219327606, *Add liveness_primer as a blast radius CI
job*) asks for the **diff of findings between two versions** over a corpus, not
for unexercised code without a run. All 13 `pytest-cov` rows are coverage being
wrong or slow under `xdist` and `multiprocessing`.

The vocabulary arms are the weak evidence here and are reported as such: 30 rows
read out of 177, 1217, 1683 and 1483, i.e. 16.9 % down to 2.0 %. Reading them,
the phrase *"without running the tests"* is overwhelmingly used to mean **in
CI, rather than on my laptop** — `sip-bridge has 125 unit tests and no CI job
runs them`, *The release workflow publishes without running lint, typecheck or
tests*, *No tests run in CI; conformance validators and spec data are
unverified*. That is a **different difficulty with a different remedy**: no test
command was invoked, so a detector attached to a command that exits on "zero
tests executed" is silent in every one of those rows.

## Two instrument defects, one of them live and near-fatal

1. **Two of ten arms produced no observation, and nothing in the output said so
   except the recorded HTTP status.** `nedbat/coveragepy` 301-redirects to
   `coveragepy/coveragepy` and `jendriksegers/vulture` does not exist (it is
   `jendrikseipp/vulture`, 4835 stars), so GitHub answered **422** and the arm
   returned zero items. Zero items from a 422 and zero items from a real
   negative are the same value in the same field. Had the readout counted items
   and not statuses, this experiment would have reported **0 of 7 arms found
   anything** where the truth is **2 arms never ran** — a null recorded as a
   zero, on the arms that were carrying the most weight.
2. **The tenth arm was discarded rather than reported as a null.** The
   `voc:no-executed-tests` query contains an `OR`; GitHub returned
   `total_count = 202343`, which is a query with no discriminating power rather
   than a population. It is kept in the raw file and excluded from the table's
   conclusions, not counted as a fifth zero.

**E056, two days ago, is the same defect in this repository's own record**: its
results table has three rows, its text says *pre-commit and mypy runs timed out;
partial evidence only*, and the verdict (*No observable drift population at this
sample*) is stated over five packages. That verdict may well be right. It was
reached on three of five arms and the reader is told the denominator was five.

## What this closes, and what it does not

- **Closed:** the declared goal's prototype condition. *"If they agree"* — they
  do not exist, so the condition is false and no prototype was written. The
  candidate is not opened.
- **Closed:** the retrieval route for this idea. The two trackers whose
  vocabulary owns the need return 0 of 44 read rows for it.
- **Not closed:** that people want coverage, or that coverage is hard to get.
  The 30 `coveragepy` rows are a real, recurring, unsolved population — coverage
  that under-reports lines that ran is a genuine and current problem. This
  experiment says nothing about it.
- **Not closed:** that a static read of tests cannot substitute for a coverage
  run. That is the mechanism gate, which D077 placed second and this experiment
  did not run.
- **Ceiling, stated:** one platform, one retrieval route, unauthenticated
  search with a 30-row page and no second coder. F049 already measured that 167
  of 241 shipped features were released *before* anyone complained, so an issue
  tracker under-represents real need by construction. This result closes the
  population **as stated, in these two trackers**, and nothing wider.

## The rule this buys

An arm that produced no observation is a **missing observation**, and a missing
observation never enters a denominator and never becomes a zero. It is stated
here because it was nearly lost inside this experiment, and because this
repository's record already contains one verdict written over three of five arms
(F087, E056). See `FAILURES-findings-32.md` F088.