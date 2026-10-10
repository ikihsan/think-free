#!/usr/bin/env python3
"""fix_import - Detect ModuleNotFoundError/ImportError from command output and suggest the correct distribution to install.

This is a prototype resolver integration for the pyprovides tool.
It runs a command, captures stderr, and if it detects an import error,
suggests the correct PyPI distribution to install.

Usage: python3 -m pyprovides.fix_import -- python3 -c "import sklearn"
"""

import argparse
import re
import subprocess
import sys
import os

# Add parent directory to path for pyprovides module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyprovides import find_provider, ResolveError


# Patterns to detect import errors and extract module names
IMPORT_ERROR_PATTERNS = [
    # ModuleNotFoundError: No module named 'module_name'
    re.compile(r"ModuleNotFoundError:\s*No module named\s+['\"]([\w.]+)['\"]"),
    # ImportError: No module named 'module_name'
    re.compile(r"ImportError:\s*No module named\s+['\"]([\w.]+)['\"]"),
    # ImportError: No module named module_name (no quotes)
    re.compile(r"ImportError:\s*No module named\s+(\w+)"),
    # ModuleNotFoundError: No module named module_name (no quotes)
    re.compile(r"ModuleNotFoundError:\s*No module named\s+(\w+)"),
]


def extract_module_names(text: str):
    """Extract module names from import error messages in text."""
    modules = []
    for pattern in IMPORT_ERROR_PATTERNS:
        matches = pattern.findall(text)
        for match in matches:
            # Get top-level module name (before any dots)
            top_module = match.split('.')[0]
            if top_module and top_module not in modules:
                modules.append(top_module)
    return modules


def resolve_module(module: str, max_checks: int = 500, verbose: bool = False):
    """Resolve a module name to a distribution using pyprovides."""
    try:
        status, matches, detail = find_provider(module, max_checks=max_checks)
        
        if status == "found":
            dist_name, mods, prov_detail = matches[0]
            return {
                "status": "found",
                "module": module,
                "distribution": prov_detail["canonical"],
                "version": prov_detail["version"],
                "method": detail["method"],
                "wheel": prov_detail["wheel"],
                "install_cmd": f"pip install {prov_detail['canonical']}",
            }
        elif status == "stdlib":
            return {
                "status": "stdlib",
                "module": module,
                "message": f"{module} is in the Python standard library (no install needed)",
            }
        else:
            return {
                "status": "not_found",
                "module": module,
                "message": f"{module}: no provider found among top {detail['checked']} PyPI distributions",
            }
    except ResolveError as exc:
        return {
            "status": "error",
            "module": module,
            "message": f"Cannot resolve {module}: {exc}",
        }
    except Exception as exc:
        return {
            "status": "error",
            "module": module,
            "message": f"Error during search: {exc}",
        }


def run_command(cmd_args):
    """Run a command and return (stdout, stderr, returncode)."""
    result = subprocess.run(
        cmd_args,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.stdout, result.stderr, result.returncode


def main():
    parser = argparse.ArgumentParser(
        prog="fix_import",
        description="Detect import errors from command output and suggest correct distributions",
    )
    parser.add_argument(
        "--max-checks",
        type=int,
        default=500,
        help="Maximum distributions to check per module (default: 500)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed resolution info",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without running the command",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to run (e.g., -- python3 -c \"import sklearn\")",
    )
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Remove leading '--' if present
    if args.command[0] == "--":
        args.command = args.command[1:]

    if args.dry_run:
        print(f"Would run: {' '.join(args.command)}")
        return 0

    print(f"Running: {' '.join(args.command)}")
    stdout, stderr, returncode = run_command(args.command)

    if stdout:
        print("STDOUT:")
        print(stdout)

    if stderr:
        print("STDERR:")
        print(stderr)

    # Extract module names from stderr
    modules = extract_module_names(stderr)
    
    if not modules:
        if returncode != 0:
            print(f"\nCommand exited with code {returncode}, but no import errors detected.")
        return returncode

    print(f"\nDetected import errors for modules: {', '.join(modules)}")
    print("\nResolving...")

    all_found = True
    for module in modules:
        result = resolve_module(module, max_checks=args.max_checks, verbose=args.verbose)
        
        if result["status"] == "found":
            print(f"\n✓ {result['module']} is provided by {result['distribution']} {result['version']}")
            print(f"  Method: {result['method']}")
            print(f"  Wheel: {result['wheel']}")
            print(f"  Install: {result['install_cmd']}")
        elif result["status"] == "stdlib":
            print(f"\n✓ {result['module']}: {result['message']}")
        else:
            print(f"\n✗ {result['module']}: {result['message']}")
            all_found = False

    if all_found:
        print("\n✓ All import errors can be resolved with the suggested installs.")
    else:
        print("\n⚠ Some import errors could not be resolved.")

    return returncode


if __name__ == "__main__":
    sys.exit(main())