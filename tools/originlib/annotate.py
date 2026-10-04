"""`origin annotate` — run a gate, and say what it rejected in GitHub's words.

Why this exists (T-0040, defect 12 in `STATE-defects.md`). CI's `Tests` step
re-emits each failing test as a `::error` line, so a red run is diagnosable
from the public check-runs API with no repository admin rights. The five
file-reading gate steps emitted nothing at all: a red `Documentation lint` named
a step and nothing more, and F019 spent an hour of elimination finding out why
(`FAILURES.md` F020). The run log does say which rule failed — reading it needs
admin rights.

So the gate stays the gate and this wrapper publishes its answer. Three things
are deliberate:

* **It runs the gate in process and reads its violations**, rather than
  scraping the `  FAIL  ` lines out of the report another layer formatted for a
  person. Reading back a formatted field is the shape of mistake D025 records:
  a reader sees the field it happened to look at and concludes about the
  property.
* **It keeps each gate's own exit code.** `skills verify` is an integrity
  failure (4), `doc lint` a lint violation (2), and CI and VM scripts branch on
  the difference. A wrapper that normalised the code would change what every
  caller does.
* **It refuses a gate or a flag it cannot read**, with exit 1, rather than
  running something else. A command that reports a gate nobody asked for is a
  green run of a gate that cannot fail (F010).

**Ceiling.** Annotations are the workflow's own emission: the runner decides how
many it renders and where it puts them, and nothing here verifies a conclusion.
It names a file to open. `origin annotate` on a clean tree prints the gate's own
report and emits no `::` line at all, which is the half of the behaviour a test
has to hold.
"""

from __future__ import annotations

from . import doclint, paths, release, skillsync
from .finding import render
from .usage import Usage

EXIT_LINT = 2
EXIT_INTEGRITY = 4


class Gate:
    """One gate, how to run it, and which flags it accepts."""

    def __init__(self, run, problems: str, failure: int, flags: tuple[str, ...] = ()) -> None:
        self.run = run
        self.problems = problems
        self.failure = failure
        self.flags = flags

    def check_flags(self, words: list[str]) -> None:
        """Refuse a flag this gate does not read.

        Passing an unknown flag through would mean silently not applying it,
        which is the same failure as a rule that quietly stops matching.
        """
        allowed = set(self.flags) | {"--help"}
        for word in words:
            if word.split("=", 1)[0] not in allowed:
                raise Usage(
                    f"annotate: this gate reads {', '.join(self.flags) or 'no flags'}, "
                    f"not {word!r}"
                )

    def report(self, words: list[str]):
        """The gate's own rendered report, its violations, and its exit code."""
        result = self.run()
        return result.render(), list(getattr(result, self.problems)), self.failure


class SessionGate(Gate):
    """`session verify`, which prints rather than returning a result.

    `cli_session.session_report` exists because of this class: it returns the
    rendered report and the violations together, so nothing has to be recovered
    from captured output.
    """

    def __init__(self) -> None:
        super().__init__(lambda: None, "violations", EXIT_INTEGRITY, ("--strict", "--lease-hours"))

    def report(self, words: list[str]):
        from .cli_session import session_report

        strict = "--strict" in words
        hours = None
        if "--lease-hours" in words:
            index = words.index("--lease-hours")
            try:
                hours = float(words[index + 1])
            except (IndexError, ValueError):
                raise Usage("annotate: --lease-hours needs a number of hours after it")
        text, violations = session_report(strict=strict, lease_hours=hours)
        return text, list(violations), self.failure


GATES: dict[str, Gate] = {
    "doc lint": Gate(doclint.lint, "violations", EXIT_LINT),
    "release check": Gate(release.check, "violations", EXIT_LINT),
    "skills check": Gate(skillsync.check, "problems", EXIT_LINT),
    "skills verify": Gate(skillsync.verify_vendor, "problems", EXIT_INTEGRITY),
    "session verify": SessionGate(),
}

NAMES = tuple(GATES)


def resolve(argv: list[str]) -> tuple[str, list[str]]:
    """The gate named in `argv`, and the flags left for it.

    Two shapes are read, because both appear in real use: `annotate -- doc lint`
    with the gate as two words, and `annotate -- "doc lint"` with it quoted —
    which is what a shell loop over the names writes. `--` is accepted and
    dropped, because a caller writing `annotate -- doc lint --quiet` means the
    flag for the gate rather than for this command.
    """
    words = list(argv)
    if words and words[0] == "--":
        words.pop(0)
    # Longest join first, so `release check` is never read as a gate named
    # `release` and `skills verify` not as `skills`.
    for size in (3, 2, 1):
        if len(words) < size:
            continue
        name = " ".join(words[:size])
        if name in GATES:
            return name, words[size:]
    raise Usage(
        "annotate: name a gate to run. One of: "
        + ", ".join(f"'{name}'" for name in NAMES)
    )


def dispatch(argv: list[str]) -> int:
    """Print the gate's report, then its violations as check-run annotations."""
    name, words = resolve(argv)
    gate = GATES[name]
    gate.check_flags(words)
    text, violations, failure = gate.report(words)
    print(text)
    for line in render(violations, paths.repo_root()):
        print(line)
    return failure if violations else 0