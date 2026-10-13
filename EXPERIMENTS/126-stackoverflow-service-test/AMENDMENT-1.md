<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E126 Amendment 1 — declared before any attempt is written

Two corrections to `PROTOCOL.md`, made after the pool was
fetched and screened but **before any attempt is written or
any answer or comment is read**:

## 1. Dedupe (fetch artifact)

The Stack Exchange API returned question `79660070` on both
pages of Arm A (the sort=votes pages overlapped on that row).
`screen.py` drops the duplicate, so the screened population is
**299 rows, not 300** (Arm A 199, Arm B 100). The duplicate
is recorded in `screening.jsonl` with `dropped: true` and its
`duplicate_of` row; the raw pool is committed verbatim in
`pool-raw.json`.

## 2. Attempt sample definition

PROTOCOL.md said the attempt sample is "the top 20 by
`view_count` within Arm A's question-shaped rows". K1 measures
the **answerable class**, and the top 20 question-shaped rows
contain only **16** answerable rows (rows 1, 2, 17, 18 of the
view_count-sorted sheet are `specific`), which would make K1's
denominator 16 against a declared n = 20.

**Amended rule:** the attempt sample is the **20 highest-
`view_count` answerable-class rows within Arm A**. This is the
class K1 measures, sampled directly; no `specific` row is
spent on a gate that cannot read it. The composition of the
top 20 question-shaped rows (16 answerable / 4 specific) is
reported in `RESULT.md` as a covariate, not discarded.

The amended sample is sheet rows **3–16, 19, 20, 22, 23, 24,
25** (question_ids in `attempts.jsonl`), all
`question/answerable`, view_count 20190 … 34266.

Nothing else changes: G0, G1, G2, K1's rule, K2, K3, the
attempt discipline, and the served definition are as declared
in `PROTOCOL.md`.
