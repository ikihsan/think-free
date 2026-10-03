"""Building one source repeatedly, and comparing the artifacts.

Split from `attribute.py` so each file stays under the repository's line cap:
this module knows how to produce artifacts, `attribute.py` knows how to judge
them. The gate itself lives in `attribute.py` and was predeclared in README.md.

Standard library only. Nothing here simulates a builder: the builds are real
`setup.py bdist_wheel` invocations of the toolchain installed on this machine,
in two real configurations (`SOURCE_DATE_EPOCH` set and unset).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tarfile
import time

import zipdiff

# Two checkout mtimes, far apart so a builder that copies mtimes is unmistakable,
# and both well after the 1980 DOS epoch.
STAMP_A = 1614834367  # 2021-03-04T05:06:07Z
STAMP_B = 1731394150  # 2024-11-12T08:09:10Z
EPOCH_H = 1600000000  # arm H's fixed SOURCE_DATE_EPOCH

# Each label is one checkout. A and A2 share a stamp, B and B2 share the other,
# and C differs from A only by one planted file, so the noise floor, the
# timestamp effect and the detector's blind spot are three separate comparisons.
CHECKOUTS = (
    ("A", STAMP_A, False), ("A2", STAMP_A, False),
    ("B", STAMP_B, False), ("B2", STAMP_B, False),
    ("C", STAMP_A, True),
)

PAIRS = {
    "noise_floor_same_mtime": ("N:A", "N:A2"),
    "arm_n_different_mtime": ("N:A", "N:B"),
    "arm_n_repeat_b": ("N:B", "N:B2"),
    "arm_h_different_mtime": ("H:A", "H:B"),
    "planted_content_defect": ("N:A", "N:C"),
}


def plant_content_defect(tree: str, entries: list[str]) -> dict:
    """Change the content of a file the wheel demonstrably contains.

    The first run planted `src/__planted__.txt`, which no `setup.py` here
    packages, so the "planted" artifact was identical to its control except for
    wall-clock stamps and the control proved nothing. Planting inside a file a
    real build already put in the wheel cannot miss for that reason.

    A wheel entry name is not always a path in the sdist: `click` ships
    `click/__init__.py` from a `src/` layout, so both forms are tried and the
    plant lands in whichever exists.
    """
    def locate(name: str) -> str | None:
        for prefix in ("", "src/"):
            candidate = os.path.join(tree, prefix + name)
            if os.path.isfile(candidate):
                return prefix + name
        return None

    ordered = sorted(entries, key=lambda n: (not n.endswith(".py"), n))
    for name in ordered:
        relative = locate(name)
        if relative is None:
            continue
        path = os.path.join(tree, relative)
        with open(path, "a", encoding="utf-8") as handle:
            handle.write("\n# planted defect for the attribution control (T-0017)\n")
        return {"file": relative, "wheel_entry": name,
                "bytes_added": os.path.getsize(path)}
    raise ValueError("no packaged file is also present in the tree")


def set_mtimes(root: str, stamp: int) -> None:
    """Give every path in the tree the same mtime.

    Directories too: the wheel builder reads file mtimes, but a directory's own
    mtime changes as extraction writes into it, and leaving it alone would make
    two otherwise identical trees differ for a reason that has nothing to do
    with the builder.
    """
    for base, _dirs, files in os.walk(root, topdown=False):
        for name in files:
            os.utime(os.path.join(base, name), (stamp, stamp))
        os.utime(base, (stamp, stamp))
    os.utime(root, (stamp, stamp))


def extract(sdist: str, workdir: str, stamp: int) -> str:
    """Extract one sdist into `workdir` with every mtime set to `stamp`.

    The tarball is third-party input and this runs without a sandbox, so member
    names are checked rather than trusted, and ownership is reset: a build must
    not depend on the uid the archive happened to record.
    """
    if os.path.exists(workdir):
        shutil.rmtree(workdir)
    os.makedirs(workdir)
    with tarfile.open(sdist) as archive:
        members = archive.getmembers()
        for member in members:
            if member.name.startswith("/") or ".." in member.name.split("/"):
                raise ValueError(f"unsafe member {member.name!r}")
            if not (member.isfile() or member.isdir()):
                raise ValueError(f"refusing non-regular member {member.name!r}")
            member.uid = member.gid = 0
            member.uname = member.gname = "root"
        archive.extractall(workdir)
    roots = [n for n in os.listdir(workdir) if os.path.isdir(os.path.join(workdir, n))]
    if len(roots) != 1:
        raise ValueError(f"expected one top-level directory, found {roots}")
    tree = os.path.join(workdir, roots[0])
    set_mtimes(tree, stamp)
    return tree


def tree_digest(tree: str) -> str:
    """Content hash of a whole tree, mtimes excluded.

    This is what makes "identical source bytes" a measurement rather than an
    assumption: two checkouts of a source must differ in mtime and must not
    differ in content, and the planted checkout must differ in content.
    """
    import hashlib

    digest = hashlib.sha256()
    for base, dirs, files in os.walk(tree):
        dirs.sort()
        for name in sorted(files):
            path = os.path.join(base, name)
            digest.update(os.path.relpath(path, tree).encode())
            with open(path, "rb") as handle:
                digest.update(handle.read())
    return digest.hexdigest()


def build(tree: str, epoch, workdir: str) -> dict:
    """Run `setup.py bdist_wheel` on a fresh copy of `tree` at a fixed path.

    The stage path is fixed across every build on purpose: a builder that
    embedded an absolute path would otherwise register as a cause of
    nondeterminism that is really an artefact of the harness. `epoch=None` means
    the variable is absent from the environment, not set to zero.
    """
    env = dict(os.environ)
    env.pop("SOURCE_DATE_EPOCH", None)
    if epoch is not None:
        env["SOURCE_DATE_EPOCH"] = str(epoch)
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    stage = os.path.join(workdir, "stage")
    if os.path.exists(stage):
        shutil.rmtree(stage)
    shutil.copytree(tree, stage)
    started = time.time()
    done = subprocess.run(
        [sys.executable, "setup.py", "--quiet", "bdist_wheel"],
        cwd=stage, env=env, capture_output=True, text=True, timeout=600,
    )
    wheels = []
    dist = os.path.join(stage, "dist")
    if os.path.isdir(dist):
        wheels = sorted(n for n in os.listdir(dist) if n.endswith(".whl"))
    row = {
        "arm": "H" if epoch is not None else "N",
        "source_date_epoch": epoch,
        "returncode": done.returncode,
        "wheel": wheels[0] if wheels else None,
        "duration_s": round(time.time() - started, 2),
        "stderr_tail": done.stderr.strip().splitlines()[-3:],
    }
    if wheels:
        with open(os.path.join(dist, wheels[0]), "rb") as handle:
            row["artifact"] = handle.read()
        row["bytes"] = len(row["artifact"])
    shutil.rmtree(stage, ignore_errors=True)
    return row


def compare(left: dict, right: dict) -> dict:
    """Attribute a pair of builds, then try the causal patch.

    `patch_identical` is the load-bearing field: True means timestamps were
    provably the only difference, because rewriting them reproduced the other
    artifact byte for byte.
    """
    a, b = left["artifact"], right["artifact"]
    diff = zipdiff.attribute(a, b)
    patched = zipdiff.patch(a, zipdiff.read_stamps(b))
    diff["patch_identical"] = patched == b
    diff["patched_sha256"] = zipdiff._digest(patched)
    after = zipdiff.attribute(patched, b)
    diff["residual_causes_after_patch"] = zipdiff.residual_causes(after, after)
    for key in ("left_entries", "right_entries", "positions"):
        diff.pop(key, None)
    return diff


def half_controls(left: dict, right: dict) -> dict:
    """C1 and C2: patching one header half must not reach byte-identity.

    If either reached it, the attribution could not localise a cause and a
    "timestamps are the only difference" result would mean nothing.
    """
    a, b = left["artifact"], right["artifact"]
    stamps = zipdiff.read_stamps(b)
    return {
        "local_header_only_reaches_identity":
            zipdiff.patch(a, stamps, halves=("local",)) == b,
        "central_directory_only_reaches_identity":
            zipdiff.patch(a, stamps, halves=("central",)) == b,
    }


def run_source(source: dict, workdir: str, sdists: str) -> dict:
    """Every build and comparison for one source.

    Order matters once: checkout C is built last, after build `N:A` has shown
    which files a real wheel contains, because the planted defect has to land in
    a packaged file for the control to test anything.
    """
    sdist = os.path.join(sdists, source["file"])
    slot = os.path.join(workdir, source["package"])
    os.makedirs(slot, exist_ok=True)
    trees = {
        label: extract(sdist, os.path.join(slot, label), stamp)
        for label, stamp in (("A", STAMP_A), ("A2", STAMP_A), ("B", STAMP_B),
                             ("B2", STAMP_B), ("C", STAMP_A))
    }

    builds = {f"N:{label}": build(trees[label], None, slot)
              for label in ("A", "A2", "B", "B2")}
    builds.update({f"H:{label}": build(trees[label], EPOCH_H, slot)
                   for label in ("A", "B")})
    built = {key: row for key, row in builds.items() if row["wheel"]}

    plant = {"file": None, "bytes_added": 0}
    if "N:A" in built:
        entries = [row["name"] for row in zipdiff._entries(built["N:A"]["artifact"])]
        plant = plant_content_defect(trees["C"], entries)
        set_mtimes(trees["C"], STAMP_A)  # planting changed one file's mtime
    builds["N:C"] = build(trees["C"], None, slot)
    if builds["N:C"]["wheel"]:
        built["N:C"] = builds["N:C"]

    digests = {label: tree_digest(tree) for label, tree in trees.items()}
    comparisons = {}
    for name, (left_key, right_key) in PAIRS.items():
        if left_key not in built or right_key not in built:
            comparisons[name] = {"error": f"build missing: {left_key} or {right_key}"}
            continue
        result = compare(built[left_key], built[right_key])
        if name == "arm_n_different_mtime":
            result["half_controls"] = half_controls(built[left_key], built[right_key])
        comparisons[name] = result

    row = {
        "package": source["package"],
        "version": source["version"],
        "sdist_sha256": source["sha256"],
        "content_digests": digests,
        "checkouts_identical_in_content": digests["A"] == digests["B"],
        "planted": plant,
        "planted_differs_in_content": digests["A"] != digests["C"],
        "built_ok": len(built) == len(builds),
        "builds": {
            key: {k: v for k, v in row.items() if k != "artifact"}
            for key, row in builds.items()
        },
        "comparisons": comparisons,
    }
    shutil.rmtree(slot, ignore_errors=True)
    return row