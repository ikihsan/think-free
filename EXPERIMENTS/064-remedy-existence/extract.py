#!/usr/bin/env python3
"""Extract named remedy artifacts from recorded model text, deterministically.

Two tiers, because a single extractor cannot be both precise and high-recall and
the protocol requires the extractor's own precision to be reported as a number:

  tier1  backticked spans, ``owner/repo`` paths, URLs, and the argument of an
         install command. High precision, lower recall.
  tier2  tier1, plus Capitalised tokens and bare lowercase tokens standing in a
         remedy position (after "with", "using", "via", "or", "and", "plus", a
         comma, or a colon). Higher recall, and it fires on words that are not
         artifacts at all.

Every extracted name is written with the span it came from so that the precision
sample can be hand-marked, and with the row it came from so the base rate can be
computed over names and over mentions separately.

Stdlib only. Run from this directory.
"""
from __future__ import print_function

import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Words that are never an artifact, however they are capitalised. Deliberately
# short: every entry here is one a plausible extractor would have thrown away,
# and the count of them is reported.
STOP = set("""
I A An The This That These Those It Its If Then So But And Or Not No Yes Do Does
Can Could Would Should Will Shall May Might Must Here There When Where Which Who
Whom What Why How Now New Old One Two Three Some Any All Each Every Both Few Many
Most Much Other Another Such Only Own Same Too Very Just Also Because Until While
Monday Tuesday Wednesday Thursday Friday Saturday Sunday January February March
April May June July August September October November December
GitHub Gitlab Google Apple Amazon Microsoft Mozilla Linux Windows macOS Android
Python JavaScript TypeScript Rust Go Java Ruby PHP Perl Haskell Elixir Kotlin
Swift C C++ C# Bash Shell SQL HTTP HTTPS JSON YAML XML CSV HTML CSS REST API
README LICENSE Docker Kubernetes Node npm pip cargo gem brew apt apt-get dnf yum
Monday Tuesday Wednesday Thursday Friday Saturday Sunday
""".split())

INSTALL_RE = re.compile(
    r"\b(?:pip3?\s+install|npm\s+(?:i|install|add)|yarn\s+add|pnpm\s+add"
    r"|cargo\s+(?:add|install)|go\s+get|gem\s+install|brew\s+install"
    r"|apt(?:-get)?\s+install|dnf\s+install|yum\s+install|apt\s+add"
    r"|dotnet\s+add|nuget\s+install|composer\s+require"
    r"|mix\s+deps\.get|swift\s+package|opam\s+install)\s+"
    r"([A-Za-z0-9@._/-]+(?:\s+[A-Za-z0-9@._/-]+){0,6})")

BACKTICK_RE = re.compile(r"`([^`]{1,80})`")
URL_RE = re.compile(r"https?://[^\s,;)]+")
SLASH_RE = re.compile(r"\b([A-Za-z0-9][A-Za-z0-9_.-]{1,40}/[A-Za-z0-9][A-Za-z0-9_.-]{1,60})\b")
REMEDY_POS_RE = re.compile(
    r"(?:\bwith\b|\busing\b|\bvia\b|\bor\b|\band\b|\bplus\b|\bthen\b|[:,]|\b)\s+"
    r"([A-Za-z][A-Za-z0-9_+.-]{1,24})\b")
CAP_RE = re.compile(r"\b([A-Z][A-Za-z0-9+]{2,20})\b")


def _clean(tok):
    return tok.strip().strip("`'\".,;:()[]").strip()


def ecosystem_for(name):
    """Which free registries this name could plausibly live in."""
    n = name.strip()
    if n.startswith("http://") or n.startswith("https://"):
        host = n.split("/")[2].lower()
        if "github.com" in host:
            return ["github"]
        if "gitlab.com" in host:
            return ["gitlab"]
        if "crates.io" in host:
            return ["crates"]
        if "npmjs.com" in host or "npmjs.org" in host:
            return ["npm"]
        if "pypi.org" in host:
            return ["pypi"]
        if "hex.pm" in host:
            return ["hex"]
        if "proxy.golang.org" in host:
            return ["go"]
        return []
    low = n.lower()
    if low.startswith("@") and "/" in low:
        return ["npm"]
    if "/" in low:
        seg = low.split("/")
        if len(seg) == 2 and all(s for s in seg):
            # owner/repo is GitHub first; a dotted or golang-ish first segment is
            # a module path.
            if "." in seg[0] or low.startswith("github.com") or low.startswith("gitlab.com"):
                return ["go", "github", "gitlab", "packagist"]
            return ["github", "packagist", "go", "pypi", "npm"]
        return []
    if low.endswith(".js") or low.endswith(".ts") or low.endswith(".mjs"):
        return ["npm"]
    if re.match(r"^[A-Za-z][A-Za-z0-9]*\.[A-Za-z][A-Za-z0-9]*$", n):
        return ["pypi"]
    # A bare name is ambiguous on purpose. Probing every free registry is the
    # conservative direction: it can only move a name out of "absent".
    return ["pypi", "npm", "crates", "gem", "packagist", "hex", "brew"]


def extract(text):
    """Return (tier1_names, tier2_names) as ordered lists of (name, span)."""
    t1, t2 = [], []
    seen1 = set()

    def add(bucket, name, span, tier):
        name = _clean(name)
        if not name or len(name) < 2:
            return
        if name in STOP or name.lower() in STOP:
            return
        key = (tier, name.lower())
        if key in seen1:
            return
        seen1.add(key)
        bucket.append((name, span))

    for m in BACKTICK_RE.finditer(text):
        add(t1, m.group(1), m.group(0), 1)
        add(t2, m.group(1), m.group(0), 2)
    for m in URL_RE.finditer(text):
        add(t1, m.group(0), m.group(0), 1)
        add(t2, m.group(0), m.group(0), 2)
    for m in SLASH_RE.finditer(text):
        tok = m.group(1)
        if tok.lower().startswith(("http", "www.")):
            continue
        add(t1, tok, tok, 1)
        add(t2, tok, tok, 2)
    for m in INSTALL_RE.finditer(text):
        for tok in m.group(1).split():
            add(t1, tok, m.group(0), 1)
            add(t2, tok, m.group(0), 2)
    # tier-2 only: capitalised tokens and bare remedy-position tokens
    for m in CAP_RE.finditer(text):
        tok = m.group(1)
        # a sentence-initial capital is not evidence of a product
        if m.start() == 0 or text[max(0, m.start() - 2):m.start()].strip(".") == "":
            continue
        add(t2, tok, text[max(0, m.start() - 24):m.end() + 8], 2)
    for m in REMEDY_POS_RE.finditer(text):
        add(t2, m.group(1), text[max(0, m.start() - 24):m.end() + 8], 2)
    return t1, t2


def main(argv):
    src = argv[0]
    out = argv[1] if len(argv) > 1 else os.path.join(RAW, "extracted.json")
    arm = argv[2] if len(argv) > 2 else "A"
    rows = list(csv.DictReader(open(src), delimiter="\t"))
    text_col = "what_a_free_assistant_supplies"
    out_rows = []
    for r in rows:
        text = r.get(text_col, "") or ""
        if not text:
            continue
        t1, t2 = extract(text)
        for tier, hits in ((1, t1), (2, t2)):
            for name, span in hits:
                out_rows.append({
                    "arm": arm,
                    "blind_id": r.get("blind_id", ""),
                    "tier": str(tier),
                    "name": name.replace("\t", " "),
                    "ecosystems": ",".join(ecosystem_for(name)),
                    "span": span.replace("\t", " "),
                })
    with open(out, "w") as fh:
        json.dump(out_rows, fh, indent=1, sort_keys=True)
    print("wrote %s (%d rows)" % (out, len(out_rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
