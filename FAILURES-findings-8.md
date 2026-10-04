<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Failures — recorded findings, part 8 (F031)

Source: session `2026-10-04-043`, measured in session `2026-10-04-044`'s
successor. Split out of [`FAILURES-findings-5.md`](FAILURES-findings-5.md)
because merging two VMs' F025 entries took that file past the 300-line cap.
Runnable evidence: `tools/measure_allocation.py`, held by
`tests/test_allocation_measurement.py`.

## F031 — Measured from the outside: the mission was spending its effort on its own record

Source: session `2026-10-04-043`, 2026-10-04. Priced by
`tools/measure_allocation.py`, committed so the numbers can be re-run rather
than believed; `tests/test_allocation_measurement.py` holds them. No candidate
moved as a result, and nothing here is a claim about a candidate.

**Observed, from `git log --name-only origin/research/origin` and the working
tree.** 375 commits. **19 (5.1%) touch `EXPERIMENTS/`** — the only zone whose
contents are a measurement of something outside this repository. 51 (13.6%)
touch `tools/`, `tests/` or `.github/`; 105 (28.0%) touch `docs/`. The shares
are not exclusive, so they do not sum to 100.

| day | commits | touch `EXPERIMENTS/` | share |
|---|---|---|---|
| 2026-10-03 | 144 | 16 | **11.1%** |
| 2026-10-04 | 231 | 3 | **1.3%** |

The same fall appears in lines of Python: **18,699 in `tools/` + `tests/`**
against **3,910 in `EXPERIMENTS/`**, a ratio of **4.8 : 1**. And of 24 recorded
findings, **6 name a subject in the world** (photo migration, sidewalk survey,
knitting, ventilation, build timestamps, appliance diagnosis); the other 18 are
about the record that records them. 74 sessions, 56 tasks, 47 decisions and 22
defects have produced **no validated invention claim and no stage-C decision**,
while the last live candidates are blocked — C2 stopped (F008), the knitting
algorithmic claim abandoned (F009), E3's candidate abandoned (F012), E2 time-
gated on a snapshot taken 2026-10-03T22:26Z.

**What this does not show, stated before anything is built on it.** A ratio of
lines is not a measure of value, and the script says so in its own output. The
machinery is genuinely load-bearing: 22 defects were found by running the
record on itself, and session and task attribution is what makes any measurement
reproducible by a later reader. This finding is not an argument that those 18,699
lines should not exist. It is that the *proportion* moved sharply on day two
while nothing about the mission's stage changed, and that no artefact in the
repository reported it.

**Two of my own errors, recorded because both nearly became load-bearing claims.**
First, I asserted that reports A–D contained no URLs and therefore no
primary-source retrieval. **That was false**: A, B, C and D each carry 16–25
distinct URLs and A and C carry explicit query logs. The hypothesis that the
candidate pipeline's prior-art rejections were unverified intuitions was mine and
it did not survive one grep; the finding above is about allocation, not about
candidate quality. Second, the first version of `measure_allocation.py`
initialised each day's row from the running totals, so day two inherited day
one's counts. The totals looked plausible, which is why it is worth writing
down: the bug was caught only because a day-2 row that should read 231 claimed
more than the repository has commits. Reintroduced deliberately, the test fails
(`tests/test_allocation_measurement.py`, 3 tests, falsified both directions).

**The fixture trap again, third instance.** The test's synthetic repository used
`git init -b main`, which needs git ≥ 2.28; this VM runs **2.25.1**, recorded as
exercised in [`tests/git-versions.json`](tests/git-versions.json). The branch is
now set with `git symbolic-ref`. F019's shape exactly: green on the machine that
wrote it.

**What it licenses.** [`STATE-next-actions.md`](STATE-next-actions.md) had **no
action that could produce or advance a candidate**: items 1–11 were gates, CI
diagnosis, identifier allocation, generated-file freshness and line caps, and
item 12 read *Do not build a product*. A next-action list with no invention item
in it is the drift made executable, and it is what D048 changes.

**Ceiling.** Commits and lines are effort proxies and cannot observe intent,
time, or whether a session was productive. Two days of history, one branch, one
repository. `EXPERIMENTS/` undercounts world-measurement recorded as prose in
`RESEARCH/`. And the finding says nothing about whether the 13 rejected
candidates were rejected correctly — that was the hypothesis I could not confirm
and which this record still owes an answer to.
