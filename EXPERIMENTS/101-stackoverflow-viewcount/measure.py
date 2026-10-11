#!/usr/bin/env python3
"""
Measure served/unserved fraction for NEED-classified Stack Overflow questions.

Per E078 three-clause rubric:
- SERVED: Has answer with score >= 1 that provides actionable solution (code, config, command)
- PARTIALLY_SERVED: Has answer with score >= 1 that provides partial guidance (link, concept, workaround)
- UNSERVED: No answer with score >= 1, or answers are irrelevant/incorrect
"""

import json
import time
import sys
import re
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

CLASSIFIED_FILE = Path(__file__).parent / "raw" / "classified.jsonl"
OUT_FILE = Path(__file__).parent / "raw" / "measured.jsonl"
GATES_FILE = Path(__file__).parent / "raw" / "gates_g3_g4.json"

BASE_URL = "https://api.stackexchange.com/2.3"

# Actionable solution indicators
ACTIONABLE_PATTERNS = [
    r"```",  # code blocks
    r"`[^`]+`",  # inline code
    r"\btry\s+(this|the following)\b",
    r"\buse\s+(this|the following)\b",
    r"\bhere\s+(is|'s)\s+(a|the)\s+(solution|fix|code|example)\b",
    r"\badd\s+(this|the following)\b",
    r"\bchange\s+(this|the following)\b",
    r"\breplace\s+(this|the following)\b",
    r"\bset\s+\w+\s*=\s*\w+",
    r"\bimport\s+\w+",
    r"\bfrom\s+\w+\s+import\b",
    r"\binstall\s+\w+",
    r"\bnpm\s+install\b",
    r"\bpip\s+install\b",
    r"\bcargo\s+add\b",
    r"\bgo\s+get\b",
    r"\bmvn\s+install\b",
    r"\bgradle\s+add\b",
    r"\bconfig(?:ure)?\b",
    r"\.json\b",
    r"\.yaml\b",
    r"\.yml\b",
    r"\.xml\b",
    r"\.ini\b",
    r"\.conf\b",
    r"\benv\b",
    r"\bexport\s+\w+",
    r"\bset\s+\w+\s*=",
]

PARTIAL_PATTERNS = [
    r"\bsee\s+(also|the|this)\b",
    r"\bcheck\s+(out|the)\b",
    r"\blink\s*:",
    r"https?://",
    r"\bdocumentation\b",
    r"\bdocs?\b",
    r"\brefer\s+to\b",
    r"\blook\s+(at|into)\b",
    r"\bworkaround\b",
    r"\balternative\w*\b",
    r"\binstead\s+of\b",
    r"\btry\s+(using|a different)\b",
    r"\bconsider\s+(using|a)\b",
]

actionable_re = [re.compile(p, re.IGNORECASE) for p in ACTIONABLE_PATTERNS]
partial_re = [re.compile(p, re.IGNORECASE) for p in PARTIAL_PATTERNS]

def fetch_answers(question_ids: list) -> dict:
    """Fetch answers for a list of question IDs (max 100 per request)."""
    ids_str = ";".join(str(qid) for qid in question_ids)
    # Filter !9Z(-wzftf includes body_markdown
    url = f"{BASE_URL}/questions/{ids_str}/answers?order=desc&sort=votes&site=stackoverflow&pagesize=100&filter=!9Z(-wzftf"
    req = Request(url, headers={"User-Agent": "think-free/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.load(resp)
            return data
    except HTTPError as e:
        if e.code == 429:
            print(f"Rate limited, waiting 60s...", file=sys.stderr)
            time.sleep(60)
            return fetch_answers(question_ids)
        raise
    except URLError as e:
        print(f"Network error fetching answers: {e}", file=sys.stderr)
        raise

def classify_answer(answer_body: str) -> str:
    """Classify answer as ACTIONABLE, PARTIAL, or NONE."""
    if not answer_body:
        return "NONE"
    
    # Check for actionable patterns
    for pattern in actionable_re:
        if pattern.search(answer_body):
            return "ACTIONABLE"
    
    # Check for partial patterns
    for pattern in partial_re:
        if pattern.search(answer_body):
            return "PARTIAL"
    
    # If answer has substantial length (>200 chars) but no clear pattern, treat as partial
    if len(answer_body) > 200:
        return "PARTIAL"
    
    return "NONE"

def classify_question_served(answers: list) -> str:
    """Classify question as SERVED, PARTIALLY_SERVED, or UNSERVED based on its answers."""
    if not answers:
        return "UNSERVED"
    
    # Sort by score descending
    sorted_answers = sorted(answers, key=lambda a: a.get("score", 0), reverse=True)
    
    # Check top answers with score >= 1
    for answer in sorted_answers:
        score = answer.get("score", 0)
        if score < 1:
            break  # No more answers with score >= 1
        
        body = answer.get("body_markdown", "")
        classification = classify_answer(body)
        if classification == "ACTIONABLE":
            return "SERVED"
        elif classification == "PARTIAL":
            # Keep checking for actionable, but remember partial
            pass
    
    # Check if any answer with score >= 1 was PARTIAL
    for answer in sorted_answers:
        score = answer.get("score", 0)
        if score < 1:
            break
        body = answer.get("body_markdown", "")
        if classify_answer(body) == "PARTIAL":
            return "PARTIALLY_SERVED"
    
    return "UNSERVED"

def main():
    if not CLASSIFIED_FILE.exists():
        print(f"Classified file not found: {CLASSIFIED_FILE}", file=sys.stderr)
        sys.exit(1)
    
    # Load NEED-classified questions
    need_questions = []
    with open(CLASSIFIED_FILE) as f:
        for line in f:
            q = json.loads(line)
            if q["classification"] == "NEED":
                need_questions.append(q)
    
    print(f"NEED questions to measure: {len(need_questions)}", file=sys.stderr)
    
    # Fetch answers in batches of 100
    measured = []
    batch_size = 100
    for i in range(0, len(need_questions), batch_size):
        batch = need_questions[i:i+batch_size]
        qids = [q["question_id"] for q in batch]
        
        print(f"Fetching answers for batch {i//batch_size + 1}/{(len(need_questions)-1)//batch_size + 1} ({len(qids)} questions)...", file=sys.stderr)
        
        try:
            data = fetch_answers(qids)
            answers_by_qid = {}
            for ans in data.get("items", []):
                qid = ans.get("question_id")
                if qid not in answers_by_qid:
                    answers_by_qid[qid] = []
                answers_by_qid[qid].append(ans)
            
            for q in batch:
                qid = q["question_id"]
                answers = answers_by_qid.get(qid, [])
                served_class = classify_question_served(answers)
                
                measured.append({
                    "question_id": qid,
                    "title": q["title"],
                    "view_count": q["view_count"],
                    "answer_count": q["answer_count"],
                    "score": q["score"],
                    "tags": q["tags"],
                    "served_classification": served_class,
                    "num_answers_fetched": len(answers),
                    "top_answer_score": max([a.get("score", 0) for a in answers], default=0),
                })
            
            time.sleep(0.5)  # Rate limit
            
        except Exception as e:
            print(f"Error fetching batch {i//batch_size + 1}: {e}", file=sys.stderr)
            # Mark batch as error
            for q in batch:
                measured.append({
                    "question_id": q["question_id"],
                    "title": q["title"],
                    "view_count": q["view_count"],
                    "served_classification": "ERROR",
                    "error": str(e),
                })
            continue
    
    # Save measured results
    with open(OUT_FILE, "w") as f:
        for m in measured:
            f.write(json.dumps(m) + "\n")
    
    # Compute G3 statistics
    valid = [m for m in measured if m["served_classification"] != "ERROR"]
    served = [m for m in valid if m["served_classification"] == "SERVED"]
    partial = [m for m in valid if m["served_classification"] == "PARTIALLY_SERVED"]
    unserved = [m for m in valid if m["served_classification"] == "UNSERVED"]
    
    total = len(valid)
    served_frac = len(served) / total if total > 0 else 0
    partial_frac = len(partial) / total if total > 0 else 0
    unserved_frac = len(unserved) / total if total > 0 else 0
    
    # Wilson CI95 for unserved fraction
    import math
    def wilson_ci(p, n, z=1.96):
        if n == 0:
            return (0, 1)
        denom = 1 + z**2 / n
        centre = (p + z**2 / (2*n)) / denom
        half = z * math.sqrt(p*(1-p)/n + z**2/(4*n**2)) / denom
        return (max(0, centre - half), min(1, centre + half))
    
    ci_lower, ci_upper = wilson_ci(unserved_frac, total)
    
    print(f"\nTotal valid: {total}")
    print(f"SERVED: {len(served)} ({served_frac:.3f})")
    print(f"PARTIALLY_SERVED: {len(partial)} ({partial_frac:.3f})")
    print(f"UNSERVED: {len(unserved)} ({unserved_frac:.3f})")
    print(f"Unserved fraction Wilson CI95: [{ci_lower:.3f}, {ci_upper:.3f}]")
    
    # G3 gate: unserved fraction CI95 upper bound < 60%
    g3_pass = ci_upper < 0.60
    print(f"G3 (unserved CI95 upper < 0.60): {'PASS' if g3_pass else 'FAIL'} (upper={ci_upper:.3f})")
    
    # G4 gate: view_count coverage 100%
    view_count_coverage = sum(1 for m in valid if "view_count" in m and m["view_count"] > 0) / total if total > 0 else 0
    g4_pass = view_count_coverage == 1.0
    print(f"G4 (view_count coverage): {view_count_coverage:.3f} ({'PASS' if g4_pass else 'FAIL'})")
    
    # Save gates
    gates = {
        "G3_unserved_fraction": unserved_frac,
        "G3_unserved_ci_lower": ci_lower,
        "G3_unserved_ci_upper": ci_upper,
        "G3_pass": g3_pass,
        "G4_view_count_coverage": view_count_coverage,
        "G4_pass": g4_pass,
        "served_counts": {
            "SERVED": len(served),
            "PARTIALLY_SERVED": len(partial),
            "UNSERVED": len(unserved),
            "ERROR": len(measured) - total,
        },
        "total_valid": total,
    }
    
    with open(GATES_FILE, "w") as f:
        json.dump(gates, f, indent=2)
    print(f"Gate results saved to {GATES_FILE}")

if __name__ == "__main__":
    main()