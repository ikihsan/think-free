#!/usr/bin/env python3
"""E175: failure report -> artifact -> tracker repository, deterministically.

Stdlib only, no model, no search engine. Written and committed before the sample
was drawn (see PROTOCOL.md). Every HTTP request and its response is written to
raw/ so the derivation can be re-read without re-running it.
"""
import json
import os
import re
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-e175/1.0"

# --- ecosystem list: fixed before the draw, 40 names (PROTOCOL.md step 1) ---
ECOSYSTEMS = [
    "python", "pypi", "pip", "conda", "node", "npm", "nodejs", "django",
    "flask", "react", "vue", "angular", "docker", "kubernetes", "postgres",
    "postgresql", "mysql", "sqlite", "redis", "nginx", "apache", "java",
    "spring", "kotlin", "swift", "xcode", "macos", "windows", "linux", "ubuntu",
    "debian", "chrome", "firefox", "safari", "vscode", "vim", "emacs", "gcc",
    "clang", "maven", "gradle",
]
# Ecosystem -> the registry to ask. None means "no registry publishes a tracker
# for this name", so the row cannot be resolved mechanically.
REGISTRY = {
    "python": "pypi", "pypi": "pypi", "pip": "pypi", "conda": "pypi",
    "django": "pypi", "flask": "pypi", "numpy": "pypi", "pandas": "pypi",
    "requests": "pypi", "setuptools": "pypi", "matplotlib": "pypi",
    "node": "npm", "npm": "npm", "nodejs": "npm", "react": "npm", "vue": "npm",
    "angular": "npm", "typescript": "npm", "webpack": "npm", "eslint": "npm",
}

_STOP = set("""a an the and or but if then than that this these those it its is are
was were be been being do does did have has had i me my we our you your he him his
she her they them their what which who when where why how all any both each more
most other some such no nor not only own same so too very can will just should
now for from with without about into over under out up down off at as of on in
""".split())

_GH = re.compile(r"github\.com[:/]+([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?(?:[#/\s)\"'<]|$)")
_NODE_MODULES = re.compile(r"node_modules/(@?[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)?)")
_PY_FRAME = re.compile(r'File "([^"]+\.py)"')
_DOTTED = re.compile(r"\b([a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+)\b")
_BACKTICK = re.compile(r"`([^`]{2,60})`")
_NAMED_VER = re.compile(r"\b([A-Za-z][A-Za-z0-9_.-]{1,40})[@ ]v?(\d+\.\d+(?:\.\d+)?)")
# PyPI names are the most common mechanically resolvable artifact, so the
# backtick and body sweep collects plausible names and asks PyPI about each.
_PYPI_NAME = re.compile(r"\b([a-z][a-z0-9]*(?:[-_][a-z0-9]+)+)\b")


def get(url, timeout=25, tries=3):
    """(status, body, error). Every call is logged to raw/http.jsonl."""
    os.makedirs(RAW, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    last = None
    for _ in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as fh:
                body = fh.read().decode("utf-8", "replace")
                rec = {"url": url, "status": fh.status, "bytes": len(body)}
                _log(rec)
                return fh.status, body, None
        except urllib.error.HTTPError as exc:
            rec = {"url": url, "status": exc.code, "error": "http_%d" % exc.code}
            _log(rec)
            return exc.code, None, rec["error"]
        except Exception as exc:                                   # noqa: BLE001
            last = "%s: %s" % (type(exc).__name__, exc)
            time.sleep(2)
    rec = {"url": url, "status": None, "error": last}
    _log(rec)
    return None, None, last


def _log(rec):
    with open(os.path.join(RAW, "http.jsonl"), "a") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")


def gh_repo(text):
    m = _GH.search(text or "")
    if not m:
        return None
    return "%s/%s" % (m.group(1).lower(), m.group(2).lower())


def artifacts(row):
    """Ordered, de-duplicated candidate artifact names from the report only."""
    text = "\n".join([row.get("title") or "", row.get("body") or ""])
    tags = [t.lower().replace("-", "") for t in (row.get("tags") or [])]
    out = []

    def add(name):
        n = (name or "").strip().lower()
        if 1 < len(n) <= 60 and n not in out and n not in _STOP:
            out.append(n)

    for m in _NODE_MODULES.finditer(text):
        add(m.group(1).split("/")[-1])
    for m in _NAMED_VER.finditer(text):
        add(m.group(1))
    for m in _PY_FRAME.finditer(text):
        tail = os.path.basename(m.group(1))[:-3]
        add(tail)
    for t in tags:
        add(t)
        for e in ECOSYSTEMS:
            if e in t and e not in out:
                out.append(e)
    for m in _BACKTICK.finditer(text):
        tok = m.group(1).strip()
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]{1,40}", tok):
            add(tok)
        else:
            for d in _DOTTED.findall(tok):
                add(d.split(".")[0])
    for m in _PYPI_NAME.finditer(text):
        add(m.group(1))
    return out


def pypi_repo(name):
    status, body, err = get("https://pypi.org/pypi/%s/json" % name)
    if status != 200 or not body:
        return None, err
    try:
        info = json.loads(body).get("info") or {}
    except ValueError:
        return None, "bad_json"
    urls = info.get("project_urls") or {}
    preferred = [k for k in urls
                 if k.lower() in ("bug tracker", "bug reports", "tracker",
                                  "issue tracker", "issues", "source", "source code",
                                  "code", "repository", "github", "homepage")]
    for key in preferred + sorted(urls):
        repo = gh_repo(urls.get(key))
        if repo:
            return repo, None
    for key in ("home_page", "package_url", "download_url"):
        repo = gh_repo(info.get(key))
        if repo:
            return repo, None
    return None, "no_github_url"


def npm_repo(name):
    for suffix in ("", "/latest"):
        status, body, err = get("https://registry.npmjs.org/%s%s" % (name, suffix))
        if status != 200 or not body:
            continue
        try:
            data = json.loads(body)
        except ValueError:
            continue
        repo = gh_repo(json.dumps(data.get("repository") or ""))
        if repo:
            return repo, None
    return None, "no_github_url"


def crates_repo(name):
    status, body, err = get("https://crates.io/api/v1/crates/%s" % name)
    if status != 200 or not body:
        return None, err
    try:
        repo = gh_repo(json.dumps(json.loads(body).get("crate") or {}))
    except ValueError:
        repo = None
    return (repo, None) if repo else (None, "no_github_url")


LOOKUP = {"pypi": pypi_repo, "npm": npm_repo, "crates": crates_repo}


def derive(row, log=None):
    """The derived repository for one report, or None. No guessing."""
    names = artifacts(row)
    tried = []
    for name in names:
        reg = REGISTRY.get(name)
        if not reg:
            continue
        repo, err = LOOKUP[reg](name)
        tried.append({"name": name, "registry": reg, "repo": repo, "error": err})
        if log is not None:
            log.append(tried[-1])
        if repo:
            return repo, tried
    return None, tried