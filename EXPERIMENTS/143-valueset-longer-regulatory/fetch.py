#!/usr/bin/env python3
"""fetch.py — fetch Federal Register final rules from the API.

Saves raw text to raw/<document_number>.txt and metadata to raw/documents.json.
Standard library only, deterministic given the API state at fetch time.
"""
import hashlib
import json
import os
import re
import time
import urllib.request

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
API = "https://www.federalregister.gov/api/v1/documents.json"


def fetch_documents(per_page=50, pages=1):
    """Fetch document metadata from the Federal Register API."""
    docs = []
    for page in range(1, pages + 1):
        url = (
            f"{API}?conditions%5Bterm%5D=final+rule&per_page={per_page}"
            f"&page={page}&fields%5B%5D=title&fields%5B%5D=abstract"
            f"&fields%5B%5D=publication_date&fields%5B%5D=document_number"
            f"&fields%5B%5D=raw_text_url&order=newest"
        )
        data = json.loads(urllib.request.urlopen(url, timeout=15).read())
        results = data.get("results", [])
        if not results:
            break
        docs.extend(results)
        time.sleep(0.3)
    return docs


def fetch_full_text(raw_url, retries=3):
    """Fetch the full text of a document."""
    for attempt in range(retries):
        try:
            return urllib.request.urlopen(raw_url, timeout=20).read().decode(
                "utf-8", "replace"
            )
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                raise


def main():
    os.makedirs(RAW, exist_ok=True)
    docs = fetch_documents()
    print(f"Fetched {len(docs)} document metadata entries")

    # Save metadata
    with open(os.path.join(RAW, "documents.json"), "w") as f:
        json.dump(docs, f, indent=2)

    # Fetch full text for docs with abstracts
    fetched = 0
    for r in docs:
        if not r.get("abstract"):
            continue
        raw_url = r.get("raw_text_url")
        if not raw_url:
            continue
        doc_num = r["document_number"]
        out_path = os.path.join(RAW, f"{doc_num}.txt")
        if os.path.exists(out_path):
            fetched += 1
            continue
        try:
            text = fetch_full_text(raw_url)
            with open(out_path, "w") as f:
                f.write(text)
            fetched += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"  Error fetching {doc_num}: {e}")

    print(f"Fetched full text for {fetched} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())