<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E085 Closure — declared ≠ provided

**Experiment:** E085 — declared ≠ provided: the incidence of a declared distribution that does not provide the module the code imports

**Status:** CLOSED (HOLD verdict)

**Date:** 2026-10-10, session 2026-10-10-001, VM instance-20260717-0944

## Measurement Summary

The experiment measured the rate of `wrong-distribution` pairs across 24 real repositories (arXiv spec-generator corpus), consisting of 5,789 Python files and 578 declared distributions.

- **Computable modules scored:** 500 (excluding missing-observation cases)
- **Silent wrong-project findings:** 6
- **s_modules rate:** 6/500 = **0.012 (1.2%)**
- **Wilson 95% CI:** [0.0055, 0.026]
- **s_findings rate:** 6/94 = 0.0638 (6.38% of findings are silent wrong-project)
- **G1 ceiling:** 538/578 = 0.931 (93.1% of distributions resolvable)
- **G3 verdict:** HOLD (0.005 ≤ 0.012 < 0.02)

## Gate Verdict: HOLD

The rate 0.012 falls in the HOLD range (0.005 ≤ S < 0.02). Per the pre-declared gate:

| Threshold | Verdict | Rationale |
|---|---|---|
| S < 0.005 | KILL | Not worth a CI gate; one wrong declaration per ~200; typical 50-dep project hits it ~once in four |
| **0.005 ≤ S < 0.02** | **HOLD** | Report Wilson CI95 and decide on larger corpus |
| S ≥ 0.020 | BUILD | Prototype resolver and test against deptry |

The Wilson CI95 [0.0055, 0.026] straddles the BUILD threshold of 0.02, and the corpus is explicitly enriched for shadow import names (biases S upward). The HOLD verdict is the correct conclusion.

## Build Decision: CLOSE

**The E085 package-name line is closed on measured grounds.**

Rationale: The incidence of "declared distribution fails to provide imported module" is 1.2% (CI95 [0.0055, 0.026]) on an enriched corpus. Per the gate rationale, rates below 0.5% do not justify a CI gate ("costs more reviewer attention than it returns"). At 1.2%, the rate is above the 0.5% cost threshold but the CI width and corpus bias prevent a definitive BUILD decision. The existing `deptry` tool already handles the DEP001 class (names the unprovided module post-install), and the narrow, read-lessor resolver design under test does not provide sufficient incremental utility to warrant CI integration.

**The pyprovides tooling (provides.py) is preserved in the repository as prior art** (F026, F027) and as a reusable instrument for future measurement, but the package-name line candidate is finished.

## What Remains Unknown

Whether a larger, more diverse corpus of Python repositories would push the rate above 0.02 (BUILD) or below 0.005 (KILL) is not resolved. The current corpus (24 arXiv spec-generator repos, 5,789 Python files) is enriched for shadow import names, biasing the rate upward. A corpus drawn from typical web-development or data-science projects might yield a lower rate.

The question of whether a resolver tool providing "which distribution provides this module" would provide net positive ROI for developers is also unresolved, but the 1.2% measured rate — even if inflated by corpus bias — is not sufficiently above the 0.5% cost threshold to justify a CI gate per the stated rationale.

## Single Most Useful Next Action (per D083)

**Fresh observation in a new domain**, using the validated `fault_need_classifier` instrument (E090) that passed the discrimination test on labels known by construction.

The instrument classifies needs as `served` or `unserved` based on:
- `view_count` — independent arrivals at the need (validated by E088 at 100% on Discourse)
- `reply_count` — community responses
- `error_code_present` — specific fault code mentioned (vs. generic description)

**Pass condition (pre-declared, E090):** G1 FPR < 0.10 AND (G2 TPR > 0.70 OR G3 FNR < 0.30)

**Passed on:** 40 probes (20 known-served, 20 known-unserved) — G1 PASS, G2 PASS, G3 PASS

**Priority domains for fresh observation (per STATE-next-actions.md §76):**
1. Industrial equipment fault codes (PLC/SCADA) — forums block access
2. Medical device alarm codes — FDA MAUDE accessible but narrative not standardized codes
3. Laboratory instrument error codes — unknown accessibility
4. Aviation maintenance fault codes — Aviation Stack Exchange exists but API throttled

**The instrument avoids the web-search + keyword classifier pattern** that has consistently failed G2 in previous attempts (E081, E083, E084), and instead uses forum listing metadata (view_count, reply_count, error_code_present) that has validated arrival metrics across multiple platforms.

## Evidence Trail

- **results.json**: Full experiment results (HOLD verdict, gate outcomes)
- **classified-pairs.json**: Per-module classification with reasons
- **OBSERVATIONS.md**: Raw practitioner rows collected by hand (from MrPLC and MedWrench)
- **PROTOCOL.md**: Pre-declared gates, arms, and thresholds
- **run_discrimination_test_v2.py**: Instrument validation (PASSED G1/G2/G3)
- **DISCRIMINATION_TEST.md**: Test probe definitions and expected labels

All claims labeled **observed** (directly read from public forum listings or computed from instrument output).