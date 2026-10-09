# Experiment 082: Microcontroller Fault Codes Fresh Observation

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

Fresh observation in the microcontroller fault/exception codes domain to discover whether a concentrated, structured problem population exists that could support a computational tool.

## Documents

| Document | Purpose |
|---|---|
| [`PROTOCOL.md`](PROTOCOL.md) | Predeclared protocol with kill gates |
| [`CLASSIFICATION_RULES.md`](CLASSIFICATION_RULES.md) | Classification criteria for fault types and root cause specificity |
| [`fetch.py`](fetch.py) | Data acquisition from electronics.stackexchange.com API (full version) |
| [`analyze_preliminary.py`](analyze_preliminary.py) | Analysis on title+tag data only (no answer data needed) |
| [`raw/questions_raw.json`](raw/questions_raw.json) | Raw questions from API (exempt from line cap) |
| [`analysis/preliminary_gate_results.json`](analysis/preliminary_gate_results.json) | Machine-readable gate results |
| [`analysis/title_candidates.json`](analysis/title_candidates.json) | Title candidates (exempt from line cap) |
| [`VERDICT.md`](VERDICT.md) | Gate evaluation results and decision |

## Status

**BLOCKED — Stack Exchange API completely inaccessible from this IP (Cloudflare 1015 / throttle 429).** No data could be fetched. G2/G3 show 0% / 0 families on empty data. G1/G4/G5 require answer data which also cannot be fetched.

## Hypothesis

Microcontroller fault/exception codes (ARM Cortex-M standardized faults + vendor-specific fault status registers) on specific MCU families form a concentrated, structured problem population where:
1. Standardized fault types appear repeatedly across MCU families
2. Embedded engineers diagnose root causes with specific register values and code fixes
3. Existing free tools don't provide cross-vendor fault code lookup with root causes
4. A computational tool mapping (fault type + MCU family + register values) → (root cause + fix) would fill a gap

## Kill Gates (Predeclared)

| Gate | Threshold | Result |
|------|-----------|--------|
| G1 Population | ≥ 200 structured cases | BLOCKED (no answer data) |
| G2 Fault concentration | Top 10 fault types cover ≥ 30% of cases | BLOCKED (no data) |
| G3 MCU coverage | ≥ 10 distinct MCU families in top 10 fault types | BLOCKED (no data) |
| G4 Root cause specificity | ≥ 60% name specific root cause | BLOCKED (no answer data) |
| G5 Incumbent gap | No free tool covers ≥ 50% of top 10 fault types | PENDING (manual) |

## Key Blocker

**Stack Exchange API completely blocked from this VM's IP** — both the public API (api.stackexchange.com) and SEDE (data.stackexchange.com) return Cloudflare challenges (error 1015) or throttle violations (429). No requests succeed.

This is the same class of blocker that affected E079 (automotive OBD2), but more severe: E079 retrieved 10,251 questions before throttle; E082 retrieves 0.

## Path Forward

1. **Obtain Stack Exchange API key** — increases quota from 300 to 10,000 req/day and may bypass IP-based throttling
2. **Use Stack Exchange data dump** — available via archive.org (quarterly dumps, ~50GB for all sites, electronics.stackexchange.com subset smaller)
3. **Run from different IP** — if another VM with different IP is available
4. **Alternative data sources** — embedded forums (EEVblog, embeddedrelated.com), vendor forums (STCommunity, ESP32 forum, etc.), but these lack structured view_count and tags

## Reproduce

```bash
# Preliminary analysis (title+tags only, no API calls)
python3 analyze_preliminary.py

# Full fetch (requires API key or unblocked IP)
python3 fetch.py
python3 analyze.py  # to be created when answer data available
```