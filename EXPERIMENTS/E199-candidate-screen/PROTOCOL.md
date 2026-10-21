<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E199 PROTOCOL — candidate screen on the money axis

**Purpose:** Test which of the five IT/software PSC codes (DA01, DA10, 7A21, 7030, D304) admits a program a small team could build and sell, by analyzing vendor concentration and entry barriers from the USAspending API.

**Screen criteria (from E199 RESULT):**
- `recipient_count`: number of distinct recipient companies (more = more entry points)
- `top10_share`: fraction of code's obligation held by top 10 recipients (lower = less concentration = easier entry)
- Score = `recipient_count × (1 − top10_share)`: higher = better fit for small team

**Experiment scope:**
- Draw from the 5 IT/software PSC codes previously analyzed in E198
- Use the `spending_by_category/recipient/` endpoint with `psc_codes` filter and `spending_level: awards`
- Analyze per-code recipient lists for concentration and volume

**Kill gate:** N/A — this is a screen/ranking experiment, not a gate-validated experiment. The screen's purpose is to prioritize which code to test further.

**Data analysis:**
- Per-code: recipient count, top-10 amount share, recipient-award count distribution
- Ranking by score = recipient_count × (1 − top10_share)
- Top-ranked code recommended for further prototype validation