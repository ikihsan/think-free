# Session 2026-10-04-056-re-adjudicate-e012-s-19-prior-art-kills

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T22:18:13+00:00
- **Duration:** 8555.9s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Re-adjudicate E012's 19 prior-art kills on three corpora with positive controls, to test whether F029's largest cause of death is sound

## Summary

E016 (T-0062) closed with both declared arms met: 6 of 6 positive controls recovered, and 3 of the 12 adjudicable prior-art kills have no prior art on GitHub, three registries and the open web, exactly at the declared threshold, with one attribution row deciding it and both numbers recorded. A thirteenth kill was never adjudicable because its clause and E012's reason asked different questions. The transferable result is corpus carriage: the open web carried 4 served verdicts two code corpora returned nothing for. Recorded as F035, F036 and D050; the protocol now states the four conditions a prior-art verdict needs. Also renumbered onto the moving base twice (F034/015 and T-0061 were taken by the other VM), merged both VMs' records by hand, and repaired the F025 allocation assertion that re-derived a two-day finding against a growing history.

## Next

Take the invention item's first mechanism question: item 7 (annotate once, then choose metric/log/trace per code path at runtime), with its own kill gate declared before any prototype. Item 12 and 16 wait behind it. The owner decision on the selection axis is now informed by F034 and F035 and can be taken at any time.

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
| tasks/T-0062-re-adjudicate-e012-s-19-prior-art-kills-on-three.md | 0c8dd689a289 | 3420 |
| ROADMAP.md | 9e3cb4a251b0 | 20202 |
| tests/test_allocation_measurement.py | 1afdac710b56 | 9224 |

## Commands

15 captured, 2 non-zero exit.

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
| 31 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 329638 |
| 32 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 337284 |
| 33 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'tests.test_allocation_measurement', '-v'] | 0 | 1009 |
| 36 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 325110 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 47 |
| declared artifacts now missing | 0 |
| integrity errors | 6 |
| redactions applied to command output | 0 |
|   undeclared | .gitignore |
|   undeclared | DECISIONS-SCREENING.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/016-prior-art-adjudication/README.md |
|   undeclared | EXPERIMENTS/016-prior-art-adjudication/adjudicate.py |
|   undeclared | EXPERIMENTS/016-prior-art-adjudication/phrasings.json |
|   undeclared | EXPERIMENTS/016-prior-art-adjudication/raw/attributions.jsonl |
|   undeclared | EXPERIMENTS/016-prior-art-adjudication/raw/brave/0_q0.log |
|   undeclared | EXPERIMENTS/016-prior-art-adjudication/raw/brave/0_q1.log |
|   undeclared | EXPERIMENTS/016-prior-art-adjudication/raw/brave/12_q0.log |
|   error | declared artifact no longer exists: EXPERIMENTS/015-prior-art-adjudication/README.md |
|   error | declared artifact no longer exists: EXPERIMENTS/015-prior-art-adjudication/phrasings.json |
|   error | declared artifact no longer exists: EXPERIMENTS/015-prior-art-adjudication/raw/attributions.jsonl |
|   error | declared artifact no longer exists: EXPERIMENTS/015-prior-art-adjudication/raw/web_log.jsonl |
|   error | declared artifact no longer exists: EXPERIMENTS/015-prior-art-adjudication/results.json |
|   error | declared artifact no longer exists: EXPERIMENTS/015-prior-art-adjudication/web_bing.py |

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
| 26 | 00:06:23 | base_advance | rebase completed outside land: base moved 5ffe28ec8d15 -> 44fa38c1b100, 6 commit(s) arrived from the shared base |
| 27 | 00:08:26 | base_advance | sync land: base moved 33749cb3b389 -> 4bde980af369, 2 commit(s) arrived from the shared base |
| 28 | 00:08:41 | artifact | wrote tasks/T-0062-re-adjudicate-e012-s-19-prior-art-kills-on-three.md |
| 29 | 00:08:59 | task_rewrite | rewrote tasks/T-0062-re-adjudicate-e012-s-19-prior-art-kills-on-three.md (status: claimed) |
| 30 | 00:08:59 | task_rewrite | appended a claim record for T-0062 |
| 31 | 00:14:46 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 32 | 00:20:29 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 33 | 00:21:17 | command | $ env PYTHONPATH=tools:tests python3 -m unittest tests.test_allocation_measurement -v |
| 34 | 00:28:02 | task_rewrite | rewrote tasks/T-0062-re-adjudicate-e012-s-19-prior-art-kills-on-three.md (status: done) |
| 35 | 00:28:02 | task_rewrite | appended a complete record for T-0062 |
| 36 | 00:40:19 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 37 | 00:40:31 | artifact | wrote ROADMAP.md |
| 38 | 00:40:32 | artifact | wrote tests/test_allocation_measurement.py |
| 39 | 00:40:32 | milestone | T-0062 verified and completed; repaired the F025 allocation assertion, which re-derived a two-day finding against a growing history (F018's shape a fo |
| 40 | 00:40:48 | unlogged_change | changed but never declared as an artifact: .gitignore |
| 89 | 00:40:48 | integrity_error | declared artifact no longer exists: EXPERIMENTS/015-prior-art-adjudication/raw/attributions.jsonl |
| 90 | 00:40:48 | integrity_error | declared artifact no longer exists: EXPERIMENTS/015-prior-art-adjudication/raw/web_log.jsonl |
| 91 | 00:40:48 | integrity_error | declared artifact no longer exists: EXPERIMENTS/015-prior-art-adjudication/results.json |
| 92 | 00:40:48 | integrity_error | declared artifact no longer exists: EXPERIMENTS/015-prior-art-adjudication/web_bing.py |
| 93 | 00:40:49 | doc_update | updated DECISIONS-SCREENING.md |
| 94 | 00:40:49 | doc_update | updated DECISIONS.md |
| 95 | 00:40:49 | doc_update | updated FAILURES.md |
| 96 | 00:40:49 | doc_update | updated ROADMAP.md |
| 97 | 00:40:49 | doc_update | updated STATE.md |
| 98 | 00:40:49 | session_end | E016 (T-0062) closed with both declared arms met: 6 of 6 positive controls recovered, and 3 of the 12 adjudicable prior-art kills have no prior art on |

_48 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-056-re-adjudicate-e012-s-19-prior-art-kills/events.jsonl
```
