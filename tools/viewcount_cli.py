"""E103+ — View-count principle CLI prototype v3.

Search a package registry for need-related packages using the view-count
principle: need-related packages have systematically higher activity metadata
(description + version) than random packages.

Usage:
    python3 tools/viewcount_cli.py <keyword> [--top N] [--registry pypi]

    python3 tools/viewcount_cli.py --list-keywords
"""
import argparse
import json
import os
import sys
import time

from viewcount_prototype import run_prototype  # v3 prototype entry point


# ---------------------------------------------------------------------------
# Prototype entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="View-count principle prototype v3: find need-related packages"
    )
    parser.add_argument("keyword", nargs="?", help="Search keyword or need description")
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top results to display (default: 10)",
    )
    parser.add_argument(
        "--registry",
        choices=["pypi"],
        default="pypi",
        help="Package registry to search (default: pypi)",
    )
    parser.add_argument(
        "--list-keywords",
        action="store_true",
        help="List example search keywords from past experiments",
    )
    args = parser.parse_args()

    if args.list_keywords:
        print("Example keywords from prior experiments:")
        for kw in [
            "database", "cache", "auth", "security", "logging",
            "monitoring", "testing", "benchmark", "performance", "api",
        ]:
            print(f"  - {kw}")
        return

    if not args.keyword:
        parser.print_usage()
        print(
            "\nEnter a keyword/need description to search for relevant packages.\n"
            "The tool classifies packages as 'need-related' (have a need indicator "
            "in their description) or 'random' and reports active/metadata status."
        )
        return

    keyword = args.keyword
    print(f"=== View-count prototype v3: searching '{keyword}' ===\n")

    results = run_prototype(keyword, max_results=200, top_n=args.top)


if __name__ == "__main__":
    main()