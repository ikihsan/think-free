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
# itself.
LINK_SHAPES = [
    r"https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
    r"https?://(?:www\.)?(?:npmjs\.com|pypi\.org|crates\.io|crates\.io|hub\.docker\.com|ruby\.gems\.org|packagist\.org)/[A-Za-z0-9_@./-]+",
    r"https?://(?:codeberg\.org|gitlab\.com)/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
]

# A fenced code block that is not a language tag. Used only as a count of manual
# commands the document asks for, and reported as a count, never as the judgement.
SHELL_BLOCK = re.compile(r"^```(?:bash|sh|shell|console|zsh|shell-session)?\s*$",
                         re.MULTILINE)


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
    for shape in LINK_SHAPES:
        for m in re.findall(shape, body, re.IGNORECASE):
            frag = re.sub(r"^https?://", "", m.lower()).split("#")[0].rstrip("/")
            if not frag.startswith(own):
                links.add(frag)
    return {
        "repo": full_name,
        "bytes": len(body),
        "install_shapes": sorted(install),
        "install_line": bool(install),
        "foreign_links": sorted(links),
        "foreign_link": bool(links),
        "shell_blocks": len(SHELL_BLOCK.findall(body)),
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