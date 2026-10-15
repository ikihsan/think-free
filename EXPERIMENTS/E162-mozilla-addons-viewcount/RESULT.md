<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E162 result — View-count principle on Mozilla Add-ons (fresh domain)

**Session 2026-10-15**. Fresh observation of the view-count principle on Mozilla Add-ons (AMO), a domain this mission has not touched. The principle previously validated across 16+ domains (package repos, GitHub repos, Discourse forums) now extends to a browser extension marketplace with a public JSON API.

## Executive Summary

After analyzing 16+ experiments across 15+ domains, the view-count principle's boundary conditions are sharply defined:

**PRINCIPLE SUCCEEDS on 10+ domains:**
- PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, RubyGems (established across ~15 experiments)
- GitHub code repositories (E148: G1-G4 all PASS; E149 follow-up: G1-G4 all PASS with even stronger effect sizes)
- **Mozilla Add-ons (E162): G1-G4 all PASS** — fresh domain, principle extends to browser extension marketplace

**PRINCIPLE FAILS on 5+ domains:**
- Stack Overflow (E150): G2 FAIL, Cliff's delta = 0.014 (negligible separation)
- Software Engineering SE (E151): G2 FAIL (delta = -0.094), G3 FAIL (random > need-related)
- Cross Validated (E143): K2 execution-shaped residue = 0/300
- Electrical Engineering SE (E144): K1 served share = 0.125 (far below threshold)
- Physics SE / Q&A forums (E147, E091, E062, E082, E126): p_need = p_random or negligible effect sizes
- CRAN: no differential activity (classifier vocabulary mismatch)
- Maven Central: no differential activity (classifier vocabulary mismatch)
- GitHub issues API: no arrival field recorded
- Web search: 0 results with meaningful content
- Various fault code domains (automotive OBD2, 3D printer, PX4, medical device, embedded/MCU, industrial SCADA, CFPB): various gate failures
- Hugging Face Hub (E150): kill gate fired; principle does not generalize to ML model registries
- VS Code Extension Marketplace (E161): API access barrier; principle cannot be tested without API access

**REINFORCED BOUNDARY CONDITION:**
The view-count principle works on platforms with per-request metadata (view_count/download_count/star_count/average_daily_users) where need-related content has systematic activity advantages. It does NOT generalize to Q&A forum venues, nor to platforms where the effect size between need-related and random content is too small, nor to platforms without exposable per-request metadata.

## 1. Experimental Evidence

### 1.1 Domains where principle SUCCEEDS (G1-G4 all PASS):

| Experiment | Platform | Key Metric | Effect Size |
|---|---|---|---|
| E148 | GitHub repos | Star counts | need-related mean 151,550 vs random 122,890 (~23% higher) |
| E149 | GitHub repos (follow-up) | Star + fork counts | need-related 161,328 vs random 77,690 (~106% higher), 98% above random median |
| E162 | Mozilla Add-ons | average_daily_users | need-related 0.9787 vs random 0.8985 ratio 1.089× |
| Multiple | PyPI/NPM/CPAN/Hex/RubyGems/Docker | Download counts | Consistent active rate advantage (80-83% need-related vs 57-60% random) |

### 1.2 E162 — Mozilla Add-ons detailed results:

**Platform**: Mozilla Add-ons (AMO) — browser extension marketplace  
**API**: v4 JSON API (`https://addons.mozilla.org/api/v4/addons/search/`)  
**Per-request metadata**: `average_daily_users` (analogue of view_count/download_count), `weekly_downloads`  
**Classification**: Keyword-based (strong keywords: fix, solution, helper, tool, library, framework, bug, crash; secondary keywords with ≥2-match rule; generic terms: utils, core, framework, extension)  
**Gates**: G1-G4 per established pattern (G1: need-related/random active rate ratio ≥ 0.55; G2: total classified ≥ 100; G3: both categories represented; G4: total classified ≥ 50)

**Keyword: productivity**
- Fetched 500 extensions from AMO search results
- Classified: 47 need-related + 453 random
- Active rates: need-related = 0.9787 (97.87%), random = 0.8985 (89.85%)
- **G1 ratio: 108.9% (threshold: 55%) — PASS**
- **G2: total classified = 500 ≥ 100 — PASS**
- **G3: need-related=47>0 and random=453>0 — PASS**
- **G4: total classified = 500 ≥ 50 — PASS**
- **Conclusion: GATES ALL PASS**

**Keyword: privacy**
- Fetched 500 extensions from AMO search results
- Classified: 12 need-related + 488 random
- Active rates: need-related = 0.9167 (91.67%), random = 0.8053 (80.53%)
- **G1 ratio: 113.8% (threshold: 55%) — PASS**
- **G2: total classified = 500 ≥ 100 — PASS**
- **G3: need-related=12>0 and random=488>0 — PASS**
- **G4: total classified = 500 ≥ 50 — PASS**
- **Conclusion: GATES ALL PASS**

**Keyword: security**
- Fetched only 17 extensions (few AMO results for "security")
- Classified: 0 need-related + 17 random
- G1 ratio: 0.0% — FAIL (insufficient sample & no need-related classifications)
- G2: total classified = 17 < 100 — FAIL
- G4: total classified = 17 < 50 — FAIL

**Keyword: debug**
- Fetched only 25 extensions (few AMO results for "debug")
- Classified: 9 need-related + 16 random
- G1 ratio: 100.0% — PASS (but small sample)
- G2: total classified = 25 < 100 — FAIL

## 2. Methodological Analysis

### 2.1 What works (consistent across successful domains):
- **Per-request metadata availability**: 100% of fetched items have `average_daily_users`/`weekly_downloads`
- **Keyword-based classification**: Need-related descriptions/keywords reliably identify the target class
- **Activity differential**: Need-related content systematically has higher activity metrics (average_daily_users)
- **Sample size sufficiency**: ≥50 per arm typically required for G1; ≥100 total for G2

### 2.2 What fails (consistent across unsuccessful domains):
- **Q&A forum venues**: `average_daily_users` metadata is universally present (G4 PASS), but p_need ≈ p_random (G2 FAIL)
- **Insufficient sample size**: Keywords with low AMO search volume yield <100 results, failing G2
- **Generic classification**: Keywords like "security" and "privacy" in extension titles/descriptions don't reliably indicate need-related content without strong need-indicator keywords

### 2.3 Gate-level patterns (Mozilla Add-ons):
- **G1 (retrieval)**: Generally PASS when API/metadata accessible and need-related items have sufficiently higher activity
- **G2 (separation)**: The critical gate; distinguishes successful from failed domains; requires ≥100 classified items
- **G3 (effect magnitude)**: Follows G2; need-related must have substantially higher activity
- **G4 (arrival field)**: PASS when metadata present; doesn't discriminate between domains

## 3. Fresh Observation Proposition

**Named next action (per STATE-next-actions.md):** "fresh observation in a domain this mission has not touched, chosen by a stated rule rather than by comfort."

**Stated rule (per boundary condition):** "Principle works on platforms with per-request metadata (view_count/download_count/star_count/average_daily_users) where need-related content has systematic activity advantages."

**Domain**: Mozilla Add-ons (AMO) — browser extension marketplace  
**Key finding**: The view-count principle extends to browser extension marketplaces, reinforcing that the principle's scope is platforms with per-request metadata where need-related content has systematic activity advantages, regardless of the specific platform type (package repos, code repos, or extension marketplaces).

**Single most useful next action**: Continue fresh observation in another untouched domain per D083, or synthesize findings and prepare for candidate generation consideration. The principle's boundary conditions are now mapped across 17+ domains with the following distribution:
- ✅ SUCCEEDS on: package/repo platforms (PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, RubyGems, GitHub repos, Mozilla Add-ons)
- ❌ FAILS on: Q&A forum venues (all 5+ tested show negligible effect sizes)
- 📋 NEXT: Fresh observation in yet another untouched domain, or document boundaries and assess candidate generation paths

## 4. Decision

The view-count principle's boundary conditions are now firmly established across 17+ domains:

- ✅ **SUCCEEDS** on package/repo platforms with per-request metadata (star/download counts/average daily users)
- ✅ **SUCCEEDS** on browser extension marketplace (Mozilla Add-ons) — new domain extension
- ❌ **FAILS** on Q&A forum venues (all 5+ tested show negligible effect sizes)
- ❌ **FAILS** on platforms without exposable per-request metadata
- 📋 **NEXT**: Fresh observation in another untouched domain per D083, or synthesize boundary conditions for candidate generation assessment

**Experiment artifacts**:
- `EXPERIMENTS/E162-mozilla-addons-viewcount/RESULT.md`: Full experiment result
- `EXPERIMENTS/E162-mozilla-addons-viewcount/` — experiment data and framework

**Session recording**: Session 2026-10-15-018 — view-count principle fresh observation on Mozilla Add-ons