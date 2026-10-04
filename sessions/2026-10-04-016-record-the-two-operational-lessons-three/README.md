# Session 2026-10-04-016-record-the-two-operational-lessons-three

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T06:00:00+00:00
- **Duration:** 311.9s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Record the two operational lessons three sessions in a row have cost: declare every changed file, and a taskless session reddens the commit it publishes

## Summary

Recorded the two operational lessons three consecutive sessions cost: declare every changed file rather than only the interesting ones, because session finish reports the rest and a closed stream accepts nothing (012 closed with 24 such events, 015 with 4); and a red session step is expected when a session with no task and no claim is open, which is twice in an hour on 2026-10-04 (37174316639, 37181374433) and each green on the next commit. Both are now where the next agent reads them, and the second is recognised from the run alone. No code changed; 400 tests green and doc lint and release check exit 0.

## Next

Open in STATE-next-actions.md and unclaimed: rule 7 does not read STATE-defects.md's numbering, a red CI run names a step rather than a test, and a taskless session publishes commits that redden its own branch until the session commit lands.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| docs/process/session-protocol.md | 5f97f2036d1a | 9545 |
| docs/operations/ci.md | efe87974dd7c | 15329 |
| STATE-next-actions.md | fd35475bf57b | 7970 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 5 | ['bash', '-c', 'tools/origin doc lint >/dev/null 2>&1; echo "lint=$?"; tools/origin release check >/dev/null 2>&1; echo "release=$?"; PYTHONPATH=tools | 0 | 236596 |

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
| 1 | 06:00:00 | session_start | Record the two operational lessons three sessions in a row have cost: declare every changed file, and a taskless session reddens the commit it publish |
| 2 | 06:00:49 | artifact | wrote docs/process/session-protocol.md |
| 3 | 06:00:50 | artifact | wrote docs/operations/ci.md |
| 4 | 06:00:50 | artifact | wrote STATE-next-actions.md |
| 5 | 06:04:51 | command | $ bash -c tools/origin doc lint >/dev/null 2>&1; echo "lint=$?"; tools/origin release check >/dev/null 2>&1; echo "release=$?"; PYTHONPATH=too |
| 6 | 06:05:12 | session_end | Recorded the two operational lessons three consecutive sessions cost: declare every changed file rather than only the interesting ones, because sessio |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-016-record-the-two-operational-lessons-three/events.jsonl
```
