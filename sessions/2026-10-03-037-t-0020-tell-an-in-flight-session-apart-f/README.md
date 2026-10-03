# Session 2026-10-03-037-t-0020-tell-an-in-flight-session-apart-f

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-03T22:35:16+00:00
- **Duration:** 1248.0s
- **Host:** `instance-20260717-0947`
- **Branch:** `task/T-0020-instance-20260717-0947`

## Goal

T-0020: tell an in-flight session apart from an abandoned one in session verify, so one VM's live session stops reddening every other VM's CI

## Summary

T-0020 complete. The strict session gate now separates in-flight from abandoned: five clauses read off the tree plus a 12-hour claim lease (D024), so 'session verify --strict' exits 0 while instance-20260717-0944's session 030 is genuinely in flight and exits 4 naming the failing clause once the claim closes or expires. ci.yml re-emits each in-flight line as a public ::warning::. Each clause has a test proven to fail by mutation. Two further defects found by executing the documented VM sequence: worktree add refused the claiming VM's own claim and refusals printed tracebacks (F012), and the local claim view ignored takeover while the remote view honoured it (F013).

## Next

Land the branch, then read the pushed CI run and record its result in STATE.md: local green is not the same claim. T-0017 remains with instance-20260717-0944. Unclaimed and unfixed: doctor does not compare a VM's git against tests/git-versions.json; reconciliation compares trees not authorship; identifiers are allocated from the local tree.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/inflight.py | b99b5bc480ea | 7732 |
| tools/originlib/cli_session.py | 296cb5eb3660 | 11227 |
| tools/originlib/cli.py | d73abef425f2 | 11610 |
| tools/originlib/cli_repo.py | eedde56f87ac | 4058 |
| tools/originlib/worktree.py | 10353a3d17d0 | 6840 |
| tools/originlib/tasks.py | 4a35afcb0f7e | 7608 |
| tests/test_inflight_session.py | 481fe837c7ac | 8371 |
| tests/test_fleet.py | efb1db0643c5 | 10164 |
| tests/harness.py | 93654b5838b8 | 8007 |
| tests/README.md | 45ac9a196291 | 3059 |
| .github/workflows/ci.yml | fe5e2a3429d7 | 2682 |
| DECISIONS-GATING.md | 244cb4b3ceaa | 13506 |
| FAILURES.md | c80566b27c19 | 3912 |
| FAILURES-findings-2.md | 3ce5d031f46f | 11992 |
| FAILURES-findings-3.md | 6135025256b8 | 3951 |
| STATE.md | d5c1b06fc2c1 | 18016 |
| STATE-history.md | 91b459c2c2e3 | 10092 |
| ROADMAP.md | e5f00f6b0149 | 8042 |
| docs/operations/ci.md | 76cd49b7c1a0 | 6612 |
| docs/process/multi-vm-coordination.md | ffc7022ad7b7 | 4324 |
| docs/process/session-protocol.md | a5f54144993d | 7120 |
| docs/reference/cli-reference.md | b11e829c562b | 6092 |
| sessions/README.md | 41961999b11d | 3886 |
| tasks/T-0020-tell-an-in-flight-session-apart-from-an-abandone.md | 9d5b49d434f6 | 4784 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 28 | ['tools/origin', 'task', 'verify', 'T-0020'] | 0 | 102620 |

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
| 1 | 22:35:16 | session_start | T-0020: tell an in-flight session apart from an abandoned one in session verify, so one VM's live session stops reddening every other VM's CI |
| 2 | 22:38:12 | milestone | classification lands: strict verify exits 0 with session 030 genuinely in flight on the other VM |
| 3 | 22:53:41 | artifact | wrote tools/originlib/inflight.py |
| 4 | 22:53:41 | artifact | wrote tools/originlib/cli_session.py |
| 5 | 22:53:41 | artifact | wrote tools/originlib/cli.py |
| 6 | 22:53:41 | artifact | wrote tools/originlib/cli_repo.py |
| 7 | 22:53:41 | artifact | wrote tools/originlib/worktree.py |
| 8 | 22:53:41 | artifact | wrote tools/originlib/tasks.py |
| 9 | 22:53:41 | artifact | wrote tests/test_inflight_session.py |
| 10 | 22:53:41 | artifact | wrote tests/test_fleet.py |
| 11 | 22:53:41 | artifact | wrote tests/harness.py |
| 12 | 22:53:41 | artifact | wrote tests/README.md |
| 13 | 22:53:41 | artifact | wrote .github/workflows/ci.yml |
| 14 | 22:53:41 | artifact | wrote DECISIONS-GATING.md |
| 15 | 22:53:41 | artifact | wrote FAILURES.md |
| 16 | 22:53:41 | artifact | wrote FAILURES-findings-2.md |
| 17 | 22:53:41 | artifact | wrote FAILURES-findings-3.md |
| 18 | 22:53:41 | artifact | wrote STATE.md |
| 19 | 22:53:41 | artifact | wrote STATE-history.md |
| 20 | 22:53:41 | artifact | wrote ROADMAP.md |
| 21 | 22:53:42 | artifact | wrote docs/operations/ci.md |
| 22 | 22:53:42 | artifact | wrote docs/process/multi-vm-coordination.md |
| 23 | 22:53:42 | artifact | wrote docs/process/session-protocol.md |
| 24 | 22:53:42 | artifact | wrote docs/reference/cli-reference.md |
| 25 | 22:53:42 | artifact | wrote sessions/README.md |
| 26 | 22:53:42 | artifact | wrote tasks/T-0020-tell-an-in-flight-session-apart-from-an-abandone.md |
| 27 | 22:53:46 | decision | An unfinished session fails CI only when it is provably abandoned: five clauses read off the tree, plus a 12-hour claim lease. A live session's presen |
| 28 | 22:55:33 | command | $ tools/origin task verify T-0020 |
| 29 | 22:56:04 | doc_update | updated DECISIONS-GATING.md |
| 30 | 22:56:04 | doc_update | updated FAILURES.md |
| 31 | 22:56:04 | doc_update | updated ROADMAP.md |
| 32 | 22:56:04 | doc_update | updated STATE.md |
| 33 | 22:56:04 | session_end | T-0020 complete. The strict session gate now separates in-flight from abandoned: five clauses read off the tree plus a 12-hour claim lease (D024), so  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-037-t-0020-tell-an-in-flight-session-apart-f/events.jsonl
```
