#!/usr/bin/env python3
"""
Discrimination Test for fault_need_classifier
Tests on forum listing data from MrPLC (manual extraction from HTML)
"""

import re
import json
from dataclasses import dataclass
from typing import List, Tuple
from math import sqrt

@dataclass
class ForumEntry:
    title: str
    forum: str
    replies: int
    views: int
    expected_label: str  # 'served' or 'unserved'
    probe_id: str

def has_specific_error_code(title: str) -> bool:
    """Check if title contains specific error/fault code patterns."""
    patterns = [
        r'error\s+\d+',
        r'fault\s+\d+',
        r'code\s+\d+',
        r'0x[0-9A-Fa-f]+',
        r'\bE\d{2,}\b',
        r'\b\d{4,5}\b',  # 4-5 digit codes
        r'fault\s+code',
        r'error\s+code',
    ]
    return any(re.search(p, title, re.IGNORECASE) for p in patterns)

def fault_need_classifier(entry: ForumEntry) -> str:
    """Classify a forum entry as 'served' or 'unserved'."""
    error_code_present = has_specific_error_code(entry.title)
    vendor_acknowledged = False  # Not available from listing alone
    
    if error_code_present and vendor_acknowledged:
        return "served"
    elif entry.views > 100 and entry.replies > 0 and error_code_present:
        return "served"
    elif entry.views > 500 and entry.replies == 0 and error_code_present:
        return "unserved"
    elif entry.views < 10 and entry.replies == 0:
        return "unserved"
    else:
        return "unserved"

def wilson_ci(p: float, n: int, z: float = 1.96) -> Tuple[float, float]:
    """Wilson score interval for binomial proportion."""
    if n == 0:
        return (0.0, 1.0)
    denominator = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denominator
    half = z * sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator
    return (max(0.0, centre - half), min(1.0, centre + half))

# Test data extracted from forum listings (MrPLC)
# Format: (title, forum, replies, views, expected_label, probe_id)
test_entries = [
    # Known-served probes (from forum listings with error codes + replies)
    ForumEntry("1747-NI8 Open Circuit", "Allen Bradley", 9, 4900, "served", "S1"),
    ForumEntry("Migration Support Needed: Honeywell HC900 to Rockwell ControlLogix", "Allen Bradley", 1, 236, "served", "S2"),
    ForumEntry("Kinetix 5500 , Studio 5000", "Allen Bradley", 1, 197, "served", "S3"),
    ForumEntry("USR-N540", "Allen Bradley", 3, 301, "served", "S4"),
    ForumEntry("Rockwell 1756-L81E ↔ Omron DRT1-COM via 1756-DNB – Analog I/O Scaling Issue", "Allen Bradley", 0, 163, "served", "S5"),
    ForumEntry("CompactLogix Ethernet/IP timing", "Allen Bradley", 17, 1400, "served", "S6"),
    ForumEntry("panelview 600", "Allen Bradley", 11, 8200, "served", "S7"),
    ForumEntry("FactoryTalkView Project Comparator HTML App", "Allen Bradley", 2, 308, "served", "S8"),
    ForumEntry("To convert .rss to .pdf", "Allen Bradley", 1, 244, "served", "S9"),
    ForumEntry("PLC Programming Language", "Allen Bradley", 11, 5500, "served", "S10"),
    ForumEntry("PowerFlex 755 Reserved web enable parameter", "Allen Bradley", 1, 299, "served", "S11"),
    ForumEntry("CCW HSC PLS config", "Allen Bradley", 1, 0, "served", "S12"),  # views not parsed
    
    # Mitsubishi forum entries
    ForumEntry("Timer not counting", "Mitsubishi", 6, 204, "served", "S13"),
    ForumEntry("Gx Work 2 software error System stop failed Please restart Windows", "Mitsubishi", 3, 1600, "served", "S14"),
    ForumEntry("Mitsubishi iQ-R PLC communication error error codes 1134 C0B2 and C709", "Mitsubishi", 11, 688, "served", "S15"),
    ForumEntry("RJ71SEIP91-T4 Diagnostics", "Mitsubishi", 2, 387, "served", "S16"),
    ForumEntry("FX5U Modbus tcp communication", "Mitsubishi", 4, 294, "served", "S17"),
    ForumEntry("Mitsubishi GT Soft GOT1000 comms problem", "Mitsubishi", 2, 275, "served", "S18"),
    ForumEntry("Mitsubishi melsec Q buildin ethernet", "Mitsubishi", 2, 143, "served", "S19"),
    ForumEntry("Mitsubishi iQ-R PLC communication error", "Mitsubishi", 11, 688, "served", "S20"),
    
    # Siemens forum entries
    ForumEntry("HMI TP1200 Comfort Panel error Application HMIRTM EXE encountered a serious error and must shutdown", "Siemens", 6, 472, "served", "S21"),
    ForumEntry("WAGOB750 GSD", "Siemens", 3, 289, "served", "S22"),
    ForumEntry("Help Im not getting any communication", "Siemens", 3, 365, "served", "S23"),
    ForumEntry("Siemens Frequency Inverter 6SL3210-1PE31-8AL0 Firmware Issues", "Siemens", 2, 278, "served", "S24"),
    ForumEntry("Backup", "Siemens", 3, 516, "served", "S25"),
    ForumEntry("Siemens 8D will not connect to Simatic s7 hardware expansion unit", "Siemens", 1, 433, "served", "S26"),
    ForumEntry("WinAC SLOT CPU 412 V3.3", "Siemens", 0, 1600, "served", "S27"),
    ForumEntry("Which Siemens PLC would you choose S7-1200 o S7-1500", "Siemens", 11, 851, "served", "S28"),
    ForumEntry("Example project for Modbus RTU communication between a Siemens S7-1200 PLC and an OMRON 3G3M1 inverter", "Siemens", 0, 1600, "served", "S29"),
    ForumEntry("WINCC Professional V17 Custom Recipe View", "Siemens", 0, 1600, "served", "S30"),
    ForumEntry("Looking for WinCC Runtime Professional V17 Installer", "Siemens", 2, 553, "served", "S31"),
    ForumEntry("Cpu 315-2eh14 gsdml file", "Siemens", 0, 0, "served", "S32"),
    
    # Omron forum entries
    ForumEntry("Light Curtain Muting Lamp Indicator", "Omron", 0, 0, "served", "S33"),
    ForumEntry("CJ2B-EIP21 with 1734-AENTR setup", "Omron", 0, 0, "served", "S34"),
    ForumEntry("Modbus Master FB for the New M1 inverters", "Omron", 0, 0, "served", "S35"),
    ForumEntry("Error -10 No system program", "Omron", 0, 0, "served", "S36"),
    ForumEntry("CX-supervisor recipe window doesn't display after updating", "Omron", 0, 0, "served", "S37"),
    ForumEntry("I am having a network access issue with an OMRON NX1P2-1040DT1 PLC", "Omron", 0, 0, "served", "S38"),
    ForumEntry("Best Practice PLC Programming", "Omron", 13, 14600, "served", "S39"),
    ForumEntry("Omron F-160 Vision System with Allen Bradley CompactLogix", "Omron", 8, 3100, "served", "S40"),
    ForumEntry("OMFINS3 Citect BAD Data", "Omron", 23, 19200, "served", "S41"),
    ForumEntry("Integrating Barcode Sensors with CP2E-N20DR-A", "Omron", 1, 1600, "served", "S42"),
    ForumEntry("NX1P2 and 3rd Party HMI timeout errors", "Omron", 5, 1300, "served", "S43"),
    
    # Modicon forum entries
    ForumEntry("Proface Logic Relay PRO-iO2", "Modicon", 0, 435, "served", "S44"),
    ForumEntry("Pro-face GP Pro EX 4.0 AGP3300 reading data by modbus", "Modicon", 0, 367, "served", "S45"),
    ForumEntry("Telemecanique FTX417 Laptop", "Modicon", 3, 740, "served", "S46"),
    ForumEntry("Software SoMachine Motion V4.4.1", "Modicon", 3, 834, "served", "S47"),
    ForumEntry("TSX 47/400 Atelier XTEL", "Modicon", 0, 796, "served", "S48"),
    ForumEntry("Problem with REAL Data type in OPC Factory server and Vijeo look", "Modicon", 0, 670, "served", "S49"),
    ForumEntry("Telemecanique TSX 47 CPU", "Modicon", 10, 3100, "served", "S50"),
    ForumEntry("Monitor 77 Telemecanique HMI Supervision software", "Modicon", 2, 641, "served", "S51"),
    ForumEntry("Programming Tsx series 7 PLCs", "Modicon", 6, 1300, "served", "S52"),
    ForumEntry("PL7-3", "Modicon", 13, 23700, "served", "S53"),
    ForumEntry("Old Modicon MM-PM10300C Help", "Modicon", 2, 734, "served", "S54"),
    
    # Known-unserved probes (fictional products - should return no results or only spam)
    # Since we can't search, we simulate: fictional products would have 0 views, 0 replies
    ForumEntry("QuantumFlux PLC error", "Allen Bradley", 0, 0, "unserved", "U1"),
    ForumEntry("HyperDrive controller fault", "Mitsubishi", 0, 0, "unserved", "U2"),
    ForumEntry("NeuralLink PLC fault", "Siemens", 0, 0, "unserved", "U3"),
    ForumEntry("FluxCapacitor timeout", "Omron", 0, 0, "unserved", "U4"),
    ForumEntry("WarpCore breach code", "Modicon", 0, 0, "unserved", "U5"),
    ForumEntry("Dilithium crystal fault", "Allen Bradley", 0, 0, "unserved", "U6"),
    ForumEntry("Heisenberg compensator error", "Mitsubishi", 0, 0, "unserved", "U7"),
    ForumEntry("Transporter buffer overflow", "Siemens", 0, 0, "unserved", "U8"),
    ForumEntry("Holodeck safety protocol", "Omron", 0, 0, "unserved", "U9"),
    ForumEntry("Replicator pattern buffer", "Modicon", 0, 0, "unserved", "U10"),
    ForumEntry("Allen Bradley 1774 fault", "Allen Bradley", 0, 0, "unserved", "U11"),
    ForumEntry("GE Fanuc 90-30 error", "GE Emerson", 0, 0, "unserved", "U12"),
    ForumEntry("Modicon 984 error code", "Modicon", 0, 0, "unserved", "U13"),
    ForumEntry("Siemens S5-115U error", "Siemens", 0, 0, "unserved", "U14"),
    ForumEntry("Honeywell TDC 3000 fault", "Other PLCs", 0, 0, "unserved", "U15"),
    ForumEntry("Bristol Babcock 3300 error", "Other PLCs", 0, 0, "unserved", "U16"),
    ForumEntry("Fisher ROC 800 fault", "Other PLCs", 0, 0, "unserved", "U17"),
    ForumEntry("Motorola MOSCAD error", "Other PLCs", 0, 0, "unserved", "U18"),
    ForumEntry("Square D SY/MAX fault", "Other PLCs", 0, 0, "unserved", "U19"),
    ForumEntry("Texas Instruments 505 error", "Other PLCs", 0, 0, "unserved", "U20"),
]

def run_test():
    print("=" * 80)
    print("DISCRIMINATION TEST: fault_need_classifier")
    print("=" * 80)
    
    # Separate served and unserved
    served_entries = [e for e in test_entries if e.expected_label == "served"]
    unserved_entries = [e for e in test_entries if e.expected_label == "unserved"]
    
    print(f"\nTest set: {len(served_entries)} known-served, {len(unserved_entries)} known-unserved")
    
    # Test on known-served
    print("\n--- Known-Served (should classify as 'served') ---")
    served_correct = 0
    for entry in served_entries:
        predicted = fault_need_classifier(entry)
        correct = predicted == entry.expected_label
        if correct:
            served_correct += 1
        status = "✓" if correct else "✗"
        print(f"  {status} {entry.probe_id}: views={entry.views}, replies={entry.replies}, error_code={has_specific_error_code(entry.title)} -> {predicted} (expected {entry.expected_label})")
        if not correct:
            print(f"      Title: {entry.title[:80]}...")
    
    # Test on known-unserved
    print("\n--- Known-Unserved (should classify as 'unserved') ---")
    unserved_correct = 0
    for entry in unserved_entries:
        predicted = fault_need_classifier(entry)
        correct = predicted == entry.expected_label
        if correct:
            unserved_correct += 1
        status = "✓" if correct else "✗"
        print(f"  {status} {entry.probe_id}: views={entry.views}, replies={entry.replies}, error_code={has_specific_error_code(entry.title)} -> {predicted} (expected {entry.expected_label})")
    
    # Compute metrics
    tpr = served_correct / len(served_entries) if served_entries else 0  # True Positive Rate (G2)
    fpr = 1 - (unserved_correct / len(unserved_entries)) if unserved_entries else 0  # False Positive Rate (G1)
    fnr = 1 - tpr  # False Negative Rate (G3)
    
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"Known-Served:  {served_correct}/{len(served_entries)} correct (TPR/G2 = {tpr:.3f})")
    print(f"Known-Unserved: {unserved_correct}/{len(unserved_entries)} correct (FPR/G1 = {fpr:.3f}, FNR/G3 = {fnr:.3f})")
    
    # Wilson 95% CIs
    tpr_ci = wilson_ci(tpr, len(served_entries))
    fpr_ci = wilson_ci(fpr, len(unserved_entries))
    fnr_ci = wilson_ci(fnr, len(served_entries))
    
    print(f"\nWilson 95% CIs:")
    print(f"  TPR (G2): [{tpr_ci[0]:.3f}, {tpr_ci[1]:.3f}]")
    print(f"  FPR (G1): [{fpr_ci[0]:.3f}, {fpr_ci[1]:.3f}]")
    print(f"  FNR (G3): [{fnr_ci[0]:.3f}, {fnr_ci[1]:.3f}]")
    
    # Gate evaluation
    print("\n" + "=" * 80)
    print("GATE EVALUATION")
    print("=" * 80)
    
    g1_pass = fpr < 0.10
    g2_pass = tpr > 0.70
    g3_pass = fnr < 0.30
    
    print(f"G1 (FPR < 0.10): {'PASS' if g1_pass else 'FAIL'} (FPR = {fpr:.3f})")
    print(f"G2 (TPR > 0.70): {'PASS' if g2_pass else 'FAIL'} (TPR = {tpr:.3f})")
    print(f"G3 (FNR < 0.30): {'PASS' if g3_pass else 'FAIL'} (FNR = {fnr:.3f})")
    
    overall_pass = g1_pass and (g2_pass or g3_pass)
    print(f"\nOVERALL: {'PASS' if overall_pass else 'FAIL'}")
    
    if not overall_pass:
        print("\n>>> INSTRUMENT FAILS DISCRIMINATION TEST <<<")
        print(">>> Per D095: Must redesign instrument before population measurement <<<")
    else:
        print("\n>>> INSTRUMENT PASSES DISCRIMINATION TEST <<<")
        print(">>> Proceed to population measurement on practitioner rows <<<")
    
    return overall_pass

if __name__ == "__main__":
    run_test()