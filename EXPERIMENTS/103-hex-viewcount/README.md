<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E103 — View-count principle on Hex.pm (Elixir/Erlang package registry)

## Summary

**ALL GATES PASS** — The view-count principle generalizes strongly to Hex.pm.

| Gate | Result | Details |
|------|--------|---------|
| G1 (sample ≥ 100) | PASS | 200 classified (100 need-related, 100 random) |
| G2 (MWU p<0.05, δ>0.147) | PASS | p≈0.000, Cliff's δ=0.861 |
| G3 (Wilson LB > 0.60) | PASS | LB=0.946 (99/100 need-related above random median) |
| G4 (both categories) | PASS | 100 each |

## Key Finding

Need-related packages on Hex.pm have **dramatically higher** 30-day download counts than random packages:

| Metric | Need-related | Random | Ratio |
|--------|--------------|--------|-------|
| Median | 80,078 | 365 | **220×** |
| Mean | 644,441 | 37,486 | **17×** |
| P10 | 3,734 | 111 | **34×** |
| P90 | 2,043,718 | 12,011 | **170×** |

99 of 100 need-related packages exceed the random median (365). The minimum need-related package (246 downloads) is near the random median.

## Interpretation

Hex.pm joins PyPI (E071), NPM (E072), and NuGet (E102) as a package registry where the view-count principle **holds strongly**. The principle fails on Maven Central (E090), crates.io (E095), and Hugging Face Hub (E101).

**Pattern emerging**: The principle works on package registries where:
1. Download counts reflect genuine usage (not inflated by CI/bots)
2. The ecosystem has a clear distinction between "infrastructure/framework" packages (high need) and "utility/niche" packages (low need)
3. The registry is mature with sufficient package diversity

Hex.pm's Elixir/Erlang ecosystem shows particularly strong separation — likely because web frameworks (Phoenix), database drivers (Ecto), and core infrastructure (Plug) dominate the need-related category, while the random sample captures many small, specialized, or abandoned packages.

## Methodology

- **Need classification**: Keyword-based (E071/E078 framework) — packages matching web, http, database, auth, cache, queue, json, logger, config, test, etc. without generic terms (utils, common, core, etc.)
- **Activity signal**: 30-day download count (`recent` field from Hex.pm API)
- **Random sample**: Default API listing (not sorted by downloads), pages 1-2
- **Need-related sample**: Keyword searches for infrastructure terms, sorted by downloads

## Files

- `PROTOCOL.md` — Experiment protocol
- `collect.py` — Data collection (Hex.pm API)
- `analyze.py` — Gate evaluation (Mann-Whitney U, Cliff's delta, Wilson CI)
- `raw/collected.json` — Raw package data (200 packages)
- `results.json` — Gate results and conclusion

## Commands

```bash
python3 collect.py    # Collect data (takes ~30s)
python3 analyze.py    # Evaluate gates
```