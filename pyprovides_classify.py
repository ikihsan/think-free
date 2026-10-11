#!/usr/bin/env python3
"""
pyprovides-classify — Prototype tool that combines the view-count principle
with import error resolution.

This is a prototype (status: draft) that integrates two pieces of the mission's
infrastructure:
  1. The view-count principle's classification framework (E071): need-related
     packages are systematically more "active" (have significant activity metadata)
     than random packages on PyPI.
  2. The pyprovides module→distribution resolution mechanism (E085): finds which
     PyPI distribution provides a given module with nothing installed.

Prototype purpose: Evidence-gathering. Test whether combining these two validated
mechanisms produces a more useful developer workflow than either alone.

NOT a product. Not released. Status: draft.
"""

import sys
import os
import argparse

# Ensure pyprovides is importable from this repository's vendor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyprovides import provides, find_provider, ResolveError
from pyprovides.fix_import import extract_module_names, resolve_module, run_command


def is_crate_active(crate_info: dict) -> bool:
    """Determine if a PyPI distribution is 'active'.
    
    'Active' means the distribution has significant activity metadata,
    analogous to the E071/E072 definitions used in the view-count principle.
    We check recent_downloads > 0 or total downloads > 0.
    """
    recent = crate_info.get("recent_downloads")
    if recent is not None and recent > 0:
        return True
    downloads = crate_info.get("downloads", 0)
    if downloads is not None and downloads > 0:
        return True
    return False


def classify_need_related(module_name: str, provider_detail: dict) -> str:
    """Classify a module as need-related or random using the view-count principle.
    
    Heuristic: modules with names that are common Python imports or provide
    widely-needed functionality are "need-related". This is a crude classification
    for prototype purposes - the goal is to test the principle, not produce a
    perfect classifier.
    """
    name = module_name.lower()
    
    # Common "need-related" module names/patterns
    need_keywords = [
        "os", "sys", "json", "math", "random", "collections", "itertools",
        "functools", "operator", "abc", "pathlib", "typing", "dataclasses",
        "unittest", "argparse", "warnings", "logging", "copy", "pprint",
        "importlib", "inspect", "textwrap", "enum", "heapq", "bisect",
        "array", "weakref", "types", "functools", "contextlib",
        "select", "fcntl", "termios", "tty", "resource", "grp", "pwd",
        "crypt", "spwd", "ossaudiodev", "audioop", "wave", "aifc",
        "sunau", "sndhdr", "colorsys", "imghdr", "tarfile", "zipfile",
        "gzip", "bz2", "lzma", "zlib", "md5", "sha", "sha256",
    ]
    
    # Check if module name matches need-related keywords
    for kw in need_keywords:
        if kw == name or name.startswith(kw + ".") or kw in name:
            return "need-related"
    
    # Also check via the provider's modules - if the provider ships many modules,
    # it's likely a "need-related" distribution
    mods = provider_detail.get("modules", set())
    if mods and len(mods) > 10:
        # Distribution that ships many modules is likely widely-used/infrastructure
        return "need-related"
    
    return "random"


def resolve_and_classify(command_args):
    """Run a command, detect import errors, and classify using view-count principle."""
    print(f"Running: {' '.join(command_args)}")
    
    stdout, stderr, returncode = run_command(command_args)
    
    if stdout:
        print("STDOUT:")
        print(stdout)
    
    if stderr:
        print("STDERR:")
        print(stderr)
    
    # Extract module names from stderr (and stdout)
    modules = extract_module_names(stderr)
    if not modules:
        if returncode != 0:
            print(f"\nCommand exited with code {returncode}, but no import errors detected.")
        return returncode
    
    print(f"\nDetected import errors for modules: {', '.join(modules)}")
    print("\nResolving and classifying...")
    
    all_found = True
    for module in modules:
        # Resolve using pyprovides
        result = resolve_module(module, max_checks=500, verbose=False)
        
        if result["status"] == "found":
            # Get detailed provider info
            try:
                status, mods, detail = find_provider(module, max_checks=500)
                classification = classify_need_related(module, detail)
                
                dist_name = detail.get("canonical", result["distribution"])
                active = is_crate_active(detail)
                
                print(f"\n✓ {module} is provided by {dist_name}")
                print(f"  Classification: {classification}")
                print(f"  Active (has metadata): {active}")
                print(f"  Install: pip install {dist_name}")
                
            except ResolveError as e:
                print(f"\n✓ {module} is provided by {result['distribution']}")
                print(f"  Classification: {classify_need_related(module, result)}")
                print(f"  Install: pip install {result['distribution']}")
        elif result["status"] == "stdlib":
            print(f"\n✓ {module}: is in the Python standard library (no install needed)")
        else:
            print(f"\n✗ {module}: no provider found among top 500 PyPI distributions")
            all_found = False
    
    if all_found:
        print("\n✓ All import errors can be resolved with the suggested installs.")
    else:
        print("\n⚠ Some import errors could not be resolved.")
    
    return returncode


def main():
    parser = argparse.ArgumentParser(
        prog="pyprovides-classify",
        description="Prototype: detect import errors and classify using view-count principle",
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
    
    print(f"pyprovides-classify prototype")
    print("=" * 40)
    return resolve_and_classify(args.command)


if __name__ == "__main__":
    sys.exit(main())