# E130 — Hex.pm View-Count Prototype

## What This Prototype Does

A command-line tool that applies the view-count principle's classification framework to Hex.pm packages. It fetches packages from the Hex.pm API, classifies each as `need-related` or `random` using the NEED_INDICATORS/GENERIC_TERMS framework from E103, and reports activity metrics (recent download counts, activity rates) along with gate evaluation results (G1–G4).

## Why This Matters

Despite E103 validating that need-related packages on Hex.pm have dramatically higher activity (220× median: 80,078 vs 365, all gates pass), Elixir/Erlang developers have no practical way to identify which packages address genuine programming needs. This prototype provides a tool for evidence gathering on the principle's practical utility.

## Important Caveats

- **E113 matched-harvest caution**: The view-count effect can be a harvest artifact driven by topic selection and unanchored substring matching. This prototype does not control for asymmetric topic arms or age confounds the way E113 does. Results should be interpreted as preliminary.
- **Prototype, not product**: This is an evidence-gathering prototype. It does not claim to solve the package discovery problem or constitute a shipped product.
- **Classifier imperfection**: The NEED_INDICATORS/GENERIC_TERMS terms are heuristics; real-package descriptions may not cleanly fall into one category.

## How to Run

```bash
# Search mode: fetch packages matching a keyword, classified
python3 cli.py --mode search --query "web framework" --max-packages 50

# Random mode: fetch from default listing, classified
python3 cli.py --mode random --max-packages 50
```

## Output

The tool prints:
- Classified totals (need-related vs random)
- Activity rates (recent downloads > 0)
- Mann-Whitney U test p-value and Cliff's delta
- Wilson CI95 lower bound for proportion of need-related above random median
- Per-gate pass/fail status (G1–G4)

## Prototype Status

**EXPERIMENTAL**. Run `python3 cli.py --help` for usage information.

## Links

- Protocol: `EXPERIMENTS/130-hex-viewcount-prototype/PROTOCOL.md`
- Results: `EXPERIMENTS/130-hex-viewcount-prototype/results.json`