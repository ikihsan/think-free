"""Secret detection for anything that gets written into the session record.

Two policies, because the risks differ:

* **Artifacts** (files about to be committed) are *refused* when a secret
  pattern matches. The file itself is the exposure; redacting it would leave a
  mangled artifact in git.
* **Command output** is *redacted* before it reaches disk, because the output
  is evidence and losing it is worse than masking a token. Every redaction is
  recorded as an event so a human can see that something sensitive appeared.

A detected secret is never echoed. Only the pattern name and the location are
reported.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

PLACEHOLDER = "REDACTED"

# (name, pattern). Ordered from most specific to most general so the reported
# name is the useful one.
PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("github-app-private-key", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{16,}")),
    ("github-fine-grained-pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}")),
    ("aws-access-key-id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("anthropic-key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    (
        "assigned-credential",
        re.compile(
            r"(?i)\b(?:api[_-]?key|secret|token|password|passwd|credential)"
            r"\s*[:=]\s*[\"']?[A-Za-z0-9/+_.-]{16,}[\"']?"
        ),
    ),
)

# Values that look like credentials but are not. Keeps obvious test fixtures
# from blocking every commit.
ALLOW_EXACT = frozenset(
    {
        "REDACTED",
        "your_token_here",
        "changeme",
        "example",
        "placeholder",
        "none",
        "null",
        "xxx",
    }
)


@dataclass(frozen=True)
class Finding:
    pattern: str
    start: int
    end: int
    priority: int = 0


def scan(text: str) -> list[Finding]:
    """Return every secret-pattern match in text, without exposing values.

    Overlapping matches collapse to the pattern declared earliest in
    `PATTERNS`, because that list is ordered most-specific first. Without this,
    `TOKEN=ghp_...` would be reported twice: once usefully as a GitHub token and
    once unhelpfully as a generic assigned credential.
    """
    raw: list[Finding] = []
    for priority, (name, pattern) in enumerate(PATTERNS):
        for match in pattern.finditer(text):
            if match.group(0).strip().lower() in ALLOW_EXACT:
                continue
            raw.append(Finding(name, match.start(), match.end(), priority))
    raw.sort(key=lambda f: (f.priority, f.start))
    kept: list[Finding] = []
    for finding in raw:
        overlaps = any(
            finding.start < other.end and other.start < finding.end for other in kept
        )
        if not overlaps:
            kept.append(finding)
    kept.sort(key=lambda f: (f.start, f.pattern))
    return kept


def names(findings: list[Finding]) -> list[str]:
    """Sorted unique pattern names. Safe to log."""
    return sorted({f.pattern for f in findings})


def redact(text: str) -> tuple[str, list[str]]:
    """Replace every match with a placeholder. Returns text and pattern names."""
    findings = scan(text)
    if not findings:
        return text, []
    pieces: list[str] = []
    cursor = 0
    for finding in findings:
        pieces.append(text[cursor : finding.start])
        pieces.append(f"<{PLACEHOLDER}:{finding.pattern}>")
        cursor = finding.end
    pieces.append(text[cursor:])
    return "".join(pieces), names(findings)


def scan_file(path) -> list[str]:
    """Read a file as text and return any pattern names found.

    Undecodable files are skipped rather than guessed at; a binary artifact
    cannot be committed with a plaintext credential by accident in a way this
    scan would catch anyway.
    """
    try:
        data = path.read_bytes()
    except OSError:
        return []
    if b"\x00" in data[:8192]:
        return []
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = data.decode("latin-1")
        except UnicodeDecodeError:
            return []
    return names(scan(text))