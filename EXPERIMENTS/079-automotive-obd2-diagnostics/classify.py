#!/usr/bin/env python3
"""
E079 — Classification helpers for Mechanics.SE data.
"""

import re
from typing import Any, Dict, List, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# OBD2 code pattern
OBD2_PATTERN = re.compile(r'\b[PBCU][0-9]{4}\b')

# Vehicle make normalization
MAKE_ALIASES = {
    "chevy": "chevrolet",
    "v.w.": "volkswagen",
    "vw": "volkswagen",
    "mercedes": "mercedes-benz",
    "benz": "mercedes-benz",
    "bmw": "bmw",
    "toyota": "toyota",
    "honda": "honda",
    "ford": "ford",
    "nissan": "nissan",
    "hyundai": "hyundai",
    "kia": "kia",
}

KNOWN_MAKES = {
    "toyota", "honda", "ford", "chevrolet", "nissan", "hyundai", "kia",
    "bmw", "mercedes-benz", "audi", "volkswagen", "subaru", "mazda",
    "dodge", "jeep", "chrysler", "ram", "gmc", "buick", "cadillac",
    "lexus", "infiniti", "acura", "volvo", "porsche", "mini",
}


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------

def extract_vehicle_config(question: Dict) -> Tuple[str, str, str, str]:
    """Extract (make, model, year, engine) from question tags and body."""
    tags = [t.lower() for t in question.get("tags", [])]
    title = question.get("title", "").lower()
    body = question.get("body", "").lower()

    make = ""
    model = ""
    year = ""
    engine = ""

    # Known make tags
    for tag in tags:
        if tag in MAKE_ALIASES:
            make = MAKE_ALIASES[tag]
            break
        if tag in KNOWN_MAKES:
            make = tag
            break

    # Model often appears as tag like "camry", "civic", "f-150"
    model_candidates = [t for t in tags if t not in MAKE_ALIASES.values() and t not in KNOWN_MAKES and len(t) > 2]
    if model_candidates:
        model = model_candidates[0]

    # Year extraction from title/body
    year_match = re.search(r'\b(19[89]\d|20[0-2]\d)\b', title + " " + body)
    if year_match:
        year = year_match.group(1)

    # Engine extraction - look for patterns like "2.5l", "3.5 v6", "2.0 turbo"
    engine_patterns = [
        r'\b(\d\.\d[lL])\b',
        r'\b(\d\.\d\s*[vV]\d)\b',
        r'\b(\d\.\d\s*[tT]urbo)\b',
        r'\b(\d\.\d\s*[dD]iesel)\b',
    ]
    for pattern in engine_patterns:
        match = re.search(pattern, title + " " + body)
        if match:
            engine = match.group(1).lower()
            break

    return make, model, year, engine


def get_best_answer(question: Dict) -> Dict | None:
    """Get the accepted answer, or highest-scored answer with score >= 3."""
    answers = question.get("answers", [])
    if not answers:
        return None

    # Find accepted answer
    for ans in answers:
        if ans.get("is_accepted", False):
            return ans

    # Find highest-scored answer with score >= 3
    qualified = [a for a in answers if a.get("score", 0) >= 3]
    if qualified:
        return max(qualified, key=lambda a: a.get("score", 0))

    return None


def answerer_is_qualified(answer: Dict) -> bool:
    """Check if answerer has reputation > 100."""
    owner = answer.get("owner", {})
    reputation = owner.get("reputation", 0)
    return reputation > 100


def classify_root_cause_specificity(answer_body: str) -> int:
    """
    Classify root cause specificity level (0-5).
    This is a heuristic - real classification needs human review.
    """
    body_lower = answer_body.lower()

    # Level 0: No root cause
    if not any(kw in body_lower for kw in ["replace", "repair", "fix", "cause", "fault", "bad", "failed", "leak"]):
        return 0

    # Level 1: Generic diagnostic
    generic_phrases = [
        "check wiring", "check connector", "inspect wiring", "check for vacuum leak",
        "diagnose further", "scan for codes", "check fuse", "check relay",
        "verify voltage", "check ground", "look for damage"
    ]
    if any(phrase in body_lower for phrase in generic_phrases):
        # But might also have specific part - check further
        pass

    # Level 4-5: Specific part indicators
    specific_indicators = [
        r"bank \d sensor \d",           # O2 sensor location
        r"part #?\s*\w+",               # Part number
        r"p/n\s*\w+",                   # Part number
        r"\b(o2|oxygen) sensor\b.*bank", # O2 sensor with bank
        r"\b(maf|map|tps|iat|ect|ckp|cmp) sensor\b", # Specific sensor types
        r"\b(evap|purge|vent) valve\b", # Specific valves
        r"\b(fuel|injector) (pump|injector)\b", # Fuel system
        r"\b(ignition|coil) (pack|coil)\b", # Ignition
        r"\b(catalytic converter|cat)\b", # Cat
        r"\b(thermostat|water pump|radiator)\b", # Cooling
    ]

    for pattern in specific_indicators:
        if re.search(pattern, body_lower):
            # Check if it also has procedure (Level 5)
            procedure_kws = ["replace", "install", "torque", "remove", "swap", "change"]
            if any(kw in body_lower for kw in procedure_kws):
                return 5
            return 4

    # Level 3: Component category
    category_indicators = [
        r"\b(o2|oxygen) sensor\b",
        r"\b(maf|map|tps|iat|ect|ckp|cmp) sensor\b",
        r"\b(evap|purge|vent) (valve|solenoid)\b",
        r"\b(fuel pump|fuel injector)\b",
        r"\b(ignition coil|coil pack)\b",
        r"\bcatalytic converter\b",
        r"\bthermostat\b",
        r"\bwater pump\b",
        r"\bradiator\b",
        r"\babs sensor\b",
        r"\bwheel speed sensor\b",
    ]
    for pattern in category_indicators:
        if re.search(pattern, body_lower):
            return 3

    # Level 2: System/subsystem
    system_indicators = [
        "evap system", "evap leak", "fuel system", "ignition system",
        "cooling system", "exhaust system", "intake system", "vacuum leak",
        "emission system", "transmission", "abs system"
    ]
    if any(sys in body_lower for sys in system_indicators):
        return 2

    # Level 1: Generic diagnostic (default if repair language present)
    return 1


def is_structured_case(question: Dict) -> bool:
    """Check if question meets structured case criteria."""
    # Has OBD2 code
    if not question.get("obd2_codes"):
        return False

    # Has qualified answer
    best = get_best_answer(question)
    if not best:
        return False

    if not answerer_is_qualified(best):
        return False

    # Answer names root cause (heuristic: specificity >= 2)
    specificity = classify_root_cause_specificity(best.get("body", ""))
    if specificity < 2:
        return False

    # Vehicle identifiable
    make, model, year, engine = extract_vehicle_config(question)
    if not (make and year):
        return False

    return True


def get_structured_cases(questions: List[Dict]) -> List[Dict]:
    """Filter and enrich structured cases."""
    structured = []
    for q in questions:
        if is_structured_case(q):
            best = get_best_answer(q)
            make, model, year, engine = extract_vehicle_config(q)
            q_enriched = q.copy()
            q_enriched["vehicle_config"] = (make, model, year, engine)
            q_enriched["best_answer"] = best
            q_enriched["specificity"] = classify_root_cause_specificity(best.get("body", ""))
            structured.append(q_enriched)
    return structured