<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E144 — Fresh observation: recurring payment detection on real OFX merchant strings

**Date:** 2026-10-15 · **Status:** Protocol declared before any implementation

---

## The claim (one sentence, scoped)

Given real OFX bank export files with messy merchant strings (e.g., `AMZN Mktp US*2Y4LM8XY3`, `SQ *BLUE BOTTLE 1234`, `PAYPAL *SOMEONE`, `VERIZON DES:PAYMENTREC ID:XXXXX3`), the deterministic interval+amount detector from E065/E066 (imported unmodified) recovers recurring payments at micro-F1 ≥ 0.80, with precision ≥ 0.70 and recall ≥ 0.90, on a predeclared sample of real OFX files from self-hosted finance tool test fixtures.

---

## Practical difficulty

When users export bank data from modern banks (OFX, QFX, CSV), the merchant strings are noisy and inconsistent:
- Truncated names: `VERIZON DES:PAYMENTREC ID:XXXXX3` vs `VERIZON`
- Payment processor prefixes: `SQ *BLUE BOTTLE 1234` vs `BLUE BOTTLE`
- Random suffixes: `AMZN Mktp US*2Y4LM8XY3` vs `AMAZON`
- Inconsistent capitalization and spacing

E066 validated the interval+amount core on Berka data (clean `k_symbol` grouping, F1 0.8194) but explicitly noted: "Not established: the merchant-name axis. Berka has no merchant text, so grouping here is cleaner than real bank-export strings." E116's service test used the same clean grouping.

This experiment tests whether the detector's existing merchant normalization (`normalize.py`) is sufficient for real OFX merchant strings, or whether merchant normalization is the bottleneck.

---

## Strongest baseline

**Naive ≥3 debits per normalized merchant** — the same baseline E065/E066 used. If the detector cannot beat this on real OFX data, the mechanism adds nothing.

---

## Kill gates (pre-declared, all must pass for the claim to survive)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| **G1** — Real positive recovery | Micro-recall on positive groups | ≥ 0.90 |
| **G2** — Real-world precision | Micro-precision on positive groups | ≥ 0.70 |
| **G3** — Baseline dominance | Detector micro-F1 − naive micro-F1 | ≥ 0.05 |
| **G4** — Instrument can say no | Permutation control (date shuffle destroys interval structure, detections ≤ 10% of unshuffled) | ≤ 0.10 |

**If any gate fails, the claim is falsified and this line of work ends.**

---

## Data

**Source:** OFX test fixtures from Actual Budget (loot-core), Firefly III, and beancount test suites. These are real OFX files committed to public repositories by the projects' maintainers for testing their own import pipelines.

**Provenance:** All files fetched from GitHub raw URLs with sha256 recorded in `raw/SOURCES.md`. Files are:
- `packages/loot-core/src/mocks/files/credit-card.ofx` (Apple Card)
- `packages/loot-core/src/mocks/files/data.ofx` (Bank of America)
- `packages/loot-core/src/mocks/files/data-multi-decimal.ofx`
- `packages/loot-core/src/mocks/files/data-payee-memo.ofx`
- Any OFX/QFX files in Firefly III test fixtures
- Any OFX/QFX files in beancount examples/ingest

**Limitations declared upfront:**
- These are test fixtures, not production exports — may be small, synthetic, or curated
- No ground truth labels exist — we must create them by manual inspection of the transaction lists
- The population is not the subscription economy broadly; it's whatever recurring payments happen to be in these test files

---

## Predeclared mapping (OFX → E065 normalized transaction)

- `DTPOSTED` → `date` (datetime.date)
- `TRNAMT` → `amount` (negative for DEBIT, positive for CREDIT). Detector reads only debits.
- `NAME` (and `MEMO` if present) → `merchant` — concatenated as `NAME | MEMO` if both exist, else whichever exists
- `FITID` → ignored (transaction ID)

**Merchant normalization:** The detector's existing `normalize_merchant()` from `normalize.py` is applied **unchanged**. This is the test: does the existing normalization handle real OFX merchant noise?

---

## Predeclared labeling (ground truth creation)

Since OFX test fixtures have no labels, we create them **before running the detector**:

1. Parse all OFX files, extract all debit transactions with merchant strings
2. Manually inspect each unique merchant string and label as:
   - **Positive (recurring):** Clear subscription, utility, insurance, loan, membership, or standing order
   - **Negative (non-recurring):** One-off purchases, variable retail, food, transport
   - **Ambiguous:** Cannot determine — excluded from both arms
3. Commit labels in `labels.jsonl` **before** running detector
4. The detector and naive baseline are then evaluated against these committed labels

---

## Predeclared sample

All accounts/transactions from all fetched OFX files. No stratification — the population is small by construction (test fixtures).

---

## Inputs, oracle, thresholds, resource limits

- **Inputs:** OFX files from `raw/`, committed labels from `labels.jsonl`
- **Oracle:** Committed labels (positive merchant groups)
- **Thresholds:** As defined in kill gates above
- **Resource limits:** Python 3.8+, stdlib only, no network after fetch, runtime < 30s
- **Random seed:** Fixed at 42 for permutation control

---

## Negative controls (must fail)

1. **Random classifier** — assigns categories uniformly at random
2. **Majority classifier** — always predicts most frequent label
3. **Naive ≥3 debits** — the baseline from E065

These must perform **worse** than the full detector on G1/G2/G3. If they perform equally, the experiment cannot distinguish signal from noise.

---

## Synthetic data declaration

**No synthetic data.** All inputs are real OFX files from public repositories. Labels are created by manual inspection of real merchant strings.

---

## Reproduction

```bash
cd EXPERIMENTS/144-ofx-merchant-noise
python3 fetch.py        # fetch OFX files -> raw/
python3 label.py        # interactive labeling -> labels.jsonl (committed before detection)
python3 parse_ofx.py    # raw/ -> transactions.jsonl (normalized)
python3 score.py        # transactions.jsonl + labels.jsonl -> gates.json
python3 -m unittest test_e144  # the checks the numbers depend on
```