<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E161 — what a spreadsheet engine really does to a CSV

**Question.** A CSV is a text file; a spreadsheet is a program with a type
system. When someone opens one in the other, which cells come back changed, how
often, and can a small deterministic program know in advance?

**Why this instrument.** E122, E147, E150 and E160 all failed the same way:
synthetic fixtures with clean keyword separation made the trivial classifier
optimal. This experiment uses a *real engine's own output* as the oracle and
*real files* as the population, so the positives are not near-copies of
anything the experiment made.

**Engine.** LibreOffice Calc 6.4.7.2, headless, CSV import with special-number
detection on (`Text - txt - csv (StarCalc):44,34,76,1,,0,false,true`), locale
`C.UTF-8`. It writes an `.xlsx`; `roundtrip.py` reads it back with `zipfile`
and `ElementTree` only and compares every cell with the source text. A cell
counts as *changed* when the value the engine stored is not the source text.
A cell counts as **damaging** when the value cannot be recovered by eye:
`leading_zero`, `precision_loss`, `datetime_time_lost`, `formula_executed`.

## Frames (declared before fetching, full provenance in `corpus-manifest.json`)

| Frame | Files | Cells | Damaging |
|---|---|---|---|
| A–C analyst exports: `vega/vega-datasets`, Our World in Data, first 12 paths each | 17 | 688,107 | **0** |
| D public-body registers: data.gov.uk most-recently-modified list (2 Camden licensing registers) | 2 | 130,115 | **0** |
| E targeted: US Census 2023 Gazetteer places, chosen because `GEOID` carries leading zeros | 1 | 387,962 | **36,697 (9.5%)** |
| controls: 78 folklore values (postcodes, FIPS, phones, long IDs, date spellings) | 1 | 158 | **13** |
| verify: frame E after `csvsafe write` | 1 | 387,962 | **0** |

## 1. The folklore is real, and it is population-specific

Frame E is a US government file. Every `GEOID` with a leading zero loses it:
`0100100` is stored as `100100`, in **36,697 cells**, and a `GEOID` is an
identifier, so the file that comes back identifies a different place. The same
engine, on 818,222 cells of analyst and public-body files, destroyed nothing.
Frames A–C changed 11,029 cells (1.6%) and frame D 18,897 (14.5%) — every one
a re-typing or re-formatting a reader can undo by eye (`date_serial`,
`datetime_serial`, `numeric_reformat`).

So the question "do spreadsheets corrupt CSVs" has no single answer. It has an
answer conditional on whether the file carries identifier columns, and a file
carries them when a *person* is the consumer rather than another program.

## 2. What the engine does, measured one value at a time

`controls.py` → `controls.csv`, 75 values, every cell compared:

| Rule | Example | Stored | Recoverable by eye? |
|---|---|---|---|
| `leading_zero` | `01234`, `0001234567890123` | `1234`, `1234567890123` | no |
| `precision_loss` | `4111111111111111` | `4111111111111110.0` | no |
| `precision_loss` | `12345678901234567` | `1.23456789012346e+16` | no |
| `formula_executed` | `=1+1` | `2` | no |
| `date_serial` | `2020-01-02`, `01/02/2020` | `43832` | yes |
| `datetime_serial` | `02/09/2005 01:30:00 PM` | `38392.5625` | yes |
| `time_serial` | `12:30` | `0.520833333333333` | yes |
| `thousands_separator` | `"1,234"` | `1234` | yes |
| `percent` / `currency` | `12%`, `$1,234.56` | `0.12`, `1234.56` | yes |
| `whitespace_trim` | `"12345 "` | `12345` | yes |
| **left alone** | `1HGBH41JXMN109186`, `GB82 WEST 1234 5698 7654 32`, `4111 1111 1111 1111`, `555-123-4567`, `9780306406157`, `1e-7`, URLs, `NULL`, emoji, 300-character strings | same text | — |

Date-times keep their clock: `02/09/2005 01:30:00 PM` is stored as
`38392.5625`, not truncated. An earlier classifier called that case
`datetime_time_lost` and an earlier count of 2,881 "destroyed" cells in frame D
came from that mistake — all of them were `12:00:00 AM`, which is midnight and
loses nothing. **No cell in 1,206,342 compared lost a time component.** The rule
remains in `roundtrip.py` as a defensive check and fires zero times.

Date interpretation is **locale-dependent and silently partial**: with
`LANG=C.UTF-8` the engine reads `02/09/2005` as 9 February and *rejects*
`31/08/2005` and `14/10/2026`, leaving them as text. The same file is read
differently by a reader in another locale. That single fact is the source of
almost all of the checker's remaining false alarms below.

## 3. Only one of six escapes works

`controls_fix.py` writes 10 values × 6 escapes and puts them through the same
engine:

| Escape | Result on `01234` |
|---|---|
| `"01234"` (quoting alone) | `01234`, still text — no protection needed, none given |
| `'01234` (the apostrophe people recommend) | stored as `'01234` — **the apostrophe is visible text** |
| `\t01234` (tab prefix) | stored with the tab still in it |
| `'="01234"` | stored literally |
| **`="01234"`** | **stored as text `01234`, exact, all 10 of 10** |

`="value"` is the only escape in this set that a real engine stores as the
value itself. Cost: a non-spreadsheet reader sees the wrapper literally, so a
repaired file is safe for the spreadsheet and unsafe for `pandas` unless the
reader strips it.

## 4. Can a small program predict the engine? (`compare.py`, `instrument-test.json`)

`csvsafe check` is 200 lines of standard library. Against the engine's own
cell-level output:

| Frame | engine changes | checker flags | precision | recall | damaging P | damaging R |
|---|---|---|---|---|---|---|
| controls | 38 | 45 | 0.8444 | 1.0 | 1.0 | 0.9231 |
| A–C analyst exports | 11,029 | 11,029 | **1.0** | **1.0** | n/a | n/a |
| D registers | 18,897 | 31,777 | 0.5947 | 1.0 | n/a | n/a |
| E census | 83,331 | 83,334 | **1.0** | **1.0** | **1.0** | **1.0** |

On the frame where damage exists, the damaging flag is **36,697 true positives,
0 false positives, 0 false negatives**. Frame D's precision is 0.59 because
12,880 of its flags are d/m/y dates the C-locale engine refused to parse — the
checker cannot know the reader's locale, and neither can the file.

## 5. The repair

`csvsafe write` protected the 36,697 damaging cells of the census file and
nothing else. Re-run through the same engine: **0 damaging cells**, and each
protected cell comes back as its exact original text (`formula_text_literal`
36,697 in `results-verify.json`). The harmless changes (14,305 number
spellings, 32,327 trimmed paddings) are left alone by design.

## Verdict

The mechanism is real, reproducible, and predictable by a 200-line standard-
library program validated against an independent implementation on real files —
the first instrument in this mission's record validated that way rather than
against synthetic fixtures.

**It is not a candidate.** The demand probes at the head of this experiment
(Stack Exchange, six sites, seven vocabularies; GitHub, PyPI and npm search for
prior art) returned a handful of high-vote reports and a set of 0-to-1-star
tools that already do parts of it. Nothing here beats "send an `.xlsx`" or
"know your own data" by a margin that supports a release, and the frame where
damage is common — identifier columns in machine-produced tables — is a
population whose members already know, because the ones who publish such files
publish `.xlsx` too.

Kept: `csvsafe.py`, `status: draft`, unreleased, with every rule measured
rather than documented. Kept and reusable: the round-trip instrument, which
produces cell-level ground truth from a real engine on real files and is the
instrument the four synthetic-fixture experiments did not have.

## Limitations, stated

- **LibreOffice, not Excel.** Every number here is that engine, version
  6.4.7.2. Excel is documented to coerce the same classes, and `="value"` is
  the technique Excel users are told to use, but neither was measured here.
- **Locale is a parameter, not a constant.** The date findings hold for
  `C.UTF-8`; a reader in a day-first locale sees `02/09/2005` differently.
- **Stored value, not pixels.** A cell's rendering also depends on column
  width and number format, which are not modelled. Comparing stored value to
  source text is the conservative direction: equal stored values cannot render
  differently, unequal ones may render as the source.
- **Frames, not the world.** 20 files, one of them chosen because it contains
  the dangerous class. The prevalence numbers are conditional on the frames
  named above and are not estimates for "CSVs at large".
- Frame D's provenance was recovered by sha256 match after the fact, not at
  fetch time; the URLs in `corpus-manifest.json` are correct for those bytes.

## Reproduce

```bash
sudo apt-get install -y --no-install-recommends libreoffice-calc
python3 corpus.py                 # frames A-C  (git clones of vega-datasets + OWID)
python3 corpus_govuk.py           # frame D    (data.gov.uk, Camden registers)
python3 controls.py controls && python3 controls_fix.py controls-fix
# frame E: fetch the Census Gazetteer zip, convert tab-delimited to CSV
for d in controls corpus corpus-census corpus-govuk; do python3 roundtrip.py $d; done
python3 compare.py controls corpus corpus-govuk corpus-census
python3 csvsafe.py check <file>; python3 csvsafe.py write <file> <out>
```