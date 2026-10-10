#!/usr/bin/env python3
"""
Population Measurement using validated fault_need_classifier_v3
Applies the instrument that passed discrimination test to practitioner rows
"""

import re
from dataclasses import dataclass
from typing import List
from math import sqrt

@dataclass
class PractitionerRow:
    id: str
    domain: str  # 'PLC' or 'Medical'
    forum: str
    title: str
    replies: int
    views: int
    error_codes: str
    notes: str

def has_fault_language(title: str) -> bool:
    """Check if title contains fault/error/problem language (same as v3 test)."""
    strong_patterns = [
        r'error\s+\d+',
        r'fault\s+\d+',
        r'code\s+\d+',
        r'0x[0-9A-Fa-f]+',
        r'\bE\d{2,}\b',
        r'\b\d{4,5}\b',
        r'fault\s+code',
        r'error\s+code',
        r'exception\s+\d+',
        r'alarm\s+\d+',
    ]
    
    moderate_patterns = [
        r'\berror\b',
        r'\bfault\b',
        r'\bproblem\b',
        r'\bissue\b',
        r'\bfail\b',
        r'\bcrash\b',
        r'\btimeout\b',
        r'\bdiagnostic\b',
        r'\btroubleshoot\b',
        r'\bnot\s+working\b',
        r'\bstopped\s+working\b',
        r'\bscaling\s+issue\b',
        r'\btiming\b',
        r'\bcommunication\s+error\b',
        r'\bconnection\s+error\b',
        r'\bnetwork\s+error\b',
        r'\bconfig\b',
        r'\bsetup\b',
        r'\bmigration\b',
        r'\bconvert\b',
    ]
    
    title_lower = title.lower()
    
    if any(re.search(p, title_lower) for p in strong_patterns):
        return True
    if any(re.search(p, title_lower) for p in moderate_patterns):
        return True
    return False

def fault_need_classifier_v3(entry: PractitionerRow) -> str:
    """Validated classifier from discrimination test."""
    fault_language = has_fault_language(entry.title)
    
    if fault_language and entry.replies > 0:
        return "served"
    if entry.views > 200 and entry.replies > 0:
        return "served"
    if entry.views > 1000 and entry.replies == 0 and fault_language:
        return "unserved"
    if entry.views < 50 and entry.replies == 0:
        return "unserved"
    return "unserved"

def wilson_ci(p: float, n: int, z: float = 1.96) -> tuple:
    if n == 0:
        return (0.0, 1.0)
    denominator = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denominator
    half = z * sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator
    return (max(0.0, centre - half), min(1.0, centre + half))

# Practitioner rows from OBSERVATIONS.md (MrPLC)
plc_rows = [
    PractitionerRow(
        id="PLC-1",
        domain="PLC",
        forum="Allen Bradley",
        title="GuardLogix fault 125/120 on 1734-IE4S",
        replies=0,  # from listing, not thread
        views=0,    # not on listing
        error_codes="125, 120",
        notes="Rockwell unsure of cause; recurrence after module replacement"
    ),
    PractitionerRow(
        id="PLC-2",
        domain="PLC",
        forum="Mitsubishi",
        title="Timer not counting",
        replies=6,
        views=204,
        error_codes="(behavioral fault)",
        notes="Timer instruction not incrementing"
    ),
    PractitionerRow(
        id="PLC-3",
        domain="PLC",
        forum="Mitsubishi",
        title="Gx Work 2 software error System stop failed Please restart Windows",
        replies=3,
        views=1600,
        error_codes='"System stop failed"',
        notes="Software launch error; practitioner doesn't know reason"
    ),
    PractitionerRow(
        id="PLC-4",
        domain="PLC",
        forum="Mitsubishi",
        title="Mitsubishi iQ-R PLC communication error error codes 1134 C0B2 and C709",
        replies=11,
        views=688,
        error_codes="1134, C0B2, C709",
        notes="Multiple specific hex/decimal error codes"
    ),
    PractitionerRow(
        id="PLC-5",
        domain="PLC",
        forum="Siemens",
        title="HMI TP1200 Comfort Panel error Application HMIRTM EXE encountered a serious error and must shutdown",
        replies=6,
        views=472,
        error_codes="HMIRTM.EXE crash",
        notes="Specific application crash error message"
    ),
    PractitionerRow(
        id="PLC-6",
        domain="PLC",
        forum="Panasonic",
        title="Why is my PLC analog input fluctuating intermittently",
        replies=0,
        views=0,
        error_codes="(analog signal fault)",
        notes="Intermittent analog input fluctuation"
    ),
    PractitionerRow(
        id="PLC-7",
        domain="PLC",
        forum="Allen Bradley",
        title="Studio 5000 Logix Designer version 38 Install Error 1606 and Error 1722",
        replies=1,
        views=123,
        error_codes="1606, 1722",
        notes="Windows installer error codes during software installation"
    ),
    PractitionerRow(
        id="PLC-8",
        domain="PLC",
        forum="Omron",
        title="Error -10 No system program",
        replies=0,
        views=0,
        error_codes="-10",
        notes="Specific error code; 'No system program'"
    ),
    PractitionerRow(
        id="PLC-9",
        domain="PLC",
        forum="Omron",
        title="NX1P2 and 3rd Party HMI timeout errors",
        replies=5,
        views=1300,
        error_codes="timeout",
        notes="Communication timeout errors with 3rd party HMI"
    ),
]

# Practitioner rows from MedWrench
medical_rows = [
    PractitionerRow(
        id="MED-1",
        domain="Medical",
        forum="MedWrench",
        title="Error 10901 with FlashIIP station",
        replies=8,
        views=0,  # not visible on listing
        error_codes="10901",
        notes="Specific error code on computed radiography system"
    ),
    PractitionerRow(
        id="MED-2",
        domain="Medical",
        forum="MedWrench",
        title="How to access Service Mode",
        replies=0,
        views=0,
        error_codes="(service mode access)",
        notes="Practitioner needs service manual/mode access"
    ),
    PractitionerRow(
        id="MED-3",
        domain="Medical",
        forum="MedWrench",
        title="troubleshooting how to test the patient cable",
        replies=3,
        views=0,
        error_codes="(cable test procedure)",
        notes="Procedural troubleshooting"
    ),
    PractitionerRow(
        id="MED-4",
        domain="Medical",
        forum="MedWrench",
        title="Image file for Compact flash which holds the unit",
        replies=13,
        views=0,
        error_codes="(firmware/image)",
        notes="Needs firmware/image file for CF card"
    ),
    PractitionerRow(
        id="MED-5",
        domain="Medical",
        forum="MedWrench",
        title="Show error E06 and led INHIBIT light",
        replies=0,
        views=0,
        error_codes="E06, INHIBIT",
        notes="Specific error code + LED indicator"
    ),
    PractitionerRow(
        id="MED-6",
        domain="Medical",
        forum="MedWrench",
        title="REPLACEMENT FAN PART NUMBER",
        replies=2,
        views=0,
        error_codes="(part number)",
        notes="Parts identification request"
    ),
    PractitionerRow(
        id="MED-7",
        domain="Medical",
        forum="MedWrench",
        title="during processing loud screech audible",
        replies=1,
        views=0,
        error_codes="(mechanical noise)",
        notes="Audible fault symptom"
    ),
]

def measure_population(rows: List[PractitionerRow], domain_name: str):
    print(f"\n{'='*80}")
    print(f"POPULATION MEASUREMENT: {domain_name} ({len(rows)} rows)")
    print(f"{'='*80}")
    
    served = []
    unserved = []
    
    for row in rows:
        classification = fault_need_classifier_v3(row)
        fault_lang = has_fault_language(row.title)
        
        if classification == "served":
            served.append(row)
        else:
            unserved.append(row)
        
        status = "✓ SERVED" if classification == "served" else "✗ UNSERVED"
        print(f"  {status} {row.id}: views={row.views}, replies={row.replies}, fault_lang={fault_lang}")
        print(f"       Title: {row.title[:70]}...")
        print(f"       Codes: {row.error_codes}")
        if row.notes:
            print(f"       Notes: {row.notes[:80]}...")
        print()
    
    total = len(rows)
    served_count = len(served)
    unserved_count = len(unserved)
    
    served_rate = served_count / total if total > 0 else 0
    unserved_rate = unserved_count / total if total > 0 else 0
    
    served_ci = wilson_ci(served_rate, total)
    unserved_ci = wilson_ci(unserved_rate, total)
    
    print(f"SUMMARY:")
    print(f"  Total: {total}")
    print(f"  Served: {served_count} ({served_rate:.1%})  CI95: [{served_ci[0]:.1%}, {served_ci[1]:.1%}]")
    print(f"  Unserved: {unserved_count} ({unserved_rate:.1%})  CI95: [{unserved_ci[0]:.1%}, {unserved_ci[1]:.1%}]")
    
    # High-interest unserved (high views, no replies, fault language)
    high_interest_unserved = [r for r in unserved if r.views > 500 and r.replies == 0 and has_fault_language(r.title)]
    print(f"  High-interest unserved (views>500, 0 replies, fault lang): {len(high_interest_unserved)}")
    for r in high_interest_unserved:
        print(f"    - {r.id}: {r.title[:60]}... (views={r.views})")
    
    return served, unserved

if __name__ == "__main__":
    print("=" * 80)
    print("POPULATION MEASUREMENT WITH VALIDATED INSTRUMENT")
    print("Instrument: fault_need_classifier_v3 (PASSED discrimination test)")
    print("=" * 80)
    
    # Measure PLC domain
    plc_served, plc_unserved = measure_population(plc_rows, "Industrial PLC (MrPLC)")
    
    # Measure Medical domain
    med_served, med_unserved = measure_population(medical_rows, "Medical Device (MedWrench)")
    
    # Combined
    all_rows = plc_rows + medical_rows
    all_served = plc_served + med_served
    all_unserved = plc_unserved + med_unserved
    
    print(f"\n{'='*80}")
    print("COMBINED SUMMARY")
    print(f"{'='*80}")
    total = len(all_rows)
    print(f"Total practitioner rows: {total}")
    print(f"  PLC: {len(plc_rows)} | Medical: {len(medical_rows)}")
    print(f"Classified as served: {len(all_served)} ({len(all_served)/total:.1%})")
    print(f"Classified as unserved: {len(all_unserved)} ({len(all_unserved)/total:.1%})")
    
    # Key findings
    print(f"\nKEY FINDINGS:")
    
    # Vendor knowledge gaps
    vendor_gaps = [r for r in all_rows if "vendor" in r.notes.lower() or "rockwell unsure" in r.notes.lower() or "service manual" in r.notes.lower()]
    print(f"  Vendor knowledge gaps observed: {len(vendor_gaps)}")
    for r in vendor_gaps:
        print(f"    - {r.id}: {r.notes[:80]}")
    
    # Recurrence after fix
    recurrence = [r for r in all_rows if "recur" in r.notes.lower() or "replacement" in r.notes.lower()]
    print(f"  Recurrence after replacement: {len(recurrence)}")
    for r in recurrence:
        print(f"    - {r.id}: {r.notes[:80]}")
    
    # Specific error codes
    specific_codes = [r for r in all_rows if has_fault_language(r.title) and any(c.isdigit() for c in r.error_codes)]
    print(f"  Specific error/fault codes cited: {len(specific_codes)}")
    for r in specific_codes:
        print(f"    - {r.id}: {r.error_codes}")
    
    # High view counts on error threads
    high_views = [r for r in all_rows if r.views > 1000]
    print(f"  High view counts (>1000): {len(high_views)}")
    for r in high_views:
        print(f"    - {r.id}: {r.views} views - {r.title[:50]}...")