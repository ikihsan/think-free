#!/usr/bin/env python3
"""pyprovides - which distribution provides this module, with nothing installed.

The mechanism this rests on was built and measured in
EXPERIMENTS/085-declared-not-provided. This is a prototype: the resolver's
mechanism and its correctness are observed; its usefulness to anyone is not.

A wheel is a zip file, and a zip's central directory sits at the end of the
file and names every entry. So the full list of modules a distribution ships
can be read with two HTTP Range requests and zero payload bytes. Nothing is
downloaded and nothing is installed, which is the gap this fills: deptry
0.25.1 resolves imports against an installed virtualenv and reports nothing
at all when the project is uninstalled.

Standard library only. Python 3.8+.
"""

import json
import os
import struct
import sys
import time
import urllib.error
import urllib.request

__version__ = "0.1.0"

USER_AGENT = "pyprovides/%s" % __version__
EOCD_SIG = b"PK\x05\x06"
CD_SIG = b"PK\x01\x02"
TAIL_BYTES = 65536
CODE_EXT = (".py", ".pyi", ".pyd", ".so", ".dll", ".dylib")
CACHE_DIR = os.environ.get("PYPROVIDES_CACHE", ".pyprovides-cache")


class ResolveError(Exception):
    """The distribution could not be resolved. Never means 'provides nothing'."""


def _get(url, headers=None, timeout=30):
    req = urllib.request.Request(
        url, headers=dict({"User-Agent": USER_AGENT}, **(headers or {})))
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(), resp.headers


def _cache_path(name, cache_dir=CACHE_DIR):
    safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in name)
    return os.path.join(cache_dir, safe + ".json")


def _read_cache(name, cache_dir=CACHE_DIR):
    path = _cache_path(name, cache_dir)
    if not os.path.exists(path):
        return None
    try:
        with open(path) as fh:
            return json.load(fh)
    except ValueError:
        return None


def _write_cache(name, row, cache_dir=CACHE_DIR):
    os.makedirs(cache_dir, exist_ok=True)
    with open(_cache_path(name, cache_dir), "w") as fh:
        json.dump(row, fh, indent=1, sort_keys=True)


def pypi(name, timeout=30):
    """(exists, payload). exists is False only on PyPI's own 404."""
    try:
        body, _ = _get("https://pypi.org/pypi/%s/json" % name, timeout=timeout)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False, None
        raise ResolveError("PyPI returned %s for %r" % (exc.code, name))
    return True, json.loads(body)


def _central_directory(url, size, timeout=30):
    """The wheel's zip central directory, fetched without the payload."""
    window = min(TAIL_BYTES, int(size))
    tail, headers = _get(url, headers={"Range": "bytes=-%d" % window},
                         timeout=timeout)
    content_range = headers.get("Content-Range", "")
    if not content_range:
        total, base = len(tail), 0        # server ignored Range: whole file
    else:
        total = int(content_range.split("/")[-1])
        base = total - len(tail)
    idx = tail.rfind(EOCD_SIG)
    if idx < 0 or idx + 22 > len(tail):
        raise ResolveError("no zip central directory in %s" % url)
    cd_size, cd_off = struct.unpack("<II", tail[idx + 12:idx + 20])
    if cd_off < base:
        body, _ = _get(url, headers={"Range": "bytes=%d-%d"
                                     % (cd_off, cd_off + cd_size - 1)},
                       timeout=timeout)
        return total, body
    return total, tail[cd_off - base:cd_off - base + cd_size]


def entry_names(cd_bytes):
    """Every filename in a zip central directory."""
    out, pos, n = [], 0, len(cd_bytes)
    while pos + 46 <= n:
        if cd_bytes[pos:pos + 4] != CD_SIG:
            nxt = cd_bytes.find(CD_SIG, pos + 1)
            if nxt < 0:
                break
            pos = nxt
            continue
        name_len, extra_len, comment_len = struct.unpack(
            "<HHH", cd_bytes[pos + 28:pos + 34])
        start = pos + 46
        out.append(cd_bytes[start:start + name_len].decode("utf-8", "replace"))
        pos = start + name_len + extra_len + comment_len
    return out


def top_level_modules(names):
    """Top-level importable names a wheel provides, from entry names alone.

    Known limit: a distribution can make a module importable with a `.pth`
    redirector without shipping a file for it, and a central directory cannot
    see that. `pynvml` 13.0.1 does exactly this and still imports cleanly.
    """
    tops = set()
    for raw in names:
        path = raw.replace("\\", "/").lstrip("/")
        parts = path.split("/")
        # A wheel's payload may be re-rooted under `<name>-<version>.data/`.
        # `purelib`/`platlib` hold code; `scripts`, `headers`, `data` do not.
        for i, part in enumerate(parts[:-1]):
            if part.endswith(".data"):
                rest = parts[i + 1:]
                if rest and rest[0] in ("purelib", "platlib"):
                    parts = rest[1:]
                else:
                    parts = []
                break
        if not parts:
            continue
        if any(p.endswith(".dist-info") for p in parts[:-1]):
            continue
        if len(parts) == 1:
            stem, ext = os.path.splitext(parts[0])
            if ext.lower() in CODE_EXT:
                tops.add(stem)
            continue
        top = parts[0]
        if top and "." not in top:
            tops.add(top)
    return tops


def _pick_wheel(payload):
    wheels = [u for u in payload.get("urls", [])
              if u.get("packagetype") == "bdist_wheel"]
    if not wheels:
        return None
    for u in wheels:
        if u["filename"].endswith("-py3-none-any.whl") or \
           u["filename"].endswith("-py2.py3-none-any.whl"):
            return u
    return min(wheels, key=lambda u: u.get("size", 0))


def provides(distribution, cache=True, cache_dir=CACHE_DIR, timeout=30):
    """Top-level modules a PyPI distribution provides.

    Returns (status, set_of_modules, detail). status is 'ok', 'no-such-project'
    or 'no-wheel'. 'no-such-project' and 'no-wheel' are answers about the
    *registry*, never about what the distribution provides.
    """
    if cache:
        hit = _read_cache(distribution, cache_dir)
        if hit:
            return hit["status"], set(hit["modules"]), hit["detail"]
    exists, payload = pypi(distribution, timeout=timeout)
    if not exists:
        return "no-such-project", set(), {"why": "PyPI has no project by that name"}
    wheel = _pick_wheel(payload)
    if wheel is None:
        return "no-wheel", set(), {
            "why": "project publishes no wheel; its install behaviour is not in the metadata",
            "canonical": payload["info"]["name"],
        }
    total, cd = _central_directory(wheel["url"], wheel.get("size"), timeout=timeout)
    mods = top_level_modules(entry_names(cd))
    detail = {
        "canonical": payload["info"]["name"],
        "version": payload["info"]["version"],
        "wheel": wheel["filename"],
        "wheel_bytes": total,
        "bytes_fetched": min(TAIL_BYTES, int(wheel.get("size") or TAIL_BYTES)),
    }
    if cache:
        _write_cache(distribution, {"status": "ok", "modules": sorted(mods),
                                    "detail": detail}, cache_dir)
    return "ok", mods, detail