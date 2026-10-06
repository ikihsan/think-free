# Venue actually used, and why

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

Declared in [`PROTOCOL.md`](PROTOCOL.md) before any fetch: primary venue is
Stack Exchange's non-programming sites, with Reddit long-form posts as the
substitution and a rule that the substitution may not be made on the basis of
which venue returned more recurrences.

**The primary venue was used. No substitution happened**, so the substitution
rule never had to fire and no choice was made after seeing data.

| | |
|---|---|
| endpoint | `https://api.stackexchange.com/2.3/questions`, unauthenticated |
| sites used | `woodworking`, `outdoors`, `cooking` — the first three of the five declared, in the declared order, each yielding ≥ 20 usable bodies |
| selection rule | **all** questions, `sort=votes`, `creation` 2025-01-01 … 2026-06-16, body 40–600 words, named author. **No requirement vocabulary anywhere in the selection** |
| questions held | 60 (20 per site) |
| distinct authors | 53 |
| body length | min 41 words, median 110, max 530 |
| posted | 2025-01-06 … 2026-06-04 |
| fetches | 6 requests, all HTTP 200, `quota_remaining` 294 at the last one |
| clauses both readers agreed on | 28 — woodworking 16, outdoors 6, cooking 6 |

Raw capture: [`raw/harvest.jsonl`](raw/harvest.jsonl), fetch log
[`raw/fetch_log.jsonl`](raw/fetch_log.jsonl).

## Why this venue and not Hacker News

F053 is the reason. Every population behind F039, F042, F043, F049 and F051 came
from `hn.algolia.com`, so the mission had one venue and five readings of it. A
second venue had to differ on the axes that could plausibly matter:

| | Hacker News (E031) | Stack Exchange (E032) |
|---|---|---|
| unit | a comment inside a story | a self-contained question |
| length | median ~11-word extracted clause, comment short | median 110-word body |
| what it is attached to | an argument about a linked artifact | nothing but itself |
| population | self-selected technical readers | woodworkers, campers, cooks |
| subject | software and developer tooling | woodworking, outdoors, cooking |
| selection | trigger vocabulary about an event | **all** questions in a site and window |

The last row is the load-bearing one and it is a change of method, not only of
population. F043 measured that a trigger vocabulary finds people who state needs
while being blind to what happens to those needs afterwards; had E032 also used a
trigger vocabulary, its population would have carried the same property and a
zero would have been uninterpretable. **E032's population is selected by date,
site and length and by nothing else**, so its zero is not the harvest's fault.