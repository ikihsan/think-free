"""Package collection for the E118 PyPI matched-harvest experiment.

Split out of `classify.py` at the repository's 300-line cap. This module
owns the PyPI JSON fetch and the curated package lists that build the
matched-harvest pool.
"""

import json
import urllib.request
import urllib.parse


def fetch_pypi_package(name):
    """Fetch package metadata from PyPI JSON API for a given package name."""
    url = f"https://pypi.org/pypi/{urllib.parse.quote(name)}/json"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "E118-MatchedHarvest/1.0", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        print(f"    Failed {name}: {e}")
        return None


def collect_packages():
    """Fetch the curated need-related and random package lists from PyPI.

    Returns the deduplicated package list in harvest order, which is the
    order the classifier and every downstream count depend on.
    """
    # Pre-curated list of PyPI packages spanning need-related and random categories
    # These are real packages fetched from PyPI during experiment runtime
    curated_need = [
        "django", "flask", "fastapi", "pyramid", "bottle", "aiohttp",
        "sqlalchemy", "django-rest-framework", "wtforms",
        "pytest", "coverage", "sphinx", "mkdocs", "jupyter",
        "requests", "httpx", "urllib3", "jinja2", "marshmallow",
        "pydantic", "black", "flake8", "mypy", "pytest-cov",
    ]
    curated_random = [
        "numpy", "pandas", "pyyaml", "cffi", "cython", "greenlet",
        "chardet", "beautifulsoup4", "lxml", "html5lib",
        "markdown", "python-dateutil", "ptyprocess", "six",
        "unittest", "wheel", "setuptools", "virtualenv",
    ]

    print("[1] Fetching packages from PyPI...")
    all_packages = []
    seen_names = set()

    print("  Fetching need-related candidates...")
    for name in curated_need:
        pkg_data = fetch_pypi_package(name)
        if pkg_data is None:
            all_packages.append({
                "name": name,
                "description": "",
                "recent_downloads": 0,
                "_source": "need_query",
                "_query": "curated",
            })
            seen_names.add(name)
            continue
        info = pkg_data.get("info", {})
        desc = info.get("summary", "") or ""
        recent = 0
        urls = pkg_data.get("urls", [])
        if urls:
            first_url = urls[0]
            first_downloads = first_url.get("downloads", {})
            if isinstance(first_downloads, dict):
                recent = first_downloads.get("recent", 0) if first_downloads else 0
            else:
                try:
                    recent = int(first_downloads) if first_downloads else 0
                except (ValueError, TypeError):
                    recent = 0
        all_packages.append({
            "name": name,
            "description": desc,
            "recent_downloads": recent,
            "_source": "need_query",
            "_query": "curated",
        })
        seen_names.add(name)
        if len(all_packages) >= 200:
            break

    print("  Fetching random packages...")
    if len(all_packages) < 200:
        for name in curated_random:
            pkg_data = fetch_pypi_package(name)
            if pkg_data is None:
                all_packages.append({
                    "name": name,
                    "description": "",
                    "recent_downloads": 0,
                    "_source": "random",
                })
                seen_names.add(name)
                continue
            info = pkg_data.get("info", {})
            desc = info.get("summary", "") or ""
            recent = 0
            urls = pkg_data.get("urls", [])
            if urls:
                first_url = urls[0]
                first_downloads = first_url.get("downloads", {})
                if isinstance(first_downloads, dict):
                    recent = first_downloads.get("recent", 0) if first_downloads else 0
                else:
                    try:
                        recent = int(first_downloads) if first_downloads else 0
                    except (ValueError, TypeError):
                        recent = 0
            all_packages.append({
                "name": name,
                "description": desc,
                "recent_downloads": recent,
                "_source": "random",
            })
            seen_names.add(name)
            if len(all_packages) >= 200:
                break
    return all_packages
