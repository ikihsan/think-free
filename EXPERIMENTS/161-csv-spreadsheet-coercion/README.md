<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E161 — CSV ↔ spreadsheet coercion

Method, files and how to re-run. The numbers and the verdict are in
[`RESULT.md`](RESULT.md).

## What this measures

A real spreadsheet engine (LibreOffice Calc, headless) opens real CSV files.
The `.xlsx` it writes is read back with `zipfile` and `ElementTree` and every
cell is compared with the source text. The engine's own output is the oracle;
nothing in this directory generates a corrupted cell.

## Files

| File | What it is |
|---|---|
| `roundtrip.py` | convert each CSV with `soffice`, read the xlsx, diff every cell, classify the change |
| `csvsafe.py` | the prototype: `check` reports, `write` repairs the damaging cells |
| `compare.py` | instrument test: checker predictions vs the engine's own changes |
| `controls.py` / `controls_fix.py` | the 75 folklore values, and 10 values × 6 escapes |
| `corpus.py` / `corpus_govuk.py` | frame assembly, with the frame rule declared in the docstring |
| `corpus-manifest.json` | every file: source, url, bytes, sha256, and the frame rule it came from |
| `results-*.json` | per-frame counts and the rule histogram |
| `instrument-test.json` | precision, recall and the top disagreements per frame |
| `sample-changes-*.tsv` | first 300 rows of each frame's full cell-level change log |

Not committed: the fetched CSVs, the generated `.xlsx`, and the full change
logs (9.3 MB for one frame). They are byte-reproducible from the scripts and
the recorded URLs and sha256 sums.

## Cells the engine is judged on

`changed` — the value the engine stored is not the source text.
`damaging` — `leading_zero`, `precision_loss`, `datetime_time_lost` or
`formula_executed`: the value cannot be recovered by eye. Everything else in the
histogram (date serials, thousands separators, trailing zeros, trimmed padding,
percent and currency symbols) is a re-formatting the reader can undo.

## One caveat that shapes the numbers

The engine ran under `LANG=C.UTF-8`, so it parsed dates day-first-fails:
`02/09/2005` became a date, `31/08/2005` and `14/10/2026` stayed text. Roughly
12,880 of frame D's cells are in that class, which is where the checker's 0.59
precision on that frame comes from.