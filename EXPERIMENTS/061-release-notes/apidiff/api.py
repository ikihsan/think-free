"""API extraction from Python source for apidiff."""

from __future__ import annotations

import ast


def _signature(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> dict:
    args = fn.args
    positional = [a.arg for a in list(args.posonlyargs) + list(args.args)]
    defaults = list(args.defaults)
    n_default = len(defaults)
    required = positional[: len(positional) - n_default]
    optional = positional[len(positional) - n_default :]
    kwonly = [a.arg for a in args.kwonlyargs]
    kwonly_required = [
        a.arg for a, d in zip(args.kwonlyargs, args.kw_defaults) if d is None
    ]
    return {
        "required": required,
        "optional": optional,
        "kwonly_required": kwonly_required,
        "kwonly_optional": sorted(set(kwonly) - set(kwonly_required)),
        "varargs": bool(args.vararg or args.kwarg),
    }


def _is_public(name: str) -> bool:
    return not name.startswith("_")


def extract_api(source: str) -> dict:
    """The public API of one module: {qualified_name: record}."""
    tree = ast.parse(source)
    exported: set[str] | None = None
    api: dict[str, dict] = {}

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    try:
                        exported = set(ast.literal_eval(node.value))
                    except (ValueError, TypeError):
                        exported = set()
    uses_all = exported is not None

    def record_function(node, qual: str, owner: str | None = None) -> None:
        if not _is_public(node.name):
            return
        api[qual] = {
            "kind": "method" if owner else "function",
            "signature": _signature(node),
            "async": isinstance(node, ast.AsyncFunctionDef),
            "decorated": [
                d.id if isinstance(d, ast.Name) else ast.dump(d)[:40]
                for d in node.decorator_list
            ],
        }

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            record_function(node, node.name)
        elif isinstance(node, ast.ClassDef):
            if not _is_public(node.name):
                continue
            api[node.name] = {
                "kind": "class",
                "bases": [ast.dump(b)[:60] for b in node.bases],
            }
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    record_function(sub, f"{node.name}.{sub.name}", owner=node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and _is_public(target.id):
                    api[target.id] = {"kind": "constant"}
        elif isinstance(node, ast.AnnAssign) and isinstance(
            node.target, ast.Name
        ):
            if _is_public(node.target.id):
                api[node.target.id] = {"kind": "constant"}
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                name = alias.asname or alias.name
                if _is_public(name):
                    api[name] = {"kind": "reexport", "from": node.module}

    if uses_all:
        for name in list(api):
            if name not in exported:
                api[name]["publicity"] = "not-in-__all__"
    return api


def package_api(modules: dict[str, str]) -> dict:
    """{qualified_name: record} across a package's modules."""
    api: dict[str, dict] = {}
    for module, source in sorted(modules.items()):
        try:
            module_api = extract_api(source)
        except SyntaxError:
            continue
        for name, record in module_api.items():
            api[f"{module}.{name}"] = record
    return api