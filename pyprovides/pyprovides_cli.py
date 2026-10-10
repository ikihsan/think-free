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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pyprovides import __version__, provides, ResolveError  # noqa: E402

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


def cmd_scan(args):
    from scan_repos import (extract_imports, parse_requirements,
                            project_local_modules_safe, setup_install_requires,
                            SKIP_DIRS, stdlib_modules)
    root = os.path.abspath(args.path)
    declared = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
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


def main(argv=None):
    p = argparse.ArgumentParser(prog="pyprovides", description=__doc__)
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd")
    w = sub.add_parser("which", help="which distribution provides this module")
    w.add_argument("module")
    w.set_defaults(func=cmd_which)
    s = sub.add_parser("scan", help="scan a project for shadowed dependency names")
    s.add_argument("path", nargs="?", default=".")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_scan)
    args = p.parse_args(argv)
    if not getattr(args, "func", None):
        p.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())