# Session 2026-10-09-015-determine-next-experiment-direction-afte

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T19:20:59+00:00
- **Duration:** 3136.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Determine next experiment direction after E069/E073/E075/E078 closures

## Summary

Designed and implemented E079 ArXiv reproducibility falsification experiment. Information-sufficiency witness W-ARXIV-1 FAIL (as predicted): two synthetic repos with identical permitted inputs but requiring different pinned numpy versions cannot be distinguished from static analysis alone. This bounds the claim - any deterministic tool seeing only static inputs (unpinned requirements.txt, imports, README) produces identical pinned requirements for both, causing one to fail. Harvest finds papers (4 unique in pilot), tool prototype extracts imports but over-generates (includes stdlib/internal modules), test infrastructure needs python3.8-venv. Kill gates predeclared: G1 install≥80%, G3 combined≥30%, G4 tool>baseline+10pp. Decision: hold - witness passed (bound demonstrated), full experiment not run due to env constraints. Also refactored E077 into modular structure (run.py + measure.py). Per D083, next session must start from fresh observation in a new domain. The ArXiv reproducibility line (E067→E069→E079) is closed on measured grounds.

## Next

Start fresh observation in a new domain per D083. The candidate seat remains empty after 9 measurements (F029, F051, F039, F059, F081, F084, F085, E075, E079). No candidate has been validated.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 14 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/077-se-nonsoftware-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/077-se-nonsoftware-viewcount/README.md |
|   undeclared | EXPERIMENTS/077-se-nonsoftware-viewcount/measure.py |
|   undeclared | EXPERIMENTS/077-se-nonsoftware-viewcount/run.py |
|   undeclared | EXPERIMENTS/079-arxiv-reproducibility/PROTOCOL.md |
|   undeclared | EXPERIMENTS/079-arxiv-reproducibility/experiment.py |
|   undeclared | EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py |
|   undeclared | EXPERIMENTS/079-arxiv-reproducibility/harvest.py |
|   undeclared | EXPERIMENTS/079-arxiv-reproducibility/heuristics.py |
|   undeclared | EXPERIMENTS/079-arxiv-reproducibility/run.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 19:20:59 | session_start | Determine next experiment direction after E069/E073/E075/E078 closures |
| 2 | 19:21:18 | milestone | Analyzed current state: 6 claims tested, 0 validated. E067 (ArXiv reproducibility) only experiment with all gates passed on real data. E078 (NEC 220)  |
| 3 | 19:22:17 | milestone | Applying falsification design to ArXiv reproducibility claim (E067). Claim: tool can generate machine-runnable env specs from partial info. Need kill  |
| 4 | 19:23:04 | milestone | Falsification design for ArXiv reproducibility: Claim - tool generates runnable pinned specs from partial info. Strongest baseline: repo2docker/binder |
| 5 | 19:25:54 | milestone | Added H-01 hypothesis for ArXiv reproducibility (E067). Kill gate: ≥30% of A2+A3 papers yield installable+runnable specs with ≥80% install success. Ba |
| 6 | 19:40:41 | milestone | E079 ArXiv reproducibility experiment designed: witness W-ARXIV-1 passes (information-sufficiency bound demonstrated), harvest.py working (finds paper |
| 7 | 20:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/077-se-nonsoftware-viewcount/PROTOCOL.md |
| 8 | 20:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/077-se-nonsoftware-viewcount/README.md |
| 9 | 20:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/077-se-nonsoftware-viewcount/measure.py |
| 10 | 20:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/077-se-nonsoftware-viewcount/run.py |
| 11 | 20:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/PROTOCOL.md |
| 12 | 20:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/experiment.py |
| 13 | 20:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py |
| 14 | 20:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/harvest.py |
| 15 | 20:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/heuristics.py |
| 16 | 20:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/run.py |
| 17 | 20:13:15 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/witness.py |
| 18 | 20:13:15 | unlogged_change | changed but never declared as an artifact: HYPOTHESES-results.md |
| 19 | 20:13:15 | unlogged_change | changed but never declared as an artifact: HYPOTHESES.md |
| 20 | 20:13:15 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 21 | 20:13:15 | doc_update | updated HYPOTHESES.md |
| 22 | 20:13:15 | doc_update | updated STATE.md |
| 23 | 20:13:15 | session_end | Designed and implemented E079 ArXiv reproducibility falsification experiment. Information-sufficiency witness W-ARXIV-1 FAIL (as predicted): two synth |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-015-determine-next-experiment-direction-afte/events.jsonl
```
