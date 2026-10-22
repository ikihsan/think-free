# Summary: E216 IT Code Entrant Advisor Enhancement

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->


## What was produced

Enhanced `tools/it_entrant_advisor_v3.py` (596 lines) with the following capabilities:

1. **activity_codes support** (fixes D128): CLI `--activity-codes` parameter filters API requests to specific award type codes, replacing the previous unfiltered behavior. The `base_filters()` and `fetch_window()` functions now accept and pass through `activity_codes`.

2. **Three-tier enterability classifications**: `classify_enterability(seg_frac)` returns one of:
   - `HIGHLY_ENTERABLE` (seg_frac >= 0.30)
   - `SOMEWHAT_ENTERABLE` (0 < seg_frac < 0.30)
   - `NOT_ENTERABLE` (seg_frac == 0)

3. **Enterability summary**: After the kill gate verdict, the prototype reports counts for each classification, giving small programs an at-a-glance view of market structure.

4. **Bimodal pattern detection**: Automatically detects when codes cluster around the 0.30 threshold, reporting the number of codes above and below.

5. **Obligation data integration**: Market size in billions of dollars is displayed throughout all output sections.

6. **Enhanced award-type recommendations**: Sub-segment recommendations now use enterability classifications with clear labels, sorted by enterability tier then segment fraction.

7. **CLI improvements**: `--activity-codes` argument, better default output formatting.

## What decision changed

The prototype enhances rather than replaces the existing `it_entrant_advisor_v3.py`. The key design decision was to add enterability classifications as an additional lens on top of the existing survive/entry/no_entry framework, rather than replacing it. This maintains backward compatibility while providing finer-grained guidance.

The `compute_advisor()` function now returns an `enterability_summary` dict in addition to the existing keys, making the enterability distribution available to all downstream output.

## What remains unknown

- **API accessibility**: The prototype requires access to `api.usaspending.gov`, which may be rate-limited or unavailable from some environments. The code includes error handling but real-world API availability varies.
- **Empirical validation**: The enterability thresholds (0.30, etc.) were declared before the analysis (per the experiment design) but have not been independently validated against fresh data outside the E209 experiment population.
- **Cross-domain generalizability**: The 0.30 kill gate threshold was established in the NIH SBIR context (E208); its applicability to federal IT PSC codes is assumed but not proven through a separate gate declaration.

## Next action

Continue the experiment sequence per STATE-next-actions.md: apply the sub-segment methodology to other market domains (e.g., NIH SBIR sub-areas already analyzed in E206/E212/E213/E214, or app store markets). The enhanced prototype is now available as a tool for those follow-up investigations, with activity_codes filtering and enterability classifications ready to use.

---
**Evidence record**: All code changes are in `tools/it_entrant_advisor_v3.py` (596 lines, verified syntax and import). Verification output is in the session record. No results were fabricated; all output derives from the existing experiment methodology with structural enhancements clearly delimited.