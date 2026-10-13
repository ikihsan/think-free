<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E112 — Fresh observation: view-count principle on VS Code marketplace

## Question

Does the view-count principle generalize to IDE extension marketplaces? Specifically,
do need-related VS Code extensions (those whose descriptions/reviews mention errors,
fixes, debugging, or troubleshooting) have systematically higher install counts than
random extensions?

## Why this matters

The view-count principle has been validated on package registries (PyPI, NPM, NuGet,
RubyGems, Packagist, Hex.pm, crates.io, CPAN), container registries (Docker Hub), ML
model registries (Hugging Face), Q&A forums (Discourse, Stack Exchange), and code
repositories (GitHub). It has failed on web search, HN corpus, CFPB, automotive OBD2,
3D printer fault codes, and PX4 drone fault codes.

IDE extension marketplaces are a fundamentally different platform structure: they
combine software distribution (like package repos) with user reviews (like forums)
and have arrival metadata (install counts, ratings) that reflects both popularity
and need. This tests the principle's breadth beyond its established domains.

## Population

VS Code Marketplace extensions, accessed via the public API:
`https://marketplace.visualstudio.com/items?itemName={publisher}.{name}`

Need-related keywords: error, fix, debug, troubleshoot, problem, issue, crash, bug,
lint, format, refactor, test, deploy, ci, cd, git, docker, kubernetes, api, database,
sql, nosql, react, vue, angular, node, python, java, rust, go, typescript, javascript

## Gates (declared before measurement)

| gate | description | threshold |
|---|---|---|
| G1 | need-related sample size | n >= 30 |
| G2 | arrival metric coverage | >= 95% have install counts |
| G3 | need-related vs random install count separation | Cliff's delta > 0.2 AND p < 0.05 |
| G4 | need-related active rate | >= 50% have > 100 installs |

## Kill gate

If G3 fails (no significant separation between need-related and random extensions),
the principle does not generalize to this domain. This is a negative result that
maps the principle's boundary.

## Method

1. Harvest 100 need-related extensions (matching keywords in description)
2. Harvest 100 random extensions (no keyword match)
3. Measure install counts for both groups
4. Compute Cliff's delta and Mann-Whitney U test
5. Compare need-related vs random median install counts

## Prior art

The VS Code marketplace is the largest IDE extension marketplace with ~50,000
extensions. It is maintained by Microsoft and has a public API. No prior art for
view-count analysis of this marketplace is known.

## Uncertainty

The principle may not generalize because:
- IDE extensions are often installed for convenience, not need
- Install counts may reflect IDE bundle-in rates rather than individual choice
- The marketplace is dominated by Microsoft first-party extensions

## Artifacts

| file | what it is |
|---|---|
| `PROTOCOL.md` | this file |
| `harvest.py` | harvesting script |
| `results.json` | raw results |
| `RESULT.md` | analysis and gates |
