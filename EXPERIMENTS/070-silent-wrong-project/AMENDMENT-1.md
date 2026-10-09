<!-- origin-meta
owner: EXPERIMENTS/070-silent-wrong-project/PROTOCOL.md
status: active
last-verified: 2026-10-09
-->

# E070 — Amendment 1 (declared 2026-09, before any row was
# classified)

Two sampling facts were underspecified in `PROTOCOL.md`,
and both are fixed here, before a single row is read, so
no classification decision can move them afterwards.

## 1. The per-query sample is the top 12, not 25

The protocol said "up to 25 items per query … target ≥
100 G rows". Fetching returned 390 rows (381 unique)
with a median body of 2 210 characters. Reading every
row at full length is a multi-day coder load, and a
tired coder is a misclassification risk the protocol did
not price. The amendment:

- **Per query, the sample is the first 12 items in the
  order the API returned them** — the venue's own
  relevance ranking, i.e. the first page a person
  browsing that search sees. No row is selected by the
  coder's interest. (Amended from 10 after the fetch:
  deduplication left 88 G rows, under the protocol's
  declared `>= 100` target; 12 restores it at 105.)
- **A row is classified once**, under the first query
  that returned it (dedup by `question_id` / issue
  number across queries and venues).
- Expected sample: PC 61 (4 SO + 2 GH queries),
  G 105 (6 SO + 4 GH), PL 24 — 190 rows.

**Ceiling:** the venue's ranking is relevance, not
exhaustiveness; a B report ranked below the first page
of its query is outside the sample. The prevalence
estimate is over *first-page* reports.

## 2. The denominator is stated twice, and the primary
one is confusion reports

"B share among G rows" is ambiguous between two
denominators. Both are pre-declared and both are
reported:

- **primary:** B / (A+B+C+D) — the share among rows that
  *are* package-name-confusion reports, which is the
  question the protocol asks ("among real reports of
  package-name confusion");
- **secondary:** B / all-G — the diluted share, reported
  because a row that is not a confusion report is also
  evidence about how often confusion arrives at all.

The gates' thresholds (K2: ≥ 0.10 build, < 0.05 close)
are read on the primary denominator.

## 3. What the coder reads, and what the second pass
checks

Classification reads the title and the first 1 500
characters of the body. The 20 % second pass (the κ
sample) re-reads the **full** body, so the sample
specifically tests whether the truncation changed any
label. A label that flips on full reading is recorded as
a truncation defect and the whole class is re-read.

## 4. Order of classification

PC first, then the K1 gate, then G and PL. If the
instrument cannot recover the known silent-class reports
(K1 fails), the G classification is not run — a broken
instrument must not produce a prevalence estimate.
