"""E165 — Vocabulary and classification utilities.

Split from run.py to stay within the 300-line cap.
"""

import re
from typing import Dict, Optional

# ---------------------------------------------------------------------------
# Vocabulary (mirrored from tools/viewcount_core.py)
# ---------------------------------------------------------------------------

NEED_INDICATORS = {
    "database", "cache", "auth", "security", "logging", "monitoring",
    "testing", "benchmark", "profiler", "tracing", "observability",
    "deployment", "ci", "cd", "pipeline", "build", "package",
    "network", "api", "client", "server", "framework", "engine",
    "parser", "lexer", "converter", "transform", "serializer",
    "validation", "sanitization", "encryption", "decryption",
    "compression", "decompression", "encoding", "decoding",
    "serialization", "deserialization", "persistance", "storage",
    "retrieval", "indexing", "search", "query", "aggregation",
    "reporting", "metrics", "observability", "dashboard",
    "debugging", "troubleshooting", "diagnostics", "audit",
    "compliance", "governance", "risk", "mitigation",
    "optimization", "performance", "scaling", "load",
    "queue", "messaging", "broker", "topic", "publish",
    "subscribe", "routing", "firehose", "stream",
    "redis", "memcached", "eviction",
    "rabbit", "kafka", "mqtt",
    "container", "docker", "kubernetes", "orchestration",
    "microservice", "distributed", "cluster",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "jar", "dependencies",
    "gem", "rake", "rails", "bundle", "assets",
}


# ---------------------------------------------------------------------------
# Classification utilities
# ---------------------------------------------------------------------------

def _matches_word_boundary(desc_lower: str, term: str) -> bool:
    return bool(re.search(r'\b' + re.escape(term) + r'\b', desc_lower))


def classify_package(description: str) -> str:
    if not description:
        return "random"
    desc_lower = description.lower()
    for term in GENERIC_TERMS:
        if _matches_word_boundary(desc_lower, term):
            return "random"
    for term in NEED_INDICATORS:
        if _matches_word_boundary(desc_lower, term):
            return "need-related"
    return "random"


def classify_by_keywords(package_info: Dict) -> Optional[str]:
    name = (package_info.get("name", "") or "").lower()
    desc = (package_info.get("description", "") or "").lower()
    for term in NEED_INDICATORS:
        if _matches_word_boundary(name, term):
            return "need-related"
    for term in GENERIC_TERMS:
        if _matches_word_boundary(name, term):
            return "random"
    return None


def is_active(package_info: Dict) -> bool:
    desc = package_info.get("description", "") or ""
    version = package_info.get("version", "") or ""
    return len(desc.strip()) > 0 and version != ""