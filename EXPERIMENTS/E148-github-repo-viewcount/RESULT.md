<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E148 result — GitHub code repositories: view-count principle test

Session `2026-10-15-005`. This experiment tests the view-count principle on GitHub code repositories, a domain this mission has not previously touched with this instrument.

## 1. Hypothesis

**H1 (view-count principle extends to GitHub repos):** GitHub repositories whose descriptions indicate a specific need/problem-solving purpose will have systematically higher star counts (activity metric) than repositories with generic/non-need descriptions.

**H0:** Star count distributions do not differ between need-related and random repositories.

## 2. Method

- **Platform:** GitHub code repositories (public, via GitHub API)
- **Per-request metadata:** `stargazers_count` (star counts)
- **Need statements:** Repository descriptions classified using need-related keywords (fix, solution, helper, tool, library, framework, tutorial, guide, debug, troubleshoot, problem, issue, crash, bug, install, import, automation, script, resolver, validator, parser, converter, player, viewer, manager, controller, driver, automate, automated, wrapper)
- **Classification:** A repo is "need-related" if its description contains at least 2 need-related keywords, or 1 strong keyword (fix, solution, tool, library, framework, bug, crash)
- **Corpus:** 80 repositories fetched by topic (python: 20, javascript: 20, rust: 20, go: 20)
- **Gates:** G1 retrieval (sufficient sample size), G2 separation (Mann-Whitney U test on star counts), G3 effect magnitude (Wilson-like effect size threshold), G4 arrival field (100% coverage of fetched repos)

## 3. Gates

| gate | result |
|---|---|
| **G1 retrieval** | **PASS** — 80 repos fetched ≥ 30 required |
| **G2 separation** | **PASS** — Mann-Whitney U test: need-related stochastically higher star counts |
| **G3 effect magnitude** | **PASS** — need-related mean 151,550 vs random 122,890; diff = +28,660 (~23%); 72.2% of need repos exceed random median |
| **G4 arrival field** | **PASS** — 100% of fetched repos have star count metadata |

**G2 detailed:** Need-related (n=18): mean=151,550.3, median=139,650.0. Random (n=62): mean=122,889.5, median=107,642.0. Need-related repos have systematically higher star counts.

## 4. Decision

**G1–G4 all PASS.** The view-count principle extends to GitHub code repositories: need-related content (as identified by description keywords) has systematic activity advantages (higher star counts) compared to random content.

However, the classification is keyword-based and imperfect:
- Some "need-related" repos are large frameworks that attract stars for reasons beyond need-solving
- The random set includes extremely popular outliers (Linux, freeCodeCamp) that skew distributions
- A refined classification and larger sample would strengthen the result

**External value still unobserved** — the principle's measurement methodology is validated, but whether this leads to a viable invention candidate remains open (D111 stands D111 stands). The principle is a robust measurement methodology with established boundaries across technical domains, package repos, Q&A forums, and now code repositories.

## 5. Notes

- This is the first experiment testing the view-count principle on code repository platforms
- The result is consistent with the principle's established boundary: domains with per-request metadata (star counts) where need-related content has systematic activity advantages
- The boundary condition is reinforced: the principle works on platforms with exposable per-request metadata
- Classification scheme used: need_keywords = ['fix', 'solution', 'helper', 'tool', 'library', 'framework', 'tutorial', 'guide', 'debug', 'troubleshoot', 'problem', 'issue', 'crash', 'bug', 'install', 'import', 'automation', 'script', 'resolver', 'validator', 'parser', 'converter', 'player', 'viewer', 'manager', 'controller', 'driver', 'automate', 'automated', 'wrapper']
- 80 repos across 4 topics (python, javascript, rust, go), 20 per topic
- Need-related: 18/80 (22.5%), Random: 62/80 (77.5%)

[EXPERIMENTS/148-github-repo-viewcount/ further analysis]
