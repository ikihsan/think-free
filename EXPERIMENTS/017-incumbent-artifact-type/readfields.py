#!/usr/bin/env python3
"""The mechanical half of 016's read protocol.

`README.md` splits the read into four fields that are decided by looking for a
string and one that is not. `install_line` and `foreign_link` are here;
`procedure` and `repeated` are judgements, written by hand into `reads.json`, and
this module only checks that every row has them and that the mechanical fields
agree with the text.

The distinction is the point. H2 survives only on rows that are `repeated` **and**
`teaches_only`, and `repeated` is the one judgement in the chain. Keeping the other
four mechanical means a reader who disagrees with my judgement can re-derive
everything the gate does not depend on, and knows exactly which single field the
disagreement is about.

    python3 readfields.py --readme owner/name      # fetch and cache one README
    python3 readfields.py --fields                # the mechanical fields
"""

import argparse
import base64
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "raw", "readmes.json")
READS = os.path.join(HERE, "reads.json")
PREV = os.path.join(os.path.dirname(HERE), "015-incumbent-serving")
for path in (PREV, HERE):
    if path not in sys.path:
        sys.path.insert(0, path)

import attribution  # noqa: E402

# Install-shaped commands. Deliberately literal: a shape that matches prose
# ("install it now") would turn a document into `tutorial` for the wrong reason,
# and `tutorial` is the class that makes H2 survive.
INSTALL_SHAPES = [
    r"pip3?\s+install", r"npm\s+(i|install|run\s+npx)\b", r"\bnpx\s+",
    r"\byarn\s+add\b", r"\bpnpm\s+(add|dlx)\b", r"brew\s+install",
    r"uvx\s+", r"uv\s+tool\s+install", r"cargo\s+install", r"go\s+install",
    r"gem\s+install", r"apt(-get)?\s+install", r"curl\b[^|\n]*\|\s*(ba)?sh",
    r"wget\b[^|\n]*\|\s*(ba)?sh", r"docker\s+run\b", r"docker\s+compose\s+up",
    r"git\s+clone\b",
]

# A link to software that is not the repository itself. Matched on an absolute
# URL, because a relative link inside the repository is the document talking about
# itself. Each entry is (host, path-prefix) and the host is part of the pattern,
# so the repository comparison below sees two path segments and not the host.
LINK_HOSTS = [
    ("github.com", 2),
    ("gitlab.com", 2),
    ("codeberg.org", 2),
]
# Registries: the path is a package name, not a repository, so any hit is foreign.
# Plain hostnames, compared as strings -- these are not patterns.
REGISTRY_HOSTS = [
    "npmjs.com", "pypi.org", "crates.io", "hub.docker.com",
    "rubygems.org", "packagist.org", "maven.org", "nuget.org",
]
URL = re.compile(r"https?://([A-Za-z0-9.-]+)(/[^\s)\"'<>]*)")

# A fenced code block with no language tag, or a shell one. Counted as *blocks*,
# not as fence lines: a pair of fences is one block, and a count of fence lines
# would double every figure. Reported as a count and never as the judgement.
SHELL_BLOCK = re.compile(r"^```(?:bash|sh|shell|console|zsh|shell-session)?\s*$",
                         re.MULTILINE)
FENCE = re.compile(r"^\s*```")


def shell_blocks(body):
    """How many untagged or shell-tagged fenced blocks the document contains."""
    inside, blocks = False, 0
    for line in body.splitlines():
        if not FENCE.match(line):
            continue
        if not inside and SHELL_BLOCK.match(line):
            blocks += 1
        inside = not inside
    return blocks


def readme(full_name):
    data = attribution.jget("https://api.github.com/repos/%s/readme" % full_name,
                            timeout=30)
    if data is attribution.REFUSED or not isinstance(data, dict):
        return None
    raw = data.get("content")
    if not isinstance(raw, str):
        return None
    try:
        return base64.b64decode(raw).decode("utf-8", "replace")
    except Exception:
        return None


def load_cache():
    if os.path.exists(CACHE):
        try:
            with open(CACHE) as fh:
                cached = json.load(fh)
            if isinstance(cached, dict):
                return cached
        except ValueError:
            pass
    return {}


def fetch_readme(full_name):
    cache = load_cache()
    text = readme(full_name)
    cache[full_name] = {"text": text, "bytes": len(text or "")}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w") as fh:
        json.dump(cache, fh, indent=1, sort_keys=True)
    return cache[full_name]


def mechanical(full_name, text):
    """The two string-decided fields, plus counts that are reported not judged."""
    body = text or ""
    install = [p for p in INSTALL_SHAPES if re.search(p, body, re.IGNORECASE)]
    own = tuple(x.lower() for x in full_name.split("/")[-2:])
    links = set()
    for host, path in URL.findall(body):
        host = host.lower()
        path = path.lower().split("#")[0].rstrip("/")
        if any(host == h or host.endswith("." + h) for h in REGISTRY_HOSTS):
            links.add(host + path)      # a package name: never the same repository
            continue
        for pattern, depth in LINK_HOSTS:
            if not (host == pattern or host.endswith("." + pattern)):
                continue
            segments = [s for s in path.split("/") if s][:depth]
            if len(segments) < depth or tuple(segments) != own:
                links.add(host + "/" + "/".join(segments))
            break
    return {
        "repo": full_name,
        "bytes": len(body),
        "install_shapes": sorted(install),
        "install_line": bool(install),
        "foreign_links": sorted(links),
        "foreign_link": bool(links),
        "shell_blocks": shell_blocks(body),
        "headings": len(re.findall(r"^#{1,3} ", body, re.MULTILINE)),
        "class": ("tutorial" if (install or links) else "teaches_only"),
    }


def fields():
    cache = load_cache()
    return {name: mechanical(name, entry.get("text"))
            for name, entry in cache.items()}


def check_reads(mech=None):
    """Shape check on the hand-written half. Returns (ok, problems).

    A missing or non-boolean `repeated` is a failure rather than a default: the
    gate would otherwise count an unread row as a negative.
    """
    if not os.path.exists(READS):
        return False, ["reads.json does not exist"]
    with open(READS) as fh:
        reads = json.load(fh)
    problems = []
    for repo, row in (reads.get("rows") or {}).items():
        if not isinstance(row.get("procedure"), str) or not row["procedure"].strip():
            problems.append("%s: no procedure quoted" % repo)
        if not isinstance(row.get("repeated"), bool):
            problems.append("%s: repeated is not a boolean" % repo)
        if not isinstance(row.get("judgement_note"), str):
            problems.append("%s: no judgement note" % repo)
    if mech is not None:
        for repo, row in (reads.get("rows") or {}).items():
            if repo in mech and row.get("class") not in (None, "tutorial", "teaches_only"):
                problems.append("%s: class %r is not one of the two" % (repo, row["class"]))
    return (not problems), problems


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--readme")
    ap.add_argument("--fields", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.readme:
        print(json.dumps(fetch_readme(args.readme), indent=1)[:400])
    if args.fields:
        print(json.dumps(fields(), indent=1, sort_keys=True))
    if args.check:
        ok, problems = check_reads(fields())
        print("reads.json:", "ok" if ok else problems)
        sys.exit(0 if ok else 1)