#!/usr/bin/env python3
"""Quick test: label JavaScript repos with JS-adapted v2 classifier."""
from __future__ import print_function

import os, sys, json, time, re

# Resolve paths relative to script location
script_dir = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(script_dir)
elev = os.path.join(parent, '113-viewcount-matched-harvest')

# Clear any cached labeling modules
for mod in list(sys.modules.keys()):
    if 'labeling' in mod:
        del sys.modules[mod]

sys.path.insert(0, elev)
import labeling_improved as L_base

# JS-specific need indicators (added to base vocabulary)
JS_NEED_INDICATORS = {
    "npm", "node", "package.json", "express", "react", "cli tool",
    "rest api", "rest endpoint", "graphql", "graphql endpoint",
    "api endpoint", "endpoint", "docker", "container", "ci/cd",
    "github actions", "bot", "discord bot", "chrome extension",
    "jest", "mocha", "unit test", "integration test",
}

# JS-specific generic terms
JS_GENERIC_TERMS = {
    "library", "framework", "starter kit", "starter template",
    "boilerplate", "scaffolding", "skeleton", "prototype", "poC",
    "proof of concept", "sample project", "template project",
    "npm package", "node module", "javascript library", "js library",
    "frontend", "backend", "fullstack", "web app", "web application",
    "single page app", "spa", "source code", "repository", "git",
    "cli tool", "command-line tool", "script", "build script",
    "ci/cd", "continuous integration", "continuous deployment",
}

# Build extended vocabularies
EXTENDED_NEED_INDICATORS = L_base.NEED_INDICATORS | JS_NEED_INDICATORS
EXTENDED_GENERIC_TERMS = L_base.GENERIC_TERMS | JS_GENERIC_TERMS

# Build anchored patterns (longest-first), same as labeling_improved v2
def _anchored_patterns(terms):
    pats = []
    for term in sorted(terms, key=len, reverse=True):
        parts = [re.escape(w) for w in term.split()]
        pats.append(re.compile(r"\b" + r"\s+".join(parts) + r"\b"))
    return pats

EXTENDED_NEED_PATTERNS = _anchored_patterns(EXTENDED_NEED_INDICATORS)
EXTENDED_GENERIC_PATTERNS = _anchored_patterns(EXTENDED_GENERIC_TERMS)

# Read the raw pool
with open(os.path.join(script_dir, "raw_pool.json"), 'r') as f:
    pool = json.load(f)

print("Pool rows: %d" % len(pool))
start = time.time()
labels = []
for i, row in enumerate(pool):
    description = row.get("description")
    if description:
        text = description.lower()
        masked = text
        need_hit = []
        for pat in EXTENDED_NEED_PATTERNS:  # already longest-first
            masked, n = pat.subn(" ", masked)
            if n:
                need_hit.append(pat.pattern)
        generic_hit = [p.pattern for p in EXTENDED_GENERIC_PATTERNS if p.search(masked)]
        has_need, has_gen = bool(need_hit), bool(generic_hit)
        if has_need and not has_gen:
            label = "need"
        elif has_gen and not has_need:
            label = "generic"
        else:
            label = "unlabelled"
    else:
        label = "unlabelled"
    labels.append(label)
    if (i + 1) % 100 == 0:
        print("  Labeled %d/%d (%.1fs)" % (i + 1, len(pool), time.time() - start))
        start = time.time()

need_count = sum(1 for l in labels if l == "need")
generic_count = sum(1 for l in labels if l == "generic")
unlabelled_count = sum(1 for l in labels if l == "unlabelled")

print()
print("Label counts (JS-adapted v2 classifier):")
print("  need: %d" % need_count)
print("  generic: %d" % generic_count)
print("  unlabelled: %d" % unlabelled_count)
print("  total: %d" % len(labels))
print()

# G1 check: need >= 100 AND generic >= 100
g1_pass = need_count >= 100 and generic_count >= 100
print("G1 (population >= 100/100): %s (need=%d, generic=%d)" %
      ('PASS' if g1_pass else 'FAIL', need_count, generic_count))

# Coverage comparison
old_cover = 38.2  # E113 Python v2 coverage from improvement summary
new_cover_pct = 100.0 * (need_count + generic_count) / len(labels)
print()
print("Coverage comparison:")
print("  Python v2 (E113): %.1f%%" % old_cover)
print("  JS-adapted: %d/%d = %.1f%%" % (need_count + generic_count, len(labels), new_cover_pct))
print("  Improved: %s" % ('YES' if new_cover_pct > old_cover else 'NO'))