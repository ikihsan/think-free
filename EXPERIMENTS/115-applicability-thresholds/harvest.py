#!/usr/bin/env python3
"""Harvest numeric applicability thresholds from one CFR title.

Declared against EXPERIMENTS/115-applicability-thresholds/PROTOCOL.md.

Standard library only. The eCFR "versioner" API serves full section XML for
a given title/date; this walks the structure tree the same service returns and
fetches candidate sections in parallel.

Two measurements come out and neither is a pass/fail:
  * extraction_coverage -- of the sections whose text was fetched, the
    fraction the extractor labelled `need` or `matched` at all.  Anything
    else is `unlabelled` and must be counted, not dropped.
  * counting_rule_divergent -- of the labelled rows, the fraction whose
    counting rule is NOT plain headcount at a moment.

The classifier anchors every match to a word boundary.  F116's measured
defect was unanchored substring matching (`ai` inside `email`), which is
exactly how a threshold extractor produces confident wrong numbers.
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


def flatten(node, out):
    """Yield every leaf section reference in a structure tree."""
    if node.get("type") == "section":
        out.append(node)
        return
    for child in node.get("children") or []:
        flatten(child, out)


# ---------------------------------------------------------------------------
# The extraction rule.  One regex for the shape, one for the counting rule.
# ---------------------------------------------------------------------------

# A threshold is a number immediately governing an applicability verb, inside
# a section whose own heading is a scope paragraph ("Scope and purpose",
# "Applicability", ...).  Requires a word boundary on the number so that
# "1953" does not match "53" and "220" does not match "1200".
THRESHOLD = re.compile(
    r"\b(?:"
    r"(?:fewer|less|more|greater|at\s+least|at\s+most|under|over|exceed(?:s|ing)?)"
    r"\s+than\s+|"
    r"(?:ten|fifteen|twenty|thirty|fifty|one\s+hundred|twenty-five)"
    r"\s+(?:or\s+more|or\s+fewer|or\s+more\s+employees|full-time\s+employees)"
    r"\b|"
    r"\d{1,4}\s+(?:or\s+more|or\s+fewer|or\s+more\s+employees|or\s+more\s+persons)"
    r")\s*"
    r"(?:\(\d+\)\s*)?"
    r"\b(?:employees|persons|workers|participants|members|individuals|"
    r"full-time\s+employees|part-time\s+employees|teachers|children|"
    r"students|residents|beds|families)\b",
    re.IGNORECASE,
)

# Numerator qualifiers: the counting rule is not plain headcount when the rule
# text names a type of person, a role, or a conversion.
NUMERATOR = re.compile(
    r"\b(full-time\s+equivalent|fte\b|full-time\s+part-time\s+employees|"
    r"excluding\s+(?:any\s+)?(?:owner|partners?|self\s+employed)|"
    r"including\s+(?:any\s+)?(?:partners?|owners?|family\s+members)|"
    r"partners?\s+or\s+sole\s+proprietors|"
    r"residents\s+or\s+patients|"
    r"employees\s+on\s+the\s+payroll)\b",
    re.IGNORECASE,
)

# Window qualifiers: a rate over a period is not a rate at a moment.
WINDOW = re.compile(
    r"\b(any\s+time\s+(?:during|in|not\s+more\s+than)|"
    r"(?:preceding|previous|last|past)\s+\d+|"
    r"\d+\s+workweeks?|"
    r"calendar\s+year|fiscal\s+year|"
    r"12\s+months?|three\s+months?|30\s+days?)\b",
    re.IGNORECASE,
)

SCOPE_HEADING = re.compile(
    r"\b(scope|applicability|application|purpose|definitions?)\b", re.IGNORECASE
)

TAG = re.compile(r"<[^>]+>")
ENT = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&apos;": "'"}
# The eCFR emits numeric character references (`&#xA7;` for the section sign)
# alongside the named ones; leaving them in makes a heading unreadable and a
# heading is half of what decides whether a row is a scope section.
NUMENT = re.compile(r"&#(?:x([0-9A-Fa-f]+)|([0-9]+));")


def _unnumerify(match):
    hexpart, decpart = match.group(1), match.group(2)
    try:
        code = int(hexpart, 16) if hexpart else int(decpart)
        return chr(code)
    except (ValueError, OverflowError):
        return match.group(0)


def totext(xml_bytes):
    s = TAG.sub(" ", xml_bytes.decode("utf-8", "replace"))
    for k, v in ENT.items():
        s = s.replace(k, v)
    s = NUMENT.sub(_unnumerify, s)
    return re.sub(r"\s+", " ", s)


def label(section_text):
    """Return (label, dict).  Never raises, never silently drops.

    `section_text` is the XML of one section, as bytes.
    """
    flat = totext(section_text)
    found = []
    for m in THRESHOLD.finditer(flat):
        start = max(0, m.start() - 220)
        window = flat[start:m.end() + 220]
        num = NUMERATOR.search(window)
        win = WINDOW.search(window)
        found.append(
            {
                "span": m.group(0)[:160],
                "context": window[:440],
                "numerator": num.group(0) if num else None,
                "window": win.group(0) if win else None,
                "divergent": bool(num or win),
            }
        )
    if not found:
        return "unlabelled", {"threshold_spans": []}
    divergent = sum(1 for r in found if r["divergent"])
    lab = "matched" if divergent else "need"
    return lab, {
        "threshold_spans": found,
        "n_threshold_spans": len(found),
        "n_divergent_spans": divergent,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", type=int, required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default="sections.jsonl")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))

    tree = json.loads(fetch("%s/structure/%s/title-%d.json" % (API, args.date, args.title)))
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

    # Coverage is measured over every SECTION in the parts that were read,
    # never over the sections the extractor happened to label.  Note what it
    # does NOT mean: most CFR sections contain no applicability threshold at
    # all, so a low figure here is the expected shape, not a defect.  The
    # instrument's own recall is measured separately by M1b (hand-read
    # negatives), because "fraction of rows labelled" is the statistic F116
    # showed cannot stand in for it.
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
    summary = {
        "title": args.title,
        "date": args.date,
        "parts_total": len(parts),
        "parts_unreadable": len(unreadable),
        "unreadable_parts": unreadable[:20],
        "sections_read": len(all_sections),
        "sections_scope_heading": sum(1 for s in all_sections if s["heading_is_scope"]),
        "extraction_coverage": round(
            len(labelled) / max(1, len(all_sections)), 6
        ),
        "extraction_coverage_scope_only": round(
            len(labelled) / max(1, sum(1 for s in all_sections if s["heading_is_scope"])),
            6,
        ),
        "rows_with_thresholds": len(rows),
        "threshold_spans": len(spans),
        "counting_rule_divergent_spans": len(div),
        "counting_rule_divergent": round(len(div) / max(1, len(spans)), 6),
        "sections_with_divergence": sum(1 for s in rows if s.get("n_divergent_spans")),
    }
    with open(os.path.join(here, "m1-summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


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


SECTION_SPLIT = re.compile(r'<DIV8\b[^>]*TYPE="SECTION"[^>]*>')
HEAD_TAG = re.compile(r"<HEAD>(.*?)</HEAD>", re.DOTALL | re.IGNORECASE)
CITATION_TAG = re.compile(r'citation&quot;:&quot;([^&]*)&quot;')


def label_part(body):
    """Split one part's XML into its sections and label each one.

    The eCFR part XML nests subparts as DIV6 and sections as DIV8 with
    TYPE="SECTION".  Splitting on DIV8 alone keeps a section's own body with
    its own heading; splitting on HEAD (the first attempt) shredded the part
    header and subpart headers into rows that are not sections at all.
    """
    text = body.decode("utf-8", "replace")
    pieces = SECTION_SPLIT.split(text)
    # pieces[0] is the part header and whatever precedes the first section;
    # it is not a section and is reported separately by the caller.
    out = []
    for chunk in pieces[1:]:
        m = HEAD_TAG.search(chunk)
        heading = totext(m.group(1).encode()) if m else ""
        cite = CITATION_TAG.search(chunk[: chunk.find(">") + 1])
        # A section's body is everything after its own HEAD.
        body_text = (chunk[m.end():] if m else chunk).encode("utf-8", "replace")
        lab, detail = label(body_text)
        rec = {
            "heading": heading[:220],
            "citation": cite.group(1) if cite else None,
            "heading_is_scope": bool(SCOPE_HEADING.search(heading)),
            "label_outcome": lab,
        }
        rec.update(detail)
        out.append(rec)
    return out

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, args.out), "w") as fh:
        for rec in out:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")

    labelled = [r for r in out if r["label_outcome"] in ("need", "matched")]
    unread = [r for r in out if r["label_outcome"] == "unreadable"]
    rows = [r for r in labelled if r.get("n_threshold_spans")]
    spans = [s for r in rows for s in r["threshold_spans"]]
    div = [s for s in spans if s["divergent"]]
    summary = {
        "title": args.title,
        "date": args.date,
        "leaf_sections": len(leaves),
        "heading_matched_candidates": len(cands),
        "sections_fetched": len(out) - len(unread),
        "sections_unreadable": len(unread),
        "extraction_coverage": round(len(labelled) / max(1, len(out) - len(unread)), 6),
        "rows_with_thresholds": len(rows),
        "threshold_spans": len(spans),
        "counting_rule_divergent_spans": len(div),
        "counting_rule_divergent": round(len(div) / max(1, len(spans)), 6),
        "sections_with_divergence": sum(
            1 for r in rows if r.get("n_divergent_spans")
        ),
    }
    with open(os.path.join(here, "m1-summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()