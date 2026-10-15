#!/usr/bin/env python3
"""
E146 — Classifier for Reddit title need-relatedness.

Adapts the E116 whole-word matching + contextual disambiguation framework
for Reddit post titles rather than package names/descriptions.
"""

import re
import json

# Vocabulary from E116/vocab.py — terms suggesting a programming need.
NEED_INDICATORS = {
    "web", "rest", "api", "http", "client", "server", "framework",
    "database", "orm", "sql", "postgres", "mysql", "mariadb", "redis",
    "mongo", "mongodb", "elasticsearch", "couchdb", "storage", "cache",
    "persistent", "state",
    "auth", "oauth", "oidc", "jwt", "session", "cookie", "security",
    "encrypt", "decrypt", "sign", "verify", "validator", "schema",
    "socket", "tcp", "udp", "grpc", "websocket",
    "pubsub", "messaging", "queue", "topic", "broker", "channel",
    "test", "mock", "fixture", "benchmark", "profile", "fuzz",
    "continuous", "integration", "deployment",
    "cli", "command", "argument", "flag", "option",
    "migration", "schema", "seed", "factory",
    "ecto", "phoenix", "plug", "absinthe", "tesla", "finch",
    "httpoison", "jason", "poison",
    "socket", "tcp", "udp",
    "web", "rest", "api",
    "database", "orm", "sql",
    "auth", "security",
    "test", "mock",
    "cli", "command",
}

# Truly generic terms: disqualifying when present (with disambiguation).
GENERIC_TERMS = {
    "base", "minimal", "alpine", "scratch", "distroless", "slim",
    "latest", "stable", "edge", "main", "master", "dev", "test",
    "example", "demo", "sample", "template", "boilerplate",
    "sandbox", "playground", "poc", "prototype", "experiment",
    "tutorial", "learning", "workshop",
    "personal", "private", "internal", "custom",
    "fork", "mirror", "copy", "backup", "archive", "old",
    "deprecated", "legacy", "unmaintained", "abandoned",
    "utils", "common", "core", "library", "package", "tool", "util",
    "helper",
    "ci", "build", "builder", "compile", "runtime", "debug",
    "example", "demo", "tutorial",
}

DISAMBIG_WINDOW = 3


def tokenize(text):
    """Tokenize text into lowercase words, preserving hyphens within words."""
    if not text:
        return []
    tokens = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())
    return tokens


def has_need_context(tokens, idx, need_set, generic_set, window=DISAMBIG_WINDOW):
    """Check if NEED_INDICATORS[idx] carries need-specific context."""
    token = tokens[idx]
    if token not in need_set:
        return False
    if token not in generic_set:
        return True
    # Token is in both NEED_INDICATORS and GENERIC_TERMS — need context
    start = max(0, idx - window)
    end = min(len(tokens), idx + window + 1)
    for j in range(start, end):
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


def classify_title(title):
    """Classify a title/description as need-related, random, or uncertain.

    Adapted from E116 classify_description for GitHub repo titles/descriptions.
    Returns (classification, reason, weight).
    weight >= 0.5 = classified; 0.0 = uncertain.
    """
    if not title:
        return "uncertain", "no title", 0.0

    tokens = tokenize(title)
    if not tokens:
        return "uncertain", "no tokens after parsing", 0.0

    need_matches = 0
    generic_matches = 0
    need_indices = []
    generic_indices = []

    for i, tok in enumerate(tokens):
        if tok in NEED_INDICATORS:
            if has_need_context(tokens, i, NEED_INDICATORS, GENERIC_TERMS, DISAMBIG_WINDOW):
                need_matches += 1
                need_indices.append(i)
            else:
                need_matches += 0.5
                need_indices.append(i)
        if tok in GENERIC_TERMS:
            generic_matches += 1
            generic_indices.append(i)

    effective_need = sum(
        1.0 for i in need_indices
        if has_need_context(tokens, i, NEED_INDICATORS, GENERIC_TERMS, DISAMBIG_WINDOW)
    )

    # Fallback: check title for question/problem/request/technical patterns
    # when the vocabulary classifier produces no matches.
    title_lower = title.lower()

    question_patterns = [
        "how do", "how can", "how to", "why does", "what is",
        "how does", "how is", "how would", "how will", "how could",
        "can you", "could you", "would you", "can anyone",
        "could anyone", "would anyone", "does anyone", "do you",
        "is there", "are there",
    ]
    problem_patterns = [
        "fix", "debug", "error", "issue", "problem", "bug",
        "crash", "fail", "exception", "not working", "cannot",
        "stuck", "help",
    ]
    request_patterns = [
        "help me", "please help", "need help", "advice",
        "suggest", "recommend", "guidance",
    ]
    technical_patterns = [
        "lint", "format", "refactor", "test", "deploy",
        "ci", "cd", "git", "docker", "kubernetes",
        "api", "database", "sql", "nosql",
    ]

    has_question = any(p in title_lower for p in question_patterns)
    has_problem = any(p in title_lower for p in problem_patterns)
    has_request = any(p in title_lower for p in request_patterns)
    has_technical = any(p in title_lower for p in technical_patterns)

    # Classification logic
    if effective_need > 0 and generic_matches > 0:
        if effective_need > generic_matches:
            return "need-related", f"{int(effective_need)} need-specific token(s) outweigh {generic_matches} generic tokens", 1.0
        else:
            return "random", f"{int(effective_need)} need token(s) but {generic_matches} generic dominates", 0.7

    if effective_need == 0 and generic_matches > 0:
        return "random", f"{int(generic_matches)} generic token(s), no need-specific signals", 0.0

    if effective_need == 0 and generic_matches == 0:
        # Fallback: did the title match question/problem/request/technical patterns?
        if has_question or has_problem or has_request or has_technical:
            return "need-related", f"title matches question/problem/request/technical patterns", 0.8
        return "uncertain", "no recognized need or generic tokens", 0.0

    # effective_need > 0 and no generics
    if effective_need > 0 and generic_matches == 0:
        return "need-related", f"{int(effective_need)} need-specific token(s) found", 1.0

    # Fallback
    return "random", "classified as random", 0.7