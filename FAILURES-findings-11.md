<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Failures — recorded findings, part 11 (F033)

Source: session `2026-10-04-054`. E012's strongest recurrent cluster,
re-measured through D049's repository-signal filter. Runnable evidence:
`EXPERIMENTS/014-repository-signal-filter/`.

## F033 — Full-text issue counting inflated E012's strongest cluster by two orders of magnitude

### What happened

E012 reported four clusters of open GitHub issues as "5805 issues across 28
repositories", "14510 across 29", and so on, and D049 promoted repository
count over issue count as the recurrence unit. E014 applied D049's missing
half — a filter on whether a repository belongs to the coding-agent problem
area at all — and re-counted.

| query | unfiltered | filtered |
|---|---|---|
| `"not asked for"` | 5813 | 15 |
| `"unrelated changes"` | 14513 | 28 |
| `"scope creep" agent` | 2235 | 76 |
| `"unrelated file" copilot` | 412 | 33 |

54% of first-page repositories passed the keyword filter, yet they hold
under 2% of the issues. The earlier reading — a cross-project practitioner
problem — does not survive. What remains is a complaint inside roughly a
dozen coding-agent project trackers, which is a statement about those
tools' issue volume.

### The lesson

An unfiltered GitHub count is not prevalence; it is a property of the whole
executing web, which talks about everything. D049's two-input rule needs
the filter half as well as the repository denominator, and this measurement
is why. The filter cannot confirm membership either (failing repos are
unverified), so the next corpus claim must use the strict number as a floor
and say so.
