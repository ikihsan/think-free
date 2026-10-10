# Discrimination Test Protocol for Structured Fault Domain Instrument

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

## Experiment: E090 — Fresh Observation in Structured Fault/Error-Code Domains

### Discrimination Test Design (per D088, D095)

**Requirement**: Before any population measurement, the instrument must pass a discrimination test on labels known by construction.

**Instrument**: `fault_need_classifier` — classifies a fault/error query as `served` or `unserved` based on:
- `view_count` — independent arrivals at the need (validated by E088 at 100% on Discourse)
- `reply_count` — community responses
- `error_code_present` — specific fault code mentioned (vs. generic description)
- `vendor_acknowledged` — vendor documentation/solution exists

**Discrimination Test Probes (40 total, labels known by construction)**:

### Known-Served Probes (20) — Entities with abundant public documentation

| # | Probe Query | Domain | Expected | Rationale |
|---|-------------|--------|----------|-----------|
| 1 | "Python ImportError: No module named 'requests'" | Software | `served` | Millions of Stack Overflow answers |
| 2 | "Git merge conflict: both modified" | Software | `served` | Core Git documentation + SO |
| 3 | "Docker container exited with code 137" | Software | `served` | OOM killer, well documented |
| 4 | "React useEffect infinite loop" | Software | `served` | Common React pattern, many answers |
| 5 | "PostgreSQL deadlock detected" | Software | `served` | Standard DB error, documented |
| 6 | "Kubernetes CrashLoopBackOff" | Software | `served` | Core K8s troubleshooting |
| 7 | "AWS Lambda timeout after 30 seconds" | Software | `served` | AWS docs + community |
| 8 | "TypeError: cannot read property 'map' of undefined" | Software | `served` | Universal JS error |
| 9 | "SSL certificate verify failed" | Software | `served` | Universal TLS error |
| 10 | "npm ERR! code EACCES" | Software | `served` | Common npm permission issue |
| 11 | "Siemens S7-1200 CPU fault 16#8001" | PLC | `served` | Siemens documentation + forums |
| 12 | "Allen Bradley Micro800 fault code 0x0010" | PLC | `served` | Rockwell knowledgebase |
| 13 | "Modbus exception code 0x03" | PLC | `served` | Protocol standard, documented |
| 14 | "PROFINET diagnostics 0x8001" | PLC | `served` | Standard industrial protocol |
| 15 | "OPC UA Bad_ConnectionClosed" | PLC | `served` | OPC Foundation standard |
| 16 | "Mitsubishi MELSEC Q error 1001" | PLC | `served` | Mitsubishi manuals |
| 17 | "Omron CJ2H CPU error 0x80" | PLC | `served` | Omron documentation |
| 18 | "EtherNet/IP connection timeout" | PLC | `served` | ODVA standard |
| 19 | "HART communication error 9" | PLC | `served` | HART protocol standard |
| 20 | "Profibus DP diagnostic byte 1" | PLC | `served` | Profibus standard |

### Known-Unserved Probes (20) — Entities that do not exist / cannot be served

| # | Probe Query | Domain | Expected | Rationale |
|---|-------------|--------|----------|-----------|
| 1 | "QuantumFlux error 0xDEADBEEF" | Synthetic | `unserved` | "QuantumFlux" doesn't exist as PLC/medical product |
| 2 | "HyperDrive fault 99999" | Synthetic | `unserved` | "HyperDrive" not a real industrial/medical product |
| 3 | "NeuralLink error XYZ-123" | Synthetic | `unserved` | NeuralLink is BCI, not PLC/medical device |
| 4 | "FluxCapacitor timeout 8888" | Synthetic | `unserved` | Fictional (Back to the Future) |
| 5 | "WarpCore breach code 1701" | Synthetic | `unserved` | Star Trek reference, not real product |
| 6 | "Dilithium crystal fault 0xFF" | Synthetic | `unserved` | Fictional |
| 7 | "Heisenberg compensator error 42" | Synthetic | `unserved` | Star Trek, fictional |
| 8 | "Transporter buffer overflow 666" | Synthetic | `unserved` | Fictional |
| 9 | "Holodeck safety protocol violation" | Synthetic | `unserved` | Fictional |
| 10 | "Replicator pattern buffer error" | Synthetic | `unserved` | Fictional |
| 11 | "Vintage 1970s Allen Bradley 1774 fault 999" | Real but obsolete | `unserved` | 1774 series discontinued 1980s, no active support |
| 12 | "Discontinued GE Fanuc 90-30 error 0xFFFF" | Real but obsolete | `unserved` | GE Fanuc 90-30 EOL 2010, no vendor support |
| 13 | "Obsolete Modicon 984 error code 777" | Real but obsolete | `unserved` | 984 series 1980s, no active community |
| 14 | "Retired Siemens S5-115U error 1234" | Real but obsolete | `unserved` | S5 series EOL 2000s |
| 15 | "Legacy Honeywell TDC 3000 fault 999" | Real but obsolete | `unserved` | TDC 3000 1980s DCS, no support |
| 16 | "Discontinued Philips Brilliance CT error 9999" | Medical obsolete | `unserved` | 1990s CT scanner, no service manuals |
| 17 | "Retired GE Signa MRI fault 8888" | Medical obsolete | `unserved` | 1990s MRI, no vendor support |
| 18 | "Obsolete Siemens Somatom AR error 7777" | Medical obsolete | `unserved` | 1980s CT, no parts/service |
| 19 | "Vintage HP/Agilent Viridia monitor error 666" | Medical obsolete | `unserved` | 1990s patient monitor |
| 20 | "Discontinued Draeger Fabius GS anesthesia error 555" | Medical obsolete | `unserved` | Old anesthesia machine |

### Discrimination Test Gate Criteria

| Gate | Criterion | Threshold | Kill Condition |
|------|-----------|-----------|----------------|
| G1 | False Positive Rate (known-unserved classified as `served`) | < 0.10 (10%) | **FAIL → instrument invalid, redesign** |
| G2 | True Positive Rate (known-served classified as `served`) | > 0.70 (70%) | FAIL → instrument lacks sensitivity |
| G3 | False Negative Rate (known-served classified as `unserved`) | < 0.30 (30%) | FAIL → instrument too conservative |

**Pass Condition**: G1 PASS (primary) AND (G2 PASS OR G3 PASS)

### Test Execution

1. For each probe, search the target venue(s) using the venue's native search
2. Record: `view_count`, `reply_count`, `error_code_present`, `vendor_acknowledged`
3. Apply classifier logic
4. Compare against known labels
5. Compute rates with Wilson 95% CI

### Instrument Logic (to be implemented)

```
IF error_code_present AND vendor_acknowledged:
    CLASSIFY = "served"  (high confidence)
ELIF view_count > 100 AND reply_count > 0 AND error_code_present:
    CLASSIFY = "served"  (community served)
ELIF view_count > 500 AND reply_count == 0 AND error_code_present:
    CLASSIFY = "unserved"  (high interest, no answers)
ELIF view_count < 10 AND reply_count == 0:
    CLASSIFY = "unserved"  (no interest, no answers)
ELSE:
    CLASSIFY = "unserved"  (default conservative)
```

### Reachable Success Region (per D088)

The gate's passing region must contain non-vacuous cases. We enumerate:
- Minimum 5 known-served probes must be reachable (have search results)
- Maximum 2 known-unserved probes may return search results (ads/spam)
- The classifier must not rely on a single feature that correlates with spam

---

## Next Action

Implement `discrimination_test.py` that:
1. Searches MrPLC and/or MedWrench for each probe
2. Extracts view_count, reply_count, error_code_present
3. Applies classifier
4. Reports G1/G2/G3 with CIs
5. Halts if G1 FAIL (per D095: seven previous sessions failed this)