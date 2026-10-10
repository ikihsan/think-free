#!/usr/bin/env python3
"""E086 harvest: web search for view-count arrival metrics.

For each fault code/query in the treatment and control corpora, perform a
Bing search and record the number of search results. This experiment measures
the view-count principle's arrival count distribution without attempting to
classify each statement as served/partial/unserved.

Usage:
    python3 harvest.py            # harvest both arms
    python3 harvest.py --arm 1    # harvest treatment arm only
    python3 harvest.py --arm 2    # harvest control arm only
"""

import json
import os
import sys
import time
from urllib.parse import quote_plus

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Bing search URL (no API key needed for basic queries)
BING_SEARCH_URL = "https://www.bing.com/search"

# Polite delay between searches (seconds)
DELAY_BETWEEN_SEARCHES = 1.0


def bing_search(query, max_results=5):
    """Perform a Bing search and return result titles/snippets."""
    try:
        params = {"q": query}
        resp = requests.get(BING_SEARCH_URL, params=params, timeout=15,
                            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
        if resp.status_code != 200:
            return []
        html = resp.text

        # Extract result blocks from Bing HTML
        results = []
        result_start = html.find('<li class="b_algo"')
        visited = set()
        while result_start >= 0 and len(results) < max_results:
            if result_start in visited:
                break
            visited.add(result_start)

            # Find the closing </li> for this block
            close_idx = html.find('</li>', result_start + 1)
            if close_idx < 0:
                break
            result_html = html[result_start:close_idx + 5]

            # Extract title from h2 element
            title = ""
            h2_idx = result_html.find('<h2')
            if h2_idx >= 0:
                h2_end = result_html.find("</h2>", h2_idx)
                if h2_end >= 0:
                    a_idx = result_html.find('<a ', h2_idx)
                    if a_idx >= 0 and a_idx < h2_end:
                        gt_idx = result_html.find('>', a_idx)
                        if gt_idx >= 0 and gt_idx < h2_end:
                            lt_idx = result_html.find('<', gt_idx + 1)
                            if lt_idx >= 0 and lt_idx <= h2_end:
                                title = result_html[gt_idx + 1:lt_idx].strip()
                    if not title:
                        h2_text_start = result_html.find('>', h2_idx)
                        if h2_text_start >= 0:
                            h2_text_end = result_html.find('<', h2_text_start + 1)
                            if h2_text_end >= 0:
                                title = result_html[h2_text_start + 1:h2_text_end].strip()

            # Extract snippet from p.b_lineclamp2 element
            snippet = ""
            snippet_start = result_html.find('class="b_lineclamp2"')
            if snippet_start >= 0:
                text_start = result_html.find('>', snippet_start)
                if text_start >= 0:
                    text_end = result_html.find('<', text_start + 1)
                    if text_end >= 0:
                        snippet = result_html[text_start + 1:text_end].strip()

            if not snippet:
                p_idx = result_html.find('<p ')
                if p_idx >= 0:
                    p_close = result_html.find('</p>', p_idx)
                    if p_close >= 0:
                        gt = result_html.find('>', p_idx)
                        if gt >= 0 and gt < p_close:
                            lt = result_html.find('<', gt + 1)
                            if lt >= 0 and lt <= p_close:
                                snippet = result_html[gt + 1:lt].strip()

            if title or snippet:
                results.append((title, snippet))

            # Move to next b_algo block
            result_start = html.find('<li class="b_algo"', close_idx + 1)

        return results
    except Exception as e:
        print(f"  search error for '{query}': {e}", file=sys.stderr)
        return []


def load_corpus(path, limit=None):
    """Load fault code statements from a JSONL corpus."""
    statements = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break
            try:
                obj = json.loads(line.strip())
                query_text = obj.get("query_text", "")
                if query_text:
                    statements.append((i, query_text))
            except (json.JSONDecodeError, KeyError):
                continue
    return statements


def run_arm(arm_id, corpus_path, output_path, limit=None):
    """Run one arm of the harvest."""
    print(f"=== E086 Arm {arm_id} harvest ===")
    statements = load_corpus(corpus_path, limit=limit)
    print(f"Loaded {len(statements)} fault code statements from {corpus_path}")

    results = []
    for i, (sid, query_text) in enumerate(statements):
        search_results = bing_search(query_text, max_results=5)
        row = {
            "query": query_text[:100] if len(query_text) > 100 else query_text,
            "query_normalized": query_text.strip(),
            "num_results": len(search_results),
            "titles": [t for t, s in search_results],
            "snippets": [s for t, s in search_results],
            "statement_id": sid,
        }
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
    parser = argparse.ArgumentParser(description="E086 harvest arm")
    parser.add_argument("--arm", type=int, choices=[1, 2], default=1,
                        help="Arm to harvest (1=treatment, 2=control)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max number of statements to harvest")
    args = parser.parse_args()

    if args.arm == 1:
        corpus = os.path.join(HERE, "raw", "treatment-needs.jsonl")
        output = os.path.join(HERE, "raw", "treatment-results.jsonl")
    else:
        corpus = os.path.join(HERE, "raw", "control-needs.jsonl")
        output = os.path.join(HERE, "raw", "control-results.jsonl")

    if not os.path.exists(corpus):
        print(f"ERROR: Corpus not found: {corpus}", file=sys.stderr)
        print("Expected paths:", os.path.join(HERE, "raw", "treatment-needs.jsonl"),
              os.path.join(HERE, "raw", "control-needs.jsonl"))
        return 1

    results = run_arm(args.arm, corpus, output, limit=args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())