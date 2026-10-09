<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Kill Gate Design Checklist

**Purpose:** Ensure a predeclared kill gate can actually fail, not always pass on vacuous cases.

**Source:** Lessons from E069 (F101, D088) and E070 — a kill gate whose passing region contains only vacuous cases cannot fail; the tool that computes it will still report a pass.

**When to use:** Before running any experiment with a predeclared kill gate. Complete this checklist before writing the first line of the protocol.

---

## 1. Enumerate the gate's passing value — BEFORE the run

**Question:** What specific values or conditions must the gate's metric take for the gate to report PASS?

- [ ] The passing region is explicitly named and its possible values are listed.
- [ ] Every possible value the metric can take is accounted for — not just the "normal" case.
- [ ] The vacuous/default case (e.g., 0, empty, None) is explicitly identified as either (a) a valid pass condition, or (b) a condition that should trigger FAIL.
- [ ] If the gate can only ever pass on the vacuous/default case, the protocol is redesigned — a gate that cannot fail is not a valid kill gate.

**Why:** E069/F101 demonstrated that a gate whose passing region contains only vacuous cases (e.g., "3 clean installs out of 3" where the only 3 installable specs named nothing) will always pass, even when the underlying mechanism is meaningless. K1 moved from KILL to "mechanism holds" when one empty file sufficed.

**Action if failing:** Redesign the gate to enumerate its passing region explicitly before the run begins.

---

## 2. Verify analyze.py reads pre-existing bytes — not run-generated files

**Question:** Does the analysis tool (`analyze.py`) read bytes that exist before the experiment run starts, or bytes that the run itself writes at the end?

- [ ] `analyze.py` reads from input directories/files that are present before `python3 run.py` is invoked.
- [ ] `analyze.py` does NOT read from `output/`, `results.json`, or any file that the run script writes during or after processing.
- [ ] If `analyze.py` reads a file generated at the end of the run, the gate cannot fail on pre-run data — redesign so the verdict is derived from durable, pre-existing bytes.

**Why:** E069's own analysis tool could not have produced its verdict because it read a file written only at the end of the run. Per D088: "analyze.py must read bytes that exist before the run ends, not a file the run writes at the end (which is how E069's own analysis tool could not have produced its verdict)."

**Action if failing:** Move the reference data to a location that exists before the run, or restructure the protocol so the verdict is computed from pre-existing input.

---

## 3. Test the gate with a "worst case" input — before the run

**Question:** Run the kill gate protocol against a input scenario where the gate SHOULD fail, and verify that it does fail.

- [ ] Construct a minimal test input that would reasonably cause the gate to fail (e.g., many credible reports, wrong data source, reports from generated-not-pre-existing data).
- [ ] Run the protocol against this test input before running it against the real data.
- [ ] If the gate passes on the "worst case" input, redesign — the gate is vulnerable to the vacuous-passing-region anti-pattern.

**Why:** A kill gate that passes on data it should fail on is worse than useless — it gives false confidence and wastes experimentation effort. E069/F101 fired the kill gate five ways over, each time confirming the gate could not fail on its own data.

**Action if failing:** Redesign the gate's threshold or passing condition, or add a pre-run verification step.

---

## 4. Document the gate's reachable set — and verify it is non-vacuous

**Question:** What is the complete set of inputs on which the gate can report PASS? Is the set larger than just the vacuous/default case?

- [ ] The reachable set of the gate is explicitly documented (e.g., "passes when credible reports < 10 from pre-existing data").
- [ ] The reachable set includes at least one non-vacuous case — i.e., there is a meaningful input on which the gate would FAIL if the condition were not met.
- [ ] If the reachable set is only the vacuous default case, the gate is not a valid kill gate — it measures nothing.

**Why:** Per F101/D088: "a kill gate whose only reachable successes are empty files measures nothing." A gate that can only pass on empty/vacuous cases does not constrain the experiment and should not be used as a kill gate.

**Action if failing:** Redesign the gate to have a non-vacuous reachable set, or reconsider whether a kill gate is needed for this experiment.

---

## 5. Cross-check with prior experiment results

**Question:** Has a similar kill gate design been tried before? What was the outcome?

- [ ] Search the repository's experiment history (FAILURES.md, HYPOTHESES.md) for prior art on this gate design.
- [ ] If a similar gate design was used in a closed experiment, review why it failed or was abandoned.
- [ ] Prior art check: 10 of 18 previously killed candidates died of something else — a falsified mechanism, a claim no observation could establish, or one promoted then parked (F044). Ensure the gate design does not replicate a known failure mode.

**Why:** The mission's prior-art check (RESEARCH/PRIOR-ART-ORIGIN.md, F026, F027) found that the dominant kill reason across 18 candidates was prior art (0.556 plurality), but 7 died of other causes. Ensure the kill gate design does not replicate a known anti-pattern.

**Action if failing:** Redesign the gate or choose a different kill condition.

---

## Summary

A valid kill gate must satisfy all five checks above. If any check fails, the protocol must be redesigned before the run begins. The cost of this redesign is small (per E069: "both are small changes to how a protocol is written") compared to the cost of running an experiment with a gate that cannot fail.

**E069/F101 verdict:** Kill gate design matters. A gate whose passing region contains only vacuous cases cannot fail — redesign before running.

**E070 demonstration:** Protocol A (vacuous) always passes; Protocol B (explicit) can fail. The checklist above ensures new protocols follow the Protocol B pattern.