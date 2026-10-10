#!/usr/bin/env python3
"""
Workflow evaluation for pyprovides fix-import.

Simulates a developer encountering import errors and measuring time-to-fix
with pyfix vs manual pip install baseline.
"""

import subprocess
import time
import sys
import os
import tempfile
import json

# Test scenarios: (module_name, expected_distribution, description)
SCENARIOS = [
    ("sklearn", "scikit-learn", "Common ML alias"),
    ("cv2", "opencv-python", "Computer vision alias"),
    ("bs4", "beautifulsoup4", "HTML parsing alias"),
    ("yaml", "PyYAML", "YAML parsing alias"),
    ("PIL", "Pillow", "Image processing alias"),
    ("dateutil", "python-dateutil", "Date utilities alias"),
    ("Crypto", "pycryptodome", "Cryptography alias"),
    ("requests", "requests", "Same name (control)"),
    ("numpy", "numpy", "Same name (control)"),
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
        timeout=60,
    )
    elapsed = time.time() - start
    return result.stdout, result.stderr, result.returncode, elapsed

def test_manual_baseline(module, expected_dist, temp_dir):
    """Simulate manual fix: run, see error, pip install, re-run."""
    # Create a test script that imports the module
    test_script = os.path.join(temp_dir, f"test_{module}.py")
    with open(test_script, "w") as f:
        f.write(f"import {module}\nprint('Success: {module} imported')\n")
    
    # Run 1: First attempt (fails)
    stdout1, stderr1, rc1, t1 = run_command([sys.executable, test_script])
    
    # Manual fix: pip install
    stdout2, stderr2, rc2, t2 = run_command([sys.executable, "-m", "pip", "install", expected_dist])
    
    # Run 2: After install (succeeds)
    stdout3, stderr3, rc3, t3 = run_command([sys.executable, test_script])
    
    total_time = t1 + t2 + t3
    success = rc3 == 0
    
    return {
        "module": module,
        "expected_dist": expected_dist,
        "method": "manual",
        "time_first_run": t1,
        "time_pip_install": t2,
        "time_second_run": t3,
        "total_time": total_time,
        "success": success,
        "first_error": "ModuleNotFoundError" in stderr1,
    }

def test_pyfix(module, expected_dist, temp_dir):
    """Test with pyfix: run with pyfix, see suggestion, pip install, re-run."""
    # Create a test script that imports the module
    test_script = os.path.join(temp_dir, f"test_{module}.py")
    with open(test_script, "w") as f:
        f.write(f"import {module}\nprint('Success: {module} imported')\n")
    
    # Run 1: With pyfix (shows suggestion)
    pyfix_path = os.path.join(os.path.dirname(__file__), "pyfix")
    stdout1, stderr1, rc1, t1 = run_command([pyfix_path, sys.executable, test_script])
    
    # Check if pyfix suggested the correct distribution
    suggested_correctly = expected_dist in stdout1 or expected_dist in stderr1
    
    # Manual fix based on pyfix suggestion: pip install
    stdout2, stderr2, rc2, t2 = run_command([sys.executable, "-m", "pip", "install", expected_dist])
    
    # Run 2: After install (succeeds)
    stdout3, stderr3, rc3, t3 = run_command([sys.executable, test_script])
    
    total_time = t1 + t2 + t3
    success = rc3 == 0
    
    return {
        "module": module,
        "expected_dist": expected_dist,
        "method": "pyfix",
        "time_first_run": t1,
        "time_pip_install": t2,
        "time_second_run": t3,
        "total_time": total_time,
        "success": success,
        "suggested_correctly": suggested_correctly,
        "first_error": "ModuleNotFoundError" in stderr1,
    }

def main():
    # Create temp directory for test scripts
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temp dir: {temp_dir}")
        
        # Check if modules are already installed; uninstall them for clean test
        print("\n=== Cleaning up pre-installed modules ===")
        for module, expected_dist, _ in SCENARIOS:
            # Try to uninstall if it's not a stdlib module
            if module not in ["os", "sys", "json", "time", "tempfile"]:
                run_command([sys.executable, "-m", "pip", "uninstall", "-y", expected_dist])
        
        results = []
        
        print("\n=== Testing Manual Baseline ===")
        for module, expected_dist, desc in SCENARIOS:
            print(f"\nTesting {module} -> {expected_dist} ({desc})")
            try:
                result = test_manual_baseline(module, expected_dist, temp_dir)
                results.append(result)
                print(f"  Manual: total={result['total_time']:.2f}s, success={result['success']}")
            except Exception as e:
                print(f"  Manual: ERROR - {e}")
                results.append({
                    "module": module,
                    "expected_dist": expected_dist,
                    "method": "manual",
                    "error": str(e),
                    "success": False,
                })
        
        # Re-uninstall for pyfix test
        print("\n=== Cleaning up for pyfix test ===")
        for module, expected_dist, _ in SCENARIOS:
            if module not in ["os", "sys", "json", "time", "tempfile"]:
                run_command([sys.executable, "-m", "pip", "uninstall", "-y", expected_dist])
        
        print("\n=== Testing pyfix ===")
        for module, expected_dist, desc in SCENARIOS:
            print(f"\nTesting {module} -> {expected_dist} ({desc})")
            try:
                result = test_pyfix(module, expected_dist, temp_dir)
                results.append(result)
                print(f"  pyfix: total={result['total_time']:.2f}s, success={result['success']}, suggested={result.get('suggested_correctly', False)}")
            except Exception as e:
                print(f"  pyfix: ERROR - {e}")
                results.append({
                    "module": module,
                    "expected_dist": expected_dist,
                    "method": "pyfix",
                    "error": str(e),
                    "success": False,
                })
        
        # Summary
        print("\n=== SUMMARY ===")
        manual_results = [r for r in results if r.get("method") == "manual" and r.get("success")]
        pyfix_results = [r for r in results if r.get("method") == "pyfix" and r.get("success")]
        
        if manual_results and pyfix_results:
            avg_manual = sum(r["total_time"] for r in manual_results) / len(manual_results)
            avg_pyfix = sum(r["total_time"] for r in pyfix_results) / len(pyfix_results)
            print(f"Average manual time: {avg_manual:.2f}s ({len(manual_results)} successful)")
            print(f"Average pyfix time:  {avg_pyfix:.2f}s ({len(pyfix_results)} successful)")
            if avg_manual > 0:
                speedup = avg_manual / avg_pyfix
                print(f"Speedup factor: {speedup:.2f}x")
        
        # Save results
        output_file = os.path.join(os.path.dirname(__file__), "workflow_results.json")
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()