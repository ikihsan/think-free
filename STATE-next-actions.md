<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
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
| E203 | completed | award description categorization for 5 PSC codes: 7030 (64.5% software, 41.4% ≤ $40k), DA10 (57.8%, 49.9%), 7A21 (71.8%, 41.6%), DA01 (12.8%), D304 (8.1%) — 7030/DA10/7A21 are software markets; DA01/D304 are not |
| E204 | completed | time-window analysis: 7030 concentrating fast (top-10 45%→64%, small awards 42%→24%, new entrants 22%→11%); DA10 diversifying (top-10 59%→52%, new entrants 16%→23%); 7A21 hardening (top-10 62%→68%); all show 30-98× obligation growth in recent 12mo |
| E205 | completed | agency distribution: all 3 codes DOD-dominated; DA10 unique VA (19%) + GSA (8%) channels; 7030 broadest civilian base; "small-biz-like" recipients are mid-size resellers (Carahsoft, DLT, Dell), not genuine small vendors; DA10 has best award accessibility (49.5% ≤ $40k, median $40,867) |
| **E206** | **completed** | **integrated CLI tool built and validated on all 5 PSC codes (7030, DA10, 7A21, DA01, D304) with all 5 modules. All screen metrics reproduce E199/E200 baselines within 0.1 pp. COMPARISON_REPORT.md created with full analysis. 7030 best overall (score 2411, 32.1% ≤$40k, 65% software, broad civilian base); DA10 strongest GWAC pathway (28% GSA MAS small vendor share, GSA Schedule channel, 8.1% sub/prime); 7A21 high concentration (Carahsoft 27%); DA01/D304 not software markets** |
| **E207** | **completed** | **contract vehicle analysis completed for all 5 PSC codes: DA10 only code with meaningful GWAC usage by small vendors (28.2% via GSA MAS + SEWP); 7030 small vendors sell direct (88.7%); 7A21 Army/Navy dominated; DA01/D304 not software markets. Next: field test with real companies (E208)** |
| **E209** | **completed** | **subcontract analysis: 7030/D304 negligible (0.1%), DA10 significant (8.1%), DA01 highest (11%) but services labor, 7A21 moderate (2.8%). Confirms 7030 is direct-sales market; DA10 has prime+sub pathways** |
| **E210** | **completed** | **GSA MAS SIN / SEWP category analysis for all 5 codes: DA10 only code with meaningful small vendor GSA MAS share (28% in 511210/511210S/518210C, 66% in 54151S); 7030/7A21 show 4-6% in software SINs; SEWP Cat B <6% all codes. DA10 is premier vehicle for small software vendors. Integrated into E206 CLI as `--module vehicle_sin`. Next: GSA eLibrary cross-ref validation, prime-specific subaward trace** |
| **E208** | **planned** | **field test: recruit 3-5 small software companies to validate the assessment framework against real pipeline opportunities** |
| **E206 full validation** | **completed** | **comprehensive comparison of all 5 PSC codes complete: 7030 best for direct sales, DA10 best for GWAC pathway, 7A21 concentrated, DA01/D304 not software markets. Next: E208 field test (requires authorization); prime-specific subaward trace via /api/v2/subawards/ for Carahsoft/Dell/Leidos/Accenture/GDIT in 7030/DA10; GSA eLibrary cross-ref for SIN validation; SEWP catalog deep dive** |
| E224 | completed | explore fresh observation in a different domain per project direction; view-count principle validated on PyPI with matched-harvest design (E227) |
| E225 | completed | award-description-term generalizability: code-specific term patterns domain-dependent (IT/software only); funded-fraction effects more generalizable |
| E226 | completed | USAspending keyword disambiguation prototype: relatedness score thresholds mechanically validated (7 keywords, G1-G4 all pass); next: field-test with human users (E227) |

<center>...</center>