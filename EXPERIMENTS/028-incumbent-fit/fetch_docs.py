#!/usr/bin/env python3
"""Store each named incumbent's own published documentation into raw/docs/.

Amendment 1's fetch table. Two rules learned in this repository's own record
are implemented here:

  * A capture holding text is never overwritten by a later failure (F041: a
    retry loop overwrote five good captures with refusals, unrecoverably).
  * A refusal is written beside the capture, never in place of it, and never
    into a zero-length file that a later reader would read as "no documentation
    exists" rather than "we did not get it".
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "raw", "docs")
CAPTURE = CAPTURE_PATH = os.path.join(HERE, "raw", "fetch_log.jsonl")
UA = "think-free-e028/1 (+mission experiment; contact via repository)"
CAP_CHARS = 12000
DELAY = 0.35


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return resp.getcode(), raw.decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, ""
    except Exception as exc:                                  # noqa: BLE001
        return None, "%s: %s" % (type(exc).__name__, exc)


def strip_html(text):
    text = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", text)
    text = re.sub(r"(?s)<!--.*?-->", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;?", " ", text)
    text = re.sub(r"&amp;?", "&", text)
    text = re.sub(r"&lt;?", "<", text)
    text = re.sub(r"&gt;?", ">", text)
    text = re.sub(r"&quot;?", '"', text)
    return re.sub(r"[ \t]+", " ", text)


def store(slug, text):
    """Write the capture once. Never overwrite a non-empty capture.

    An empty capture is never written, and an empty file left by an earlier
    version is removed rather than left to be read as "this product's
    documentation says nothing". HTTP 200 with a body that strips to nothing is
    a refusal, not a capture, and a later reader must see the difference.
    """
    path = os.path.join(DOCS, slug + ".txt")
    if not text.strip():
        if os.path.exists(path) and os.path.getsize(path) == 0:
            os.remove(path)
        return path, 0, "not_stored_empty"
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path, os.path.getsize(path), "already_stored"
    body = text[:CAP_CHARS]
    with open(path, "w") as fh:
        fh.write(body)
    return path, len(body), "stored"


def fetch_github(repo):
    for branch in ("HEAD", "master", "main"):
        for name in ("README.md", "readme.md", "README.rst", "README.txt"):
            url = "https://raw.githubusercontent.com/%s/%s/%s" % (repo, branch,
                                                                  name)
            code, text = get(url)
            time.sleep(DELAY)
            if code == 200 and text.strip():
                return url, code, text, "github %s/%s" % (branch, name)
    return None, None, "", "github: no README at HEAD/master/main"


REGISTRY_ENDPOINTS = {
    "pypi": "https://pypi.org/pypi/%s/json",
    "npm": "https://registry.npmjs.org/%s",
    "crates.io": "https://crates.io/api/v1/crates/%s",
}


def fetch_registry(label):
    """`label` is E016's own recorded string, e.g. `sharp (npm, 436,835,441 dl/mo)`."""
    m = re.match(r"^\s*([^(\s]+)\s*\(([^,)]+)", label)
    if not m:
        return None, None, "", "registry: unparseable label %r" % label
    name, registry = m.group(1), m.group(2).strip()
    for key, tmpl in REGISTRY_ENDPOINTS.items():
        if key in registry:
            url = tmpl % name
            code, text = get(url)
            time.sleep(DELAY)
            if code == 200 and text.strip():
                try:
                    doc = json.loads(text)
                except ValueError:
                    return url, code, text, "registry %s: body not json" % key
                if key == "pypi":
                    info = doc.get("info", {})
                    parts = [str(info.get(k) or "") for k in
                             ("summary", "description", "home_page")]
                    urls = (info.get("project_urls") or {}).values()
                elif key == "npm":
                    parts = [str(doc.get(k) or "") for k in
                             ("description", "readme", "homepage")]
                    urls = [doc.get("homepage") or ""]
                else:
                    crate = doc.get("crate") or {}
                    parts = [str(crate.get(k) or "") for k in
                             ("description", "documentation", "homepage")]
                    urls = [crate.get("homepage") or "",
                            crate.get("documentation") or ""]
                body = "\n\n".join(p for p in parts if p)
                body += "\n\nLinks: " + "\n".join(str(u) for u in urls)
                return url, code, body, "registry %s metadata + description" % key
            return url, code, "", "registry %s: http %s" % (key, code)
    return None, None, "", "registry: unknown registry %r" % registry


DOMAIN = re.compile(r"(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}(?:/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]*)?")


def url_from_label(label):
    """Recover the URL E016 recorded, without inventing one.

    E016's `openweb` entries are three shapes: a bare domain, a domain with a
    path, and a product name followed by a domain in parentheses. The first two
    are URLs; the third names the product and cites where it is documented, and
    the cited domain is the best primary text available. If nothing in the
    string is a domain, nothing is stored and the reason says so.
    """
    text = label.strip()
    first = text.split()[0] if text.split() else ""
    if re.match(r"^[a-z]+://", first):
        return first
    if re.match(r"^(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}", first):
        return "https://" + first
    domains = DOMAIN.findall(text)
    if domains:
        return "https://" + max(domains, key=len)
    return None


def fetch_openweb(label):
    url = url_from_label(label)
    if url is None:
        return None, None, "", ("openweb: no domain in the recorded label "
                                "(%r); no documentation stored" % label)
    code, text = get(url)
    time.sleep(DELAY)
    if code == 200 and text.strip():
        return url, code, strip_html(text), "openweb page text"
    return url, code, "", "openweb: http %s for %s" % (code, url)


def slug_for(row, corpus, artifact):
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", artifact)[:80]
    return "%s__%s__%s" % (row, corpus.replace(".", ""), safe)


def main():
    os.makedirs(DOCS, exist_ok=True)
    incumbents = [json.loads(l) for l in open(
        os.path.join(HERE, "raw", "incumbents.jsonl"))]
    seen = set()
    log = []
    if os.path.exists(CAPTURE):
        for line in open(CAPTURE):
            if line.strip():
                rec = json.loads(line)
                # Only a capture holding text blocks a retry. A refusal is
                # retried, and the refusal stays in the log beside the answer.
                if rec.get("has_text"):
                    seen.add((rec["row"], rec["corpus"], rec["artifact"]))
    fresh = 0
    for bundle in incumbents:
        row = bundle["row"]
        for entry in bundle["artifacts"]:
            key = (row, entry["corpus"], entry["artifact"])
            if key in seen:
                continue
            corpus, artifact = entry["corpus"], entry["artifact"]
            if corpus == "github":
                url, code, text, how = fetch_github(artifact)
            elif corpus == "registries":
                url, code, text, how = fetch_registry(artifact)
            else:
                url, code, text, how = fetch_openweb(artifact)
            slug = slug_for(row, corpus, artifact)
            path, chars, state = store(slug, text)
            rec = {"row": row, "corpus": corpus, "artifact": artifact,
                   "url": url, "http": code, "how": how, "path": path,
                   "chars": chars, "store": state,
                   "has_text": state in ("stored", "already_stored")}
            with open(CAPTURE, "a") as fh:
                fh.write(json.dumps(rec, sort_keys=True) + "\n")
            seen.add(key)
            fresh += 1
    log_rows = []
    for line in open(CAPTURE):
        if line.strip():
            log_rows.append(json.loads(line))
    best = {}
    for rec in log_rows:
        key = (rec["row"], rec["corpus"], rec["artifact"])
        if key not in best or (rec["has_text"]
                               and not best[key]["has_text"]):
            best[key] = rec
    log_rows = list(best.values())
    got = [r for r in log_rows if r["has_text"]]
    rows_with_text = {r["row"] for r in got}
    rows = sorted({r["row"] for r in log_rows})
    print(json.dumps({
        "artifacts_attempted": len(log_rows),
        "artifacts_with_stored_text": len(got),
        "artifacts_without_text": len(log_rows) - len(got),
        "rows_with_at_least_one_stored_doc": len(rows_with_text),
        "rows_with_no_stored_doc": sorted(set(rows) - rows_with_text),
        "by_corpus_with_text": {c: sum(1 for r in got if r["corpus"] == c)
                                for c in sorted({r["corpus"]
                                                 for r in log_rows})},
        "freshly_fetched_this_run": fresh,
    }, indent=2))


if __name__ == "__main__":
    main()