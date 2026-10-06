<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- task-meta
id: T-0081
status: open
created: 2026-10-06
-->

# T-0081 — Measure what happened to E012's 1401 public need statements

## Goal

Measure whether the reply subtree of the need corpus carries a serving signal no
channel this mission owns has read, and whether the needs nobody answered are a
usable candidate population

## Why this matters

The mission's only demand-side asset is 1401 Hacker News comments shaped like "is
there a tool that X", carrying 1250 distinct requesters. It has been used only as
a bag of problem statements: F029 screened 50 and 0 survived; F039 showed the
corpus cannot express need-level recurrence. Nobody measured **what happened to
those statements**. Each is a live comment whose own thread was asked the same
question at the same moment and answered in public — contemporaneous,
demand-side, made by practitioners, which is what every corpus and registry the
mission has searched is not. The result decides whether this corpus is a
population whose requests were adjudicated, or 1401 rows.

## Preconditions

Unauthenticated public HN endpoints only, no token. A refused answer is kept
apart from a zero. Gates declared in `EXPERIMENTS/021-need-statement-response/PROTOCOL.md`
before any count on the population was read.

## Steps

1. Declare hypotheses, the load-bearing kill alternative, controls and gates in
   `EXPERIMENTS/021-need-statement-response/PROTOCOL.md` before the first fetch.
2. Calibrate the reply-structure instrument against a second API and record where
   it disagrees (`calibration.py`), rather than trusting one endpoint's subtree.
3. Capture every comment of all 1276 parent stories; reconstruct each need's
   subtree from `parent_id` edges; treat every other comment in those stories as
   the matched control.
4. Evaluate the gates in `stats.py`, evaluate the residual by hand in
   `read_silent.py`, and report what the read found rather than what it was
   expected to find.

## Acceptance criteria

Both declared gate arms answered from `results.json`, the control arm's coverage
reported, the residual read and characterised, and F060 recorded or its ceiling
stated.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
```

## Rollback

The capture is gitignored and rebuilt by `capture.py`; its record is
`EXPERIMENTS/021-need-statement-response/raw/MANIFEST.json`. Removing the
experiment directory removes the experiment.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**Outcome (2026-10-06).** The kill gate fired on three independent estimators:
needs are answered at 1.235× the matched control rate against a bar of 1.5
declared in advance, so attention to a need is not distinguishable from position
in a thread. The finding that changes a decision: **0 of 1391 needs drew a link to
a host new to its thread**, and **1 of 794 requesters replied again** — so the
public record of responding to a need carries no outcome signal, and item 0's
proposed axis cannot be measured off the thread the request was made in. Recorded
as F060.