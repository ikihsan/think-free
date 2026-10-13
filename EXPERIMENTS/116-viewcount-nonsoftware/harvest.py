#!/usr/bin/env python3
"""E116 — harvest one matched pool for the view-count control on non-software
conference proceedings (Crossref API).

The whole point is that the query contains no need vocabulary and no topic
filter, so the need/generic label cannot be a restatement of how the row was
selected. Contrast E107, where 80/80 need rows carry `web-framework` and
80/80 random rows carry `utils` before any classifier runs.

The pool is fetched from the Crossref API. Papers are selected by query, and
the label (need/generic) is assigned randomly after the pool is fixed — the
label cannot restate the selection (matched harvest design).

Stdlib only (plus `requests` or `urllib`). Writes raw_pool.json and
pool_with_arms.json.
"""

from __future__ import print_function

import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "raw_pool.json")
POOL_WITH_ARMS = os.path.join(HERE, "raw", "pool_with_arms.json")

# Crossref API endpoint
CROSSREF_API = "https://api.crossref.org/works"

# Candidate query terms spanning diverse academic domains.
CANDIDATE_TERMS = [
    "quantum", "machine learning", "climate", " genomics", " cosmology",
    "materials", "robotics", "neuroscience", "energy", "health",
    "astrophysics", "biology", "chemistry", "physics", "computer science",
]

# Strata by term (to ensure subject diversity)
STRATA = [("q", 0), ("m", 1), ("c", 2), ("g", 3), ("e", 4)]

PER_STRATUM = 60


def fetch_crossref(term, rows=100):
    """Fetch papers from Crossref API for a given query term."""
    params = {
        "query": term,
        "rows": rows,
        "select": "title,author,abstract,is-referenced-by-count",
    }
    url = CROSSREF_API + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "origin-mission-E116"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("message", {}).get("items", [])
    except Exception as exc:  # noqa: BLE001 - network failure is data here
        print("  error fetching %s: %s" % (term, exc))
        return []


def classify_description(description, rule="masked"):
    """Classify a paper abstract using the masked rule (primary)."""
    from labeling import label
    if not description:
        return "unlabelled"
    result = label(description, rule=rule)
    return result


def strip_html(text):
    """Strip HTML tags and non-alphanumeric characters from a string,
    returning clean lowercase text with only letters and spaces."""
    import re
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&[a-z]+;', '', text)
    text = re.sub(r'\.\. [a-z_]+::', '', text)
    text = re.sub(r'!\[.*?\]\([^)]+\)', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = ' '.join(text.lower().split())
    return text.strip()


def main():
    pool = []
    seen = set()
    fetched = 0
    max_candidates = 600

    for term in CANDIDATE_TERMS:
        if fetched >= max_candidates:
            break
        papers = fetch_crossref(term)
        fetched += 1

        for paper in papers:
            if fetched >= max_candidates:
                break

            # Use first title element as paper identifier
            title_arr = paper.get("title", [""])[0]
            if not title_arr or title_arr.strip() == "":
                continue
            title = strip_html(title_arr)

            if title in seen:
                continue
            seen.add(title)

            # Extract abstract, handling "N/A" string
            abstract_arr = paper.get("abstract", [""])[0]
            if abstract_arr == "N/A" or abstract_arr is None:
                abstract = ""
            else:
                abstract = strip_html(abstract_arr) if isinstance(abstract_arr, str) else ""

            # Combine title + abstract for classification
            combined_text = (title + " " + abstract).lower()

            # Classify using the masked rule
            lab = classify_description(combined_text, rule="masked")

            # Get citation count
            cited_by_raw = paper.get("is-referenced-by-count")
            if isinstance(cited_by_raw, int):
                cited_by = cited_by_raw
            elif isinstance(cited_by_raw, list) and cited_by_raw:
                cited_by = cited_by_raw[0]
            else:
                cited_by = 0

            # Determine active status: paper has citation data
            active = 1 if cited_by is not None and cited_by >= 0 else 0

            row = {
                "title": title[:100],
                "abstract": abstract[:500],
                "cited_by": cited_by,
                "api_success": True,
                "classification": lab,
                "active": active,
                "stratum": term[0],
                "term": term,
            }
            pool.append(row)
            print("  fetched %s: cited_by=%d, class=%s" % (term, cited_by, lab))

        time.sleep(0.5)

    # Stratify and assign arms
    for row in pool:
        row["arm"] = "need" if random.random() < 0.5 else "generic"

    print("\n--- Stratum breakdown ---")
    for term_letter in ["q", "m", "c", "g", "e"]:
        strata_rows = [r for r in pool if r["stratum"] == term_letter]
        if strata_rows:
            need_count = sum(1 for r in strata_rows if r["arm"] == "need")
            generic_count = sum(1 for r in strata_rows if r["arm"] == "generic")
            active_need = sum(1 for r in strata_rows if r["arm"] == "need" and r["active"])
            active_gen = sum(1 for r in strata_rows if r["arm"] == "generic" and r["active"])
            print("  Term %s: %d packages (need=%d, generic=%d, active_need=%d, active_gen=%d)"
                  % (term_letter, len(strata_rows), need_count, generic_count, active_need, active_gen))

    with open(RAW, "w") as fh:
        json.dump(pool, fh, indent=1, sort_keys=True)
    print("\nraw pool written to %s (%d rows)" % (RAW, len(pool)))

    with open(POOL_WITH_ARMS, "w") as fh:
        json.dump(pool, fh, indent=1, sort_keys=True)
    print("pool with arms written to %s" % POOL_WITH_ARMS)

    need_pkgs = [r for r in pool if r["arm"] == "need"]
    generic_pkgs = [r for r in pool if r["arm"] == "generic"]
    active_need = sum(1 for r in need_pkgs if r["active"])
    active_gen = sum(1 for r in generic_pkgs if r["active"])
    unlabelled = sum(1 for r in pool if r["classification"] == "unlabelled")

    print("\n--- Summary ---")
    print("Total packages: %d" % len(pool))
    print("Need arm: %d packages" % len(need_pkgs))
    print("Generic arm: %d packages" % len(generic_pkgs))
    print("Unlabelled: %d packages" % unlabelled)
    print("Need active rate: %d/%d = %.3f" % (active_need, len(need_pkgs), active_need / len(need_pkgs) if need_pkgs else 0))
    print("Generic active rate: %d/%d = %.3f" % (active_gen, len(generic_pkgs), active_gen / len(generic_pkgs) if generic_pkgs else 0))


if __name__ == "__main__":
    main()
