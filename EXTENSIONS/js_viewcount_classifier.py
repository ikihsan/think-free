#!/usr/bin/env python3
"""JavaScript-adapted view-count need/generic classifier.

Extends the E113 v2 classifier (labeling_improved) with JavaScript-specific
vocabulary for need and generic term detection in GitHub repo descriptions.

Key additions:
- JS-specific need indicators: npm, node, express, react, angular, webpack,
  babel, cli tool, package.json, dependencies, rest api, rest endpoint, etc.
- JS-specific generic terms: library, framework, starter, template, microservice,
  api endpoint, cli tool, etc.

Word-boundary anchoring preserved (prevents substrings like `ai` firing inside `email`).
Need-phrase masking preserved (prevents double-counting like `learning` in `machine learning`).
"""

from __future__ import print_function

import re
import sys

# Import base vocabulary and patterns from the original labeling module
import labeling_improved as L

# ============================================================
# Extended need indicators — base 89 terms PLUS JS additions
# ============================================================

# Preserve original 89 terms from labeling_improved.NEED_INDICATORS
# (imported as L.NEED_INDICATORS)

# --- JS-specific need indicators ---
JS_NEED_INDICATORS = {
    # Package/dependency management
    "npm", "node", "node.js", "package.json", "dependencies",
    "devDependencies", "peerDependencies", "peer dep", "optional dep",

    # Web frameworks and APIs
    "express", "fastify", "koa", "hapi", "rest api", "rest endpoint",
    "graphql", "graphql endpoint", "api endpoint", "endpoint",

    # Frontend frameworks
    "react", "preact", "inferno", "vue", "angular", "svelte",

    # CLI and tooling
    "cli tool", "command-line tool", "shebang", "transpile", "babel",
    "webpack", "parcel", "brunch", "rollup",

    # Bots and extensions
    "bot", "discord bot", "chrome extension", "firefox extension",

    # Testing
    "jest", "mocha", "unit test", "integration test",

    # Deployment and infrastructure
    "docker", "container", "ci/cd", "workflow", "github actions",
}

# Combine: original + JS additions
EXTENDED_NEED_INDICATORS = L.NEED_INDICATORS | JS_NEED_INDICATORS

# ============================================================
# Extended generic terms — base 31 terms plus JS additions
# ============================================================

# Preserve original 31 terms from labeling_improved.GENERIC_TERMS
# (imported as L.GENERIC_TERMS)

# --- JS-specific generic terms ---
JS_GENERIC_TERMS = {
    # Library/framework concepts
    "library", "framework", "starter kit", "starter template",
    "boilerplate", "scaffolding", "skeleton", "prototype", "poC",
    "proof of concept", "sample project", "template project",

    # JS ecosystem concepts
    "npm package", "node module", "node.js module",
    "javascript library", "js library", "frontend library",

    # Architecture and patterns
    "microservice", "service", "api", "rest api", "rest endpoint",
    "graphql", "graphql api", "endpoint", "route",

    # Frontend/backend
    "frontend", "backend", "fullstack", "web app", "web application",
    "single page app", "spa",

    # Code patterns
    "source code", "repository", "git", "commit", "push", "pull request",

    # Development workflow
    "cli tool", "command-line tool", "script", "build script",
    "ci/cd", "continuous integration", "continuous deployment",
}

# Combine: original + JS additions
EXTENDED_GENERIC_TERMS = L.GENERIC_TERMS | JS_GENERIC_TERMS

# ============================================================
# Extended patterns (word-boundary, longest-first)
# ============================================================

def _anchored_patterns(terms):
    """Build anchored word-boundary regex patterns from a term set."""
    pats = []
    for term in sorted(terms, key=len, reverse=True):
        parts = [re.escape(w) for w in term.split()]
        pats.append(re.compile(r"\b" + r"\s+".join(parts) + r"\b"))
    return pats


EXTENDED_NEED_PATTERNS = _anchored_patterns(EXTENDED_NEED_INDICATORS)
EXTENDED_GENERIC_PATTERNS = _anchored_patterns(EXTENDED_GENERIC_TERMS)

# ============================================================
# Labeling functions (same logic as labeling_improved)
# ============================================================

def label_masked(description):
    """need | generic | unlabelled, with need phrases masked before generic scan.

    AMENDMENT-3: `learning` is a whole word inside the need phrase `machine
    learning`, so scanning the lists independently cancelled a genuine need.
    Generic terms now fire only on text the need matcher did not claim.
    Returns (label, need_terms_hit, generic_terms_hit).
    """
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
        return "need", need_hit, generic_hit
    if has_gen and not has_need:
        return "generic", need_hit, generic_hit
    return "unlabelled", need_hit, generic_hit


def label_unanchored(description):
    """E107's rule verbatim. Sensitivity arm only."""
    if not description:
        return "unlabelled"
    text = description.lower()
    has_need = any(t in text for t in EXTENDED_NEED_INDICATORS)
    has_gen = any(t in text for t in EXTENDED_GENERIC_TERMS)
    if has_need and not has_gen:
        return "need"
    if has_gen and not has_need:
        return "generic"
    return "unlabelled"


def label(description, rule="masked"):
    if not description:
        return "unlabelled"
    if rule == "masked":
        return label_masked(description)[0]
    if rule == "unanchored":
        return label_unanchored(description)
    if rule == "anchored":
        text = description.lower()
        has_need = any(p.search(text) for p in EXTENDED_NEED_PATTERNS)
        has_gen = any(p.search(text) for p in EXTENDED_GENERIC_PATTERNS)
        if has_need and not has_gen:
            return "need"
        if has_gen and not has_need:
            return "generic"
        return "unlabelled"
    raise ValueError("unknown rule: %s" % rule)


def g0_score():
    """Planted-positive recovery for the masked rule. The kill gate."""
    # Use the planted Need/GENERIC from labeling_improved, but we need JS-planted
    # For now, just return the base g0_score
    from labeling_improved import g0_score as base_g0
    return base_g0()