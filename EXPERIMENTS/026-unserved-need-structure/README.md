# E026: is the corpus's unserved tail structured?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

The last open reading of the E022 corpus: the **589 need statements that drew
no reply at all**. Measured 2026-10-05, task T-0070. Full protocol in
[PROTOCOL.md](PROTOCOL.md), raw capture in
[`raw/texts.jsonl`](raw/texts.jsonl), machine-readable numbers in
[`results.json`](results.json).

## Method

For each of the 1401 rows in E022's outcomes table, the comment text was
fetched from the same Firebase item endpoint E022 used. All 1401 returned
parseable text, so gate A1 (≥95%) passes at 100%. Word counts are words after
HTML tag stripping; arms split on `answered` from E022's table.

## Results

| Gate | Declared rule | Observed | Verdict |
|---|---|---|---|
| A1 | ≥95% of fetches return text | 1401/1401 = 100% | pass |
| B1 (H1: unserved are vaguer) | unserved median words ≤ half of answered | 55 vs 58, ratio 0.948 | **fails** |
| B2 (H2: a trigger is ≥2× over-represented) | any trigger's unserved share ≥ 2× its answered share | two fire: `does anyone know a tool` 4.14×, `is there a python library` 2.07× | **fires** — see sensitivity |

**B2's sensitivity reading withdraws the structure claim.** The two firing
triggers carry 4 and 5 rows total. The corpus-wide chi-square test of
trigger × answered independence is χ² = 34.33 on 23 df, p ≈ 0.06 — not
significant at 0.05. The two over-represented rows are consistent with
small-count noise. Nothing here survives as a structure finding.

`dead`/`deleted` flags: 0 in either arm, so the tail is not moderated-away.

## Verdict

**H0, with the corpus's own caveat made measured.** The unserved tail is
diffuse in the dimensions measured here: statement length (ratio 0.948) and
trigger phrase (p ≈ 0.06). The only numeric hint — two trigger phrases with
answer rates of 0.25 and 0.40 against the corpus's 0.58 — rests on 9 rows
total and is not established. The corpus's closure stands without a hidden
structured sub-population, at this resolution. A decision would need a
population too small to defend at this sample size.

## Ceiling

One platform, one corpus, one reader of the text. Length is stripped words,
not human judgement of vagueness. Trigger phrases are E012's 23, which F042
showed mark staters rather than outcomes. What the requests became is
unmeasured by design; whether any of the 589 named a need no artifact serves
was E012's 0-of-50 result and is not re-run.
