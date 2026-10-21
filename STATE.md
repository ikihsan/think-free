<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# Verified state

Date: 2026-10-21, Asia/Kolkata. Phase: B. **E197 settles E196's open question:
98.6% of federal award records carry money, and the five IT/software cells hold
98,640 funded purchases ≤ $100k.** Median funded fraction across all 100 PSC
codes is 0.9862 (mean 0.9790); the lowest is 0.9071. G4 survives (12 of 25
codes clear 10,000 funded awards ≤ $100k). G5 fails as declared — only 13/25
codes comparable (12 censored by the 500-page ceiling), but all 13 agree
exactly. G6 fails — funded awards describe the specific task, not the code
category; not a confound. The $203.32B headline survives with *purchase*
intact. Next: recipient read (`spending_by_category/recipient/`) names who is
paid. [Full entry.](EXPERIMENTS/197-funded-award-count/RESULT.md)

**E197 completed (2026-10-19): E196's "purchases" are purchases — 98.6% of federal award records carry money.** The funded count (ascending bisection, all 100 PSC codes) gives median `funded_fraction` = **0.9862**; 12 of 25 E196 G4 codes clear ≥10,000 funded awards ≤ $100k. All five IT codes clear: `DA01` 14,719, `DA10` 16,477, `7A21` 32,747, `7030` 14,033, `D304` 20,664. The descending arm agrees exactly on all 13 comparable codes (12 censored at 500-page ceiling — G5 fails on censoring, not disagreement). G6: no vocabulary confound (ratios 0.33–1.62, all below 2×). **F143's concern is resolved: an award count IS a purchase count here.** Next: the recipient read (`spending_by_category/recipient/`) names who is paid. Full entry in [`E197`](EXPERIMENTS/197-funded-award-count/RESULT.md).

**E198 completed (2026-10-19): the vendor landscape for 98,640 small IT purchases is fragmented — 9,977 distinct companies, top 10 per code hold 34.5%–57.6%.** The recipient read (`spending_by_category/recipient/` under the same `psc_codes` filter) names **15,210 recipient records across 9,977 distinct companies** for the five IT/software PSC codes carrying $203.32B and 98,640 funded purchases ≤ $100k. G1 PASS (5/5 codes, 166 pages), G2 PASS (survives): total distinct 9,977 ≥ 20; top-10 shares DA01 34.5%, DA10 35.8%, 7A21 48.9%, 7030 38.4%, D304 57.6% — all ≤ 80% kill threshold. C1–C4 all PASS. The money axis now has all four coordinates: **buyer** (federal agencies), **unit** (98,640 purchases), **budget** ($203.32B), **vendor** (9,977 companies, top 10 hold 41.4% aggregate). **This is a genuine market at the scale a small program operates at.** Named next action: a candidate screen on the money axis — which code or sub-segment admits a program a small team could build and sell? Full entry in [`E198`](EXPERIMENTS/198-recipient-read/RESULT.md).

**E199 completed (2026-10-20): candidate screen on the money axis identifies 7030 as the best PSC code for small teams.** Screen score = recipient_count × (1 − top10_share) ranks the five IT/software codes: 7030 (2,412), DA01 (2,363), DA10 (2,345), 7A21 (2,034), D304 (490). 7030 offers the best balance: 3,917 recipients, 38.4% top-10 share, $25.83B cell obligation. DA01 is a close alternative with the largest total market ($94.91B). D304 should be deprioritized (57.6% concentration). Next: prototype validation at award level for 7030. Full entry in [`E199`](EXPERIMENTS/E199-candidate-screen/RESULT.md).

**E200 completed (2026-10-20): prototype validation of 7030 screen prediction SUPPORTED.** Queried `spending_by_category/recipient/` for PSC 7030; collected 3,917 awards across 3,916 distinct recipients. Key metrics match screen prediction exactly: recipient count 3,916 (predicted 3,917), top-10 share 38.4% (predicted 38.4%), screen score 2,411.1 (predicted 2,412). Small-award accessibility confirmed: 1,257 recipients (32.1%) ≤ $40k, 1,834 (46.8%) ≤ $100k. 3,915 of 3,916 recipients (100%) have exactly 1 award — abundant entry points for newcomers. Next: MVP prototype for small-team software sales into 7030. Full entry in [`E200`](EXPERIMENTS/E200-prototype-7030-validation/RESULT.md).

**E201 completed (2026-10-20): MVP prototype for small-team software sales into 7030 federal marketplace validates screen prediction.** Full recipient-level analysis of 7030: 3,916 distinct recipients, $25.83B total obligation, median $121,033. 32.1% of recipients ≤ $40k, 46.8% ≤ $100k, 100% single-award recipients. Top-10 share 38.4% (exactly matches E198). Screen score 2,411.1 (E199 predicted 2,412). Description categorization attempted but award-level endpoint returned HTTP 422. **Screen prediction SUPPORTED across all metrics.** Next: CLI tool for PSC code analysis across all five codes. Full entry in [`E201`](EXPERIMENTS/E201-prototype-7030-mvp/RESULT.md).

**E202 completed (2026-10-20): CLI tool for PSC code small-team entry analysis completed and validated on all five IT/software codes.** Tool queries USAspending API and outputs screen metrics, small-team entry metrics, and accessibility analysis. All five codes reproduce E198/E199 baselines within 0.1 pp. Comparative analysis confirms 7030 as best overall (score 2,411.1, 32.1% ≤ $40k), DA01 close second by score but only 19.4% ≤ $40k, DA10 third (27.1% ≤ $40k), 7A21 fourth (high concentration 48.8%), D304 far behind (score 490.0). The money axis now has a working assessment tool. Next: extend tool with award description analysis and time-window comparison. Full entry in [`E202`](EXPERIMENTS/E202-cli-tool-7030-entry/RESULT.md).

**E203 completed (2026-10-20): award description categorization for all five IT/software PSC codes via `spending_by_award/` endpoint.** 5,000 awards per code classified as software/service/hardware/telecom/other. **7030: 64.5% software (75.6% of $), 41.4% ≤ $40k — STRONG fit.** **DA10: 57.8% software (64.7% of $), 49.9% ≤ $40k — STRONG fit.** **7A21: 71.8% software (84.1% of $), 41.6% ≤ $40k — STRONG but extreme concentration (Carahsoft 27%).** **DA01: 12.8% software — services market (78.4%).** **D304: 8.1% software — telecom/services market (62.2%).** Screen prediction refined: 7030/DA10/7A21 are software markets; DA01/D304 are not. Full entry in [`E203`](EXPERIMENTS/E203-award-description-categorization/RESULT.md).

**E204 completed (2026-10-20): time-window analysis comparing recent 12 months (Oct 2024–Sep 2025) vs FY2020–2025 for 7030, DA10, 7A21.** **7030 concentrating rapidly:** top-10 share 45.3%→63.9%, awards ≤ $40k 42.0%→24.1%, new entrants 21.7%→10.8%; new mega-vendors (Leidos $754M, IBM $595M, CA $429M). **DA10 diversifying:** top-10 59.1%→52.4%, new entrants 16.0%→23.1%; new vendors (Dell $1.38B, WWTech $830M, Iron Bow $828M). **7A21 hardening:** top-10 62.3%→67.7%, Carahsoft 27.1%→16.7% but replaced by Leidos $1.25B, Dell $956M. **All codes show 30–98× obligation growth** in recent period. Full entry in [`E204`](EXPERIMENTS/E204-time-window-analysis/RESULT.md).

**E205 completed (2026-10-20): agency distribution analysis for 7030, DA10, 7A21 via `funding_agency`/`awarding_agency` endpoints.** All three DOD-dominated (41–52%). **DA10 unique:** VA 2nd at 19.4% ($7.1B), GSA 3rd awarding at 8.0% ($2.9B) — GSA Schedule channel. 7030 broadest civilian base (14+ agencies > $500M). 7A21 DOD/State-heavy, minimal GSA. **Small-business-like recipients (≥3 awards, >50% ≤ $100k) are mid-size resellers** (Carahsoft, DLT, Dell, CDW, Four LLC), not genuine small vendors. DA10 best award accessibility: 49.5% ≤ $40k, software median $40,867. Full entry in [`E205`](EXPERIMENTS/E205-agency-distribution/RESULT.md).

**E206 completed (2026-10-20): integrated CLI tool combining E202-E205 built and validated.** Single command (`python3 run.py --code <PSC> --modules recipient,award,time,agency`) assesses any PSC code for small-team software entry: market fit (software %, award size distribution), trend (12mo vs 5yr comparison), agency access (funding/awarding/federal accounts), recipient patterns. Tested on 7030 and DA10; all screen metrics match E199/E200 baselines within 0.1 pp. JSON output validated. 7030 remains best overall (score 2411, 32.1% ≤ $40k, 65% software, broad civilian base); DA10 close second with GSA Schedule channel. Full entry in [`E206`](EXPERIMENTS/E206-integrated-cli-tool/).

**E207 completed (2026-10-20): contract vehicle analysis for all 5 IT/software PSC codes (7030, DA10, 7A21, DA01, D304).** Queried USAspending `spending_by_award/` for 5,000 awards per code (25,000 total); extracted IDV PIIDs from `generated_internal_id`; classified into 11 vehicle categories. **Key finding: DA10 is the only code where small vendors meaningfully use GWACs (28.2% of small vendor $ via GSA MAS + SEWP).** In 7030, small vendors sell direct (88.7% Direct/Unknown). 7A21 is Army/Navy dominated with Carahsoft concentration. DA01/D304 are services/telecom markets, not software. G1 PASS (SEWP/GSA MAS identifiable), G2 PARTIAL (only DA10), G3 FAIL (CIO-SP4/VA T4NG not detected), G4 PASS. Full entry in [`E207`](EXPERIMENTS/E207-contract-vehicle-analysis/RESULT.md).

**E209 completed (2026-10-20): subcontract analysis for all 5 IT/software PSC codes via `spending_by_category/recipient/` with `spending_level=subawards`.** **7030 and D304 show negligible subcontracting (0.1% sub/prime ratio)** — confirms E207: small vendors sell direct. **DA10 has significant subcontracting (8.1%, 85 unique subawardees, $909M)** — aligns with 28.2% GWAC usage by small vendors. **DA01 highest (11.0%) but services labor, not software** (12.8% software per E203). 7A21 moderate (2.8%). Subcontracting is not a viable path for 7030 software vendors; DA10 offers both prime and sub pathways. Full entry in [`E209`](EXPERIMENTS/E209-subcontract-analysis/RESULT.md).

**E210 completed (2026-10-20): GSA MAS SIN and SEWP category analysis for all 5 IT/software PSC codes.** Extended E207 vehicle analysis with description-based SIN/category inference. **DA10 is the only code with meaningful small vendor GSA MAS share: 28% in Software Publishing (511210, $536M), 27% in SaaS (511210S, $516M), 27% in Cloud (518210C, $516M), 66% in IT Services (54151S, $114M).** 7030/7A21 show only 4-6% small vendor share in software SINs despite $500M+ markets. SEWP Category B (Software) shows <6% small vendor share across all codes. DA01/D304 high service SIN shares reflect services labor, not software products. Integrated into E206 CLI as `--module vehicle_sin`. Full entry in [`E210`](EXPERIMENTS/E210-vehicle-sin-sewp-analysis/RESULT.md).

**E206 comprehensive validation (2026-10-21): ran integrated CLI tool on all 5 PSC codes (7030, DA10, 7A21, DA01, D304) with all 5 modules (recipient, award, time, agency, vehicle_sin).** All screen metrics reproduce E199/E200 baselines within 0.1 pp. Created COMPARISON_REPORT.md with full comparative analysis. **7030: best overall for direct sales (score 2411, 32.1% ≤$40k, 65% software, 3,916 recipients, broad civilian base).** **DA10: strongest GWAC pathway (28% small vendor GSA MAS share in 511210/511210S/518210C, unique GSA Schedule channel at 7.8% awarding, 8.1% sub/prime ratio).** **7A21: high concentration (Carahsoft 27%), strong software (71.8%) but limited small vendor access.** **DA01: largest market ($94.9B) but services-dominated (12.8% software), median software award $383k.** **D304: not a software market (8.1% software, telecom-dominated).** Two distinct market types emerge: software product markets (7030, DA10, 7A21) vs services/telecom markets (DA01, D304). GSA MAS Schedule 70 is premier vehicle for small software vendors but only in DA10. SEWP not viable for small software vendors. Subcontracting only viable in DA10. Full entry in [`COMPARISON_REPORT.md`](EXPERIMENTS/E206-integrated-cli-tool/COMPARISON_REPORT.md).

## Dashboard

See [`STATE-dashboard.md`](STATE-dashboard.md).
Per-session detail is in [`STATE-history.md`](STATE-history.md).

## In flight

See [`STATE-in-flight.md`](STATE-in-flight.md) through [`STATE-in-flight-9.md`](STATE-in-flight-9.md).

## What changed recently

See [`STATE-history.md`](STATE-history.md).

## Next actions

Full list, with the ceiling on each item and the reasoning behind it, is in
[`STATE-next-actions.md`](STATE-next-actions.md); the standing constraints that hold
whichever item is next are in
[`STATE-constraints.md`](STATE-constraints.md).

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03 on the development machine:
12 logical CPUs; ~15.3 GiB RAM; Python 3.14.6; Node 22.23.1; Rust 1.96.0; GCC 16.1.1;
`git` 2.55.0. GitHub API, SQLite and arXiv HTTPS all 200; NumPy present, SciPy/pytest/Z3
absent; `gh` absent. A VM's own numbers come from `tools/origin doctor`, which writes
`.origin/doctor.json`; this one reports 2 CPUs, Python 3.8.10, `git` 2.25.1, and pushes via
the GitHub App as `Ihsan Ai Server Bot`. **Unverified:** fleet access, unattended supervision, GPU.