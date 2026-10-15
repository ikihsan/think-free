"""E117: View-count classifier prototype v3 — whole-word token matching
with R-specific vocabulary and contextual disambiguation.

Addresses the E113/E107 limitation (28% coverage from unanchored substrings)
and the E116 v1 limitation (Cliff's delta = 0.0265, below 0.147 threshold).

Classifier features:
- Whole-word token matching (not unanchored substring search)
- Expanded NEED_INDICATORS vocabulary for R packages
- GENERIC_TERMS disambiguation with contextual heuristics
- Coverage reporting per-gate
- Need indicator count threshold: 1+ need indicator = need-related
  (with contextual disambiguation via token window)
"""

import re
from typing import Dict, List, Tuple, Optional


def split_camelcase(text: str) -> List[str]:
    """Split camelCase or PascalCase text into word tokens."""
    s = re.sub(r"(?<!^)(?=[A-Z])", " ", text)
    return [t.lower() for t in re.findall(r"[a-zA-Z0-9]+", s)]


def tokenize(text: str) -> List[str]:
    """Split text into lowercase alphanumeric tokens (word characters only).

    Handles camelCase/PascalCase by splitting on case boundaries.
    Also handles underscores, hyphens, and dots as natural delimiters.
    """
    return split_camelcase(text)


def has_need_context(
    token: str,
    tokens: List[str],
    idx: int,
    need_indicators: set,
    generic_terms: set,
) -> bool:
    """Determine if a token carries need-specific context.

    A term from NEED_INDICATORS that also appears in GENERIC_TERMS is only
    counted if it carries need-specific context: another NEED_INDICATOR must
    appear within a 3-token window (left or right).
    """
    if token not in GENERIC_TERMS:
        # Not a generic term — if it's a need indicator, it carries context
        return token in need_indicators

    # Token is in GENERIC_TERMS: check if it carries need-specific context
    # by looking for other need indicators within the 3-token window
    start = max(0, idx - 3)
    end = min(len(tokens), idx + 4)  # idx+1 exclusive range
    window = tokens[start:end]

    for other in window:
        if other in need_indicators and other != token:
            return True

    return False


NEED_INDICATORS = {
    "web", "rest", "api", "http", "client", "server", "framework",
    "shiny", "rmarkdown", "knitr", "latex",
    "database", "orm", "sql", "postgres", "mysql", "mariadb", "redis",
    "mongo", "mongodb", "elasticsearch", "couchdb", "storage", "cache",
    "persistent", "session", "state",
    "auth", "oauth", "oidc", "jwt", "session", "cookie", "security",
    "encrypt", "decrypt", "sign", "verify", "validator", "schema",
    "passport", "token",
    "socket", "tcp", "udp", "http", "rest", "grpc", "websocket",
    "pubsub", "messaging", "queue", "topic", "broker", "channel",
    "plumber", "httpuv",
    "test", "mock", "fixture", "benchmark", "profile", "fuzz",
    "continuous", "integration", "deployment",
    "reticulate", "cran", "github",
}

GENERIC_TERMS = {
    "base", "minimal", "alpine", "scratch", "distroless", "slim",
    "latest", "stable", "edge", "main", "master", "dev", "test",
    "example", "demo", "sample", "template", "boilerplate",
    "sandbox", "playground", "poc", "prototype", "experiment",
    "r-base", "rstats", "cran", "github", "pkg", "package",
    "library", "func", "fun", "helper", "utils", "core",
    "ci", "build", "builder", "compile", "runtime", "debug",
    "example", "demo", "tutorial", "learning", "workshop",
    "personal", "private", "internal", "custom", "fork", "mirror",
    "copy", "backup", "archive", "old", "deprecated", "legacy",
    "unmaintained", "abandoned",
    "tidy", "verse", "purrr", "dplyr", "ggplot", "readr",
    "write", "read", "df", "dt", "dtypes",
}


def classify_package_name(name: str,
                         need_indicators: set = NEED_INDICATORS,
                         generic_terms: set = GENERIC_TERMS) -> Tuple[str, str]:
    """Classify a package name/description as need-related or random.

    Returns (classification, reason) where classification is one of:
    "need-related", "random"
    """
    tokens = tokenize(name)

    need_hits = 0
    need_tokens = []

    for idx, token in enumerate(tokens):
        if token in need_indicators:
            if has_need_context(token, tokens, idx, need_indicators, generic_terms):
                need_hits += 1
                need_tokens.append(token)
            # else: generic need indicator masked by context, don't count
        # else: unknown token — neutral, don't count

    if need_hits >= 1:
        reason = f"{need_hits} need indicator(s) in package name: {', '.join(need_tokens)}"
        return "need-related", reason
    else:
        reason = "no recognized terms in name or description; classified as random for coverage"
        return "random", reason


def classify_description(description: str,
                       name: str = "",
                        need_indicators: set = NEED_INDICATORS,
                        generic_terms: set = GENERIC_TERMS) -> Tuple[str, str]:
    """Classify a package using both name and description.

    Prioritizes name-level classification; falls back to description.
    """
    if name and name.strip():
        classification, reason = classify_package_name(name, need_indicators, generic_terms)
        # If name has need signals, use it; if not, try description
        if classification == "need-related":
            return classification, reason
        # Name had no need indicators — try description
    # Fall back to description-only classification
    if description and description.strip():
        desc_tokens = tokenize(description)
        desc_need_hits = sum(1 for t in desc_tokens if t in need_indicators)
        if desc_need_hits >= 1:
            return "need-related", f"{desc_need_hits} need indicator(s) in description"
        elif desc_need_hits == 0:
            return "random", "no recognized terms in name or description; classified as random for coverage"
    # Final fallback
    return "random", "no recognized terms in name or description; classified as random for coverage"


def need_hits_in_name(name: str,
                      need_indicators: set = NEED_INDICATORS,
                      generic_terms: set = GENERIC_TERMS) -> int:
    """Count need-indicator tokens in a package name with context disambiguation."""
    tokens = tokenize(name)
    count = 0
    for idx, token in enumerate(tokens):
        if token in need_indicators:
            if has_need_context(token, tokens, idx, need_indicators, generic_terms):
                count += 1
    return count


__all__ = [
    "split_camelcase",
    "tokenize",
    "has_need_context",
    "classify_package_name",
    "classify_description",
    "need_hits_in_name",
]
