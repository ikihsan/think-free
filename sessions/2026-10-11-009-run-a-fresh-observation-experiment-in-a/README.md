# Session 2026-10-11-009-run-a-fresh-observation-experiment-in-a

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T08:15:56+00:00
- **Duration:** 1972.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run a fresh observation experiment in a new untested domain to map view-count principle boundaries

## Summary

Completed fresh observation experiment E101 on Stack Overflow (software Q&A on Stack Exchange). All four gates pass: G1 (1,530 NEED questions), G2 (56.7% NEED concentration), G3 (18.6% unserved, CI95 [16.7%, 20.6%]), G4 (100% view_count coverage). The view-count principle generalizes to Stack Overflow. Unserved fraction (18.6%) is consistent with embedded Discourse (15.3%, E082) but higher than non-software Discourse (11.7%, E077), suggesting software Q&A has more unserved needs than general Q&A.

## Next

Analyze whether the 18.6% unserved fraction on Stack Overflow represents a viable candidate population for a tool, or if it's served by existing mechanisms (Stack Overflow answers, documentation, LLMs). Consider testing the view-count principle on another software-owning venue (e.g., GitHub Discussions if view counts available, or a different package registry like crates.io) to further map platform invariance.

## Artifacts

_none_

## Commands

56 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['curl', '-s', '-I', 'https://www.cnczone.com/'] | 0 | 791 |
| 3 | ['curl', '-s', 'https://www.cnczone.com/forums/'] | 0 | 87 |
| 4 | ['curl', '-s', 'https://www.cnczone.com/forums/'] | 0 | 160 |
| 5 | ['curl', '-s', 'https://www.cnczone.com/forums/'] | 0 | 106 |
| 6 | ['curl', '-sL', 'https://www.cnczone.com/forums/'] | 0 | 257 |
| 7 | ['curl', '-sL', 'https://www.practicalmachinist.com/'] | 0 | 589 |
| 8 | ['curl', '-sL', 'https://forum.arduino.cc/'] | 0 | 1123 |
| 9 | ['curl', '-sL', 'https://forums.raspberrypi.com/'] | 0 | 508 |
| 10 | ['curl', '-sL', 'https://www.plctalk.net/'] | 0 | 234 |
| 11 | ['curl', '-sH', 'Accept: application/vnd.github.v3+json', 'https://api.github.com/repos/microsoft/vscode/discussions/categories'] | 0 | 397 |
| 12 | ['curl', '-sH', 'Accept: application/vnd.github.v3+json', 'https://api.github.com/repos/github/docs/discussions/categories'] | 0 | 341 |
| 13 | ['curl', '-sH', 'Accept: application/vnd.github.v3+json', 'https://api.github.com/repos/tensorflow/tensorflow/discussions/categories'] | 0 | 328 |
| 14 | ['curl', '-sH', 'Accept: application/vnd.github.v3+json', 'https://api.github.com/repos/vercel/next.js/discussions/categories'] | 0 | 390 |
| 15 | ['curl', '-sH', 'Accept: application/vnd.github.v3+json', 'https://api.github.com/repos/kubernetes/kubernetes/discussions/categories'] | 0 | 334 |
| 16 | ['curl', '-sL', 'https://www.quora.com/topic/Programming'] | 0 | 445 |
| 17 | ['curl', '-sL', 'https://repost.aws/'] | 0 | 464 |
| 18 | ['curl', '-sL', 'https://learn.microsoft.com/en-us/answers/'] | 0 | 371 |
| 19 | ['curl', '-sL', 'https://learn.microsoft.com/en-us/answers/questions'] | 0 | 1177 |
| 20 | ['curl', '-sL', 'https://learn.microsoft.com/en-us/answers/questions'] | 0 | 455 |
| 21 | ['curl', '-sL', 'https://learn.microsoft.com/en-us/answers/questions'] | 0 | 396 |
| 22 | ['curl', '-sL', 'https://learn.microsoft.com/en-us/answers/questions'] | 0 | 539 |
| 23 | ['curl', '-sH', 'Accept: application/vnd.github.v3+json', 'https://api.github.com/repos/orgs/github/discussions'] | 0 | 386 |
| 24 | ['curl', '-s', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', '{"query": "{ repository(owner: \\"github\\", name: \\"feedback\\") { discu | 0 | 252 |
| 25 | ['curl', '-s', 'https://pub.dev/api/packages?page=1'] | 0 | 1010 |
| 26 | ['curl', '-sL', 'https://learn.microsoft.com/en-us/answers/questions'] | 0 | 501 |
| 27 | ['curl', '-sL', 'https://learn.microsoft.com/en-us/answers/questions'] | 0 | 415 |
| 28 | ['curl', '-sL', 'https://learn.microsoft.com/en-us/answers/questions'] | 0 | 477 |
| 29 | ['curl', '-sL', 'https://learn.microsoft.com/static/assets/0.4.03568.8292-0a6c2196/scripts/en-us/index-critical-qna.js'] | 0 | 180 |
| 31 | ['curl', '-sL', 'https://learn.microsoft.com/static/assets/0.4.03568.8292-0a6c2196/scripts/en-us/index-critical-qna.js'] | 0 | 429 |
| 33 | ['curl', '-sL', 'https://learn.microsoft.com/api/search?search=azure&facet=contentType&qna=true'] | 0 | 382 |
| 34 | ['curl', '-sL', 'https://learn.microsoft.com/api/search?search=azure&locale=en-us&qna=true'] | 0 | 1535 |
| 35 | ['curl', '-sL', 'https://learn.microsoft.com/api/search?search=error&locale=en-us&qna=true&contentType=Question'] | 0 | 1414 |
| 36 | ['curl', '-s', 'https://api.stackexchange.com/2.3/questions?order=desc&sort=views&tagged=python&site=stackoverflow&pagesize=5&filter=!nOedRLbBQ'] | 0 | 620 |
| 37 | ['curl', '-s', 'https://api.stackexchange.com/2.3/questions?order=desc&sort=views&tagged=python&site=stackoverflow&pagesize=5'] | 0 | 388 |
| 38 | ['curl', '-s', 'https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&tagged=python&site=stackoverflow&pagesize=5'] | 0 | 388 |
| 39 | ['curl', '-s', 'https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&tagged=python&site=stackoverflow&pagesize=5&answers=0'] | 0 | 414 |
| 40 | ['curl', '-s', 'https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&tagged=python&site=stackoverflow&pagesize=100'] | 0 | 656 |
| 41 | ['curl', '-s', 'https://api.stackexchange.com/2.3/questions?order=desc&sort=creation&tagged=python&site=stackoverflow&pagesize=100'] | 0 | 424 |
| 42 | ['curl', '-s', 'https://api.stackexchange.com/2.3/questions/unanswered?order=desc&sort=views&tagged=python&site=stackoverflow&pagesize=10'] | 0 | 338 |
| 43 | ['curl', '-s', 'https://api.stackexchange.com/2.3/questions/unanswered?order=desc&sort=votes&tagged=python&site=stackoverflow&pagesize=10'] | 0 | 407 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 40 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 2 |
|   undeclared | EXPERIMENTS/083-aviation-maintenance-fault-codes/results.json |
|   undeclared | EXPERIMENTS/093-discrimination-test |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/PROTOCOL.md |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/RESULTS.md |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/collect_practitioner_rows.py |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/deduplicate.py |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/measure_population.py |
|   undeclared | EXPERIMENTS/098-home-assistant-fresh/run_discrimination_test.py |
|   undeclared | EXPERIMENTS/09X-hnews-viewcount/results.json |
|   undeclared | EXPERIMENTS/09X-hnews-viewcount/run.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:15:56 | session_start | Run a fresh observation experiment in a new untested domain to map view-count principle boundaries |
| 2 | 08:17:06 | command | $ curl -s -I https://www.cnczone.com/ |
| 3 | 08:17:12 | command | $ curl -s https://www.cnczone.com/forums/ |
| 4 | 08:17:18 | command | $ curl -s https://www.cnczone.com/forums/ |
| 5 | 08:17:25 | command | $ curl -s https://www.cnczone.com/forums/ |
| 6 | 08:17:30 | command | $ curl -sL https://www.cnczone.com/forums/ |
| 7 | 08:17:42 | command | $ curl -sL https://www.practicalmachinist.com/ |
| 8 | 08:17:53 | command | $ curl -sL https://forum.arduino.cc/ |
| 9 | 08:18:02 | command | $ curl -sL https://forums.raspberrypi.com/ |
| 10 | 08:18:09 | command | $ curl -sL https://www.plctalk.net/ |
| 11 | 08:18:57 | command | $ curl -sH Accept: application/vnd.github.v3+json https://api.github.com/repos/microsoft/vscode/discussions/categories |
| 12 | 08:19:03 | command | $ curl -sH Accept: application/vnd.github.v3+json https://api.github.com/repos/github/docs/discussions/categories |
| 13 | 08:19:08 | command | $ curl -sH Accept: application/vnd.github.v3+json https://api.github.com/repos/tensorflow/tensorflow/discussions/categories |
| 14 | 08:19:40 | command | $ curl -sH Accept: application/vnd.github.v3+json https://api.github.com/repos/vercel/next.js/discussions/categories |
| 15 | 08:19:53 | command | $ curl -sH Accept: application/vnd.github.v3+json https://api.github.com/repos/kubernetes/kubernetes/discussions/categories |
| 16 | 08:20:02 | command | $ curl -sL https://www.quora.com/topic/Programming |
| 17 | 08:20:15 | command | $ curl -sL https://repost.aws/ |
| 18 | 08:20:31 | command | $ curl -sL https://learn.microsoft.com/en-us/answers/ |
| 19 | 08:20:42 | command | $ curl -sL https://learn.microsoft.com/en-us/answers/questions |
| 20 | 08:20:49 | command | $ curl -sL https://learn.microsoft.com/en-us/answers/questions |
| 21 | 08:20:57 | command | $ curl -sL https://learn.microsoft.com/en-us/answers/questions |
| 22 | 08:21:04 | command | $ curl -sL https://learn.microsoft.com/en-us/answers/questions |
| 23 | 08:22:24 | command | $ curl -sH Accept: application/vnd.github.v3+json https://api.github.com/repos/orgs/github/discussions |
| 24 | 08:22:33 | command | $ curl -s -X POST -H Content-Type: application/json -d {"query": "{ repository(owner: \"github\", name: \"feedback\") { discussions(first: 5) |
| 25 | 08:24:34 | command | $ curl -s https://pub.dev/api/packages?page=1 |
| 26 | 08:26:56 | command | $ curl -sL https://learn.microsoft.com/en-us/answers/questions |
| 27 | 08:27:03 | command | $ curl -sL https://learn.microsoft.com/en-us/answers/questions |
| 28 | 08:27:11 | command | $ curl -sL https://learn.microsoft.com/en-us/answers/questions |
| 29 | 08:27:21 | command | $ curl -sL https://learn.microsoft.com/static/assets/0.4.03568.8292-0a6c2196/scripts/en-us/index-critical-qna.js |
| 30 | 08:27:21 | redaction | redacted 1 secret pattern(s) from command output |
| 31 | 08:27:31 | command | $ curl -sL https://learn.microsoft.com/static/assets/0.4.03568.8292-0a6c2196/scripts/en-us/index-critical-qna.js |
| 32 | 08:27:31 | redaction | redacted 1 secret pattern(s) from command output |
| 33 | 08:27:43 | command | $ curl -sL https://learn.microsoft.com/api/search?search=azure&facet=contentType&qna=true |
| 34 | 08:27:53 | command | $ curl -sL https://learn.microsoft.com/api/search?search=azure&locale=en-us&qna=true |
| 35 | 08:28:01 | command | $ curl -sL https://learn.microsoft.com/api/search?search=error&locale=en-us&qna=true&contentType=Question |
| 36 | 08:28:56 | command | $ curl -s https://api.stackexchange.com/2.3/questions?order=desc&sort=views&tagged=python&site=stackoverflow&pagesize=5&filter=!nOedRLbBQ |
| 37 | 08:29:07 | command | $ curl -s https://api.stackexchange.com/2.3/questions?order=desc&sort=views&tagged=python&site=stackoverflow&pagesize=5 |
| 38 | 08:29:19 | command | $ curl -s https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&tagged=python&site=stackoverflow&pagesize=5 |
| 39 | 08:29:36 | command | $ curl -s https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&tagged=python&site=stackoverflow&pagesize=5&answers=0 |
| 40 | 08:29:50 | command | $ curl -s https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&tagged=python&site=stackoverflow&pagesize=100 |
| 91 | 08:48:49 | unlogged_change | changed but never declared as an artifact: raw/discrimination_test_results.json |
| 92 | 08:48:49 | unlogged_change | changed but never declared as an artifact: raw/population_measurement_results.json |
| 93 | 08:48:49 | unlogged_change | changed but never declared as an artifact: raw/practitioner_rows.jsonl |
| 94 | 08:48:49 | unlogged_change | changed but never declared as an artifact: raw/practitioner_rows_dedup.jsonl |
| 95 | 08:48:49 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-005-run-pyfix-prototype-and-view-count-hacke/events.jsonl |
| 96 | 08:48:49 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-006-fresh-observation-in-a-new-domain-per-d0/events.jsonl |
| 97 | 08:48:49 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-007-design-and-run-a-fresh-observation-exper/events.jsonl |
| 98 | 08:48:49 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-008-build-and-evaluate-discrimination-test-p/events.jsonl |
| 99 | 08:48:49 | unlogged_change | changed but never declared as an artifact: viewcount_crates.py |
| 100 | 08:48:49 | session_end | Completed fresh observation experiment E101 on Stack Overflow (software Q&A on Stack Exchange). All four gates pass: G1 (1,530 NEED questions), G2 (56 |

_50 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-009-run-a-fresh-observation-experiment-in-a/events.jsonl
```
