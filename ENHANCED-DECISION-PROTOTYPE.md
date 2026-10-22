# Enhanced Decision Prototype Implementation Plan

## Goal

Build an enhanced PSC code selection decision support prototype that implements the project's two-axis framework (entry accessibility vs. business sustainability) with proper normalized scoring, exploration mode, subcontract go-to-market support, and survival/sustainability integration — providing small software teams with actionable guidance on PSC code selection and entry strategy.

## Architecture

The prototype enhances the existing `fedmarket` package with:

1. **`decide.py`** — Core decision logic with proper normalized scoring replacing heuristic point-additions
2. **`decide_cli.py`** — CLI entry point with all GTM options, exploration mode, and improved UX
3. **`lookup.py`** — Updated static data with survival integration and E213 validation notes
4. **New `explore.py`** — Exploration mode showing all codes ranked by different profile priorities

The key design decision: replace the heuristic `+20` / `+15` point overrides in `decide_code()` with a principled normalized scoring system that weights Axis 1 (accessibility) and Axis 2 (sustainability) based on the team's profile priorities, then selects the top code.

## Tech Stack

- Python 3.8+ (project requirement)
- Existing fedmarket package (no new dependencies)
- Standard library only (pytest, json, argparse)

## Global Constraints (from AGENTS.md / REPO)

- No file may exceed 300 lines (split at 250 lines)
- Every document carries origin-meta block
- Must run `tools/origin doc lint` exit 0 before committing
- Label claims as observed, source-supported, inferred, speculative, or untested
- Never fabricate results, novelty, users, or adoption
- Separate mechanism, performance, practical usefulness, differentiation, and adoption

## Tasks

### Task 1: Enhance `decide.py` with proper normalized scoring

**Files to modify:** `fedmarket/fedmarket/decide.py`

**What to do:**
- Replace the heuristic profile-matching (arbitrary `+20`/`+15` point additions) with a proper scoring function
- The scoring should: normalize Axis 1 (accessibility) and Axis 2 (sustainability) scores to a 0-100 scale, weight them based on team profile priorities, and select the top-scoring code
- Support all 3 budget levels (leq_40k, leq_100k, enterprise)
- Support all 3 GTM options (direct, gsa_mas, subcontract)
- Support all 3 focus options (software, saas, services)
- Integrate survival data from KNOWN_SURVIVAL
- Keep backward compatibility with existing function signature

**Interface:**
- `decide_code(team_budget: str, team_gtm: str, team_focus: str) -> Dict[str, Any]` — unchanged signature
- Internal: `score_code(code, budget, gtm, focus, survival_weight) -> float` — new function

**Success criteria:**
- All existing tests in `tests/test_fedmarket_dynamic.py` and `tests/test_fedmarket.py` continue to pass
- The function produces different (and more reasoned) selections across profile combinations
- No arbitrary point additions (+20/+15)

### Task 2: Add subcontract GTM option to `decide_cli.py`

**Files to modify:** `fedmarket/fedmarket/decide_cli.py`

**What to do:**
- Add "subcontract" as a third GTM choice alongside "direct" and "gsa_mas"
- Map the subcontract option to the subcontract go-to-market approach
- Update the rationale/next-steps generation for subcontract profile
- Ensure the CLI accepts `--gtm subcontract`

**Interface:**
- `BUDGET_CHOICES = ("leq_40k", "leq_100k", "enterprise")` — unchanged
- `GTM_CHOICES = ("direct", "gsa_mas", "subcontract")` — updated
- `FOCUS_CHOICES = ("software", "saas", "services")` — unchanged

**Success criteria:**
- CLI accepts `--gtm subcontract` without errors
- `--gtm subcontract --focus software` produces a DA10 recommendation with subcontract rationale
- All existing CLI usage patterns continue to work

### Task 3: Add exploration mode — new `explore.py`

**Files to create:** `fedmarket/fedmarket/explore.py`

**What to do:**
- Create a new module that shows how all 5 PSC codes rank under different profile priority combinations
- Support priority weights for Axis 1 (accessibility) vs Axis 2 (sustainability)
- Generate a ranked table for each priority combination
- Include both static metrics and survival/sustainability data
- CLI: `fedmarket-explore --ax1-weight 0.5 --ax2-weight 0.5`
- Programmatic: `explore_rankings(ax1_weight, ax2_weight) -> Dict[str, List[tuple]]`

**Interface:**
- `explore_rankings(ax1_weight=0.5, ax2_weight=0.5, include_survival=True) -> dict`
  - Returns rankings of all codes by total score
  - Each code's score = ax1_weight * axis1_normalized + ax2_weight * axis2_normalized
- CLI entry point: `fedmarket-explore`

**Success criteria:**
- Can show how codes rank under different priority combinations
- Default (0.5/0.5) rankings match expectations: 7030 for accessibility-focused, DA10 for sustainability-focused
- Includes survival data in the output

### Task 4: Update `lookup.py` with survival integration and E213 notes

**Files to modify:** `fedmarket/fedmarket/lookup.py`

**What to do:**
- Integrate KNOWN_SURVIVAL and KNOWN_GRADUATION data into the assess_code output
- Add survival data fields to the static lookup (or ensure they're included when survival module data is available)
- Update E213 validation notes for all 5 codes
- Ensure the `assess_code` function returns comprehensive data for the decision logic

**Interface:**
- `assess_code(code) -> dict` — enhanced output with survival_integration field
- New fields: `survival_pct`, `graduation_pct`, `survival_name_est_pct`

**Success criteria:**
- All existing tests pass
- assess_code output includes survival-related fields
- E213 notes are accurate per experiment E213 findings

### Task 5: Update CLI entry point and pyproject.toml

**Files to modify:** `fedmarket/fedmarket/cli.py`, `fedmarket/pyproject.toml`

**What to do:**
- Add `fedmarket-explore` CLI command
- Update the main CLI to support the new features
- Ensure entry points are properly configured

**Interface:**
- `fedmarket --code 7030 --decision` — decision mode (existing)
- `fedmarket-explore` — new exploration mode

**Success criteria:**
- `fedmarket-explore` command works
- All existing CLI commands continue to work

### Task 6: Verify all tests pass and doc lint

**Files to verify:** All test files, doclint

**What to do:**
- Run the full test suite: `python3 -m pytest tests/ -v --tb=short` (network tests excluded)
- Run `tools/origin doc lint`
- Fix any issues

**Success criteria:**
- All non-network tests pass exit 0
- doc lint exits 0
- No file exceeds 300 lines

## Plan History

| Date | Version | Change |
|------|---------|--------|
| 2026-10-22 | 1.0 | Initial plan created |