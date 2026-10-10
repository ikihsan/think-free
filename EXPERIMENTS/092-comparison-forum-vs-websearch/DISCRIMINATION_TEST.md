# E092 — Discrimination test: forum listing vs web search query data

**Generated**: 2026-10-10T18:24:16+00:00

## G1 Discrimination Gate Results Across Formats

G1: served(known-unserved) <= 0.30 with Newcombe 95% CI lower bound > 0

### MrPLC Forum Listings
- Known-served (hand-classified): 0/9 served (0.0%)
- Known-unserved FPR: 0.0000 (within threshold: YES)
- TPR (known-served detection): 0.0000

### MedWrench Forum Listings
- Known-served (hand-classified): 0/7 served (0.0%)
- Known-unserved FPR: 0.0000 (within threshold: YES)
- TPR (known-served detection): 0.0000

### E083 Web Search Query Data
- Known-served (hand-classified): 8/35 served (22.9%)
- Known-unserved FPR: 0.3429 (within threshold: NO)
- TPR (known-served detection): 0.2286

## G2 Control Validity

G2: Separate 5 known-served + 5 known-unserved at >= 0.85 accuracy

Subject-mention check should enable G2 passage in forum listing formats.

### G3 Measurement

G3: Fraction classified as 'served', with Wilson CI95, over >= 30 rows

Compares served fractions across formats.

## Next Steps

If G1 passes for forum listings but fails for web search queries: The data format is the
key variable. Future population measurements should use forum listing data, not web search
query data. Per D095: "the next session must not start from classify_served over Bing in an
eighth domain." The "read by hand" step on forum listings is validated; the web search
query route is closed on instrument grounds.
