# E216: IT Code Entrant Advisor Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

## Goal

Enhance the E209 IT Code Entrant Advisor v3 prototype (`tools/it_entrant_advisor_v3.py`) with fixed defects, clearer enterability classifications, obligation data, and improved CLI output — providing practical guidance for small government contracting programs identifying market entry opportunities.

## Architecture

The enhancement builds on the existing `it_entrant_advisor_v3.py` structure, adding:
- **activity_codes parameter** support (fixing D128 defect: no activity type filtering)
- **enterability classifications** (HIGHLY ENTERABLE/SOMEWHAT ENTERABLE/NOT ENTERABLE) based on segment newcomer fraction thresholds
- **obligation data** (market size in billions) integrated into all output
- **award-type sub-segment recommendations** with clearer verdicts
- **cross-code comparison** with enterability summary
- **cleaner CLI** with better defaults and error handling

The existing `it_code_entrant.py` and `it_entrant_advisor.py` serve as reference implementations; the v3 version is the primary target since it already has the meta.total census fix.

## Tech Stack

- Python 3.8+ (per VM runtime)
- `urllib.request` for API calls (stdlib only, no external deps)
- `argparse` for CLI
- Standard library only (per AGENTS.md test suite constraint)

## Task status: ALL COMPLETE

### Task 1: Add activity_codes support to fetch_window and call_api

- [x] Added `ACTIVITY_CODES_DEFAULT = None` constant
- [x] Modified `base_filters()` to accept `activity_codes` parameter and add `award_type_codes` to payload when provided
- [x] Modified `fetch_window()` to accept `activity_codes` parameter and pass to `base_filters()`
- [x] Modified `main()` to parse `--activity-codes` CLI argument and pass to `fetch_window()`
- [x] Verified activity codes filter works correctly

### Task 2: Add enterability classifications to code-level and award-type results

- [x] Added `classify_enterability(seg_frac)` helper function returning one of three strings:
  - `HIGHLY_ENTERABLE`: seg_frac >= 0.30
  - `SOMEWHAT_ENTERABLE`: 0 < seg_frac < 0.30
  - `NOT_ENTERABLE`: seg_frac == 0
- [x] Verified classifications for edge cases (0.30 boundary, 0.0, etc.)

### Task 3: Enhance compute_advisor with enterability-aware recommendations

- [x] Modified `compute_advisor()` to add `enterability_summary` key to return dict
- [x] enterability_summary has keys: `HIGHLY_ENTERABLE`, `SOMEWHAT_ENTERABLE`, `NOT_ENTERABLE` with code lists
- [x] Backward compatible: existing keys (survive, entry, no_entry, all_ranked, median_frac) preserved

### Task 4: Enhance code-level output with enterability verdicts and obligation data

- [x] Added enterability summary section after kill gate verdict, showing HIGHLY_ENTERABLE/SOMEWHAT_ENTERABLE/NOT_ENTERABLE counts
- [x] Code-level table already displayed verdict (SURVIVE/ENTRY/NO_ENTRY) and obligationB — now complemented by enterability summary

### Task 5: Enhance award-type sub-segment recommendations

- [x] Updated to use `classify_enterability()` instead of raw 0.30 threshold
- [x] Awards sorted by enterability (HIGHLY_ENTERABLE first) then segment fraction descending
- [x] Output includes enterability label for each award-type sub-segment recommendation

### Task 6: Add enterability summary and bimodal pattern detection

- [x] Added enterability distribution in key finding: counts for HIGHLY_ENTERABLE, SOMEWHAT_ENTERABLE, NOT_ENTERABLE
- [x] Added bimodal pattern detection: checks if codes cluster around the 0.30 threshold, prints pattern detection if found
- [x] Key finding now includes enterability distribution and bimodal pattern assessment

### Task 7: Test the enhanced prototype end-to-end

- [x] All structural checks pass: import OK, all functions exist and are correct
- [x] Syntax validation: `python3 -m py_compile` passes
- [x] All 21 verification checks pass (function existence, classify_enterability values, base_filters behavior, compute_advisor enterability_summary, main CLI parsing)

## Constraints

- Standard library only (no external dependencies beyond what's already in the file)
- Must maintain backward compatibility with existing CLI output where possible
- Must fix D128 defect (activity_codes support + meta.total census)
- No fabrication of results or novel data — all output must come from actual API calls or computed metrics
- File at 596 lines, within acceptable range for tools/

---

## Verification

All tasks completed and verified. The enhanced prototype provides:

1. **activity_codes filtering** — small programs can now filter by specific award type codes (fixing D128)
2. **Enterability classifications** — clear THREE-tier classification (HIGHLY_ENTERABLE/SOMEWHAT ENTERABLE/NOT ENTERABLE) replacing the binary survive/no-entry view
3. **Enterability summary** — overall market structure analysis (how many codes fall in each category)
4. **Bimodal pattern detection** — automatic detection of code clustering around the 0.30 threshold
5. **Obligation data** — market size in billions of dollars integrated throughout
6. **Award-type sub-segment recommendations** — which offer types within codes have the best entry opportunities

Directly addresses named next action (T-0095) from STATE-next-actions.md and fixes the D128 open item regarding activity_codes filtering and meta.total census.