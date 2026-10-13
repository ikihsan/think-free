# Session 2026-10-13-005-e125-measure-whether-preflight-can-be-po

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-13
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-13T02:06:36+00:00
- **Duration:** 1983.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E125: measure whether preflight can be pointed at third-party evaluation harnesses, and whether the silent-scoring defect it catches occurs outside this repository

## Summary

E125 predeclared and ran: can a third party point preflight at their own harness? 22 repos inspected (G1 pass), 5 M4-qualified pairs (G1 FAIL vs declared 10), zero-adapter path works on all 5 (G2 pass), 0 SILENT_NO_MATCH (G3 not observed). Coverage: 0.2450 of 857 sampled data files stdlib-readable; 21/857 carry output-shaped fields. Control 2: C1 false-positive rate 1.00 on a working positional join. F124: field-name rule admitted 3 non-pairs; provenance term needed. Verdict: not_evaluated; preflight stays internal.

## Next

E125 RESULT section 7: read one harness's output writer end to end (evalscope) to settle whether a run-output directory has the shape preflight needs; separately, the mission-level choice of the next fresh observation.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/125-third-party-harness-preflight/PROTOCOL.md | ad6982e7700b | 8437 |
| EXPERIMENTS/125-third-party-harness-preflight/pool.py | 73ded4d9af65 | 5247 |
| EXPERIMENTS/125-third-party-harness-preflight/screen_readme.py | 8a4fb7a27cbe | 4919 |
| EXPERIMENTS/125-third-party-harness-preflight/pool.json | 934d309a551a | 45621 |
| EXPERIMENTS/125-third-party-harness-preflight/inspect.json | 62e5117668f0 | 12716 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/1517005260__graph-rag-agent.md | 8e6e11d56996 | 43618 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/AgentSafeLabs__safelabs-eval.md | 50b151467f95 | 23426 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/Ayanami0730__arag.md | 4588c90749ca | 13758 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/CodeSoul-co__Hypha.md | 0352bb0c8190 | 38856 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/IBM__AssetOpsBench.md | 178087092c0d | 38422 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/NVIDIA__SkillEvaluator.md | 57372744c5fa | 9963 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/Noietch__EVA-CLIENT.md | 7440ff1dc4e4 | 11006 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/OpenBMB__UltraEval-Audio.md | 25d8974b8dac | 24987 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/ZJU-REAL__ClawGUI.md | 3f0aaefce322 | 13817 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/agentscope-ai__OpenJudge.md | cb5f0d358c4d | 22573 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/aielte-research__HackSynth.md | 6ba8ac624b9d | 2509 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/awslabs__agent-evaluation.md | 79fdda07b0f3 | 2103 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/calmrocks__ai-engineer-notebooks.md | b2b3b344a534 | 19713 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/claw-eval__claw-eval.md | 25e20c74d435 | 8668 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/deer-flow__llm-space.md | 8b22efc794b1 | 8032 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/harbor-framework__harbor.md | 7b5e24d0974e | 2990 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/lmgame-org__GamingAgent.md | b5231ac6e61f | 9000 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/microsoft__AIOpsLab.md | 02a7d09401d4 | 22640 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/modelscope__evalscope.md | b7aac89ea3c9 | 28830 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/mozilla-ai__any-agent.md | 20efde950551 | 6175 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/openai__evals.md | f0b50bd53e2f | 6463 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/plurai-ai__intellagent.md | 952af0eb0588 | 7850 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/raga-ai-hub__RagaAI-Catalyst.md | 4530edece36d | 15360 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/responsibleai__ASSERT.md | 24efd0b2e818 | 19953 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/reworkd__bananalyzer.md | c7f5574143b8 | 7662 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/sunblaze-ucb__cybergym.md | 066c3fc3c19e | 8882 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/suyoumo__ClawProBench.md | d5129e67c12a | 14379 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/tensortrade-org__tensortrade.md | 36448a231945 | 8274 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/trpc-group__trpc-agent-go.md | 9fdf5f1f155e | 29946 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/verifywise-ai__verifywise.md | 8bec98a7d101 | 17863 |
| EXPERIMENTS/125-third-party-harness-preflight/AMENDMENT-1.md | 42fa2df9a4f5 | 3622 |
| EXPERIMENTS/125-third-party-harness-preflight/probe.py | 8671ef12976a | 12139 |
| EXPERIMENTS/125-third-party-harness-preflight/fetch.py | 12678c6f0349 | 3544 |
| EXPERIMENTS/125-third-party-harness-preflight/coverage.py | deb47d23a3f6 | 4899 |
| EXPERIMENTS/125-third-party-harness-preflight/pairs.json | 7b7807d66d98 | 33813 |
| EXPERIMENTS/125-third-party-harness-preflight/coverage.json | 845c712db218 | 12899 |
| EXPERIMENTS/125-third-party-harness-preflight/trees.json | c75c4bda8055 | 3965 |
| EXPERIMENTS/125-third-party-harness-preflight/fieldnames.json | afba87a13791 | 1696 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/1517005260__graph-rag-agent.tsv | 0a1d234353eb | 16754 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/AgentSafeLabs__safelabs-eval.tsv | b2a62b87f0c2 | 4522 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/Ayanami0730__arag.tsv | 97a6a03e8724 | 889 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/CodeSoul-co__Hypha.tsv | 319f94da049f | 97525 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/IBM__AssetOpsBench.tsv | 44d6e5a22bff | 12136 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/NVIDIA__SkillEvaluator.tsv | 6753a7c19b90 | 18504 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/Noietch__EVA-CLIENT.tsv | 47ebe94058e1 | 118415 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/OpenBMB__UltraEval-Audio.tsv | 105c96f69808 | 113018 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/ZJU-REAL__ClawGUI.tsv | 4afaf03405db | 46096 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/agentscope-ai__OpenJudge.tsv | ffced5015b41 | 33649 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/calmrocks__ai-engineer-notebooks.tsv | fca93ba3830a | 2162 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/claw-eval__claw-eval.tsv | 76bb05c2698e | 63639 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/microsoft__AIOpsLab.tsv | 6645c08b20df | 30443 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/modelscope__evalscope.tsv | a05170b94fc2 | 142805 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/openai__evals.tsv | f01bb6a31867 | 97605 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/plurai-ai__intellagent.tsv | 9dd72c086f36 | 6208 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/raga-ai-hub__RagaAI-Catalyst.tsv | 1b687c4eb890 | 11905 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/responsibleai__ASSERT.tsv | fdc17dac13b3 | 43663 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/suyoumo__ClawProBench.tsv | f1168af9e63d | 382673 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/tensortrade-org__tensortrade.tsv | 1690838fa9d6 | 22070 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/trpc-group__trpc-agent-go.tsv | 50a6e6afc37b | 203373 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/verifywise-ai__verifywise.tsv | fa2e5b01834c | 418967 |
| EXPERIMENTS/125-third-party-harness-preflight/RESULT.md | 97e26cc348d4 | 7323 |
| EXPERIMENTS/125-third-party-harness-preflight/README.md | d0939083514d | 3125 |
| EXPERIMENTS/125-third-party-harness-preflight/results.json | 05b306654498 | 4580 |
| EXPERIMENTS/125-third-party-harness-preflight/pair_sampled.py | 43f8bb2c8fcd | 4489 |
| EXPERIMENTS/125-third-party-harness-preflight/sample.json | f39627974995 | 177665 |
| EXPERIMENTS/125-third-party-harness-preflight/gate.py | 2d99ec81a55c | 9669 |
| EXPERIMENTS/125-third-party-harness-preflight/controls.py | 75d96c9685ad | 5936 |
| EXPERIMENTS/125-third-party-harness-preflight/controls.json | d2b6b4983417 | 1266 |
| EXPERIMENTS/125-third-party-harness-preflight/pairs-sampled.json | 03d16ec2bc5b | 16957 |
| EXPERIMENTS/125-third-party-harness-preflight/AMENDMENT-1.md | 42fa2df9a4f5 | 3622 |
| EXPERIMENTS/125-third-party-harness-preflight/PROTOCOL.md | ad6982e7700b | 8437 |
| EXPERIMENTS/125-third-party-harness-preflight/README.md | d0939083514d | 3125 |
| EXPERIMENTS/125-third-party-harness-preflight/RESULT.md | 97e26cc348d4 | 7323 |
| EXPERIMENTS/125-third-party-harness-preflight/controls.json | d2b6b4983417 | 1266 |
| EXPERIMENTS/125-third-party-harness-preflight/controls.py | 75d96c9685ad | 5936 |
| EXPERIMENTS/125-third-party-harness-preflight/coverage.json | 845c712db218 | 12899 |
| EXPERIMENTS/125-third-party-harness-preflight/coverage.py | 71df160f6770 | 5769 |
| EXPERIMENTS/125-third-party-harness-preflight/fetch.py | 12678c6f0349 | 3544 |
| EXPERIMENTS/125-third-party-harness-preflight/fieldnames.json | afba87a13791 | 1696 |
| EXPERIMENTS/125-third-party-harness-preflight/gate.py | 2d99ec81a55c | 9669 |
| EXPERIMENTS/125-third-party-harness-preflight/inspect.json | 62e5117668f0 | 12716 |
| EXPERIMENTS/125-third-party-harness-preflight/pair_sampled.py | 43f8bb2c8fcd | 4489 |
| EXPERIMENTS/125-third-party-harness-preflight/pairs-sampled.json | 03d16ec2bc5b | 16957 |
| EXPERIMENTS/125-third-party-harness-preflight/pairs.json | 7b7807d66d98 | 33813 |
| EXPERIMENTS/125-third-party-harness-preflight/pool.json | 934d309a551a | 45621 |
| EXPERIMENTS/125-third-party-harness-preflight/pool.py | 73ded4d9af65 | 5247 |
| EXPERIMENTS/125-third-party-harness-preflight/probe.py | 8671ef12976a | 12139 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/1517005260__graph-rag-agent.md | 8e6e11d56996 | 43618 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/AgentSafeLabs__safelabs-eval.md | 50b151467f95 | 23426 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/Ayanami0730__arag.md | 4588c90749ca | 13758 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/CodeSoul-co__Hypha.md | 0352bb0c8190 | 38856 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/IBM__AssetOpsBench.md | 178087092c0d | 38422 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/NVIDIA__SkillEvaluator.md | 57372744c5fa | 9963 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/Noietch__EVA-CLIENT.md | 7440ff1dc4e4 | 11006 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/OpenBMB__UltraEval-Audio.md | 25d8974b8dac | 24987 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/ZJU-REAL__ClawGUI.md | 3f0aaefce322 | 13817 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/agentscope-ai__OpenJudge.md | cb5f0d358c4d | 22573 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/aielte-research__HackSynth.md | 6ba8ac624b9d | 2509 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/awslabs__agent-evaluation.md | 79fdda07b0f3 | 2103 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/calmrocks__ai-engineer-notebooks.md | b2b3b344a534 | 19713 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/claw-eval__claw-eval.md | 25e20c74d435 | 8668 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/deer-flow__llm-space.md | 8b22efc794b1 | 8032 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/harbor-framework__harbor.md | 7b5e24d0974e | 2990 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/lmgame-org__GamingAgent.md | b5231ac6e61f | 9000 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/microsoft__AIOpsLab.md | 02a7d09401d4 | 22640 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/modelscope__evalscope.md | b7aac89ea3c9 | 28830 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/mozilla-ai__any-agent.md | 20efde950551 | 6175 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/openai__evals.md | f0b50bd53e2f | 6463 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/plurai-ai__intellagent.md | 952af0eb0588 | 7850 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/raga-ai-hub__RagaAI-Catalyst.md | 4530edece36d | 15360 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/responsibleai__ASSERT.md | 24efd0b2e818 | 19953 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/reworkd__bananalyzer.md | c7f5574143b8 | 7662 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/sunblaze-ucb__cybergym.md | 066c3fc3c19e | 8882 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/suyoumo__ClawProBench.md | d5129e67c12a | 14379 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/tensortrade-org__tensortrade.md | 36448a231945 | 8274 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/trpc-group__trpc-agent-go.md | 9fdf5f1f155e | 29946 |
| EXPERIMENTS/125-third-party-harness-preflight/readmes/verifywise-ai__verifywise.md | 8bec98a7d101 | 17863 |
| EXPERIMENTS/125-third-party-harness-preflight/results.json | 05b306654498 | 4580 |
| EXPERIMENTS/125-third-party-harness-preflight/sample.json | f39627974995 | 177665 |
| EXPERIMENTS/125-third-party-harness-preflight/screen_readme.py | 8a4fb7a27cbe | 4919 |
| EXPERIMENTS/125-third-party-harness-preflight/search-raw/search-responses.json | 69bcef7b8a1b | 761126 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/1517005260__graph-rag-agent.tsv | 0a1d234353eb | 16754 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/AgentSafeLabs__safelabs-eval.tsv | b2a62b87f0c2 | 4522 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/Ayanami0730__arag.tsv | 97a6a03e8724 | 889 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/CodeSoul-co__Hypha.tsv | 319f94da049f | 97525 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/IBM__AssetOpsBench.tsv | 44d6e5a22bff | 12136 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/NVIDIA__SkillEvaluator.tsv | 6753a7c19b90 | 18504 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/Noietch__EVA-CLIENT.tsv | 47ebe94058e1 | 118415 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/OpenBMB__UltraEval-Audio.tsv | 105c96f69808 | 113018 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/ZJU-REAL__ClawGUI.tsv | 4afaf03405db | 46096 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/agentscope-ai__OpenJudge.tsv | ffced5015b41 | 33649 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/calmrocks__ai-engineer-notebooks.tsv | fca93ba3830a | 2162 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/claw-eval__claw-eval.tsv | 76bb05c2698e | 63639 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/microsoft__AIOpsLab.tsv | 6645c08b20df | 30443 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/modelscope__evalscope.tsv | a05170b94fc2 | 142805 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/openai__evals.tsv | f01bb6a31867 | 97605 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/plurai-ai__intellagent.tsv | 9dd72c086f36 | 6208 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/raga-ai-hub__RagaAI-Catalyst.tsv | 1b687c4eb890 | 11905 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/responsibleai__ASSERT.tsv | fdc17dac13b3 | 43663 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/suyoumo__ClawProBench.tsv | f1168af9e63d | 382673 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/tensortrade-org__tensortrade.tsv | 1690838fa9d6 | 22070 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/trpc-group__trpc-agent-go.tsv | 50a6e6afc37b | 203373 |
| EXPERIMENTS/125-third-party-harness-preflight/trees/verifywise-ai__verifywise.tsv | fa2e5b01834c | 418967 |
| EXPERIMENTS/125-third-party-harness-preflight/trees.json | c75c4bda8055 | 3965 |

## Commands

21 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/pool.py'] | 0 | 20703 |
| 5 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/screen_readme.py'] | 0 | 23598 |
| 40 | ['git', 'add', 'EXPERIMENTS/125-third-party-harness-preflight'] | 0 | 182 |
| 41 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/fetch.py'] | 0 | 246720 |
| 42 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/fetch.py'] | 0 | 8790 |
| 43 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/probe.py'] | 1 | 976 |
| 44 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/probe.py'] | 0 | 14011 |
| 45 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/fetch.py'] | 0 | 3307 |
| 46 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/probe.py'] | 0 | 1913 |
| 47 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/coverage.py'] | 0 | 16183 |
| 78 | ['git', 'add', '-A', 'EXPERIMENTS/125-third-party-harness-preflight'] | 0 | 204 |
| 79 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/coverage.py'] | 0 | 13804 |
| 80 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/pair_sampled.py'] | 0 | 306 |
| 81 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/pair_sampled.py'] | 0 | 312 |
| 82 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/controls.py'] | 1 | 117 |
| 83 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/controls.py'] | 0 | 105 |
| 84 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/gate.py'] | 0 | 193 |
| 85 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/gate.py'] | 0 | 108 |
| 86 | ['python3', 'EXPERIMENTS/125-third-party-harness-preflight/gate.py'] | 0 | 105 |
| 171 | ['git', 'add', '-A', 'EXPERIMENTS/125-third-party-harness-preflight'] | 0 | 102 |
| 172 | ['./tools/origin', 'doc', 'lint'] | 2 | 133628 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | FAILURES-findings-40.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 02:06:36 | session_start | E125: measure whether preflight can be pointed at third-party evaluation harnesses, and whether the silent-scoring defect it catches occurs outside th |
| 2 | 02:08:41 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/PROTOCOL.md |
| 3 | 02:08:42 | milestone | E125 protocol committed before any third-party fetch |
| 4 | 02:09:39 | command | $ python3 EXPERIMENTS/125-third-party-harness-preflight/pool.py |
| 5 | 02:10:57 | command | $ python3 EXPERIMENTS/125-third-party-harness-preflight/screen_readme.py |
| 6 | 02:11:07 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/pool.py |
| 7 | 02:11:08 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/screen_readme.py |
| 8 | 02:11:09 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/pool.json |
| 9 | 02:11:10 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/inspect.json |
| 10 | 02:11:12 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/1517005260__graph-rag-agent.md |
| 11 | 02:11:13 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/AgentSafeLabs__safelabs-eval.md |
| 12 | 02:11:14 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/Ayanami0730__arag.md |
| 13 | 02:11:14 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/CodeSoul-co__Hypha.md |
| 14 | 02:11:15 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/IBM__AssetOpsBench.md |
| 15 | 02:11:16 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/NVIDIA__SkillEvaluator.md |
| 16 | 02:11:17 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/Noietch__EVA-CLIENT.md |
| 17 | 02:11:18 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/OpenBMB__UltraEval-Audio.md |
| 18 | 02:11:18 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/ZJU-REAL__ClawGUI.md |
| 19 | 02:11:19 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/agentscope-ai__OpenJudge.md |
| 20 | 02:11:20 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/aielte-research__HackSynth.md |
| 21 | 02:11:21 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/awslabs__agent-evaluation.md |
| 22 | 02:11:22 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/calmrocks__ai-engineer-notebooks.md |
| 23 | 02:11:23 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/claw-eval__claw-eval.md |
| 24 | 02:11:24 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/deer-flow__llm-space.md |
| 25 | 02:11:25 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/harbor-framework__harbor.md |
| 26 | 02:11:25 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/lmgame-org__GamingAgent.md |
| 27 | 02:11:26 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/microsoft__AIOpsLab.md |
| 28 | 02:11:27 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/modelscope__evalscope.md |
| 29 | 02:11:28 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/mozilla-ai__any-agent.md |
| 30 | 02:11:29 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/openai__evals.md |
| 31 | 02:11:30 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/plurai-ai__intellagent.md |
| 32 | 02:11:31 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/raga-ai-hub__RagaAI-Catalyst.md |
| 33 | 02:11:31 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/responsibleai__ASSERT.md |
| 34 | 02:11:32 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/reworkd__bananalyzer.md |
| 35 | 02:11:33 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/sunblaze-ucb__cybergym.md |
| 36 | 02:11:34 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/suyoumo__ClawProBench.md |
| 37 | 02:11:35 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/tensortrade-org__tensortrade.md |
| 38 | 02:11:36 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/trpc-group__trpc-agent-go.md |
| 39 | 02:11:38 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/readmes/verifywise-ai__verifywise.md |
| 40 | 02:11:39 | command | $ git add EXPERIMENTS/125-third-party-harness-preflight |
| 165 | 02:27:25 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/trees/responsibleai__ASSERT.tsv |
| 166 | 02:27:26 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/trees/suyoumo__ClawProBench.tsv |
| 167 | 02:27:26 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/trees/tensortrade-org__tensortrade.tsv |
| 168 | 02:27:27 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/trees/trpc-group__trpc-agent-go.tsv |
| 169 | 02:27:28 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/trees/verifywise-ai__verifywise.tsv |
| 170 | 02:27:29 | artifact | wrote EXPERIMENTS/125-third-party-harness-preflight/trees.json |
| 171 | 02:27:30 | command | $ git add -A EXPERIMENTS/125-third-party-harness-preflight |
| 172 | 02:32:29 | command | $ ./tools/origin doc lint |
| 173 | 02:39:39 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-40.md |
| 174 | 02:39:39 | session_end | E125 predeclared and ran: can a third party point preflight at their own harness? 22 repos inspected (G1 pass), 5 M4-qualified pairs (G1 FAIL vs decla |

_124 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-13-005-e125-measure-whether-preflight-can-be-po/events.jsonl
```
