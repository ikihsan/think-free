# 011 — adjacent-niche adoption census (E, flat-tail test)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

Extends the F027 sample: F027 measured adoption only inside the
agent-session-auditing niche and could not say whether its flatness is
niche-specific. This census reads the same shape from seven GitHub search
vocabularies on 2026-10-04 (`results.json`, raw output).

- Young vocabularies in the same candidate era — `lockfile drift`
  (top-1 6 stars), `dependency quarantine` (top-1 8 stars) — reproduce the
  F027 flat tail exactly. New-vocabulary candidates in this era are all at
  zero regardless of the problem.
- Established vocabularies — `reproducible builds`, `build provenance`,
  `supply chain audit`, `artifact provenance` — carry a heavy tail (top
  4135, 1050, 772, 1050), but the outliers are long-lived or
  vendor-official (`please` since 2016, Open Build Service since 2011,
  `actions/attest-build-provenance`) or templates. The top of
  `agent session log` is the one 40k-star outlier; everything below it
  is under 400.
- No young project in a young vocabulary shows an adoption outlier.

**Verdict:** the flat tail is a property of vocabulary age, not of this
niche. A candidate-screening criterion measured in stars carries no
information inside any vocabulary younger than a few years, which is where
this mission's candidates have all lived. See F028.

Limits: one snapshot of one endpoint, search-by-name-and-description,
personal proxies; not a benchmark of usefulness.
