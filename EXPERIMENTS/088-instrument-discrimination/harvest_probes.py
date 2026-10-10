#!/usr/bin/env python3
"""E088 probe harvest: run the E087 instrument unchanged on known-label probes.

Imports `bing_search` from E087's harvest.py and nothing else from it, so the
retrieval path under test is byte-for-byte the one that produced E081-E087.
Writes raw/probe-results.jsonl.

Usage:
    python3 harvest_probes.py
    python3 harvest_probes.py --limit 5     # smoke test only; not a result
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
E087 = os.path.join(REPO, "EXPERIMENTS", "087-environmental-monitoring")

sys.path.insert(0, E087)
from harvest import bing_search, DELAY_BETWEEN_SEARCHES  # noqa: E402

PROBES = os.path.join(HERE, "probes.jsonl")
OUT = os.path.join(HERE, "raw", "probe-results.jsonl")


def load_probes():
    probes = []
    with open(PROBES, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                probes.append(json.loads(line))
    return probes


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    probes = load_probes()
    if limit is not None:
        probes = probes[:limit]
    print(f"E088 probe harvest: {len(probes)} probes")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as out:
        for i, p in enumerate(probes):
            results = bing_search(p["query"], max_results=5)
            row = {
                "id": p["id"],
                "arm": p["arm"],
                "true_label": p["true_label"],
                "query": p["query"],
                "num_results": len(results),
                "titles": [t for t, s in results],
                "snippets": [s for t, s in results],
            }
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            if (i + 1) % 10 == 0:
                print(f"  {i + 1}/{len(probes)}")
            time.sleep(DELAY_BETWEEN_SEARCHES)

    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())