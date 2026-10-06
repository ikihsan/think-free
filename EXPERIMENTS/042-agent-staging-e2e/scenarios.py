#!/usr/bin/env python3
"""Scenarios for KILL-Q evaluation and E042 agent staging test."""

from dataclasses import dataclass
from typing import List

STG_PATH = "/home/ubuntu/think-free/stage-lines/stg"


@dataclass
class Scenario:
    name: str
    setup_code: str
    target_spec: str
    description: str


# Scenario definitions for KILL-Q evaluation
KILL_Q_SCENARIOS: List[Scenario] = [
    Scenario(
        name="func_modify",
        setup_code='''
d = tempfile.mkdtemp(prefix="kill-q-ex1-")
with open(os.path.join(d, "f"), "w") as f:
    f.write("def foo():\\n    x = 1\\n    y = 2\\n    return x + y\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "init1", "--no-gpg-sign"], cwd=d, capture_output=True)
with open(os.path.join(d, "f"), "w") as f:
    f.write("def foo():\\n    x = 10\\n    y = 20\\n    return x + y\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "changed1", "--no-gpg-sign"], cwd=d, capture_output=True)
''',
        target_spec="f:2",
        description="Modify a single line in function body (line 2: x=1 -> x=10)"
    ),
    Scenario(
        name="adjacent_mods",
        setup_code='''
d = tempfile.mkdtemp(prefix="kill-q-ex2-")
with open(os.path.join(d, "f"), "w") as f:
    f.write("a\\nb\\nc\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "init2", "--no-gpg-sign"], cwd=d, capture_output=True)
with open(os.path.join(d, "f"), "w") as f:
    f.write("A\\nb\\nc\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "changed2", "--no-gpg-sign"], cwd=d, capture_output=True)
''',
        target_spec="f:1",
        description="Split adjacent modifications (the key stg advantage): a->A on line 1"
    ),
    Scenario(
        name="multi_line_insert",
        setup_code='''
d = tempfile.mkdtemp(prefix="kill-q-ex3-")
with open(os.path.join(d, "f"), "w") as f:
    f.write("a\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "init3", "--no-gpg-sign"], cwd=d, capture_output=True)
with open(os.path.join(d, "f"), "w") as f:
    f.write("a\\nb1\\nb2\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "changed3", "--no-gpg-sign"], cwd=d, capture_output=True)
''',
        target_spec="f:2",
        description="Multi-line insertion: add b1, b2 after line a, stage line 2"
    ),
    Scenario(
        name="deletion_end",
        setup_code='''
d = tempfile.mkdtemp(prefix="kill-q-ex4-")
with open(os.path.join(d, "f"), "w") as f:
    f.write("a\\nb\\nc\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "init4", "--no-gpg-sign"], cwd=d, capture_output=True)
with open(os.path.join(d, "f"), "w") as f:
    f.write("a\\nb\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "changed4", "--no-gpg-sign"], cwd=d, capture_output=True)
''',
        target_spec="f:3",
        description="Deletion at end: remove c (line 3), stage it"
    ),
    Scenario(
        name="deletion_top",
        setup_code='''
d = tempfile.mkdtemp(prefix="kill-q-ex5-")
with open(os.path.join(d, "f"), "w") as f:
    f.write("a\\nb\\c\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "init5", "--no-gpg-sign"], cwd=d, capture_output=True)
with open(os.path.join(d, "f"), "w") as f:
    f.write("c\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "changed5", "--no-gpg-sign"], cwd=d, capture_output=True)
''',
        target_spec="f:1",
        description="Deletion at top: remove a and b, leaving only c, stage line 1"
    ),
    Scenario(
        name="range_selection",
        setup_code='''
d = tempfile.mkdtemp(prefix="kill-q-ex6-")
with open(os.path.join(d, "f"), "w") as f:
    f.write("a\\nb\\c\\nd\\ne\\nf\\ng\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "init6", "--no-gpg-sign"], cwd=d, capture_output=True)
with open(os.path.join(d, "f"), "w") as f:
    f.write("A\\nb\\C\\D\\e\\nf\\ng\\n")
subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
subprocess.run(["git", "commit", "-m", "changed6", "--no-gpg-sign"], cwd=d, capture_output=True)
''',
        target_spec="f:1-4",
        description="Range selection: stage lines 1-4 (a,A and b,c->C,D)"
    ),
]


# Target specs mapped by scenario name
TARGET_SPECS = {
    "func_modify": "f:2",
    "adjacent_mods": "f:1",
    "multi_line_insert": "f:2",
    "deletion_end": "f:3",
    "deletion_top": "f:1",
    "range_selection": "f:1-4",
}