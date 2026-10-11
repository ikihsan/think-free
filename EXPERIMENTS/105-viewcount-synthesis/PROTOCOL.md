<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# Experiment Protocol: View-Count Principle Synthesis Across Ecosystems

## Origin
- Mission: Think Free
- Decision driver: D083 — "the next session must start from fresh observation in a new domain"
- Predecessors: E071 (PyPI), E072 (NPM), E102 (NuGet), E104 (GitHub repos)
- This experiment synthesizes and compares the view-count principle across all ecosystems where it has been tested, and identifies the generalization boundaries.

## Question
What are the generalization boundaries of the view-count principle across package repositories and other platforms? Specifically: does the principle consistently distinguish need-related from random packages across ecosystems, and what platform characteristics determine success or failure?

## Hypothesis
H0: The view-count principle's ability to distinguish need-related from random packages is consistent across all tested ecosystems (no boundary).
H1: The view-count principle's effectiveness varies systematically with platform characteristics, with clear boundaries between ecosystems where it works and where it fails.

## Background
The view-count principle measures whether packages/metadata addressing a developer need are systematically more "active" (have exposure/arrival metadata) than random packages. It has been tested on:

- **PyPI (E071)**: Supported. 82.93% need-related active vs 57.50% random. G1-G3 all pass. Difference: 25.43pp. Key: PyPI JSON API provides activity metadata (release count, URLs, classifiers).
- **NPM (E072)**: Supported. 100% need-related active vs 0% random. G1-G3 all pass. Key: NPM JSON API provides activity metadata (release presence, homepage, repository, keywords).
- **NuGet (E102)**: Supported. Need-related median 7.8M downloads vs random 195K (~40×). G1-G4 all pass. Key: NuGet Azure Search API provides totalDownloads field.
- **GitHub repos (E104)**: Failed G2. Both need-related and random repos have 100% "active" rate (by stars), with no systematic difference in star counts. Key: GitHub stars don't systematically differentiate need-related from random repos.

Failed ecosystems:
- **crates.io (E095)**: G1 FAIL (n<30), G2 FAIL, G4 PASS (all have recent_downloads > 0)
- **Maven Central (E090)**: G3 FAIL (activity-rate difference 7.8pp, CI95 LB −0.41 < 10pp), G4 FAIL (arrival-field rate 53.6% < 95%)
- **Hugging Face Hub (E101)**: G2 FAIL (p=0.089), G3 FAIL (LB=0.089)
- **Web search (E065)**: 0 results with meaningful content
- **GitHub issues API (E063/E066)**: No arrival field

## Platform characteristic pattern
The view-count principle works on package repositories where the JSON/API metadata exposes activity indicators (download counts, release metrics, version history, project URLs, keywords). It does NOT generalize to:
- Social media / issue-tracking platforms without exposable arrival metrics
- Registries where all items are active (crates.io: 100% recent_downloads > 0)
- Registries where the activity metric doesn't differentiate need-related from random

## Arms
| arm | source | what it carries |
|---|---|---|
| **A** | Need-related packages from E071/E072/E102 harvests | package name, classification, activity metrics, gate results |
| **B** | Random packages from same harvests | package name, classification, activity metrics, gate results |

## Procedure
1. Read existing experiment results from EXPERIMENTS/071-pypi-viewcount-denominator/, EXPERIMENTS/072-npm-view-count-prototype/, EXPERIMENTS/102-nuget-viewcount/, EXPERIMENTS/104-github-repo-viewcount/
2. Extract gate outcomes, effect sizes, active rates, and key findings for each ecosystem
3. Compare across ecosystems and identify patterns
4. Document generalization boundaries and platform characteristics
5. Report results and suggest next experiments per D083

## Gates (retrospective analysis, not pre-registered for this synthesis)
All predeclared gates from the original experiments are reported. No new gates are declared for this synthesis.

## Analysis script
`run.py` — reads existing experiment results, produces comparison table and synthesis.

## Reproduction
```bash
cd EXPERIMENTS/105-viewcount-synthesis
python3 run.py --synthesize
```

## Outputs
- `results.json` — machine-readable synthesis results and raw data
- `README.md` — human-readable summary of the view-count principle's generalization boundaries