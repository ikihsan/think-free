#!/usr/bin/env python3
"""E041 mechanism probe: can one repository's whole issue space be captured
through the search API alone?

This is D067's check, run before the protocol is written. It decides the
design, and it costs two search requests:

  * does `repo:<o>/<r> is:issue` enumerate the repository's issues with full
    bodies, so that a duplicate issue AND the target it names are both inside
    one capture, and
  * what share of duplicate-labelled issues actually name a parseable target,
    which sets the positive population's ceiling before any similarity is
    computed.

The second number is a *mechanism yield*, not a result: it says what the source
can serve, which is the thing F059 spent 1125 rows learning the expensive way.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = {"User-Agent": "think-free-research", "Accept": "application/vnd.github+json"}

# Target-reference shapes seen in duplicate-issue bodies. Fixed list, applied
# identically to every row; recorded here rather than tuned later.
REF_PATTERNS = [
    re.compile(r"duplicate\s+of\s+#(\d+)", re.I),
    re.compile(r"dup(?:e|licate)?\s*(?:of|:)\s*#(\d+)", re.I),
    re.compile(r"same\s+(?:as|issue\s+as)\s+#(\d+)", re.I),
    re.compile(r"->\s*#(\d+)"),
    re.compile(r"see\s*#(\d+)"),
    re.compile(r"https?://github\.com/[^/\s]+/[^/\s]+/issues/(\d+)"),
]
BOILERPLATE = [
    re.compile(r"<!--.*?-->", re.S),
    re.compile(r"duplicate\s+of\s*#\d+", re.I),
    re.compile(r"dup(?:e|licate)?\s*(?:of|:)\s*#\d+", re.I),
    re.compile(r"same\s+(?:as|issue\s+as)\s*#\d+", re.I),
    re.compile(r"https?://\S+", re.I),
]


def search_url(q, page, per_page=100):
    """Build a search URL with spaces encoded as `+` (GitHub's own convention).

    `quote(q, safe="")` percent-encodes a literal `+`, which GitHub then reads as
    a plus and not as a space, so the query silently matches nothing.
    """
    return ("https://api.github.com/search/issues?q=%s&per_page=%d&page=%d"
            % (urllib.parse.quote_plus(q), per_page, page))


def get(url, tries=3):
    last = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                        timeout=60) as r:
                return json.load(r), dict(r.headers), None
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            last = repr(exc)[:200]
            time.sleep(6.0 * (attempt + 1))
    return None, {}, last


def target_ref(body):
    """First parseable target number in a body, or None."""
    for pat in REF_PATTERNS:
        m = pat.search(body or "")
        if m:
            return int(m.group(1))
    return None


def main():
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    report = {}

    # --- 1. whole-repo enumeration, with bodies ---
    for repo in ("tiangolo/typer", "pallets/click"):
        rows, pages, total = [], 0, None
        for page in range(1, 4):
            q = "repo:%s is:issue" % repo
            url = search_url(q, page)
            d, headers, err = get(url)
            if d is None:
                report.setdefault("errors", []).append(
                    {"repo": repo, "page": page, "error": err})
                break
            items = d.get("items") or []
            total = d.get("total_count")
            for it in items:
                rows.append({
                    "repo": repo, "number": it.get("number"),
                    "title": it.get("title") or "",
                    "body": it.get("body") or "",
                    "state_reason": it.get("state_reason"),
                    "user": (it.get("user") or {}).get("login"),
                })
            pages += 1
            with open(os.path.join(RAW, "mech_repo_%s.json" % repo.replace("/", "_")),
                      "w") as fh:
                json.dump({"total_count": total, "rows": rows}, fh)
            print("%-18s page=%d total=%s rows=%d bodies=%d" % (
                repo, page, total, len(rows),
                sum(1 for r in rows if r["body"])))
            if not items:
                break
            time.sleep(7.0)
        dups = [r for r in rows if r["state_reason"] == "duplicate"]
        withref = [r for r in dups if target_ref(r["body"]) is not None]
        inpage = [r for r in withref
                  if any(o["number"] == target_ref(o["body"]) for o in rows)]
        report[repo] = {
            "pages": pages, "rows": len(rows),
            "with_body": sum(1 for r in rows if r["body"]),
            "duplicate_labelled": len(dups),
            "duplicate_with_parseable_ref": len(withref),
            "duplicate_with_ref_inside_capture": len(inpage),
            "search_total_count": total,
        }
        print("  -> %s" % json.dumps(report[repo], sort_keys=True))

    # --- 2. yield of the parseable-reference rule over a cross-repo duplicate sample ---
    q = 'is:issue reason:duplicate "duplicate of #"'
    url = search_url(q, 1)
    d, headers, err = get(url)
    if d is None:
        report["cross_repo_error"] = err
        print("cross-repo fetch failed: %s" % err)
    else:
        items = d.get("items") or []
        with open(os.path.join(RAW, "mech_cross_repo_dups.json"), "w") as fh:
            json.dump({"total_count": d.get("total_count"), "items": items}, fh)
        repos = {}
        refs = 0
        for it in items:
            repos[it["repository_url"].split("/repos/")[-1]] = \
                repos.get(it["repository_url"].split("/repos/")[-1], 0) + 1
            if target_ref(it.get("body") or ""):
                refs += 1
        top = sorted(repos.items(), key=lambda kv: -kv[1])[:10]
        report["cross_repo"] = {
            "search_total_count": d.get("total_count"), "rows": len(items),
            "with_parseable_ref": refs,
            "distinct_repos": len(repos),
            "top_repos": top,
        }
        print("cross-repo: %s" % json.dumps(report["cross_repo"], sort_keys=True))

    with open(os.path.join(RAW, "mechanism_probe.json"), "w") as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
