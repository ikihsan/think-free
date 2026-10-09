#!/usr/bin/env python3
"""E065 harvest: web search for need statements.

For each need statement in the treatment and control corpora, perform a
web search and record the number of search results along with titles and
snippets. The harvest produces raw data that outcome.py uses for gate
evaluation.

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

# Corpora paths
TREATMENT_CORPUS = os.path.join(HERE, "raw", "treatment-needs.jsonl")
CONTROL_CORPUS = os.path.join(HERE, "raw", "control-needs.jsonl")

# Output paths
TREATMENT_RESULTS = os.path.join(HERE, "raw", "treatment-results.jsonl")
CONTROL_RESULTS = os.path.join(HERE, "raw", "control-results.jsonl")

# Bing search URL (no API key needed for basic queries)
BING_SEARCH_URL = "https://www.bing.com/search"

# polite delay between searches (seconds)
DELAY_BETWEEN_SEARCHES = 2.0


def bing_search(query, max_results=10):
    """Perform a Bing search and return result titles/snippets.

    Returns a list of (title, snippet) tuples for the top results.
    """
    try:
        params = {"q": query}
        resp = requests.get(BING_SEARCH_URL, params=params, timeout=15,
                            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
        if resp.status_code != 200:
            return []
        html = resp.text

        # Extract result blocks from Bing HTML
        results = []
        # Bing results are in li elements with class b_algo
        result_start = html.find('<li class="b_algo"')
        visited = set()
        while result_start >= 0 and len(results) < max_results:
            # Use a visited set to avoid infinite loops on malformed HTML
            if result_start in visited:
                break
            visited.add(result_start)

            # Find the closing </li> for this block
            # Search from result_start+1 to avoid finding the same one
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
                    # The h2 contains an <a> tag with the actual title text
                    a_idx = result_html.find('<a ', h2_idx)
                    if a_idx >= 0 and a_idx < h2_end:
                        # Extract text between > and </a>
                        gt_idx = result_html.find('>', a_idx)
                        if gt_idx >= 0 and gt_idx < h2_end:
                            lt_idx = result_html.find('<', gt_idx + 1)
                            if lt_idx >= 0 and lt_idx <= h2_end:
                                title = result_html[gt_idx + 1:lt_idx].strip()
                    if not title:
                        # Fallback: extract text between <h2> and </h2>
                        h2_text_start = result_html.find('>', h2_idx)
                        if h2_text_start >= 0:
                            h2_text_end = result_html.find('<', h2_text_start + 1)
                            if h2_text_end >= 0:
                                title = result_html[h2_text_start + 1:h2_text_end].strip()

            # Extract snippet from p.b_lineclamp2 element
            snippet = ""
            snippet_start = result_html.find('class="b_lineclamp2"')
            if snippet_start >= 0:
                # Find the > that opens the text and the < that closes it
                text_start = result_html.find('>', snippet_start)
                if text_start >= 0:
                    text_end = result_html.find('<', text_start + 1)
                    if text_end >= 0:
                        snippet = result_html[text_start + 1:text_end].strip()

            # Alternative snippet: any <p> element within the result
            if not snippet:
                p_idx = result_html.find('<p ')
                if p_idx >= 0:
                    # Find the closing </p> within the b_algo block
                    p_close = result_html.find('</p>', p_idx)
                    if p_close >= 0:
                        # Find > after <p
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
        search_results = bing_search(need_text, max_results=5)
        row = {
            "query": need_text[:100] if len(need_text) > 100 else need_text,
            "query_normalized": need_text.strip(),
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