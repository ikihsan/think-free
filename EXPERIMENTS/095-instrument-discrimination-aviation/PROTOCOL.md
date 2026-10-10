# Experiment E095 — Instrument Discrimination Test on E083 Aviation Ground Truth

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

## Experiment: E095 — Fresh Observation Instrument Discrimination Test

### Goal

Test the adapted `fault_need_classifier` instrument against the E083 hand-classified aviation ground truth: 30 aviation maintenance fault code statements (0 served, 6 partially_served, 24 unserved). This directly addresses the open question per D088/D095 whether the validated instrument can pass G2 on "labels known by construction" before any population measurement.

Per D088: "the gate's passing value must be enumerated before the run — the route must be re-entered through a discrimination test that passes on labels known by construction, not through another domain screen."

Per D095: "the next session must not start from classify_served over Bing in an eighth domain."

Per STATE.md §265: "The single most useful next action, after E088. The discrimination test must pass on labels known by construction before any population measurement."

Per STATE.md §267: "the next work is not another domain and not another screen: it is a real need population measured by an instrument that has first passed a discrimination test on labels known by construction."

---

### Instrument Under Test

**Adapted `fault_need_classifier` for E083 data:**

The full E090 instrument requires `view_count` and `reply_count`, which are not available in the E083 raw data (all entries have `num_results=5` from Bing search). This adaptation uses available features:

```
IF error_code_present AND has_solution_keyword:
    CLASSIFY = "served"
ELIF error_code_present AND NOT has_solution_keyword:
    CLASSIFY = "unserved"
ELIF NOT error_code_present:
    CLASSIFY = "unserved"
ELSE:
    CLASSIFY = "unserved"
```

**Features used (available from E083 treatment-results.jsonl):**
- `error_code_present`: whether the title contains specific error/fault code patterns via `has_specific_error_code()`
- `has_solution_keyword`: whether titles/snippets contain resolution-oriented keywords (how to, tutorial, guide, solution, fix, repair, tool, software, app, download, install, step by step, method, procedure, resolution, fix for, fixes, troubleshooting)

**Not used (unavailable from E083 data):**
- `view_count`: all entries have num_results=5 (constant, no discrimination possible)
- `reply_count`: not present in E083 raw data
- `vendor_acknowledged`: not available from listing pages alone

---

### E083 Hand-Classified Ground Truth

(from EXPERIMENTS/083-aviation-maintenance-fault-codes/results.json)

| Expected Label | Count | Fraction |
|----------------|-------|----------|
| `served`       | 0     | 0.000    |
| `partially_served` | 6   | 0.200    |
| `unserved`     | 24    | 0.800    |

**Rubric (from E083 PROTOCOL.md):**
- `served`: working solution, direct link to tool/manual, or step-by-step resolution guide for the specific fault code
- `partially_served`: relevant info (error code definition, manufacturer notes) but no complete resolution guide
- `unserved`: no relevant results, or only irrelevant results

**Key E083 findings (from SUMMARY.md/F112):**
- The automated keyword classifier produces 19/30 false positives for "served" — labels content as served based on incidental keyword matches
- All 30 are either unserved or partially_served — NONE are fully served
- G2 discrimination test FAILED: best accuracy 0.70 (7/10 separated), requires ≥0.85
- G1 false positive rate: 19/30 known-unserved classified as served = 0.633 (well above 0.30 threshold)
- This is the class of failure documented in F109/D095: the classifier's solution keywords match irrelevant content by coincidence

---

### Test Data: 30 Aviation Statements

The 30 treatment statements from `treatment-results.jsonl`, each a Bing search result entry with:
- `query`: the original query text (e.g., "boeing error code 1")
- `query_normalized`: normalized query version
- `num_results`: 5 for all entries (Bing search results count)
- `titles`: list of result titles (5 titles, some empty)
- `snippets`: list of result snippets (5 snippets, some empty)
- `statement_id`: 0-29 index

For each entry, the test extracts:
- `error_code_present`: pattern match on title text
- `has_solution_keyword`: keyword check on concatenated titles + snippets

---

### Discrimination Test Gates (adapted for available data)

| Gate | Criterion | Threshold | Kill Condition |
|------|-----------|-----------|----------------|
| G1 | False Positive Rate (known-unserved classified as served) | < 0.10 (10%) | FAIL → instrument invalid, redesign |
| G2 | True Positive Rate (known-served classified as served) | > 0.70 (70%) | FAIL → instrument lacks sensitivity |
| G3 | False Negative Rate (known-served classified as unserved) | < 0.30 (30%) | FAIL → instrument too conservative |

**Pass Condition**: G1 PASS (primary) AND (G2 PASS OR G3 PASS)

**Critical adaptation**: With 0/30 served in the E083 ground truth, G2 and G3 are **not evaluable** in the standard form (no known-served entities exist). The test will focus on G1 (FPR on known-unserved) and document that G2/G3 are not applicable with this ground truth.

**Adapted evaluation**:
- G1: Of the 30 entries (24 known-unserved + 6 known-partially_served), how many are classified as "served"? FPR must be < 0.10 to pass.
- G2/G3: Documented as "not evaluable with 0 served in ground truth." The instrument can still be evaluated for its ability to filter unserved from the available data.
- If G1 passes: instrument successfully filters known-unserved from the E083 ground truth, but population measurement requires served entities (which this domain has 0 of per hand classification).
- If G1 fails: instrument produces false positives on known-unserved, confirming the pattern seen in E083 (19/30 false positives) and E090-instrument-discrimination (FPR=0.80).

---

### Expected Outcomes

Given the E083 findings and the adapted classifier logic:

**Outcome A (G1 FAIL)**: The classifier labels many entries as "served" due to error code patterns matching incidental content (e.g., "error" in non-fault contexts, "fix" in unrelated guides). FPR >> 0.10. This confirms the pattern seen in E083 (19/30 false positives) and E090-instrument-discrimination (FPR=0.80), and supports the SUMMARY.md conclusion that "population measurement is unfalsifiable and should not proceed" with the current instrument design.

**Outcome B (G1 PASS, G2/G3 not evaluable)**: The classifier correctly identifies most entries as "unserved" (FPR < 0.10), but since 0/30 are served per hand classification, G2/G3 cannot be evaluated. The instrument can filter unserved from the E083 ground truth, but population measurement in this domain is still unfalsifiable — the instrument can identify unserved needs, but there are no served needs to measure against.

**Outcome C (Instrument redesign needed)**: G1 FAIL confirms the view-count-based classifier's fundamental limitations in fault-code domains, supporting D095's constraint that "the next session must not start from classify_served over Bing in an eighth domain."

---

### Evidence Trail

- **Ground truth**: E083 hand classifications (0 served, 6 partially_served, 24 unserved) from EXPERIMENTS/083-aviation-maintenance-fault-codes/results.json
- **Instrument**: Adapted `fault_need_classifier` using available E083 data features
- **Test script**: `run_discrimination_test.py` in EXPERIMENTS/095-instrument-discrimination-aviation/
- **Results**: `results.json` with per-entry classification details and gate evaluation
- **Falsification record**: To be linked in FAILURES-findings if G1 FAIL; if G1 PASS, documents the generalizability finding

---

### Next Steps (per Outcomes)

**If G1 FAIL**: The instrument cannot reliably filter known-unserved from the E083 ground truth. This confirms the view-count-based classifier's limitations in fault-code domains and supports the SUMMARY.md conclusion: "population measurement is unfalsifiable and should not proceed." The way forward would be a different instrument approach (e.g., human judgment of actual resolution guides, platform-specific metrics, different classification strategy), or accepting that this route is closed per D083/D095.

**If G1 PASS**: The instrument successfully filters known-unserved from the E083 ground truth (FPR < 0.10). However, since 0/30 are served per hand classification, population measurement in this domain is still unfalsifiable — the instrument can identify unserved needs, but there are no served needs to measure against. The finding would support D095's constraint: "the next session must not start from classify_served over Bing in an eighth domain," and STATE.md §267: "the next work is not another domain and not another screen."

**If G1 PASS but G2/G3 documented as not evaluable**: The instrument has discriminative power for the unserved/served distinction on available features, but the E083 ground truth has 0 served entities. This result would be informative for instrument designers: the core features (error code presence, resolution keywords) can separate unserved from served+inconclusive in some domains, but fault-code domains may have a distinct distribution (0 served) that requires different instrumentation.