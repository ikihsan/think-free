<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E058 — AMENDMENT-1: the venue changes, the question does not

2026-10-08, session `2026-10-08-006`, before any population row was fetched.

## What happened

`PROTOCOL.md` named **Steam per-game feature requests** as arm 1, because that
route was the only one I could name that is large, public, unauthenticated,
non-software, **and records an outcome per request**. Valve's classic per-game
feature-request boards no longer exist.

The probe is in `raw/steam-probe.json`: three requests, all **HTTP 200**, on the
largest game on the platform (Team Fortress 2, appid 440).

| url | status | bytes | boards found | feature-request board | word "feature" in page |
|---|---|---|---|---|---|
| `steamcommunity.com/app/440/discussions/` | 200 | 76,925 | 4 | **no** | 4 |
| `steamcommunity.com/app/440/discussions/0/` | 200 | 76,941 | 4 | **no** | 4 |
| `steamcommunity.com/games/440/discussions/0/` | 200 | 26,796 | 0 | **no** | 1 |

The four boards that exist are `General Discussions`, `Mann vs. Machine`,
`Looking For Players` and `Virtual Reality`. The word "feature" appears four
times on the page and in none of them names a board.

**G1 therefore fails for this venue and the route is retired.** This is F036's
shape one layer up: a capture that answers **HTTP 200 with a page unrelated to
what was asked for**, and a count of bytes or rows would have read it as a
working route. Had the harvest been written against `/app/440/discussions/0/` it
would have collected general discussion threads and reported them as feature
requests.

## What replaces it, and what does not change

**Arm 1 becomes: never-answered questions on six non-software Stack Exchange
sites**, harvested through the same public API this repository already uses for
E034 and E035, with the same fields (`is_answered`, `accepted_answer_id`,
`closed_reason`, `score`, `tags`, body). Sites: `cooking`, `gardening`,
`bicycles`, `woodworking`, `diy`, `astronomy`.

Why it is the right substitute and not a retreat:

- It is **outside software as a domain**, which is the only thing the question
  needs. The remedy people seek is a technique, a product, a material or a
  source, not a library.
- It carries a **platform-recorded outcome** — answered, accepted answer, or
  closed with a reason — so G4 is measurable here too.
- The route is **already exercised in this repository**, which is the one thing
  E041's failure taught: reuse a route that has produced bytes before, rather
  than a new one that has produced a 200.

**Unchanged: the question, the rubric, the decision it changes, and gates G2, G3,
G4.** G1 is restated for the new venue and nothing else in the protocol moves.

| gate | restated |
|---|---|
| **G1 retrieval** | ≥ 300 rows across ≥ 6 distinct non-software sites, each carrying title, body, tags, score and the outcome fields; the harvest reconciled against each site's own `total_count`, and rows that produced no body are reported as missing observations, never as zeros (D081) |

## Ceiling added by this amendment

The substitute venue is **one platform**, so the domain comparison is
non-software *within a software-shaped platform*: its members are technical
enough to be on Stack Exchange, which the Steam venue would not have imposed.
**That biases the arm toward tool-shaped need**, so a null result here is weaker
evidence against the domain hypothesis than a Steam result would have been, and
the README must say so. The confound cuts in one direction only: it can manufacture
a positive, not a negative.
