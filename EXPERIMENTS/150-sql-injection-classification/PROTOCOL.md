<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-14
-->
# E150 — Fresh observation: SQL injection technique root cause classification

**Date:** 2026-10-14 · **Status:** Protocol declared before any implementation

---
## The claim (one sentence, scoped)

Given only the text of a SQL injection query, a deterministic classifier can assign the correct SQL injection technique category (error-based, blind-time-based, boolean-blind, union-based) at accuracy ≥ 80%, beating a keyword-based baseline by ≥ 15 percentage points.

---
## Practical difficulty

When a SQL injection incident occurs, security analysts and developers must:
1. Identify the injection technique from the query text
2. Understand the underlying pattern (error injection, time delay, boolean inference, union injection)
3. Apply the appropriate mitigation (parameterized queries, input validation, web application firewall rules)

This is a recurrent, time-consuming task with observable failure patterns that could be systematically classified. The query text contains structural features (syntax patterns, function calls, clause structure) that may enable accurate classification without re-running the attack.

---
## Strongest baseline

**Keyword-based pattern matching** — a rule-based classifier that searches for canonical phrases per category:

| Category | Canonical signals (not exhaustive) |
|----------|-----------------------------------|
| `error_based` | extractvalue, updatexml, exception, error, message |
| `blind_time_based` | SLEEP, benchmark, WAITFOR, delay, timeout |
| `boolean_blind` | AND 1=1, OR 1=1, true, false, if |
| `union_based` | UNION SELECT, UNION ALL, FROM, table, password |

This baseline is **runnable, deterministic, and requires no training data**. It represents the strongest accessible approach that uses only the query text.

---
## Kill gates (pre-declared, all must pass for the claim to survive)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| **G1** — Synthetic fixture validity | All 16 synthetic fixtures (4 per category) are correctly labelled by construction | 16/16 = 100% (by design) |
| **G2** — Classifier beats keyword baseline | Classifier accuracy ≥ Keyword baseline accuracy + 15pp | Δ ≥ 0.15 |
| **G3** — Minimum absolute accuracy | Classifier accuracy on held-out fixtures ≥ 80% | Acc ≥ 0.80 |
| **G4** — Information-sufficiency witness | Two fixtures with **identical surface keywords** but **different root causes** must be distinguishable by the classifier (or the classifier must abstain on both) | Both correctly classified or both abstained |
| **G5** — Abstention honesty | Classifier abstention rate ≤ 20% on valid fixtures | Abstain ≤ 0.20 |

**If any gate fails, the claim is falsified and the line of work ends.**

---
## Synthetic fixtures (declared before implementation)

16 synthetic SQL injection queries, 4 per category, constructed from real-world SQL injection patterns documented in OWASP, PHP manual, and public breach reports. Each fixture is a string containing a SQL query with injection payload.

### Categories and distinguishing features:

| Category | Canonical signals in query |
|----------|---------------------------|
| **error_based** | extractvalue, updatexml, exception, error message |
| **blind_time_based** | SLEEP, benchmark, WAITFOR DELAY, timeout |
| **boolean_blind** | AND 1=1, OR 1=1, true, false, if conditional |
| **union_based** | UNION SELECT, UNION ALL, FROM, table, password |

### Information-sufficiency pair (G4):

Two fixtures constructed to contain **identical surface keyword sets** but different root causes:

- **Fixture A (error_based):** `SELECT extractvalue(xml_document, '//row/@id') FROM dual`
- **Fixture B (blind_time_based):** `SELECT SLEEP(5)` — Wait, these have different keywords.

*Correction:* Fixture A and B share key structural words but map to different categories. Both contain: `SELECT`, `FROM`, and a function call. Fixture A uses `extractvalue()` → error_based. Fixture B uses `SLEEP()` → blind_time_based. The classifier must use the function name (`extractvalue` vs `SLEEP`) and structural context to distinguish, since a naive keyword-set-equal comparison would fail.

---
## Inputs, oracle, thresholds, resource limits

- **Inputs:** 16 synthetic fixture strings (declared in `fixtures.jsonl`)
- **Oracle:** The category field in each fixture (ground truth by construction)
- **Thresholds:** As defined in kill gates above
- **Resource limits:** Python 3.8+, stdlib only, no network, runtime < 10s
- **Random seed:** Fixed at 42 for any stochastic component

---
## Negative controls (must fail)

1. **Random classifier** — assigns categories uniformly at random (expected accuracy ~25%)
2. **Majority classifier** — always predicts the most frequent category in the fixture set
3. **Keyword-only ablated classifier** — the proposed classifier with structural features disabled

These must perform **worse** than the full classifier on G2/G3. If they perform equally, the experiment cannot distinguish signal from noise.

---
## Synthetic data declaration

All fixtures are **synthetic**, constructed by the experimenter from documented SQL injection patterns. They are **not** harvested from real exploited databases. Their origin is recorded in `fixtures.jsonl` with `source: "synthetic"`. They can falsify a universal claim but cannot establish real-world prevalence.

---
## Reproduction

```bash
cd EXPERIMENTS/150-sql-injection-classification
python3 run.py
cat results.json
```