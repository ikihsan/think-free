# Small Program Entrant Advisor Implementation Plan

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->


> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

## Goal

Build a reversible exploratory prototype (Small Program Entrant Advisor) that helps small government contracting and NIH SBIR program applicants identify the best market entry points. The prototype fixes the known D128 defect in the NIH accessibility prototype and integrates learnings from all prior experiments (E204-E215).

## Architecture

Two integrated modules:
1. **IT Code Entrant Advisor v3** (`tools/it_entrant_advisor_v3.py`) — uses `meta.total` for complete census
2. **NIH SBIR Category Advisor v3** (`tools/nih_small_program_advisor_v3.py`) — activity_codes + meta.total

Both modules share common metrics (segment newcomer fraction, fragmentation, top-5 share, obligation) and follow the same experimental design as E208/E209.

## Tech Stack

Python 3.8+, urllib.request (stdlib only)

## Global Constraints

- Prototype is evidence-gathering, not product validation
- All gates declared before code/fetch
- Use API `meta.total` for complete census, no arbitrary caps
- Activity codes must be filtered when specified (D128 fix)
- Raw data and scripts preserved for reproducibility
- No fabricated results, novelty, users, or adoption
- Session logging via `tools/origin session` workflow
- `doc lint` must exit 0 after changes

## Task Plan

### Task 1: Verify NIH `fetch_grants()` has activity_codes + meta.total

**Files:** `tools/nih_sbir_metrics.py` — already correct (verified: activity_codes filter at lines 56-57, meta.total census at lines 84-86)

**Steps:**
- [x] **Complete:** Function already has both features. D128 defect was in `nih_accessibility_prototype.py` which is a separate file.

### Task 2: Implement IT code entrant v3 with meta.total census

**Files:**
- Create: `tools/it_entrant_advisor_v3.py`
- Modify: `tools/it_code_entrant.py` — replace 500-page ceiling with meta.total

**Interfaces:**
- Consumes: PSC code list, current/prior window data from USAspending
- Produces: code-level results, award-type sub-segment results, advisor recommendations

**Steps:**
- [x] **Complete:** `it_entrant_advisor_v3.py` created and verified. `it_code_entrant.py` updated with `meta.total`-based `fetch_window()`.

### Task 3: Implement NIH SBIR category advisor v3

**Files:**
- Create: `tools/nih_small_program_advisor_v3.py`

**Interfaces:**
- Consumes: spending category code, fiscal year, optional activity_codes
- Produces: ranked Funding ICs by access_score, consensus IC identification, cross-category comparison

**Steps:**
- [x] **Complete:** `nih_small_program_advisor_v3.py` created and verified. Uses `screen_category()` from `nih_small_program_screener.py` with activity_codes + meta.total.

### Task 4: Integrate and document the combined prototype

**Files:**
- Create: `tools/small_program_advisor.py` (wrapper dispatcher)
- Create: `EXPERIMENTS/E216-small-program-advisor/PROTOCOL.md`
- Create: `EXPERIMENTS/E216-small-program-advisor/RESULT.md`

**Interfaces:**
- Consumes: user specifies --it-codes or --category-code
- Produces: complete advisor output for the chosen domain

**Steps:**
- [ ] **Step 1:** Create `tools/small_program_advisor.py` that dispatches to either IT or NIH module based on CLI args
- [ ] **Step 2:** Document the prototype in experiment directory `EXPERIMENTS/E216-small-program-advisor/`
- [ ] **Step 3:** Run the full prototype and capture results
- [ ] **Step 4:** Write `RESULT.md` with all findings, gates, and raw data
- [ ] **Step 5:** Run `tools/origin doc lint` to verify compliance
- [ ] **Step 6:** Commit all changes

## Verification

1. `tools/origin doctor` reports clean state
2. `tools/origin doc lint` exits 0
3. IT code test: it_entrant_advisor_v3.py produces structural output matching E209 expectations
4. NIH test: nih_small_program_advisor_v3.py category 101 produces 147 grants with activity_codes filter
5. No new dependencies: stdlib only
6. Reproducibility: raw data + sha256 hashes preserved

## Exit Criteria

All four tasks complete:
- Both v3 modules are runnable and produce correct-by-construction output
- D128 defect (activity_codes + meta.total) is fixed in `nih_sbir_metrics.py` (was already correct)
- All raw data and sha256 hashes preserved
- doc lint passes
- Prototype documented in RESULT.md experiment entry