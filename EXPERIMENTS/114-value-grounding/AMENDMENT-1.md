<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# AMENDMENT-1 — population changed from court opinions to Federal Register rules

**Date:** 2026-10-12, before any document was fetched into this experiment.

**What changed.** The population clause of `PROTOCOL.md` named *US federal
court opinions from CourtListener*. It is now *US Federal Register final rules*.

**Why.** The search API returned 20 records unauthenticated and every opinion
carried a `download_url` on `cdn.ca9.uscourts.gov`. Those PDFs are PDF-1.6
with subsetted TrueType fonts and per-font CMaps: 58 Flate streams of which
none is a page-content stream in a stdlib-reachable encoding, and `/Encoding`
is absent, so a character code cannot be mapped to a glyph without parsing each
embedded font program. The opinion endpoint itself returns **401**
unauthenticated and the public HTML page returned **HTTP 200 with a zero-byte
body** — recorded as a refusal, not a capture, per the standing constraint on
empty bodies.

Writing a CMap-resolving PDF text extractor is not the experiment. The
population clause is the only thing changed; the question, the arms, the
instrument, and all four kill gates are untouched.

**Why Federal Register is at least as good a population for this question.**

| property | court opinion | Federal Register final rule |
|---|---|---|
| public, no account | PDF only, needs CMap work | plain text, `raw_text_url` |
| non-software | yes | yes |
| numerically dense | docket/filing dates, dollar amounts, page cites | effective dates, dollar thresholds, CFR sections, comment counts, OMB control numbers, page ranges |
| a wrong value costs something | high | high — these documents *create* binding obligations |
| realistic "read this for me" task | yes | yes |

**Cost of the change, stated:** Federal Register documents are more uniform
than opinions, so a perfect extraction rate here is a weaker claim than it would
have been on opinions. This is noted as a limitation, not resolved.
