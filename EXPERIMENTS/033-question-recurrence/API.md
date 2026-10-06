# E033 — what the Stack Exchange API v2.3 does and does not expose

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

Observed 2026-10-06 from `api.stackexchange.com`, API revision
`2026.5.26.43284`, unauthenticated, `quota_max` **300 requests per IP per day**. Every
claim here has a request in `raw/fetch_log.jsonl` or `raw/resolve_log.jsonl`, or is a
`curl` recorded in this session's command log.

This file exists because the protocol's §7 cross-check could not be run, and the reason
is a property of the API rather than of the code — the kind of thing that costs an hour
if it is only in a session log.

## Available, and used

| what | where |
|---|---|
| `closed_reason` on a question, with the literal value `Duplicate` | `/questions` with any filter that returns it (it is in the default set) |
| `owner.user_id`, `score`, `answer_count`, `is_answered`, `accepted_answer_id`, `creation_date`, `title` | same |
| `body` | `/questions?filter=withbody` |
| up to 100 items per page; **anonymous page cap 25** | `/docs` |

## Not available

| what | observed response |
|---|---|
| `closed_details` — the field that names the **canonical** a duplicate was closed against | rejected: `filter=closed_details` → `400 invalid filter`. `POST /filters/create` returns 392 available fields and `question.closed_details` is **not** among them (only `question.closed_date`, `question.closed_reason`). |
| `question_type` — which marks a row returned by `related` as the duplicate rather than merely related | not a selectable field either; `filters/create` lists no field of that name, and the default filter on `/questions/{id}/related` omits it. |
| **any** vectorised `{ids}` path | `GET /questions/1644,1011?site=stackoverflow` → `400 {"error_id":404,"error_name":"no_method"}`. Same for `POST /posts/1644,1011`. So `questions/{ids}` and `questions/{ids}/comments` cannot batch, and **one canonical costs one request**. |
| the question's own HTML page, for scraping the "already has an answer here" banner | `travel.stackexchange.com/questions/189910` → **HTTP 403** with a 5 KB challenge body |
| StackPrinter rendering of that banner | `stackprinter.appspot.com/export?question=189910&service=travel.stackexchange` → **HTTP 200 with a 1,213-byte "The StackExchange server is too busy at the moment" page**, twice, 5 seconds apart |

## What that costs this experiment

`/questions/{id}/related` **does** return rows (6–10 per edge here) with full owner and
answer metadata, so a canonical is *guessable*. But the top-ranked row is a **related**
question, not necessarily the closure's target, and nothing in the public API says which.

The reader arm was built to check exactly that, and it **failed its gate**: 6 of 24 rows
read `same` by both readers against a declared floor of 30 of 40. So the "edge set" this
protocol hoped to build is not an edge set — it is a set of topical neighbours. Gate A3
failing is the finding, and `tally.py` refuses to print the visibility product that
depends on it rather than printing one anyway.

Two consequences for any future work on this API, both transferable:

1. **A duplicate closure is a reliable label and an unreliable edge.** The rate
   (`closed_reason == "Duplicate"`) is measured over 1000 rows with no missing field. The
   *target* of the closure is not recoverable from the public API by any route found here,
   including two third-party renderers.
2. **Where the canonical is needed and cannot be had, substitute a measurement that does
   not need it.** AMENDMENT-2's D7 is that substitution: the counterfactual draw needs only
   scores and closure reasons, and it answers the same question the visibility product was
   meant to answer.