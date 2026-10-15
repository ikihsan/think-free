<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E147 — Fresh observation: PostgreSQL deadlock report root cause classification

**Date:** 2026-10-14 · **Status:** Protocol declared before any implementation

---

## The claim (one sentence, scoped)

**Given only the text of a single PostgreSQL deadlock report (from `log_lock_waits` or `deadlock_timeout`), a deterministic classifier can assign the correct root cause category (foreign key lock contention, index lock contention, tuple lock contention, advisory lock contention, explicit locking) at accuracy ≥ 80%, beating a keyword-based baseline by ≥ 15 percentage points.**

---

## Practical difficulty

When a PostgreSQL deadlock occurs, developers and DBAs must:
1. Find the deadlock report in logs (often buried in verbose output)
2. Parse the report to understand which processes, queries, and locks are involved
3. Identify the root cause pattern (FK checks, index updates, tuple updates, etc.)
4. Apply the correct fix (query reordering, index changes, isolation level, advisory locks)

This is a recurrent, time-consuming task with observable failure patterns that could be systematically classified. The deadlock report contains structured information (process IDs, lock modes, relation names, query text) that may enable accurate classification without re-running the workload.

---

## Strongest baseline

**Keyword-based pattern matching** — a rule-based classifier that searches for canonical phrases per category:

| Category | Canonical signals (not exhaustive) |
|----------|-----------------------------------|
| `fk_lock_contention` | `ShareLock`, `FOR KEY SHARE`, `FOR SHARE`, `FOR NO KEY UPDATE`, `FOR UPDATE`, `trigger`, `foreign key`, `references` |
| `index_lock_contention` | `index`, `btree`, `hash`, `gin`, `gist`, `page`, `tuple`, `insert`, `unique`, `duplicate key` |
| `tuple_lock_contention` | `tuple`, `heap`, `update`, `delete`, `lock_tuple`, `FOR UPDATE`, `FOR NO KEY UPDATE`, `ctid` |
| `advisory_lock_contention` | `advisory`, `pg_advisory_lock`, `pg_advisory_xact_lock`, `pg_try_advisory_lock` |
| `explicit_lock_contention` | `LOCK TABLE`, `pg_sleep`, `pg_advisory_lock`, `exclusive`, `access exclusive` |

This baseline is **runnable, deterministic, and requires no training data**. It represents the strongest accessible approach that uses only the deadlock report text.

---

## Kill gates (pre-declared, all must pass for the claim to survive)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| **G1** — Synthetic fixture validity | All 25 synthetic fixtures (5 per category) are correctly labelled by construction | 25/25 = 100% (by design) |
| **G2** — Classifier beats keyword baseline | Classifier accuracy ≥ Keyword baseline accuracy + 15pp | Δ ≥ 0.15 |
| **G3** — Minimum absolute accuracy | Classifier accuracy on held-out fixtures ≥ 80% | Acc ≥ 0.80 |
| **G4** — Information-sufficiency witness | Two fixtures with **identical surface keywords** but **different root causes** must be distinguishable by the classifier (or the classifier must abstain on both) | Both correctly classified or both abstained |
| **G5** — Abstention honesty | Classifier abstention rate ≤ 20% on valid fixtures | Abstain ≤ 0.20 |

**If any gate fails, the claim is falsified and the line of work ends.**

---

## Synthetic fixtures (declared before implementation)

25 synthetic deadlock reports, 5 per root cause category, constructed from real-world patterns observed in PostgreSQL documentation, mailing lists, and public bug reports. Each fixture is a string containing a realistic deadlock report with process details, lock information, and query text.

### Categories and distinguishing features:

| Category | Canonical signals in deadlock report |
|----------|-------------------------------------|
| **fk_lock_contention** | Process holds `ShareLock` on referenced table; waiting process requests `RowExclusiveLock` for FK check; query shows `INSERT`/`UPDATE` on referencing table with `FOR KEY SHARE`/`FOR SHARE` on referenced |
| **index_lock_contention** | Processes contend on index pages/btree locks; queries show concurrent `INSERT`/`UPDATE` on same index; `duplicate key value violates unique constraint` often present |
| **tuple_lock_contention** | Processes hold conflicting tuple locks (`FOR UPDATE` vs `FOR NO KEY UPDATE`); same `ctid` or heap tuple referenced; concurrent `UPDATE`/`DELETE` on same row |
| **advisory_lock_contention** | Lock type shows `advisory`; `pg_advisory_lock`/`pg_advisory_xact_lock` in query; no table/index relations involved |
| **explicit_lock_contention** | `LOCK TABLE` statements; `AccessExclusiveLock` or `ExclusiveLock` modes; explicit locking in application code |

### Information-sufficiency pair (G4):

Two fixtures constructed to contain **identical keyword sets** (`lock`, `wait`, `process`, `relation`, `ShareLock`) but different root causes:

- **Fixture A (fk_lock_contention):** Process 1 holds `ShareLock` on `parent` table; Process 2 waits for `RowExclusiveLock` on `parent` while inserting into `child` (FK check)
- **Fixture B (tuple_lock_contention):** Process 1 holds `RowExclusiveLock` on `items` tuple; Process 2 waits for `RowExclusiveLock` on same `items` tuple (concurrent UPDATE)

Both contain keywords: `lock`, `wait`, `process`, `relation`, `ShareLock`, `RowExclusiveLock`, `tuple`. Keyword-only classifier maps both to same category → G4 fails. The classifier must use structural cues (lock mode combinations, relation pairs, query patterns) to distinguish.

---

## Inputs, oracle, thresholds, resource limits

- **Inputs:** 25 synthetic fixture strings (declared in `fixtures.jsonl`)
- **Oracle:** The `category` field in each fixture (ground truth by construction)
- **Thresholds:** As defined in kill gates above
- **Resource limits:** Python 3.8+, stdlib only, no network, runtime < 10s
- **Random seed:** Fixed at 42 for any stochastic component

---

## Negative controls (must fail)

1. **Random classifier** — assigns categories uniformly at random (expected accuracy ~20%)
2. **Majority classifier** — always predicts the most frequent category in training (if any)
3. **Keyword-only ablated classifier** — the proposed classifier with structural features disabled

These must perform **worse** than the full classifier on G2/G3. If they perform equally, the experiment cannot distinguish signal from noise.

---

## Synthetic data declaration

All fixtures are **synthetic**, constructed by the experimenter from documented PostgreSQL deadlock patterns. They are **not** harvested from real production deadlocks. Their origin is recorded in `fixtures.jsonl` with `source: "synthetic"`. They can falsify a universal claim but cannot establish real-world prevalence.

---

## Reproduction

```bash
cd EXPERIMENTS/147-postgres-deadlock-classification
python3 run.py
cat results.json
```