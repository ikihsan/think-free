<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Hypotheses — experiment results (continued)

Split from [`HYPOTHESES-results.md`](HYPOTHESES-results.md) on 2026-10-09 at the 300-line cap.

## E080 — Food recall purchase matching: falsification experiment result

**Result:** `observed` (synthetic), 2026-10-09

**Claim under test (H-01).** A consumer's purchase records (receipts, loyalty exports, manual entry) can be matched against FDA/USDA recall data with sufficient accuracy to warn them of recalled products they own.

**Kill gates (predeclared).**
- G1: Precision ≥80% on each format
- G2: Recall ≥60% on each format
- G3: ≥2 of 3 formats pass both G1 and G2
- G4: Specificity = 1.0 (zero false positives on clean negatives) on each format

**Result.** All gates pass on 5/5 random seeds. Receipt: 1.00/1.00; Loyalty CSV: 1.00/1.00; Manual entry: 1.00/0.93. Specificity 1.000 on all.

**Critical limitation.** Synthetic fixtures guarantee identifier linkage by construction: each recall and its purchases share the same store (→ same UPC), lot code, and best-by date. The matching algorithm correctly exploits this guaranteed linkage. Real-world preconditions are unmet: receipts have UPCs in 10-30% of lines, almost never lot codes; store brands use different UPCs than national brands; FDA recall API has UPC in ~40% of records. Loyalty programs (Kroger, Costco, Safeway) already solve this for their members — they possess the purchase UPC + store mapping.

**Conclusion.** Technical feasibility shown: the matching logic works when identifiers align. Practical viability untested: the identifier linkage problem is the hard part, not the matching algorithm. Record as technical feasibility result only. **Decision: hold** — not a candidate for product engineering.

**Ceiling.** 5 seeds, 30 products, 3 formats, stdlib Python. Measures matching logic correctness given identifiers; does not measure identifier availability, OCR noise, store-brand UPC divergence, recall data sparsity, or user adoption.

**Artifacts:** [`EXPERIMENTS/080-food-recall-matching/RESULTS.md`](EXPERIMENTS/080-food-recall-matching/RESULTS.md), [`results.json`](EXPERIMENTS/080-food-recall-matching/results.json).