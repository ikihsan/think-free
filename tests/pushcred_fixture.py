# origin-allow-secret-patterns: github-app-private-key, github-token
"""Shared fixtures for the push-credential tests (T-0024).

Split out rather than imported from a test module: `test_pushcred.py` and
`test_pushcred_safety.py` both need a throwaway HOME, and one test file
importing another is a dependency the runner's discovery order should not decide.

The rule every fixture here obeys, and the reason it is written down twice in
the tests as well: **build paths inside the sandbox and never name a real one.**
`FAILURES.md` F014 is what happens when a fixture writes where the machine is —
here it destroyed this VM's git identity. A fixture that names a real path is
also a fixture whose result depends on whichever VM runs the suite, which is how
the recorded-defect test first passed for the wrong reason.
"""

from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from pathlib import Path

FAKE_TOKEN = "ghs_pretendthisisnotarealtoken0000000000000000"

# A git credential `get` exchange: consume the blank line, then answer. This is
# the shape `tools/x` never sees, because the real helper mints an App token.
ANSWER = (
    "#!/bin/sh\n"
    'while read -r line; do [ -z "$line" ] && break; done\n'
    "echo protocol=https\necho host=github.com\necho username=x-access-token\n"
    f"echo password={FAKE_TOKEN}\n"
)


def rmtree(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


class Sandbox:
    """A throwaway HOME, its own git config, and its own App directory."""

    def __init__(self, test: unittest.TestCase) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="origin-pushcred-"))
        test.addCleanup(rmtree, self.root)
        self.home = self.root / "home"
        self.home.mkdir()
        self.gitconfig = self.home / ".gitconfig"

    def helper(self, body: str, mode: int = 0o700) -> Path:
        script = self.home / "helper.sh"
        script.write_text(body, encoding="utf-8")
        script.chmod(mode)
        return script

    def app_key(self, mode: int = 0o600) -> Path:
        directory = self.home / ".config" / "github-app"
        directory.mkdir(parents=True, exist_ok=True)
        key = directory / "private-key.pem"
        key.write_text("-----BEGIN PRIVATE KEY-----\nx\n", encoding="utf-8")
        key.chmod(mode)
        return key

    def activate(self, test: unittest.TestCase, helper: Path | None = None) -> None:
        """Point HOME, XDG_CONFIG_HOME, and git at the sandbox, for this test."""
        body = f"[credential]\n\thelper = {helper}\n" if helper else ""
        self.gitconfig.write_text(body, encoding="utf-8")
        names = (
            "HOME", "XDG_CONFIG_HOME", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM",
            "GIT_TERMINAL_PROMPT", "GIT_ASKPASS",
        )
        saved = {name: os.environ.get(name) for name in names}
        os.environ.update(
            HOME=str(self.home),
            XDG_CONFIG_HOME=str(self.home / ".config"),
            GIT_CONFIG_GLOBAL=str(self.gitconfig),
            GIT_CONFIG_SYSTEM="/dev/null",
            GIT_TERMINAL_PROMPT="0",
        )

        def restore() -> None:
            for name, value in saved.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value

        test.addCleanup(restore)