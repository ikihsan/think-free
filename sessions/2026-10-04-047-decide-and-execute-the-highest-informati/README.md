# Session 2026-10-04-047-decide-and-execute-the-highest-informati

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T20:22:19+00:00
- **Duration:** 4273.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Decide and execute the highest-information research action after 12 prior-art deaths: test whether the mission's selection rule, not the candidates, is the cause

## Summary

T-0059 / F032: counted registry installs instead of stars in five niches and found stars do not predict installs anywhere (|rho| <= 0.35, mature included), so F028's star tail was never a statement about adoption. Three young vocabularies have 88-100% of leading implementations with no measurable monthly install, so a crowded niche is the normal state of every crowded vocabulary and 'prior art exists' cannot mean 'served'. Three instrument defects were caught by pre-flight, each of which would have flattered the hypothesis, including an HTTP 200 meaning 'rate limited' read as zero downloads and a package name matching a repository it does not belong to (25% of the time), which under-counted the mature arm's leader by three orders of magnitude. Renumbered F029 to F032 and 012 to 013 on landing.

## Next

Decide the install-path axis with the owner and falsify it: find a crowded niche whose incumbents ARE heavily installed, which is the one observation that would show the axis fails. Alternative if the owner declines: re-run 013 on niches outside software registries, since registry installs cannot see binary-distributed tools and that is what made the gate's dead branch inexecutable.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/012-prior-art-predicts-adoption/results.json | ab5cb539e002 | 54863 |
| STATE.md | 7d3c28b507f4 | 26720 |
| FAILURES.md | 910d7f5bb482 | 6653 |
| FAILURES-findings-6.md | 5c2a2d8ec826 | 15858 |
| AGENTS.md | a8092dda5c62 | 8434 |
| docs/INDEX.md | a37320a7f112 | 22145 |
| EXPERIMENTS/012-prior-art-predicts-adoption/README.md | 4648addabd79 | 4732 |
| EXPERIMENTS/README.md | 786d2f1ec4b7 | 2070 |
| EXPERIMENTS/README.md | a210a8c95905 | 2098 |

## Commands

2 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 6 | ['tools/origin', 'doc', 'lint'] | 0 | 3814 |
| 7 | ['git', 'add', '-A'] | 0 | 17 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 7 |
| declared artifacts now missing | 0 |
| integrity errors | 2 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/013-prior-art-predicts-adoption/README.md |
|   undeclared | EXPERIMENTS/013-prior-art-predicts-adoption/census.py |
|   undeclared | EXPERIMENTS/013-prior-art-predicts-adoption/results.json |
|   undeclared | EXPERIMENTS/013-prior-art-predicts-adoption/run.log |
|   undeclared | EXPERIMENTS/013-prior-art-predicts-adoption/stats.py |
|   undeclared | EXPERIMENTS/013-prior-art-predicts-adoption/usage.py |
|   undeclared | tests/test_census_stats.py |
|   error | declared artifact no longer exists: EXPERIMENTS/012-prior-art-predicts-adoption/README.md |
|   error | declared artifact no longer exists: EXPERIMENTS/012-prior-art-predicts-adoption/results.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 20:22:19 | session_start | Decide and execute the highest-information research action after 12 prior-art deaths: test whether the mission's selection rule, not the candidates, i |
| 2 | 20:25:04 | task_rewrite | appended a create record for T-0059 |
| 3 | 20:26:16 | task_rewrite | rewrote tasks/T-0059-measure-whether-prior-art-exists-can-predict-any.md (status: claimed) |
| 4 | 20:26:16 | task_rewrite | appended a claim record for T-0059 |
| 5 | 20:50:50 | artifact | wrote EXPERIMENTS/012-prior-art-predicts-adoption/results.json |
| 6 | 21:02:21 | command | $ tools/origin doc lint |
| 7 | 21:02:32 | command | $ git add -A |
| 8 | 21:02:34 | milestone | T-0059 census run: stars do not predict installs in 5/5 niches; H survives; F029 written |
| 9 | 21:02:39 | artifact | wrote STATE.md |
| 10 | 21:02:39 | artifact | wrote FAILURES.md |
| 11 | 21:02:40 | artifact | wrote FAILURES-findings-6.md |
| 12 | 21:02:41 | artifact | wrote AGENTS.md |
| 13 | 21:02:41 | artifact | wrote docs/INDEX.md |
| 14 | 21:02:42 | artifact | wrote EXPERIMENTS/012-prior-art-predicts-adoption/README.md |
| 15 | 21:02:53 | note | updated STATE.md |
| 16 | 21:02:54 | note | updated FAILURES.md |
| 17 | 21:02:54 | note | updated FAILURES-findings-6.md |
| 18 | 21:02:55 | note | updated AGENTS.md |
| 19 | 21:02:55 | note | updated docs/INDEX.md |
| 20 | 21:30:55 | base_advance | rebase completed outside land: base moved 5bb2e2409339 -> 682f43ee7913, 11 commit(s) arrived from the shared base |
| 21 | 21:31:09 | base_advance | sync land: base moved 738094b536a7 -> 76e471dd0875, 1 commit(s) arrived from the shared base |
| 22 | 21:31:18 | task_rewrite | rewrote tasks/T-0059-measure-whether-prior-art-exists-can-predict-any.md (status: done) |
| 23 | 21:31:18 | task_rewrite | appended a complete record for T-0059 |
| 24 | 21:32:01 | note | updated EXPERIMENTS/README.md with the inventory including 013 |
| 25 | 21:32:01 | artifact | wrote EXPERIMENTS/README.md |
| 26 | 21:33:04 | artifact | wrote EXPERIMENTS/README.md |
| 27 | 21:33:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-prior-art-predicts-adoption/README.md |
| 28 | 21:33:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-prior-art-predicts-adoption/census.py |
| 29 | 21:33:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-prior-art-predicts-adoption/results.json |
| 30 | 21:33:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-prior-art-predicts-adoption/run.log |
| 31 | 21:33:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-prior-art-predicts-adoption/stats.py |
| 32 | 21:33:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-prior-art-predicts-adoption/usage.py |
| 33 | 21:33:31 | unlogged_change | changed but never declared as an artifact: tests/test_census_stats.py |
| 34 | 21:33:31 | integrity_error | declared artifact no longer exists: EXPERIMENTS/012-prior-art-predicts-adoption/README.md |
| 35 | 21:33:31 | integrity_error | declared artifact no longer exists: EXPERIMENTS/012-prior-art-predicts-adoption/results.json |
| 36 | 21:33:32 | doc_update | updated FAILURES.md |
| 37 | 21:33:32 | doc_update | updated STATE.md |
| 38 | 21:33:32 | session_end | T-0059 / F032: counted registry installs instead of stars in five niches and found stars do not predict installs anywhere (\|rho\| <= 0.35, mature inc |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-047-decide-and-execute-the-highest-informati/events.jsonl
```
