<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E041 — AMENDMENT-4: a 403 from this API is the rate limit, and my correction
## to AMENDMENT-1's retry rule caused the failure it was meant to prevent

**Written after the run was stopped and before it was restarted.** No similarity
between two rows has been computed at any point in this experiment.

## What happened

`AMENDMENT-1`'s correction declared **403 non-retryable**, on the evidence of
`tiangolo/typer` returning 422 — a renamed repository. It then listed 403 in the
same fatal set on no evidence at all.

On restart the capture hit GitHub's unauthenticated search limit — **10 requests
per minute**, confirmed by reading the response headers rather than by guessing:

```
HTTP/1.1 403
{"message":"API rate limit exceeded for 140.245.241.183. ..."}
X-RateLimit-Limit: 10   X-RateLimit-Remaining: 0   X-RateLimit-Reset: 1791303915
```

**Every one of those 403s was the rate limit, and the run treated them as fatal.**
Four repositories were recorded as `{"error": "HTTPError 403"}` and skipped
permanently: `douglasjarquin`'s neighbour `pl0n3r/brvtal`,
`buchochelliq-labs/rs-rich-cli`, `unvde/CP3407-Assessment`, and by-name
`pytest-dev/pytest`, `vuejs/vue`, `d3/d3`, `tiangolo/typer`.

**So the correction was not neutral: it converted a transient condition into four
missing repositories**, and it did so silently, because a skipped repository
looks identical to a repository that legitimately returned nothing. Three of the
six were *screened* repositories — the ones the gates are read on.

## What is corrected

**403 is classified by its headers, not by its status code.**

- 403 with `X-RateLimit-Remaining: 0` → **rate limit**: sleep until
  `X-RateLimit-Reset` and retry.
- Any other 403 → fatal, recorded, skipped.
- 401 and 422 → fatal. **422 is the renamed-repository case and remains the
  evidence the original correction was reaching for; 403 was never evidence of
  anything.**

Pacing is now read from `X-RateLimit-Remaining` on **every** response rather than
assumed from a constant interval, so the run slows before it is refused instead
of after.

**Two supporting fixes, both consequences of the same diagnosis.**

1. **A repository recorded with an error is retried, not skipped.** The resume
   set is now `{reconciled: True}` rather than "any entry present". A previous
   run's error entries would otherwise have cemented the loss permanently.
2. **Date ranges are split recursively rather than queried year by year.** A
   year-per-query split spends a request on every empty year; a repository whose
   history spans fifteen years cost nineteen requests for a fraction of the rows.
   Ranges whose `total_count` exceeds the index's 1000-hit paging ceiling are now
   halved and requeued, so the request count follows the data instead of the
   calendar.

## What this amendment does not decide

- It does not relax the reconciliation requirement. A repository that still fails
  to match the API's `total_count` is reported unreconciled and **excluded**, and
  the exclusion is visible in `capture_log.json` rather than absorbed.
- It does not substitute for the missing repositories: **`pmxt-dev/pmxt`,
  `pl0n3r/brvtal`, `buchochelliq-labs/rs-rich-cli` and
  `unvde/CP3407-Assessment` were identified by the screening rule and are owed a
  capture.** If the restarted run cannot reach them, that is a shortage of pairs
  and it is reported as one, not as a smaller arm presented as the declared one.
- **The lesson is the transferable part and it is the eleventh instance of this
  record's most repeated shape.** F055, F058 and F059 are all "a fact about the
  instrument's own selection, read after the measurement rather than before".
  This one is the same shape one level down: **a fact about the instrument's own
  *error handling*, read by treating one status code as one condition.** A 403 is
  not a condition; it is a code that a dozen conditions arrive under. The
  generalisation is that an instrument's failure modes must be enumerated from
  its responses, not from its status vocabulary.
