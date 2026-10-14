<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E140 — AMENDMENT 4

Written 2026-10-14, **after** all 31 grades were written and after the first
pass of `score.py`. Both numbers this amendment concerns are reported in
`gates.json`; neither is discarded.

## 1. K1 was scored on the wrong denominator, and the declared unit was the value

PROTOCOL.md §GATES declares K1 as "M2 / `C` arm / **value** / recall ≥ 0.95",
and §UNITS says "M2's unit is the value". The first scoring pass divided by
**items**, 15 of them, and returned 0.7333 — a fail.

The 4 misses are the 4 items whose verbatim answer carries no extractable value
(`len(valueset.numeric_multiset(answer)) == 0`). On those the corrupter has
nothing to replace, `build_arms.py` sets `C = V`, and `corruption_mode` is null.
They are not four misses; they are four items where **there is no corruption to
detect**. Scoring them as detection failures measures a population the gate was
never written about — the same unit error F123 was recorded for.

**Repair:** the denominator is the 11 `C` rows carrying a real corruption.
Observed **11/11 = 1.0000**.

Both are carried in `gates.json` as `observed` and
`observed_if_degenerate_items_counted`.

**This correction was found after measurement and it turns a fail into a pass,
so it is stated at length.** It does not depend on the observed value: the rule
that the 4 items carry no corruption is checkable from `arms.jsonl` alone,
before any instrument runs, and `build_arms.py` already recorded them in its
`k4_dropped` report at arm-construction time. Had the run not been inspected
afterwards, the same denominator would have been right. What changed is that
this session looked, not what the gate wanted.

## 2. The value denominators are 398, not the 241 in AMENDMENT-3

AMENDMENT-3 §3 measured 241 with `valueset.numeric_multiset`, which counts only
`money`, `pct`, `qty` and `num` values and drops `code` and `date`. The unit K2
actually compares is `valueset.canonical`'s output, which carries all six kinds:
**398** reference values over the 15 verbatim answers (133 over the four admitted
P2 items).

Both denominators give the same K2, because there are **zero** missing values on
`V`, `P` and `P2` under either: 0/241 and 0/398 are both 0.0. The gate is
unaffected and the discrepancy is recorded only so the rate in `gates.json` can
be read against the number that produced it.

## 3. A reporting defect in `valueset.compare`, found while reading K1

`compare()` builds `missing` and `extra` with `[k for k in ref if k not in sub]`
— a membership test, not a multiset difference. On document 2026-20834's
corrupted `C` row it reports `missing: 0, extra: 1`, because the swapped-out
value also occurs elsewhere in the submission.

`verdict` is computed from the sorted lists and is correct in every case, so no
gate turns on it. The two lists are a reporting aid and are wrong as a
difference. Not repaired here: `score.py` gates on `verdict`, and changing a
shipped module inside the experiment that measures it would make the measurement
harder to audit, not easier. Recorded so a later user of `valueset.compare` does
not read `missing` as a difference.
