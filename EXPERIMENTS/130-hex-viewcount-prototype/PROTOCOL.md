# E130 — Hex.pm View-Count Prototype Protocol

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

## Objective

Build a runnable prototype CLI tool that applies the view-count principle's classification framework to Hex.pm packages, enabling evidence gathering on practical utility. This prototype tests whether the NEED_INDICATORS/GENERIC_TERMS classification from E103 produces consistent results with real user interaction, and whether download activity differences are observable in human-executed queries.

## Practical Difficulty

Elixir/Erlang developers exploring Hex.pm have no easy way to identify which packages address actual programming needs versus generic ones. Despite E103's validation that need-related packages have systematically higher activity (220× median difference, all gates pass), there is no tooling for developers to apply this classification in practice.

## Who Experiences It

Elixir/Erlang developers, Hex.pm users who want to surface packages that address genuine programming needs rather than generic/utility packages.

## Available Evidence

- **E103**: View-count principle passes all 4 gates on Hex.pm; need-related packages have median 80,078 recent downloads vs random's 365 (220× difference)
- **E113**: Matched harvest control shows view-count effects can be artifacts of topic selection and unanchored substring matching; any practical tool must control for these confounds
- **E103 classification framework**: NEED_INDICATORS (77 terms) and GENERIC_TERMS (8 terms) for package classification
- **Hex.pm API endpoints**: search, random listing, package detail with downloads

## Prototype Difference

A small, reversible CLI prototype (`hex_viewcount`) that:
1. Fetches packages from Hex.pm API (search or random listing)
2. Classifies each package using the NEED_INDICATORS/GENERIC_TERMS framework
3. Reports recent download counts and activity status
4. Computes activity rate differential (need-related vs random)
5. Can be run against any query or the default listing

The prototype is **evidence-gathering**, not product validation. It answers: "Does the E103 classifier produce consistent need/random classifications when users manually apply it to real Hex.pm packages, and are the activity differences observable?"

## Strongest Accessible Alternative

Manual exploration of Hex.pm without classification aids. Developers currently must read each package description manually to determine if it addresses their need - a time-consuming and inconsistent process.

## Failure Condition

- Classifier produces < 70% consistent classifications when run against a held-out sample (tests G0 discrimination)
- Activity rate differential is ≤ 0 (fails G2)
- Coverage < 100 packages (fails G1)
- Wilson CI95 lower bound for need-above-random proportion ≤ 0.60 (fails G3)

## Tech Stack

- Python 3.8+ (stdlib only, no external dependencies)
- Hex.pm JSON API
- Mann-Whitney U test (custom implementation, stdlib only)
- Cliff's delta (custom implementation, stdlib only)
- Wilson score interval

## Deliverables

- `collect.py` — Data collection and classification script
- `analyze.py` — Gate evaluation and activity statistics script
- `cli.py` — Command-line interface
- `PROTOCOL.md` — Experiment protocol
- `README.md` — Prototype summary
- `results.json` — Gate outcomes