"""CLI entry point for apidiff."""

from __future__ import annotations

import json
import sys

from . import sdist
from . import api
from . import diff


def diff_versions(package: str, old_version: str, new_version: str) -> dict:
    meta = sdist.pypi_json(package)
    result = {"package": package, "from": old_version, "to": new_version}
    apis = {}
    for version in (old_version, new_version):
        url = sdist.sdist_url(meta, version)
        if url is None:
            result["error"] = f"no sdist for {version}"
            return result
        modules = sdist.sdist_modules(sdist.fetch(url))
        result[f"modules_{version}"] = len(modules)
        apis[version] = api.package_api(modules)
    changes = diff.diff_api(apis[old_version], apis[new_version])
    result["changes"] = changes
    result["breaking"] = [c for c in changes if c["breaking"]]
    return result


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        print(__doc__.splitlines()[1])
        print("usage: apidiff.py PACKAGE OLD_VERSION NEW_VERSION [--json]")
        return 1
    package, old_version, new_version = argv[1], argv[2], argv[3]
    as_json = "--json" in argv
    result = diff_versions(package, old_version, new_version)
    if "error" in result:
        print(f"apidiff: {result['error']}", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps(result, indent=1))
        return 0
    breaking = result.pop("breaking")
    print(f"{package} {old_version} -> {new_version}: "
          f"{len(result['changes'])} public API change(s), "
          f"{len(breaking)} breaking")
    for change in result["changes"]:
        flag = "BREAKING " if change["breaking"] else "         "
        print(f"  {flag}{change['change']:<12} {change['name']}")
        if change["detail"]:
            print(f"             {change['detail']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))