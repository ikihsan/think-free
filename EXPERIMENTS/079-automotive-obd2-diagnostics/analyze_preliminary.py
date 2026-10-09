#!/usr/bin/env python3
"""
E079 — Analyze title+tag data from Mechanics.SE (preliminary, no answer data).
API throttle prevents fetching bodies/answers.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RAW_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "questions_raw.json")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis")
os.makedirs(OUTPUT_DIR, exist_ok=True)

OBD2_PATTERN = re.compile(r'\b[PBCU][0-9]{4}\b')

# Known vehicle make tags
MAKE_TAGS = {
    "toyota", "honda", "ford", "chevrolet", "nissan", "hyundai", "kia",
    "bmw", "vw", "subaru", "dodge", "jeep", "mazda", "acura", "lexus",
    "volvo", "porsche", "mini", "mitsubishi", "suzuki", "infiniti",
    "cadillac", "buick", "gmc", "ram", "chrysler", "jaguar", "fiat", "tesla"
}

# Model tags (common ones)
MODEL_TAGS = {
    "camry", "corolla", "prius", "civic", "accord", "cr-v", "f-150", "silverado",
    "ram", "altima", "sentra", "elantra", "tucson", "sportage", "3-series",
    "5-series", "golf", "jetta", "passat", "outback", "forester", "impreza",
    "wrangler", "grand-cherokee", "cherokee", "cx-5", "mazda3", "mazda6",
    "tlx", "rdx", "rx", "nx", "xc60", "xc90", "911", "cayenne", "cooper",
    "lancer", "evo", "swift", "vitara", "q50", "q60", "escalade", "encore",
    "sierra", "1500", "2500", "300", "pacifica", "f-pace", "500", "model-3",
    "model-y", "model-s", "model-x"
}


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def extract_vehicle_info(tags: List[str]) -> Tuple[str, str]:
    """Extract (make, model) from tags."""
    make = ""
    model = ""
    for tag in tags:
        tag_lower = tag.lower()
        if tag_lower in MAKE_TAGS and not make:
            make = tag_lower
        elif tag_lower in MODEL_TAGS and not model:
            model = tag_lower
    return make, model


def main() -> int:
    print("=== E079 Preliminary Analysis (Title + Tags Only) ===")
    print(f"Loading {RAW_FILE}...")

    with open(RAW_FILE, "r") as f:
        questions = json.load(f)

    print(f"Total questions: {len(questions)}")

    # Find questions with OBD2 codes in title
    candidates = []
    code_counts = Counter()
    make_model_counts = Counter()
    code_by_make = defaultdict(Counter)

    for q in questions:
        title = q.get("title", "")
        codes = OBD2_PATTERN.findall(title.upper())
        if not codes:
            continue

        tags = [t.lower() for t in q.get("tags", [])]
        make, model = extract_vehicle_info(tags)

        for code in codes:
            code_counts[code] += 1
            if make:
                make_model_counts[(make, model or "unknown")] += 1
                code_by_make[make][code] += 1

        candidates.append({
            "question_id": q["question_id"],
            "title": title,
            "tags": tags,
            "codes": codes,
            "make": make,
            "model": model,
            "score": q.get("score", 0),
            "view_count": q.get("view_count", 0),
            "answer_count": q.get("answer_count", 0),
            "is_answered": q.get("is_answered", False),
        })

    print(f"\nTitle candidates: {len(candidates)}")
    print(f"Total code mentions: {sum(code_counts.values())}")
    print(f"Unique codes: {len(code_counts)}")

    # G2: Code concentration - top 10 codes coverage
    total_mentions = sum(code_counts.values())
    top10 = code_counts.most_common(10)
    top10_count = sum(c for _, c in top10)
    top10_coverage = top10_count / total_mentions if total_mentions > 0 else 0

    print(f"\n=== G2: Code Concentration ===")
    print(f"Top 10 codes cover {top10_coverage:.1%} of mentions")
    print("Top 20 codes:")
    for code, count in code_counts.most_common(20):
        print(f"  {code}: {count}")

    # G3: Vehicle coverage from tags
    makes_with_codes = set(m for m, _ in make_model_counts.keys())
    print(f"\n=== G3: Vehicle Coverage (from tags) ===")
    print(f"Makes represented: {len(makes_with_codes)}")
    print(f"Make-model pairs: {len(make_model_counts)}")

    # Top codes by make
    print("\nTop codes per make:")
    for make in sorted(makes_with_codes):
        top = code_by_make[make].most_common(3)
        print(f"  {make}: {top}")

    # Check top 10 codes across makes
    top10_codes = {c for c, _ in top10}
    vehicles_for_top10 = set()
    for q in candidates:
        if any(c in top10_codes for c in q["codes"]) and q["make"]:
            vehicles_for_top10.add((q["make"], q["model"]))

    print(f"\nVehicle configs (make+model) for top 10 codes: {len(vehicles_for_top10)}")
    for vm in sorted(vehicles_for_top10)[:20]:
        print(f"  {vm}")

    # G1/G4: Need answer data - cannot evaluate
    print(f"\n=== G1 & G4: Require Answer Data ===")
    print("Cannot evaluate - API throttle prevents fetching answers")
    print("Title candidates with answers (from metadata):")
    answered = sum(1 for c in candidates if c["is_answered"])
    print(f"  {answered}/{len(candidates)} marked as answered")
    print(f"  Average answer count: {sum(c['answer_count'] for c in candidates)/len(candidates):.1f}")

    # Save results
    results = {
        "total_questions": len(questions),
        "title_candidates": len(candidates),
        "total_code_mentions": total_mentions,
        "unique_codes": len(code_counts),
        "code_counts": dict(code_counts.most_common()),
        "top10_codes": top10,
        "top10_coverage": top10_coverage,
        "makes_with_codes": list(makes_with_codes),
        "make_model_pairs": len(make_model_counts),
        "vehicles_for_top10": len(vehicles_for_top10),
        "answered_candidates": answered,
        "avg_answer_count": sum(c["answer_count"] for c in candidates)/len(candidates) if candidates else 0,
        "gate_status": {
            "G1_population": "PENDING - needs answer data",
            "G2_code_concentration": "PASS" if top10_coverage >= 0.30 else "FAIL",
            "G3_vehicle_coverage": "PASS" if len(vehicles_for_top10) >= 15 else "FAIL",
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
    g3_pass = len(vehicles_for_top10) >= 15
    print(f"G2 (code concentration ≥30%): {'PASS' if g2_pass else 'FAIL'} ({top10_coverage:.1%})")
    print(f"G3 (vehicle coverage ≥15): {'PASS' if g3_pass else 'FAIL'} ({len(vehicles_for_top10)})")
    print("G1, G4: PENDING (require answer data)")
    print("G5: PENDING (manual)")

    if g2_pass and g3_pass:
        print("\n→ Population shows code concentration and vehicle diversity. Worth pursuing with answer data.")
    else:
        print("\n→ Population may not meet concentration/coverage thresholds.")

    return 0


if __name__ == "__main__":
    sys.exit(main())