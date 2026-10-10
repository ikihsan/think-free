# Fresh Observation: Structured Fault/Error-Code Domains

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

## Session 2026-10-10-006

**Goal**: Fresh observation in structured fault/error-code domains (industrial PLC, medical device) — read actual practitioner rows by hand before any classifier.

**Per STATE.md D083, D095**: The next session must start from fresh observation in a new domain. The instrument must pass a discrimination test before any population row is read. Seven previous sessions (E081-E087) and a committed synthesis rested on a classifier that never separated known-served from known-unserved cases (F109, D095).

---

## Domain 1: Industrial PLC — MrPLC.com

**Venue**: MrPLC.com — active practitioner forum (69,099 members, 39.7k topics, 193.6k posts)
**Access**: Publicly readable forum listings and threads (no authentication required for reading)
**View counts**: Available on forum listing pages (validated by E088 as 100% present)

### Practitioner Rows Collected (by hand from forum listings)

| # | Forum | Topic Title | Author | Date | Replies | Views | Error/Fault Codes | Notes |
|---|-------|-------------|--------|------|---------|-------|-------------------|-------|
| 1 | Allen Bradley | GuardLogix fault 125/120 on 1734-IE4S | Maf | May 19, 2014 | — | — | **125, 120** | Specific fault codes on 1734-IE4S analog module; Rockwell unsure of cause; practitioner seeks root cause after module replacement failed to prevent recurrence |
| 2 | Mitsubishi | Timer not counting | Megaraun | Oct 1 | 6 | 204 | (behavioral fault) | Timer instruction not incrementing |
| 3 | Mitsubishi | Gx Work 2 software error "System stop failed. Please restart Windows." | phamphong1804 | Mar 6 | 3 | **1,600** | **"System stop failed"** | Software launch error; practitioner doesn't know reason |
| 4 | Mitsubishi | Mitsubishi iQ-R PLC communication error - error codes 1134, C0B2, and C709 | Akseer | Aug 17 | 11 | 688 | **1134, C0B2, C709** | **Multiple specific hex/decimal error codes**; communication error on iQ-R series |
| 5 | Siemens | HMI TP1200 Comfort Panel error [Application HMIRTM.EXE encountered a serious error and must shutdown.] | Hati | Sep 9 | — | — | **HMIRTM.EXE crash** | Specific application crash error message |
| 6 | Panasonic | Why is my PLC analog input fluctuating intermittently? | Strategi Automation | Feb 27 | — | — | (analog signal fault) | Intermittent analog input fluctuation |
| 7 | Allen Bradley | Studio 5000 Logix Designer version 38: Install Error 1606 and Error 1722 | Chris Elston | Oct 1 | 1 | 123 | **1606, 1722** | Windows installer error codes during software installation |
| 8 | Omron | Error -10 - No system program | Asif128935 | Mar 29 | — | — | **-10** | Specific error code; "No system program" |
| 9 | Omron | NX1P2 and 3rd Party HMI timeout errors | Pauljm. | Jan 12 | 5 | 1,300 | **timeout** | Communication timeout errors with 3rd party HMI |

### Observations from MrPLC

1. **Specific error/fault codes are prevalent**: Practitioners cite exact codes (125, 120, 1134, C0B2, C709, -10, 1606, 1722, HMIRTM.EXE)
2. **Vendor support gaps**: Row 1 explicitly states "Spoke to Rockwell and they were unsure as to the cause" — vendor doesn't know
3. **Recurrence after replacement**: Row 1 shows same fault on different module — suggests systemic issue, not hardware defect
4. **High view counts on error threads**: Row 3 has 1,600 views for a software error; Row 4 has 688 views for communication errors
5. **Cross-vendor, cross-platform**: Errors span Allen Bradley, Mitsubishi, Siemens, Panasonic, Omron
6. **Practitioners are technicians/engineers**: Language indicates hands-on commissioning, factory testing, site work

---

## Domain 2: Medical Device — MedWrench.com

**Venue**: MedWrench.com — "The Medical Product Support Network" for biomedical equipment technicians (BMETs)
**Access**: Publicly readable forum listings and threads
**View counts**: Not directly visible on listing pages (need to verify per thread)

### Practitioner Rows Collected (by hand from forum listings)

| # | Topic Title | Equipment | Category | Answers | Error/Fault Codes | Notes |
|---|-------------|-----------|----------|---------|-------------------|-------|
| 1 | Error 10901 with FlashIIP station | Fuji FCR Carbon X (CR-IR 357) | Radiography | 8 | **10901** | Specific error code on computed radiography system |
| 2 | How to access Service Mode | Philips X-ray Dura Diagnost M-Cabinet CXA Pro 80 KW | R/F Systems | 0 | (service mode access) | Practitioner needs service manual/mode access |
| 3 | troubleshooting how to test the patient cable | Burdick Atria 3100 | Electrocardiograph (EKG/ECG) | 3 | (cable test procedure) | Procedural troubleshooting |
| 4 | Image file for Compact flash which holds the unit | Aloka Prosound 2 | Ultrasound Systems | 13 | (firmware/image) | Needs firmware/image file for CF card |
| 5 | Show error E06 and led INHIBIT light | Genoray RG-600 mammo | Mammography | 0 | **E06, INHIBIT** | Specific error code + LED indicator |
| 6 | REPLACEMENT FAN PART NUMBER | Blickman 7922TG | Warming Cabinet | 2 | (part number) | Parts identification request |
| 7 | during processing loud screech audible | ACP2150 | Freezing unit | 1 | (mechanical noise) | Audible fault symptom |

### Observations from MedWrench

1. **Specific error codes**: E06, 10901 — manufacturer-specific codes
2. **Service manual/mode access**: Multiple requests for service documentation (Rows 2, 4)
3. **Parts identification**: Row 6 asks for replacement part number
4. **Multi-modal faults**: Error codes + LED indicators + audible symptoms
5. **BMET practitioners**: Biomedical equipment technicians — different population than PLC techs
6. **Regulatory context**: Medical devices have FDA/service manual restrictions

---

## Cross-Domain Patterns

| Pattern | PLC (MrPLC) | Medical (MedWrench) |
|---------|-------------|---------------------|
| Specific error codes | Yes (125, 1134, C0B2, -10, etc.) | Yes (E06, 10901) |
| Vendor knowledge gaps | Explicit (Rockwell unsure) | Implied (service manual requests) |
| Recurrence after fix | Yes (Row 1) | Not observed in sample |
| View counts available | Yes (100% on listings) | Need verification |
| Practitioner role | Controls technicians, commissioning engineers | BMETs, clinical engineers |
| Equipment specificity | High (module + firmware + config) | High (model + serial + firmware) |
| Regulatory constraints | Low | High (FDA, service manuals restricted) |

---

## Instrument Design Requirements (per D088, D095)

Before measuring any population, the instrument must:

1. **Name the instrument and call that instrument rather than a local copy**
2. **Pass a discrimination test on labels known by construction** — test on:
   - Known-served cases (entities with abundant public documentation/solutions)
   - Known-unserved cases (entities that do not exist / cannot be served)
3. **Enumerate what its gate's passing value can be made of** — define the reachable success region

### Candidate Instrument: `view_count` + `reply_count` + `error_code_specificity`

**Hypothesis**: Threads with (high view_count AND high reply_count AND specific error codes) indicate **served** needs (community has answers). Threads with (high view_count AND low reply_count AND specific error codes) indicate **unserved** needs (many arrive, few answer).

**Discrimination test probes (labels known by construction)**:

| Probe Type | Examples | Expected Label | Rationale |
|------------|----------|----------------|-----------|
| Known-served (abundant docs) | "Python ImportError", "Git merge conflict", "Docker container exited" | `served` | Vast public documentation, Stack Overflow answers |
| Known-unserved (nonexistent) | "QuantumFlux error 0xDEADBEEF", "HyperDrive fault 99999", "NeuralLink error XYZ-123" | `unserved` | Entities don't exist; any "served" classification is false positive |
| Known-unserved (real but niche) | "Vintage 1980s PLC error", "Discontinued medical device fault" | `unserved` | No active community, no vendor support |

---

## Next Steps

1. **Build discrimination test harness** — fetch view/reply counts for probe set
2. **Run discrimination test** — must achieve <10% false positive rate on known-unserved
3. **If gate passes**, apply instrument to practitioner rows above
4. **If gate fails**, redesign instrument (per D095: "must not start from classify_served over Bing in an eighth domain")

---

## Evidence Links

- MrPLC main forums: https://www.mrplc.com/forums/
- MrPLC Mitsubishi forum: https://www.mrplc.com/forums/forum/15-mitsubishi/
- MrPLC Omron forum: https://www.mrplc.com/forums/forum/17-omron/
- MrPLC Modicon forum: https://www.mrplc.com/forums/forum/20-modicon-telemecanique-schneider-electric/
- MedWrench forums: https://www.medwrench.com/forums/

All observations are **observed** (directly read from public forum listings).