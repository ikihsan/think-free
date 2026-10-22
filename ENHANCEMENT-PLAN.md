# Fedmarket Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

## Goal

Enhance the `fedmarket.py` federal marketplace assessment prototype to incorporate E211 two-axis survival analysis, dynamic data refresh from USAspending API, and improved two-axis recommendations (entry vs sustainability) for small software teams considering federal marketplace entry.

## Architecture

The enhanced `fedmarket.py` will have three major capabilities:

1. **Static assessment mode** - uses pre-computed lookup data (existing behavior, verified against E199/E200 baselines within 0.1 pp)
2. **Dynamic API refresh mode** - queries USAspending API for current metrics, caches results locally
3. **Two-axis recommendation engine** - combines accessibility metrics (screen score, award size distribution) with sustainability metrics (entry survival, graduation rates from E211)

The prototype will remain clearly labeled as a reversible exploratory prototype: it packages observed data with clear provenance and does not claim new algorithms or real-world validation.

Key design decisions:
- **Backward compatibility**: existing static data and CLI behavior unchanged
- **Provenance tracking**: every dynamically fetched metric records source URL, fetch date, and page count
- **Graceful degradation**: if API fetch fails, falls back to static lookup with clear warning
- **Two-axis axis**: code-dependent recommendation of "entry" (7030-style) vs "business" (DA10-style)

## Tech Stack

- Python 3.14+
- USAspending API v2 (public, no authentication required)
- SQLite for caching API responses
- Existing `fedmarket.py` data schema as baseline

## Provenance

This plan is grounded in experiments E197-E211 (2026-10-20/21), specifically:
- E202-E206: recipient, award, time-window, agency, vehicle SIN/SEWP analysis
- E211: entry survival - 7030 53.3% survival, 1.2% graduation; DA10 72.6% survival, 23.7% graduation
- COMPARISON_REPORT.md: full comparative analysis of all 5 PSC codes
- fedmarket.py static data reproduced from E206 validated metrics within 0.1 pp

## Files to Create/Modify

### Create:
- `fedmarket_dynamic.py` - new module for dynamic API querying and caching
- `tests/test_fedmarket_dynamic.py` - test suite for dynamic module

### Modify:
- `fedmarket.py` - integrate two-axis recommendation, import dynamic module, add `--refresh` CLI flag
- `tests/test_fedmarket.py` - add tests for two-axis recommendation and dynamic mode

## Task Breakdown

### Task 1: Add dynamic API querying module (`fedmarket_dynamic.py`)

**Files:**
- Create: `fedmarket_dynamic.py`
- Create: `tests/test_fedmarket_dynamic.py`

**Interfaces:**
- Consumes: USAspending API v2 endpoints (`/api/v2/awards/`, `/api/v2/subawards/`)
- Produces: dict with metrics: survival_pct, graduation_pct, n_cohort, etc.

**Steps:**
- [ ] **Step 1:** Write test for USAspending API connection check (skips if no network)
  - Test that API is reachable at base URL
  - Test that authentication is not required
- [ ] **Step 2:** Implement `fetch_awards()` function that queries `/api/v2/awards/` with PSC code filter, pagination, and returns award summaries (PIID, amount, UEI, description, agency)
  - Handle pagination (page/per_page params)
  - Cap at 100 pages (4000 awards) as ceiling from E211
  - Return list of dicts with minimal fields
- [ ] **Step 3:** Implement `fetch_subawards()` function for subaward analysis
  - Query `/api/v2/subawards/` with filters
  - Return subaward records with prime vendor, subvendor flags
- [ ] **Step 4:** Implement `compute_survival()` function that takes award cohort and return-window awards, computes:
  - Survival % (UEI match between entry window and return window)
  - Graduation % (aggregate > $100k in return window)
  - Mean/median awards per UEI
- [ ] **Step 5:** Implement caching with SQLite, storing fetch metadata (URL, date, page count, records count)
- [ ] **Step 6:** Write all tests and verify they pass (integration tests use recorded data or mock)

### Task 2: Integrate dynamic module into fedmarket.py and add two-axis recommendation

**Files:**
- Modify: `fedmarket.py` (add imports, CLI flags, two-axis engine)

**Interfaces:**
- Consumes: `fedmarket_dynamic` module functions
- Produces: enhanced assessment output with two-axis recommendation

**Steps:**
- [ ] **Step 1:** Add import of `fedmarket_dynamic` with try/except (optional dependency)
- [ ] **Step 2:** Add `--refresh` CLI flag that triggers dynamic API fetch and updates static data
- [ ] **Step 3:** Implement two-axis recommendation engine that combines:
  - Accessibility axis: screen score, <=$40k fraction, recipient count, software %
  - Sustainability axis: survival %, graduation %, net-positive return
  - Code-dependent mapping (7030 → entry, DA10 → business, etc.)
- [ ] **Step 4:** Update `decision_guide()` function to include two-axis recommendation based on both axes
- [ ] **Step 5:** Update `format_result()` to include survival/graduation metrics when dynamic data available
- [ ] **Step 6:** Update `compare_codes()` to rank by combined two-axis score

### Task 3: Add tests and verify

**Files:**
- Modify: `tests/test_fedmarket.py`
- Modify: `tests/test_fedmarket_dynamic.py`

**Steps:**
- [ ] **Step 1:** Write test for two-axis recommendation logic (entry vs business)
- [ ] **Step 2:** Write test that static mode still works without API
- [ ] **Step 3:** Write test that dynamic mode degrades gracefully when API unavailable
- [ ] **Step 4:** Run full test suite and verify all pass
- [ ] **Step 5:** Manual CLI testing: `python3 fedmarket.py 7030`, `python3 fedmarket.py DA10 --refresh`

### Task 4: Documentation and provenance

**Files:**
- Modify: `fedmarket.py` docstring
- Create: `EXPERIMENTS/fedmarket-enhancement/RESULT.md` (if needed)

**Steps:**
- [ ] **Step 1:** Update module docstring with E211 provenance and two-axis description
- [ ] **Step 2:** Add `--refresh` help text explaining dynamic mode
- [ ] **Step 3:** Record raw API fetch commands and results in a session
- [ ] **Step 4:** Run `tools/origin doc lint` to verify caps and metadata

## Success Criteria

- [ ] Enhanced `fedmarket.py` runs unchanged without --refresh flag
- [ ] `--refresh` flag triggers API fetch and updates metrics
- [ ] Two-axis recommendation correctly identifies 7030 for entry, DA10 for business
- [ ] Graceful degradation when API unavailable (falls back to static data with warning)
- [ ] All existing tests pass
- [ ] Doc lint exits 0
- [ ] Provenance metadata recorded for any dynamically fetched data

## Risk Mitigation

- **API rate limits**: cap at 100 pages total per code (matching E211 ceiling)
- **Network failures**: graceful fallback to static data with clear warning label
- **Data staleness**: cache with fetch date; recommend `--refresh` monthly or quarterly
- **Scope creep**: keep prototype focused on assessment + two-axis recommendation, not lead generation or web interface