# Session 2026-10-16-003-record-the-e168-addendum-checks-link-out

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-16
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-16T03:47:53+00:00
- **Duration:** 6.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Record the E168 addendum checks (link-out count, retrieval handles) and the web-search unavailability

## Summary

Two post-landing checks narrowed E168's own claim. 20 of 24 threads link out (github.com in 15), so the incumbent mechanism is issue-tracker search, which the no-retrieval attempt arm does not test -- G2 measures unaided parametric memory, not performance against the strongest alternative. Of the 13 top answers the unaided arm failed: 8 carry a URL, 5 a config key, only 2 a version token. The search arm's ceiling is unmeasured because web search returned 'Web search cancelled' on every attempt from this VM. STATE.md compressed 294 -> 241 lines and a stale 'works on 5 domains' claim that D105 had already made false is corrected. doc lint OK.

## Next

Run E168 G3 with the search arm from a host that has web search: take each post's exact error string, query it, and check whether the linked source surfaces. That bounds the third arm's ceiling with no assistant in the loop. If the search arm matches the grounded arm, the version-pinned class is real, large and served, and this is the thirteenth service closure with a sharper reason than the other twelve.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/168-version-pinned-need/RESULT.md | 3ec3059a0eaf | 12970 |
| STATE.md | 3f7b27da5b7c | 17987 |
| STATE-next-actions.md | 4235464a13f1 | 16156 |

## Commands

0 captured, 0 non-zero exit.

_none_

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
| 1 | 03:47:53 | session_start | Record the E168 addendum checks (link-out count, retrieval handles) and the web-search unavailability |
| 2 | 03:47:55 | artifact | wrote EXPERIMENTS/168-version-pinned-need/RESULT.md |
| 3 | 03:47:57 | artifact | wrote STATE.md |
| 4 | 03:47:57 | artifact | wrote STATE-next-actions.md |
| 5 | 03:47:59 | session_end | Two post-landing checks narrowed E168's own claim. 20 of 24 threads link out (github.com in 15), so the incumbent mechanism is issue-tracker search, w |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-16-003-record-the-e168-addendum-checks-link-out/events.jsonl
```
