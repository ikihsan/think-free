#!/usr/bin/env python3
"""E069 static arm: do the pins E068 generated admit the interpreter it resolved for?

E068's PROTOCOL.md declares "Resolution assumes target Python 3.10 (median of
A1 repos)" and resolves every pin to the latest stable version it finds on
PyPI. This asks the metadata E068 already downloaded whether the pin it chose
can actually be installed on 3.10: a release's own `requires_python` is the
package author's statement of which interpreters it supports.

The answer is about the pins, not about any repository, so it needs no
virtualenv, no install, and no network beyond the cached metadata.

Requires-Python handling is deliberately explicit and says so. The parser
below understands the forms that actually occur in the cached metadata —
`>=`, `>`, `<=`, `<`, `==`, `!=X.Y.*`, `~=` and a bare version — and refuses to
guess about anything else. A pin whose constraint this parser cannot read is
counted `unparsed` and **never** counted as compatible, so the reported share
of excluded pins is a floor, not a ceiling.

A second, separate defect is counted: a pin naming a version that PyPI lists
with **zero downloadable files**. pip cannot install that either, and the two
defects have different causes, so they are not pooled.
"""

import glob
import json
import os
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
CACHE = BASE.parent / "068-arxiv-spec-generator" / "cache"
TARGET = (3, 10)          # E068's declared resolution target, PROTOCOL.md
PYPI_CACHE = CACHE / "pypi"
OUT = BASE / "pin_compatibility.json"

# Forms this file decides. Anything else is `unparsed`, never "ok".
COMPARISON = re.compile(r"^\s*(>=|==|!=|~=|<=|>|<)\s*(\d+)(?:\.(\d+))?(\.\*)?\s*$")
BARE = re.compile(r"^\s*(\d+)(?:\.(\d+))?\s*$")


def _satisfies(op, spec_minor):
    """Would TARGET satisfy one comparison clause, given only major.minor?"""
    spec = (TARGET[0], spec_minor)
    got = TARGET
    return {
        ">=": spec <= got,
        ">": spec < got,
        "<=": spec >= got,
        "<": spec > got,
        "==": spec == got,
        # ~=X.Y means >=X.Y and ==X.*, i.e. the same minor line.
        "~=": spec <= got and spec[0] == got[0],
    }[op]


def parse_target(text):
    """Return (verdict, note). verdict is 'admits', 'excludes' or 'unparsed'."""
    text = (text or "").strip()
    if not text or text == "*":
        return "admits", "no requires_python"
    verdicts = []
    for part in [p.strip() for p in text.split(",") if p.strip()]:
        match = COMPARISON.match(part)
        if match:
            op, major, minor, wildcard = match.groups()
            minor = int(minor) if minor is not None else 0
            if op == "!=":
                if wildcard or (minor is not None):
                    # Excludes a version range; only decisive if it covers TARGET.
                    excluded = (TARGET[0], minor)
                    if excluded == (TARGET[0], TARGET[1]):
                        verdicts.append(False)
                        continue
                    verdicts.append(True)
                    continue
                verdicts.append(True)
                continue
            verdicts.append(bool(_satisfies(op, minor)))
            continue
        match = BARE.match(part)
        if match:
            verdicts.append(int(match.group(1)) == TARGET[0])
            continue
        return "unparsed", text
    ok = all(verdicts)
    return ("admits" if ok else "excludes"), text


def main():
    pins = {}
    for source in ("generation_results.json",):
        data = json.loads((CACHE / source).read_text())
        for repo in data["a1_repos"] + data["test_repos"]:
            for line in repo["packages"]:
                if "==" not in line:
                    continue
                pkg, ver = line.split("==", 1)
                pins.setdefault(pkg, set()).add(ver)

    cached = {}
    for path in glob.glob(str(PYPI_CACHE / "*.json")):
        cached[os.path.basename(path)[:-5]] = json.loads(Path(path).read_text())

    rows = []
    for pkg, versions in sorted(pins.items()):
        data = cached.get(pkg)
        if data is None:
            rows.append({"package": pkg, "versions": sorted(versions),
                         "status": "no_cached_metadata"})
            continue
        for ver in sorted(versions):
            releases = data.get("releases", {})
            if ver not in releases:
                rows.append({"package": pkg, "version": ver,
                             "status": "version_absent_from_cached_metadata"})
                continue
            files = releases[ver]
            if not files:
                # PyPI lists the version with no downloadable file: every upload
                # was yanked or removed. pip cannot install this pin.
                rows.append({"package": pkg, "version": ver,
                             "status": "version_has_no_downloadable_file",
                             "n_releases_listed": len(releases)})
                continue
            verdicts = [parse_target(f.get("requires_python")) for f in files]
            names = {v for v, _ in verdicts}
            if "excludes" in names and names <= {"excludes", "unparsed"}:
                status = "excluded_by_every_file"
            elif names == {"admits"}:
                status = "admits"
            else:
                status = "unparsed_or_mixed"
            rows.append({
                "package": pkg, "version": ver, "status": status,
                "requires_python": sorted({(f.get("requires_python") or "") for f in files}),
                "files": len(files),
                "targets": TARGET,
            })

    INSTALL_BLOCKING = ("excluded_by_every_file", "version_has_no_downloadable_file",
                    "version_absent_from_cached_metadata")
    decided = [r for r in rows if r["status"] in ("admits",) + INSTALL_BLOCKING]
    excluded = [r for r in rows if r["status"] == "excluded_by_every_file"]
    undownloadable = [r for r in rows if r["status"] in
                      ("version_has_no_downloadable_file", "version_absent_from_cached_metadata")]
    unparsed = [r for r in rows if r["status"] in ("unparsed_or_mixed", "no_cached_metadata")]
    blocking = [r for r in rows if r["status"] in INSTALL_BLOCKING]

    per_repo = {}
    gen = json.loads((CACHE / "generation_results.json").read_text())
    status_by_pin = {(r["package"], r.get("version")): r["status"] for r in rows}
    for repo in gen["test_repos"]:
        key = "%s/%s" % (repo["owner"], repo["repo"])
        verdicts = []
        for line in repo["packages"]:
            if "==" not in line:
                continue
            verdicts.append((line, status_by_pin.get(tuple(line.split("==", 1)))))
        bad = [l for l, s in verdicts if s == "excluded_by_every_file"]
        nodl = [l for l, s in verdicts if s in ("version_has_no_downloadable_file",
                                               "version_absent_from_cached_metadata")]
        per_repo[key] = {
            "arm": repo["arm"], "pins": len(repo["packages"]),
            "pins_excluded_from_target": len(bad),
            "pins_with_no_downloadable_file": len(nodl),
            "pins_blocking_install": len(bad) + len(nodl),
            "pins_unparsed": sum(1 for _, s in verdicts if s == "unparsed_or_mixed"),
            # A floor: unparsed pins are not assumed installable.
            "spec_installable_on_target": len(bad) + len(nodl) == 0,
            "examples_excluded": bad[:5],
            "examples_no_file": nodl[:5],
        }

    installable = [k for k, v in per_repo.items() if v["spec_installable_on_target"]]
    # A second, separate defect, on the *name* rather than the version: a pin
    # that resolves to a real project which has nothing to do with the import it
    # came from. Distribution size is the cheapest available proxy for "this is
    # not the library the code means" — numpy and torch are hundreds of MB,
    # `modules` and `idx` are placeholders under 1 KB. It is a proxy, not proof:
    # the threshold is declared here so a reader can disagree with 20 KB rather
    # than with an unstated judgement.
    SMALL_BYTES = 20 * 1024
    tiny = []
    for pkg, versions in sorted(pins.items()):
        doc = cached.get(pkg)
        if not doc:
            continue
        for ver in sorted(versions):
            sizes = [f.get("size") for f in (doc.get("releases", {}).get(ver) or [])
                     if f.get("size")]
            if sizes and max(sizes) < SMALL_BYTES:
                tiny.append({"package": pkg, "version": ver,
                             "largest_file_bytes": max(sizes)})
    result = {
        "question": "do E068's pins admit the Python 3.10 it resolved against?",
        "target": list(TARGET),
        "metadata_source": "EXPERIMENTS/068-arxiv-spec-generator/cache/pypi/*.json",
        "metadata_packages_cached": len(cached),
        "pins_total": sum(len(v) for v in pins.values()),
        "pins_decided": len(decided),
        "pins_excluded_from_target": len(excluded),
        "pins_with_no_downloadable_file": len(undownloadable),
        "pins_blocking_install": len(blocking),
        "pins_unparsed_not_counted_as_installable": len(unparsed),
        "share_blocking_of_decided": (round(len(blocking) / len(decided), 4) if decided else None),
        "share_excluded_of_decided": (round(len(excluded) / len(decided), 4) if decided else None),
        "interpretation_note": (
            "share_blocking_of_decided is a floor: a pin this parser cannot read is "
            "counted neither blocking nor compatible"),
        "per_pin": rows,
        "per_repo": per_repo,
        "near_miss_names": {
            "question": ("how many pins name a project whose pinned release is "
                         "under %d bytes - a name collision, not the intended library" % SMALL_BYTES),
            "threshold_bytes": SMALL_BYTES,
            "rule": "largest distribution file for the pinned version",
            "pins_total": len(pins),
            "count": len(tiny),
            "share": round(len(tiny) / len(pins), 4) if pins else None,
            "examples": tiny[:20],
        },
        "generated_specs_installable_on_target": len(installable),
        "generated_specs_installable_list": installable,
    }
    OUT.write_text(json.dumps(result, indent=1))
    print("pins total %d, decided %d" % (result["pins_total"], len(decided)))
    print("  excluded from Python %d.%d by their own metadata: %d (%.1f%% of decided)" % (
        TARGET[0], TARGET[1], len(excluded),
        100.0 * result["share_excluded_of_decided"] if decided else 0))
    print("  version listed with no downloadable file: %d" % len(undownloadable))
    print("  pins blocking install (floor): %d (%.1f%% of decided)" % (
        len(blocking), 100.0 * result["share_blocking_of_decided"] if decided else 0))
    print("  unparsed, not counted as installable: %d" % len(unparsed))
    print("generated specs with no blocking pin: %d of %d" % (len(installable), len(per_repo)))
    nm = result["near_miss_names"]
    print("pins naming a project under %d bytes: %d of %d (%.1f%%)" % (
        nm["threshold_bytes"], nm["count"], nm["pins_total"], 100.0 * nm["share"]))
    print()
    for key, row in sorted(per_repo.items()):
        print("  %-50s %-3s %3d pins, %2d excluded, %2d no-file, %2d unparsed  %s" % (
            key, row["arm"], row["pins"], row["pins_excluded_from_target"],
            row["pins_with_no_downloadable_file"], row["pins_unparsed"],
            "no blocking pin" if row["spec_installable_on_target"] else "BLOCKED"))
    print("\nwrote %s" % OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())