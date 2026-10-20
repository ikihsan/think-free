<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E193 AMENDMENT 1 — two instrument defects in the probe, and a second panel

**Declared:** 2026-10-19, after panel 1 ran and before panel 2 was sent.
**Bars are unchanged.** Nothing in this amendment moves G1 or G2.

## 1. Panel 1 stands as declared

`tools/x -- python3 EXPERIMENTS/193-source-capability-probe/probe.py` returned
**G1 FAIL** (2 of 4 controls captured) and **G2 FAIL** (1 of 6 demand rows
captured). That is the declared result of the declared panel and **it is not
overturned here**.

## 2. Two defects in the probe's own instrument

**D1 — a length rule cannot tell a small valid response from a refusal.**
GitHub returned `200` with `{"total_count":0,"incomplete_results":false,"items":[]}`,
a well-formed, valid API response that happens to be 55 bytes. The probe's
`nonws_chars >= 200` rule recorded it as `refusal`. The same rule recorded the
**Census response as a capture** when its body is an HTML page titled
`Missing Key` — a soft refusal at 8,531 bytes. *A 200 whose body is a challenge
page is a refusal, not a capture* is the E028 lesson, and a byte-count proxy for
"did we get content" implements it badly in both directions.

**Corrected rule:** a row is a `capture` only if the status is 2xx **and** the
body parses as JSON for a JSON endpoint, **or** the body contains a declared
content marker for an HTML endpoint (the endpoint's own product name). A 2xx
body containing a refusal marker (`Missing Key`, captcha, `challenge`) is a
`refusal` regardless of length. Both markers are listed in the script.

**D2 — two rows tested the probe's URL construction, not the source.**
`allCategories` is not a field on Open Collective's `Query` type (`400`,
`GRAPHQL_VALIDATION_FAILED`); `catalog.data.gov/api/3/action/package_search`
returns `404 Not Found`. A `4xx` from a malformed request is evidence about the
request, not the source.

## 3. Panel 2 — an extension, not a re-run

Panel 1's answer is *"the paid-demand marketplaces this host can reach are
blocked"*: Etsy `403` with a captcha-delivery URL, eBay `403`, Reddit `403`
behind a Cloudflare-style challenge page, DuckDuckGo `202` anomaly page,
Census requiring a key. **That is a real constraint and it is recorded as the
finding.**

Panel 2 asks a different question: **are there money-bearing sources reachable
that are not marketplaces?** Four rows are added, with the same roles, and the
same bars applied to panel 2 as a panel of its own:

| # | Source | Role | Endpoint |
|---|---|---|---|
| 11 | iTunes Search API | demand | `itunes.apple.com/search?entity=software` — paid apps, real prices, real review counts |
| 12 | Google Books API | demand | `www.googleapis.com/books/v1/volumes` — `listPrice` where the publisher sets one |
| 13 | UN Comtrade | demand | trade values for a product keyword, official statistics, no key |
| 14 | Open Collective (corrected query) | demand | `api.opencollective.com/graphql`, `totalTransactions` |

**A panel-2 pass does not overturn panel 1's failure.** The axis is declared as
*"marketplaces unreachable"*, and panel 2 can only add *"app-store and
official-statistics demand signals are reachable"*.

## 4. What panel 2 decides

If **≥2 of 4** panel-2 rows capture, the demand axis exists here, and the next
action is a declared harvest that measures **price and competition for a named
practical difficulty** — the first money-per-problem measurement in this
record. If it does not, the money axis is closed as unreachable from this host,
and the axis is retired with the failing statuses attached.

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/193-source-capability-probe/probe.py       # panel 1, unchanged
tools/x -- python3 EXPERIMENTS/193-source-capability-probe/probe2.py      # panel 2
```