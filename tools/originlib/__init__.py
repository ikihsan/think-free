"""originlib: session logging, task dispatch, documentation lint, and skill checks.

Standard library only, so the tooling runs on any machine with Python 3.11+
and needs no installation step on a fresh VM.
"""

__all__ = [
    "cli",
    "docindex",
    "doclint",
    "doctor",
    "events",
    "gitutil",
    "paths",
    "pushcred",
    "pushprobe",
    "report",
    "secrets",
    "session",
    "skillsync",
    "tasks",
]

__version__ = "0.1.0"