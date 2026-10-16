<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E170 PROTOCOL AMENDMENT 2 — the web surface and the API are different instruments

**Declared 2026-10-16, after the API arms and both controls ran, before any HTML
query was executed against a row.** No new population and no new arm queries: the
arm queries are the ones committed in `queries.json` before any fetch, and the
two controls are the ones declared in Amendment 1.

## What prompted it

`html_probe.py` ran the quoted literal `"Docker.app will damage your computer"`
against `github.com/search?type=issues`, the surface a developer actually uses,
and got **HTTP 200, one result, and that result is the target**
(`docker/for-mac#7520`, rank 1). The API endpoint, given the same corpus,
reported **2 436** matches for a nonsense phrase and a median of **2 167**
documents for the bare literal.

The two surfaces do not have the same matching semantics:

| | API `search/issues` | web `github.com/search` |
|---|---|---|
| `"quoted phrase"` | quotes not enforced — a phrase is term-AND | honours the phrase: 1 result |
| bare number | parsed as an issue-number qualifier (2 436 hits for nonsense + `9987`) | — |
| `a/b` in the query | parsed as a repository qualifier, `http_422` when it does not exist | — |
| query length | rejected above 256 characters | — |
| rate limit | 10 requests/minute unauthenticated | none observed in 2 requests |

**That difference explains both control failures.** The API arm's "phrase" was
never a phrase: it was three terms ANDed over a corpus of a hundred million
issues, which is why a body-mined phrase matched a median 718 258 documents and
ranked nothing first. G0t passed on the API only because a title is short and
its words are rare. The web surface is the instrument the incumbent mechanism
actually uses, and it is therefore the stronger alternative to measure against.

## G — the arms on the web surface

Per row, on `github.com/search?type=issues`, ranked by document order:

- **G-A0** the developer's quoted error string, global. *The incumbent.*
- **G-A1** the component + symptom keywords, global. *E169's design rule.*
- **G-C1** the Amendment 1 rare-phrase control. *Capability.*
- **G-C2** the `in:title` control. *Capability, replicates G0t on a second surface.*

**Controls must pass on this surface too**, at the same bar: ≥ 10 of 13 for
G-C2 at rank 1. If G-C1 passes here and failed on the API, the API's failure is
established as a phrase-semantics artifact rather than an index property, and the
API's arm rates are explained rather than merely void.

**Primary comparison, declared now:** G-A1 against G-A0, global scope, paired
McNemar exact. **Kill, as before: G-A1 ≤ G-A0.** A non-firing kill at N = 13 is
not evidence of no difference, and is reported as such.

## What this does not do

It does not reopen the class as a product. It measures whether the mechanism
E168 named and E169 proposed reaches the fix on the surface where such a
mechanism would be used, which is the one question both experiments left open.
A pass would make the prior-art screen the next action; a kill closes the line.

Cost: 52 requests, about three minutes. Polite delay between requests, 429
retried with backoff, every response's ordered result list recorded.