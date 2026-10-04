#!/usr/bin/env python3
"""Which numbers a mission record states about an experiment are not its own?

Task T-0056's measurement, and the reason it is a script rather than a sentence:
the repair makes a restated result number checkable against the artifact it
claims to come from, and the number of such numbers that would be reported is
not something to guess at. It reads the tree and writes nothing into it.

    python3 tools/sweep_result_numbers.py [--root REPO] [--verbose]

Every experiment under `EXPERIMENTS/` that has a `results.json` is a candidate,
and every tracked Markdown file is a candidate claim. A claim is *attributable*
when one line names exactly one experiment — that is a bounded, decidable unit,
because a line naming two experiments says nothing about which one a number
belongs to. Numbers inside a line naming one experiment are then held to that
artifact's **headline** values: the top-level scalars, plus the length of its
`cases` list.

The headline restriction is the whole point, and it was measured rather than
assumed. The looser question — *does this number occur anywhere in the
artifact* — **passes** the defect that motivated this task: `113` is stated for
`005-knitting-bounded-search`, whose `cases_with_oracle` is `115`, and `113`
nevertheless occurs at `patch_cost_sensitivity/*/cases`. A rule reading "any
value in the file" concludes about a different property than the one being
claimed, which is D025's shape: the reader sees the field it happened to look
at. Only the headline values answer "how many cases did this experiment check".

`--verbose` additionally reports, for each reported number, whether the looser
rule would also have reported it — the falsification of the restriction, on the
real tree.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from originlib import paths  # noqa: E402

# One line that names exactly one experiment. `005-knitting-bounded-search` and
# the bare `005` are both forms that appear; the three-digit form alone is
# ambiguous with a task number in prose, so only the full slug counts.
SLUG = re.compile(r"\b(\d{3}-[a-z0-9-]+)\b")
# A number, not part of a dotted version (`2.25`), a date, or a path segment.
NUMBER = re.compile(r"(?<![\w.\-/])(\d+(?:\.\d+)?)(?![\w.\-])")
# A table row is the structural claim shape here, but a prose line naming one
# experiment states the same thing, so both are read; the row shape is only used
# to keep the attribution to a single cell where one is present.
ROW = re.compile(r"^\|(.+)\|\s*$")
GENERATED = "<!-- generated-by:"

EXPERIMENTS = "EXPERIMENTS"


def result_file(root: pathlib.Path, slug: str) -> pathlib.Path | None:
    candidate = root / EXPERIMENTS / slug / "results.json"
    return candidate if candidate.is_file() else None


def headline(data) -> set:
    """The values a restated headline number may legitimately name.

    Top-level scalars, the numbers inside a top-level string, and the length of a
    top-level ``cases`` list. Deliberately shallow: a nested value answers a
    question about a sub-case of the experiment, so a prose claim naming it
    would have to say which one, and no line here does.
    """
    values: set = set()
    for value in data.values():
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            values.add(value)
        elif isinstance(value, str):
            for match in NUMBER.finditer(value):
                values.add(float(match.group(1)))
    cases = data.get("cases")
    if isinstance(cases, list):
        values.add(len(cases))
    return values


def anywhere(data) -> set:
    """Every number the artifact mentions at all — the rule this one rejects."""
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
            for match in NUMBER.finditer(node):
                values.add(float(match.group(1)))

    walk(data)
    return values


def matches(number: str, values: set) -> bool:
    if number in {str(value) for value in values}:
        return True
    try:
        number_value = float(number)
    except ValueError:
        return False
    return number_value in values or int(number_value) in values


def markdown_files(root: pathlib.Path) -> list[pathlib.Path]:
    """Tracked Markdown, generated documents excluded.

    A generated index renders its own summary line from another file, so a
    number in one is a copy rather than a claim about the artifact. Excluded by
    the marker in the document rather than by a path, for the reason T-0052's
    generated-document exemption gives.

    Nesting is decided by the path *relative to this root*, never by looking for
    a directory name in the absolute parts: a worktree lives at
    `.worktrees/<task>-<vm>/`, so every path inside it has `.worktrees` in its
    parts and the name test would discard the whole repository. That is defect
    19's shape — a verdict that depends on where the checkout sits rather than on
    what the repository holds — and it was caught by the script reporting **zero**
    documents, which is a count a reader should never have to accept.
    """
    found = []
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if ".git" in relative.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if GENERATED in text:
            continue
        found.append(path)
    return found


def sweep(root: pathlib.Path, loose: bool = False) -> dict:
    """One report per number a mission record states that its artifact disowns."""
    cache: dict[str, tuple[set, set]] = {}
    reports = []
    lines_read = 0
    attributable = 0
    documents_read = 0
    for path in markdown_files(root):
        documents_read += 1
        rel = path.relative_to(root).as_posix()
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            lines_read += 1
            slugs = set(SLUG.findall(line))
            if len(slugs) != 1:
                continue
            slug = slugs.pop()
            if result_file(root, slug) is None:
                continue
            attributable += 1
            if slug not in cache:
                data = json.loads(result_file(root, slug).read_text(encoding="utf-8"))
                cache[slug] = (headline(data), anywhere(data))
            strict, loose_values = cache[slug]
            # In a table row the claim is the row; reading the whole line is what
            # admits a number from a neighbouring cell about a different thing.
            row = ROW.match(line)
            scope = row.group(1) if row else line
            for candidate in NUMBER.findall(scope):
                values = loose_values if loose else strict
                if not matches(candidate, values):
                    reports.append(
                        {
                            "path": rel,
                            "line": number,
                            "slug": slug,
                            "value": candidate,
                            "loose_also_reports": not matches(candidate, loose_values),
                        }
                    )
    return {
        "reports": reports,
        "lines_read": lines_read,
        "attributable_lines": attributable,
        "documents": documents_read,
        "experiments": len(cache),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=None, help="repository to read (default: this one)")
    parser.add_argument(
        "--loose",
        action="store_true",
        help="use the rejected rule: any number occurring anywhere in the artifact",
    )
    parser.add_argument("--verbose", action="store_true", help="name the loose rule's verdict too")
    args = parser.parse_args()
    root = pathlib.Path(args.root).resolve() if args.root else paths.repo_root()
    result = sweep(root, loose=args.loose)
    rule = "any value in the artifact" if args.loose else "headline values only"
    print(f"rule: {rule}")
    print(
        f"{result['documents']} document(s), {result['lines_read']} line(s) read; "
        f"{result['attributable_lines']} name exactly one experiment with an artifact; "
        f"{result['experiments']} artifact(s) consulted"
    )
    print(f"\n=== numbers stated about an experiment that its artifact disowns: {len(result['reports'])}")
    for item in result["reports"]:
        extra = ""
        if args.verbose:
            extra = "  [loose rule also reports this]" if item["loose_also_reports"] else "  [loose rule MISSES this]"
        print(f"{item['path']}:{item['line']}  [{item['slug']}]  {item['value']}{extra}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())