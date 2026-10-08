# Session 2026-10-08-006-fresh-observation-probe-per-d080-on-a-ne

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-08T05:00:14+00:00
- **Duration:** 1008.3s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh-observation probe per D080 on a new corpus/population; pre-register gates and kill or name a testable opportunity

## Summary

E058: ran E057's exact pre-registered protocol on the 38 Stack Exchange survivors E057 skipped (76 arms, 11092 rows, 7022 requesters). G1's nominal clusters all read as topics, no step survives; KILL, nothing built. Channel-level null extended to the whole survivor set; F090 recorded; STATE/FAILURES/index updated; doc lint OK

## Next

Continue the D080 fresh-observation search on a channel other than Stack Exchange (HN Algolia search or lobste.rs), holding the E057 lesson that corpus-named incumbents are the decisive gate

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/058-se-remaining-sites/README.md | 3d2accd1140e | 2999 |
| EXPERIMENTS/058-se-remaining-sites/PROTOCOL.md | 5c482a3ccfbe | 2005 |
| EXPERIMENTS/058-se-remaining-sites/fetch.py | 07d079149a5d | 3982 |
| EXPERIMENTS/058-se-remaining-sites/cluster.py | 9bc83bdd8719 | 6525 |
| FAILURES-findings-32.md | 0e50e2381ca1 | 2226 |
| FAILURES.md | c10d7fdfc679 | 53504 |
| STATE.md | 60acae107659 | 37625 |
| STATE.md | ff497605d558 | 37625 |

## Commands

7 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/058-se-remaining-sites/fetch.py'] | 0 | 271310 |
| 3 | ['python3', 'EXPERIMENTS/058-se-remaining-sites/cluster.py'] | 0 | 7414 |
| 11 | ['tools/origin', 'doc', 'index'] | 0 | 4294 |
| 12 | ['tools/origin', 'doc', 'index'] | 0 | 6479 |
| 13 | ['tools/origin', 'doc', 'lint'] | 0 | 151080 |
| 14 | ['tools/origin', 'doc', 'lint'] | 0 | 88676 |
| 16 | ['tools/origin', 'doc', 'lint'] | 0 | 57594 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 79 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/058-se-remaining-sites/raw/clusters.json |
|   undeclared | EXPERIMENTS/058-se-remaining-sites/raw/craftcms-head.json |
|   undeclared | EXPERIMENTS/058-se-remaining-sites/raw/craftcms-tail.json |
|   undeclared | EXPERIMENTS/058-se-remaining-sites/raw/diy-head.json |
|   undeclared | EXPERIMENTS/058-se-remaining-sites/raw/diy-tail.json |
|   undeclared | EXPERIMENTS/058-se-remaining-sites/raw/ebooks-head.json |
|   undeclared | EXPERIMENTS/058-se-remaining-sites/raw/ebooks-tail.json |
|   undeclared | EXPERIMENTS/058-se-remaining-sites/raw/eosio-head.json |
|   undeclared | EXPERIMENTS/058-se-remaining-sites/raw/eosio-tail.json |
|   undeclared | EXPERIMENTS/058-se-remaining-sites/raw/expatriates-head.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 05:00:14 | session_start | Fresh-observation probe per D080 on a new corpus/population; pre-register gates and kill or name a testable opportunity |
| 2 | 05:08:15 | command | $ python3 EXPERIMENTS/058-se-remaining-sites/fetch.py |
| 3 | 05:08:32 | command | $ python3 EXPERIMENTS/058-se-remaining-sites/cluster.py |
| 4 | 05:12:05 | artifact | wrote EXPERIMENTS/058-se-remaining-sites/README.md |
| 5 | 05:12:06 | artifact | wrote EXPERIMENTS/058-se-remaining-sites/PROTOCOL.md |
| 6 | 05:12:07 | artifact | wrote EXPERIMENTS/058-se-remaining-sites/fetch.py |
| 7 | 05:12:07 | artifact | wrote EXPERIMENTS/058-se-remaining-sites/cluster.py |
| 8 | 05:12:08 | artifact | wrote FAILURES-findings-32.md |
| 9 | 05:12:09 | artifact | wrote FAILURES.md |
| 10 | 05:12:09 | artifact | wrote STATE.md |
| 11 | 05:12:20 | command | $ tools/origin doc index |
| 12 | 05:13:46 | command | $ tools/origin doc index |
| 13 | 05:14:52 | command | $ tools/origin doc lint |
| 14 | 05:15:17 | command | $ tools/origin doc lint |
| 15 | 05:15:51 | artifact | wrote STATE.md |
| 16 | 05:16:49 | command | $ tools/origin doc lint |
| 17 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/clusters.json |
| 18 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/craftcms-head.json |
| 19 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/craftcms-tail.json |
| 20 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/diy-head.json |
| 21 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/diy-tail.json |
| 22 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/ebooks-head.json |
| 23 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/ebooks-tail.json |
| 24 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/eosio-head.json |
| 25 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/eosio-tail.json |
| 26 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/expatriates-head.json |
| 27 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/expatriates-tail.json |
| 28 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/expressionengine-head.json |
| 29 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/expressionengine-tail.json |
| 30 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/freelancing-head.json |
| 31 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/freelancing-tail.json |
| 32 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/genai-head.json |
| 33 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/genai-tail.json |
| 34 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/homebrew-head.json |
| 35 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/homebrew-tail.json |
| 36 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/index.json |
| 37 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/interpersonal-head.json |
| 38 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/interpersonal-tail.json |
| 39 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/iota-head.json |
| 40 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/iota-tail.json |
| 89 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/ux-tail.json |
| 90 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/vegetarianism-head.json |
| 91 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/vegetarianism-tail.json |
| 92 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/woodworking-head.json |
| 93 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/woodworking-tail.json |
| 94 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/writing-head.json |
| 95 | 05:17:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/058-se-remaining-sites/raw/writing-tail.json |
| 96 | 05:17:02 | doc_update | updated FAILURES.md |
| 97 | 05:17:02 | doc_update | updated STATE.md |
| 98 | 05:17:02 | session_end | E058: ran E057's exact pre-registered protocol on the 38 Stack Exchange survivors E057 skipped (76 arms, 11092 rows, 7022 requesters). G1's nominal cl |

_48 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-08-006-fresh-observation-probe-per-d080-on-a-ne/events.jsonl
```
