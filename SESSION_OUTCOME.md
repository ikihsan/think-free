# Session 2026-10-14-025 — Value Canonicalizer Prototype

**Goal:** Build and evaluate a value canonicalizer prototype for regulatory text extraction.

## What was produced

**`tools/regvalue/regvalue_cli.py`** — A CLI prototype implementing the `ground.py` + `valueset.py` canonicalizer for extracting and grounding named values from regulatory text. Usage:

```
python3 regvalue_cli.py <document_path> <answers_jsonl> [threshold=0.6]
```

The tool:
- Normalizes the document using `ground.normalize()` (strips HTML tags, joins line wraps, decodes entities)
- Extracts value claims from each answer using `ground.PATTERNS` (date, money, code, pct, qty, num)
- Calls `ground.judge(doc, answer, threshold)` to determine verdict for each value
- Reports verdict: `grounded` (context matches above threshold), `ungrounded_claim` (value occurs but context doesn't match), or `ungrounded_value` (value not found in document)
- Outputs per-value verdicts with confidence scores (0.0–1.0) and a summary counts

## What was observed

Tested on 3 Federal Register documents (E114/E142 corpus, agency rule final rules):

| Document | Values Checked | Grounded | Ungrounded Claim | Ungrounded Value | Key Pattern |
|---|---|---|---|---|---|
| **2026-21031** (NRC AP1000) | 4 | 3 (75.0%) | 1 (25.0%) | 0 (0.0%) | Dates (score=1.0) and CFR codes (score=1.0) reliably grounded; money $1,000 → ungrounded_claim (context mismatch) |
| **2026-21019** (PBGC Assets) | 5 | 3 (60.0%) | 1 (20.0%) | 1 (20.0%) | Dates (score=1.0) and CFR codes (score=1.0) grounded; pct "0.78 percent" → ungrounded_value (not in doc); num "0.13" → ungrounded_claim (context mismatch) |
| **2026-21020** (Immigration penalties, HTML) | 3 | 0 (0.0%) | 0 (0.0%) | 3 (100.0%) | HTML normalization issue: values ($100,000, 15-business days, 8 CFR part 281) not found in normalized text; may reflect document-format limitation rather than instrument failure |

**Key findings:**
- **Dates** are reliably grounded when they appear in both answer and document (score 1.0)
- **CFR/regulatory codes** are reliably grounded (e.g., "10 CFR Part 52", "29 CFR part 4044")
- **Money values** are variable: sometimes `ungrounded_claim` (context doesn't match), sometimes `ungrounded_value` (not in document at all)
- **The instrument is genre-specific**: confirmed working on Federal Register final rules (E114: 0/374 fabricated, E142: 1.0 detection on 4/4), failing on SQuAD (0.2826 detection vs ≥0.95 gate) and Hacker News titles (0 extracted)
- **HTML-wrapped Federal Register documents** may have normalization limitations that affect instrument performance

## Build decision changed

Prototype development of the value canonicalizer CLI rather than pursuing a new candidate. This follows the mission's established pattern: build a runnable experiment/prototype first, measure it against concrete evidence, then decide on product engineering. The decision is consistent with the mission's narrowed applicability domain — the value canonicalizer is confirmed as a genre-specific instrument (Federal Register rules only), not a general extractor.

## What remains unknown

1. **Genre limitation boundary**: Confirmed Federal Register–specific, but the exact breadth of the failure on other genres (social media, issue-tracking, ML registries) still needs mapping. The mission has already shown the principle does not generalize across package registries under matched harvest.

2. **Money value variability**: Whether `ungrounded_claim` (context mismatch) vs `ungrounded_value` (absent from document) rates can be improved by pattern refinement or whether this is a structural bound.

3. **HTML normalization reliability**: Full Federal Register HTML documents may lose content during normalization, affecting instrument performance. Need to test with properly parsed/text-only versions.

4. **Real-world adoption**: The prototype is evidence-gathering, not product validation. No users have been observed; usefulness is inferred from the mechanism's performance on the target genre.

## Single most useful next action

**Run the prototype on a larger, systematically-sampled corpus of Federal Register final rules (20+ documents across different agencies) to establish statistically reliable grounded/ungrounded rates and further delineate the instrument's applicability domain.** This experiment would:

- Test the instrument on a broader sample than the 3 documents currently evaluated
- Produce concrete numbers (e.g., "78% of money values are grounded on Federal Register rules, with 12% ungrounded_claim and 10% ungrounded_value")
- Determine whether the HTML normalization issue is document-specific or systematic
- Provide the evidence needed for a well-informed decision: refine the instrument for regulatory compliance use, apply it to a different domain, or close this line of inquiry

**Reproduction:** `python3 tools/regvalue/regvalue_cli.py <doc-path> <answers-jsonl>` on documents from `EXPERIMENTS/142-valueset-regulatory-human/raw/` with answers from `EXPERIMENTS/142-valueset-regulatory-human/arms.jsonl`.

**Kill gate (predeclared, from E114/E142):** If grounded rate on a 20-document Federal Register corpus falls below 50%, the instrument is confirmed as not practical for general regulatory value extraction. If grounded rate is ≥70% on dates+codes+Money (≥50% on money alone), the instrument has a viable niche as a ranked human-review prioritizer (a value flagged as grounded is worth a human glance, consistent with E114's finding that it is "worthless as a gate but worth reusing as a ranker").

**Verification:** `PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests` must exit 0.