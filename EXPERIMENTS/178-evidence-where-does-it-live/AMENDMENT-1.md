<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# AMENDMENT-1 — G0d's vocabulary loses two of E177's six `kind` values, because two of them are ordinary English here

**Declared:** 2026-10-17, **before the first fetch in this experiment** and
before the reader saw any row.

## What changed

Control G0d's inherited-vocabulary list drops `configuration` and `data_value`.
Both are two of E177's six `kind` values (`labels.json`: configuration 6,
data_value 4) and both are ordinary words in this domain: "configuration" is a
noun that appears in exactly the config-shaped questions this population is full
of, and `data_value` does not occur in the population at all.

The control fired on **4 of the 46** rows before anything was fetched, all four
on the word "configuration" in a question body or a key answer.

## Why the control was wrong rather than the inputs

A blindness control has to distinguish *the label vocabulary leaking into the
reader's input* from *the document's own words*. `EVID`, `SELF`, `"arm"`,
`"kind"`, `"why"`, `missing_evidence`, `not_reached` and `upstream_source` are
not English and stay in the list. A whole-word grep for `why` and `kind` also
fires on six rows ("that's why", "kind of"), which is the same failure in the
opposite direction and is why this control checks **the JSON key names and the
arm labels**, not the words.

Keeping `configuration` in the list would have meant either editing the reader
inputs to remove an English word from a bug report, or switching off a control
that fires on the population it is meant to protect. Both were worse than
narrowing the vocabulary and saying so.

## What this costs the control

`configuration` and `data_value` can no longer be detected if they leak. They
were the two kind values that a reader could plausibly have been anchored by if
it had seen `labels.json`, so this is a real loss. It is bounded: **no reader
input contains any of the ten remaining vocabulary terms, no reader input
contains any field name, and the reader is given one file per row with no
neighbouring row in it** (`ANY_QID` check), so a leak would have to be one
reader's memory of another reader's batch rather than something in the bytes.

`controls.py` reports the rows each dropped term would have flagged, every run,
so the number of rows this control can no longer see is visible rather than
assumed.