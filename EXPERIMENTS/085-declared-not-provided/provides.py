"""E085 instrument: what top-level modules does a PyPI distribution provide?

Read from the wheel's zip *central directory* only, fetched with HTTP Range.
No payload byte is downloaded and nothing is installed.

A zip's End-Of-Central-Directory record sits at the very end of the file and
names the offset and size of the central directory; the central directory
names every entry. Entry names are wheel paths like `requests/adapters.py`, so
the top-level module is the first path component.

Standard library only. Python 3.8.
"""

import json
import os
import struct
import urllib.error
import urllib.request

USER_AGENT = "think-free-e085/1.0 (+https://github.com/ikihsan/think-free)"
CACHE_DIR = "cache"
EOCD_SIG = b"PK\x05\x06"
CD_SIG = b"PK\x01\x02"
TAIL_BYTES = 65536


def _get(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers=dict({"User-Agent": USER_AGENT}, **(headers or {})))
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(), resp.headers


def pypi_json(name, timeout=30):
    """Return (exists, info_dict). exists is False only on a 404 from PyPI."""
    try:
        body, _ = _get("https://pypi.org/pypi/%s/json" % name, timeout=timeout)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False, None
        raise
    return True, json.loads(body)


def _eocd(tail):
    """Locate the End-Of-Central-Directory record inside the fetched tail."""
    idx = tail.rfind(EOCD_SIG)
    if idx < 0:
        return None
    # fixed part is 22 bytes; comment length follows at offset 20.
    if idx + 22 > len(tail):
        return None
    cd_size, cd_off = struct.unpack("<II", tail[idx + 12:idx + 20])
    return cd_size, cd_off


def _central_directory(url, size=None, timeout=30):
    """Return (total_size, central_directory_bytes) for a remote zip.

    A Range window larger than the file answers 416, so the window is clamped
    to the size PyPI already told us in the JSON payload.
    """
    window = TAIL_BYTES if not size else min(TAIL_BYTES, int(size))
    tail, headers = _get(url, headers={"Range": "bytes=-%d" % window}, timeout=timeout)
    cr = headers.get("Content-Range", "")
    if not cr:
        # Server ignored Range: we hold the whole file.
        return len(tail), tail
    total = int(cr.split("/")[-1])
    found = _eocd(tail)
    if found is None:
        return None, None
    cd_size, cd_off = found
    if cd_off >= len(tail):
        # Central directory starts before the window: fetch exactly it.
        body, _ = _get(
            url,
            headers={"Range": "bytes=%d-%d" % (cd_off, cd_off + cd_size - 1)},
            timeout=timeout,
        )
        return total, body
    # Range held: tail covers absolute bytes [total-len(tail), total).
    start = cd_off - (total - len(tail))
    return total, tail[start:start + cd_size]


def entry_names(cd_bytes):
    """Yield every filename in a zip central directory."""
    out = []
    pos = 0
    n = len(cd_bytes)
    while pos + 46 <= n:
        if cd_bytes[pos:pos + 4] != CD_SIG:
            # Directory entries are not sorted; resync on the next signature.
            nxt = cd_bytes.find(CD_SIG, pos + 1)
            if nxt < 0:
                break
            pos = nxt
            continue
        name_len, extra_len, comment_len = struct.unpack("<HHH", cd_bytes[pos + 28:pos + 34])
        start = pos + 46
        out.append(cd_bytes[start:start + name_len].decode("utf-8", "replace"))
        pos = start + name_len + extra_len + comment_len
    return out


CODE_EXT = (".py", ".pyi", ".pyd", ".so", ".dll", ".dylib")


def top_level_modules(names):
    """Top-level importable names a wheel provides, from entry names alone.

    Wheel entries are paths. `pkg/mod.py` and root-level `mod.py` both provide
    the top-level module `pkg` / `mod`; `.dist-info` provides nothing, and a
    `.data/purelib` prefix is stripped because it re-roots the payload.
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
                parts = rest[1:] if rest and rest[0] in ("purelib", "platlib") else []
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


def window_of(wheel):
    """Bytes actually fetched for a wheel: the tail window, clamped to its size."""
    return min(TAIL_BYTES, int(wheel.get("size") or TAIL_BYTES))


def pick_wheel(info, prefer_pure=True):
    urls = [u for u in info.get("urls", []) if u.get("packagetype") == "bdist_wheel"]
    if not urls:
        return None
    if prefer_pure:
        for u in urls:
            if u["filename"].endswith("-py3-none-any.whl") or u["filename"].endswith("-py2.py3-none-any.whl"):
                return u
    # Otherwise the smallest wheel available: smallest central-directory work.
    return min(urls, key=lambda u: u.get("size", 0))


def provides(distribution, timeout=30):
    """Return (status, set_of_top_level_modules, detail).

    status is one of: 'ok', 'no-pypi-record', 'no-wheel', 'unreadable'.
    'no-pypi-record' and 'unreadable' are missing observations, never 'the
    distribution provides nothing' (D082).
    """
    exists, info = pypi_json(distribution, timeout=timeout)
    if not exists:
        return "no-pypi-record", set(), {"why": "404"}
    wheel = pick_wheel(info)
    if wheel is None:
        return "no-wheel", set(), {"why": "sdist-only", "name": info["info"]["name"]}
    total, cd = _central_directory(wheel["url"], size=wheel.get("size"), timeout=timeout)
    if not cd:
        return "unreadable", set(), {"why": "no central directory", "file": wheel["filename"]}
    mods = top_level_modules(entry_names(cd))
    return "ok", mods, {
        "canonical": info["info"]["name"],
        "version": info["info"]["version"],
        "file": wheel["filename"],
        "size": wheel.get("size"),
        "central_directory_bytes": len(cd),
        "wheel_bytes": total,
        "downloaded_bytes": window_of(wheel),
    }