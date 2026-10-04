#!/usr/bin/env python3
"""Falsify T-0051's rule by mutating it, on real bytes.

D025 asks a gate to be falsified against the defect it was written for, and
T-0047's session recorded the failure mode of doing it carelessly: a mutation
whose `str.replace` pattern did not match the file's real indentation changed
nothing, every test stayed green, and the run read as "the clause is not
load-bearing". So the pattern here is counted before anything is written, and a
count other than one is refused rather than run.

One mutation falsifies both directions at once, because it *is* the previous
rule: dropping the containment filter leaves `check_links` deciding every link by
`exists()` on whatever path it resolves to.

  * the escape is unreported, so the three tests that require it fail; and
  * the same bytes are judged differently in two checkout locations again, so
    the parent-independence test fails too.

    python3 tools/mutate_link_rule.py apply
    PYTHONPATH=tools:tests python3 -m unittest tests.test_link_escape   # must fail
    python3 tools/mutate_link_rule.py restore
    PYTHONPATH=tools:tests python3 -m unittest tests.test_link_escape   # must pass
"""

from __future__ import annotations

import sys
from pathlib import Path

TARGET = Path(__file__).resolve().parent.parent / "tools" / "originlib" / "doclint.py"

REPAIRED = """            candidates = [(path.parent / clean), (base / clean)]
            inside = [one for one in candidates if _inside_repository(one, base)]
            if not inside:
                result.violations.append(
                    Finding.at(rel, f"link leaves the repository -> {target}", line)
                )
            elif not any(one.exists() for one in inside):
"""

PREVIOUS = """            candidates = [(path.parent / clean), (base / clean)]
            inside = candidates
            if not any(one.exists() for one in inside):
"""


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] not in ("apply", "restore"):
        print(__doc__)
        return 1
    text = TARGET.read_text(encoding="utf-8")
    old, new = (REPAIRED, PREVIOUS) if argv[0] == "apply" else (PREVIOUS, REPAIRED)
    count = text.count(old)
    if count != 1:
        print(
            f"refusing to {argv[0]}: the pattern matched {count} times, so the run "
            "would prove nothing about the rule. Read doclint.py and fix the pattern."
        )
        return 2
    TARGET.write_text(text.replace(old, new), encoding="utf-8")
    verb = "applied" if argv[0] == "apply" else "restored"
    print(f"{verb}: containment {'removed' if argv[0] == 'apply' else 'back'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
