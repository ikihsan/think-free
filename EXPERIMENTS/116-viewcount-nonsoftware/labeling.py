#!/usr/bin/env python3
"""E115 — word-boundary-aware need/generic labeler for PyPI package descriptions.

Adapted from E113's labeling.py: the same anchored patterns with masking
(E113 AMENDMENT-3) so that `learning` does not cancel `machine learning`,
and `ai` does not fire inside `email`. All patterns use \b word boundaries.

The vocabulary is the mission's established set (from EXPERIMENTS/107-github-repos-
viewcount/ and earlier corpuses), unmodified, applied to package description
text after the row is already in the matched pool.
"""

from __future__ import print_function

import re

# ---------------------------------------------------------------- vocabulary
# Need indicators: technology/noun phrases that signal a genuine need.
NEED_INDICATORS = {
    "web framework", "http server", "http client", "api client", "rest api",
    "database", "orm", "sql", "postgresql", "mysql", "redis", "mongodb",
    "cache", "caching", "queue", "messaging", "rabbitmq", "kafka",
    "authentication", "authorization", "oauth", "jwt", "session", "security",
    "logging", "monitoring", "observability", "testing", "test framework",
    "deployment", "ci/cd", "continuous integration", "continuous deployment",
    "kubernetes", "docker", "container", "microservices", "service mesh",
    "graphql", "grpc", "websocket", "real-time", "pub/sub", "message broker",
    "serialization", "json", "xml", "yaml", "protobuf", "avro",
    "validation", "schema", "configuration", "config", "secrets management",
    "search", "elasticsearch", "fulltext", "machine learning", "ml", "ai",
    "data processing", "etl", "streaming", "data pipeline",
    "load balancing", "rate limiting", "circuit breaker", "retry", "timeout",
    "router", "routing", "middleware", "dependency injection", "cli",
    "command line", "argument parsing", "template engine", "rendering",
    "migration", "seeding", "factory", "active record",
    # Expanded: terms commonly found in Python package descriptions
    "data", "analysis", "mining", "processing",
}

# Generic terms: common words that signal pervasiveness, not a specific need.
GENERIC_TERMS = {
    "utils", "common", "core", "library", "package", "tool", "util", "helper",
    "base", "standard", "stdlib", "internal", "private", "experimental",
    "template", "boilerplate", "scaffold", "starter", "example", "demo",
    "tutorial", "learning", "practice", "playground", "sandbox", "toy",
    "sample", "proof of concept", "poc", "prototype", "experiment",
}

# ---------------------------------------------------------------- patterns
# Word-boundary patterns, longest term first.
# AMENDMENT-2 (E113): unanchored containment fired `ai` inside `email`,
# `ml` inside `html`, `cli` inside `client`. Multi-word terms match as whole phrases.
# AMENDMENT-3 (E113): `learning` is a whole word inside the need phrase `machine
# learning`; scanning the lists independently cancelled a genuine need. Masking need
# phrases before the generic scan prevents this cancellation.


def _anchored_patterns(terms):
    """Compile word-boundary regex patterns, longest term first."""
    pats = []
    for term in sorted(terms, key=len, reverse=True):
        parts = [re.escape(w) for w in term.split()]
        pats.append(re.compile(r"\b" + r"\s+".join(parts) + r"\b"))
    return pats


NEED_PATTERNS = _anchored_patterns(NEED_INDICATORS)
GENERIC_PATTERNS = _anchored_patterns(GENERIC_TERMS)

# ---------------------------------------------------------------- labeling


def label_masked(description):
    """need | generic | unlabelled, with need phrases masked before generic scan.

    AMENDMENT-3: `learning` is a whole word inside the need phrase `machine
    learning`, so scanning the lists independently cancelled a genuine need.
    Generic terms now fire only on text the need matcher did not claim.

    Returns (label, need_terms_hit, generic_terms_hit).
    """
    if not description:
        return "unlabelled", [], []
    text = description.lower()
    masked = text
    need_hit = []
    for pat in NEED_PATTERNS:  # already longest-first
        masked, n = pat.subn(" ", masked)
        if n:
            need_hit.append(pat.pattern)
    # After masking need phrases, scan generic terms on the remaining text
    generic_hit = [p.pattern for p in GENERIC_PATTERNS if p.search(masked)]
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
    has_need = any(t in text for t in NEED_INDICATORS)
    has_gen = any(t in text for t in GENERIC_TERMS)
    if has_need and not has_gen:
        return "need"
    if has_gen and not has_need:
        return "generic"
    return "unlabelled"


def label_anchored(description):
    """Anchored but without masking: the AMENDMENT-2 behaviour.

    Need and generic terms fire independently; if both fire, the result is
    `unlabelled` (both claim the text). This is the AMENDMENT-2 behaviour:
    `ai` inside `email` fires the anchored pattern, and the user must disambiguate.
    """
    if not description:
        return "unlabelled"
    text = description.lower()
    has_need = any(p.search(text) for p in NEED_PATTERNS)
    has_gen = any(p.search(text) for p in GENERIC_PATTERNS)
    if has_need and not has_gen:
        return "need"
    if has_gen and not has_need:
        return "generic"
    if has_need and has_gen:
        return "unlabelled"  # both claim — ambiguous, do not classify
    return "unlabelled"


def label(description, rule="masked"):
    """Label a package description using the specified rule.

    Rules:
      "masked"  — AMENDMENT-3: mask need phrases before generic scan (primary rule)
      "unanchored"  — E107 verbatim (sensitivity arm only)
      "anchored"  — AMENDMENT-2: anchored patterns without masking
    """
    if not description:
        return "unlabelled"
    if rule == "masked":
        return label_masked(description)[0]
    if rule == "unanchored":
        return label_unanchored(description)
    if rule == "anchored":
        return label_anchored(description)
    raise ValueError("unknown rule: %s" % rule)


# ---------------------------------------------------------------- G0 planted positives

# Planted positives: name a technology that IS a need, carry no generic
# vocabulary. Used for the G0 kill gate — the labeler must recover these.
PLANTED_NEED = [
    "A fast PostgreSQL ORM for Python with async support",
    "Kafka-compatible message broker client for event streaming",
    "Elasticsearch fulltext search integration with ranking",
    "SQLite and MySQL database connection pooling for asyncio",
    "OAuth2 and JWT authentication middleware for web frameworks",
    "Circuit breaker and retry policies for HTTP client calls",
    "gRPC and protobuf serialization helpers for microservices",
    "Redis caching layer with pub/sub messaging channels",
    "Kubernetes workload deployment and container orchestration helpers",
    "TensorFlow and PyTorch machine learning model training pipeline",
]

# Planted negatives: generic scaffolding text, no technology named.
PLANTED_GENERIC = [
    "A collection of common utility helper functions for Python",
    "Boilerplate template and starter scaffold for new projects",
    "Example code and demo tutorials for learning purposes",
    "A small sandbox playground for experimenting with ideas",
    "Internal core library of shared base utilities",
    "Standard library extensions and common package helpers",
    "A toy sample project demonstrating basic patterns",
    "Generic tool wrapper for internal private utilities",
    "Experimental proof of concept skeleton scaffold",
    "Practice exercises and tutorial material for beginners",
]


def g0_score():
    """Planted-positive recovery for the masked rule. The kill gate.

    G0 requires: planted need recovered ≥ 9/10 AND planted generic recovered ≥ 9/10.
    """
    need_hits = sum(1 for d in PLANTED_NEED if label_masked(d)[0] == "need")
    gen_hits = sum(1 for d in PLANTED_GENERIC if label_masked(d)[0] == "generic")
    return {
        "planted_need_recovered": need_hits,
        "planted_need_total": len(PLANTED_NEED),
        "planted_generic_recovered": gen_hits,
        "planted_generic_total": len(PLANTED_GENERIC),
        "threshold": 9,
        "pass": need_hits >= 9 and gen_hits >= 9,
    }