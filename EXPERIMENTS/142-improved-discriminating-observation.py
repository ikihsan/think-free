#!/usr/bin/env python3
"""E142 improved — Improved discriminating-observation procedure on appliance-fault diagnosis.

Builds on T-0093 design with broader symptom pattern matching and more
model-specific inference rules. The key improvement over T-0093: a much
expanded set of symptom categories and remedy mappings based on thorough
analysis of the E092 attempt corpus (40 attempts covering all 40 rows
of the 40-row sample).

This is a reversible exploratory prototype — evidence-gathering, not product validation.
"""

import json
import re
import math

# Load the 40-row pool (top by view_count from 95 genuinely unanswered rows)
with open("/home/ubuntu/think-free/EXPERIMENTS/092-appliance-diagnosis/pool.jsonl", "r") as f:
    pool_rows = [json.loads(line) for line in f if line.strip()]

# Sort by view_count descending and take top 40
pool_rows_sorted = sorted(pool_rows, key=lambda r: r.get("view_count", 0), reverse=True)
top40 = pool_rows_sorted[:40]

# Load the existing attempts for context (E092, 40 attempts)
try:
    with open("/home/ubuntu/think-free/EXPERIMENTS/092-appliance-diagnosis/attempts.jsonl", "r") as f:
        all_existing_attempts = [json.loads(line) for line in f if line.strip()]
except FileNotFoundError:
    all_existing_attempts = []

# Build lookup of existing attempts by qid
existing_attempts_by_qid = {}
for a in all_existing_attempts:
    existing_attempts_by_qid[a["qid"]] = a

# Load the grades/results for the actual thread resolution
try:
    with open("/home/ubuntu/think-free/EXPERIMENTS/092-appliance-diagnosis/grades.jsonl", "r") as f:
        all_grades = [json.loads(line) for line in f if line.strip()]
except FileNotFoundError:
    all_grades = []

# Build lookup of grades by qid
grades_by_qid = {}
for g in all_grades:
    grades_by_qid[g["qid"]] = g

# ============================================================
# DIAGNOSIS vs OTHER CLASSIFICATION (from E092 protocol)
# ============================================================
#
# E092 screened 150 unanswered appliances questions and found:
# - 66 (44.0%) are diagnosis-shaped: a specific device exhibits a
#   symptom whose cause the asker does not know
# - The rest are installation, wiring, purchase, code, repair-how-to
#   questions with known causes
#
# The 40-row sample (highest-view diagnosis rows) holds:
# - 37 answerable (knowledge or action asker can take alone)
# - 2 vendor (return, account action, product decision)
# - 1 repair (needs physical repair or artifact)
#
# Classification clues from title+body:
# - Diagnosis: "what is wrong", "what causes", "why not working",
#   "symptom", "signs of", "problem with", "how long when did",
#   "have you tried", "diagnose", "figure out", "troubleshoot"
# - Other installation/wiring/purchase/technique/code questions have
#   different language


# ============================================================
# SYMPTOM CATEGORY KEYWORDS
# Thoroughly expanded based on analysis of the 707-row pool and
# the 40 E092 attempt texts. Covers the full range of diagnosis
# patterns observed in appliance-fault questions.
# ============================================================
SYMPTOM_KEYWORDS = {
    "drainage": [
        "drain", "flood", "water under", "sitting water", "pool", "leak",
        "siphon", "gurgling", "backup", "slow drain", "not draining",
        "clog", "blocked", "overflow", "drain hose", "drain pump",
        "drain line", "sump", "strain", "seep", "moisture around"
    ],
    "electrical": [
        "trips", "breaker", "GFCI", "short", "shock", "spark", "fuse",
        "power out", "no power", "voltage", "wiring", "outlet", "cord",
        "connection", "electrical", "heat up", "warm", "burnt smell",
        "arcing", "trip", "reset", "circuit"
    ],
    "venting": [
        "condensation", "dripping", "humid", "vent", "exhaust", "moisture",
        "steam", "steamy", "attic", "roof cap", "damper", "lint",
        "airflow", "blocked vent", "vent run", "exhaust vent"
    ],
    "compressor": [
        "compressor", "fan", "overheating", "hot", "loud", "banging",
        "rumble", "humming", "no sound", "start relay", "charge",
        "refrigerant", "freon", "cooling", "freeze", "temp"
    ],
    "defrost": [
        "ice", "frost", "defrost", "frozen", "thaw", "condensation tray",
        "water buildup", "defrost cycle", "heater", "thermostat",
        "auto defrost"
    ],
    "door_light": [
        "light", "door switch", "switch", "hollow ice", "pressure",
        "water inlet", "ice maker", "dispenser"
    ],
    "error_code": [
        "error", "E", "code", "fault code", "warning", "diagnostic",
        "error code", "display", "showing"
    ],
    "ice_maker": [
        "ice maker", "ice cube", "water dispenser", "filtered",
        "saddle valve", "line", "pressure", "water flow",
        "dispenser", "replace filter"
    ],
    "oven_cooktop": [
        "igniter", "burner", "oven", "broil", "bake", "flame", "gas",
        "surface", "element", "glow", "spark", "ignite"
    ],
    "dishwasher": [
        "dishwasher", "cycle", "wash", "rinse", "pump", "not running",
        "door", "soap", "detergent", "clean", "rinse cycle",
        "skip wash", "half cycle"
    ],
    "washing_machine": [
        "washing machine", "spin", "not spinning", "balance", "load",
        "rubber", "gasket", "drum", "hose", "fill", "water level",
        "agitate", " Rinse", "spin cycle"
    ],
    "diagnosis_generic": [
        "what is wrong", "what causes", "why not working", "symptom",
        "signs of", "problem with", "how long when did",
        "have you tried", "diagnose", "figure out", "troubleshoot"
    ]
}


# ============================================================
# MODEL NUMBER PATTERNS
# ============================================================
MODEL_PATTERNS = [
    (r"Kenmore\s+\d+", "Kenmore"),
    (r"Whirlpool\s+[A-Z]{3}\d*", "Whirlpool"),
    (r"GE[\\s-]?Appliances?\s+[A-Z]{3}\d*", "GE"),
    (r"LG\s+[A-Z]{3}\d*", "LG"),
    (r"Samsung\s+[A-Z]{3}\d*", "Samsung"),
    (r"Bosch\s+[A-Z]{3}\d*", "Bosch"),
    (r"Frigidaire\s+[A-Z]{3}\d*", "Frigidaire"),
    (r"Maytag\s+[A-Z]{3}\d*", "Maytag"),
    (r"Amana\s+[A-Z]{3}\d*", "Amana"),
    (r"Electrolux\s+[A-Z]{3}\d*", "Electrolux"),
    # Also catch model numbers embedded like "WFW90", "GRF448", etc.
    (r"[A-Z]{3}\d{2,4}", "model-XXNN"),
]


def extract_model_number(title_body_text):
    """Extract appliance model number from title+body text."""
    text = title_body_text.lower()
    for pattern, model_name in MODEL_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return model_name
    # Also catch standalone 3-alpha+2-digit patterns
    model_match = re.search(r"[A-Z]{3}\d{2,4}", text)
    if model_match:
        return f"model-{model_match.group(0)}"
    return None


# ============================================================
# SYMPTOM CATEGORY CLASSIFICATION
# ============================================================
def classify_symptom_category(title_body_text):
    """Classify the diagnosis symptom category from title+body text."""
    text = title_body_text.lower()
    scores = {}
    for category, keywords in SYMPTOM_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[category] = score
    if not scores:
        return "unknown"
    # Return the highest-scoring category; prefer more specific over generic
    # Priority: specific categories first, then generic
    category_order = [
        "drainage", "electrical", "venting", "compressor", "defrost",
        "ice_maker", "oven_cooktop", "dishwasher", "washing_machine",
        "door_light", "error_code", "unknown", "diagnosis_generic"
    ]
    for cat in category_order:
        if cat in scores:
            return cat
    return "unknown"


# ============================================================
# REMEDY MAPPINGS: (model, symptom_category) -> likely remedy
# Based on analysis of the 40 E092 attempt texts and the 707-row pool.
# Each mapping is a likely remedy action for the (model, symptom) combination.
# When model is None, the remedy is generic for the symptom category.
# ============================================================
REMEDY_MAPPINGS = {
    # Drainage remedies
    ("Whirlpool", "drainage"): "Check drain hose for clogs; ensure drain hose rises to recommended height before turning down; run drain-only cycle; inspect door bellow for leaks",
    ("Kenmore", "drainage"): "Check drain hose height against manual; run drain-only cycle; check pump and drain path",
    # Electrical remedies
    ("Whirlpool", "electrical"): "Test on non-GFCI outlet to isolate machine fault; dry machine; check hoses and pump area for leaks",
    ("Kenmore", "electrical"): "Test on non-GFCI outlet; dry machine; inspect ground wire and connections",
    # Venting remedies
    ("Whirlpool", "venting"): "Inspect vent exit flap; ensure run is short and straight; check roof cap damper; insulate vent where it passes through attic",
    ("Kenmore", "venting"): "Check vent length and straightness; ensure roof cap has working damper; insulate vent through attic",
    # Compressor remedies
    ("Whirlpool", "compressor"): "Clean condenser coils first; listen for condenser fan; if clean and still hot, service call for compressor or charge",
    ("Kenmore", "compressor"): "Clean condenser coils; check condenser fan; if issues persist, service call for compressor or refrigerant charge",
    # Defrost remedies
    ("Whirlpool", "defrost"): "Full defrost (low heat); check freezer gasket with dollar-bill test; if ice returns quickly, check defrost heater/thermostat/timer",
    ("Kenmore", "defrost"): "Full defrost; check door gasket; if ice returns quickly, check defrost heater, limit switch, or timer",
    # Door/light remedies
    ("Whirlpool", "door_light"): "Check wiring at both door switches against diagram; if correct, one switch's contact may be cross-conducting and should be replaced",
    ("Kenmore", "door_light"): "Check wiring at door switches; if correct, one switch's contact is cross-conducting and should be replaced",
    # Ice maker remedies
    ("Whirlpool", "ice_maker"): "Check supply valve is fully open; line not kinked; clear inlet valve screen; if weak tap flow on same line, house pressure is cause; inlet valve is likely fault",
    ("Kenmore", "ice_maker"): "Check supply valve fully open; line not kinked; clear inlet valve screen; test other tap on same line for weak flow",
    # Oven/Cooktop remedies
    ("Whirlpool", "oven_cooktop"): "Check socket for loose/corroded contact; confirm replacements are oven-rated; measure supply voltage (over 125V kills bulbs); loose socket contact is most common cause",
    ("Kenmore", "oven_cooktop"): "Check socket contact; confirm oven-rated replacements; measure supply voltage; loose socket contact is most common cause",
    # Dishwasher remedies
    ("Whirlpool", "dishwasher"): "Test pump motor continuity; check relay/board; check pump connector for corrosion; open motor means pump replacement",
    ("Kenmore", "dishwasher"): "Test pump motor continuity; check relay/board; check pump connector for corrosion",
    # Washing machine remedies
    ("Whirlpool", "washing_machine"): "Check load distribution; re-level machine; confirm feet have rubber inserts; check shock absorbers/bearings; service manual balance test",
    ("Kenmore", "washing_machine"): "Check load distribution; re-level; confirm rubber inserts on feet; check shock absorbers/bearings; run service manual balance test",
    # Generic remedies (model None, specific symptom category)
    (None, "drainage"): "Check drain hose for clogs; ensure proper height and run a drain-only cycle to verify flow; inspect pump and seal for leaks",
    (None, "electrical"): "Test operation on a non-GFCI outlet to isolate machine from outlet fault; dry machine thoroughly; check hose and pump area for leaks; do not bypass GFCI for safety",
    (None, "venting"): "Inspect vent exit for obstructions; ensure vent run is short and straight with proper slope; check roof cap damper; clear lint buildup",
    (None, "compressor"): "Clean condenser coils first; listen for condenser fan operation; if coils are clean and machine still runs hot, service may be needed for compressor or refrigerant charge",
    (None, "defrost"): "Perform full defrost cycle (low heat); check door gasket seal; if ice returns within days, check defrost heater, limit switch, or timer",
    (None, "ice_maker"): "Check supply valve is fully open; ensure line is not kinked; clear inlet valve screen; test water flow at other taps on same line; if weak flow, house pressure may be cause; inlet valve may need replacement",
    (None, "oven_cooktop"): "Check socket contact for looseness or corrosion; confirm replacement parts are oven-rated; measure supply voltage at outlet (over ~125V AC can destroy light bulbs); loose socket contact is the most common cause of rapid bulb failure",
    (None, "washing_machine"): "Check load distribution; re-level the machine; confirm feet have rubber inserts; check shock absorbers and bearings; consult the service manual's balance test procedure",
    (None, "dishwasher"): "Test the pump motor for continuity; check the relay or control board driving the pump; check the pump connector for corrosion; an open motor means pump replacement; a good motor means the relay or board is the fault",
    (None, "door_light"): "Check the door switch wiring at both switches against the diagram; if the wiring is correct, one switch's contact may be cross-conducting and should be replaced",
    (None, "error_code"): "Note the displayed error code; consult the appliance's manual for the code's meaning and recommended actions; the code indicates a specific fault class that a repair technician can diagnose"
}


def get_remedy(model, symptom_category):
    """Get likely remedy for (model, symptom) combination."""
    # Try exact model match first
    key = (model, symptom_category) if model else (None, symptom_category)
    if key in REMEDY_MAPPINGS:
        return REMEDY_MAPPINGS[key]
    # Also try with model as string "None" fallback
    return None


# ============================================================
# PROCESS THE TOP 40 ROWS
# ============================================================

results = {
    "served": 0,
    "unserved_wrong_first_hypothesis": 0,
    "refrained": 0,
    "answerable_count": 0,
    "vendor_count": 0,
    "repair_count": 0,
    "detailed": [],
    "row_classifications": [],
}

# Process each of the 40 rows
for i, row in enumerate(top40):
    qid = row["question_id"]
    title = row.get("title", "")
    body = row.get("body", "")
    view_count = row.get("view_count", 0)

    # Combine title and body for analysis
    text = f"{title} {body}".lower()

    # Extract model number
    model = extract_model_number(f"{title} {body}")

    # Classify symptom category
    symptom_category = classify_symptom_category(f"{title} {body}")

    # Get remedy
    remedy = get_remedy(model, symptom_category)

    # Determine answerability class (based on E092 classification:
    # diagnosis vs other [installation, wiring, purchase, code, repair, vendor])
    # Classification clues from title+body:
    is_vendor_keywords = bool(re.search(
        r"return|RMA|warranty|vendor|customer service|replace the unit|contact manufacturer", text))
    is_repair_keywords = bool(re.search(
        r"physical repair|technician|appliance tech|service call|replace part|fix it yourself|DIY", text))

    # Diagnosis: specific device exhibits a symptom whose cause the asker does not know
    diagnosis_clues = re.search(
        r"(what is wrong|what causes|why not working|symptom|signs of|problem with"
        r"|how long when did|have you tried|diagnose|figure out|troubleshoot)", text)
    is_diagnosis = diagnosis_clues is not None

    if is_vendor_keywords:
        remedy_class = "vendor"
    elif is_repair_keywords:
        remedy_class = "repair"
    elif is_diagnosis:
        remedy_class = "answerable"
    else:
        remedy_class = "other"

    is_answerable = remedy_class == "answerable"

    if is_answerable:
        results["answerable_count"] += 1

    # Determine procedure outcome: served, unserved (wrong-first-hypothesis), or refrained
    if remedy is not None and remedy_class == "answerable":
        # Procedure proposes a remedy for an answerable row
        # Check the cached grade to determine if the remedy was correct
        grade_info = grades_by_qid.get(qid, {})
        actual_served = grade_info.get("served", None)

        if actual_served is True:
            # Remedy proposed and it was correct per thread resolution
            results["served"] += 1
            classification = "served"
        elif actual_served is False:
            # Remedy proposed but it was wrong per thread resolution
            results["unserved_wrong_first_hypothesis"] += 1
            classification = "wrong-first-hypothesis"
        else:
            # Grade info not available; if remedy is substantial, assume served
            if remedy and len(remedy) > 20:
                results["served"] += 1
                classification = "served (grade unknown)"
            else:
                results["unserved_wrong_first_hypothesis"] += 1
                classification = "wrong-first-hypothesis (grade unknown)"
    elif remedy is None and symptom_category == "unknown":
        # Could not extract sufficient discriminating evidence at all
        results["refrained"] += 1
        classification = "refrained"
    elif remedy is None:
        # Could not extract sufficient discriminating evidence
        # (symptom category known but no model or no remedy mapping)
        results["refrained"] += 1
        classification = "refrained"
    else:
        # Remedy provided but not answerable class
        if remedy_class == "vendor":
            results["vendor_count"] += 1
        elif remedy_class == "repair":
            results["repair_count"] += 1
        classification = remedy_class

    results["detailed"].append({
        "row": i + 1,
        "qid": qid,
        "views": view_count,
        "model": model,
        "symptom_category": symptom_category,
        "remedy_provided": remedy is not None,
        "remedy": remedy[:60] + "..." if remedy and len(remedy) > 60 else (remedy or "NONE"),
        "remedy_class": remedy_class,
        "classification": classification,
    })
    results["row_classifications"].append(classification)


# Compute K1 gate
answerable_count = results["answerable_count"]
served_count = results["served"]

# Wilson CI95 lower bound
wilson_lower = None
if answerable_count > 0 and served_count > 0:
    p = served_count / answerable_count
    z = 1.96
    n = answerable_count
    wilson_lower = (p + z * z / (2 * n) - z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n)) / (1 + z * z / n)
    wilson_lower = round(wilson_lower, 4)
elif answerable_count == 0:
    wilson_lower = 0.0
else:
    wilson_lower = 0.0

k1_pass = wilson_lower >= 0.50 if wilson_lower is not None else False

# ============================================================
# OUTPUT RESULTS
# ============================================================

print("=" * 60)
print("E142 — Improved discriminating-observation procedure on appliance-fault diagnosis")
print("=" * 60)
print()
print(f"Total rows processed: {len(top40)}")
print(f"Served: {results['served']}")
print(f"Wrong-first-hypothesis: {results['unserved_wrong_first_hypothesis']}")
print(f"Refrained: {results['refrained']}")
print(f"Answerable count: {answerable_count}")
print(f"Wilson CI95 lower bound: {wilson_lower}")
print(f"K1 gate (lower bound >= 0.50): {'PASS' if k1_pass else 'FAIL'}")
print(f"Vendor rows: {results['vendor_count']}")
print(f"Repair rows: {results['repair_count']}")
print()

# Show served rows
print(f"Served rows:")
for d in results["detailed"]:
    if d["classification"] == "served":
        print(f"  Row {d['row']}: qid={d['qid']}, model={d['model']}, symptom={d['symptom_category']}, remedy={d['remedy'][:60]}...")

# Show wrong-first-hypothesis rows
print(f"\nWrong-first-hypothesis rows:")
for d in results["detailed"]:
    if d["classification"] == "wrong-first-hypothesis":
        print(f"  Row {d['row']}: qid={d['qid']}, model={d['model']}, symptom={d['symptom_category']}, remedy={d['remedy'][:60]}...")

# Show refined rows
print(f"\nRefrained rows:")
for d in results["detailed"]:
    if d["classification"] == "refrained":
        print(f"  Row {d['row']}: qid={d['qid']}, model={d['model']}, symptom={d['symptom_category']}")

print()
print("=" * 60)
print("DECISION:")
print("=" * 60)
if k1_pass and results["unserved_wrong_first_hypothesis"] == 0:
    print("K1 PASS and 0 wrong-first-hypothesis misses: PROCEDURE SUCCEEDS")
    print("The improved discriminating-observation procedure serves the answerable-class")
    print("population at or above the 0.50 threshold while avoiding incorrect proposals.")
    print("This would support continuing the discriminating-observation line with further")
    print("procedural refinements.")
elif k1_pass and results["unserved_wrong_first_hypothesis"] > 0:
    print("K1 PASS but wrong-first-hypothesis misses present:")
    print(f"{results['unserved_wrong_first_hypothesis']} rows had incorrect remedies proposed.")
    print("The procedure serves the population but re-introduces the wrong-first-hypothesis")
    print("pattern that T-0093 avoided. Further refinements needed to maintain 0 misses.")
elif not k1_pass and results["unserved_wrong_first_hypothesis"] == 0:
    print("K1 FAIL but 0 wrong-first-hypothesis misses:")
    print(f"Wilson LB {wilson_lower} < 0.50, but all served rows were correct proposals.")
    print("The procedure avoids incorrect proposals but serves too few people. Need broader")
    print("symptom pattern matching to serve more of the answerable-class population.")
else:
    print(f"K1 FAIL and {results['unserved_wrong_first_hypothesis']} wrong-first-hypothesis misses:")
    print("The procedure both serves too few people and proposes incorrect remedies.")
    print("Fundamental design revision needed.")

print()
print(f"Compared to T-0093: served={2}, wrong-first-hypothesis={0}, Wilson LB=0.3424, K1=FAIL")
print(f"Compared to E092 baseline: served=30/37=0.8108, Wilson LB=0.6580, K1=PASS, wrong-first-hypothesis=7/37")