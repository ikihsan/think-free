<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Findings — part 35

Split out of [`FAILURES-findings-34.md`](FAILURES-findings-34.md) on
2026-10-09. Finding **F185**. See [`STATE.md`](STATE.md) for the reload point.

## F185 — E066's detector does not transfer to real modern subscription data, and the reason is the amount gate, not the merchant gate (2026-10-09)

`observed` 2026-10-09, session 2026-10-09-002, E072.
Population: **36 real bank exports, 34,231 transactions, 29 public
repositories, 2021–2026**, hand-read watchlist of 18 distinct subscription
merchants. Instrument: E065's `detect.py`, unmodified.

**The claim this closes.** E066 recorded the only line in this repository with
all four predeclared gates passing on real data (P 0.7006 / R 0.9867 / F1
0.8194, permutation control 0.0022) and named its own open question: *Berka
carries no merchant text, so grouping here is cleaner than any real bank-export
string.* E072 ran it on exports that do carry merchant text. **Recall 0.394,
F1 0.160. G1 (recall ≥ 0.50) and G2 (F1 margin over Actual Budget's shipping
`findSchedules` ≥ +0.05, observed +0.0098) did not fire.** No candidate, no
prototype.

**The failure is not the one the record predicted.** Decomposing the 20 missed
watchlist families by cause:

1. **Under-grouping — 6 misses, and it is the axis E066 named.**
   `normalize.py` strips a trailing run of `≥4 digits`; card processors emit
   3-character and mixed alphanumeric references, so `AMAZON PRIME*111` and
   `AMAZON PRIME*7U1` both survive verbatim. **13 rows → 13 normalized names,
   21 → 21, 12 → 12, 13 → 13.** Each fragment falls under the `n ≥ 3` floor.
2. **The amount-consistency gate — 14 misses, and it was never predicted.**
   `detect.py` rejects any group with amount CV > 0.15. Five accounts pay for
   the same subscription monthly on the same day: a34 (CV 0.048) is detected;
   a36 (0.151), a35 (0.225), a11 (0.318), a28 (0.352) are not. **One price
   change and the detector stops seeing it.** a35 and a36 have *higher* interval
   regularity than the detected a34.

**Why E066 could not see this, from E066's own record.** E066's README reports
its false positives as *"all 159 monthly, amount CV ≈ 0.000"*. In 1990s Czech
retail banking a standing order's amount does not drift. **The gate E066 passed
four times was never exposed to a price change**, so passing it said nothing
about a population where subscription prices move. E066 also estimated its 159
false positives as *"overwhelmingly real recurring payments"* — and the label
gap it inferred was correct; what it could not see is that the same
CV ≈ 0.000 that made the false positives look like rent also made the true
positives look like nothing had changed.

**Second finding inside the same run: the incumbent comparison is a floor, not
a contest.** Actual Budget ships `findSchedules()`, an automatic
recurring-payment detector. E072 ported it (285 lines, stdlib only) and ran it
on the same rows: F1 **0.150** against E065's **0.160**. Two detectors within
0.01 of each other, both far below usefulness, is a statement about the
population, not about either. `actual_shared` — both given E065's merchant
axis — is 0.146 vs 0.141: **the interval/amount engines are within noise of
each other, so the engine is not the differentiator and the merchant axis is.**
And because Actual's production matcher runs on a payee its importer has
already cleaned, `actual_raw` is a **lower bound on the incumbent**, not a fair
fight.

**A third, about this repository's own record-keeping.** `precision` computed
against the watchlist reads **0.100**; a hand-read stratified sample of 13
unclaimed groups reads **0.91** — the difference between counting a mortgage
auto-pay and a school meal plan as errors and not counting them. Both numbers
are in `results.json`. A precision figure against a positives-only label set
is not a precision figure, and E065's headline 1.0000 was measured against
labels that *were* positives-only. It is a **lower bound that happened to sit
at 1.0 on synthetic data with no unclaimed groups in it.**

**What survives.** Not the detector. The *question*, with a bounded repair
already visible in the evidence: a24's ChatGPT — 9 × $20.00, CV **0.000**,
interval regularity 0.922, score 0.915 — is detected today. The five Spotify
accounts are the same mechanism with one price step between them, and they are
missed. **A detector that models piecewise-constant price rather than rejecting
on CV is a different mechanism from E065's, it is the next experiment, and it
is not a retune.** See the single next action in [`STATE.md`](STATE.md).

**Ceiling.** Closed on 36 real exports that are public because their owners were
building something else. Not a random sample of bank exports; no claim of
representativeness. The Actual port is this experiment's own work, and a reader
who judges it unfaithful voids G2. Two accounts are excluded from precision
scoring because their descriptors carry a personal legal name — recorded as a
cost, not hidden.

## F186 — the piecewise-constant repair is a real improvement over the CV ceiling but recovers only 2 of 14 misses and does not reach the gates (2026-10-09)

`observed` 2026-10-09, session 2026-10-09-003, E073.
Population: E072's frozen corpus — 36 real bank exports, 34,231 transactions,
33-family watchlist. Instrument: E065's `detect.py` with one change — the
0.15 amount-CV ceiling replaced by a piecewise-constant price model (at most 2
constant amount segments, i.e. at most one price change).

**The claim this closes.** F185 diagnosed 14 of E072's 20 misses as an
amount-consistency gate defect and named the repair: a piecewise-constant
price model. E073 ran that repair with two predeclared gates — G1 recall ≥
0.50, G2 F1 margin over the incumbent ≥ +0.05. **Both fail.** Recall 0.455,
F1 margin +0.048.

**What the repair does achieve.** Against the frozen E065 baseline, the pwc arm
is strictly better on every count:

| metric | e065_raw | e073_pwc_raw | change |
|---|---|---|---|
| precision | 0.100 | 0.126 | +0.026 |
| recall | 0.394 | 0.455 | +0.061 |
| F1 | 0.160 | 0.197 | +0.037 |
| TP | 13 | 15 | +2 |
| FP | 117 | 104 | −13 |
| FN | 20 | 18 | −2 |

The 17 added groups are real price-change subscriptions — 13 unambiguously
recurring, 3 with a real recurring component mixed with a one-time charge, 1
not recurring (P1b hand-read, precision ≥ 0.80). This is not a CV-ceiling
relaxation: a loosened CV would add groups with no recurring pattern, and the
pwc model rejects groups with 3+ amount segments.

**Why it is not enough.** The pwc model recovers **2 of the 14 CV-gate
misses** — the one-price-step Spotify subscriptions (a35, a36) and Comcast.
The other 12 have amount shapes a one-step model cannot capture: drift
(State Farm, Progressive), oscillation (AT&T, T-Mobile), or multiple changes
(Amazon Prime FR with 13 segments, ChatGPT with 5). The diagnosis was
directionally right — the amount gate was the binding constraint for a
measurable set of real subscriptions — but the repair is narrower than the
diagnosis predicted.

**A real cost of the stricter gate.** The pwc model drops 27 groups E065
accepted, including **2 watchlist hits**: Brightwheel (3 segments) and TELEKOM
(9 segments). These are real subscriptions whose amounts have more than 2
segments. The pwc model correctly rejects them as non-piecewise-constant, but
they are real recurring expenses the model cannot see.

**The model's structural weakness.** It cannot distinguish a price step from
a one-time purchase plus a subscription at a different amount. Three added
groups (Apple $138 + $5.36/month, Fedloanservicing $13,500 + $750/month,
Twitch $114 + $5.71/month) have a one-time charge followed by a recurring
charge. The pwc model sees 2 segments and accepts them, exactly as it would a
price change. The recurring component is real, but the group is impure.

**What survives.** Not the detector. The finding that a one-step price model
is the right *shape* of repair for a measurable subset of real subscriptions —
and that the remaining misses need a richer model (drift, seasonality, multiple
changes) or are not recurring at all (payroll, mortgage escrow with varying
amounts). No predeclared gate in this experiment tests those.

**Ceiling.** Closed on the same 36 exports as E072, with the same corpus and
watchlist, frozen. G0 fidelity passes (the baseline reproduces E072's row
exactly after a mixed-side filter defect was repaired). The detector line
remains closed (F185, D090); this finding does not reopen it.