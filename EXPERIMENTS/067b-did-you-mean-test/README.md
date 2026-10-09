<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-09
-->

# E067b — a deterministic "did you mean" cannot separate the two classes

**Date:** 2026-10-08 · **Session:** 2026-10-08-021 · **Status:** complete —
**kill gate FAIL, as predeclared**

Landed 2026-10-09 (session 2026-10-09-002) from an unlanded tree. No protocol
was written before the run; the predeclared thresholds are the two in
`EXPERIMENT-RESULT.json` (recall ≥ 0.80, specificity ≥ 0.90), and the gate
failed on both arms.

## What was asked

E064 measured that 93 of 576 plausible near-miss mutations of real package
names resolve to a **real, different** artifact (F099) — the existence bit every
installer returns is wrong 16% of the time, silently. Its declared metadata
repair failed its recall arm because the 24 it misses are healthy, popular
projects. This experiment asks whether **syntax** can do what metadata could
not: does a deterministic "did you mean a different project?" rule separate the
93 false accepts from the 483 true negatives.

## Results (observed)

| instrument | recall | specificity | reading |
|---|---|---|---|
| prefix/suffix match on PyPI (E067 prototype) | **0.000** | 1.000 | separates nothing |
| `difflib.get_close_matches(cutoff=0.3)` | **1.000** | **0.000** | flags every name |

**Kill gate: FAIL.** Neither instrument reaches both thresholds.

## What it establishes

`observed`: neither syntactic rule separates the classes. The edit-distance arm
is the informative failure — at a cutoff loose enough to catch all 93 it also
accepts all 483 real names, because a mutation like `requests-cli` is *closer to
`requests`* than `requests` is to most of what a user means. **Distance measures
the mutation, not the error**, so it cannot be tuned into a discriminator.

This corroborates E064's own conclusion from the opposite direction: the
separator that remains is semantic — "does this package do what was asked" —
which is a model call, and takes the cost and determinism advantage that
justified a deterministic checker with it. Two independent deterministic
families now fail on the same population.

**Ceiling:** 576 mutations from E064's single author's mutation families, one
registry's naming shapes for the prefix/suffix arm, one cutoff for the
edit-distance arm, and no sweep over `cutoff`. A tighter cutoff would trade
recall for specificity along the same curve; the arm at 0.000 specificity is
evidence about that curve's shape, not about every cutoff.

## Reproduction

```bash
cat EXPERIMENT-RESULT.json    # gate and both arms
# the 576 scored names are a subset of E064's committed mutation set:
python3 -c "import json;d=json.load(open('../064-remedy-existence/raw/mutations.json'));print(len(d),'entries')"
```

Raw per-name outcomes are in `results-raw.json` (117 KB); ground truth is
E064's `raw/metadata-falseaccepts.json`, unchanged. The experiment's own
`mutation-names.txt` was removed on 2026-10-09 — every one of its 576 names was
already in `EXPERIMENTS/064-remedy-existence/raw/mutations.json`, so it was
byte-redundant with a tracked source and its length tripped the doc-lint cap.