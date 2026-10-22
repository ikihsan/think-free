# Fedmarket Decision Prototype Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

## Goal

Build a polished, standalone prototype decision support tool that small software teams can use to navigate the federal IT marketplace, based on the project's two-axis framework (entry accessibility vs. business sustainability). The prototype is a reversible exploratory prototype — it gathers evidence about framework behavior without claiming adoption or user numbers.

## Architecture

The prototype extends the existing `fedmarket-decide` CLI and `fedmarket-explore` exploration tool with:
1. A enhanced interactive CLI with better prompts and formatting
2. A summary document of all 27 profile-based recommendations
3. A simple importable Python module for integration into other tools
4. Improved output with metrics, caveats, and next steps

The core decision logic (`fedmarket/decide.py:decide_code()`) and data (`fedmarket/data.py:PSC_CODES_STATIC`) remain unchanged — the prototype adds usability enhancements and documentation around the existing framework.

## Tech Stack

- Python 3.8+ (project requirement)
- Existing fedmarket package (no new dependencies)
- Fedmarket CLI entry points: `fedmarket-decide`, `fedmarket-explore`
- Static lookup data from experiments E206/E211

## Global Constraints

- No new external dependencies (keep `pyproject.toml` dependencies empty)
- Maintain compatibility with Python 3.8+
- Keep all files under 300-line cap
- Preserve existing static data from E206/E211 experiments
- No fabricating results, novelty, or adoption claims
- Prototype is evidence-gathering, not product validation

## Task Breakdown

### Task 1: Enhance fedmarket-decide CLI

**Files:**
- Create: `fedmarket/fedmarket/enhanced_decide_cli.py` (new module)
- Modify: None (existing files remain as-is for backward compatibility)

**Interfaces:**
- Consumes: `fedmarket.decide.decide_code()` — the core recommendation function
- Produces: Enhanced CLI output with better formatting, metrics display, and two-axis context

**Steps:**
- [ ] **Step 1:** Create `enhanced_decide_cli.py` with improved interactive prompts
  - [ ] Add clear question framing with descriptive option texts
  - [ ] Add two-axis framework context display after recommendation
  - [ ] Add `--profile` flag to specify a profile directly (skip interactive)
  - [ ] Add `--compare` flag to show how other codes ranked for the same profile
- [ ] **Step 2:** Run the enhanced CLI with each of the 3 primary profiles (leq_40k+direct+software, leq_100k+gsa_mas+software, enterprise+direct+services) to verify output quality
- [ ] **Step 3:** Test `--profile` and `--compare` flags with representative profiles
- [ ] **Step 4:** Commit enhanced CLI module

### Task 2: Create 27-Profile Summary Document

**Files:**
- Create: `docs/PROTOTYPE-SUMMARY.md` (new document, will be split if over 250 lines)
- Modify: None

**Interfaces:**
- Consumes: Exploration results from `fedmarket-explore --all`
- Produces: Human-readable summary of which PSC code is recommended for each of the 27 profile combinations, with key metrics and rationale

**Steps:**
- [ ] **Step 1:** Run `fedmarket-explore --all` and capture all 27 results
- [ ] **Step 2:** Extract for each profile: recommended code, entry axis, primary vehicle, screen score, ≤$40k fraction, software %, survival %, graduation %, and the rationale
- [ ] **Step 3:** Organize into a clear table format: Profile | Recommended Code | Entry Axis | Key Metrics | Rationale
- [ ] **Step 4:** Add summary analysis of patterns (which codes win in which scenarios)
- [ ] **Step 5:** Commit summary document (split if over 250 lines)

### Task 3: Create Importable Decision Module

**Files:**
- Create: `fedmarket/fedmarket/decision.py` (new module with public API)
- Modify: None

**Interfaces:**
- Consumes: `fedmarket.decide.decide_code()`, `fedmarket.lookup.assess_code()`
- Produces: A clean Python API: `decide_code(budget, gtm, focus) -> dict` with standardized output format

**Steps:**
- [ ] **Step 1:** Create `decision.py` that wraps `decide_code` with input validation and output normalization
- [ ] **Step 2:** Test import and basic usage: `from fedmarket.decision import decide; decide("leq_40k", "direct", "software")`
- [ ] **Step 3:** Verify output contains: recommended_code, entry_axis, primary_vehicle, rationale, next_steps
- [ ] **Step 3:** Commit decision module

### Task 4: Run Comprehensive Validation

**Files:**
- Modify: None (read-only validation)
- Test: Run all 27 profiles through enhanced CLI and importable module

**Steps:**
- [ ] **Step 1:** Run `fedmarket-decide` with all 27 profile combinations via scripted flags
- [ ] **Step 2:** Compare outputs with `fedmarket-explore --all` rankings
- [ ] **Step 3:** Document any discrepancies or confirm consistency
- [ ] **Step 4:** Commit validation results

### Task 5: Finish with Decision and Continuation

**Files:**
- Modify: `STATE-next-actions.md` (update next action)
- Modify: `STATE.md` (update dashboard if needed)

**Steps:**
- [ ] **Step 1:** Record the prototype build decision in the session outcome
- [ ] **Step 2:** Update STATE-next-actions.md with the new next action
- [ ] **Step 3:** Document what was produced, which build decision changed, what remains unknown, and the single most useful next action
- [ ] **Step 4:** Finish the session with proper recording

## Success Criteria

The prototype is successful if it:
1. Runs without errors on all 27 profile combinations
2. Produces clear, actionable recommendations with proper rationale and next steps
3. Correctly identifies 7030 for leq_40k+direct+software (the prototype's original recommendation)
4. Correctly identifies DA10 for gsa_mas profiles (especially leq_100k+gsa_mas+software)
5. Correctly identifies DA01 for enterprise+direct+services
6. Generates a summary document that reveals meaningful patterns
7. Creates an importable Python API that works without errors
8. Preserves all existing data and doesn't break any existing functionality
9. Is documented as a reversible exploratory prototype (not a product claim)

## Known Patterns from Exploration (for reference)

Based on running all 27 profiles, the consistent findings are:
- **7030 wins** for: `leq_40k + direct + software` (by 0.5 points over DA10)
- **DA10 wins** for: Most profiles involving `gsa_mas` GTM, or `leq_100k`/`enterprise` budgets
- **DA01 wins** for: `enterprise + direct + services` (by small margin over DA10)
- **7A21** rarely wins, only in specific weight configurations
- **D304** never wins (as expected - not a software market)
- The tradeoff is consistent: 7030 maximizes entry ease, DA10/DA01/7A21 offer stronger sustainability