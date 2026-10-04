#!/usr/bin/env python3
"""Falsify T-0052's rule by mutating it, on real bytes.

D025 asks a gate to be falsified against the defect it was written for, and two
sessions in this repository have recorded the failure mode of skipping it: a
mutation whose `str.replace` pattern did not match the file's real indentation
changed nothing and fourteen green tests read as "the clause is not
load-bearing". So the pattern is counted before anything is written and a count
other than one is refused rather than run.

Two mutations, one per direction, and the second is the one that is easy to get
wrong. Removing the rule reports nothing on `eff1126`. Removing only the
generated-document exemption makes the rule *right about the wrong thing*: it
then reports 47 findings on a clean tree, every one of them a session report
listing an artifact twice, which is what those reports are for.

    python3 tools/mutate_table_rule.py apply no-rule           # must fail
    python3 tools/mutate_table_rule.py restore
    python3 tools/mutate_table_rule.py apply no-generated-exempt # must fail
    python3 tools/mutate_table_rule.py restore
"""

from __future__ import annotations

import sys
from pathlib import Path

TARGET = Path(__file__).resolve().parent.parent / "tools" / "originlib" / "doclint_table.py"

WITH_RULE = """    from .doclint import FENCE, GENERATED_MARK

    base = paths.repo_root()
    for path in files:
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if GENERATED_MARK in text[:2048]:
            continue
        rel = path.relative_to(base).as_posix()
"""

WITHOUT_RULE = """    from .doclint import FENCE, GENERATED_MARK

    base = paths.repo_root()
    for path in files:
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(base).as_posix()
"""

WITHOUT_EXEMPT = """        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(base).as_posix()
"""

MUTATIONS = {
    "no-rule": (WITH_RULE, WITHOUT_RULE),
    "no-generated-exempt": (WITH_RULE, WITHOUT_EXEMPT),
}


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("apply", "restore"):
        print(__doc__)
        return 1
    if argv[0] == "restore":
        for old, new in reversed(list(MUTATIONS.values())):
            text = TARGET.read_text(encoding="utf-8")
            if new in text and old not in text:
                TARGET.write_text(text.replace(new, old), encoding="utf-8")
                print("restored: doclint_table.py")
                return 0
        print("nothing to restore")
        return 0
    name = argv[1] if len(argv) > 1 else ""
    if name not in MUTATIONS:
        print(f"apply needs a mutation name; one of: {', '.join(sorted(MUTATIONS))}")
        return 1
    old, new = MUTATIONS[name]
    text = TARGET.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        print(
            f"refusing to apply {name}: the pattern matched {count} times, so the run "
            "would prove nothing about the rule. Read doclint_table.py and fix the pattern."
        )
        return 2
    TARGET.write_text(text.replace(old, new), encoding="utf-8")
    print(f"applied: {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
