"""Need vocabulary and gate thresholds for the view-count experiment family.

Split out of `experiment.py` at the 300-line cap. These are the only place
the vocabulary and the gate thresholds are written down, which is why they
live here rather than inside the fetch-and-classify program.
"""

# Need indicators shared with the view-count experiment family
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
    "cache", "redis", "memcached", "eviction",
    "queue", "rabbit", "kafka", "mqtt",
    "container", "docker", "kubernetes", "orchestration",
    "micro service", "distributed", "cluster",
}

# Generic terms that classify as "random" (overly broad terms)
GENERIC_TERMS = {"utils", "common", "core", "library", "framework", "jar", "dependencies", "gem", "rake", "rails", "cpan", "perl"}

SAMPLE_SIZE = 200  # G2 gate: minimum 100 classified (we fetch 200 to ensure threshold)
MIN_CLASSIFIED = 100  # G2 gate: minimum classified for meaningful results
MIN_CLASSIFIED_G4 = 50  # G4 gate: minimum 50 classified
THRESHOLD_RATIO = 0.55  # G1: need-related active rate must be >= 55% of random active rate
