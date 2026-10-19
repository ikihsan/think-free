<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E193 RESULT — the price-bearing sources reachable from this host

**Date:** 2026-10-19. **Outcome: panel 1 G1 FAIL and G2 FAIL; panel 2 G2-panel
PASS. The marketplaces are hard-blocked and the app store is reachable.**

Protocol [`PROTOCOL.md`](PROTOCOL.md), correction
[`AMENDMENT-1.md`](AMENDMENT-1.md). Panels: `probe.py` (1), `probe2.py` (2).
Raw: [`raw/probe.json`](raw/probe.json), [`raw/probe2.json`](raw/probe2.json).

## 1. Panel 1 — every marketplace refused

| source | status | what came back |
|---|---|---|
| Stack Exchange API | **200** | valid results (control PASS) |
| GitHub REST | 200 | `{"total_count":0,…}`, 55 bytes — valid, mis-scored (D1) |
| OpenAlex | **200** | valid results (control PASS) |
| DuckDuckGo HTML | 202 | anomaly-detection page — **no general web search** (F130 reconfirmed) |
| Reddit `/r/knitting/search.json` | 403 | bot-protection page, 190 KB of it |
| Etsy search | 403 | captcha-delivery URL |
| eBay search | 403 | block page |
| Open Collective | 400 | my query was invalid (D2) |
| US Census CBP | 200 | HTML page titled **`Missing Key`** — a soft refusal at 8,531 bytes |
| data.gov CKAN | 404 | endpoint moved (D2) |

**G1 FAIL (2 of 4 controls) → every demand row is `not_evaluated` under the
declared protocol. G2 FAIL.** The axis as declared — *does a paid-demand
marketplace answer from this host* — is closed as **no**.

Two rows are the probe's own fault, not the sources': an invalid GraphQL field
and a moved endpoint (D2). Neither is a claim about reachability.

## 2. Two defects in the probe's own instrument (D1)

A body-length rule cannot classify a response. It called GitHub's valid
55-byte zero-result response a `refusal`, **and** called Census's
`Missing Key` HTML page a `capture`. *A 200 whose body is a challenge page is a
refusal* is the E028 rule; a byte count implements it in both directions at
once. Corrected in panel 2 to: parse JSON for JSON endpoints, require a declared
content marker for HTML ones, and treat a refusal marker in any 2xx body as a
refusal regardless of length.

## 3. Panel 2 — an extension, not a re-run

Panel 1's failure stands. Panel 2 asked whether money-bearing sources that are
*not* marketplaces answer at all: **iTunes Search API 200 / 50 KB (capture)**,
**UN Comtrade 200 (capture)**, Google Books **429**, Open Collective **400**
again (`stats` fields wrong).

**G2-panel2 PASS (2 of 4).** So the money axis exists on this host in exactly
one place today: the app store, where a listing carries a price and a rating
count. E194 uses it.

## 4. What this decides

**It is a constraint on candidate selection, and it explains the record's shape.**
Every one of the 187 earlier experiments harvested a source this host could
reach — Stack Exchange, GitHub, registries, arXiv — because those were the
reachable ones. The sources that carry **price** were unreachable the whole
time. "Unserved need" was therefore measured, over and over, with instruments
that cannot see money. This is recorded as a limitation of the instrument set,
not as a defect in those experiments, each of which remains valid on its own
population.

The stronger money sources still reachable are **spend**, not **price**: US
federal contract amounts (USAspending) and international trade values
(Comtrade, confirmed `200` here). Neither has been used in this record.

## 5. Artifacts

- `PROTOCOL.md`, `AMENDMENT-1.md` — declared before each panel
- `probe.py`, `probe2.py` — one request per source, no retries
- `raw/probe.json`, `raw/probe2.json` — status, content type, bytes, sha256, excerpt