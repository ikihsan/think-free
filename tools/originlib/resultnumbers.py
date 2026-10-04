"""A mission record's restated experiment number, held to the artifact it names.

Why this exists (T-0056, defect 22 in `STATE-defects.md`).
`docs/process/experiment-protocol.md` stated that
`005-knitting-bounded-search` "reproduces the oracle on **113/113** checked
cases". That artifact's `results.json` says `cases_with_oracle = 115` and
`cases_tested = 118`, and the experiment's own README says 115/115. The wrong
number was in the same commit that published the artifact — `318374a` — so no
later edit introduced it, and every gate passed: nothing read a number in a
mission record against the machine-readable result it restates.

**The obvious rule for this does not work, and that is the reason this module is
not one line.** The question "does this number occur anywhere in the artifact?"
answers **yes** for `113`: the value also sits at
`patch_cost_sensitivity/*/cases`, a per-patch-cost count that has nothing to do
with how many cases the headline result is about. A rule reading "any value in
the file" concludes about a different property than the one being claimed —
D025's shape, the reader seeing the field it happened to look at. Measured on
the defect's own bytes: the loose rule reports **nothing**.

So the property is decided by what the number *is*, and two shapes are read
separately because they mean different things:

* **A fraction `N/M`** is a claim about a countable population, so `M` must be a
  count the artifact declares — an integer field whose name says how many cases,
  fixtures or instances, or the length of its `cases` list. This is the shape the
  defect is, and it is decidable without guessing which nested value is the
  "headline".
* **A decimal with a fractional part** is distinctive enough to be checked
  against any value the artifact states, so it is. `0.965` and `0.833` are
  matched; a coincidence at two significant figures is not a realistic way for
  a record to become false unnoticed, and a rule that refused every decimal
  because it *could* coincide would be a rule nobody could satisfy.

**Scope: one table row naming exactly one experiment.** A results index states
one experiment's outcome per row, which makes the attribution decidable. Two
deliberate exclusions, both because a record that *discusses* a number is not
restating it: a line naming two experiments says nothing about which one a
number belongs to, and prose paragraphs are not read. This module therefore
reports nothing on `STATE.md`'s dashboard row, which names all nine experiments
at once — a stated ceiling, not an oversight.

**A gate whose input it cannot read has to say so** (D025). An experiment with a
`results.json` this module cannot parse, and a document it cannot decode, are
both reported rather than skipped.

**Ceiling.** It reads one row per experiment in one index. A count restated in a
prose paragraph, a bare integer that is not a denominator, and a number quoted
from a run whose artifact was not committed (the `116/116` figure from 005's
`--slow` run is such a number, and this rule would report it) are all unexamined.
Two shapes are reported that a reader may think should not be: a **version**
written inside a results row, because `2.30` and `0.30` are the same shape and no
rule can tell a tool version from a measurement — the remedy is to keep
environment facts out of the results table, which is where the ceiling is aimed;
and the `116/116` figure above, because the artifact that would justify it is not
in this tree. Both are the honest direction: a claim nothing here can check is
reported rather than assumed true.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .finding import Finding

EXPERIMENTS = "EXPERIMENTS"
RESULT_FILE = "results.json"
# `005-knitting-bounded-search`. The bare `005` form is deliberately not matched:
# in prose it is indistinguishable from a task number, and an attribution that
# cannot be made must not be guessed.
SLUG = re.compile(r"\b(\d{3}-[a-z0-9-]+)\b")
# A decimal that is not part of a longer dotted token. The trailing guard is
# `(?!\.\d)` rather than `(?![\w.\-])`: prose ends a sentence with a period, and a
# guard that rejects any following dot also rejects every number that ends one —
# found by a test, because the first version silently read "met at 0.965." as no
# number at all. The leading `(?<!\d\.)` stops `3.8.10` from being read as `8.10`.
DECIMAL = re.compile(r"(?<![\w-])(?<!\d\.)(\d+\.\d+)(?![\w-]|\.\d)")
FRACTION = re.compile(r"(?<![\w.\-/])(\d+)\s*/\s*(\d+)(?![\w])")
# A field whose *name* says how many cases, fixtures or instances the run
# covered. Read from the name because the property is about what the number
# counts, and a key that means "how many" in another word is a stated ceiling.
COUNT_KEY = re.compile(r"case|fixture|instance", re.IGNORECASE)
GENERATED_MARK = "<!-- generated-by:"


def result_file(root: Path, slug: str) -> Path:
    return root / EXPERIMENTS / slug / RESULT_FILE


def declared_counts(data) -> set:
    """The counts an artifact declares about how many things it examined.

    An integer field whose name counts cases, fixtures or instances, plus the
    length of the artifact's own `cases` list. Deliberately shallow: a nested
    value answers a question about one family, one patch cost or one sweep
    setting, which is exactly the coincidence that lets `113` pass a rule
    reading the whole file.
    """
    counts: set = set()
    for key, value in data.items():
        if COUNT_KEY.search(key) and isinstance(value, int) and not isinstance(value, bool):
            counts.add(value)
    cases = data.get("cases")
    if isinstance(cases, list):
        counts.add(len(cases))
    return counts


def every_value(data) -> set:
    """Every number the artifact states anywhere, for a distinctive decimal."""

    values: set = set()

    def walk(node):
        if isinstance(node, dict):
            for item in node.values():
                walk(item)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, bool):
            return
        elif isinstance(node, (int, float)):
            values.add(node)
        elif isinstance(node, str):
            for match in DECIMAL.finditer(node):
                values.add(float(match.group(1)))

    walk(data)
    return values


def stated(value: str, values: set) -> bool:
    """Whether `value` is one of `values`, comparing as the artifact would print it."""
    if value in {str(item) for item in values}:
        return True
    try:
        number = float(value)
    except ValueError:
        return False
    return number in values or int(number) in values


def unreadable_issue(slug: str, detail: str) -> Finding:
    return Finding(
        f"{EXPERIMENTS}/{slug}/{RESULT_FILE}: this experiment's result cannot be read "
        f"({detail}), so a number a mission record states about it would go unreported. "
        f"Fix the artifact rather than deleting the rule (D025)",
        f"{EXPERIMENTS}/{slug}/{RESULT_FILE}",
    )


def row_issues(row: str, slug: str, counts: set, values: set) -> list[Finding]:
    """The numbers one row states that its artifact does not."""
    issues = []
    for numerator, denominator in FRACTION.findall(row):
        if not stated(denominator, counts):
            issues.append(
                f"{numerator}/{denominator}: {denominator} is not a count this experiment "
                f"declares (it declares {sorted(counts)}), so the row does not restate "
                f"this experiment's result"
            )
    for value in DECIMAL.findall(row):
        if not stated(value, values):
            issues.append(f"{value}: no such value appears in this experiment's result")
    return issues


def issues(root: Path, files: list[Path]) -> list[Finding]:
    """Every restated experiment number this tree does not own.

    `files` is the tracked file list `doc lint` already holds, so the module
    reads the same documents every other rule does rather than walking the disk
    for a second, different set.
    """
    found: list[Finding] = []
    cache: dict[str, tuple[set, set] | str] = {}
    for path in files:
        if path.suffix != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if GENERATED_MARK in text:
            # A generated index renders a summary line from another file, so a
            # number in one is a copy rather than a claim about the artifact.
            continue
        rel = path.relative_to(root).as_posix()
        for number, line in enumerate(text.splitlines(), start=1):
            if not line.startswith("|"):
                continue
            slugs = set(SLUG.findall(line))
            if len(slugs) != 1:
                continue
            slug = slugs.pop()
            if slug not in cache:
                artifact = result_file(root, slug)
                if not artifact.is_file():
                    cache[slug] = ""
                else:
                    try:
                        data = json.loads(artifact.read_text(encoding="utf-8"))
                    except (OSError, ValueError) as error:
                        cache[slug] = f"{type(error).__name__}: {error}"
                    else:
                        cache[slug] = (declared_counts(data), every_value(data))
            held = cache[slug]
            if held == "":
                continue
            if isinstance(held, str):
                found.append(unreadable_issue(slug, held))
                continue
            for message in row_issues(line, slug, held[0], held[1]):
                found.append(
                    Finding.at(rel, f"result restated from {slug}: {message}", number)
                )
    return found


def report(root: Path, files: list[Path]) -> list[Finding]:
    return issues(root, files)