<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E098 — Discrimination Test for Aviation Maintenance Fault Code Instrument

## Experiment: E098 — Fresh Observation in Aviation Maintenance Fault Codes

### Discrimination Test Design (per D088, D095)

**Requirement**: Before any population measurement, the instrument must pass a discrimination test on labels known by construction.

**Instrument**: `aviation_fault_classifier` — classifies a fault/error query as `served` or `unserved` based on Aviation Stack Exchange metadata:
- `view_count` — independent arrivals at the need (validated by E088 at 100% on Stack Exchange)
- `answer_count` — community responses
- `accepted_answer` — accepted solution exists
- `fault_code_specific` — specific fault code mentioned in title (vs. generic description)

**Discrimination Test Probes (30 total, labels known by construction)**:

### Known-Served Probes (15) — Entities with abundant public documentation/solutions

| # | Probe Query | Domain | Expected | Rationale |
|---|-------------|--------|----------|-----------|
| S1 | "Wing Loop Fault A320" | Aviation | `served` | Specific A320 fault code, manufacturer documentation exists |
| S2 | "FWC 1+2 FAULT A320" | Aviation | `served` | Specific Airbus fault, known procedure |
| S3 | "ECAM warning A320" | Aviation | `served` | Standard Airbus system, well documented |
| S4 | "magneto failure procedure" | Aviation | `served` | Standard piston engine procedure |
| S5 | "engine failure turnback" | Aviation | `served` | Standard emergency procedure, widely taught |
| S6 | "pitot static blockage detection" | Aviation | `served` | Standard instrument procedure |
| S7 | "stall warning system AOA vane" | Aviation | `served` | Standard system design, documented |
| S8 | "ADIRU failure GPWS" | Aviation | `served` | Known A330/A340 system interaction |
| S9 | "landing gear failure extension" | Aviation | `served` | Standard emergency procedure |
| S10 | "MCAS AOA sensor disagreement" | Aviation | `served` | 737 MAX system, extensively documented post-accidents |
| S11 | "auto-pilot disengage warning" | Aviation | `served` | Standard avionics alert, documented |
| S12 | "Control Law Degradation Airbus" | Aviation | `served` | Airbus flight control law, documented |
| S13 | "FADEC diagnostics protocol" | Aviation | `served` | Industry standard, documented |
| S14 | "EICAS system details" | Aviation | `served` | Standard Boeing system, documented |
| S15 | "electrical failure fly-by-wire" | Aviation | `served` | Standard Airbus design, documented |

### Known-Unserved Probes (15) — Entities that do not exist / cannot be served

| # | Probe Query | Domain | Expected | Rationale |
|---|-------------|--------|----------|-----------|
| U1 | "QuantumFlux avionics error 0xDEADBEEF" | Synthetic | `unserved` | Fictional brand, impossible code |
| U2 | "HyperDrive flight computer fault 99999" | Synthetic | `unserved` | Fictional product |
| U3 | "NeuralLink aircraft system error XYZ-123" | Synthetic | `unserved` | Wrong domain (BCI) |
| U4 | "FluxCapacitor avionics timeout 8888" | Synthetic | `unserved` | Fictional (Back to the Future) |
| U5 | "WarpCore engine breach code 1701" | Synthetic | `unserved` | Star Trek reference |
| U6 | "Dilithium crystal fuel fault 0xFF" | Synthetic | `unserved` | Fictional |
| U7 | "Heisenberg compensator nav error 42" | Synthetic | `unserved` | Fictional |
| U8 | "Transporter buffer overflow 666" | Synthetic | `unserved` | Fictional |
| U9 | "Holodeck safety protocol violation" | Synthetic | `unserved` | Fictional |
| U10 | "Replicator pattern buffer error" | Synthetic | `unserved` | Fictional |
| U11 | "Vintage 1960s Concorde fault code 999" | Real but obsolete | `unserved` | Concorde retired 2003, no active support |
| U12 | "Discontinued Lockheed L-1011 error 0xFFFF" | Real but obsolete | `unserved` | L-1011 production ended 1984, no vendor support |
| U13 | "Obsolete Boeing 727 fault code 777" | Real but obsolete | `unserved` | 727 retired from commercial service |
| U14 | "Retired DC-10 hydraulic error 1234" | Real but obsolete | `unserved` | DC-10 retired, no active community |
| U15 | "Legacy Fokker F28 avionics fault 999" | Real but obsolete | `unserved` | F28 1960s design, no support |

### Discrimination Test Gate Criteria

| Gate | Criterion | Threshold | Kill Condition |
|------|-----------|-----------|----------------|
| G1 | False Positive Rate (known-unserved classified as `served`) | < 0.10 (10%) | **FAIL → instrument invalid, redesign** |
| G2 | True Positive Rate (known-served classified as `served`) | > 0.70 (70%) | FAIL → instrument lacks sensitivity |
| G3 | False Negative Rate (known-served classified as `unserved`) | < 0.30 (30%) | FAIL → instrument too conservative |

**Pass Condition**: G1 PASS (primary) AND (G2 PASS OR G3 PASS)

**Note**: Thresholds apply to point estimates. Wilson 95% CIs are reported for context.

### Test Execution

1. For each probe, search Aviation Stack Exchange using the Stack Exchange API
2. Record: `view_count`, `answer_count`, `accepted_answer`, `fault_code_specific`
3. Apply classifier logic
4. Compare against known labels
5. Compute rates with Wilson 95% CI

### Instrument Logic

```
aviation_fault_classifier(api_result):
    view_count = api_result.view_count
    answer_count = api_result.answer_count
    accepted = api_result.accepted_answer_id is not None
    fault_code_specific = has_specific_fault_code(api_result.title)
    
    # High confidence served: accepted answer + specific fault code
    if accepted and fault_code_specific and view_count > 0:
        return "served"
    # Community served: answers + specific fault code + decent engagement
    elif answer_count > 0 and fault_code_specific and view_count > 100:
        return "served"
    # High interest unserved: many views, no answers, specific fault code
    elif view_count > 500 and answer_count == 0 and fault_code_specific:
        return "unserved"
    # Low engagement unserved
    elif view_count < 10 and answer_count == 0:
        return "unserved"
    else:
        return "unserved"  # default conservative

has_specific_fault_code(title):
    # Patterns for aviation fault codes
    patterns = [
        r'fault\s+code',
        r'error\s+code',
        r'warning\s+\w+',
        r'\b[A-Z]{2,}\d+\s+FAULT\b',  # FWC 1+2 FAULT
        r'\bECAM\b', r'\bEICAS\b', r'\bMCAS\b', r'\bADIRU\b',
        r'\bFADEC\b', r'\bGPWS\b', r'\bTCAS\b', r'\bEGPWS\b',
        r'\b[A-Z]{3,}\s+\d+\s+FAULT\b',
        r'\b[A-Z]{2,}\d+\s+FAULT\b',
    ]
    return any(re.search(p, title, re.IGNORECASE) for p in patterns)
```

### Reachable Success Region (per D088)

The gate's passing region must contain non-vacuous cases. We enumerate:
- Minimum 5 known-served probes must be reachable (have search results with view_count > 0)
- Maximum 2 known-unserved probes may return search results (ads/spam)
- The classifier must not rely on a single feature that correlates with spam

---

## Next Action

Implement `discrimination_test.py` that:
1. Searches Aviation Stack Exchange API for each probe
2. Extracts view_count, answer_count, accepted_answer_id, fault_code_specific
3. Applies classifier
4. Reports G1/G2/G3 with CIs
5. Halts if G1 FAIL (per D095: seven previous sessions failed this)