# Fedmarket CLI Decision Mode Implementation Plan

## Goal
Implement the `--decision` mode in `fedmarket.py` that helps small software teams apply the project's two-axis framework (entry accessibility vs. business sustainability) to choose a PSC code and entry strategy matched to their characteristics. This implements the E212 decision prototype.

## Architecture
The `--decision` flag will add a new argparse mode to `fedmarket.py`. When invoked, the user provides their profile characteristics (budget threshold, go-to-market strategy, focus), and the tool outputs a two-axis assessment with a profile-matched code recommendation. The implementation will:

1. Add `--decision` argparse flag with three sub-parameters: `budget`, `gtm`, `focus`
2. Implement `decide_code(budget, gtm, focus)` function that maps profiles to PSC codes and entry strategies
3. Integrate the two-axis entry_score and business_score from the existing assessment
4. Update `format_text` output to include the decision recommendation
5. Keep static mode and dynamic mode fully functional

## Tech Stack
- Python 3.14.6 (per capabilities file)
- fedmarket.py, fedmarket_data.py, fedmarket_core.py, fedmarket_dynamic_rec.py
- Existing two_axis_recommendation function
- E211 survival data (already loaded from raw/ results.json)
- E212 profile-based decision logic

## Implementation Plan

### Task 1: Add `--decision` argparse flag to fedmarket.py
**Modify:** `fedmarket.py` lines 40-78 (argparse section)
**Add:** `--decision` flag with three sub-parameters: `--decision budget gtm focus`
**Consumes:** None (new CLI argument)
**Produces:** None (just enables the decision mode)
**Test:** Run `python3 fedmarket.py 7030 --decision leq_40k direct software` and verify it doesn't error

### Task 2: Implement `decide_code` function
**Modify:** `fedmarket.py` - add after `main()` function or in a new helper section
**Function signature:** `decide_code(budget, gtm, focus)` → returns `(code, entry_axis, primary_vehicle, caveats)`
**Logic:**
- `budget` in `{"leq_40k", "leq_100k", "enterprise"}`
- `gtm` in `{"direct", "gsa_mas", "services"}`
- `focus` in `{"software", "services"}`
- Profile → code mapping (from E212):
  - `leq_40k` + `direct` + `software` → 7030, direct_sales
  - `leq_100k` + `gsa_mas` + `software` → DA10, gsa_mas_schedule_70
  - `enterprise` + `services` + `services` → DA01, gsa_schedule
- Also considers two-axis scores as tiebreaker/validation

### Task 3: Integrate decision into the two-axis assessment flow
**Modify:** `fedmarket.py` main() function - when `--decision` is set, run the profile decision and merge the result into the output dict
**Consumes:** budget, gtm, focus from CLI; static_metrics, dyn_metrics from assessment
**Produces:** `entry_axis`, `primary_vehicle`, `recommendation`, `caveats` fields in output

### Task 4: Update format_text output to display decision recommendation
**Modify:** `fedmarket_core.py` `format_text()` function
**Add:** Display section for "Decision recommendation" showing the code, entry axis, primary vehicle, and caveats when `output.get("recommendation")` is present

### Task 5: Test the new --decision mode
**Test:** Run fedmarket.py with various profiles and verify correct recommendations
- `python3 fedmarket.py 7030 --decision leq_40k direct software` → 7030, entry, direct_sales
- `python3 fedmarket.py DA10 --decision leq_100k gsa_mas software` → DA10, gwac_pathway, gsa_mas_schedule_70
- `python3 fedmarket.py DA01 --decision enterprise services services` → DA01, services_market, gsa_schedule

## Files Modified
- `fedmarket.py` - argparse, main(), decide_code function
- `fedmarket_core.py` - format_text output enhancement

## Verification
Run the full test suite: `PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests`
Check that existing functionality is not broken.