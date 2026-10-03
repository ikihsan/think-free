<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-03
-->

# 003-information-sufficiency

Applies the information-sufficiency witness (the cheap pre-implementation gate in
`docs/process/hypothesis-lifecycle.md` and the `falsification-design` skill) to
the three candidates held in `HYPOTHESES.md`, before any of them is implemented.

The test: construct **two underlying realities that give the proposed system
identical permitted inputs but require different outputs**. If such a pair exists
and no permitted observation separates it, the design is wrong regardless of
implementation quality; the response is to narrow the claim, request one more
observation, or permit abstention.

For a passive system, identical inputs that need different outputs are fatal. For
an active system — one allowed to choose the next observation — the pair is only
fatal if **no permitted action** separates the two realities. The witness
therefore tries to find a silent pair and reports whether it failed.

All inputs are **synthetic**. A synthetic witness can falsify an unbounded claim;
it cannot measure how often the ambiguity occurs in real data. That limit is
stated in `results.json` and below.

## Reproduce

```bash
python3 EXPERIMENTS/003-information-sufficiency/witness.py
```

Expected: `results.json` is rewritten; each verdict is printed. Standard library
only.

## W1 — decision-directed sidewalk survey

**Claim under test.** Given masked crossing attributes and a set of
origin/destination pairs, expecting one crossing to be surveyed, the policy
chooses the crossing whose result changes the recommended repair package.

**Inputs (synthetic).** Two crossings `c1`, `c2`, both initially `unknown`; two
destinations D1 (weight 10, via `c1`) and D2 (weight 6, via `c2`); budget 1
repair; the OD pairs are a permitted input (per `RESEARCH/A.md` step 2).

**Oracle.** The exact best repair package under full information, versus the
package chosen from the masked input after one inspection.

**Construction.** Reality A has `c1` safe, `c2` unsafe; Reality B is the reverse.
Both present the *same* permitted input (both crossings `unknown`). Their optimal
repairs differ (`{c1}` vs `{c2}`), and inspecting `c1` — a permitted action —
exposes the difference.

**Result.** `observed`. `silent_pair_found: false`. The witness could **not**
construct a pair with identical permitted inputs and a different required output
that no askable observation separates. **Verdict: survives**, under the explicit
scope condition that the OD pairs are among the inputs. If the OD pairs were
dropped from the input set, the candidate would be information-insufficient; the
specification does not drop them.

**Limit.** One synthetic two-crossing network. It shows the mechanism is not
*structurally* information-insufficient; it says nothing about the 25 %
regret advantage, which the A1 masking experiment (`EXPERIMENTS/002-a1-masking`)
measures separately, nor about whether graph-connectivity error (a risk noted in
`RESEARCH/A.md`) dominates. Connectivity is not in this witness's vocabulary.

## W2 — knitting repair planner

**Claim under test.** Given the intended chart, the actual local error, the live
stitches, and the facing side, produce a bounded, checkable intervention plan.

**Inputs (synthetic).** A four-loop patch with chart symbols and connectivity, a
declared error, the live stitches, and the public-facing side. Physical
**mount** (whether a loop is twisted) is deliberately absent from the input, to
test whether the stated input set is sufficient.

**Oracle.** The exact valid repair for each underlying stitch state.

**Construction.** Reality A: the dropped loops are mounted normally → repair by
re-forming in place. Reality B: the same loops are mounted twisted → repair by
re-forming **and** untwisting. The permitted chart-level inputs are identical;
the valid repairs differ.

**Result.** `observed`. The two realities share identical permitted inputs yet
require different repairs, and no input in the stated set can represent the
difference. **Verdict: information-insufficient as specified — narrow the input
or permit refusal.** This does **not** kill the mechanism: a knitter can see a
twist, so orientation *can* be added to the input (or the planner can refuse
ambiguous states). It bounds the input set, exactly as the candidate's own
kill-gate text anticipates ("refuse unsupported shaping/ambiguous states rather
than accepting them silently").

**Limit.** A four-loop synthetic patch with one error class. It shows the
specification is silent about orientation; it does not measure how often real
errors are ambiguous, nor whether physical manipulation defeats the plan.

## W3 — adaptive ventilation measurement

**Claim under test.** Given commodity CO2 sensor CSV, choosing the next ordinary
observation separates competing exchange-rate explanations better than a fixed
passive trace.

**Inputs (synthetic).** A two-room mass-balance model with outdoor exchange
`lam1`, inter-room coupling `k`, a second-room exchange `lam2`, occupancy
source, and a sensor bias. Permitted actions (no tracer gas, no deliberate
release): `passive` (one sensor), `co-locate` (add a room-2 sensor),
`close-internal-door` (`k → 0`), and `unoccupied-decay` (source off, normal
occupancy beforehand).

**Oracle.** Whether any permitted action produces a reading difference between
the two realities larger than 2 % of the signal peak (the assumed sensor-noise
scale).

**Construction.** Search the parameter grid for a pair with `lam1 + k` held
equal — so total loss matches — whose passive single-sensor traces coincide
within 2 %. The found pair: P = `lam1 0.05, k 0.01`; Q = `lam1 0.06, k 0.00`.
Their passive traces differ by 1.96 % of peak, below the noise scale.

**Result.** `observed`. The passive traces are indistinguishable within the noise
scale, **but** `co-locate` (14.8 %) and `close-internal-door` (14.6 %) exceed it,
so a permitted ordinary observation separates the realities. `unoccupied-decay`
(1.88 %) does not, because holding total loss equal makes the decay similar.
**Verdict: survives** — next-observation selection carries decision-relevant
information the passive trace lacks.

**Limit.** A deterministic two-room model, not measured rooms. It establishes
mathematical possibility only; `RESEARCH/C.md` requires independent room
measurements before any practical claim. The 2 % noise scale is an assumption,
not a measurement.

## Cross-cutting limits

- All three inputs are synthetic. No prevalence is measured.
- A survivor here has passed one cheap gate; it has not been shown useful,
  differentiated, or novel, and no candidate has a user.
- One error class per candidate. A different construction could still find a
  silent pair; these results are `observed` for the witness, `inferred` for the
  broader claim.
