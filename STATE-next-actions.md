<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# Next actions

Actions ranked by information gain per unit effort, with the honest ceiling on each.
When a document passes 250 lines, it is split by section into siblings;
see `STATE-next-actions-2.md` for the split content.

This file tracks the single most useful next action across experiments.
Each experiment section records what was tested, the result, and the named
next action. When a candidate fails, the reason is preserved and the
investigation narrows or moves on.

| Experiment | Status | Named next action |
|---|---|---|
| E197 | completed | the recipient read (`spending_by_category/recipient/`) names who is paid |
| E199 | completed | candidate screen on the money axis: which PSC code admits a small program? (7030 best, DA01 close alternative) |
| E200 | completed | prototype validation of 7030 screen: test if 7030 admits small programs at award level (supported) |
| E201 | completed | MVP prototype for small-team software sales into 7030 federal marketplace; screen validated: 3,916 recipients, 38.4% top-10 share, 32.1% ≤ $40k, 46.8% ≤ $100k, 100% single-award recipients |
| E202 | completed | CLI tool for PSC code small-team entry analysis; outputs recipient count, top-10 share, small-award fractions, single-award fraction, screen score for any PSC code |
| **E203** | **planned** | **award description categorization for 7030: classify individual awards as software/service/other via `spending_by_award/` endpoint to confirm software-market fit** |
| **E204** | **planned** | **time-window analysis: compare last 12 months vs. FY2020–FY2025 to detect market trends and new entrant velocity** |
| **E205** | **planned** | **agency distribution analysis: which agencies buy in 7030, and do small vendors win direct or only subcontract?** |
| E224 | completed | explore fresh observation in a different domain per project direction; view-count principle validated on PyPI with matched-harvest design (E227) |
| E225 | completed | award-description-term generalizability: code-specific term patterns domain-dependent (IT/software only); funded-fraction effects more generalizable |
| E226 | completed | USAspending keyword disambiguation prototype: relatedness score thresholds mechanically validated (7 keywords, G1-G4 all pass); next: field-test with human users (E227) |

<center>...</center>