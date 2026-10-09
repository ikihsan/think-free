<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-09
-->

# E073 — piecewise-constant price model vs the CV ceiling

**Date:** 2026-10-09 · **Status: complete — G1 and G2 fail. The pwc repair
improves every metric over the CV ceiling but does not meet the predeclared
gates. The detector line remains closed (F185, D090).**

Protocol (predeclared before any pwc detector ran): [`PROTOCOL.md`](PROTOCOL.md).
Measurements: [`results.json`](results.json). Gates: [`verdict.json`](verdict.json).
Hand-read census: [`added_labels.json`](added_labels.json).

## The one-line result

**The piecewise-constant amount gate is a real improvement over E065's CV
ceiling — more true positives, fewer false positives, higher precision and
recall — but it recovers only 2 of the 14 CV-gate misses, not enough to
reach the predeclared recall gate, and it does not beat the incumbent by the
predeclared margin.**

## What was asked

E072 closed E065's detector on 36 real bank exports and attributed 14 of 20
misses to an amount-consistency gate nobody had questioned: a fixed 0.15
amount-CV ceiling that treats a price change as evidence of non-recurrence.
E073 tested the diagnosis with a different mechanism: replace the CV ceiling
with a piecewise-constant price model that admits exactly one price change
(at most 2 constant amount segments). The predeclared gates were recall ≥ 0.50
(G1) and F1 margin over the incumbent ≥ +0.05 (G2).

## Results (observed)

| arm | precision | recall | F1 | TP | FP | FN | groups |
|---|---|---|---|---|---|---|---|
| `e065_raw` (frozen E065 baseline) | 0.100 | **0.394** | **0.160** | 13 | 117 | 20 | 130 |
| `e073_pwc_raw` (pwc gate, primary) | **0.126** | **0.455** | **0.197** | 15 | 104 | 18 | 119 |
| `e073_pwc_norm` (pwc on normalized) | 0.121 | 0.455 | 0.191 | 15 | 109 | 18 | 124 |
| `actual_raw` (incumbent) | 0.091 | 0.424 | 0.150 | 14 | 140 | 19 | 154 |
| `naive` (≥3 debits) | 0.018 | 0.697 | 0.035 | 23 | 1263 | 10 | 1286 |

| gate | threshold | observed | result |
|---|---|---|---|
| **G0** fidelity | reproduce E072 exactly | P 0.100 / R 0.394 / F1 0.160, TP 13 / FP 117 / FN 20 | ✅ |
| **G1** recall ≥ 0.50 | 0.50 | **0.455** | ❌ |
| **G2** F1 margin ≥ +0.05 | +0.05 | **+0.048** | ❌ |
| **G3** permutation ≤ 0.10 | 0.10 | 0.000 (0/99 both arms) | ✅ |
| **G5** leave-one-out | direction stable | stable (dropping a00) | ✅ |
| **P1a** precision ≥ baseline − 0.02 | 0.080 | **0.126** | ✅ |
| **P1b** added groups ≥ 0.80 recurring | 0.80 | 13/17 strict (0.765), 16/17 with impure (0.941) | ✅ borderline |

## What the run established

**The pwc model is strictly better than the CV ceiling on every count.**
Against `e065_raw` it adds 2 true positives, removes 13 false positives,
and drops 2 false negatives. Precision rises (0.100 → 0.126), recall rises
(0.394 → 0.455), F1 rises (0.160 → 0.197). The 17 added groups are real
price-change subscriptions — 13 unambiguously, 3 with a real recurring
component mixed with a one-time charge. This is not a CV-ceiling relaxation:
a loosened CV would add groups with no recurring pattern, and the pwc model
rejects groups with 3+ amount segments (drift, oscillation, second steps).

**But it recovers only 2 of the 14 CV-gate misses.** E072 attributed 14
misses to the CV ceiling. The pwc model finds 2 of them (the one-price-step
Spotify subscriptions a35/a36 and Comcast). The other 12 have amount shapes
a one-step model cannot capture: drift (State Farm, Progressive), oscillation
(AT&T, T-Mobile), or multiple changes (Amazon Prime FR with 13 segments,
ChatGPT with 5). The diagnosis was directionally right — the amount gate was
the binding constraint for a *measurable set* of real subscriptions — but
the repair is narrower than the diagnosis predicted.

**The pwc model drops 27 groups E065 accepted, including 2 watchlist hits.**
Brightwheel (3 segments, watchlist hit) and TELEKOM (9 segments, watchlist
hit) are real subscriptions whose amounts have more than 2 segments. The pwc
model correctly rejects them as non-piecewise-constant, but they are real
recurring expenses the model cannot see. This is a real cost of the stricter
gate.

**The model's weakness: it cannot distinguish a price step from a one-time
purchase plus a subscription.** Three added groups (Apple $138 + $5.36/month,
Fedloanservicing $13,500 + $750/month, Twitch $114 + $5.71/month) have a
one-time charge followed by a recurring charge at a different amount. The
pwc model sees 2 segments and accepts them, exactly as it would a price
change. The recurring component is real, but the group is impure.

## What this closes, and what it does not

**Closed, on this population:** the piecewise-constant price model as a
replacement for the CV ceiling. It is a better mechanism — every metric
improves and the added groups are real — but it does not reach the predeclared
gates. G1 (recall ≥ 0.50) and G2 (F1 margin ≥ +0.05) both fail. The detector
line remains closed (F185, D090).

**The remaining misses are a different problem.** The 12 CV-gate misses the
pwc model cannot recover have amount shapes that need a richer model (drift,
seasonality, multiple changes) — or they are not recurring at all (payroll,
mortgage escrow with varying amounts). No predeclared gate in this
experiment tests those.

**Not claimed:** anything about usefulness, adoption, or a market. The
incumbent (Actual Budget's `findSchedules`) scores F1 0.150 on the same rows
and is a *lower bound* on the production tool (D090). Even a pass would not
have started the differentiation question.

## Harness repairs (defect-class, no gate/arm/threshold change)

Two repairs were needed before the first clean run, both logged in the
session event stream:

1. **Mixed-side filter (G0-breaking).** An earlier version of `load_all()`
   filtered mixed-side accounts, claiming it was "E072's rule." It is not —
   E072 loads all 36 accounts. The filter dropped a00 and a14 (2,612
   transactions, 1 TP, 26 FP, 1 FN) and made G0 fail. Removed to match
   E072's loading byte-for-byte.
2. **Census KeyError.** `pwc_accepted` pre-initialized only `segments_1` and
   `segments_2`, but `describe_group` reported a 4-segment group. Changed to
   `dict.get`-based counting.

A third repair (census view including positive-credit rows the detector never
sees) was logged in the session before the first run and is in the event
stream.

## Reproduction

```bash
cd EXPERIMENTS/073-piecewise-price
python3 eval_arms.py    # run all five arms, write results.json + census JSONs
cat verdict.json       # gate evaluation
cat added_labels.json  # P1b hand-read census
```

Environment: Python 3.8.10, stdlib only, no network. Runtime ≈ 90s on this
VM (2 CPUs). The corpus is E072's frozen `raw/CORPUS.json`, loaded through
E072's own `corpus.py` and `arm_sign.py`.
