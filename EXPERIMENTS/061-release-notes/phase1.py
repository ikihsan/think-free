"""E061 Phase 1: is there a discoverable "what changed" artifact for
popular PyPI packages' latest release?

Sample: a named candidate list of well-known packages (a judgment
sample, stated as such), ranked by *observed* last-month downloads
from pypistats.org, taking the top N.

Three artifacts are checked per package:
  a. a "Changelog" entry in the PyPI project_urls (JSON API)
  b. a CHANGELOG/RELEASES/HISTORY/NEWS file in the linked
     repository root (GitHub contents API)
  c. a non-trivial description on the latest PyPI release page
     (HTML scrape, best-effort: PyPI sometimes serves a bot
     challenge, which is recorded as "unknown" rather than "no")

A package is "silent" only when (a) and (b) are both absent and
(c) is absent-or-unknown. Raw responses are preserved under raw/.
"""

import json
import re
import sys
import time
import urllib.request
from pathlib import Path

CANDIDATES = [
    "requests", "urllib3", "botocore", "pip", "setuptools", "six",
    "certifi", "idna", "charset-normalizer", "PyYAML", "numpy", "pandas",
    "scipy", "matplotlib", "beautifulsoup4", "selenium", "python-dateutil",
    "pytz", "attrs", "packaging", "flask", "django", "fastapi", "uvicorn",
    "starlette", "pydantic", "sqlalchemy", "alembic", "celery", "redis",
    "psycopg2-binary", "pytest", "virtualenv", "wheel", "black", "mypy",
    "ruff", "pylint", "click", "rich", "typer", "jinja2", "werkzeug",
    "pygments", "tornado", "aiohttp", "httpx", "openai", "boto3",
    "google-auth", "protobuf", "pymongo", "lxml", "pillow",
    "scikit-learn", "ipython", "markdown", "jsonschema", "cffi",
]

RAW = Path("raw")
RAW.mkdir(exist_ok=True)


def get(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) think-free-release-notes-probe/0.1",
                    "Accept": "text/html,application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001 - recorded, retried
            if attempt == retries - 1:
                return json.dumps({"__error__": str(exc)})
            time.sleep(3)
    return "{}"


def cached(path, url, delay=0.4):
    path = Path(path)
    if not path.exists():
        path.write_text(get(url))
        time.sleep(delay)
    return path.read_text()


def pypistats(package):
    return json.loads(cached(RAW / f"stats-{package}.json",
                             f"https://pypistats.org/api/packages/{package}/recent"))


def pypi_meta(package):
    return json.loads(cached(RAW / f"pypi-{package}.json",
                             f"https://pypi.org/pypi/{package}/json"))


def repo_root_files(owner, repo):
    return json.loads(cached(RAW / f"gh-{owner}-{repo}.json",
                             f"https://api.github.com/repos/{owner}/{repo}/contents/",
                             delay=1.5))


def github_slug(meta):
    info = meta.get("info", {})
    urls = dict(info.get("project_urls") or {})
    if info.get("home_page"):
        urls["Home-page"] = info["home_page"]
    for value in urls.values():
        if not value:
            continue
        m = re.search(r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)/?$", value)
        if m:
            return m.group(1), m.group(2)
    return None


def changelog_url(meta):
    for key, value in (meta.get("info", {}).get("project_urls") or {}).items():
        if "changelog" in key.lower() or "changes" in key.lower():
            return value
    return None


def has_changelog_file(files):
    if isinstance(files, dict):  # error payload
        return False
    for entry in files:
        name = (entry.get("name") or "").lower()
        if re.match(r"^(changelog|changes|release|releasenotes|news|history)", name):
            if name.endswith((".md", ".rst", ".txt")) or "." not in name:
                return True
    return False


def release_description_present(package, version):
    """Best-effort: does the PyPI release page describe this release?

    Returns True / False / None (unknown, e.g. bot challenge).
    The release-history card for a version carries a version link and
    a meta line; a description, when present, is further body content
    of the same card.
    """
    html = get(f"https://pypi.org/project/{package}/{version}/")
    (RAW / f"release-{package}-{version}.html").write_text(html)
    if len(html) < 20000 or "Release history" not in html:
        return None  # challenge page or fetch failure
    card = re.search(
        r'<p class="release__version">\s*<a[^>]*>' + re.escape(version) + r"</a>(.{0,3000}?)</div>\s*<div class=\"release\">",
        html, re.S,
    )
    if not card:
        return None
    body = re.split(r'<p class="release__version">', card.group(1))[0]
    text = re.sub(r"<[^>]+>", " ", body)
    text = re.sub(r"\s+", " ", text).strip()
    # The meta line (date, file count) is always present; anything
    # beyond it is the release description.
    return len(text) > 220


def main():
    ranked = []
    for package in CANDIDATES:
        stats = pypistats(package)
        month = stats.get("data", {}).get("last_month")
        ranked.append([month or 0, package])
        print(f"{month or 0:>13,}  {package}", file=sys.stderr)
    ranked.sort(reverse=True)
    top = [p for _, p in ranked[:40]]
    (RAW / "ranked.json").write_text(json.dumps(ranked, indent=1))
    print("TOP40:", top, file=sys.stderr)

    rows = []
    for package in top:
        meta = pypi_meta(package)
        if "__error__" in meta:
            rows.append({"package": package, "error": meta["__error__"]})
            continue
        info = meta.get("info", {})
        version = info.get("version", "")
        slug = github_slug(meta)
        gh_files = repo_root_files(*slug) if slug else None
        rows.append({
            "package": package,
            "version": version,
            "month_downloads": next(m for m, p in ranked if p == package),
            "repo": "/".join(slug) if slug else None,
            "changelog_project_url": bool(changelog_url(meta)),
            "repo_changelog": has_changelog_file(gh_files) if gh_files is not None else None,
            "pypi_release_description": release_description_present(package, version),
        })
        row = rows[-1]
        row["silent"] = (
            not row["changelog_project_url"]
            and row["repo_changelog"] is not True
            and row["pypi_release_description"] is not True
        )
        print(package, version, row["changelog_project_url"],
              row["repo_changelog"], row["pypi_release_description"],
              "->", row["silent"], file=sys.stderr)
    out = Path("results-phase1.json")
    out.write_text(json.dumps(rows, indent=1))
    silent = [r for r in rows if r.get("silent")]
    print(f"\nsilent: {len(silent)} of {len(rows)}", file=sys.stderr)
    for r in silent:
        print(" ", r["package"], r["version"], file=sys.stderr)


if __name__ == "__main__":
    main()
