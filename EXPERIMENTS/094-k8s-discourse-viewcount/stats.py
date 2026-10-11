<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->
#!/usr/bin/env python3
"""
Experiment 094: View-count principle on Kubernetes Discourse forum — Core logic.
Tests whether the view-count principle generalizes to Kubernetes error/failure topics.
"""

import math
import statistics
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional


@dataclass
class Topic:
    id: int
    title: str
    slug: str
    views: int
    reply_count: int
    posts_count: int
    has_accepted_answer: bool
    created_at: str
    last_posted_at: str
    tags: List[str]
    category_id: int
    excerpt: str = ""
    classification: str = "unclassified"
    unserved: bool = False


# Pre-declared classification keywords (written before first fetch)
ERROR_KEYWORDS = [
    "error", "failed", "fail", "crash", "exit code", "error code",
    "rpc error", "timeout", "deadline", "oom", "kill", "panic",
    "exception", "traceback", "stack trace", "500", "502", "503", "504",
    "404", "403", "connection refused", "connection reset", "dial tcp",
    "i/o timeout", "context deadline", "unknown desc", "malformed",
    "unexpected eof", "not ready", "not healthy", "crashloop", "backoff",
    "evicted", "pending", "imagepull", "errimagepull",
    "createcontainerconfigerror", "createcontainererror", "invalid",
    "denied", "forbidden", "unauthorized", "certificate", "tls", "x509"
]

NON_ERROR_KEYWORDS = [
    "how to", "best practice", "recommend", "suggest", "opinion",
    "discussion", "announcement", "release", "version", "upgrade",
    "migration", "strategy", "architecture", "design", "pattern",
    "tutorial", "guide", "tip", "trick", "experience", "story",
    "case study", "comparison", "vs ", "versus", "alternative",
    "tool", "monitoring", "observability", "logging", "metrics",
    "dashboard", "visualization", "cicd", "gitops", "argocd", "flux",
    "helm", "kustomize", "operator", "crd", "custom resource"
]

EXCLUDE_KEYWORDS = [
    "about the", "welcome to", "forum feedback", "bug bounty",
    "exam content", "cheatsheet", "hackerone"
]

MIN_VIEWS_FOR_ANALYSIS = 10


def classify_topic(topic: Topic) -> str:
    """Classify topic as 'error', 'non-error', or 'excluded' based on pre-declared rules."""
    text = (topic.title + " " + topic.excerpt).lower()

    for kw in EXCLUDE_KEYWORDS:
        if kw in text:
            return "excluded"

    for kw in ERROR_KEYWORDS:
        if kw in text:
            return "error"

    for kw in NON_ERROR_KEYWORDS:
        if kw in text:
            return "non-error"

    return "unclassified"


def is_unserved(topic: Topic) -> bool:
    """Determine if topic is unserved-open-like: no replies AND no accepted answer."""
    return topic.reply_count == 0 and not topic.has_accepted_answer


def mann_whitney_u(treatment: List[float], control: List[float]) -> Tuple[float, float]:
    """Mann-Whitney U test (two-sided). Returns (U statistic, p-value)."""
    n1 = len(treatment)
    n2 = len(control)

    if n1 == 0 or n2 == 0:
        return 0.0, 1.0

    combined = [(v, 0) for v in treatment] + [(v, 1) for v in control]
    combined.sort(key=lambda x: x[0])

    ranks = {}
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j

    r1 = sum(ranks[i] for i, (_, g) in enumerate(combined) if g == 0)
    u1 = r1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)

    mean_u = n1 * n2 / 2
    std_u = (n1 * n2 * (n1 + n2 + 1) / 12) ** 0.5

    if std_u == 0:
        return u, 1.0

    z = (u - mean_u) / std_u
    p = 2 * (1 - 0.5 * (1 + math_erf(abs(z) / 2**0.5)))
    return u, p


def math_erf(x: float) -> float:
    """Abramowitz and Stegun approximation of error function."""
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911

    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y


def wilson_ci_lower(k: int, n: int, z: float = 1.96) -> float:
    """Wilson score interval lower bound."""
    if n == 0:
        return 0.0
    p = k / n
    denominator = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    half_width = z * (p * (1 - p) / n + z**2 / (4 * n**2))**0.5
    return (centre - half_width) / denominator


def wilson_ci_upper(k: int, n: int, z: float = 1.96) -> float:
    """Wilson score interval upper bound."""
    if n == 0:
        return 0.0
    p = k / n
    denominator = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    half_width = z * (p * (1 - p) / n + z**2 / (4 * n**2))**0.5
    return (centre + half_width) / denominator