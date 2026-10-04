"""`origin probe` — publish how GitHub renders the annotator's own output.

Why this exists (T-0046). `docs/operations/ci-diagnosis.md` carried the claim
that whether GitHub files a check-run annotation on a workflow command's `file=`
property was `unmeasured`, and beside it a run whose annotation had `path=.github`.
Both were wrong, and both were read off the public check-runs API
(`EXPERIMENTS/010-annotation-rendering/`, `FAILURES.md` F021). What actually
happened is the general failure of D025: a reader saw the field it happened to
look at and drew a conclusion about the property.

The mechanism is now measured on the run that reports the failure. One annotation
per rendering shape, each with `title=annotation-probe/<shape>` so a reader can
match them, so the reference and the failure come from the same place rather than
from whatever run happened to be red when somebody went looking. That is the
difference between a diagnostic that can be compared and one that cannot.

**It never fails, and it never emits `::error`.** A measurement that can redden
CI on a clean tree is a measurement that gets deleted after its first false
alarm. The two levels it does emit are the ones a green run already publishes
(`::notice` for the runner's own notices, `::warning` for the session step's
in-flight note), so the probe adds nothing that can fail a job. `::error` with a
`file=` is the shape the gates emit and it is already observed, on run
`37191658964` — which is the one thing a green run could not have told us.

**Ceiling.** Nothing here measures GitHub's annotation cap, a path outside the
checkout, or a `file=` value containing `:` or `,` — this repository has no file
whose name contains either, so the property escaping has no real input on this
tree and a synthetic one would measure a path that cannot exist. `line=` is
emitted here for the first time by shape 1, and arm A's `start_line: 0` is the
only observation of a `file=` with no `line=`.
"""

from __future__ import annotations

from pathlib import Path

from . import paths
from .finding import Finding, render

EXIT_OK = 0

# One entry per shape, and the title a reader matches it by. The titles are the
# contract: `tests/test_probe.py` asserts that every shape named here is emitted
# with the file, line, level and message this table says, so a shape cannot be
# dropped from the table, the code or the document without one of the three
# disagreeing with the other two.
#
# `path` and `line` are real files in this repository with real line counts,
# because `finding.location` drops a `file=` that is not a file and a `line=`
# past the end of one — the probe would then measure the drop rather than the
# rendering.
SHAPES: tuple[tuple[str, str, int, str, str], ...] = (
    (
        "filed-with-line",
        "STATE.md",
        7,
        "notice",
        "a file and a line, so the annotation's own start_line can be read back",
    ),
    (
        "filed-no-line",
        "MISSION.md",
        0,
        "notice",
        "a file and no line: run 37191658964 observed start_line 0 for this shape",
    ),
    (
        "message-percent",
        "ROADMAP.md",
        1,
        "notice",
        "50% of this sentence is a percent sign, which must arrive escaped and must "
        "not become a second command",
    ),
    (
        "message-colon-comma",
        "HYPOTHESES.md",
        1,
        "notice",
        "keys: a, b; c — a colon and a comma are data, and are not escaped in a message",
    ),
    (
        "message-newline",
        "FAILURES.md",
        1,
        "notice",
        "two\nlines, which must arrive as one annotation and not as two commands",
    ),
    (
        "warning-level",
        "README.md",
        1,
        "warning",
        "a level other than error, which is what the session step's in-flight note emits",
    ),
    (
        "no-file",
        "",
        0,
        "notice",
        "no file at all, which is how a fileless command reads: path .github",
    ),
)


def commands(root: Path) -> list[str]:
    """One workflow command per shape, in the table's order."""
    findings = []
    for name, path, line, level, message in SHAPES:
        findings.append(
            (level, Finding(f"annotation-probe/{name}: {message}", path, line))
        )
    out: list[str] = []
    for level, finding in findings:
        out.extend(render([finding], root, level=level))
    return out


def dispatch(args) -> int:
    """Print the probe's commands. Always exit 0: nothing here is a gate."""
    for line in commands(paths.repo_root()):
        print(line)
    return EXIT_OK