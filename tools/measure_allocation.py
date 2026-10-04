#!/usr/bin/env python3
"""Measure how the repository's own work divides between measuring the world
and maintaining the machinery that records measurements.

Priced the drift recorded in `FAILURES.md` F025, in the same spirit and with the
same shape as `tools/sweep_unlogged_data.py`: one committed script so a reader can
re-run the number rather than trust it.

It reads git history and the working tree. It measures *effort proxies* — commits
by zone, and lines of code by zone — and it cannot observe intent, time, or
whether a session was productive. Those limits are stated in the output, because a
ratio of lines is not a measure of value.

Usage:
    tools/measure_allocation.py [--ref REF] [--since DATE] [--json]

Exit codes: 0 ok, 1 usage error, 3 git could not be read.
"""
import argparse
import json
import os
import re
import subprocess
import sys

# A commit "touches the world" if it changes a file under EXPERIMENTS/ — the only
# zone whose contents are a measurement of something outside this repository.
WORLD_PREFIXES = ("EXPERIMENTS/",)
MACHINERY_PREFIXES = ("tools/", "tests/", ".github/")
PROSE_PREFIXES = ("docs/",)


def git(args, cwd):
    p = subprocess.run(["git"] + args, cwd=cwd, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    if p.returncode != 0:
        sys.stderr.write(p.stderr.decode("utf-8", "replace"))
        raise SystemExit(3)
    return p.stdout.decode("utf-8", "replace")


def commits_by_zone(ref, since):
    """Return {date: {zone: count}} and totals, from `git log --name-only`."""
    args = ["log", "--format=COMMIT|%ad", "--date=short", "--name-only", ref]
    if since:
        args.append("--since=" + since)
    zones = {"world": 0, "machinery": 0, "prose": 0}
    per_day = {}
    day = None
    files = set()

    def flush():
        if day is None:
            return
        row = per_day.setdefault(day, {"commits": 0, "world": 0,
                                       "machinery": 0, "prose": 0})
        row["commits"] += 1
        for name, prefixes in (("world", WORLD_PREFIXES),
                               ("machinery", MACHINERY_PREFIXES),
                               ("prose", PROSE_PREFIXES)):
            if any(f.startswith(pfx) for f in files for pfx in prefixes):
                zones[name] += 1
                row[name] += 1

    for line in git(args, os.getcwd()).splitlines():
        if line.startswith("COMMIT|"):
            flush()
            day = line.split("|", 1)[1]
            files = set()
        elif line.strip():
            files.add(line.strip())
    flush()
    return zones, per_day


def lines_by_zone():
    """Count lines of Python in the machinery and experiment zones."""
    def count(roots, suffixes=(".py",)):
        total, files = 0, 0
        for root in roots:
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = [d for d in dirnames if d != "__pycache__"]
                for name in filenames:
                    if not name.endswith(suffixes):
                        continue
                    path = os.path.join(dirpath, name)
                    try:
                        with open(path, encoding="utf-8",
                                  errors="replace") as fh:
                            total += sum(1 for _ in fh)
                        files += 1
                    except (IOError, OSError):
                        pass
        return total, files

    mach, mach_files = count(["tools", "tests"])
    world, world_files = count(["EXPERIMENTS"])
    return (mach, mach_files), (world, world_files)


def findings_split():
    """Count findings whose subject is the world against the record itself."""
    world_subjects = re.compile(
        r"photo|sidewalk|knitting|ventilation|timestamp|lockfile|"
        r"appliance|accessib|artifact|reproduc", re.I)
    rows = []
    try:
        text = open("FAILURES.md", encoding="utf-8").read()
    except (IOError, OSError):
        return rows
    for line in text.splitlines():
        m = re.match(r"\|\s*(F\d{3})\s*\|\s*(.+?)\s*\|", line)
        if m:
            rows.append((m.group(1), m.group(2),
                         bool(world_subjects.search(m.group(2)))))
    return rows


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--ref", default="origin/research/origin")
    ap.add_argument("--since", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.ref:
        sys.stderr.write("usage: measure_allocation.py [--ref REF] [--json]\n")
        return 1

    try:
        zones, per_day = commits_by_zone(args.ref, args.since)
    except SystemExit:
        return 3
    total = sum(r["commits"] for r in per_day.values())
    (mach, mach_files), (world, world_files) = lines_by_zone()
    findings = findings_split()

    data = {
        "ref": args.ref,
        "total_commits": total,
        "commits_by_zone": zones,
        "per_day": per_day,
        "lines": {
            "machinery": {"lines": mach, "files": mach_files},
            "experiment_code": {"lines": world, "files": world_files},
            "ratio_machinery_to_experiment": (
                round(mach / float(world), 2) if world else None),
        },
        "findings": {
            "total": len(findings),
            "about_the_world": sum(1 for _, _, w in findings if w),
        },
    }

    if args.json:
        print(json.dumps(data, indent=1, sort_keys=True))
        return 0

    print("Allocation of work, measured from git and the tree.")
    print("ref=%s  total commits=%d\n" % (args.ref, total))
    print("%-26s %6s %8s" % ("zone (commit touches)", "commits", "share"))
    for name in ("world", "machinery", "prose"):
        n = zones[name]
        print("%-26s %6d %7.1f%%" % (
            "EXPERIMENTS/" if name == "world" else
            "tools|tests|.github" if name == "machinery" else "docs",
            n, 100.0 * n / total if total else 0.0))
    print()
    print("%-12s %8s %8s %8s %8s" % ("day", "commits", "world", "machin", "share"))
    for day in sorted(per_day):
        r = per_day[day]
        print("%-12s %8d %8d %8d %7.1f%%" % (
            day, r["commits"], r["world"], r["machinery"],
            100.0 * r["world"] / r["commits"] if r["commits"] else 0.0))
    print()
    print("%-26s %6s %8s" % ("zone (lines of Python)", "files", "lines"))
    print("%-26s %6d %8d" % ("tools/ + tests/", mach_files, mach))
    print("%-26s %6d %8d" % ("EXPERIMENTS/", world_files, world))
    if world:
        print("%-26s %6s %8s" % ("ratio machinery:experiment",
                                  "", "%.1f:1" % (mach / float(world))))
    print()
    print("findings about the world: %d of %d" % (
        data["findings"]["about_the_world"], data["findings"]["total"]))
    print()
    print("Limits: commits and lines are effort proxies, not measures of value.")
    print("A zone can be large because it is load-bearing (session and task")
    print("logging, without which no measurement is attributable) and a")
    print("commit can be cheap. This script cannot observe intent or time.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
