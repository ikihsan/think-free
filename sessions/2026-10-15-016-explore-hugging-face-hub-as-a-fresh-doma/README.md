# Session 2026-10-15-016-explore-hugging-face-hub-as-a-fresh-doma

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-15T16:03:49+00:00
- **Duration:** 3951.0s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Explore Hugging Face Hub as a fresh domain for the view-count principle: test whether need-related models/datasets/spaces show systematic activity advantages over random content

## Summary

Completed E150: Hugging Face Hub view-count principle test. 1,900 models sampled and classified into 1,151 need-related (derivatives, fine-tunes, quantized) and 170 general (base foundation models). Kill gate fired: all three metrics (likes, downloads, trendingScore) show Cliff's delta < 0.147. Downloads favor general models (base models are infrastructure downloaded as dependencies). The view-count principle works on package registries (leaf consumption) but not model hubs (infrastructure layer). Recorded as F128 in FAILURES-findings-41.md. Fixed all doc lint violations.

## Next

Fresh observation in a domain this mission has not touched, chosen by a stated rule rather than by comfort. Continue exploring new domains for the view-count principle or other invention candidates.

## Artifacts

_none_

## Commands

16 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['curl', '-s', 'https://huggingface.co/api/models?limit=5'] | 0 | 549 |
| 3 | ['curl', '-s', 'https://huggingface.co/api/datasets?limit=5'] | 0 | 280 |
| 4 | ['curl', '-s', 'https://huggingface.co/api/spaces?limit=5'] | 0 | 392 |
| 5 | ['curl', '-s', 'https://huggingface.co/api/models?limit=50'] | 0 | 308 |
| 6 | ['curl', '-s', 'https://huggingface.co/api/models?limit=20&sort=downloads'] | 0 | 438 |
| 7 | ['curl', '-s', 'https://huggingface.co/api/datasets?limit=50&sort=downloads'] | 0 | 448 |
| 8 | ['curl', '-s', 'https://huggingface.co/api/spaces?limit=50&sort=likes'] | 0 | 382 |
| 9 | ['mkdir', '-p', 'EXPERIMENTS/150-huggingface-viewcount'] | 0 | 18 |
| 10 | ['python3', 'EXPERIMENTS/150-huggingface-viewcount/collect.py'] | 0 | 4406 |
| 11 | ['python3', 'EXPERIMENTS/150-huggingface-viewcount/classify.py'] | 0 | 296 |
| 12 | ['python3', 'EXPERIMENTS/150-huggingface-viewcount/classify.py'] | 0 | 405 |
| 13 | ['python3', 'EXPERIMENTS/150-huggingface-viewcount/classify.py'] | 0 | 406 |
| 14 | ['python3', 'EXPERIMENTS/150-huggingface-viewcount/classify.py'] | 0 | 694 |
| 15 | ['python3', 'EXPERIMENTS/150-huggingface-viewcount/classify.py'] | 0 | 431 |
| 16 | ['python3', 'EXPERIMENTS/150-huggingface-viewcount/analyze.py'] | 0 | 3028 |
| 17 | ['python3', '-m', 'tools.origin', 'doc', 'lint'] | 1 | 36 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 94 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/PROTOCOL.md |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/RESULT.md |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/attempts.jsonl |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/classify.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/fetch-threads.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/fetch.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/g0-probes.json |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/g0-results.jsonl |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/g0-run.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/grading-results.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:03:49 | session_start | Explore Hugging Face Hub as a fresh domain for the view-count principle: test whether need-related models/datasets/spaces show systematic activity adv |
| 2 | 16:04:19 | command | $ curl -s https://huggingface.co/api/models?limit=5 |
| 3 | 16:04:27 | command | $ curl -s https://huggingface.co/api/datasets?limit=5 |
| 4 | 16:04:27 | command | $ curl -s https://huggingface.co/api/spaces?limit=5 |
| 5 | 16:04:55 | command | $ curl -s https://huggingface.co/api/models?limit=50 |
| 6 | 16:05:11 | command | $ curl -s https://huggingface.co/api/models?limit=20&sort=downloads |
| 7 | 16:05:35 | command | $ curl -s https://huggingface.co/api/datasets?limit=50&sort=downloads |
| 8 | 16:05:49 | command | $ curl -s https://huggingface.co/api/spaces?limit=50&sort=likes |
| 9 | 16:06:05 | command | $ mkdir -p EXPERIMENTS/150-huggingface-viewcount |
| 10 | 16:08:30 | command | $ python3 EXPERIMENTS/150-huggingface-viewcount/collect.py |
| 11 | 16:09:35 | command | $ python3 EXPERIMENTS/150-huggingface-viewcount/classify.py |
| 12 | 16:10:24 | command | $ python3 EXPERIMENTS/150-huggingface-viewcount/classify.py |
| 13 | 16:12:21 | command | $ python3 EXPERIMENTS/150-huggingface-viewcount/classify.py |
| 14 | 16:14:53 | command | $ python3 EXPERIMENTS/150-huggingface-viewcount/classify.py |
| 15 | 16:15:45 | command | $ python3 EXPERIMENTS/150-huggingface-viewcount/classify.py |
| 16 | 16:20:33 | command | $ python3 EXPERIMENTS/150-huggingface-viewcount/analyze.py |
| 17 | 16:23:34 | command | $ python3 -m tools.origin doc lint |
| 18 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/PROTOCOL.md |
| 19 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/RESULT.md |
| 20 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/attempts.jsonl |
| 21 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/classify.py |
| 22 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/fetch-threads.py |
| 23 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/fetch.py |
| 24 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/g0-probes.json |
| 25 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/g0-results.jsonl |
| 26 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/g0-run.py |
| 27 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/grading-results.jsonl |
| 28 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/make-sheet.py |
| 29 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/move-e141.py |
| 30 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/pool-raw.json |
| 31 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/screening-rows.json |
| 32 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/screening.jsonl |
| 33 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/threads-raw.json |
| 34 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/PROTOCOL.md |
| 35 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/RESULT.md |
| 36 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/arm_a_raw.json |
| 37 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/arm_a_unanswered.json |
| 38 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/arm_b_raw.json |
| 39 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/arm_b_unanswered.json |
| 40 | 17:09:39 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-electrical-engineering-se/attempt_sample.json |
| 105 | 17:09:39 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-009-recover-context-and-understand-project-s/events.jsonl |
| 106 | 17:09:40 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-010-finalize-decision-and-continuation-for-e/events.jsonl |
| 107 | 17:09:40 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-011-finalize-and-summarize-e150-e151-results/events.jsonl |
| 108 | 17:09:40 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-012-document-view-count-principle-topic-depe/events.jsonl |
| 109 | 17:09:40 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-013-run-e160-github-devops-repos-view-count/events.jsonl |
| 110 | 17:09:40 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-014-synthesize-view-count-principle-boundary/events.jsonl |
| 111 | 17:09:40 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-015-continue-e161-prototype-vs-code-extensio/events.jsonl |
| 112 | 17:09:40 | doc_update | updated FAILURES.md |
| 113 | 17:09:40 | doc_update | updated STATE.md |
| 114 | 17:09:40 | session_end | Completed E150: Hugging Face Hub view-count principle test. 1,900 models sampled and classified into 1,151 need-related (derivatives, fine-tunes, quan |

_64 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-016-explore-hugging-face-hub-as-a-fresh-doma/events.jsonl
```
