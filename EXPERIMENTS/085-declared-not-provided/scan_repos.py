"""E085 arm A: parse declared dependencies and extract imports from real repos.

Standard library only, Python 3.8. Writes repo-scan.json.

Declared dependencies come from requirements*.txt and setup.py install_requires.
Imports come from ast, so conditional and try/except imports are seen.
Dynamic imports (importlib.import_module, __import__) are not resolvable
statically and are a declared ceiling, not a zero.
"""

import ast
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.normpath(os.path.join(
    HERE, "..", "068-arxiv-spec-generator", "repos"))

REQ_NAMES = ("requirements.txt", "requirements_dev.txt", "requirements-test.txt")
SKIP_DIRS = {".git", "__pycache__", ".idea", "node_modules", ".mypy_cache", "build", "dist"}
# Lines that are directives, not dependency names.
DIRECTIVE = re.compile(r"^\s*(-|--|#|$)")


def stdlib_modules():
    """Top-level modules this interpreter ships, as a declared approximation.

    `pkgutil.iter_modules` over the stdlib path yields both single-file modules
    and package directories. A first version listed only files ending in
    `.py`/`.so`, which missed every standard-library *package* - `asyncio`,
    `json`, `logging`, `email`, `concurrent`, `unittest` - and therefore
    counted them as unprovided third-party imports. That inflated both the
    numerator and the denominator; it is instrumentation defect 2 in
    README.md.

    The corpus targets 3.6-3.10 and this VM runs 3.8, so a module added or
    removed between those versions is a declared limit on the stdlib arm.
    """
    import pkgutil
    import sysconfig
    lib = sysconfig.get_paths()["stdlib"]
    paths = [lib]
    dynload = os.path.join(lib, "lib-dynload")
    if os.path.isdir(dynload):
        # `resource`, `ssl`, `readline` and friends are built extensions that
        # live here, not in the stdlib directory.
        paths.append(dynload)
    mods = set(sys.builtin_module_names)
    for entry in paths:
        try:
            mods.update(name for _, name, _ in pkgutil.iter_modules([entry]))
        except OSError:
            pass
    return mods


def parse_requirements(path):
    """Distribution names from a requirements file, following -r includes."""
    names, unresolved = [], []
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        return names, ["unreadable: %s" % exc]
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or DIRECTIVE.match(raw):
            if line.startswith("-r"):
                target = line[2:].strip()
                if not os.path.isabs(target):
                    target = os.path.join(os.path.dirname(path), target)
                if os.path.exists(target):
                    more, bad = parse_requirements(target)
                    names += more
                    unresolved += bad
                else:
                    unresolved.append("missing include %s" % target)
            continue
        line = re.sub(r"\[[^\]]*\]", "", line)          # extras
        line = line.split(";")[0].strip()                # environment markers
        name = re.match(r"^([A-Za-z0-9._-]+)", line)
        if name:
            names.append(name.group(1))
        elif line:
            unresolved.append("unparsed: %s" % raw.strip()[:60])
    return names, unresolved


def setup_install_requires(path):
    """Distribution names from setup.py's install_requires, via ast when possible."""
    try:
        tree = ast.parse(open(path, encoding="utf-8", errors="replace").read())
    except (OSError, SyntaxError):
        return [], ["unparseable setup.py"]
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        label = getattr(func, "attr", None) or getattr(func, "id", None)
        if label not in ("setup", "install_requires"):
            continue
        for kw in node.keywords or []:
            if kw.arg not in ("install_requires", "requires", "deps"):
                continue
            try:
                for elt in ast.literal_eval(kw.value):
                    m = re.match(r"^([A-Za-z0-9._-]+)", str(elt))
                    if m:
                        found.append(m.group(1))
            except (ValueError, SyntaxError):
                continue
    return found, []


def extract_imports(root):
    """Top-level module names imported anywhere under root, with file counts."""
    counts = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            full = os.path.join(dirpath, fn)
            try:
                tree = ast.parse(open(full, encoding="utf-8", errors="replace").read())
            except (OSError, SyntaxError, ValueError, RecursionError):
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        counts[alias.name.split(".")[0]] = \
                            counts.get(alias.name.split(".")[0], 0) + 1
                elif isinstance(node, ast.ImportFrom):
                    if node.level:      # relative import: project-local
                        continue
                    if node.module:
                        top = node.module.split(".")[0]
                        counts[top] = counts.get(top, 0) + 1
    return counts


def scan_repo(path):
    declared, notes = [], []
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            if fn.startswith("requirements") and fn.endswith((".txt", ".in")):
                names, bad = parse_requirements(full)
                declared += names
                notes += ["%s: %s" % (fn, b) for b in bad]
            elif fn == "setup.py":
                names, bad = setup_install_requires(full)
                declared += names
                notes += ["setup.py: %s" % b for b in bad]
    imports = extract_imports(path)
    return {
        "repo": os.path.basename(path),
        "path": os.path.relpath(path, CORPUS),
        "declared": sorted(set(declared)),
        "n_declared_rows": len(declared),
        "imports": imports,
        "n_import_sites": sum(imports.values()),
        "n_top_level_imports": len(imports),
        "parse_notes": notes[:20],
    }


def project_local_modules_safe(repo_path):
    """Top-level names the repository defines itself, so not dependencies.

    Two shapes count. A directory holding `__init__.py` is a package. A
    directory holding any source file also counts, and so does a root-level
    compiled or cython file: a first version required `__init__.py` and so
    scored LPMP_BDD's own `BDD/` C-extension directory and NCO's vendored
    `LEHD/` tree as third-party imports. Because a PyPI project named `BDD`
    and one named `LEHD` both exist, both then scored as silent wrong-project
    findings. Instrumentation defect 3 in E085's README.md.
    """
    tops = set()
    for dirpath, dirnames, filenames in os.walk(repo_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for d in list(dirnames):
            inner_dir = os.path.join(dirpath, d)
            if not os.path.isdir(inner_dir):
                continue
            try:
                inner = os.listdir(inner_dir)
            except OSError:
                continue
            if any(f.endswith((".py", ".pyx", ".pxd", ".c", ".cpp", ".cc",
                               ".h", ".hpp", ".so", ".pyd")) for f in inner):
                tops.add(d)
        for fn in filenames:
            if fn.endswith(".py"):
                tops.add(fn[:-3])
            elif dirpath == repo_path and fn.endswith((".pyx", ".so", ".pyd")):
                tops.add(fn.rsplit(".", 1)[0])
    return tops


def main():
    std = stdlib_modules()
    repos = []
    for arm in sorted(os.listdir(CORPUS)):
        arm_dir = os.path.join(CORPUS, arm)
        if not os.path.isdir(arm_dir):
            continue
        for name in sorted(os.listdir(arm_dir)):
            full = os.path.join(arm_dir, name)
            if not os.path.isdir(full) or name.startswith("."):
                continue
            row = scan_repo(full)
            row["arm"] = arm
            repos.append(row)
            print("%-6s %-45s declared=%3d imports=%4d" % (
                arm, name, row["n_declared_rows"], row["n_top_level_imports"]))
    out = {
        "corpus": CORPUS,
        "stdlib_modules": len(std),
        "n_repos": len(repos),
        "repos": repos,
    }
    with open(os.path.join(HERE, "repo-scan.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    usable = [r for r in repos if r["declared"] and r["imports"]]
    print("\n%d repos; %d with both declarations and imports" % (len(repos), len(usable)))
    print("%d unique declared distributions" % len(
        {d for r in repos for d in r["declared"]}))


if __name__ == "__main__":
    sys.exit(main() or 0)