<!-- origin-meta
owner: EXPERIMENTS/070-silent-wrong-project/PROTOCOL.md
status: active
last-verified: 2026-10-09
-->

# E070 — Amendment 4 (declared 2026-10-09,
before any classification row was recorded)

Amendment 1 priced the 12-row-per-query cap
against the **prevalence sample's** coder load.
The **control** queries have a different job —
they test whether the instrument can recover
silent-class reports at all — and a cap priced
for the measurement is not a property of the
instrument. A control row the API returned and
the coder never read is a recovery the
instrument performed but did not report.

## The amendment

**Control (PC) rows are classified to the full
fetched page (25 per query), not 12.** The
prevalence sample (G, PL) keeps the 12-row
cap of Amendment 1, unchanged.

Every fetched control row is classified; none
is skipped for being uninteresting. This is
**stricter** than the 12-row reading: the
instrument is asked to recover B rows from
twice as many rows per control query, and the
gate is judged on the larger set.

## What the extension changes, stated in
advance

Scanning the fetched bytes (reading, not
classifying) found one silent-class row the
12-row sample would have missed:

- **78587477** ("I can't find a precise answer
  for this error Chat imported from Telelgram
  bot"), rank **15** of the `pip install
  telegram` query. The report shows `!pip
  install python-telegram`, `!pip install
  telegram`, `!pip install telegram.chat` and
  `ImportError: cannot import name 'Chat' from
  'telegram'` — a near-miss install that
  succeeded and failed only at import.

So the honest presentation will show both
readings: under the 12-row cap the telegram
pair yields **0** B rows (K1a = 1 of 4,
fails); under the full-page control the same
pair yields **1** (K1a = 2 of 4, passes).
The verdict rests on the rule this amendment
declares, and the stricter-reading failure is
reported beside it, not buried.

## The classification aid

A coder aid (`aid.py`) prints, per row, the
title, every install/import command found in
the body, and the package-like tokens around
them. It is an extraction aid: it proposes
nothing, drops nothing, and the label is the
coder's. Rows the aid shows as having no
install command and no second package name are
still read and labelled (usually E).

## Why the prevalence sample is not extended

The G sample's 12-row cap was priced against
its own coder load and its estimate's interval
(Wilson CI95 at n=105). Extending it now,
after seeing where B rows sit, would be
sampling on the outcome. Controls and the
measurement are extended or capped for their
own reasons, or not at all — and the G sample
is not touched.
