# Session 2026-10-04-056-re-adjudicate-e012-s-19-prior-art-kills

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T22:18:13+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Re-adjudicate E012's 19 prior-art kills on three corpora with positive controls, to test whether F029's largest cause of death is sound

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/015-prior-art-adjudication/README.md | c30ef4326cd3 | 6713 |
| EXPERIMENTS/015-prior-art-adjudication/phrasings.json | 5c62c51b8f7a | 8835 |
| EXPERIMENTS/015-prior-art-adjudication/web_bing.py | 04f196093f4a | 3034 |
| EXPERIMENTS/015-prior-art-adjudication/results.json | 60e3bec3916e | 11685 |
| EXPERIMENTS/015-prior-art-adjudication/raw/attributions.jsonl | 042f715f7c50 | 21785 |
| EXPERIMENTS/015-prior-art-adjudication/raw/web_log.jsonl | 44710ee13a3c | 23954 |
| FAILURES-findings-12.md | 0f2b8070ed75 | 8501 |
| FAILURES-findings-13.md | 70b749d617d4 | 9440 |

## Commands

11 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['python3', 'EXPERIMENTS/015-prior-art-adjudication/adjudicate.py'] | 0 | 276840 |
| 5 | ['python3', 'EXPERIMENTS/015-prior-art-adjudication/web_probe.py', 'first'] | 0 | 77871 |
| 8 | ['python3', 'EXPERIMENTS/015-prior-art-adjudication/web_bing.py'] | 0 | 164794 |
| 11 | ['python3', 'EXPERIMENTS/015-prior-art-adjudication/stats.py'] | 0 | 193 |
| 12 | ['python3', 'EXPERIMENTS/015-prior-art-adjudication/stats.py'] | 0 | 193 |
| 13 | ['python3', 'EXPERIMENTS/015-prior-art-adjudication/stats.py'] | 0 | 125 |
| 14 | ['python3', 'EXPERIMENTS/015-prior-art-adjudication/stats.py'] | 0 | 118 |
| 15 | ['python3', 'EXPERIMENTS/015-prior-art-adjudication/stats.py'] | 0 | 178 |
| 21 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 327413 |
| 22 | ['python3', 'EXPERIMENTS/016-prior-art-adjudication/stats.py'] | 0 | 97 |
| 23 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 334419 |

## Integrity

| check | result |
|---|---|
| session_end event | MISSING - session may be unfinished |
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 22:18:13 | session_start | Re-adjudicate E012's 19 prior-art kills on three corpora with positive controls, to test whether F029's largest cause of death is sound |
| 2 | 22:19:33 | artifact | wrote EXPERIMENTS/015-prior-art-adjudication/README.md |
| 3 | 22:19:34 | artifact | wrote EXPERIMENTS/015-prior-art-adjudication/phrasings.json |
| 4 | 22:25:32 | command | $ python3 EXPERIMENTS/015-prior-art-adjudication/adjudicate.py |
| 5 | 22:28:46 | command | $ python3 EXPERIMENTS/015-prior-art-adjudication/web_probe.py first |
| 6 | 22:32:40 | milestone | resuming on this VM: DDG endpoint returned 202 (refused) on all 19 first-pass queries; probing alternate open-web instruments |
| 7 | 22:32:40 | decision | duckduckgo-html/202 is a refused instrument, recorded as refused; bing organic results parse cleanly (n=10), so the declared open-web corpus will be r |
| 8 | 22:36:01 | command | $ python3 EXPERIMENTS/015-prior-art-adjudication/web_bing.py |
| 9 | 22:36:20 | artifact | wrote EXPERIMENTS/015-prior-art-adjudication/web_bing.py |
| 10 | 23:16:30 | milestone | resumed after context reset: bing capture is HTTP 200 but returns results unrelated to the query (YouTube Music for a Linux distro query), so the thir |
| 11 | 23:24:58 | command | $ python3 EXPERIMENTS/015-prior-art-adjudication/stats.py |
| 12 | 23:25:30 | command | $ python3 EXPERIMENTS/015-prior-art-adjudication/stats.py |
| 13 | 23:26:07 | command | $ python3 EXPERIMENTS/015-prior-art-adjudication/stats.py |
| 14 | 23:26:32 | command | $ python3 EXPERIMENTS/015-prior-art-adjudication/stats.py |
| 15 | 23:33:16 | command | $ python3 EXPERIMENTS/015-prior-art-adjudication/stats.py |
| 16 | 23:38:29 | milestone | E015 complete: arm 1 6/6 controls, arm 2 3 of 12 no prior art found (threshold 3, one row decides it); open web carried 4 verdicts two code corpora mi |
| 17 | 23:38:29 | artifact | wrote EXPERIMENTS/015-prior-art-adjudication/results.json |
| 18 | 23:38:30 | artifact | wrote EXPERIMENTS/015-prior-art-adjudication/raw/attributions.jsonl |
| 19 | 23:38:31 | artifact | wrote EXPERIMENTS/015-prior-art-adjudication/raw/web_log.jsonl |
| 20 | 23:38:32 | artifact | wrote FAILURES-findings-12.md |
| 21 | 23:46:10 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 22 | 23:49:38 | command | $ python3 EXPERIMENTS/016-prior-art-adjudication/stats.py |
| 23 | 00:05:44 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 24 | 00:06:15 | artifact | wrote FAILURES-findings-13.md |
| 25 | 00:06:15 | milestone | merged onto the new base by hand: kept both VMs' findings parts (12 and 13), both experiments rows, both STATE-next-actions items 0/0b/0c/0d, and repa |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-056-re-adjudicate-e012-s-19-prior-art-kills/events.jsonl
```
