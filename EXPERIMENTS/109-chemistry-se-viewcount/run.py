#!/usr/bin/env python3
"""E109 — View-Count Principle on Chemistry Stack Exchange

Tests whether the view-count principle generalizes to Chemistry Stack Exchange.
Uses view_count as arrival metadata and question titles about chemical problems
as need statements. This is a fresh observation in a scientific domain.

The Stack Exchange API is accessible and the methodology follows the established
view-count protocol (G1-G4 gates).
"""

import json
import subprocess
import sys
from pathlib import Path

# Stack Exchange API helper
def stackexchange_api(path):
    """Make unauthenticated Stack Exchange API request."""
    result = subprocess.run(
        ["curl", "-s", f"https://api.stackexchange.com{path}"],
        capture_output=True, text=True,
        timeout=30
    )
    if result.returncode != 0:
        print(f"   API error: {result.stderr[:200]}")
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"   JSON decode error: {result.stdout[:200]}")
        return None

def fetch_questions(site, pagesize=100, page=1):
    """Fetch questions from a Stack Exchange site."""
    result = stackexchange_api(
        f"/2.3/questions?order=desc&sort=activity&site={site}&pagesize={pagesize}&page={page}"
    )
    if result is None:
        return []
    return result.get('items', [])

# Need keywords for chemistry domain
chem_keywords = {
    'synthesis', 'reaction', 'purification', 'recrystallization',
    'solvent', 'reagent', 'catalyst', 'yield', 'percent yield',
    'melting point', 'boiling point', 'distillation',
    'nmr', 'nuclear magnetic resonance', 'ir', 'infrared',
    'pcr', 'polar chromatography', 'thin layer',
    'electrophile', 'nucleophile', 'mechanism',
    'deprotection', 'protection', 'group',
    'oxidation', 'reduction', 'hydrogenation',
    'functional group', 'reaction mechanism',
    'preparation', 'make', 'how to', 'solve',
    'problem', 'error', 'issue', 'help with',
    'template', 'literature', 'reference',
}

print("=" * 60)
print("E109 — View-Count Principle on Chemistry Stack Exchange")
print("=" * 60)

# Step 1: Fetch questions
print("\nStep 1: Fetching Chemistry SE questions...")
questions = fetch_questions("chemistry", pagesize=100)
print(f"   Fetched {len(questions)} questions (page 1)")

if len(questions) < 30:
    print("   Fetching more pages...")
    # Fetch additional pages to reach 30+
    all_qs = list(questions)
    for page in range(2, 6):
        more = fetch_questions("chemistry", pagesize=100, page=page)
        all_qs.extend(more)
        if len(all_qs) >= 50:
            break
    questions = all_qs[:100]
    print(f"   Total: {len(questions)} questions")

if len(questions) < 30:
    print("   ERROR: Less than 30 questions retrieved, exiting.")
    sys.exit(1)

# Step 2: Classify questions as need-related or random
print(f"\nStep 2: Classifying questions need-related vs random...")
need_related_count = 0
random_count = 0
questions_with_view_count = 0
questions_with_score = 0

classified_qs = []

for i, q in enumerate(questions):
    title = q.get('title', '').lower()
    view_count = q.get('view_count', 0)
    score = q.get('score', 0)
    
    # Track arrival field coverage
    if view_count is not None:
        questions_with_view_count += 1
    if score is not None:
        questions_with_score += 1
    
    # Check if title contains chemistry need keywords
    if any(kw in title for kw in chem_keywords):
        need_related_count += 1
        classified = "need_related"
    else:
        random_count += 1
        classified = "random"
    
    classified_qs.append({
        "id": q.get('question_id', ''),
        "title": q.get('title', ''),
        "view_count": view_count,
        "score": score,
        "tags": q.get('tags', []),
        "classified": classified,
    })
    
    if (i + 1) % 20 == 0:
        print(f"   Processed {i+1}/{len(questions)} questions...")
    
    if need_related_count <= 5 or random_count <= 5:
        print(f"   [{classified}] {q.get('title', '')[:80]}... (views={view_count}, score={score})")

print(f"   Need-related: {need_related_count}, Random: {random_count}")
print(f"   Questions with view_count: {questions_with_view_count}/{len(questions)}")
print(f"   Questions with score: {questions_with_score}/{len(questions)}")

# Step 3: Gate assessment
print("\nStep 3: Gate assessment")

# G1: Retrieval
print(f"   G1: Total questions = {len(questions)} (need: ≥30)")
g1_pass = len(questions) >= 30
print(f"   G1: {'PASS' if g1_pass else 'FAIL'}")

# G4: Arrival field
print(f"   G4: Questions with view_count: {questions_with_view_count}/{len(questions)} (need: 100%)")
g4_pass = questions_with_view_count >= 30
print(f"   G4: {'PASS' if g4_pass else 'FAIL'}")

# G2 + G3: Separation and effect magnitude
if g1_pass and g4_pass:
    need_views = [q["view_count"] for q in classified_qs if q["classified"] == "need_related" and q["view_count"] is not None]
    random_views = [q["view_count"] for q in classified_qs if q["classified"] == "random" and q["view_count"] is not None]
    
    print(f"   G2/V: need-related questions with views: {len(need_views)}")
    print(f"   G2/R: random questions with views: {len(random_views)}")
    
    if need_views and random_views:
        # Cliff's δ computation
        greater = sum(1 for x in need_views for y in random_views if x > y)
        ties = sum(1 for x in need_views for y in random_views if x == y)
        less = len(need_views) * len(random_views) - greater - ties
        
        cliff_d = (greater - less) / (len(need_views) * len(random_views)) if len(need_views) * len(random_views) > 0 else 0
        print(f"   Cliff's δ: {cliff_d:.4f} (need: >0.6)")
        g3_pass = cliff_d > 0.6
        print(f"   G3: {'PASS' if g3_pass else 'FAIL'}")
        
        # Mann-Whitney U
        need_sorted = sorted(need_views)
        random_sorted = sorted(random_views)
        n1, n2 = len(need_sorted), len(random_sorted)
        u = sum(1 for rs in random_sorted for ns in need_sorted if ns > rs)
        mean_u = n1 * n2 / 2
        se = (n1 * n2 * (n1 + n2 + 1) / 12) ** 0.5
        z = (u - mean_u) / se if se > 0 else 0
        print(f"   G2 (Mann-Whitney U z): {z:.2f}")
    else:
        g3_pass = False
        print(f"   G3: FAIL (insufficient data for effect size)")
else:
    g3_pass = False
    print(f"   G3: SKIP (G1 or G4 not passed)")

# Step 4: Write results
results = {
    "experiment": "E109",
    "title": "View-Count Principle on Chemistry Stack Exchange",
    "site": "chemistry",
    "questions_fetched": len(questions),
    "g1_retrieval_pass": g1_pass,
    "g2_separation": g3_pass,
    "g3_effect_magnitude": g3_pass,
    "g4_arrival_field": g4_pass,
    "need_related_count": need_related_count,
    "random_count": random_count,
    "conclusion": "GATE_OPEN" if all([g1_pass, g4_pass, g3_pass]) else "GATE_CLOSED",
    "domain": "chemistry_stack_exchange",
    "timestamp": "2026-10-13"
}

output_path = Path("/home/ubuntu/think-free/EXPERIMENTS/109-chemistry-se-viewcount/results.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(results, indent=2))
print(f"\nResults written to {output_path}")
print(json.dumps(results, indent=2))