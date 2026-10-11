#!/usr/bin/env python3
"""
Classify Stack Overflow questions as NEED or NOT-NEED per E078 three-clause rubric.

NEED: Question expresses a concrete technical need ("how do I...", "why does...", "error when...", "fix for...")
NOT-NEED: Homework, opinion, recommendation, meta, duplicate-closure-bait, debugging-without-context
"""

import json
import re
import sys
from pathlib import Path

IN_FILE = Path(__file__).parent / "raw" / "harvest.jsonl"
OUT_FILE = Path(__file__).parent / "raw" / "classified.jsonl"

# NEED patterns (question asks for help with a concrete technical problem)
NEED_PATTERNS = [
    # Direct question patterns
    r"\bhow\s+(do|to|can|would|could)\b",
    r"\bwhy\s+(does|is|do|did|would)\b",
    r"\bwhat\s+(is|are|does|do|causes?)\b",
    r"\bwhen\s+(does|do|would|should)\b",
    r"\bwhere\s+(is|are|do|does|can|to)\b",
    # Error/problem patterns
    r"\berror\s+(when|if|on|after|during)\b",
    r"\bfix\s+(for|the|this)\b",
    r"\bsolve[sd]?\b",
    r"\bresolve[sd]?\b",
    r"\bdebug\s+(this|the|my)\b",
    r"\bgetting\s+(error|exception)\b",
    r"\bfail(s|ed|ing)\s+(to|with)\b",
    r"\bnot\s+working\b",
    r"\bdoesn['']?t\s+work\b",
    r"\bunable\s+to\b",
    r"\bcan['']?t\s+(get|make|find|use)\b",
    r"\bhow\s+to\s+(fix|resolve|solve|debug)\b",
    r"\bhelp\s+(me\s+)?(with|fix|solve|debug)\b",
    r"\bissue\s+(with|when|after)\b",
    r"\bproblem\s+(with|when|after)\b",
    r"\btrouble\s+(with|when|after)\b",
    r"\bstuck\s+(on|with|at)\b",
    r"\bneed\s+(help|to|a)\b",
    r"\bwant\s+to\s+(know|understand|do)\b",
    # Technical question patterns (question mark + technical context)
    r"\bwhy\s+is\s+\w+\s+(not|failing|returning|giving)\b",
    r"\bwhat\s+causes?\s+\w+\b",
    r"\bhow\s+(can|do|to)\s+i\s+\w+\b",
    r"\bgetting\s+\w+\s+error\b",
    r"\bexception\s+(when|in|during)\b",
    r"\btype\s+error\b",
    r"\bsyntax\s+error\b",
    r"\bruntime\s+error\b",
    r"\bcompile\s+error\b",
    r"\bimport\s+error\b",
    r"\bmodule\s+not\s+found\b",
    r"\battribute\s+error\b",
    r"\bkey\s+error\b",
    r"\bindex\s+error\b",
    r"\bvalue\s+error\b",
    r"\bpermission\s+denied\b",
    r"\bconnection\s+(refused|timeout|error)\b",
    r"\btimeout\s+(error|expired)\b",
    r"\bout\s+of\s+memory\b",
    r"\bsegmentation\s+fault\b",
    r"\bnull\s+pointer\b",
    r"\bundefined\s+(variable|reference|function)\b",
]

# NOT-NEED patterns (homework, opinion, recommendation, meta)
NOT_NEED_PATTERNS = [
    r"\bhomework\b",
    r"\bassignment\b",
    r"\bexercise\b",
    r"\bbest\s+(practice|way|approach|library|tool|framework)\b",
    r"\brecommend\w*\b",
    r"\bsuggest\w*\b",
    r"\bopinion\b",
    r"\bvs\b|\bversus\b",
    r"\bcompare\w*\b",
    r"\bwhich\s+(is|are)\s+better\b",
    r"\bshould\s+i\s+use\b",
    r"\bwhat\s+(is|are)\s+the\s+(best|pros|cons)\b",
    r"\bpros\s+and\s+cons\b",
    r"\bduplicate\b",
    r"\bclosed\s+as\b",
    r"\bmigrate[sd]?\b",
    r"\bmeta\b",
    r"\bstack\s+overflow\b",
    r"\bhow\s+to\s+ask\b",
    r"\bdownvote\w*\b",
    r"\bclose\s+vote\b",
]

# Compile patterns
need_re = [re.compile(p, re.IGNORECASE) for p in NEED_PATTERNS]
not_need_re = [re.compile(p, re.IGNORECASE) for p in NOT_NEED_PATTERNS]

def classify_question(title: str, body: str = "") -> str:
    """Classify a question as NEED, NOT-NEED, or AMBIGUOUS."""
    text = f"{title} {body}".lower()
    
    # Check NOT-NEED first (stronger signal)
    for pattern in not_need_re:
        if pattern.search(text):
            return "NOT-NEED"
    
    # Check NEED patterns
    need_matches = sum(1 for pattern in need_re if pattern.search(text))
    if need_matches >= 1:
        return "NEED"
    
    # Check for question marks and technical terms
    if "?" in title and any(term in text for term in ["error", "exception", "bug", "issue", "problem", "fail", "not work", "crash", "null", "undefined", "syntax", "import", "module", "package", "library", "api", "function", "method", "class", "object", "variable", "loop", "array", "list", "dict", "string", "int", "float", "bool"]):
        return "NEED"
    
    return "AMBIGUOUS"

def main():
    if not IN_FILE.exists():
        print(f"Input file not found: {IN_FILE}", file=sys.stderr)
        sys.exit(1)
    
    counts = {"NEED": 0, "NOT-NEED": 0, "AMBIGUOUS": 0}
    classified = []
    
    with open(IN_FILE) as f:
        for line in f:
            q = json.loads(line)
            title = q.get("title", "")
            body = q.get("body", "")  # may not be present in default filter
            classification = classify_question(title, body)
            counts[classification] += 1
            
            classified.append({
                "question_id": q["question_id"],
                "title": title,
                "view_count": q["view_count"],
                "answer_count": q["answer_count"],
                "score": q["score"],
                "tags": q["tags"],
                "classification": classification,
            })
    
    # Save classified
    with open(OUT_FILE, "w") as f:
        for c in classified:
            f.write(json.dumps(c) + "\n")
    
    total = sum(counts.values())
    print(f"Total: {total}")
    print(f"NEED: {counts['NEED']} ({counts['NEED']/total*100:.1f}%)")
    print(f"NOT-NEED: {counts['NOT-NEED']} ({counts['NOT-NEED']/total*100:.1f}%)")
    print(f"AMBIGUOUS: {counts['AMBIGUOUS']} ({counts['AMBIGUOUS']/total*100:.1f}%)")
    
    # G2 gate: NEED concentration >= 30%
    need_frac = counts["NEED"] / total if total > 0 else 0
    print(f"\nG2 (NEED concentration): {need_frac:.3f} ({'PASS' if need_frac >= 0.30 else 'FAIL'})")
    
    # Save gate results
    gates = {
        "G1_population": total,
        "G1_pass": total >= 100,
        "G2_need_fraction": need_frac,
        "G2_pass": need_frac >= 0.30,
        "classification_counts": counts,
    }
    gates_file = Path(__file__).parent / "raw" / "gates_g1_g2.json"
    with open(gates_file, "w") as f:
        json.dump(gates, f, indent=2)
    print(f"Gate results saved to {gates_file}")

if __name__ == "__main__":
    main()