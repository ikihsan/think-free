# Initial experimental-discovery plan

Date: 2026-10-03. This is a plan for inquiry, not a selected product design.

## Constraints

Use the verified local environment. Keep initial reports independent. Do not import personal memory. No external writes, purchases, unsolicited contact, or deployment during initial discovery. Keep experiment inputs licensed or synthetic and mark the distinction. Tests must target claims and failure modes, not merely mirror implementation.

## Task 1 — Establish capability evidence

Files: `000-capabilities/results.json`, root mission and state records.

- [x] Verify the directory is empty and outside another Git repository.
- [x] Initialize an isolated repository and the mission record.
- [x] Check runtime execution and public networking, recording raw outputs.
- [x] Record actual resource and persistence limits.

## Task 2 — Independent exploration

Files: `RESEARCH/A.md` through `RESEARCH/F.md`.

- [ ] Obtain six sealed reports with materially different methods and primary-source checks.
- [ ] Require nearest prior art, reasons to abandon, and an executable test for serious candidates.
- [ ] Consolidate only after initial reports are complete; preserve disagreements.

## Task 3 — Competing experiments

Files: one self-contained directory per chosen experiment, with `README.md`, runnable implementation, tests where meaningful, and raw result files.

- [ ] Select at least two materially different claims to test; this is not product commitment.
- [ ] Write the design, controls, acceptance/rejection criteria, expected failure modes, and exact reproduction command before implementation.
- [ ] For nontrivial reusable mechanisms, write and run failing behavioral tests before implementation, then implement and rerun.
- [ ] Run actual experiments and record unexpected/negative outcomes.
- [ ] Independently reproduce or review results and challenge whether the baseline is fair.

## Task 4 — Checkpoint and next decision

- [ ] Update HYPOTHESES.md, RESEARCH.md, FAILURES.md, DECISIONS.md, and STATE.md from observed results.
- [ ] Inspect diffs and verify claims against artifacts; commit focused checkpoints.
- [ ] Choose the next highest-information experiment. Keep the mission active until independently verifiable impact exists or continuation is externally blocked.

Each experiment gets its own concrete design once evidence identifies a claim worth testing; inventing detailed implementation plans before discovery would prematurely anchor the project.
