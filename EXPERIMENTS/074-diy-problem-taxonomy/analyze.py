#!/usr/bin/env python3
"""
Experiment 074: DIY Problem Taxonomy — Analysis Script
stdlib only, Python 3.8+
"""

import json
import csv
import re
import sys
from pathlib import Path
from collections import Counter

# ─── Taxonomy ──────────────────────────────────────────────────────────────
TAXONOMY = {
    "DIAG": "Appliance/equipment diagnosis",
    "CALC": "Engineering calculation",
    "CODE": "Code compliance",
    "IDENT": "Identification",
    "PROC": "Procedure/method",
    "MATL": "Material selection",
    "COST": "Cost estimation",
    "SAFE": "Safety assessment",
    "MAINT": "Maintenance schedule",
    "OTHER": "Other",
}

STRUCTURED_PATTERNS = [
    # Error codes: F83, E1, E01, blinking 3 times, fault code
    (re.compile(r'\b([A-Z]\d{1,3}|[A-Z]{2,}\d{1,3})\b'), "error_code"),
    (re.compile(r'\b(fault|error|code)\s+([A-Z0-9]+)\b', re.I), "error_code"),
    (re.compile(r'blinking\s+\d+', re.I), "error_code"),
    # Model numbers: alphanumeric with dashes, at least 3 chars, mixed case/numbers
    (re.compile(r'\b([A-Z]{2,}\d{2,}[A-Z0-9\-]*)\b'), "model_number"),
    (re.compile(r'\b(\d+[A-Z]{2,}\d*)\b'), "model_number"),
    # Measurements: volts, amps, watts, AWG, feet, inches, mm, cm, psi, GPM
    (re.compile(r'\b\d+(?:\.\d+)?\s*(?:V|A|W|VAC|VDC|AWG|ft|in|mm|cm|m|psi|GPM|CFM|BTU)\b', re.I), "measurement"),
    # Code references: NEC 300.4, UPC 908.2.4, IRC R302
    (re.compile(r'\b(NEC|IPC|UPC|IRC|IBC|NFPA)\s+\d+[\.\d]*\b', re.I), "code_ref"),
    # Standards: UL, ASTM, ANSI, ISO
    (re.compile(r'\b(UL|ASTM|ANSI|ISO|CSA|ETL)\s+(?:listed|certified|standard)?\s*\d*\b', re.I), "standard"),
]

def has_structured_input(text):
    """Return (bool, list_of_match_types)"""
    matches = []
    for pattern, label in STRUCTURED_PATTERNS:
        if pattern.search(text):
            matches.append(label)
    return len(matches) > 0, matches

def classify_question(title, tags, body):
    """
    Heuristic classification based on title, tags, and body.
    Returns primary type code.
    """
    text = f"{title} {' '.join(tags)} {body}".lower()

    # DIAG: appliance/equipment diagnosis - symptoms, error codes, "won't work", "humming", "leaking"
    diag_keywords = [
        "error", "fault", "code", "blink", "hum", "buzz", "leak", "won't", "wont",
        "not working", "stopped", "failed", "malfunction", "trouble", "problem with",
        "diagnos", "symptom", "indicator", "light", "beep"
    ]
    appliance_tags = ["appliance", "washing-machine", "dryer", "refrigerator", "hvac", "furnace",
                      "boiler", "water-heater", "generator", "motor", "pump", "compressor",
                      "ac", "air-conditioner", "heat-pump", "dishwasher", "oven", "range",
                      "cooktop", "microwave", "disposal", "sump-pump", "well-pump"]

    if any(kw in text for kw in diag_keywords) or any(t in tags for t in appliance_tags):
        return "DIAG"

    # CALC: calculations - voltage drop, load, sizing, span, height
    calc_keywords = [
        "calculate", "calculation", "voltage drop", "load", "sizing", "size",
        "span", "capacity", "ampacity", "wire size", "pipe size", "btu",
        "flow rate", "pressure drop", "head loss", "voltage", "amperage",
        "how many", "how much", "what size", "measure", "height of"
    ]
    if any(kw in text for kw in calc_keywords):
        return "CALC"

    # CODE: code compliance - NEC, UPC, IPC, IRC, "code", "legal", "compliant", "permit"
    code_keywords = [
        "code", "nec", "upc", "ipc", "irc", "ibc", "nfpa", "compliant",
        "legal", "permit", "inspection", "approved", "listed", "ul listed",
        "does the", "allowed", "allowed by", "required by"
    ]
    if any(kw in text for kw in code_keywords):
        return "CODE"

    # IDENT: identification - "what is this", "identify", "unknown", "mystery"
    ident_keywords = [
        "what is this", "identify", "unknown", "mystery", "what are these",
        "what kind", "what type", "name of", "called"
    ]
    if any(kw in text for kw in ident_keywords):
        return "IDENT"

    # PROC: procedure - "how do i", "how to", "steps", "procedure", "method"
    proc_keywords = [
        "how do i", "how to", "how can i", "steps", "procedure", "method",
        "technique", "way to", "install", "replace", "remove", "repair",
        "fix", "build", "construct", "mount", "attach", "connect"
    ]
    # But not if it's clearly DIAG (symptom-based)
    if any(kw in text for kw in proc_keywords) and not any(kw in text for kw in diag_keywords):
        return "PROC"

    # MATL: material selection - "what type of", "what kind of", "best", "recommend", "choose"
    matl_keywords = [
        "what type of", "what kind of", "best ", "recommend", "choose",
        "which ", "better ", "vs ", "versus", "compare", "difference between",
        "grade", "quality", "brand"
    ]
    material_tags = ["concrete", "cement", "mortar", "grout", "adhesive", "sealant",
                     "wire", "cable", "pipe", "tube", "pvc", "cpvc", "pex", "copper",
                     "lumber", "plywood", "osb", "drywall", "insulation", "fastener",
                     "screw", "nail", "bolt", "anchor", "paint", "stain", "primer"]
    if any(kw in text for kw in matl_keywords) or any(t in tags for t in material_tags):
        return "MATL"

    # COST: cost estimation
    cost_keywords = [
        "cost", "price", "expensive", "cheap", "budget", "afford", "estimate",
        "quote", "bid", "worth it", "cost-effective", "save money"
    ]
    if any(kw in text for kw in cost_keywords):
        return "COST"

    # SAFE: safety
    safe_keywords = [
        "safe", "dangerous", "hazard", "risk", "fire", "shock", "electrocute",
        "collapse", "structural", "toxic", "asbestos", "lead", "mold"
    ]
    if any(kw in text for kw in safe_keywords):
        return "SAFE"

    # MAINT: maintenance schedule
    maint_keywords = [
        "how often", "when should", "schedule", "maintenance", "service",
        "interval", "replace filter", "change oil", "flush", "clean",
        "inspect", "check"
    ]
    if any(kw in text for kw in maint_keywords):
        return "MAINT"

    return "OTHER"


def main():
    exp_dir = Path(__file__).parent
    data_dir = exp_dir / "data"
    data_dir.mkdir(exist_ok=True)

    # Load fetched questions
    questions_file = data_dir / "questions.json"
    if not questions_file.exists():
        print(f"Error: {questions_file} not found. Run fetch first.")
        return 1

    with open(questions_file) as f:
        data = json.load(f)

    questions = data.get("items", [])
    print(f"Loaded {len(questions)} questions")

    # Classify each question
    rows = []
    type_counts = Counter()
    structured_by_type = Counter()
    total_structured = 0

    for q in questions:
        qid = q["question_id"]
        title = q.get("title", "")
        tags = [t for t in q.get("tags", [])]
        body = q.get("body", "")

        # Truncate body for analysis (first 2000 chars)
        body_short = body[:2000]

        qtype = classify_question(title, tags, body_short)
        has_struct, match_types = has_structured_input(f"{title} {body_short}")

        type_counts[qtype] += 1
        if has_struct:
            structured_by_type[qtype] += 1
            total_structured += 1

        rows.append({
            "question_id": qid,
            "title": title,
            "tags": ";".join(tags),
            "primary_type": qtype,
            "has_structured_input": has_struct,
            "structured_match_types": ";".join(match_types),
            "view_count": q.get("view_count", 0),
            "score": q.get("score", 0),
            "answer_count": q.get("answer_count", 0),
            "is_answered": q.get("is_answered", False),
        })

    # Write taxonomy.jsonl (exempt from line cap)
    jsonl_file = data_dir / "taxonomy.jsonl"
    with open(jsonl_file, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
    print(f"Wrote {jsonl_file}")

    # Distribution
    total = len(rows)
    distribution = {}
    for t, count in type_counts.most_common():
        pct = count / total * 100
        structured_count = structured_by_type.get(t, 0)
        structured_pct = structured_count / count * 100 if count > 0 else 0
        distribution[t] = {
            "count": count,
            "percentage": round(pct, 1),
            "structured_count": structured_count,
            "structured_percentage": round(structured_pct, 1),
            "label": TAXONOMY.get(t, t)
        }

    dist_file = data_dir / "distribution.json"
    with open(dist_file, "w") as f:
        json.dump(distribution, f, indent=2)
    print(f"Wrote {dist_file}")

    # Structured by type
    structured_data = {}
    for t in TAXONOMY:
        count = type_counts.get(t, 0)
        structured = structured_by_type.get(t, 0)
        structured_data[t] = {
            "total": count,
            "structured": structured,
            "rate": round(structured / count * 100, 1) if count > 0 else 0
        }

    struct_file = data_dir / "structured_by_type.json"
    with open(struct_file, "w") as f:
        json.dump(structured_data, f, indent=2)
    print(f"Wrote {struct_file}")

    # Evaluate gates
    print("\n=== GATE EVALUATION ===")
    # G1: any type >= 15%
    g1_pass = False
    g1_type = None
    for t, info in distribution.items():
        if info["percentage"] >= 15:
            g1_pass = True
            g1_type = t
            print(f"G1 PASS: {t} ({info['label']}) = {info['percentage']}%")
            break
    if not g1_pass:
        top = max(distribution.items(), key=lambda x: x[1]["percentage"])
        print(f"G1 FAIL: top type {top[0]} ({top[1]['label']}) = {top[1]['percentage']}% < 15%")

    # G2: for G1 type, structured >= 50%
    g2_pass = False
    if g1_pass:
        info = structured_data[g1_type]
        if info["rate"] >= 50:
            g2_pass = True
            print(f"G2 PASS: {g1_type} structured rate = {info['rate']}%")
        else:
            print(f"G2 FAIL: {g1_type} structured rate = {info['rate']}% < 50%")

    # G3: tool check (manual, recorded in tool_check.md)
    g3_pass = None  # requires manual check

    # Verdict
    verdict = {
        "G1_population": {"pass": g1_pass, "type": g1_type, "detail": distribution.get(g1_type, {})},
        "G2_structure": {"pass": g2_pass, "type": g1_type, "detail": structured_data.get(g1_type, {})},
        "G3_gap": {"pass": g3_pass, "note": "Requires manual tool_check.md review"},
        "overall": "PENDING_G3" if g1_pass and g2_pass else "FAIL"
    }

    verdict_file = data_dir / "verdict.json"
    with open(verdict_file, "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"Wrote {verdict_file}")

    # Print summary
    print(f"\nTotal questions: {total}")
    print(f"Total with structured input: {total_structured} ({total_structured/total*100:.1f}%)")
    print("\nDistribution:")
    for t, info in distribution.items():
        print(f"  {t:6s} ({info['label']:35s}): {info['count']:3d} ({info['percentage']:5.1f}%)  structured: {info['structured_percentage']:5.1f}%")

    return 0 if (g1_pass and g2_pass) else 1


if __name__ == "__main__":
    sys.exit(main())