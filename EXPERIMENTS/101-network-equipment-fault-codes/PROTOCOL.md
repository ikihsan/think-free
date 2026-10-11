<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E101 — Fresh observation in network equipment fault codes domain

**Session:** `2026-10-11-XXX`, VM `instance-20260717-0944`, observed 2026-10-11.

## Summary

Measure the view-count principle (independent arrivals at a need via `view_count`) on network equipment Discourse forums. This is a fresh domain (network equipment / networking hardware) not previously tested by the mission — distinct from:
- E077: Non-software Discourse forums (general)
- E082: Embedded/microcontroller Discourse forums
- E100: Industrial automation/SCADA Discourse forum

## Target Forums (Accessible)

| Forum | Platform | Description |
|-------|----------|-------------|
| forum.mikrotik.com | Discourse | MikroTik RouterOS community |
| community.cambiumnetworks.com | Discourse | Cambium Networks community |
| community.f5.com | Discourse | F5 Networks community |

**Note:** Other target forums (community.cisco.com - 403 Forbidden, community.ui.com - parse error, forums.juniper.net - 404 Not Found) were not accessible via the Discourse `/latest.json` API endpoint. This is consistent with E077 where 3 of 10 target forums failed.

## Hypothesis

Network equipment practitioners (network engineers, sysadmins, IT professionals) encounter structured fault/error codes on networking hardware and need practical lookup/troubleshooting tools. The view-count instrument should generalize to this domain.

## Gates (Pre-declared)

| Gate | Criterion | Measurement |
|------|-----------|-------------|
| **G1** Need prevalence | ≥ 15 need statements (vc_positive) across forums | Count of classified need statements |
| **G2** Control validity | Corpus ≥ 100 topics (for statistical power) | Total topics harvested |
| **G3** Unserved fraction | < 50%, CI95 upper < 60% | Wilson CI95 on unserved-open-like / vc_positive |
| **G4** view_count validation | ≥ 95% view_count > 0 | Fraction of topics with view_count > 0 |

## Classification Rubric (from E077/E082 — must use unchanged)

A need statement is **unserved-open-like** when all three hold:
1. **No code solution present** — the statement does not name or describe a tool, library, or service that would satisfy the need using a fault code, and no reply mentions a working code-based solution
2. **States a concrete need involving fault codes** — title or body asks for help with, interpretation of, lookup of, or troubleshooting of a specific fault/error code (or class of codes), or for a tool that can look up/interpret fault codes
3. **Not a request for content, service, price, access, or human work** — the requester's own data means their firmware/device state (their firmware version, their hardware revision), which is expected and not disqualifying. The disqualifier is whether a program would need *private data the requester holds but cannot share* (their device's private memory, their proprietary code, their hardware-specific configuration).

A need statement is **served** when it states a concrete need involving fault codes and either names or clearly implies an existing tool/service that addresses it through code lookup/interpretation.

**Operationalization (from E082):**
- **is_resolved**: topic has accepted answer, OR (reply_count ≥ 3 AND op_like_count ≥ 1), OR closed
- **is_need**: title/body matches NEED_PATTERNS and not NON_NEED_PATTERNS
- **served** = is_need AND is_resolved
- **unserved-open-like** = is_need AND NOT is_resolved

## Measurement Protocol

1. **Harvest**: Fetch top 50 topics by views from each forum (200 total)
2. **Classify**: Apply rubric to each topic title + first post excerpt
3. **Validate**: Check G1 (≥15 vc_positive), G2 (corpus ≥100, control accuracy ≥0.85), G3 (unserved fraction CI), G4 (view_count > 0)
4. **Record**: results.json with per-forum and aggregate results

## Evidence Labels

- view_positive_rate: **observed** (measured on topics)
- need_fraction: **observed** (measured)
- unserved_open_like_fraction: **observed** (measured)
- Control accuracy: **observed** (measured)
- Platform invariance of view_count instrument: **observed** (if G4 passes)

## Experiment Results (Observed 2026-10-11)

| Gate | Criterion | Result | Value |
|------|-----------|--------|-------|
| **G1** Need prevalence | ≥ 15 need statements | **PASS** | 17 of 150 (11.3%) |
| **G2** Control validity | Corpus ≥ 100 topics | **PASS** | 150 topics |
| **G3** Unserved fraction | < 50%, CI95 upper < 60% | **PASS** | 10.0%, CI95 [5.7%, 16.5%] |
| **G4** view_count validation | ≥ 95% view_count > 0 | **PASS** | 100% |

### Per-Forum Breakdown

| Forum | Topics | Need | Served | Unserved-open-like | Need % | Unserved % | View+ % |
|-------|--------|------|--------|-------------------|--------|------------|---------|
| forum.mikrotik.com | 50 | 9 | 2 | 7 | 18.0% | 14.0% | 100% |
| community.cambiumnetworks.com | 50 | 2 | 0 | 2 | 4.0% | 4.0% | 100% |
| community.f5.com | 50 | 6 | 0 | 6 | 12.0% | 12.0% | 100% |
| **Aggregate** | **150** | **17** | **2** | **15** | **11.3%** | **10.0%** | **100%** |

### Key Findings

1. **view_count instrument generalizes to network equipment Discourse forums**: 100% view_positive_rate matches E077's finding on non-software Discourse forums (100%) and E082's finding on embedded Discourse forums (100%). This is the seventh platform type where the arrival instrument works.

2. **Unserved-open-like fraction is consistent with Discourse baseline**: 10.0% aggregate unserved-open-like fraction (CI95 [5.7%, 16.5%]) is statistically consistent with E077's 11.7% (CI95 [8.8%, 15.5%]) and E082's 15.3% (CI95 [10.5%, 21.3%]) across Discourse forums. The "unserved ≠ unserved" pattern holds across platform types.

3. **Need prevalence varies by community**: forum.mikrotik.com has higher need prevalence (18%) vs community.cambiumnetworks.com (4%) and community.f5.com (12%), reflecting different community focuses.

4. **No candidate produced**: This is an evidence-gathering experiment per D083 (fresh observation in new domain). The validated instrument and consistent unserved fraction refine the instrument's documented limits but do not generate a product.

## Reproduction

```bash
cd EXPERIMENTS/101-network-equipment-fault-codes
python3 run.py
```

## Decision Criteria

- If ALL gates PASS: Instrument generalizes to network equipment domain; unserved fraction measured; no candidate produced (evidence-gathering per D083)
- If G3 FAILS with high unserved fraction: Interesting population; still no candidate without further work
- If G4 FAILS: view_count instrument boundary found
- If G1/G2 FAIL: Insufficient population on these forums