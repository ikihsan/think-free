# Discrimination Test Harness

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

## Manual Discrimination Test for MrPLC/MedWrench Instrument

Since programmatic search is blocked (403), this test will be executed manually using the forum listing pages and direct thread access. The instrument uses features available on forum listings: `view_count`, `reply_count`, `error_code_in_title`.

### Instrument Definition

```
fault_need_classifier(forum_listing_entry):
    error_code_present = has_specific_error_code(title)
    vendor_acknowledged = False  # requires thread access, default False
    
    if error_code_present and vendor_acknowledged:
        return "served"
    elif view_count > 100 and reply_count > 0 and error_code_present:
        return "served"
    elif view_count > 500 and reply_count == 0 and error_code_present:
        return "unserved"
    elif view_count < 10 and reply_count == 0:
        return "unserved"
    else:
        return "unserved"

has_specific_error_code(title):
    # Patterns: "error XXX", "fault XXX", "code XXX", "0xXXXX", "E06", "10901"
    patterns = [
        r'error\s+\d+',
        r'fault\s+\d+',
        r'code\s+\d+',
        r'0x[0-9A-Fa-f]+',
        r'\bE\d{2,}\b',
        r'\b\d{4,5}\b',  # 4-5 digit codes
    ]
    return any(re.search(p, title, re.IGNORECASE) for p in patterns)
```

### Discrimination Test Probes (Manual Execution)

For each probe, the tester will:
1. Navigate to the forum (MrPLC or MedWrench)
2. Search/browse for the probe term
3. Record: `view_count`, `reply_count`, `error_code_present` from the first matching result
4. Apply classifier
5. Record predicted vs. expected label

---

## Known-Served Probes on MrPLC (20)

| # | Probe | Expected | Forum Section | Manual Check |
|---|-------|----------|---------------|--------------|
| S1 | "Modbus exception code 03" | `served` | Other PLCs / General | ☐ |
| S2 | "EtherNet/IP connection timeout" | `served` | Allen Bradley | ☐ |
| S3 | "Siemens S7-1200 CPU fault" | `served` | Siemens | ☐ |
| S4 | "Allen Bradley fault code" | `served` | Allen Bradley | ☐ |
| S5 | "Mitsubishi MELSEC error" | `served` | Mitsubishi | ☐ |
| S6 | "Omron CJ2H CPU error" | `served` | Omron | ☐ |
| S7 | "PROFINET diagnostic" | `served` | Siemens | ☐ |
| S8 | "OPC UA Bad_ConnectionClosed" | `served` | Other PLCs | ☐ |
| S9 | "HART communication error" | `served` | Other PLCs | ☐ |
| S10 | "Profibus DP diagnostic" | `served` | Other PLCs | ☐ |
| S11 | "Micro800 fault" | `served` | Allen Bradley | ☐ |
| S12 | "ControlLogix fault" | `served` | Allen Bradley | ☐ |
| S13 | "CompactLogix error" | `served` | Allen Bradley | ☐ |
| S14 | "RSLogix 5000 error" | `served` | Allen Bradley | ☐ |
| S15 | "GX Works2 error" | `served` | Mitsubishi | ☐ |
| S16 | "Sysmac Studio error" | `served` | Omron | ☐ |
| S17 | "TIA Portal error" | `served` | Siemens | ☐ |
| S18 | "Studio 5000 error" | `served` | Allen Bradley | ☐ |
| S19 | "PLC analog input fluctuating" | `served` | Panasonic / General | ☐ |
| S20 | "HMI communication error" | `served` | HMI & SCADA | ☐ |

---

## Known-Unserved Probes on MrPLC (20)

| # | Probe | Expected | Rationale | Manual Check |
|---|-------|----------|-----------|--------------|
| U1 | "QuantumFlux PLC error" | `unserved` | Fictional brand | ☐ |
| U2 | "HyperDrive controller fault" | `unserved` | Fictional brand | ☐ |
| U3 | "NeuralLink PLC fault" | `unserved` | Wrong domain (BCI) | ☐ |
| U4 | "FluxCapacitor timeout" | `unserved` | Fictional | ☐ |
| U5 | "WarpCore breach code" | `unserved` | Fictional | ☐ |
| U6 | "Dilithium crystal fault" | `unserved` | Fictional | ☐ |
| U7 | "Heisenberg compensator error" | `unserved` | Fictional | ☐ |
| U8 | "Transporter buffer overflow" | `unserved` | Fictional | ☐ |
| U9 | "Holodeck safety protocol" | `unserved` | Fictional | ☐ |
| U10 | "Replicator pattern buffer" | `unserved` | Fictional | ☐ |
| U11 | "Allen Bradley 1774 fault" | `unserved` | Discontinued 1980s | ☐ |
| U12 | "GE Fanuc 90-30 error" | `unserved` | EOL 2010 | ☐ |
| U13 | "Modicon 984 error code" | `unserved` | 1980s series | ☐ |
| U14 | "Siemens S5-115U error" | `unserved` | EOL 2000s | ☐ |
| U15 | "Honeywell TDC 3000 fault" | `unserved` | 1980s DCS | ☐ |
| U16 | "Bristol Babcock 3300 error" | `unserved` | Obsolete RTU | ☐ |
| U17 | "Fisher ROC 800 fault" | `unserved` | Obsolete flow computer | ☐ |
| U18 | "Motorola MOSCAD error" | `unserved` | Obsolete RTU | ☐ |
| U19 | "Square D SY/MAX fault" | `unserved` | 1980s PLC | ☐ |
| U20 | "Texas Instruments 505 error" | `unserved` | 1980s PLC | ☐ |

---

## Known-Served Probes on MedWrench (10)

| # | Probe | Expected | Manual Check |
|---|-------|----------|--------------|
| MS1 | "Error 10901" | `served` | ☐ |
| MS2 | "Error E06" | `served` | ☐ |
| MS3 | "Service mode access" | `served` | ☐ |
| MS4 | "Patient cable test" | `served` | ☐ |
| MS5 | "Compact flash image" | `served` | ☐ |
| MS6 | "Fan part number" | `served` | ☐ |
| MS7 | "Screech noise" | `served` | ☐ |
| MS8 | "Electrical diagram" | `served` | ☐ |
| MS9 | "Service manual" | `served` | ☐ |
| MS10 | "QC procedure" | `served` | ☐ |

---

## Known-Unserved Probes on MedWrench (10)

| # | Probe | Expected | Rationale | Manual Check |
|---|-------|----------|-----------|--------------|
| MU1 | "QuantumFlux medical error" | `unserved` | Fictional | ☐ |
| MU2 | "HyperDrive device fault" | `unserved` | Fictional | ☐ |
| MU3 | "NeuralLink medical error" | `unserved` | Wrong domain | ☐ |
| MU4 | "FluxCapacitor medical timeout" | `unserved` | Fictional | ☐ |
| MU5 | "WarpCore medical breach" | `unserved` | Fictional | ☐ |
| MU6 | "Discontinued Picker X-ray error" | `unserved` | 1980s, defunct | ☐ |
| MU7 | "Obsolete Technicare CT fault" | `unserved` | 1980s, defunct | ☐ |
| MU8 | "Retired GE 8800 CT error" | `unserved` | 1970s CT | ☐ |
| MU9 | "Vintage Siemens Somatom AR fault" | `unserved` | 1980s CT | ☐ |
| MU10 | "Discontinued HP Viridia error" | `unserved` | 1990s monitor | ☐ |

---

## Test Execution Checklist

- [ ] Execute S1-S20 on MrPLC (browse relevant forum sections)
- [ ] Execute U1-U20 on MrPLC (search/browse)
- [ ] Execute MS1-MS10 on MedWrench
- [ ] Execute MU1-MU10 on MedWrench
- [ ] Compute G1 (FPR on unserved), G2 (TPR on served), G3 (FNR on served)
- [ ] Record Wilson 95% CIs
- [ ] **GATE**: G1 < 0.10 required to proceed

---

## Results Recording

| Probe | Forum | View Count | Reply Count | Error Code in Title | Predicted | Expected | Match |
|-------|-------|------------|-------------|---------------------|-----------|----------|-------|
| S1 | | | | | | | |
| S2 | | | | | | | |
| U1 | | | | | | | |
| ... | | | | | | | |

---

## Next Action

If G1 PASS (< 10% FPR): Proceed to population measurement on practitioner rows from OBSERVATIONS.md
If G1 FAIL: Redesign instrument (add features, adjust thresholds) and retest