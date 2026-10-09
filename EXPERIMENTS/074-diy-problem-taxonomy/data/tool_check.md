<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Tool Check — Existing Computational Tools for Top Problem Types

## PROC (Procedure/Method) — 27.8% of questions, 1.1% structured
**No single computational tool** covers the breadth of "how do I" questions.
- YouTube, manufacturer manuals, forum threads serve this population
- No general-purpose procedure generator exists
- Specific tools exist for narrow tasks (e.g., voltage drop calculators) but not for general procedures

## DIAG (Appliance/Equipment Diagnosis) — 24.3%, 4.9% structured
**Existing tools:**
- Manufacturer service manuals (often behind paywalls or login)
- Appliance error code databases: RepairClinic, PartSelect, AppliancePartsPros — cover major brands but not comprehensive
- HVAC diagnostic apps: MeasureQuick, HVAC Buddy — professional tools, not DIY-friendly
- Vehicle OBD2 scanners — automotive only
- **Gap**: No unified, free, DIY-accessible diagnostic tool that takes error code + symptoms → root cause across appliance categories

## CODE (Code Compliance) — 5.5%, 8.1% structured
**Existing tools:**
- NEC/NFPA free access (read-only, no search API)
- Local jurisdiction amendments vary widely
- UpCodes (paid), CodeCheck (paid) — professional tools
- **Gap**: No free, searchable code compliance checker with jurisdiction awareness

## CALC (Engineering Calculation) — 4.1%, 3.6% structured
**Existing tools:**
- Voltage drop calculators: many free web calculators (Southwire, Calculator.net, etc.)
- Pipe sizing calculators: various free tools
- Beam/joist span calculators: AWC, various engineering sites
- Concrete calculators: many free tools
- **Status**: Well-served by free web calculators for specific calculations

## MATL (Material Selection) — 6.8%, 0% structured
**Existing tools:**
- Manufacturer selection guides
- Home Depot/Lowes product filters
- **Gap**: No computational tool that takes requirements → specific product recommendation

## Summary
| Type | Population | Structured | Existing Tools | Gap? |
|------|------------|------------|----------------|------|
| PROC | 27.8% | 1.1% | Videos, manuals, forums | Broad, no |
| DIAG | 24.3% | 4.9% | Brand-specific databases | Yes, cross-brand |
| CODE | 5.5% | 8.1% | Paid pro tools | Yes, free/jurisdiction |
| CALC | 4.1% | 3.6% | Many free calculators | No |
| MATL | 6.8% | 0% | Catalog filters | Yes, requirement-based |

**Conclusion**: DIAG and CODE have genuine tool gaps, but neither meets the population threshold (G1) AND structure threshold (G2) simultaneously. The domain does not yield a candidate under the declared protocol.