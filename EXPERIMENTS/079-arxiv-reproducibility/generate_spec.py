#!/usr/bin/env python3
"""
Generate pinned environment specification from ArXiv paper's GitHub repo.

This is the core tool being tested. It uses:
1. Static analysis of imports (pipreqs-style)
2. Paper submission date to narrow version search space
3. Limited trial installation to verify compatibility
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import venv
from pathlib import Path
from urllib.request import Request, urlopen

from heuristics import get_version_range, map_import_to_package


def extract_imports(repo_path: Path):
    """Extract Python imports from all .py files in repo."""
    imports = set()
    for py_file in repo_path.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            # Simple import extraction
            for line in content.splitlines():
                line = line.strip()
                if line.startswith("import "):
                    parts = line[7:].split(",")
                    for p in parts:
                        imports.add(p.split(".")[0].strip())
                elif line.startswith("from "):
                    parts = line[5:].split(" import")
                    if parts:
                        imports.add(parts[0].split(".")[0].strip())
        except Exception:
            pass
    return imports


def fetch_pypi_versions(package: str):
    """Fetch available versions from PyPI."""
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        req = Request(url, headers={"Accept": "application/json"})
        with urlopen(req, timeout=10) as resp:
            data = json.load(resp)
        return list(data.get("releases", {}).keys())
    except Exception:
        return []


def filter_versions(versions, min_v: str, max_v: str):
    """Filter versions within range (simplified)."""
    from packaging import version
    try:
        min_ver = version.parse(min_v) if min_v != "0" else version.parse("0")
        max_ver = version.parse(max_v) if max_v != "999" else version.parse("999.999")
        filtered = [v for v in versions if min_ver <= version.parse(v) <= max_ver]
        return sorted(filtered, key=version.parse, reverse=True)
    except Exception:
        return versions[:10]  # Fallback


def find_entry_point(repo_path: Path):
    """Find the main entry point module."""
    # Check setup.py / pyproject.toml for entry_points
    for f in ["setup.py", "pyproject.toml", "setup.cfg"]:
        fp = repo_path / f
        if fp.exists():
            content = fp.read_text()
            if "entry_points" in content or "console_scripts" in content:
                # Would need proper parsing; skip for now
                pass

    # Check common entry points
    for name in ["main.py", "__main__.py", "run.py", "train.py", "experiment.py"]:
        if (repo_path / name).exists():
            return name.replace(".py", "")

    # Check for single .py file in root
    py_files = list(repo_path.glob("*.py"))
    if len(py_files) == 1:
        return py_files[0].stem

    return None


def test_install_and_run(requirements, repo_path: Path, entry_point: str, timeout: int = 300):
    """Test install and smoke test in a clean venv."""
    with tempfile.TemporaryDirectory() as tmpdir:
        venv_dir = Path(tmpdir) / "test_env"
        try:
            # Create venv
            venv.create(venv_dir, with_pip=True)
            pip = venv_dir / "bin" / "pip"
            python = venv_dir / "bin" / "python"

            # Install requirements
            req_file = Path(tmpdir) / "requirements.txt"
            req_file.write_text("\n".join(requirements))

            result = subprocess.run(
                [str(pip), "install", "-r", str(req_file)],
                capture_output=True, text=True, timeout=timeout
            )
            if result.returncode != 0:
                return False, f"Install failed: {result.stderr[:500]}"

            # Smoke test: import and run --help
            if entry_point:
                # Try to import the module
                test_code = f"""
import sys
sys.path.insert(0, '{repo_path}')
try:
    import {entry_point}
    print('Import OK')
except Exception as e:
    print(f'Import failed: {{e}}')
    sys.exit(1)
"""
                result = subprocess.run(
                    [str(python), "-c", test_code],
                    capture_output=True, text=True, timeout=60
                )
                if result.returncode != 0:
                    return False, f"Import failed: {result.stderr[:500]}"

                # Try running with --help
                result = subprocess.run(
                    [str(python), "-m", entry_point, "--help"],
                    capture_output=True, text=True, timeout=60
                )
                # --help may return 0 or 1 (argparse), but should not crash
                if result.returncode not in (0, 1, 2):
                    return False, f"Run failed with code {result.returncode}: {result.stderr[:500]}"

            return True, "OK"

        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except Exception as e:
            return False, f"Error: {e}"


def generate_pinned_requirements(repo_path: Path, paper_year: int):
    """
    Generate pinned requirements for a repository.
    Returns (pinned_requirements_list, metadata_dict)
    """
    imports = extract_imports(repo_path)
    packages = []
    for imp in imports:
        pkg = map_import_to_package(imp)
        if pkg:
            packages.append(pkg)

    # Also check existing requirements.txt
    req_file = repo_path / "requirements.txt"
    if req_file.exists():
        for line in req_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                pkg = line.split("==")[0].split(">=")[0].split("<=")[0].strip()
                if pkg and pkg not in packages:
                    packages.append(pkg)

    # Deduplicate
    packages = list(dict.fromkeys(packages))

    # For each package, select a version
    pinned = []
    metadata = {"packages_analyzed": packages, "versions_selected": {}}

    for pkg in packages:
        versions = fetch_pypi_versions(pkg)
        if not versions:
            pinned.append(pkg)  # Unpinned fallback
            metadata["versions_selected"][pkg] = "latest"
            continue

        min_v, max_v = get_version_range(pkg, paper_year)
        candidates = filter_versions(versions, min_v, max_v)

        if not candidates:
            # Fallback: try latest
            candidates = versions[:5]

        # For now, pick the latest in range (most likely to work)
        # Real implementation would try multiple
        selected = candidates[0] if candidates else versions[0]
        pinned.append(f"{pkg}=={selected}")
        metadata["versions_selected"][pkg] = selected

    return pinned, metadata


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate pinned requirements for ArXiv repo")
    parser.add_argument("--repo", required=True, help="Path to cloned repository")
    parser.add_argument("--year", type=int, required=True, help="Paper submission year")
    parser.add_argument("--output", help="Output requirements.txt path")
    parser.add_argument("--test", action="store_true", help="Test install and run")
    args = parser.parse_args()

    repo_path = Path(args.repo)
    if not repo_path.exists():
        print(f"Repo not found: {repo_path}", file=sys.stderr)
        return 1

    print(f"Analyzing repo: {repo_path}")
    print(f"Paper year: {args.year}")

    pinned, metadata = generate_pinned_requirements(repo_path, args.year)

    print(f"Found packages: {metadata['packages_analyzed']}")
    print(f"Selected versions: {metadata['versions_selected']}")
    print(f"Pinned requirements:")
    for req in pinned:
        print(f"  {req}")

    if args.output:
        Path(args.output).write_text("\n".join(pinned) + "\n")
        print(f"Written to {args.output}")

    if args.test:
        entry = find_entry_point(repo_path)
        print(f"Entry point: {entry}")
        success, msg = test_install_and_run(pinned, repo_path, entry or "")
        print(f"Test result: {'PASS' if success else 'FAIL'} - {msg}")
        return 0 if success else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())