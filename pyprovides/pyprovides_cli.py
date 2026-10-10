#!/usr/bin/env python3
"""pyprovides command line: scan a project for shadowed dependencies, or ask
which distribution provides a module.

status: draft. Prototype, not a product. See ../README.md for what is measured
and what is not.
"""

import argparse
import json
import os
import sys

# Add the parent directory of pyprovides to sys.path so 'pyprovides' package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyprovides import __version__, provides, find_provider, ResolveError  # noqa: E402
from pyprovides.fix_import import (  # noqa: E402
    extract_module_names,
    resolve_module,
    run_command,
)

# SKIP_DIRS for the scan command - expanded to avoid common VCS and build dirs
CLI_SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", ".tox",
                 ".venv", "venv", "build", "dist", ".eggs", "site-packages",
                 ".mypy_cache", ".pytest_cache", ".idea", ".vscode",
                 "EXPERIMENTS", "sessions", ".pyprovides-cache", "docs",
                 "tests", "tools", "vendor", "RESEARCH", ".origin",
                 ".agents", ".claude", "stage-lines", "tasks", "vendor"}

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir, "EXPERIMENTS",
                                "085-declared-not-provided"))


def cmd_which(args):
    """Which distributions provide this module, from what is known locally."""
    try:
        status, mods, detail = provides(args.module)
    except ResolveError as exc:
        print("cannot resolve %r: %s" % (args.module, exc), file=sys.stderr)
        return 3
    if status == "no-such-project":
        print("%s: no distribution of that name exists on PyPI." % args.module)
        print("  pip will refuse the install, which is a loud and clear error.")
        return 1
    if status == "no-wheel":
        print("%s: a project of that name exists but publishes no wheel." % args.module)
        print("  %s" % detail.get("why", ""))
        return 1
    if args.module in mods:
        print("%s: provided by %s %s (it provides itself)" % (
            args.module, detail["canonical"], detail["version"]))
        return 0
    print("%s is NOT provided by the distribution named %s." % (
        args.module, detail["canonical"]))
    print("  %s %s ships: %s" % (detail["canonical"], detail["version"],
                                  ", ".join(sorted(mods)[:8]) or "(nothing importable)"))
    if detail["canonical"].lower().replace("-", "").replace("_", "") != \
            args.module.lower().replace("-", "").replace("_", ""):
        print("  These names differ, so this is the silent case: the install "
              "succeeds and the import fails later.")
    return 0


def cmd_find(args):
    """Find which distribution provides a module (query-time reverse lookup)."""
    try:
        status, matches, detail = find_provider(
            args.module,
            max_checks=args.max_checks,
            cache=not args.no_cache,
            cache_dir=args.cache_dir,
            timeout=args.timeout,
        )
    except ResolveError as exc:
        print("cannot resolve: %s" % exc, file=sys.stderr)
        return 3
    except Exception as exc:  # noqa: BLE001
        print("error during search: %s" % exc, file=sys.stderr)
        return 3

    method = detail.get("method", "unknown")
    
    if status == "found":
        dist_name, mods, prov_detail = matches[0]
        print("%s is provided by %s %s" % (args.module, prov_detail["canonical"], prov_detail["version"]))
        print("  method: %s" % method)
        print("  checked %d distributions in %.2fs" % (detail["checked"], detail["elapsed_seconds"]))
        print("  wheel: %s (%d bytes, fetched %d bytes)" % (
            prov_detail["wheel"], prov_detail["wheel_bytes"], prov_detail["bytes_fetched"]))
        if args.verbose:
            print("  also provides: %s" % ", ".join(sorted(mods)[:20]))
        return 0
    elif status == "stdlib":
        print("%s is in the Python standard library (no install needed)" % args.module)
        print("  method: stdlib (instant)")
        return 0
    else:
        print("%s: no provider found among top %d PyPI distributions" % (args.module, detail["checked"]))
        print("  method: %s" % method)
        print("  checked %d distributions in %.2fs" % (detail["checked"], detail["elapsed_seconds"]))
        return 1


def cmd_scan(args):
    from scan_repos import (extract_imports, parse_requirements,
                            project_local_modules_safe, setup_install_requires,
                            stdlib_modules)
    root = os.path.abspath(args.path)
    declared = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in CLI_SKIP_DIRS]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            if fn.startswith("requirements") and fn.endswith((".txt", ".in")):
                declared.update(parse_requirements(full)[0])
            elif fn == "setup.py":
                declared.update(setup_install_requires(full)[0])
    if not declared:
        print("no parseable declarations under %s" % root, file=sys.stderr)
        return 1
    imports = extract_imports(root)
    local = project_local_modules_safe(root)
    stdlib = stdlib_modules()
    covered, findings = set(), []
    for dist in sorted(declared):
        try:
            status, mods, _ = provides(dist)
        except ResolveError:
            continue
        if status == "ok":
            covered |= mods
    for module, sites in sorted(imports.items()):
        if module in covered or module in stdlib or module in local:
            continue
        try:
            status, mods, detail = provides(module)
        except ResolveError:
            continue
        if status == "ok" and module not in mods:
            findings.append((module, sites, detail, sorted(mods)))
    if args.json:
        print(json.dumps([{"module": m, "import_sites": s,
                           "distribution": d["canonical"], "version": d["version"],
                           "that_distribution_provides": mods}
                          for m, s, d, mods in findings], indent=1))
    else:
        if not findings:
            print("no shadowed dependency names found (%d declared, %d imports)"
                  % (len(declared), len(imports)))
        for module, sites, detail, mods in findings:
            print("%s is imported at %d site(s). The distribution named %s "
                  "exists and provides: %s"
                  % (module, sites, detail["canonical"],
                     ", ".join(mods[:6]) or "(nothing importable)"))
    return 1 if findings else 0


def cmd_fix_import(args):
    """Run a command, detect import errors, and suggest correct distributions."""
    if not args.command:
        print("fix-import: no command provided", file=sys.stderr)
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


def main(argv=None):
    p = argparse.ArgumentParser(prog="pyprovides", description=__doc__)
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd")
    w = sub.add_parser("which", help="which distribution provides this module")
    w.add_argument("module")
    w.set_defaults(func=cmd_which)
    f = sub.add_parser("find", help="find which distribution provides a module (query-time reverse lookup)")
    f.add_argument("module")
    f.add_argument("--max-checks", type=int, default=500, help="maximum distributions to check (default: 500)")
    f.add_argument("--no-cache", action="store_true", help="disable wheel metadata cache")
    f.add_argument("--cache-dir", default=os.environ.get("PYPROVIDES_CACHE", ".pyprovides-cache"))
    f.add_argument("--timeout", type=int, default=30, help="HTTP timeout per request (default: 30)")
    f.add_argument("--verbose", "-v", action="store_true", help="show all modules the provider ships")
    f.set_defaults(func=cmd_find)
    s = sub.add_parser("scan", help="scan a project for shadowed dependency names")
    s.add_argument("path", nargs="?", default=".")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_scan)
    fi = sub.add_parser("fix-import", help="run a command, detect import errors, and suggest correct distributions")
    fi.add_argument("--max-checks", type=int, default=500, help="maximum distributions to check per module (default: 500)")
    fi.add_argument("--verbose", "-v", action="store_true", help="show detailed resolution info")
    fi.add_argument("--dry-run", action="store_true", help="show what would be done without running the command")
    fi.add_argument("command", nargs=argparse.REMAINDER, help="command to run (e.g., -- python3 -c \"import sklearn\")")
    fi.set_defaults(func=cmd_fix_import)
    args = p.parse_args(argv)
    if not getattr(args, "func", None):
        p.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())