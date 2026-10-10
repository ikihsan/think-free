#!/usr/bin/env python3
"""
Test pyfix with a script that has multiple missing imports.
Simulates a realistic scenario: cloning a repo and running a script.
"""

import subprocess
import time
import sys
import os
import tempfile

def run_command(cmd, cwd=None, env=None):
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=env, timeout=120)
    elapsed = time.time() - start
    return result.stdout, result.stderr, result.returncode, elapsed

def main():
    # Create a test script with multiple missing imports (alias cases that are truly missing)
    test_script_content = '''
# Test script with multiple missing dependencies (alias cases)
import psycopg2
import MySQLdb
import some_random_module_that_does_not_exist_xyz

print("All imports successful!")
'''
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_script = os.path.join(temp_dir, "multi_test.py")
        with open(test_script, "w") as f:
            f.write(test_script_content)
        
        pyfix_path = os.path.join(os.path.dirname(__file__), "pyfix")
        
        print("=== Running script with pyfix (first run - all missing) ===")
        stdout, stderr, rc, t = run_command([pyfix_path, sys.executable, test_script])
        print(f"Time: {t:.2f}s")
        print(f"Return code: {rc}")
        if stdout:
            print(f"STDOUT:\n{stdout}")
        if stderr:
            print(f"STDERR:\n{stderr}")
        
        # Extract suggested installs
        print("\n=== Suggested installs from pyfix ===")
        for line in stdout.split('\n'):
            if 'Install:' in line or 'pip install' in line:
                print(f"  {line.strip()}")

if __name__ == "__main__":
    main()