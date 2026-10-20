"""E169 step 2 (G0): does the record's own summary figure reproduce?

E168's addendum states "20 of 24 answer sets link out to an external source,
and the destination is overwhelmingly an issue tracker -- github.com in 15 of
24".  This recomputes both from the committed bytes under every URL-reading
rule a reader could plausibly have used, and reports which rules reproduce
which figure.  A figure no rule reproduces is recorded as not reproducible.
"""
import collections
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "168-version-pinned-need",
                   "threads.json")
RULES = {
    "href": re.compile(r'href="(https?://[^"]+)"'),
    "any_text": re.compile(r'https?://[^\s"\'<>)\]]+'),
    "href_plus_src": re.compile(r'(?:href|src)="(https?://[^"]+)"'),
}


def host(u):
    m = re.match(r"https?://(?:www\.)?([^/]+)", u)
    return m.group(1).lower() if m else ""


def main():
    raw = open(SRC, "rb").read()
    threads = json.loads(raw.decode("utf-8"))
    out = {"source": os.path.relpath(SRC, os.path.dirname(HERE)),
           "source_sha256": hashlib.sha256(raw).hexdigest(),
           "threads": len(threads), "rules": {}}
    for name, rx in RULES.items():
        per_thread = collections.defaultdict(set)
        for qid, t in threads.items():
            for a in (t.get("answers") or []):
                for u in rx.findall(a.get("body") or ""):
                    h = host(u)
                    if h:
                        per_thread[qid].add(h)
        any_url = set(per_thread)
        external = {q for q in per_thread
                    if per_thread[q] - {"stackoverflow.com", "i.sstatic.net",
                                        "i.stack.imgur.com"}}
        githubish = {q for q in per_thread
                     if any("github" in h or "githubusercontent" in h
                            for h in per_thread[q])}
        external_github = {q for q in external
                           if any("github" in h for h in per_thread[q])}
        out["rules"][name] = {
            "threads_with_any_url": len(any_url),
            "threads_with_external_url": len(external),
            "threads_with_github_family": len(githubish),
            "external_and_github": len(external_github),
            "host_counts": collections.Counter(
                h for hs in per_thread.values() for h in hs).most_common(10),
        }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())