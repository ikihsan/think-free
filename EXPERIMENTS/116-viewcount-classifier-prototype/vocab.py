"""Vocabulary for the E116 view-count classifier.

Split out of `classify.py` at the repository's 300-line cap. This module
owns the two term sets and the disambiguation window; it has no dependency
on the classifier or on the experiment driver.
"""

# ── Vocabulary ──────────────────────────────────────────────────

# Need indicators: terms that suggest the package addresses a programming need.
# Carefully curated to avoid package-name collisions (e.g., "plug" removed).
NEED_INDICATORS = {
    # Web infrastructure
    "web", "rest", "api", "http", "client", "server", "framework",
    # Database & storage
    "database", "orm", "sql", "postgres", "mysql", "mariadb", "redis",
    "mongo", "mongodb", "elasticsearch", "couchdb", "storage", "cache",
    "persistent", "state",
    # Authentication & security
    "auth", "oauth", "oidc", "jwt", "session", "cookie", "security",
    "encrypt", "decrypt", "sign", "verify", "validator", "schema",
    # Networking & communication
    "socket", "tcp", "udp", "http", "rest", "grpc", "websocket",
    "pubsub", "messaging", "queue", "topic", "broker", "channel",
    # Testing & CI
    "test", "mock", "fixture", "benchmark", "profile", "fuzz",
    "continuous", "integration", "deployment",
    # Elixir/Erlang specific (for Hex.pm coverage)
    "ecto", "phoenix", "plug", "absinthe", "tesla", "finch",
    "httpoison", "jason", "poison",
    # General programming need terms
    "cli", "command", "argument", "flag", "option",
    "migration", "schema", "seed", "factory",
    "pubsub", "broadcast", "channel", "presence",
    "exq", "oban", "quantum", "cron", "scheduler",
    "broadway", "genstage", "flow", "stream",
    "nimble", "csv", "excel", "pdf", "docx",
    "timex", "calendar", "tzdata", "chrono",
    "decimal", "money", "currency", "exchange",
    "uuid", "ulid", "nanoid", "slug", "parameterize",
    "json",
    "token",
    "crypto"
}


# Truly generic terms: always disqualifying when present (with disambiguation)
GENERIC_TERMS = {
    # Generic packaging/container labels
    "base", "minimal", "alpine", "scratch", "distroless", "slim",
    # Version/channel labels
    "latest", "stable", "edge", "main", "master", "dev", "test",
    # Example/demo/tutelage
    "example", "demo", "sample", "template", "boilerplate",
    "sandbox", "playground", "poc", "prototype", "experiment",
    # Learning/training
    "tutorial", "learning", "workshop",
    # Vague qualification
    "personal", "private", "internal", "custom",
    # Version control / copies
    "fork", "mirror", "copy", "backup", "archive", "old",
    # Maintenance status
    "deprecated", "legacy", "unmaintained", "abandoned",
    # Always-generic computing terms
    "utils", "common", "core", "library", "package", "tool", "util",
    "helper",
    # Infrastructure labels
    "ci", "build", "builder", "compile", "runtime", "debug",
    # Always-generic example markers
    "example", "demo", "tutorial",
}


# Token window for contextual disambiguation
DISAMBIG_WINDOW = 3  # tokens left/right
