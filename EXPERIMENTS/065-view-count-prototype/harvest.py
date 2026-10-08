#!/usr/bin/env python3
"""E065 harvest: web search for need statements.

For each need statement in the treatment and control corpora, perform a
DuckDuckGo web search and record the results. The harvest produces raw data
that outcome.py uses for gate evaluation.

Usage:
    python3 harvest.py            # harvest both arms
    python3 harvest.py --arm 1    # harvest treatment arm only
    python3 harvest.py --arm 2    # harvest control arm only
"""

import json
import os
import re
import sys
import time
from urllib.parse import quote_plus

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Corpora paths
TREATMENT_CORPUS = os.path.join(HERE, "raw", "treatment-needs.jsonl")
CONTROL_CORPUS = os.path.join(HERE, "raw", "control-needs.jsonl")

# Output paths
TREATMENT_RESULTS = os.path.join(HERE, "raw", "treatment-results.jsonl")
CONTROL_RESULTS = os.path.join(HERE, "raw", "control-results.jsonl")

# DuckDuckGo search URL (no API key needed)
DDG_SEARCH_URL = "https://html.duckduckgo.com/html/search"

# polite delay between searches (seconds)
DELAY_BETWEEN_SEARCHES = 1.0


def load_corpus(path, limit=None):
    """Load need statements from a JSONL corpus.

    Each line should have at least a 'need_text' field.
    Returns a list of (id, need_text) tuples.
    """
    statements = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break
            try:
                obj = json.loads(line.strip())
                need_text = obj.get("need_text", "")
                if need_text:
                    statements.append((i, need_text))
            except (json.JSONDecodeError, KeyError):
                continue
    return statements


def duckduckgo_search(query, max_results=10):
    """Perform a DuckDuckGo search and return result titles/snippets.

    Returns a list of (title, snippet) tuples for the top results.
    """
    try:
        params = {"q": query}
        resp = requests.get(DDG_SEARCH_URL, params=params, timeout=15)
        if resp.status_code != 200:
            return []
        html = resp.text

        # Extract result blocks
        results = []
        # DuckDuckGo result headers are in <a class="result-title"> tags
        title_pattern = r'<a class="result-title"[^>]*>([^<]*</a>[^<]*)|<a class="result-title"[^>]*>([^<]+)</a>'
        # Simpler: find all result-title divs
        # Actually, let's use a more robust approach
        # Find all result divs
        result_starts = html.find('<div class="result"')
        while result_start >= 0 and len(results) < max_results:
            result_end = html.find("</div>", result_start)
            if result_end < 0:
                break
            result_html = html[result_start:result_end]

            # Extract title
            title_start = result_html.find('<a class="result-title"')
            if title_start >= 0:
                title_end = result_html.find(">", title_start)
                if title_end >= 0:
                    title_body = result_html[title_end + 1:]
                    title_close = title_body.find("</a>")
                    if title_close >= 0:
                        title = title_body[:title_close].strip()
                    else:
                        title = title_body.strip()
                else:
                    title = ""
            else:
                # Fallback: get first h3 or strong text
                title = ""

            # Extract snippet/description
            snippet_start = result_html.find('<a class="result-snippet"')
            if snippet_start >= 0:
                snippet_end = result_html.find(">", snippet_start)
                if snippet_end >= 0:
                    snippet_body = result_html[snippet_end + 1:]
                    snippet_close = snippet_body.find("</a>")
                    if snippet_close >= 0:
                        snippet = snippet_body[:snippet_close].strip()
                    else:
                        snippet = snippet_body.strip()
                else:
                    snippet = ""
            else:
                snippet = ""

            if title or snippet:
                results.append((title, snippet))

            result_start = html.find('<div class="result"', result_end)

        return results
    except Exception as e:
        print(f"  search error for '{query}': {e}", file=sys.stderr)
        return []


def search_need(need_text, max_results=10):
    """Search for a need statement and return formatted results."""
    # Use the need text as the query; truncate if very long
    query = need_text.strip()
    if len(query) > 200:
        query = query[:200] + "..."

    results = duckduckgo_search(query, max_results=max_results)
    return {
        "query": need_text[:100] if len(need_text) > 100 else need_text,
        "query_normalized": query,
        "num_results": len(results),
        "results": results,
    }


def run_arm(arm_id, corpus_path, output_path, limit=None):
    """Run one arm of the harvest.

    Args:
        arm_id: 1 for treatment, 2 for control
        corpus_path: path to the JSONL corpus
        output_path: path to write results JSONL
        limit: max number of statements to harvest (None = all)
    """
    print(f"=== E065 Arm {arm_id} harvest ===")
    statements = load_corpus(corpus_path, limit=limit)
    print(f"Loaded {len(statements)} need statements from {corpus_path}")

    results = []
    for i, (sid, need_text) in enumerate(statements):
        row = search_need(need_text, max_results=5)
        row["statement_id"] = sid
        results.append(row)

        if (i + 1) % 10 == 0:
            print(f"  harvested {i + 1}/{len(statements)}...")

        # Polite delay
        time.sleep(DELAY_BETWEEN_SEARCHES)

    # Write results
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for row in results:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote {len(results)} results to {output_path}")
    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="E065 harvest arm")
    parser.add_argument("--arm", type=int, choices=[1, 2], default=1,
                        help="Arm to harvest (1=treatment, 2=control)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max number of statements to harvest")
    args = parser.parse_args()

    if args.arm == 1:
        corpus = TREATMENT_CORPUS
        output = TREATMENT_RESULTS
    else:
        corpus = CONTROL_CORPUS
        output = CONTROL_RESULTS

    if not os.path.exists(corpus):
        print(f"ERROR: Corpus not found: {corpus}", file=sys.stderr)
        print("Expected paths:", TREATMENT_CORPUS, CONTROL_CORPUS)
        return 1

    results = run_arm(args.arm, corpus, output, limit=args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())