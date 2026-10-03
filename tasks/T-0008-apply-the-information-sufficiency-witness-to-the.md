<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0008
status: claimed
created: 2026-10-03
claim-agent: opencode
claim-session: 2026-10-03-020-apply-the-information-sufficiency-witnes
claim-vm: instance-20260717-0947
verify: test -f EXPERIMENTS/003-information-sufficiency/results.json && test -f EXPERIMENTS/003-information-sufficiency/README.md
-->

# T-0008 — Apply the information-sufficiency witness to the three held candidates

## Goal

Apply the information-sufficiency witness to the three held candidates and record which survive

## Why this matters

STATE.md next actions 1 and 4 and ROADMAP stage B make this the highest-priority step before any implementation: it is cheap, needs no code beyond a tiny witness each, and has already killed two proposals in this repository. A candidate that fails the witness must be narrowed or killed, not implemented.

## Preconditions

RESEARCH/A.md and RESEARCH/C.md candidate sections are sealed and readable; HYPOTHESES.md carries a witness description for each of the three held candidates.

## Steps

1. For each held candidate (decision-directed sidewalk survey; knitting repair planner; adaptive ventilation measurement), construct two underlying realities that give the proposed system identical permitted inputs but require different outputs. 2. Encode each as a small stdlib-Python witness that prints the identical inputs and the divergent required decisions, with a machine-readable result. 3. State for each whether the witness succeeds (ambiguity real, candidate must narrow/abstain/add an observation) or fails (witness cannot be built; candidate's inputs are sufficient for the decision). 4. Record raw output in results.json and a README with the claim, inputs, oracle, and limits. 5. Update HYPOTHESES.md with each result and FAILURES.md for any candidate the witness kills.

## Acceptance criteria

- [ ] results.json holds one witness per held candidate with observed output and exit status. - [ ] README.md states claim, inputs, oracle, and limits for each. - [ ] Each candidate is labelled survive / narrow / killed with the reason. - [ ] HYPOTHESES.md and (where a candidate dies) FAILURES.md updated. - [ ] Full test suite and doc lint exit 0.

## Verification

```bash
test -f EXPERIMENTS/003-information-sufficiency/results.json && test -f EXPERIMENTS/003-information-sufficiency/README.md
```

## Rollback

Delete EXPERIMENTS/003-information-sufficiency/ and revert the HYPOTHESES.md/FAILURES.md edits; no tooling depends on it.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
