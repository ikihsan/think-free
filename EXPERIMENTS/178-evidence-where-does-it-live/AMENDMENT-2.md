<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# AMENDMENT-2 — the default filter has no `comment_count`, and one comment chunk was silently truncated

**Declared:** 2026-10-17, **after the first fetch of this experiment and before
any population row was read**. Both defects were in the movement of bytes, not
in a judgement, and both are in the record rather than repaired quietly.

## Defect 1 — `comment_count` does not exist in either filter this API returns

`fetch.py` asked `questions/{ids}?filter=default` for `comment_count` as G0b's
independent count. The committed response in `raw/se.jsonl` shows what came
back:

```
question keys: answer_count, content_license, creation_date, is_answered,
last_activity_date, last_edit_date, link, owner, question_id, score, tags,
title, view_count
```

**No `comment_count`.** E177's own committed `withbody` question response has
the same field list plus `body`, so `withbody` does not carry it either. The
script turned the absent field into `0` (`it.get("comment_count") or 0`), which
is why **all 98 rows read as zero comments** and why G0b reported 33 mismatches
against the comments endpoint — the cross-check was not disagreeing with the
fetch, it was disagreeing with a field that was never there.

**Consequence, and the repair.** There is no independent per-question comment
count in this API without an application key, so G0b's *count reconciliation*
is withdrawn as a check that cannot be performed. What remains, and is the
check the threat actually needs, is **pagination**: E177 lost 18 of 50 rows to a
`filter` chunk cap and lost another population to the 100-answer cap across a
request (AMENDMENT-2 there), both silently. So G0b becomes:

1. every one of the 46 returns a response, with no error and no backoff;
2. every chunk is paged until `has_more == false`, with each page's `has_more`
   and item count written to `raw/se.jsonl`;
3. **the two chunks that paged are re-fetched at a different `pagesize` and must
   return the same total item count** — a page-size agreement check, which is
   independent of the paging loop in the way a count from the same loop is not.

## Defect 2 — one chunk was truncated at 100 items and reported `has_more: true`

`fetch.py` read one page per chunk and did not page. The second recorded
response is `n_items 100, has_more true` for the chunk starting at 79385315 —
**sixteen ids' comments are under-counted**, and the run printed no warning,
because the truncation was in a field the script did not look at.

**Consequence.** Every M1 number from the first fetch is a **lower bound of
unknown tightness on up to 16 of the 46 rows**, and the control set was chosen
from five questions that the defective field said had no comments.

**The repair** pages to exhaustion and re-fetches the paged chunks at
`pagesize=50`.

## What this amendment does not change

The population, the buckets, the reader instruction, the gates and the kill are
untouched. This is the third byte-level defect in this experiment's first hour
and the second in three sessions, which is the same failure E177 recorded as
defects 1, 2 and 3 and E091 recorded as F114: **a pipeline whose only job was to
move bytes, failing at the byte.** The first fetch's seven requests stay in
`raw/se.jsonl`; nothing is deleted, so the two runs are both auditable.

## Quota

First fetch 7 requests, repair fetch 12, of the 300/day this host is allowed.
`quota_remaining` is in the body on this gateway, not in the headers.