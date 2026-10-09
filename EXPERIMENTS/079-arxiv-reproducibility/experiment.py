#!/usr/bin/env python3
"""
Experiment helper functions for E079 ArXiv reproducibility.
"""

import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def clone_repo(github_url: str, target_dir: Path) -> bool:
    """Clone a GitHub repository shallowly."""
    try:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", github_url, str(target_dir)],
            capture_output=True, text=True, timeout=120
        )
        return result.returncode == 0
    except Exception as e:
        print(f"  Clone error: {e}")
        return False


def run_tool_on_repo(repo_dir: Path, paper_year: int, output_req: Path):
    """Run the spec generation tool on a repository."""
    cmd = [
        sys.executable, "generate_spec.py",
        "--repo", str(repo_dir),
        "--year", str(paper_year),
        "--output", str(output_req)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if result.returncode == 0:
            reqs = output_req.read_text().strip().splitlines() if output_req.exists() else []
            return True, reqs, {"stdout": result.stdout, "stderr": result.stderr}
        else:
            return False, [], {"stdout": result.stdout, "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        return False, [], {"error": "Tool timeout"}
    except Exception as e:
        return False, [], {"error": str(e)}


def test_install_and_smoke(requirements_file: Path, repo_dir: Path, timeout: int = 300):
    """Test pip install and smoke test in clean venv."""
    with tempfile.TemporaryDirectory() as tmpdir:
        venv_dir = Path(tmpdir) / "env"
        try:
            # Create venv
            import venv
            venv.create(venv_dir, with_pip=True)
            pip = venv_dir / "bin" / "pip"
            python = venv_dir / "bin" / "python"

            # Install
            result = subprocess.run(
                [str(pip), "install", "-r", str(requirements_file)],
                capture_output=True, text=True, timeout=timeout
            )
            if result.returncode != 0:
                return False, f"Install failed: {result.stderr[:500]}"

            # Find entry point
            entry = find_entry_point(repo_dir)
            if not entry:
                return True, "No entry point found (install OK)"

            # Test import
            test_code = f"""
import sys
sys.path.insert(0, '{repo_dir}')
try:
    import {entry}
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

            # Test run --help
            result = subprocess.run(
                [str(python), "-m", entry, "--help"],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode not in (0, 1, 2):
                return False, f"Run failed: code {result.returncode}, {result.stderr[:500]}"

            return True, "OK"

        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except Exception as e:
            return False, f"Error: {e}"


def find_entry_point(repo_path: Path):
    """Find the main entry point module."""
    for name in ["main.py", "__main__.py", "run.py", "train.py", "experiment.py"]:
        if (repo_path / name).exists():
            return name.replace(".py", "")
    py_files = list(repo_path.glob("*.py"))
    if len(py_files) == 1:
        return py_files[0].stem
    return None


def run_repo2docker_baseline(repo_dir: Path, timeout: int = 600):
    """Run repo2docker on repo and test smoke test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            # repo2docker builds a Docker image
            image_name = f"e079-test-{int(time.time())}"
            result = subprocess.run(
                ["repo2docker", "--no-run", "--image-name", image_name, str(repo_dir)],
                capture_output=True, text=True, timeout=timeout
            )
            if result.returncode != 0:
                return False, f"repo2docker build failed: {result.stderr[:500]}"

            # Run container and test
            entry = find_entry_point(repo_dir)
            if not entry:
                # Clean up image
                subprocess.run(["docker", "rmi", image_name], capture_output=True)
                return True, "No entry point (build OK)"

            # Test in container
            test_cmd = f"python -c \"import sys; sys.path.insert(0, '/home/jovyan'); import {entry}; print('Import OK')\""
            result = subprocess.run(
                ["docker", "run", "--rm", image_name, "bash", "-c", test_cmd],
                capture_output=True, text=True, timeout=60
            )
            subprocess.run(["docker", "rmi", image_name], capture_output=True)

            if result.returncode != 0:
                return False, f"Container import failed: {result.stderr[:500]}"

            # Test --help
            help_cmd = f"python -m {entry} --help"
            result = subprocess.run(
                ["docker", "run", "--rm", image_name, "bash", "-c", help_cmd],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode not in (0, 1, 2):
                return False, f"Container run failed: {result.stderr[:500]}"

            return True, "OK"

        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except FileNotFoundError:
            return False, "repo2docker not installed"
        except Exception as e:
            return False, f"Error: {e}"


def load_papers(harvest_file: Path):
    """Load harvested papers from JSONL."""
    papers = []
    with open(harvest_file) as f:
        for line in f:
            line = line.strip()
            if line:
                papers.append(json.loads(line))
    return papers


def select_a2_a3_papers(papers: list, sample_size: int):
    """Select A2+A3 papers using stride sampling."""
    a2_a3 = [p for p in papers if p.get("env_classification") in ("A2", "A3", "A1_or_A2")]
    if len(a2_a3) <= sample_size:
        return a2_a3
    stride = len(a2_a3) // sample_size
    return [a2_a3[i * stride] for i in range(sample_size)]


def evaluate_gates(results):
    """Evaluate kill gates and return verdict."""
    n_tool = len(results["tool"]["details"])
    n_base = len(results["baseline"]["details"])

    tool_install_rate = results["tool"]["install_success"] / n_tool if n_tool > 0 else 0
    tool_combined_rate = results["tool"]["combined_success"] / n_tool if n_tool > 0 else 0
    base_combined_rate = results["baseline"]["combined_success"] / n_base if n_base > 0 else 0

    verdict = {
        "G1_install": tool_install_rate >= 0.80,
        "G3_combined": tool_combined_rate >= 0.30,
        "G4_baseline": tool_combined_rate > base_combined_rate + 0.10,
        "tool_install_rate": tool_install_rate,
        "tool_combined_rate": tool_combined_rate,
        "baseline_combined_rate": base_combined_rate,
    }
    return verdict


def print_results(results, verdict):
    """Print results summary."""
    n_tool = len(results["tool"]["details"])
    n_base = len(results["baseline"]["details"])

    tool_install_rate = verdict["tool_install_rate"]
    tool_combined_rate = verdict["tool_combined_rate"]
    base_combined_rate = verdict["baseline_combined_rate"]

    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)

    print(f"Tool:     {n_tool} papers tested")
    print(f"  Install success: {results['tool']['install_success']}/{n_tool} = {tool_install_rate:.1%}")
    print(f"  Combined (install+smoke): {results['tool']['combined_success']}/{n_tool} = {tool_combined_rate:.1%}")

    print(f"\nBaseline (repo2docker): {n_base} papers tested")
    print(f"  Combined success: {results['baseline']['combined_success']}/{n_base} = {base_combined_rate:.1%}")

    print(f"\nGate evaluation:")
    print(f"  G1 Install ≥80%: {tool_install_rate:.1%} {'✅ PASS' if verdict['G1_install'] else '❌ FAIL'}")
    print(f"  G3 Combined ≥30%: {tool_combined_rate:.1%} {'✅ PASS' if verdict['G3_combined'] else '❌ FAIL'}")
    print(f"  G4 Tool > Baseline + 10pp: {tool_combined_rate:.1%} vs {base_combined_rate:.1%} "
          f"{'✅ PASS' if verdict['G4_baseline'] else '❌ FAIL'}")

    all_pass = all(verdict[k] for k in ("G1_install", "G3_combined", "G4_baseline"))
    print(f"\nOVERALL: {'ALL GATES PASSED' if all_pass else 'GATES FAILED - ABANDON'}")
    return all_pass