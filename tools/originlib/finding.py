"""A violation that also knows where it is, and how to say so to GitHub.

Why this exists (T-0040, defect 12 in `STATE-defects.md`). The `Tests` step of
CI re-emits a failing test as a `::error` line, so a red run is diagnosable from
the public check-runs API without repository admin rights. The four other
file-reading gate steps emit nothing at all: a red `Documentation lint` names a
step and nothing more, and F019 cost an hour of elimination before that was
established. The run log, which does say, needs admin rights.

The location therefore has to travel with the violation, and it has to be the
**structured** location rather than a path parsed back out of the message. D025
is the shape of the mistake: `doc lint` reported a violation whose text begins
`docs/INDEX.md: …`, so a renderer could read the first token and be right most
of the time — and wrong silently on `identifier collision: …`, where the first
token is not a path at all. A `Finding` carries `path` and `line` because the
rule that found the violation is the only thing that knows them.

It subclasses `str` on purpose. Every gate here reports strings and every test
asserts on those strings, so the rendered report is unchanged by construction
and the existing assertions keep testing what they were written to test. A
separate parallel list of locations would have had to be kept in step with a
list of messages; parsing would have had to be right every time.

**Escaping** is the toolkit's, from `packages/core/src/command.ts` in
`actions/toolkit`: `%` -> `%25`, CR -> `%0D`, LF -> `%0A` in a message, and
additionally `:` -> `%3A` and `,` -> `%2C` in a property value
(`source-supported`, read 2026-10-04). The awk in the workflow's `Tests` step
doubles the percent instead, which renders one `%` as two; see defect 13.

**Ceiling.** These are the workflow's own emissions: the runner, not this
repository, decides how many it renders and where. The cap below is this
repository's choice, inherited from the awk window, and the platform's own limit
was not measured. Nothing here verifies a conclusion; it names a file to open.
"""

from __future__ import annotations

from pathlib import Path

# The number of annotations one gate emits. Inherited from the `awk` window in
# the `Tests` step rather than measured: GitHub's own limit is not stated on the
# workflow-commands page (read 2026-10-04), so a cap that is not the platform's
# is better than one that pretends to be.
CAP = 60

_DATA_ESCAPES = (("%", "%25"), ("\r", "%0D"), ("\n", "%0A"))
_PROPERTY_ESCAPES = _DATA_ESCAPES + ((":", "%3A"), (",", "%2C"))


class Finding(str):
    """One violation: the text every report already prints, plus where it is.

    `path` is empty when the rule does not know a single file to point at, and
    `line` is 0 when it does not know a line. Both are honest absences rather
    than defaults, which is why they are not filled in by parsing the text.
    """

    path: str
    line: int

    def __new__(cls, text: str, path: str = "", line: int = 0) -> "Finding":
        found = super().__new__(cls, text)
        found.path = path
        found.line = line
        return found

    # Both halves are needed: `str.__init__` rejects the extra positional
    # arguments once `__new__` has been overridden, so a three-argument call
    # raises TypeError without this. Found by running the renderer over a
    # planted conflict marker rather than by reading it (T-0040).
    def __init__(self, text: str, path: str = "", line: int = 0) -> None:
        super().__init__()
        self.path = path
        self.line = line

    @classmethod
    def at(cls, path: str, message: str, line: int = 0) -> "Finding":
        """A violation in a file, printed the way these gates have always printed it."""
        return cls(f"{path}: {message}", path, line)


def escape_data(text: str) -> str:
    for needle, replacement in _DATA_ESCAPES:
        text = text.replace(needle, replacement)
    return text


def escape_property(text: str) -> str:
    for needle, replacement in _PROPERTY_ESCAPES:
        text = text.replace(needle, replacement)
    return text


def location(finding: Finding, root: Path) -> tuple[str, int]:
    """The `file` and `line` properties to publish, and neither when untrue.

    Two guards, each a falsifiable claim rather than a convenience:

    * a `path` that is not a file in this tree gets no `file=`, so a rule that
      reports a directory, a glob, or a path it invented cannot point an
      annotation at something that does not exist. Several gates legitimately
      report a directory (`.claude/skills/<name>`) or a subject that spans two
      files (a defect number taken twice in two files).
    * a `line` past the end of the file gets no `line=`. A generated index
      shorter than the line the previous commit recorded would otherwise publish
      a position that cannot exist.
    """
    path = finding.path
    if not path:
        return "", 0
    target = root / path
    if not target.is_file():
        return "", 0
    if not finding.line:
        return path, 0
    total = len(target.read_text(encoding="utf-8", errors="replace").splitlines())
    return path, (finding.line if 0 < finding.line <= total else 0)


def command(finding: Finding, root: Path, level: str = "error", title: str = "") -> str:
    """One GitHub workflow command, in the order the documentation gives."""
    path, line = location(finding, root)
    properties = []
    if path:
        properties.append(f"file={escape_property(path)}")
    if line:
        properties.append(f"line={line}")
    if title:
        properties.append(f"title={escape_property(title)}")
    head = f"::{level}"
    if properties:
        head += " " + ",".join(properties)
    return f"{head}::{escape_data(str(finding))}"


def render(findings: list, root: Path, level: str = "error", cap: int = CAP) -> list[str]:
    """Workflow commands for these violations. Nothing at all when there are none.

    The empty case is the point, not a special case: a gate that always
    annotates is indistinguishable from a gate that found something, so a test
    asserts that a clean tree emits zero lines.
    """
    if not findings:
        return []
    lines = [command(item, root, level) for item in findings[:cap]]
    hidden = len(findings) - len(lines)
    if hidden > 0:
        lines.append(
            command(
                Finding(
                    f"{hidden} further violation(s) are not annotated: the cap is {cap}. "
                    "The run log names them, and reading it needs repository admin rights"
                ),
                root,
                "warning",
                title="annotation cap reached",
            )
        )
    return lines