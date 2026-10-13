#!/usr/bin/env python3
"""
E121 — Fetch Code Review Stack Exchange data for E119 matched-harvest measurement.

Uses Stack Exchange API to fetch Code Review questions, then applies
the E119 classifier_v3 with matched-harvest design.
"""

import json
import sys
import urllib.request
from pathlib import Path

# Import classifier_v3 from E119 prototype
import sys
from pathlib import Path
# Get the absolute path to the repository root, then to 119-viewcount-prototype
repo_root = Path(__file__).resolve().parent.parent.parent
e119_path = repo_root / "EXPERIMENTS" / "119-viewcount-prototype"
sys.path.insert(0, str(e119_path))
# Change to E119 dir for relative imports in classifier_v3
old_cwd = Path.cwd()
import os
os.chdir(e119_path)
from classifier_v3 import compute_coverage
os.chdir(old_cwd)
import re


def fetch_codereview_questions(tags=None, pages_per_tag=5, min_view_count=500, max_total=1000):
    """
    Fetch questions from Code Review Stack Exchange API.
    
    Returns list of question dicts with standard fields.
    """
    if tags is None:
        # Code Review relevant tags - use fewer to avoid rate limits
        tags = ["python", "refactoring", "performance", "debugging"]
    
    BASE_URL = "https://api.stackexchange.com/2.3"
    PAGESIZE = 100
    all_questions = []
    
    # Use activity sort like E100, which worked
    # Add delay between requests to avoid rate limiting
    import time
    
    for tag in tags:
        tag_questions = []
        for page in range(1, pages_per_tag + 1):
            url = (
                f"{BASE_URL}/questions"
                f"?order=desc&sort=activity&tagged={tag}&site=codereview"
                f"&pagesize={PAGESIZE}&page={page}"
            )
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "think-free/E121"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.load(resp)
                    items = data.get("items", [])
                    if not items:
                        break
                    tag_questions.extend(items)
                    if not data.get("has_more", False):
                        break
            except Exception as e:
                print(f"Error fetching {tag} page {page} on codereview: {e}", file=sys.stderr)
                continue
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        # Filter for min view count
        filtered = [
            q for q in tag_questions
            if q.get("view_count", 0) >= min_view_count
        ]
        all_questions.extend(filtered)
        print(f"  Tag {tag}: {len(filtered)} items (view_count >= {min_view_count})", file=sys.stderr)
        
        if len(all_questions) >= max_total:
            break
    
    # Deduplicate by question_id
    seen = set()
    unique = []
    for q in all_questions:
        qid = q.get("question_id")
        if qid and qid not in seen:
            seen.add(qid)
            unique.append(q)
    
    # Sort by view_count descending (same metric for both arms - matched harvest)
    unique.sort(key=lambda q: q.get("view_count", 0), reverse=True)
    
    return unique[:max_total]


def save_jsonl(questions, output_path):
    """Save questions as JSONL with combined_text field for classification."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for q in questions:
            title = q.get("title", "")
            body = q.get("body", "")
            combined = f"{title} {body}" if body else title
            
            row = {
                "question_id": q.get("question_id"),
                "title": title,
                "body": body[:200] if body else "",
                "view_count": q.get("view_count", 0),
                "answer_count": q.get("answer_count", 0),
                "score": q.get("score", 0),
                "accepted_answer_id": q.get("accepted_answer_id"),
                "tags": q.get("tags", []),
                "combined_text": combined,
            }
            f.write(json.dumps(row) + "\n")
    
    print(f"Saved {len(questions)} questions to {output_path}", file=sys.stderr)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="E121 fetch Code Review SE data for E119 measurement")
    parser.add_argument("--output", "-o", type=str, default="data_codereview.jsonl",
                        help="Output JSONL file path")
    parser.add_argument("--size", type=int, default=300,
                        help="Target number of items (default: 300)")
    parser.add_argument("--min-views", type=int, default=500,
                        help="Minimum view_count threshold (default: 500)")
    parser.add_argument("--tags", type=str, nargs="+",
                        help="Tags to fetch (default: Code Review relevant tags)")
    args = parser.parse_args()
    
    questions = fetch_codereview_questions(
        tags=args.tags,
        pages_per_tag=3,
        min_view_count=args.min_views,
        max_total=args.size,
    )
    
    save_jsonl(questions, args.output)
    
    # Quick coverage check
    coverage_result = compute_coverage(questions)
    print(f"\n=== Coverage Check ===")
    print(f"Total: {coverage_result['total']}")
    print(f"Classified: {coverage_result['classified']} ({coverage_result['coverage']*100:.1f}%)")
    print(f"Need-related: {coverage_result['need_related']}")
    print(f"Random: {coverage_result['random']}")
    print(f"Unclassified: {coverage_result['unclassified']}")
    
    if coverage_result['coverage'] >= 0.60:
        print("✓ Coverage floor (60%) MET")
    else:
        print("✗ Coverage floor (60%) NOT MET")


if __name__ == "__main__":
    main()