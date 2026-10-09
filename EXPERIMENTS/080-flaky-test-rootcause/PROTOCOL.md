<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E080 — Fresh observation: Can flaky test failure logs classify root causes without re-runs?

**Date:** 2026-10-09 · **Status:** Protocol declared before any implementation

---

## The claim (one sentence, scoped)

**Given only the failure log text of a single flaky test run (stdout/stderr/traceback), a deterministic classifier can assign the correct root cause category (timing, concurrency, external dependency, test pollution, random seed, resource exhaustion) at accuracy > 70%, beating a keyword-based baseline by ≥ 15 percentage points.**

---

## Strongest baseline

**Keyword-based pattern matching** — a rule-based classifier that searches for canonical phrases per category:
- timing: `timeout`, `timed out`, `deadline exceeded`, `took longer`
- concurrency: `deadlock`, `race condition`, `lock`, `mutex`, `concurrent`, `thread`
- external dependency: `connection refused`, `connection reset`, `dns`, `network`, `unreachable`, `503`, `504`, `rate limit`
- test pollution: `state`, `fixture`, `teardown`, `setup`, `shared`, `global`, `singleton`, `cache`
- random seed: `random`, `seed`, `flaky`, `non-deterministic`, `intermittent`
- resource exhaustion: `memory`, `oom`, `disk`, `space`, `quota`, `limit`, `ulimit`, `file descriptor`

This baseline is **runnable, deterministic, and requires no training data**. It represents the strongest accessible approach that uses only the failure log text.

---

## Kill gates (pre-declared, all must pass for the claim to survive)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| **G1** — Synthetic fixture validity | All 30 synthetic fixtures (5 per category) are correctly labelled by construction | 30/30 = 100% (by design) |
| **G2** — Classifier beats keyword baseline | Classifier accuracy ≥ Keyword baseline accuracy + 15pp | Δ ≥ 0.15 |
| **G3** — Minimum absolute accuracy | Classifier accuracy on held-out fixtures ≥ 70% | Acc ≥ 0.70 |
| **G4** — Information-sufficiency witness | Two fixtures with **identical surface keywords** but **different root causes** must be distinguishable by the classifier (or the classifier must abstain on both) | Both correctly classified or both abstained |
| **G5** — Abstention honesty | Classifier abstention rate ≤ 30% on valid fixtures | Abstain ≤ 0.30 |

**If any gate fails, the claim is falsified and the line of work ends.**

---

## Synthetic fixtures (declared before implementation)

30 synthetic failure logs, 5 per root cause category, constructed from real-world patterns observed in public CI logs (GitHub Actions, GitLab CI, CircleCI, Azure Pipelines). Each fixture is a string containing realistic traceback, error message, and context.

**Categories and distinguishing features:**

| Category | Canonical signals (not exhaustive) |
|----------|-----------------------------------|
| **timing** | Test exceeds configured timeout; explicit `TimeoutError`, `pytest-timeout`, CI job timeout |
| **concurrency** | Thread/process interaction bugs; `Deadlock`, `RaceCondition`, lock contention, `asyncio` task collision |
| **external_dependency** | Network/service failures; DNS, connection refused/reset, HTTP 5xx, rate limits, service unavailable |
| **test_pollution** | Shared mutable state between tests; fixture leakage, global variable contamination, database state bleed |
| **random_seed** | Non-determinism from RNG; hash randomization, test order dependence, `random.seed` not set |
| **resource_exhaustion** | OOM, disk full, file descriptor exhaustion, CPU quota, memory limit |

**Information-sufficiency pair (G4):** Two fixtures constructed to contain **identical keyword sets** (`timeout`, `connection`, `error`, `failed`) but different root causes:
- Fixture A (timing): Test hits CI job timeout after 3600s, last log line shows successful DB query
- Fixture B (external_dependency): Test fails with "connection timeout" to external API, retry exhausted

If the classifier uses only keywords, both map to same category → G4 fails. The classifier must use structural/contextual cues (position in log, exception type, stack trace shape) to distinguish.

---

## Inputs, oracle, thresholds, resource limits

- **Inputs:** 30 synthetic fixture strings (declared in `fixtures.jsonl`)
- **Oracle:** The `category` field in each fixture (ground truth by construction)
- **Thresholds:** As defined in kill gates above
- **Resource limits:** Python 3.8+, stdlib only, no network, runtime < 10s
- **Random seed:** Fixed at 42 for any stochastic component

---

## Negative controls (must fail)

1. **Random classifier** — assigns categories uniformly at random (expected accuracy ~16.7%)
2. **Majority classifier** — always predicts the most frequent category in training (if any)
3. **Keyword-only ablated classifier** — the proposed classifier with structural features disabled

These must perform **worse** than the full classifier on G2/G3. If they perform equally, the experiment cannot distinguish signal from noise.

---

## Synthetic data declaration

All fixtures are **synthetic**, constructed by the experimenter from documented failure patterns. They are **not** harvested from real CI runs. Their origin is recorded in `fixtures.jsonl` with `source: "synthetic"`. They can falsify a universal claim but cannot establish real-world prevalence.

---

## Reproduction

```bash
cd EXPERIMENTS/080-flaky-test-rootcause
python3 run.py
cat results.json
```