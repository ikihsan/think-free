# E014 — Does the strongest recurrent cluster survive a repository-signal filter?

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

**Date:** 2026-10-04. **Verdict: the cluster is real but narrow.** E012's
"strongest measured recurrence" — open issues complaining that coding agents
make changes nobody asked for — collapses roughly two orders of magnitude
once repositories are classified and the issue count is taken only over the
ones that belong to the coding-agent problem area. The earlier reading of
"5805 issues across 28 repositories" as a cross-project problem was an
artifact of full-text counting. See F033.

## The question and the falsification

E012 found four clusters by counting open issues *per repository*, but the
counts were full-text over titles and bodies (D049's ceiling). A repository
in `"not asked for"` results may be a web app built with an agent, a hobby
repo, or a tool for a different problem. **Claim:** the cluster is
cross-project in the coding-agent problem area, i.e., many of the
repositories it spans belong to that area and hold many of the issues.
**Kill gate (declared before classification):** if fewer than half of the
first-page repositories pass the filter, or the filtered issue count is
negligible against the unfiltered one (a 10× or greater collapse on every
query), the cluster is not the cross-project signal E012 believed it was, and
the corpus route needs a different strongest cluster or none.

## Method

| step | script | what it fixes |
|---|---|---|
| re-collect | `collect_repos.py` | E012's probe stored only repository names; this keeps `owner/name` |
| classify | `scrape_classify.py` | each repo's own description and topics, via its public HTML page (the core REST API was exhausted at 60/hr mid-run; the filter terms and verdict rule are unchanged) |
| filter | stated terms: `agent, copilot, claude, llm, coding assistant, ai coding, ai-agent, ai agent, ai assistant, pair-programming, cursor`, matched case-insensitively over `owner/name + description + topics` | a repository passes only if its own metadata says it belongs to the area |
| re-count | `filtered_count.py` | each of the four issue queries, restricted with `repo:` qualifiers to the passing repositories |

## Result

99 unique repositories behind the four first pages; **45 passed** the filter
(29 of the 19-repo copilot page, but many of the agent pages are small
hobby repos). Filtered counts:

| query | unfiltered | passing repos | filtered issues |
|---|---|---|---|
| `"not asked for"` | 5813 | 9 | 15 |
| `"unrelated changes"` | 14513 | 9 | 28 |
| `"scope creep" agent` | 2235 | 19 | 76 |
| `"unrelated file" copilot` | 412 | 9 | 33 |

Every query collapsed by more than 100×. The cross-project claim fails its
own gate. What survives is a complaint concentrated *inside* a dozen or so
coding-agent project trackers — `anthropics/claude-code`,
`github/copilot-cli`, `MervinPraison/PraisonAI`, `Paige-Agent-AI/Agent` —
which is a statement about those tools' issue volume, not a practitioner
need shared across projects.

## What this licenses

The corpus stays demoted (E012's verdict stands), and D049's rule now has
its first measured application: recurrence must be counted over
repositories that pass a relevance filter, and almost none of the
unfiltered volume does. The candidate generator remains refuted; no new
candidate was produced, consistent with the record.

## Limits

- The keyword filter is one-directional: failing repos are *unverified*, not
  exonerated (a tool described as "developer productivity" fails, and
  passing names like `AI-waysMeme` are hobby projects). This is F030's
  asymmetry inside the filter itself.
- First-page results only; GitHub's ranking decides which repositories were
  eligible. One terminology probe per cluster, one date (2026-10-04), all
  counts re-runnable from the scripts.
- Core REST API exhaustion mid-run is why classification reads HTML pages;
  a follow-up could re-check a sample against the API once the 60/hr window
  resets, as a verification half.
