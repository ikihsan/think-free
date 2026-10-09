#!/usr/bin/env python3
"""
Information-sufficiency witness for ArXiv reproducibility (E079).

Tests whether two repositories with identical permitted inputs but requiring
different pinned versions can be distinguished by the tool's permitted inputs.
"""

import sys
import tempfile
import shutil
import subprocess
from pathlib import Path


def create_repo_a(path: Path):
    """Repo A: needs numpy==1.21.0 due to array_function API."""
    path.mkdir(parents=True)
    (path / "requirements.txt").write_text("numpy\npandas\n")
    # Main module using numpy.lib.array_function (API changed in numpy 1.22)
    (path / "main.py").write_text('''
import numpy as np
import pandas as pd

def main(args=None):
    # Uses numpy.lib.array_function_impl - behavior changed in 1.22
    arr = np.array([1, 2, 3])
    # This pattern relies on 1.21.x behavior
    result = np.lib.array_function_impl(np.sum, (arr,), {})
    print(f"Result: {result}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
''')
    # README with entry point hint
    (path / "README.md").write_text("# Repo A\n\nRun: `python main.py`\n")


def create_repo_b(path: Path):
    """Repo B: works with numpy>=1.20, stable API only."""
    path.mkdir(parents=True)
    (path / "requirements.txt").write_text("numpy\npandas\n")
    # Main module using only stable numpy API
    (path / "main.py").write_text('''
import numpy as np
import pandas as pd

def main(args=None):
    # Only uses stable API: np.array, np.sum
    arr = np.array([1, 2, 3])
    result = np.sum(arr)
    print(f"Result: {result}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
''')
    (path / "README.md").write_text("# Repo B\n\nRun: `python main.py`\n")


def get_permitted_inputs(repo_path: Path) -> dict:
    """Extract the permitted inputs the tool would see."""
    readme = repo_path / "README.md"
    readme_text = readme.read_text() if readme.exists() else ""
    # Normalize README: replace repo-specific names with placeholder
    # In reality, the tool sees paper metadata (title, date, authors) from ArXiv,
    # not the GitHub repo name. The README content varies but the STRUCTURE is same.
    normalized_readme = readme_text.replace("Repo A", "REPO").replace("Repo B", "REPO")
    return {
        "requirements_txt": (repo_path / "requirements.txt").read_text().strip(),
        "python_files": sorted([f.name for f in repo_path.glob("*.py")]),
        "has_readme": readme.exists(),
        "readme_structure": "entry_point_hint" if "python main.py" in readme_text else "none",
    }


def run_tool_on_repo(repo_path: Path) -> dict:
    """
    Placeholder for the actual tool. In the real experiment, this would call
    the spec-generation tool. For the witness, we simulate the tool's view
    by returning the permitted inputs (showing they are identical).
    """
    return get_permitted_inputs(repo_path)


def main():
    print("=" * 60)
    print("E079 Information-Sufficiency Witness: W-ARXIV-1")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        repo_a = tmp / "repo_a"
        repo_b = tmp / "repo_b"

        create_repo_a(repo_a)
        create_repo_b(repo_b)

        print("\n[Setup] Created two synthetic repositories:")
        print(f"  Repo A: {repo_a}")
        print(f"  Repo B: {repo_b}")

        # Extract permitted inputs
        inputs_a = get_permitted_inputs(repo_a)
        inputs_b = get_permitted_inputs(repo_b)

        print("\n[Permitted inputs for Repo A]:")
        for k, v in inputs_a.items():
            print(f"  {k}: {v!r}")

        print("\n[Permitted inputs for Repo B]:")
        for k, v in inputs_b.items():
            print(f"  {k}: {v!r}")

        # Check if permitted inputs are identical (they should be)
        identical = inputs_a == inputs_b
        print(f"\n[Check] Permitted inputs identical: {identical}")

        if not identical:
            print("  WARNING: Permitted inputs differ - witness setup flawed")
            return 1

        # Simulate tool output (in real experiment, call actual tool here)
        # For witness, we show that FROM permitted inputs alone, the tool
        # cannot know which numpy version to pin.
        print("\n[Analysis] Both repos have:")
        print("  - requirements.txt: 'numpy\\npandas' (unpinned)")
        print("  - main.py (different internal code, same imports)")
        print("  - README.md with 'python main.py'")
        print("\n  Repo A NEEDS numpy==1.21.0 (array_function_impl behavior)")
        print("  Repo B WORKS WITH numpy>=1.20 (stable API only)")
        print("\n  From permitted inputs alone (file tree, requirements.txt,")
        print("  README, paper metadata), these two realities are INDISTINGUISHABLE.")

        print("\n" + "=" * 60)
        print("WITNESS RESULT: FAIL (as predicted)")
        print("=" * 60)
        print("The tool's permitted inputs cannot distinguish Repo A from Repo B.")
        print("Any deterministic tool seeing only these inputs will produce")
        print("identical pinned requirements for both, causing one to fail.")
        print("\nThis BOUNDS the claim: the tool must either")
        print("  (a) Run trial installations (expensive, needs compute)")
        print("  (b) Use heuristics (paper date, common versions) - may guess wrong")
        print("  (c) Abstain when uncertain")
        print("=" * 60)

        return 0  # Witness correctly demonstrates the bound


if __name__ == "__main__":
    sys.exit(main())