#!/usr/bin/env python3
"""Falsification of the screening itself: verify the `prior_art` verdicts.

`screen_sample.py` kills 19 of 50 items with the verdict "a tool already serves
this", and that verdict is a judgement. If it is wrong, the headline number --
zero survivors -- is wrong, so the verdicts that carry weight are re-checked
against a countable source rather than left as opinion. This is the
gate-falsification discipline from `docs/policy/gate-falsification.md` applied to
a judgement rather than to a gate: the property that decides the verdict is
"does a maintained public tool exist", and the cheapest honest reader of that
property is a population count.

Two directions, both recorded:
  * `kill`   -- a populated count supports the verdict, the verdict stands;
  * `revise` -- a thin or empty count means the verdict was asserted from
    memory, exactly the error F025 records its author making twice.

Limits, stated before the counts are read: a count of zero does not mean a tool
does not exist, because a product published only to PyPI or npm, a commercial
service, or a tool nobody indexes would all read as zero. So `revise` means
"this verdict is unverified", never "this need is novel". Run from this
directory:

    python3 verify_prior_art.py
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import os


HERE = os.path.dirname(os.path.abspath(__file__))


def path(*parts):
    """Resolve a data path next to this script.

    The evidence is only reproducible if it can be re-run from anywhere, so the
    raw files are addressed relative to the script rather than to the caller's
    working directory.
    """
    return os.path.join(HERE, *parts)


UA = {"User-Agent": "think-free-research", "Accept": "application/vnd.github+json"}
# (screening index, name, the verdict to check, query)
CHECKS = [
    (36, "s3-alternative", "Garage, MinIO, SeaweedFS and others",
     "s3 object storage server in:name,description"),
    (8, "flashcards", "Anki plus an LLM is widely available",
     "flashcard spaced repetition in:name,description"),
    (3, "webp-encode", "libwebp and libvips are fast",
     "image encoder webp in:name,description"),
    (42, "selective-stage", "git add -p and jj's split already do this",
     "version control partial stage in:name,description"),
    (7, "runtime-instrumentation", "eBPF plus OpenTelemetry sample at runtime",
     "ebpf tracing runtime in:name,description"),
    (30, "bulk-seed-books", "calibre, OPDS and Kavita serve this",
     "ebook library server calibre in:name,description"),
    (45, "model-changelog", "OpenRouter changelogs and newsletters",
     "llm model changelog tracker in:name,description"),
    (49, "gdrive-disk-usage", "ggdu exists; TreeSize is commercial",
     "gdrive disk usage in:name,description"),
    (1, "atomic-distro", "Silverblue, Bazzite, Talos and similar exist",
     "immutable atomic linux system in:name,description"),
    (38, "cheap-monitoring", "uptime-kuma is 92k stars",
     "uptime monitor in:name,description"),
]


def search(q):
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": q, "per_page": 5, "sort": "stars", "order": "desc"})
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    out = []
    killed = revised = 0
    for idx, name, claim, q in CHECKS:
        try:
            d = search(q)
        except urllib.error.HTTPError as e:
            print("HTTP %s on %s" % (e.code, name), file=sys.stderr)
            time.sleep(65)
            continue
        items = d.get("items", [])
        top = [{"repo": it["full_name"], "stars": it["stargazers_count"],
                "pushed": it["pushed_at"][:10],
                "desc": (it["description"] or "")[:80]} for it in items[:3]]
        total = d.get("total_count")
        # a verdict is "supported" when a maintained, actually-used tool shows up
        supported = any(t["stars"] >= 100 for t in top)
        verdict = "kill" if supported else "revise"
        if supported:
            killed += 1
        else:
            revised += 1
        out.append({"index": idx, "name": name, "claim": claim, "query": q,
                    "total_count": total, "top": top, "verdict": verdict})
        print("%-20s %-6s %-9s %s" % (
            name, total, verdict,
            ", ".join("%s(%s*)" % (t["repo"], t["stars"]) for t in top[:2])))
        time.sleep(7)
    with open(path("raw", "verify_prior_art.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("\nverdicts supported by a populated count: %d" % killed)
    print("verdicts asserted from memory, now unverified: %d" % revised)
    return 0


if __name__ == "__main__":
    sys.exit(main())