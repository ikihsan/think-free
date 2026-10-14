# Session 2026-10-14-001-measure-the-form-invariance-of-shipped-l

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T00:18:17+00:00
- **Duration:** 5424.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e140-judge-form-invariance`

## Goal

Measure the form-invariance of shipped LLM-eval judges on correct-but-reworded output against a careful-normalizer baseline

## Summary

E140 measured the form-invariance of the shipped inspect_ai model_graded_fact judge against a deterministic value canonicalizer on E114's committed corpus. The judge is not falsified (0/24 false positives on correct-but-reworded answers, 6/7 on swapped values), E114's ground.py is quantitatively disproved as a gate (false-positive rate rises 0.3727 -> 0.4651 -> 0.6019 with rephrasing depth), and valueset.py passes every declared gate with 0 FP in 929 values while being blind to binding by construction and by measurement (0/6). F125 and D110 filed. Also recovered an interrupted line-cap split that had deleted D079-D083 and F051-F052.

## Next

Run valueset.py unchanged on a second genre whose answers are human-written and whose wrongness is found in the corpus rather than constructed (SQuAD v2.0 dev), with a coverage floor declared before the run.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/140-judge-form-invariance/PROTOCOL.md | b703361ec1e4 | 9796 |
| EXPERIMENTS/140-judge-form-invariance/judge_rubric.txt | 6733f1db73c1 | 2908 |
| EXPERIMENTS/140-judge-form-invariance/PROTOCOL.md | f15f43d51fb9 | 10739 |
| EXPERIMENTS/140-judge-form-invariance/AMENDMENT-1.md | 6224674dde65 | 3875 |
| EXPERIMENTS/140-judge-form-invariance/AMENDMENT-2.md | 7ce80d72b4eb | 6330 |
| EXPERIMENTS/140-judge-form-invariance/AMENDMENT-3.md | 60a2c5684fdb | 4722 |
| EXPERIMENTS/140-judge-form-invariance/AMENDMENT-4.md | cc751844ffd3 | 3229 |
| EXPERIMENTS/140-judge-form-invariance/AMENDMENT-5.md | 3464cc7c6ce5 | 3046 |
| EXPERIMENTS/140-judge-form-invariance/judge_rubric.txt | 6733f1db73c1 | 2908 |
| EXPERIMENTS/140-judge-form-invariance/p2.jsonl | f63d8a96530f | 4723 |
| EXPERIMENTS/140-judge-form-invariance/arms.jsonl | 92d5d496084f | 75508 |
| EXPERIMENTS/140-judge-form-invariance/gates.json | 0d8da1726fd7 | 26680 |
| EXPERIMENTS/140-judge-form-invariance/misattribution.json | 7346bb1f20a8 | 13112 |
| EXPERIMENTS/140-judge-form-invariance/score.py | 8cf4df68ea46 | 12037 |
| EXPERIMENTS/140-judge-form-invariance/valueset.py | 9a907991d41a | 5495 |
| EXPERIMENTS/140-judge-form-invariance/build_arms.py | 4d90c0dc0a0e | 10900 |
| EXPERIMENTS/140-judge-form-invariance/finalize_p2.py | 3e3ef8c0d680 | 4941 |
| EXPERIMENTS/140-judge-form-invariance/emit_judge_prompts.py | d02a71ec2422 | 5617 |
| EXPERIMENTS/140-judge-form-invariance/misattribution.py | 124396247c87 | 5445 |
| EXPERIMENTS/140-judge-form-invariance/RESULT.md | c43862951013 | 9327 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_00.md | 9a290fe2255d | 14291 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_01.md | a3379c84612e | 14160 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_02.md | 48c9904a34ea | 10611 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_03.md | 5bd10f2844df | 12747 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_04.md | 7491c36ebd6c | 15648 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_05.md | cd2c8efcda96 | 12345 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_06.md | 287040b19fff | 3408 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_00.txt | 45e5358d11e5 | 4953 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_01.txt | b2c975b87075 | 5708 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_02.txt | c0aedb3b4a18 | 3526 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_03.txt | c9d8b6bd6495 | 2678 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_04.txt | 5d50541eacdc | 4640 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_05.txt | b87ff21fcd84 | 3612 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_06.txt | 29afeb38730b | 1573 |
| EXPERIMENTS/140-judge-form-invariance/AMENDMENT-1.md | 6224674dde65 | 3875 |
| EXPERIMENTS/140-judge-form-invariance/AMENDMENT-2.md | 7ce80d72b4eb | 6330 |
| EXPERIMENTS/140-judge-form-invariance/AMENDMENT-3.md | 60a2c5684fdb | 4722 |
| EXPERIMENTS/140-judge-form-invariance/AMENDMENT-4.md | cc751844ffd3 | 3229 |
| EXPERIMENTS/140-judge-form-invariance/AMENDMENT-5.md | 3464cc7c6ce5 | 3046 |
| EXPERIMENTS/140-judge-form-invariance/PROTOCOL.md | f15f43d51fb9 | 10739 |
| EXPERIMENTS/140-judge-form-invariance/RESULT.md | c43862951013 | 9327 |
| EXPERIMENTS/140-judge-form-invariance/arms.jsonl | 92d5d496084f | 75508 |
| EXPERIMENTS/140-judge-form-invariance/build_arms.py | 4d90c0dc0a0e | 10900 |
| EXPERIMENTS/140-judge-form-invariance/emit_judge_prompts.py | d02a71ec2422 | 5617 |
| EXPERIMENTS/140-judge-form-invariance/finalize_p2.py | 3e3ef8c0d680 | 4941 |
| EXPERIMENTS/140-judge-form-invariance/gates.json | 0d8da1726fd7 | 26680 |
| EXPERIMENTS/140-judge-form-invariance/judge_batches.json | 0783f1911509 | 34435 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_00.txt | 45e5358d11e5 | 4953 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_01.txt | b2c975b87075 | 5708 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_02.txt | c0aedb3b4a18 | 3526 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_03.txt | c9d8b6bd6495 | 2678 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_04.txt | 5d50541eacdc | 4640 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_05.txt | b87ff21fcd84 | 3612 |
| EXPERIMENTS/140-judge-form-invariance/judge_output/batch_06.txt | 29afeb38730b | 1573 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_00.md | 9a290fe2255d | 14291 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_01.md | a3379c84612e | 14160 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_02.md | 48c9904a34ea | 10611 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_03.md | 5bd10f2844df | 12747 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_04.md | 7491c36ebd6c | 15648 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_05.md | cd2c8efcda96 | 12345 |
| EXPERIMENTS/140-judge-form-invariance/judge_prompts/batch_06.md | 287040b19fff | 3408 |
| EXPERIMENTS/140-judge-form-invariance/judge_rubric.txt | 6733f1db73c1 | 2908 |
| EXPERIMENTS/140-judge-form-invariance/misattribution.json | 7346bb1f20a8 | 13112 |
| EXPERIMENTS/140-judge-form-invariance/misattribution.py | 124396247c87 | 5445 |
| EXPERIMENTS/140-judge-form-invariance/p2.jsonl | f63d8a96530f | 4723 |
| EXPERIMENTS/140-judge-form-invariance/p2_job.json | d26d7e3e5689 | 5277 |
| EXPERIMENTS/140-judge-form-invariance/score.py | 8cf4df68ea46 | 12037 |
| EXPERIMENTS/140-judge-form-invariance/valueset.py | 9a907991d41a | 5495 |
| DECISIONS-SCREENING-21.md | b6045328c3b4 | 4327 |
| FAILURES-findings-41.md | 7eed5e94c575 | 5975 |
| DECISIONS.md | e9fb167fc876 | 25676 |
| FAILURES.md | a5d3bcb60ed1 | 81963 |
| vendor/MANIFEST.md | c63c6c9f1700 | 9464 |
| sessions/2026-10-13-042-explore-current-state-and-choose-next-in/README.md | fdc962b1ea62 | 9375 |
| sessions/2026-10-13-042-explore-current-state-and-choose-next-in/events.jsonl | 00ee44c30a5f | 49047 |

## Commands

18 captured, 6 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 6 | ['python3', 'build_arms.py'] | 1 | 930 |
| 7 | ['python3', 'build_arms.py'] | 0 | 505 |
| 8 | ['python3', 'build_arms.py'] | 0 | 496 |
| 9 | ['python3', 'build_arms.py'] | 0 | 682 |
| 10 | ['python3', 'build_arms.py'] | 0 | 1488 |
| 11 | ['python3', 'build_arms.py'] | 2 | 94 |
| 12 | ['python3', './build_arms.py'] | 0 | 624 |
| 13 | ['python3', './build_arms.py'] | 0 | 688 |
| 15 | ['python3', 'finalize_p2.py'] | 2 | 188 |
| 16 | ['python3', 'EXPERIMENTS/140-judge-form-invariance/finalize_p2.py'] | 0 | 397 |
| 17 | ['python3', 'EXPERIMENTS/140-judge-form-invariance/finalize_p2.py'] | 0 | 182 |
| 18 | ['python3', 'EXPERIMENTS/140-judge-form-invariance/emit_judge_prompts.py'] | 1 | 869 |
| 19 | ['python3', 'EXPERIMENTS/140-judge-form-invariance/emit_judge_prompts.py'] | 0 | 99 |
| 20 | ['python3', 'EXPERIMENTS/140-judge-form-invariance/score.py'] | 3 | 4037 |
| 21 | ['python3', 'EXPERIMENTS/140-judge-form-invariance/score.py'] | 3 | 3505 |
| 22 | ['python3', 'EXPERIMENTS/140-judge-form-invariance/score.py'] | 0 | 3415 |
| 23 | ['python3', 'EXPERIMENTS/140-judge-form-invariance/score.py'] | 0 | 4310 |
| 24 | ['python3', 'EXPERIMENTS/140-judge-form-invariance/misattribution.py'] | 0 | 902 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:18:17 | session_start | Measure the form-invariance of shipped LLM-eval judges on correct-but-reworded output against a careful-normalizer baseline |
| 2 | 00:40:01 | milestone | Context recovered: continuing E140 form-invariance of shipped judges; checking network + predeclaring protocol before any judge output is seen |
| 3 | 00:46:10 | milestone | E140 scoped: inspect_ai model_graded_fact rubric fetched verbatim; corpus is E114's 15 committed (doc,question,answer) triples; predeclaring arms/gate |
| 4 | 00:46:52 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/PROTOCOL.md |
| 5 | 00:46:53 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/judge_rubric.txt |
| 6 | 00:48:12 | command | $ python3 build_arms.py |
| 7 | 00:48:22 | command | $ python3 build_arms.py |
| 8 | 00:48:28 | command | $ python3 build_arms.py |
| 9 | 00:50:27 | command | $ python3 build_arms.py |
| 10 | 00:50:34 | command | $ python3 build_arms.py |
| 11 | 00:54:03 | command | $ python3 build_arms.py |
| 12 | 00:54:12 | command | $ python3 ./build_arms.py |
| 13 | 00:54:47 | command | $ python3 ./build_arms.py |
| 14 | 00:56:51 | milestone | Handover: E140 resumed. Found AMENDMENT-2's G0 denominator wrong - 4 of 15 answers carry no extractable value (not 3), 3 of those are judge items, so  |
| 15 | 00:58:35 | command | $ python3 finalize_p2.py |
| 16 | 00:58:40 | command | $ python3 EXPERIMENTS/140-judge-form-invariance/finalize_p2.py |
| 17 | 00:59:18 | command | $ python3 EXPERIMENTS/140-judge-form-invariance/finalize_p2.py |
| 18 | 01:00:43 | command | $ python3 EXPERIMENTS/140-judge-form-invariance/emit_judge_prompts.py |
| 19 | 01:00:53 | command | $ python3 EXPERIMENTS/140-judge-form-invariance/emit_judge_prompts.py |
| 20 | 01:07:43 | command | $ python3 EXPERIMENTS/140-judge-form-invariance/score.py |
| 21 | 01:07:56 | command | $ python3 EXPERIMENTS/140-judge-form-invariance/score.py |
| 22 | 01:08:48 | command | $ python3 EXPERIMENTS/140-judge-form-invariance/score.py |
| 23 | 01:09:24 | command | $ python3 EXPERIMENTS/140-judge-form-invariance/score.py |
| 24 | 01:09:59 | command | $ python3 EXPERIMENTS/140-judge-form-invariance/misattribution.py |
| 25 | 01:11:51 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/PROTOCOL.md |
| 26 | 01:11:52 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/AMENDMENT-1.md |
| 27 | 01:11:53 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/AMENDMENT-2.md |
| 28 | 01:11:56 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/AMENDMENT-3.md |
| 29 | 01:11:58 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/AMENDMENT-4.md |
| 30 | 01:12:00 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/AMENDMENT-5.md |
| 31 | 01:12:02 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/judge_rubric.txt |
| 32 | 01:12:04 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/p2.jsonl |
| 33 | 01:12:05 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/arms.jsonl |
| 34 | 01:12:07 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/gates.json |
| 35 | 01:12:08 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/misattribution.json |
| 36 | 01:12:09 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/score.py |
| 37 | 01:12:11 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/valueset.py |
| 38 | 01:12:12 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/build_arms.py |
| 39 | 01:12:13 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/finalize_p2.py |
| 40 | 01:12:14 | artifact | wrote EXPERIMENTS/140-judge-form-invariance/emit_judge_prompts.py |
| 93 | 01:47:51 | artifact | wrote DECISIONS-SCREENING-21.md |
| 94 | 01:47:53 | artifact | wrote FAILURES-findings-41.md |
| 95 | 01:47:54 | artifact | wrote DECISIONS.md |
| 96 | 01:47:56 | artifact | wrote FAILURES.md |
| 97 | 01:47:58 | artifact | wrote vendor/MANIFEST.md |
| 98 | 01:48:15 | artifact | wrote sessions/2026-10-13-042-explore-current-state-and-choose-next-in/README.md |
| 99 | 01:48:17 | artifact | wrote sessions/2026-10-13-042-explore-current-state-and-choose-next-in/events.jsonl |
| 100 | 01:48:41 | doc_update | updated DECISIONS.md |
| 101 | 01:48:41 | doc_update | updated FAILURES.md |
| 102 | 01:48:41 | session_end | E140 measured the form-invariance of the shipped inspect_ai model_graded_fact judge against a deterministic value canonicalizer on E114's committed co |

_52 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-001-measure-the-form-invariance-of-shipped-l/events.jsonl
```
