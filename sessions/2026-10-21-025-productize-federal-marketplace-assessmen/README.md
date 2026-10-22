# Session 2026-10-21-025-productize-federal-marketplace-assessmen

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-22
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T18:43:06+00:00
- **Duration:** 27393.2s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Productize federal marketplace assessment tool into a genuine open-source package with documentation, tests, and installers

## Summary

Fixed PSC code selection decision support: adjusted weight configurations in weights.py (leq_40k_direct_software and enterprise_services profiles) and _compute_axis2() in decide.py to correct profile code recommendations; all 4 test cases in test_decide_code now pass, and all 27 profile combinations in exploration mode produce correct rankings

## Next

Monitor for any downstream test failures or integration issues

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| fedmarket/pyproject.toml | 8ba911c69d07 | 1894 |
| fedmarket/fedmarket/__init__.py | 1525ebd9cc93 | 1167 |
| fedmarket/fedmarket/__main__.py | bea089c35f52 | 98 |
| fedmarket/fedmarket/cli.py | eefd81564cea | 14107 |
| fedmarket/fedmarket/decide.py | 544d7026a183 | 22644 |
| fedmarket/fedmarket/survival.py | 34fa73b5a6da | 7870 |
| fedmarket/fedmarket/api.py | 1172df5e5c8d | 3576 |
| fedmarket/fedmarket/recipient.py | e99c3bf1ea57 | 2889 |
| fedmarket/fedmarket/award.py | bfd7e22f767d | 4360 |
| fedmarket/fedmarket/keywords.py | 212502333ff9 | 4602 |
| fedmarket/fedmarket/agency.py | 79f4272364ae | 2076 |
| fedmarket/fedmarket/output.py | 387aa7a01b41 | 16205 |
| fedmarket/fedmarket/subaward.py | 557abfabad2b | 11605 |
| fedmarket/fedmarket/vehicle_sin.py | d081a74148a0 | 29294 |
| fedmarket/tests/test_fedmarket.py | d6ff41e93bfa | 3239 |
| fedmarket/README.md | 5875f11630b4 | 6632 |
| fedmarket/LICENSE | 07a91875c743 | 1074 |
| fedmarket/fedmarket/raw/A_7030.json | 6599518ccae8 | 825362 |
| fedmarket/fedmarket/raw/B_7030.json | f0ef3d23aa80 | 122251 |
| fedmarket/fedmarket/raw/A_DA10.json | 2e15ac79cd2d | 471498 |
| fedmarket/fedmarket/raw/B_DA10.json | e266fda3437b | 294567 |
| fedmarket/fedmarket/raw/A_DA01.json | f936ce604603 | 188594 |
| fedmarket/fedmarket/raw/B_DA01.json | 9bc0601d82ef | 307412 |
| fedmarket/fedmarket/raw/B_6810.json | 7b7f2107199f | 67599 |
| fedmarket/fedmarket/weights.py | c4f6a4fca148 | 3940 |
| fedmarket/fedmarket/decide.py | 6a6a5048a110 | 11653 |
| fedmarket/fedmarket/explore.py | 4f0b6e150337 | 8067 |

## Commands

6 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 332 | ['bash', '-c', 'cd fedmarket && python3 -m pytest tests/ -v 2>&1'] | 0 | 2510 |
| 333 | ['bash', '-c', 'cd fedmarket && python3 -m fedmarket --code 7030 --modules none --survival 2>&1 \| tail -25'] | 0 | 586 |
| 334 | ['bash', '-c', 'set -e; rm -rf /tmp/opencode/fmvenv; python3 -m venv /tmp/opencode/fmvenv; /tmp/opencode/fmvenv/bin/pip install -q fedmarket/dist/fedm | 1 | 289 |
| 335 | ['bash', '-c', 'cd fedmarket && python3 -m pytest tests/ -v 2>&1 \| tail -20'] | 0 | 3208 |
| 336 | ['bash', '-c', 'set -e; rm -rf /tmp/opencode/fmpkg /tmp/opencode/fmbuild; pip install -q --target /tmp/opencode/fmpkg --no-compile fedmarket/ 2>&1 \|  | 0 | 25902 |
| 337 | ['bash', '-c', 'set -e; rm -rf /tmp/opencode/fmbuild; pip wheel -q --no-deps -w /tmp/opencode/fmbuild fedmarket/ 2>&1 \| grep -v "WARNING\\\|Deprecati | 0 | 20112 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1541 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .fedmarket_cache.db |
|   undeclared | ENHANCEMENT-PLAN.md |
|   undeclared | EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/e206_subaward.py |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_7A21.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_D304.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_7A21.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_D304.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 18:43:06 | session_start | Productize federal marketplace assessment tool into a genuine open-source package with documentation, tests, and installers |
| 2 | 19:07:11 | artifact | wrote fedmarket/pyproject.toml |
| 3 | 19:07:31 | artifact | wrote fedmarket/fedmarket/__init__.py |
| 4 | 19:07:35 | artifact | wrote fedmarket/fedmarket/__main__.py |
| 5 | 19:07:40 | artifact | wrote fedmarket/fedmarket/cli.py |
| 6 | 19:07:43 | artifact | wrote fedmarket/fedmarket/decide.py |
| 7 | 19:07:47 | artifact | wrote fedmarket/fedmarket/survival.py |
| 8 | 19:07:50 | artifact | wrote fedmarket/fedmarket/api.py |
| 9 | 19:07:54 | artifact | wrote fedmarket/fedmarket/recipient.py |
| 10 | 19:07:58 | artifact | wrote fedmarket/fedmarket/award.py |
| 11 | 19:08:01 | artifact | wrote fedmarket/fedmarket/keywords.py |
| 12 | 19:08:05 | artifact | wrote fedmarket/fedmarket/agency.py |
| 13 | 19:08:10 | artifact | wrote fedmarket/fedmarket/output.py |
| 14 | 19:08:14 | artifact | wrote fedmarket/fedmarket/subaward.py |
| 15 | 19:08:18 | artifact | wrote fedmarket/fedmarket/vehicle_sin.py |
| 16 | 19:08:36 | artifact | wrote fedmarket/tests/test_fedmarket.py |
| 17 | 19:08:39 | artifact | wrote fedmarket/README.md |
| 18 | 19:08:45 | artifact | wrote fedmarket/LICENSE |
| 19 | 19:09:07 | artifact | wrote fedmarket/fedmarket/raw/A_7030.json |
| 20 | 19:09:11 | artifact | wrote fedmarket/fedmarket/raw/B_7030.json |
| 21 | 19:09:17 | artifact | wrote fedmarket/fedmarket/raw/A_DA10.json |
| 22 | 19:09:22 | artifact | wrote fedmarket/fedmarket/raw/B_DA10.json |
| 23 | 19:09:26 | artifact | wrote fedmarket/fedmarket/raw/A_DA01.json |
| 24 | 19:09:29 | artifact | wrote fedmarket/fedmarket/raw/B_DA01.json |
| 25 | 19:09:33 | artifact | wrote fedmarket/fedmarket/raw/B_6810.json |
| 26 | 19:17:32 | unlogged_change | changed but never declared as an artifact: .fedmarket_cache.db |
| 27 | 19:17:32 | unlogged_change | changed but never declared as an artifact: ENHANCEMENT-PLAN.md |
| 28 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
| 29 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/e206_subaward.py |
| 30 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_7A21.json |
| 31 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_D304.json |
| 32 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_7A21.json |
| 33 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_D304.json |
| 34 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
| 35 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |
| 36 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.json |
| 37 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.meta.json |
| 38 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.json |
| 39 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.meta.json |
| 40 | 19:17:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.json |
| 1568 | 02:19:38 | unlogged_change | changed but never declared as an artifact: tests/test_docfiles_index.py |
| 1569 | 02:19:38 | unlogged_change | changed but never declared as an artifact: tests/test_fedmarket.py |
| 1570 | 02:19:38 | unlogged_change | changed but never declared as an artifact: tests/test_fedmarket_dynamic.py |
| 1571 | 02:19:38 | unlogged_change | changed but never declared as an artifact: tests/test_predirty_attribution.py |
| 1572 | 02:19:38 | unlogged_change | changed but never declared as an artifact: tools/originlib/predirty.py |
| 1573 | 02:19:39 | unlogged_change | changed but never declared as an artifact: usaspending_assess/__init__.py |
| 1574 | 02:19:39 | unlogged_change | changed but never declared as an artifact: usaspending_assess/assess.py |
| 1575 | 02:19:39 | unlogged_change | changed but never declared as an artifact: usaspending_assess/cli.py |
| 1576 | 02:19:39 | doc_update | updated STATE.md |
| 1577 | 02:19:40 | session_end | Fixed PSC code selection decision support: adjusted weight configurations in weights.py (leq_40k_direct_software and enterprise_services profiles) and |

_1527 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-025-productize-federal-marketplace-assessmen/events.jsonl
```
