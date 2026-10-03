# Experimental decision protocol

## Before implementation

1. State a falsifiable claim and its scope in one sentence. "Useful" and "novel" are not test assertions.
2. Name the strongest existing alternative. If it cannot be executed here, label the comparison unperformed. Never treat a deliberately weak baseline as the state of the art.
3. Specify inputs, expected output/oracle, negative controls, thresholds, and resource limits before observing results. Separate mechanism correctness, performance, human usefulness, and novelty: one cannot validate the others.
4. State what result would cause abandonment, narrowing, or another experiment. An initial arbitrary threshold is a provisional engineering screen, not an empirical adoption requirement.
5. For reusable code, write behavioral tests that can fail on a meaningful defect; observe the failure before implementing. A small analytical impossibility proof may be more informative than a large implementation.

## During execution

- Save commands, seeds, versions, raw output, exit codes, and the source revision or content hashes. Record failures instead of silently replacing them with successful runs.
- Label synthetic data clearly; do not turn planted defects into claims about naturally occurring prevalence.
- Keep dependencies and data small initially. Use timeouts and bounded allocations. Escalate scale only when it tests a decision-relevant uncertainty.
- Do not silently tune thresholds on evaluation data. Keep adversarial or holdout cases outside the implementation's development loop where practical.
- If timing is meaningful, repeat measurements and describe what is and is not included. One local timing is not a comparative benchmark.

## After execution

- Have a separate reviewer inspect the oracle, baseline fairness, inputs, and whether results actually support the stated claim.
- Report both positive and negative cases. A mechanism can pass its tests while the product hypothesis fails.
- Update the hypothesis record and next action. Prefer a decisive small rejection over preserving a candidate to justify sunk effort.
- Before product commitment, require evidence beyond agent-authored synthetic cases: public real cases, independent reproduction, or actual users. Human usefulness and sustainable adoption remain untested until observed.

## Role independence audit

Agents have isolated initial contexts and disjoint report files, but share similar learned priors and this mission framing. Agreement among them is therefore weak evidence. Search outside the concepts they agree on, and give strongest prior art a chance to invalidate the synthesis.
