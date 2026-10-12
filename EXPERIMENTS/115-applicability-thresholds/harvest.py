#!/usr/bin/env python3
"""Harvest numeric applicability thresholds from one CFR title.

Declared against EXPERIMENTS/115-applicability-thresholds/PROTOCOL.md.

Standard library only.  The eCFR "versioner" API serves one part per request,
so this walks the structure tree, fetches each part's XML, and hands every
section to `classify.label_part`.  The classification rules themselves live
in `classify.py`; this file is the fetching and the reporting.

Three things it reports, and none of them is a pass/fail:

* `threshold_spans` -- the population.
* `counting_rule_divergent` -- the fraction whose counting rule is NOT plain
  headcount at a moment.  **This is a candidate figure, not a result**: M1b
  hand-read the 15 spans it flagged and found 11 real and 4 artifacts, and
  the artifact shapes are pinned in `test_classify.py`.
* `extraction_coverage` -- the fraction of sections labelled at all.  **It is
  expected to be near zero and cannot fail**, because most CFR sections
  contain no applicability threshold.  The protocol's K2 gate named this
  statistic as a kill and it is the wrong statistic; see M1.md.  The
  instrument's recall is measured by hand-reading, not by this number.
"""

import argparse
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify import SCOPE_HEADING, label_part  # noqa: E402

API = "https://www.ecfr.gov/api/versioner/v1"
UA = "think-free-e115/1.0 (research; unauthenticated)"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")


def fetch(url, retries=4):
    key = re.sub(r"[^A-Za-z0-9]+", "_", url)[-180:]
    path = os.path.join(CACHE, key)
    if os.path.exists(path):
        with open(path, "rb") as fh:
            return fh.read()
    last = None
    for attempt in range(retries):
        try:
            # The versioner endpoint refuses (HTTP 406) unless the client
            # advertises that it can decode a compressed response; urllib
            # sends neither Accept nor Accept-Encoding by default.
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": UA,
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate",
                },
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read()
                if resp.headers.get("Content-Encoding") == "gzip":
                    body = gzip.decompress(body)
            os.makedirs(CACHE, exist_ok=True)
            tmp = path + ".part"
            with open(tmp, "wb") as fh:
                fh.write(body)
            os.replace(tmp, path)
            return body
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("fetch failed %s: %s" % (url, last))


def collect_parts(node, out):
    if node.get("type") == "part":
        out.append(node)
        return
    for child in node.get("children") or []:
        collect_parts(child, out)


def count_leaves(node):
    if node.get("type") == "section":
        return 1
    return sum(count_leaves(c) for c in node.get("children") or [])


def summarise(args, parts, out):
    """Build the M1 summary.  Denominators are stated, never assumed."""
    all_sections = []
    unreadable = []
    for rec in out:
        if rec["label_outcome"] == "read":
            all_sections.extend(rec["sections"])
        else:
            unreadable.append(rec["part"])
    labelled = [s for s in all_sections if s["label_outcome"] in ("need", "matched")]
    rows = [s for s in labelled if s.get("n_threshold_spans")]
    spans = [sp for s in rows for sp in s["threshold_spans"]]
    div = [sp for sp in spans if sp["divergent"]]
    scope_n = sum(1 for s in all_sections if s["heading_is_scope"])
    return {
        "title": args.title,
        "date": args.date,
        "parts_total": len(parts),
        "parts_unreadable": len(unreadable),
        "unreadable_parts": unreadable[:20],
        "sections_read": len(all_sections),
        "sections_scope_heading": scope_n,
        "extraction_coverage": round(len(labelled) / max(1, len(all_sections)), 6),
        "extraction_coverage_scope_only": round(
            len(labelled) / max(1, scope_n), 6
        ),
        "rows_with_thresholds": len(rows),
        "threshold_spans": len(spans),
        "counting_rule_divergent_spans": len(div),
        "counting_rule_divergent": round(len(div) / max(1, len(spans)), 6),
        "sections_with_divergence": sum(1 for s in rows if s.get("n_divergent_spans")),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", type=int, required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default="parts-title.jsonl")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))

    tree = json.loads(
        fetch("%s/structure/%s/title-%d.json" % (API, args.date, args.title))
    )
    parts = []
    for node in tree.get("children") or []:
        collect_parts(node, parts)
    print(
        "structure: %d leaf sections, %d parts, %d bytes of part XML"
        % (count_leaves(tree), len(parts), sum(p.get("size") or 0 for p in parts)),
        file=sys.stderr,
    )
    if args.limit:
        parts = parts[: args.limit]

    def one(part):
        ident = part["identifier"]
        url = "%s/full/%s/title-%d.xml?part=%s" % (API, args.date, args.title, ident)
        rec = {"part": ident, "label": part.get("label")}
        try:
            body = fetch(url)
        except Exception as exc:  # noqa: BLE001 - recorded, never dropped
            rec.update({"label_outcome": "unreadable", "error": str(exc)[:200]})
            return rec
        rec.update({"label_outcome": "read", "bytes": len(body)})
        rec["sections"] = label_part(body)
        return rec

    out = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i, rec in enumerate(pool.map(one, parts), 1):
            out.append(rec)
            if i % 10 == 0:
                print("fetched %d/%d parts" % (i, len(parts)), file=sys.stderr)

    with open(os.path.join(here, args.out), "w") as fh:
        for rec in out:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")

    summary = summarise(args, parts, out)
    with open(os.path.join(here, "m1-summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()