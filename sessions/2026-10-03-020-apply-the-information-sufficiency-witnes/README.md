# Session 2026-10-03-020-apply-the-information-sufficiency-witnes

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-03T16:57:50+00:00
- **Duration:** 1105.5s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Apply the information-sufficiency witness to the three held candidates and record which survive

## Summary

Applied the information-sufficiency witness to the three held candidates: W1 sidewalk survey and W3 ventilation survive (a permitted observation separates realities with identical inputs); W2 knitting repair planner is information-insufficient as specified (orientation absent; F007). Also repaired push credentialing on this VM (durable JWT generator; App ID recovered) and recorded D018/D019. task verify T-0008 exit 0; 168 tests green; doc lint OK.

## Next

Repair the knitting candidate's input set (add orientation or require refusal), then run its Stage-A local-planner vs. exhaustive-search comparison

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| HYPOTHESES.md | 1d39c6131011 | 11561 |
| FAILURES.md | 6cc45066dff7 | 13068 |
| EXPERIMENTS/003-information-sufficiency/README.md | 0a591fa892a6 | 6917 |
| EXPERIMENTS/003-information-sufficiency/results.json | c2c00041ec91 | 8327 |
| EXPERIMENTS/003-information-sufficiency/witness.py | 879b5200ebd7 | 2592 |
| EXPERIMENTS/003-information-sufficiency/witness_vent.py | 6fa6c4b41882 | 6975 |
| EXPERIMENTS/003-information-sufficiency/witnesses.py | de209bb5ad21 | 7428 |
| DECISIONS.md | bc124895e526 | 15808 |
| ROADMAP.md | 3f88e4f570be | 4563 |
| STATE.md | 09f3a82eb877 | 9121 |

## Commands

10 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/003-information-sufficiency/witness.py'] | 1 | 607 |
| 4 | ['python3', 'EXPERIMENTS/003-information-sufficiency/witness.py'] | 0 | 110 |
| 5 | ['python3', 'EXPERIMENTS/003-information-sufficiency/witness.py'] | 0 | 210 |
| 6 | ['tools/origin', 'doc', 'lint'] | 2 | 821 |
| 7 | ['tools/origin', 'doc', 'index'] | 0 | 608 |
| 8 | ['python3', 'EXPERIMENTS/003-information-sufficiency/witness.py'] | 0 | 194 |
| 9 | ['python3', 'EXPERIMENTS/003-information-sufficiency/witness.py'] | 0 | 127 |
| 18 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 85278 |
| 19 | ['tools/origin', 'doc', 'lint'] | 0 | 825 |
| 22 | ['tools/origin', 'doc', 'lint'] | 0 | 817 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | tasks/T-0008-apply-the-information-sufficiency-witness-to-the.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:57:50 | session_start | Apply the information-sufficiency witness to the three held candidates and record which survive |
| 2 | 16:58:22 | milestone | Push credential repaired (App ID 5173845, durable JWT generator); T-0008 created and pushed |
| 3 | 17:03:50 | command | $ python3 EXPERIMENTS/003-information-sufficiency/witness.py |
| 4 | 17:04:08 | command | $ python3 EXPERIMENTS/003-information-sufficiency/witness.py |
| 5 | 17:06:19 | command | $ python3 EXPERIMENTS/003-information-sufficiency/witness.py |
| 6 | 17:07:27 | command | $ tools/origin doc lint |
| 7 | 17:07:33 | command | $ tools/origin doc index |
| 8 | 17:09:19 | command | $ python3 EXPERIMENTS/003-information-sufficiency/witness.py |
| 9 | 17:10:29 | command | $ python3 EXPERIMENTS/003-information-sufficiency/witness.py |
| 10 | 17:11:31 | experiment_result | Information-sufficiency witnesses applied to the three held candidates: W1 sidewalk survey survives (askable inspection separates), W2 knitting repair |
| 11 | 17:11:42 | artifact | wrote HYPOTHESES.md |
| 12 | 17:11:42 | artifact | wrote FAILURES.md |
| 13 | 17:11:42 | artifact | wrote EXPERIMENTS/003-information-sufficiency/README.md |
| 14 | 17:11:42 | artifact | wrote EXPERIMENTS/003-information-sufficiency/results.json |
| 15 | 17:11:42 | artifact | wrote EXPERIMENTS/003-information-sufficiency/witness.py |
| 16 | 17:11:42 | artifact | wrote EXPERIMENTS/003-information-sufficiency/witness_vent.py |
| 17 | 17:11:42 | artifact | wrote EXPERIMENTS/003-information-sufficiency/witnesses.py |
| 18 | 17:13:12 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 19 | 17:13:20 | command | $ tools/origin doc lint |
| 20 | 17:15:34 | decision | App JWT generator and App ID live under ~/.config/github-app/, not ephemeral /tmp |
| 21 | 17:15:34 | decision | Run the information-sufficiency witness for every held candidate before implementing any of them |
| 22 | 17:15:41 | command | $ tools/origin doc lint |
| 23 | 17:15:45 | artifact | wrote DECISIONS.md |
| 24 | 17:15:46 | artifact | wrote ROADMAP.md |
| 25 | 17:15:46 | artifact | wrote STATE.md |
| 26 | 17:16:15 | unlogged_change | changed but never declared as an artifact: tasks/T-0008-apply-the-information-sufficiency-witness-to-the.md |
| 27 | 17:16:15 | doc_update | updated DECISIONS.md |
| 28 | 17:16:15 | doc_update | updated FAILURES.md |
| 29 | 17:16:15 | doc_update | updated HYPOTHESES.md |
| 30 | 17:16:15 | doc_update | updated ROADMAP.md |
| 31 | 17:16:15 | doc_update | updated STATE.md |
| 32 | 17:16:15 | session_end | Applied the information-sufficiency witness to the three held candidates: W1 sidewalk survey and W3 ventilation survive (a permitted observation separ |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-020-apply-the-information-sufficiency-witnes/events.jsonl
```
