#!/usr/bin/env python3
"""E113 — the need/generic labeler, split out of analyze.py.

Three rules live here, all after the row is already in the matched pool:

  unanchored  E107's own rule, verbatim substring containment. Kept as the
              sensitivity arm so a harvest-design comparison is not confounded
              with the labeler repair (AMENDMENT-2).
  anchored    word-boundary matching, so `ai` stops firing inside `email`
              (AMENDMENT-2).
  masked      anchored, with matched need phrases masked out before the generic
              scan, so `learning` stops cancelling `machine learning`
              (AMENDMENT-3). This is the primary rule.

The vocabulary is E107's own (from
EXPERIMENTS/107-github-repos-viewcount/harvest.py), unmodified, applied to a
pool whose harvest query contains none of it.

Stdlib only. Import from analyze.py and stratified.py.
"""
from __future__ import print_function

import re

# ---------------------------------------------------------------- vocabulary
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
    "email", "notification", "push", "file storage", "object storage", "s3",
    "search", "elasticsearch", "fulltext", "machine learning", "ml", "ai",
    "data processing", "etl", "streaming", "data pipeline",
    "load balancing", "rate limiting", "circuit breaker", "retry", "timeout",
    "router", "routing", "middleware", "dependency injection", "cli",
    "command line", "argument parsing", "template engine", "rendering",
    "migration", "seeding", "factory", "active record",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "package", "tool", "util", "helper",
    "base", "standard", "stdlib", "internal", "private", "experimental",
    "template", "boilerplate", "scaffold", "starter", "example", "demo",
    "tutorial", "learning", "practice", "playground", "sandbox", "toy",
    "sample", "proof of concept", "poc", "prototype", "experiment",
}

# G0 planted positives: name a technology that IS a need, carry no generic
# vocabulary. AMENDMENT-3 records the one-word deletion to the "Kafka ... "
# probe, which named a packaging form as well and so violated this rule.
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
# G0 planted negatives: generic scaffolding text, no technology named.
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


def _anchored_patterns(terms):
    """Word-boundary patterns, longest term first.

    AMENDMENT-2: unanchored containment fired `ai` inside `email`, `ml` inside
    `html`, `cli` inside `client`. Multi-word terms match as whole phrases.
    """
    pats = []
    for term in sorted(terms, key=len, reverse=True):
        parts = [re.escape(w) for w in term.split()]
        pats.append(re.compile(r"\b" + r"\s+".join(parts) + r"\b"))
    return pats


NEED_PATTERNS = _anchored_patterns(NEED_INDICATORS)
GENERIC_PATTERNS = _anchored_patterns(GENERIC_TERMS)


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
    for pat in NEED_PATTERNS:  # already longest-first
        masked, n = pat.subn(" ", masked)
        if n:
            need_hit.append(pat.pattern)
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


def label(description, rule="masked"):
    if not description:
        return "unlabelled"
    if rule == "masked":
        return label_masked(description)[0]
    if rule == "unanchored":
        return label_unanchored(description)
    if rule == "anchored":
        # anchored but without masking: the AMENDMENT-2 behaviour
        text = description.lower()
        has_need = any(p.search(text) for p in NEED_PATTERNS)
        has_gen = any(p.search(text) for p in GENERIC_PATTERNS)
        if has_need and not has_gen:
            return "need"
        if has_gen and not has_need:
            return "generic"
        return "unlabelled"
    raise ValueError("unknown rule: %s" % rule)


def g0_score():
    """Planted-positive recovery for the masked rule. The kill gate."""
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