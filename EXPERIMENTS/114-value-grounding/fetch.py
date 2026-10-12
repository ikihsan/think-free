#!/usr/bin/env python3
"""Fetch the E114 population: US Federal Register final rules, plain text.

Standard library only. Writes raw/manifest.jsonl and raw/text/<docnum>.txt.
An empty or non-text body is recorded as a refusal, never as a capture.
"""
import gzip
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

UA = "think-free-research/1.0 (open-source invention mission; contact: repository owner)"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
TXT = os.path.join(RAW, "text")

API = ("https://www.federalregister.gov/api/v1/documents.json"
       "?per_page=100&order=newest&conditions[type]=RULE"
       "&conditions[publication_date][gte]=2025-06-01"
       "&fields[]=document_number&fields[]=title&fields[]=raw_text_url"
       "&fields[]=publication_date&fields[]=effective_on&fields[]=agencies"
       "&fields[]=cfr_references&fields[]=docket_ids&fields[]=page_length"
       "&fields[]=abstract&fields[]=html_url")


def get(url, tries=3):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                       "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return raw
        except urllib.error.HTTPError as e:
            last = "HTTP %s" % e.code
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 * (attempt + 1))
                continue
            return None, last
        except Exception as e:  # network, timeout, TLS
            last = type(e).__name__
            time.sleep(2 * (attempt + 1))
    return None, last


def main():
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    os.makedirs(TXT, exist_ok=True)
    body = get(API)
    if isinstance(body, tuple):
        print("manifest fetch failed:", body[1])
        return 3
    meta = json.loads(body)
    cands = meta.get("results", [])
    print("candidates offered:", len(cands), "total matching:", meta.get("count"))

    manifest = []
    for rec in cands:
        if len(manifest) >= target:
            break
        num = rec.get("document_number")
        url = rec.get("raw_text_url")
        if not num or not url:
            continue
        path = os.path.join(TXT, num + ".txt")
        if os.path.exists(path):
            text = open(path, "rb").read()
        else:
            got = get(url)
            if isinstance(got, tuple):
                print("  refuse", num, got[1])
                continue
            text = got
            if len(text) < 2000:
                # a 200 whose body strips to nothing is a refusal, not a capture
                print("  refuse", num, "body too short (%d bytes)" % len(text))
                continue
            with open(path, "wb") as fh:
                fh.write(text)
        try:
            decoded = text.decode("utf-8")
        except UnicodeDecodeError:
            decoded = text.decode("utf-8", "replace")
        if len(decoded) < 2000:
            print("  refuse", num, "decoded too short")
            continue
        manifest.append({
            "document_number": num,
            "title": rec.get("title"),
            "publication_date": rec.get("publication_date"),
            "effective_on": rec.get("effective_on"),
            "raw_text_url": url,
            "html_url": rec.get("html_url"),
            "cfr_references": rec.get("cfr_references"),
            "docket_ids": rec.get("docket_ids"),
            "page_length": rec.get("page_length"),
            "bytes": len(text),
            "chars": len(decoded),
            "sha256": hashlib.sha256(text).hexdigest(),
        })
        print("  ok %s  %7d bytes  %s" % (num, len(text), (rec.get("title") or "")[:60]))

    with open(os.path.join(RAW, "manifest.jsonl"), "w") as fh:
        for row in manifest:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    print("captured:", len(manifest), "refused:", len(cands) - len(manifest))
    return 0


if __name__ == "__main__":
    sys.exit(main())