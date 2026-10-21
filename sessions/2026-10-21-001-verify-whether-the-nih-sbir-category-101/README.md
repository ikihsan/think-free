# Session 2026-10-21-001-verify-whether-the-nih-sbir-category-101

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T00:04:04+00:00
- **Duration:** 26933.9s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Verify whether the NIH SBIR category-101 accessibility finding (E204/E206) survives a complete, SBIR-filtered census of FY2023 RePORTER data, since it sits at STATE.md's reload point and is encoded in a committed prototype

## Summary

E207 verified the reload-point number, and the 2026-10-20/21 backlog is landed in commit 4bd8d91d. A complete R41/R42 FY2023 RePORTER census (368 rows, stopped by the API's meta.total, no cap, no sampling) reproduces E204's category-101 headline to the dollar - 147 grants, 134 distinct orgs, top-5 share 0.1159, $63,254,235 - all five predeclared gates PASS, and the script plus raw data that E204/E206 never had are committed beside the result (D128: verify a reload-point number by re-deriving it from the population it names). Landing: 113 paths, every one declared with sha256, reconcile pre-check unlogged 0; doc lint OK, doc index current, release check OK (194 paths) after classifying the three new top-level splits as internal in RELEASE-MANIFEST.md, which release check refused to pass while they were unclassified; full suite captured through tools/x at 849 tests with exactly 1 failure - F151, a fixture that pins git check-ignore exiting 0 for a negated path while this VM's git 2.50.1 exits 1 (reproduced in an isolated repository, the other 848 tests pass); neither the assertion nor the gate was weakened, and STATE.md's stale claim that this VM runs git 2.25.1 was corrected to the observed 2.50.1. Pre-existing and deliberately not repaired: session verify reports two unfinished sessions (2026-10-10-013, 2026-10-19-005) that only their own event streams can close, so preflight still exits 2 although release check now passes. Nothing was pushed: no remote publication was requested or performed.

## Next

Run E208, the entrant-share screen on NIH SBIR category 101: fetch R41/R42 awards for FY2014-FY2023 from RePORTER with gates declared in a PROTOCOL before any fetch, and measure what fraction of FY2023 category-101 award-holding organizations had no award in that segment in the previous five years, against the same fraction in a concentrated category - this tests the unmeasured step between 'the vendor landscape is fragmented' and 'a small program can actually enter'

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E207-sbir-category101-census/PROTOCOL.md | c7b4031004eb | 4857 |
| EXPERIMENTS/E207-sbir-category101-census/census.py | 8f448dca3581 | 4088 |
| EXPERIMENTS/E207-sbir-category101-census/RESULT.md | f63b503f0d07 | 4850 |
| EXPERIMENTS/E207-sbir-category101-census/raw/census.json | 4fc51c7e7018 | 4580146 |
| EXPERIMENTS/E207-sbir-category101-census/summary.json | e3f5b8c145e4 | 26226 |
| .gitignore | 8253fd3e7235 | 7393 |
| DECISIONS-RECORDS-6.md | 455924903eae | 10002 |
| DECISIONS.md | 079eeecea3d5 | 35467 |
| EXPERIMENTS/113-viewcount-matched-harvest/README.md | 13a78b9330f3 | 6533 |
| EXPERIMENTS/121-codereview-e119/README.md | ddf89b78eb65 | 6132 |
| EXPERIMENTS/130-hex-viewcount-prototype/README.md | 931dccf380a1 | 2288 |
| EXPERIMENTS/131-viewcount-java-repos-matched-harvest/RESULTS.md | f6a445ca4e2d | 5302 |
| EXPERIMENTS/132-viewcount-rust-repos-matched-harvest/RESULTS.md | 091959c2a352 | 4858 |
| EXPERIMENTS/136-ultraeval-adapter/README.md | 4909a8ed552b | 878 |
| EXPERIMENTS/138-cicd-debugging-fresh/README.md | 7ba7633350de | 4616 |
| EXPERIMENTS/141-scorer-false-negatives/RESULT.md | ff196dc7f769 | 9351 |
| EXPERIMENTS/144-ofx-merchant-noise/raw/SOURCES.md | 5019051dcb09 | 853 |
| EXPERIMENTS/174-scoped-reach-recompute/RESULT.md | 22bb584b1281 | 6737 |
| EXPERIMENTS/175-repo-from-report/RESULT.md | 7a655c7df3f6 | 7919 |
| EXPERIMENTS/185-knitting-repair-planner-stage-a/RESULT.md | ecb8e5c2f025 | 5836 |
| EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-1.md | e4883c87c796 | 2872 |
| EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-2.md | a88e827fd39d | 2595 |
| EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-3.md | 5b03b601575c | 5502 |
| EXPERIMENTS/202-line-anchor-rewrite/PRIOR-ART.md | b56ab6396371 | 5114 |
| EXPERIMENTS/202-line-anchor-rewrite/PROTOCOL.md | 6e8a191e0926 | 8733 |
| EXPERIMENTS/202-line-anchor-rewrite/RESULT.md | 75074540a598 | 9829 |
| EXPERIMENTS/202-line-anchor-rewrite/analyze.js | f3eac7c643ee | 7026 |
| EXPERIMENTS/202-line-anchor-rewrite/corpus-manifest.json | 1a52013955b4 | 40006 |
| EXPERIMENTS/202-line-anchor-rewrite/fetch.js | 6300fc7b3df2 | 6164 |
| EXPERIMENTS/202-line-anchor-rewrite/fetch2.js | dcfe537293a1 | 4628 |
| EXPERIMENTS/202-line-anchor-rewrite/fixtures/k1.html | 5a5c6909c8a7 | 1005 |
| EXPERIMENTS/202-line-anchor-rewrite/gates.json | 31dccc146dba | 2497 |
| EXPERIMENTS/202-line-anchor-rewrite/merge-g0.js | 656a695446e3 | 6777 |
| EXPERIMENTS/202-line-anchor-rewrite/package.json | e3d4710e994a | 585 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/issue-codecrew57.json | f2f3a3d0685a | 4022 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/issue-crawl4ai5.json | 8f9c572e3809 | 7695 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/issue-ras462.json | e0aff01a07e6 | 3411 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/pa-anchor-linenums-a11y.json | 9e91ee0788bf | 150957 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/pa-codelineno-remove.json | f2b225b3e8e7 | 97904 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/pa-codelineno-visibility.json | 6137e79264ac | 100465 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/pa-linkname-codelineno.json | e9762fa3785f | 184036 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/pa-repos-codelineno.json | 4af480b8ee5b | 55 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/probe-anchor-linenums.json | c423cb8cc856 | 4098 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/probe-codelineno.json | a238c10e00c5 | 4097 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/search-repoA.json | 71a1e30df8bc | 278390 |
| EXPERIMENTS/202-line-anchor-rewrite/raw/search-repoB.json | 1828940fd282 | 283429 |
| EXPERIMENTS/202-line-anchor-rewrite/results-arms.json | 17f8c40d8cf3 | 159179 |
| EXPERIMENTS/202-line-anchor-rewrite/results-control.json | 904efdfdd14f | 3446 |
| EXPERIMENTS/202-line-anchor-rewrite/results-g0.json | 910d77802385 | 4118 |
| EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0-part0.json | 7241a9035751 | 129292 |
| EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0-part1.json | 3fab94cf1427 | 40188 |
| EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0-part2.json | 5d6756f630b4 | 35646 |
| EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0.json | c4612c264e4d | 170131 |
| EXPERIMENTS/202-line-anchor-rewrite/run-arms.js | 828eaedfc49c | 8593 |
| EXPERIMENTS/202-line-anchor-rewrite/shard-sweep.js | f014f7691cbb | 3301 |
| EXPERIMENTS/202-line-anchor-rewrite/sweep.js | 6e628c854b53 | 2076 |
| EXPERIMENTS/E199-candidate-screen/screen.py | 45cec8ea14d8 | 4747 |
| EXPERIMENTS/E200-subsegment-screen/screen.py | d5ad67864bd8 | 7408 |
| EXPERIMENTS/E201-practical-access/screen.py | 22c69266d58f | 5892 |
| EXPERIMENTS/E203-github-repos-viewcount-20261020201751/RESULT.md | c57bc2976789 | 4902 |
| EXPERIMENTS/E203-github-repos-viewcount-20261020201751/raw/run-1792527618.json | cdf1029b8045 | 478 |
| EXPERIMENTS/E203-github-repos-viewcount-20261020201751/raw/run-1792527660.json | a1b79519bb3b | 866 |
| EXPERIMENTS/E204-sbir-spending-category-screen/RESULT.md | 487d7fb94914 | 8818 |
| EXPERIMENTS/E205-crate-io-viewcount/RESULT.md | 09eb2c26bc31 | 4631 |
| EXPERIMENTS/E206-sbir-subsegment-category101/RESULT.md | 5419377433e5 | 10319 |
| EXPERIMENTS/e203-project-evaluation/RESULT.md | c106f5a005e9 | 11721 |
| EXPERIMENTS/e203-project-evaluation/eval-results.jsonl | bc95c7225092 | 5469 |
| EXPERIMENTS/e203-project-evaluation/eval-summary.json | ae376c08e78f | 704 |
| EXPERIMENTS/nih-sbir-multi-category-screen/RESULT.md | c3bd11aec1d4 | 11413 |
| FAILURES-findings-43.md | d981eb83ae5e | 12222 |
| FAILURES-findings-48.md | 39f119588efc | 7483 |
| FAILURES.md | 5251ef1c7823 | 117172 |
| README.md | 7b9d3fb48fb4 | 5282 |
| STATE-next-actions-archive-evid.md | 9193d1d89577 | 10419 |
| STATE-next-actions-archive-money.md | c6ae3761415d | 9450 |
| STATE-next-actions.md | 49a8ff85125a | 8534 |
| STATE.md | bab96bd6c3a9 | 33632 |
| sessions/2026-10-20-001-land-the-two-diverged-lineages-then-run/commands.log | e6ed20dcd87f | 25971 |
| sessions/2026-10-20-001-land-the-two-diverged-lineages-then-run/events.jsonl | f62cf35754c2 | 39075 |
| sessions/2026-10-20-002-verify-and-record-e203-experiment-contin/events.jsonl | a38c11319294 | 27269 |
| sessions/2026-10-20-004-continue-e204-nih-sbir-experiment-and-do/events.jsonl | 2cb453640d6d | 29701 |
| sessions/2026-10-20-005-run-sub-segment-screen-within-nih-sbir-c/events.jsonl | 8d531ea01b22 | 29132 |
| sessions/2026-10-20-006-review-session-outcomes-and-prepare-for/events.jsonl | dae42c1e5f4f | 30485 |
| sessions/2026-10-20-007-continue-e206-follow-up-practical-resour/events.jsonl | f2d1767b21bd | 32008 |
| sessions/2026-10-20-008-prototype-ic-recommendation-feature-for/events.jsonl | bdf39cd8e8b2 | 31752 |
| sessions/2026-10-20-009-summarize-session-t-0095-contributions/events.jsonl | b3ed3f94ad2f | 31764 |
| sessions/2026-10-20-010-build-nih-sbir-multi-category-accessibil/events.jsonl | 84b7efa2878e | 33175 |
| sessions/2026-10-20-011-finalize-nih-sbir-multi-category-accessi/events.jsonl | 41003f661d67 | 34685 |
| tools/nih_sbir_metrics.py | 7e0f14435cdd | 5509 |
| tools/nih_sbir_screener.py | 1614b96c3bd0 | 8663 |
| tools/nih_sbir_subsegment.py | fad286be5264 | 7538 |
| tools/nih_small_program_screener.py | 2b2e28bc2e8d | 1176 |
| tools/regvalue/README.md | 71aa56ccd760 | 4568 |
| vendor/MANIFEST.md | 801af5b44e34 | 16517 |
| RELEASE-MANIFEST.md | 6248169f0ee3 | 9839 |
| STATE.md | e3ebaf20a7d0 | 33890 |
| FAILURES.md | 30498e8ee71d | 118266 |
| FAILURES-findings-48.md | 1ef56c0aea04 | 10333 |
| FAILURES.md | 30498e8ee71d | 118266 |

## Commands

24 captured, 8 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', '/tmp/opencode/probe_population.py'] | 0 | 15334 |
| 4 | ['python3', '/tmp/opencode/census_probe.py'] | 1 | 5996 |
| 5 | ['python3', '/tmp/opencode/census_probe2.py'] | 0 | 1573 |
| 6 | ['python3', 'EXPERIMENTS/E207-sbir-category101-census/census.py'] | 0 | 19427 |
| 7 | ['python3', '/tmp/opencode/check_gates.py'] | 1 | 913 |
| 8 | ['python3', '/tmp/opencode/check_gates.py'] | 0 | 240 |
| 17 | ['tools/origin', 'doc', 'lint'] | 2 | 5173507 |
| 18 | ['python3', '/tmp/opencode/verify_backlog_exemptions.py'] | 1 | 6807 |
| 19 | ['python3', '/tmp/opencode/verify_backlog_exemptions.py'] | 0 | 13895 |
| 20 | ['python3', '/tmp/opencode/prestage_cap_check.py'] | 1 | 17205 |
| 21 | ['python3', '/tmp/opencode/verify_backlog_exemptions.py'] | 0 | 7284 |
| 22 | ['python3', '/tmp/opencode/prestage_cap_check.py'] | 0 | 18100 |
| 23 | ['tools/origin', 'doc', 'index'] | 0 | 28608 |
| 24 | ['tools/origin', 'doc', 'lint'] | 0 | 1504301 |
| 25 | ['python3', '/tmp/opencode/compute_unlogged.py'] | 0 | 3284 |
| 26 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 2183537 |
| 27 | ['python3', '/tmp/opencode/compute_unlogged.py'] | 0 | 853 |
| 118 | ['python3', '/tmp/opencode/compute_unlogged.py'] | 0 | 1283 |
| 119 | ['tools/origin', 'doc', 'lint'] | 0 | 860092 |
| 120 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 1307479 |
| 121 | ['./tools/origin', 'preflight'] | 2 | 417876 |
| 128 | ['./tools/origin', 'release', 'check'] | 0 | 85224 |
| 129 | ['./tools/origin', 'doc', 'lint'] | 0 | 343512 |
| 130 | ['git', 'commit', '-F', '/tmp/opencode/commitmsg.txt'] | 0 | 679 |

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
| 1 | 00:04:04 | session_start | Verify whether the NIH SBIR category-101 accessibility finding (E204/E206) survives a complete, SBIR-filtered census of FY2023 RePORTER data, since it |
| 2 | 00:04:32 | milestone | identified concrete integrity problem: E204/E206 marked completed at STATE.md reload point with specific numbers, but directories hold only RESULT.md  |
| 3 | 00:04:46 | command | $ python3 /tmp/opencode/probe_population.py |
| 4 | 00:05:33 | command | $ python3 /tmp/opencode/census_probe.py |
| 5 | 00:05:49 | command | $ python3 /tmp/opencode/census_probe2.py |
| 6 | 00:07:16 | command | $ python3 EXPERIMENTS/E207-sbir-category101-census/census.py |
| 7 | 00:07:53 | command | $ python3 /tmp/opencode/check_gates.py |
| 8 | 00:08:33 | command | $ python3 /tmp/opencode/check_gates.py |
| 9 | 00:11:08 | milestone | E207 census run: complete R41/R42 FY2023 census (368 rows) reproduces E204 category-101 headline exactly — 147 grants, 134 orgs, top5 11.59%, $63,254, |
| 10 | 00:13:28 | artifact | wrote EXPERIMENTS/E207-sbir-category101-census/PROTOCOL.md |
| 11 | 00:13:30 | artifact | wrote EXPERIMENTS/E207-sbir-category101-census/census.py |
| 12 | 00:13:32 | artifact | wrote EXPERIMENTS/E207-sbir-category101-census/RESULT.md |
| 13 | 00:13:37 | artifact | wrote EXPERIMENTS/E207-sbir-category101-census/raw/census.json |
| 14 | 00:13:39 | artifact | wrote EXPERIMENTS/E207-sbir-category101-census/summary.json |
| 15 | 00:13:40 | decision | D128: a number at the reload point is verified by re-deriving it from the population it names; a committed prototype whose sampling cannot produce tha |
| 16 | 01:03:55 | milestone | recovered post-restart: E207 work intact on disk; doc lint baseline established - 49 violations pre-exist at HEAD (files byte-identical to HEAD), 6 fr |
| 17 | 04:07:19 | command | $ tools/origin doc lint |
| 18 | 04:47:15 | command | $ python3 /tmp/opencode/verify_backlog_exemptions.py |
| 19 | 04:49:08 | command | $ python3 /tmp/opencode/verify_backlog_exemptions.py |
| 20 | 04:50:51 | command | $ python3 /tmp/opencode/prestage_cap_check.py |
| 21 | 04:59:53 | command | $ python3 /tmp/opencode/verify_backlog_exemptions.py |
| 22 | 05:00:23 | command | $ python3 /tmp/opencode/prestage_cap_check.py |
| 23 | 05:03:31 | command | $ tools/origin doc index |
| 24 | 05:29:07 | command | $ tools/origin doc lint |
| 25 | 05:38:37 | command | $ python3 /tmp/opencode/compute_unlogged.py |
| 26 | 05:40:25 | command | $ python3 -m unittest discover -s tests -t tests |
| 27 | 05:40:31 | command | $ python3 /tmp/opencode/compute_unlogged.py |
| 28 | 05:47:31 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 29 | 05:47:33 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 30 | 05:47:35 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 31 | 05:47:37 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 32 | 05:47:38 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 33 | 05:47:40 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 34 | 05:47:41 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 35 | 05:47:44 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 36 | 05:47:47 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 37 | 05:47:48 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 38 | 05:47:50 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 39 | 05:47:52 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 40 | 05:47:53 | artifact | landing declaration: sha256 recorded while landing the uncommitted 2026-10-20/21 backlog; content verified against latest prior declarations where the |
| 126 | 07:23:30 | note | git on this VM is 2.50.1 (git --version and doctor, observed 2026-10-21), not the 2.25.1 STATE.md claimed; tests/git-versions.json lists 2.50.1 as unr |
| 127 | 07:23:45 | artifact | wrote FAILURES.md |
| 128 | 07:25:29 | command | $ ./tools/origin release check |
| 129 | 07:31:26 | command | $ ./tools/origin doc lint |
| 130 | 07:32:20 | command | $ git commit -F /tmp/opencode/commitmsg.txt |
| 131 | 07:32:57 | doc_update | updated DECISIONS-RECORDS-6.md |
| 132 | 07:32:57 | doc_update | updated DECISIONS.md |
| 133 | 07:32:57 | doc_update | updated FAILURES.md |
| 134 | 07:32:57 | doc_update | updated STATE.md |
| 135 | 07:32:57 | session_end | E207 verified the reload-point number, and the 2026-10-20/21 backlog is landed in commit 4bd8d91d. A complete R41/R42 FY2023 RePORTER census (368 rows |

_85 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-001-verify-whether-the-nih-sbir-category-101/events.jsonl
```
