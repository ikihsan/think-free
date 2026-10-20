"""Classifier core for the E130 view-count classifier v3.

Split out of `classify.py` at the repository's 300-line cap. This module
owns tokenisation, contextual disambiguation, and the classifier entry points.
It reads the vocabulary from `vocab.py` and nothing else from the experiment.
"""

import re

# Vocabulary definitions for the E130 view-count classifier v3.
# Kept inline to avoid import-chain issues (classify_core -> vocab -> classify_core).

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


def tokenize(text):
    """Tokenize text into lowercase words, preserving hyphens within words,
    splitting on non-alphanumeric characters.

    v3: Returns only whole-word tokens. No substring matching.
    """
    if not text:
        return []
    tokens = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())
    return tokens


def window_tokens(tokens, center, window=DISAMBIG_WINDOW):
    """Return tokens in [center-window, center+window] range."""
    start = max(0, center - window)
    end = min(len(tokens), center + window + 1)
    return tokens[start:end]


def has_need_context(tokens, idx, need_set, generic_set, window=DISAMBIG_WINDOW):
    """Check if tokens[idx] carries need-specific context.

    v3: A term from NEED_INDICATORS that also appears in GENERIC_TERMS is only
    counted if it has contextual support from other need indicators within
    the disambiguation window. No substring fallback.
    """
    token = tokens[idx]
    if token not in need_set:
        return False
    if token not in generic_set:
        return True
    # Token is both a need indicator and a generic term — requires contextual support
    # Check nearby token indices (within disambiguation window) for other need indicators
    top = min(len(tokens), idx + window + 1)
    bottom = max(0, idx - window)
    for j in range(bottom, top):
        if j == idx:
            continue
        if tokens[j] in need_set:
            return True
    for offset in range(1, window + 1):
        if idx - offset >= 0 and tokens[idx - offset] in need_set:
            return True
        if idx + offset < len(tokens) and tokens[idx + offset] in need_set:
            return True
    return False


def classify_repo(name, description):
    """Classify a repository/package by name and description (v3).

    Returns (classification, confidence, coverage_weight).
    classification: "need-related", "random", or "uncertain"
    confidence: float in [0, 1] - higher is more confident (0.0 = uncertain)
    coverage_weight: float in [0, 1] - 1.0 = fully classified, 0.0 = uncertain

    v3 KEY CHANGES vs E116:
    - No substring matching in names (eliminates E113/F116 binding constraint)
    - Combined name+description scoring (not name-first fallback)
    - Uncertainty weighting: weak signals -> "uncertain" weight=0, excluded from arms
    - Stricter generic term disambiguation with contextual window
    - Matched-harvest compatible: both arms drawn from same pool, classified differently
    """
    description = description or ""
    fullname = name

    # ── Step 1: Tokenize name and description ────────────────────────────
    name_tokens = tokenize(fullname.lower())
    desc_tokens = tokenize(description.lower())
    all_tokens = name_tokens + desc_tokens  # combined pool for disambiguation

    # ── Step 2: Count need and generic token matches ─────────────────────
    need_in_name = sum(1 for tok in name_tokens if tok in NEED_INDICATORS)
    generic_in_name = sum(1 for tok in name_tokens if tok in GENERIC_TERMS)
    need_in_desc = sum(1 for tok in desc_tokens if tok in NEED_INDICATORS)
    generic_in_desc = sum(1 for tok in desc_tokens if tok in GENERIC_TERMS)

    # Track which need tokens have contextual support
    need_indices = []  # (token_index, is_name) in all_tokens
    generic_indices = []  # token_index in all_tokens
    need_context_count = 0  # number of need tokens with contextual support

    # Check name tokens for need/generic status with context
    name_offset = 0
    for i, tok in enumerate(name_tokens):
        if tok in NEED_INDICATORS:
            abs_idx = name_offset + i
            if has_need_context(all_tokens, abs_idx, NEED_INDICATORS, GENERIC_TERMS, DISAMBIG_WINDOW):
                need_context_count += 1
                need_indices.append((abs_idx, "name"))
            else:
                # Need indicator without contextual support — downweight but don't discard
                need_context_count += 0.5
                need_indices.append((abs_idx, "name"))
        if tok in GENERIC_TERMS:
            generic_indices.append(name_offset + i)
        name_offset += 1

    # Check description tokens for need/generic status with context
    desc_offset = len(name_tokens)
    for i, tok in enumerate(desc_tokens):
        abs_idx = desc_offset + i
        if tok in NEED_INDICATORS:
            if has_need_context(all_tokens, abs_idx, NEED_INDICATORS, GENERIC_TERMS, DISAMBIG_WINDOW):
                need_context_count += 1
                need_indices.append((abs_idx, "desc"))
            else:
                need_context_count += 0.5
                need_indices.append((abs_idx, "desc"))
        if tok in GENERIC_TERMS:
            generic_indices.append(abs_idx)

    effective_need = need_context_count  # weighted count (full or 0.5 for no context)
    effective_generic = len(generic_indices)

    # ── Step 3: Classification decision ──────────────────────────────────

    # Case: No need or generic tokens recognized at all
    if effective_need == 0 and effective_generic == 0:
        # No recognized terms — truly uncertain; no forced classification
        return "uncertain", 0.0, "no recognized need or generic tokens in name or description"

    # Case: Need signals present but generic signals also present
    if effective_need > 0 and effective_generic > 0:
        # Check if need tokens have contextual support within generic window
        need_in_generic_window = 0
        for gidx in generic_indices:
            for nidx, nsource in need_indices:
                dist = abs(nidx - gidx)
                if dist <= DISAMBIG_WINDOW:
                    # Contextual support: need token within disambiguation window of generic
                    need_in_generic_window += 1
                    break

        if need_in_generic_window > effective_generic / 2:
            # Need tokens outweigh generic tokens within disambiguation window
            return "need-related", 0.8, f"{int(effective_need)} need-specific token(s) outweigh {effective_generic} generic tokens (with context)"
        else:
            # Generic tokens dominate — classify as random
            return "random", 0.7, f"{int(effective_need)} need token(s) but {effective_generic} generic dominates"

    # Case: Only need signals present (no generic conflict)
    if effective_need > 0 and effective_generic == 0:
        # Check if we have enough need-specific signal
        if effective_need >= 2:
            # Strong signal: 2+ need indicators with contextual support
            return "need-related", 1.0, f"{int(effective_need)} need-specific token(s) found (name and description)"
        if effective_need == 1:
            # Single need indicator — check if it's in the name or description
            # Names carry stronger signal; descriptions carry weaker but useful signal
            # Classify based on where the single need token came from
            need_source = [ns for idx, ns in need_indices if idx < len(name_tokens)]
            if need_source:
                # Need indicator in name — stronger signal
                return "need-related", 0.9, "1 need indicator in package name"
            else:
                # Need indicator only in description — weaker signal
                return "need-related", 0.6, "1 need indicator in package description"

    # Case: Only generic signals present (no need signals with context)
    if effective_need == 0 and effective_generic > 0:
        # Check if any generic tokens are in the name vs description
        # Generic names are common; classify as random
        return "random", 0.8, f"{effective_generic} generic token(s) in name/description, no need-specific signals"

    # Fallback: should not reach here, but just in case
    return "uncertain", 0.0, "classification indeterminate"