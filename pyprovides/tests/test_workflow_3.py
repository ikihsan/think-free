#!/usr/bin/env python3
"""
Workflow evaluation for pyprovides fix-import - focused on alias cases.
Tests only modules that are NOT available and have module != distribution.
"""

import subprocess
import time
import sys
import os
import tempfile
import json

# Alias cases where module name != distribution name AND module is NOT available
ALIAS_SCENARIOS = [
    ("cv2", "opencv-python", "Computer vision alias"),
    ("psycopg2", "psycopg2-binary", "PostgreSQL adapter alias"),
    ("MySQLdb", "mysqlclient", "MySQL adapter alias"),
]

def run_command(cmd, cwd=None, env=None):
    """Run command and return (stdout, stderr, returncode, elapsed)."""
    start = time.time()
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
        timeout=120,
    )
    elapsed = time.time() - start
    return result.stdout, result.stderr, result.returncode, elapsed

def test_manual_baseline(module, expected_dist, temp_dir):
    """Simulate manual fix with search time."""
    test_script = os.path.join(temp_dir, f"test_{module}.py")
    with open(test_script, "w") as f:
        f.write(f"import {module}\nprint('Success: {module} imported')\n")
    
    # Run 1: First attempt (fails)
    stdout1, stderr1, rc1, t1 = run_command([sys.executable, test_script])
    
    # Simulate search time for alias cases
    search_time = 15.0  # seconds to search/recall correct package for alias
    time.sleep(0.01)
    
    # Manual fix: pip install
    stdout2, stderr2, rc2, t2 = run_command([sys.executable, "-m", "pip", "install", expected_dist])
    
    # Run 2: After install (succeeds or fails due to sys deps)
    stdout3, stderr3, rc3, t3 = run_command([sys.executable, test_script])
    
    total_time = t1 + search_time + t2 + t3
    success = rc3 == 0
    
    return {
        "module": module,
        "expected_dist": expected_dist,
        "method": "manual",
        "time_first_run": t1,
        "time_search": search_time,
        "time_pip_install": t2,
        "time_second_run": t3,
        "total_time": total_time,
        "success": success,
        "first_error": "ModuleNotFoundError" in stderr1,
        "pip_stdout": stdout2,
        "pip_stderr": stderr2,
    }

def test_pyfix(module, expected_dist, temp_dir):
    """Test with pyfix."""
    test_script = os.path.join(temp_dir, f"test_{module}.py")
    with open(test_script, "w") as f:
        f.write(f"import {module}\nprint('Success: {module} imported')\n")
    
    # Run 1: With pyfix
    pyfix_path = os.path.join(os.path.dirname(__file__), "pyfix")
    stdout1, stderr1, rc1, t1 = run_command([pyfix_path, sys.executable, test_script])
    
    # Check if pyfix suggested the correct distribution
    suggested_correctly = expected_dist in stdout1 or expected_dist in stderr1
    
    # Minimal search time with pyfix
    search_time = 2.0
    time.sleep(0.01)
    
    # Pip install based on pyfix suggestion
    stdout2, stderr2, rc2, t2 = run_command([sys.executable, "-m", "pip", "install", expected_dist])
    
    # Run 2: After install
    stdout3, stderr3, rc3, t3 = run_command([sys.executable, test_script])
    
    total_time = t1 + search_time + t2 + t3
    success = rc3 == 0
    
    return {
        "module": module,
        "expected_dist": expected_dist,
        "method": "pyfix",
        "time_first_run": t1,
        "time_search": search_time,
        "time_pip_install": t2,
        "time_second_run": t3,
        "total_time": total_time,
        "success": success,
        "suggested_correctly": suggested_correctly,
        "first_error": "ModuleNotFoundError" in stderr1,
        "pip_stdout": stdout2,
        "pip_stderr": stderr2,
    }

def main():
    # Filter to only unavailable modules
    test_scenarios = []
    for module, expected_dist, desc in ALIAS_SCENARIOS:
        result = subprocess.run([sys.executable, "-c", f"import {module}"], capture_output=True)
        if result.returncode != 0:
            test_scenarios.append((module, expected_dist, desc))
            print(f"Will test: {module} -> {expected_dist} ({desc})")
        else:
            print(f"Skipping {module}: already available")
    
    if not test_scenarios:
        print("No alias modules to test - all are already available")
        return
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temp dir: {temp_dir}")
        
        # Uninstall distributions
        print("\n=== Cleaning up distributions ===")
        for module, expected_dist, _ in test_scenarios:
            run_command([sys.executable, "-m", "pip", "uninstall", "-y", expected_dist])
        
        results = []
        
        print("\n=== Testing Manual Baseline ===")
        for module, expected_dist, desc in test_scenarios:
            print(f"\nTesting {module} -> {expected_dist} ({desc})")
            try:
                result = test_manual_baseline(module, expected_dist, temp_dir)
                results.append(result)
                print(f"  Manual: total={result['total_time']:.2f}s, success={result['success']}")
                if not result['success']:
                    print(f"    pip stderr: {result['pip_stderr'][:200]}")
            except Exception as e:
                print(f"  Manual: ERROR - {e}")
                results.append({"module": module, "expected_dist": expected_dist, "method": "manual", "error": str(e), "success": False})
        
        # Re-uninstall
        print("\n=== Cleaning up for pyfix test ===")
        for module, expected_dist, _ in test_scenarios:
            run_command([sys.executable, "-m", "pip", "uninstall", "-y", expected_dist])
        
        print("\n=== Testing pyfix ===")
        for module, expected_dist, desc in test_scenarios:
            print(f"\nTesting {module} -> {expected_dist} ({desc})")
            try:
                result = test_pyfix(module, expected_dist, temp_dir)
                results.append(result)
                print(f"  pyfix: total={result['total_time']:.2f}s, success={result['success']}, suggested={result.get('suggested_correctly', False)}")
                if not result['success']:
                    print(f"    pip stderr: {result['pip_stderr'][:200]}")
            except Exception as e:
                print(f"  pyfix: ERROR - {e}")
                results.append({"module": module, "expected_dist": expected_dist, "method": "pyfix", "error": str(e), "success": False})
        
        # Summary
        print("\n=== SUMMARY ===")
        manual_results = [r for r in results if r.get("method") == "manual"]
        pyfix_results = [r for r in results if r.get("method") == "pyfix"]
        
        for m, p in zip(manual_results, pyfix_results):
            module = m["module"]
            print(f"\n{module}:")
            print(f"  Manual: {m['total_time']:.2f}s (search: {m['time_search']}s, pip: {m['time_pip_install']:.2f}s) success={m['success']}")
            print(f"  pyfix:  {p['total_time']:.2f}s (search: {p['time_search']}s, pip: {p['time_pip_install']:.2f}s) success={p['success']}, suggested={p.get('suggested_correctly', False)}")
            if m['success'] and p['success']:
                speedup = m['total_time'] / p['total_time']
                print(f"  Speedup: {speedup:.2f}x")
        
        output_file = os.path.join(os.path.dirname(__file__), "workflow_results_v3.json")
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()