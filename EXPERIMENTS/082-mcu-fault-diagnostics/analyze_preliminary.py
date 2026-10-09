#!/usr/bin/env python3
"""
E082 — Analyze title+tag data from electronics.SE (preliminary, no answer data).
API throttle prevents fetching bodies/answers.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Set

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RAW_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "questions_raw.json")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fault pattern regex (case-insensitive) - must match fetch.py
FAULT_PATTERN = re.compile(
    r'\b(?:'
    r'HardFault|MemManage|BusFault|UsageFault|SecureFault|'
    r'HFSR|CFSR|DFSR|AFSR|MMFAR|BFAR|UFSR|BFSR|SHCSR|'
    r'EXC_RETURN|FAULTMASK|PRIMASK|BASEPRI|'
    r'stack\s+overflow|watchdog|brownout|brown-out|'
    r'Hard\s+Fault|Bus\s+Fault|Usage\s+Fault|MemManage\s+Fault|Secure\s+Fault|'
    r'DIVBYZERO|UNALIGNED|NOCP|INVSTATE|UNDEFINSTR|INVPC|'
    r'IBUSERR|PRECISERR|IMPRECISERR|UNSTKERR|STKERR|'
    r'null\s+pointer|division\s+by\s+zero|undefined\s+instruction|'
    r'fault|exception|crash|reset|watchdog|brownout'
    r')\b',
    re.IGNORECASE
)

# Known MCU family tags
MCU_FAMILY_TAGS = {
    "stm32", "stm32f1", "stm32f4", "stm32h7", "stm32g0", "stm32l4", "stm32wb", "stm32wl",
    "arm", "cortex-m", "cortex-m0", "cortex-m3", "cortex-m4", "cortex-m7", "cortex-m33",
    "atmel", "avr", "atmega", "attiny", "arduino",
    "pic", "dspic", "pic16", "pic18", "pic24", "pic32",
    "esp32", "esp8266", "espressif",
    "nrf52", "nrf51", "nordic",
    "msp430", "msp432", "ti-msp",
    "tm4c", "tiva", "stellaris", "lm4f",
    "lpc", "lpc17", "lpc43", "lpc55", "nxp",
    "kinetis", "k20", "k22", "k64", "k66", "k80", "k82",
    "efm32", "gecko", "silabs", "silicon-labs",
    "sam", "samd", "samc", "same", "saml", "samg", "samv", "samrh",
    "rp2040", "rp2350", "raspberry-pi-pico", "pico",
}

# Canonical MCU families (for G3)
CANONICAL_FAMILIES = {
    "STM32": {"stm32", "stm32f1", "stm32f4", "stm32h7", "stm32g0", "stm32l4", "stm32wb", "stm32wl"},
    "ARM_Cortex-M": {"arm", "cortex-m", "cortex-m0", "cortex-m3", "cortex-m4", "cortex-m7", "cortex-m33"},
    "AVR": {"atmel", "avr", "atmega", "attiny", "arduino"},
    "PIC": {"pic", "dspic", "pic16", "pic18", "pic24", "pic32"},
    "ESP32": {"esp32", "esp8266", "espressif"},
    "nRF52": {"nrf52", "nrf51", "nordic"},
    "MSP430": {"msp430", "msp432", "ti-msp"},
    "TM4C": {"tm4c", "tiva", "stellaris", "lm4f"},
    "LPC": {"lpc", "lpc17", "lpc43", "lpc55", "nxp"},
    "Kinetis": {"kinetis", "k20", "k22", "k64", "k66", "k80", "k82"},
    "EFM32": {"efm32", "gecko", "silabs", "silicon-labs"},
    "SAM": {"sam", "samd", "samc", "same", "saml", "samg", "samv", "samrh"},
    "RP2040": {"rp2040", "rp2350", "raspberry-pi-pico", "pico"},
}

# Fault type canonicalization (for G2)
FAULT_CATEGORIES = [
    (r'HardFault|Hard\s+Fault|hardfault', 'HardFault'),
    (r'MemManage|MemManage\s+Fault|Memory\s+Management\s+Fault', 'MemManage'),
    (r'BusFault|Bus\s+Fault|busfault|IBUSERR|PRECISERR|IMPRECISERR|UNSTKERR|STKERR', 'BusFault'),
    (r'UsageFault|Usage\s+Fault|usagefault|DIVBYZERO|UNALIGNED|NOCP|INVSTATE|UNDEFINSTR|INVPC', 'UsageFault'),
    (r'SecureFault|Secure\s+Fault|LSERR|SFARERR', 'SecureFault'),
    (r'stack\s+overflow|stackover\s+flow|stack\s+overrun|stack\s+exhaustion|MSP|PSP|stack\s+pointer', 'StackOverflow'),
    (r'watchdog|WDT|IWDG|WWDG|watchdog\s+reset|watchdog\s+timeout', 'WatchdogReset'),
    (r'brownout|brown-out|BOR|POR|PDR|power-on\s+reset|brownout\s+reset|power\s+failure|VDD', 'BrownoutReset'),
    (r'clock\s+failure|HSE|LSE|PLL|clock\s+security|CSS|clock\s+monitor|oscillator\s+failure', 'ClockFailure'),
    (r'null\s+pointer|NULL|0x0|0x00000000|dereference|access\s+violation', 'NullPointer'),
    (r'unaligned|UNALIGNED|alignment\s+fault|alignment\s+trap|misaligned', 'UnalignedAccess'),
    (r'division\s+by\s+zero|divide\s+by\s+zero|DIVBYZERO|divide\s+error', 'DivByZero'),
    (r'undefined\s+instruction|UNDEFINSTR|illegal\s+instruction|invalid\s+opcode', 'UndefinedInstr'),
    (r'FPU|coprocessor|NOCP|floating\s+point|VFP|NEON', 'FPUFault'),
    (r'USB|PHY|endpoint|NAK|STALL|CRC\s+error|babble', 'USBFault'),
    (r'CAN|bus\s+off|error\s+passive|stuff\s+error|form\s+error|ACK\s+error', 'CANFault'),
    (r'Ethernet|MAC|PHY|CRC\s+error|collision|jabber', 'EthFault'),
    (r'DMA|transfer\s+error|FIFO\s+error|address\s+error', 'DMAFault'),
    (r'ADC|DAC|conversion\s+error|overrun|watchdog', 'ADCFault'),
    (r'interrupt|priority|NVIC|pending|tail-chaining|late\s+arrival', 'IRQFault'),
    (r'flash|bootloader|erase|program|verify|write\s+protect|read\s+protect', 'FlashFault'),
    (r'FreeRTOS|ThreadX|Zephyr|context\s+switch|task|semaphore|mutex|queue', 'RTOSFault'),
]

FAULT_CATEGORY_PATTERNS = [(re.compile(pattern, re.IGNORECASE), canonical) for pattern, canonical in FAULT_CATEGORIES]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def canonicalize_fault(indicator: str) -> str:
    """Map a raw fault indicator to its canonical category."""
    for pattern, canonical in FAULT_CATEGORY_PATTERNS:
        if pattern.search(indicator):
            return canonical
    return 'Other'


def extract_mcu_families(tags: List[str]) -> Set[str]:
    """Extract canonical MCU families from tags."""
    families = set()
    tags_lower = {t.lower() for t in tags}
    for family, tag_set in CANONICAL_FAMILIES.items():
        if tags_lower & tag_set:
            families.add(family)
    return families


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def main() -> int:
    print("=== E082 Preliminary Analysis (Title + Tags Only) ===")
    print(f"Loading {RAW_FILE}...")

    if not os.path.exists(RAW_FILE):
        print(f"ERROR: {RAW_FILE} not found. Run fetch.py first (or wait for API throttle to reset).")
        return 1

    with open(RAW_FILE, "r") as f:
        questions = json.load(f)

    print(f"Total questions: {len(questions)}")

    # Find questions with fault indicators in title
    candidates = []
    fault_counts = Counter()
    family_counts = Counter()
    fault_by_family = defaultdict(Counter)
    fault_families = defaultdict(set)  # fault -> set of families

    for q in questions:
        title = q.get("title", "")
        fault_matches = FAULT_PATTERN.findall(title)
        if not fault_matches:
            continue

        tags = [t.lower() for t in q.get("tags", [])]
        families = extract_mcu_families(tags)

        for fault in fault_matches:
            canonical = canonicalize_fault(fault)
            fault_counts[canonical] += 1
            for fam in families:
                family_counts[fam] += 1
                fault_by_family[fam][canonical] += 1
                fault_families[canonical].add(fam)

        candidates.append({
            "question_id": q["question_id"],
            "title": title,
            "tags": tags,
            "fault_indicators": fault_matches,
            "fault_categories": [canonicalize_fault(f) for f in fault_matches],
            "families": list(families),
            "score": q.get("score", 0),
            "view_count": q.get("view_count", 0),
            "answer_count": q.get("answer_count", 0),
            "is_answered": q.get("is_answered", False),
        })

    print(f"\nTitle candidates (with fault indicators): {len(candidates)}")
    print(f"Total fault mentions: {sum(fault_counts.values())}")
    print(f"Unique fault categories: {len(fault_counts)}")

    # G2: Fault concentration - top 10 fault categories coverage
    total_mentions = sum(fault_counts.values())
    top10 = fault_counts.most_common(10)
    top10_count = sum(c for _, c in top10)
    top10_coverage = top10_count / total_mentions if total_mentions > 0 else 0

    print(f"\n=== G2: Fault Concentration ===")
    print(f"Top 10 fault categories cover {top10_coverage:.1%} of mentions")
    print("Top 20 fault categories:")
    for fault, count in fault_counts.most_common(20):
        print(f"  {fault}: {count}")

    # G3: MCU family coverage from tags
    print(f"\n=== G3: MCU Family Coverage (from tags) ===")
    print(f"MCU families represented: {len(family_counts)}")
    for fam, count in family_counts.most_common():
        print(f"  {fam}: {count}")

    # Top faults by family
    print("\nTop fault categories per MCU family:")
    for fam in sorted(fault_by_family.keys()):
        top = fault_by_family[fam].most_common(3)
        print(f"  {fam}: {top}")

    # Check top 10 faults across families
    top10_faults = {c for c, _ in top10}
    families_for_top10 = set()
    for fault in top10_faults:
        families_for_top10.update(fault_families.get(fault, set()))

    print(f"\nMCU families for top 10 fault categories: {len(families_for_top10)}")
    for fam in sorted(families_for_top10):
        print(f"  {fam}")

    # G1/G4: Need answer data - cannot evaluate
    print(f"\n=== G1 & G4: Require Answer Data ===")
    print("Cannot evaluate - API throttle prevents fetching answers")
    print("Title candidates with answers (from metadata):")
    answered = sum(1 for c in candidates if c["is_answered"])
    print(f"  {answered}/{len(candidates)} marked as answered")
    print(f"  Average answer count: {sum(c['answer_count'] for c in candidates)/len(candidates):.1f}" if candidates else "  No candidates")
    print(f"  Average view count: {sum(c['view_count'] for c in candidates)/len(candidates):.1f}" if candidates else "  No candidates")

    # View count analysis (instrument validation)
    vc_positive = sum(1 for c in candidates if c["view_count"] > 0)
    vc_rate = vc_positive / len(candidates) if candidates else 0
    print(f"\n=== View Count Instrument (E069/F096 validation) ===")
    print(f"Candidates with view_count > 0: {vc_positive}/{len(candidates)} = {vc_rate:.1%}")

    # Save results
    results = {
        "total_questions": len(questions),
        "title_candidates": len(candidates),
        "total_fault_mentions": total_mentions,
        "unique_fault_categories": len(fault_counts),
        "fault_counts": dict(fault_counts.most_common()),
        "top10_faults": top10,
        "top10_coverage": top10_coverage,
        "mcu_families": dict(family_counts.most_common()),
        "families_for_top10": len(families_for_top10),
        "answered_candidates": answered,
        "avg_answer_count": sum(c["answer_count"] for c in candidates)/len(candidates) if candidates else 0,
        "avg_view_count": sum(c["view_count"] for c in candidates)/len(candidates) if candidates else 0,
        "view_count_positive_rate": vc_rate,
        "gate_status": {
            "G1_population": "PENDING - needs answer data",
            "G2_fault_concentration": "PASS" if top10_coverage >= 0.30 else "FAIL",
            "G3_mcu_coverage": "PASS" if len(families_for_top10) >= 10 else "FAIL",
            "G4_root_cause_specificity": "PENDING - needs answer data",
            "G5_incumbent_gap": "PENDING - manual review needed",
        },
        "limitation": "API throttle (300 req/day) prevented fetching question bodies and answers. Full gate evaluation requires answer data.",
    }

    out_path = os.path.join(OUTPUT_DIR, "preliminary_gate_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved preliminary results to {out_path}")

    # Save candidates for later
    cand_path = os.path.join(OUTPUT_DIR, "title_candidates.json")
    with open(cand_path, "w") as f:
        json.dump(candidates, f, indent=2)
    print(f"Saved title candidates to {cand_path}")

    # Verdict
    print("\n=== PRELIMINARY VERDICT ===")
    g2_pass = top10_coverage >= 0.30
    g3_pass = len(families_for_top10) >= 10
    print(f"G2 (fault concentration ≥30%): {'PASS' if g2_pass else 'FAIL'} ({top10_coverage:.1%})")
    print(f"G3 (MCU family coverage ≥10): {'PASS' if g3_pass else 'FAIL'} ({len(families_for_top10)})")
    print("G1, G4: PENDING (require answer data)")
    print("G5: PENDING (manual)")

    if g2_pass and g3_pass:
        print("\n→ Population shows fault concentration and MCU family diversity. Worth pursuing with answer data.")
    else:
        print("\n→ Population may not meet concentration/coverage thresholds.")

    return 0


if __name__ == "__main__":
    sys.exit(main())