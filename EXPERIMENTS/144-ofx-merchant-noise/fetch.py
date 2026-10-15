#!/usr/bin/env python3
"""
Fetch OFX test fixtures from public repositories.
"""

import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

RAW_DIR = Path(__file__).parent / "raw"
RAW_DIR.mkdir(exist_ok=True)

SOURCES = [
    # Actual Budget (loot-core) OFX mock files
    {
        "url": "https://raw.githubusercontent.com/actualbudget/actual/master/packages/loot-core/src/mocks/files/credit-card.ofx",
        "filename": "actual_credit-card.ofx",
        "source": "actualbudget/actual",
        "description": "Apple Card OFX sample"
    },
    {
        "url": "https://raw.githubusercontent.com/actualbudget/actual/master/packages/loot-core/src/mocks/files/data.ofx",
        "filename": "actual_data.ofx",
        "source": "actualbudget/actual",
        "description": "Bank of America OFX sample"
    },
    {
        "url": "https://raw.githubusercontent.com/actualbudget/actual/master/packages/loot-core/src/mocks/files/data-multi-decimal.ofx",
        "filename": "actual_data-multi-decimal.ofx",
        "source": "actualbudget/actual",
        "description": "Bank of America multi-decimal OFX sample"
    },
    {
        "url": "https://raw.githubusercontent.com/actualbudget/actual/master/packages/loot-core/src/mocks/files/data-payee-memo.ofx",
        "filename": "actual_data-payee-memo.ofx",
        "source": "actualbudget/actual",
        "description": "OFX sample with payee and memo"
    },
    {
        "url": "https://raw.githubusercontent.com/actualbudget/actual/master/packages/loot-core/src/mocks/files/utf-8-bom.csv",
        "filename": "actual_utf-8-bom.csv",
        "source": "actualbudget/actual",
        "description": "CSV sample with UTF-8 BOM"
    },
]

SOURCES_MD = RAW_DIR / "SOURCES.md"

def fetch_url(url: str, dest: Path) -> dict:
    """Fetch a URL and return metadata."""
    print(f"Fetching {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            dest.write_bytes(content)
            sha256 = hashlib.sha256(content).hexdigest()
            print(f"  -> {dest.name} ({len(content)} bytes, sha256={sha256[:16]}...)")
            return {
                "url": url,
                "filename": dest.name,
                "bytes": len(content),
                "sha256": sha256,
                "status": "success"
            }
    except Exception as e:
        print(f"  -> FAILED: {e}")
        return {
            "url": url,
            "filename": dest.name,
            "bytes": 0,
            "sha256": None,
            "status": f"failed: {e}"
        }

def main():
    print("Fetching OFX test fixtures...")
    print(f"Raw directory: {RAW_DIR}")
    
    results = []
    for src in SOURCES:
        dest = RAW_DIR / src["filename"]
        result = fetch_url(src["url"], dest)
        result.update({
            "source": src["source"],
            "description": src["description"]
        })
        results.append(result)
    
    # Write SOURCES.md
    with open(SOURCES_MD, 'w') as f:
        f.write("# OFX Test Fixture Sources\n\n")
        f.write("Fetched on: 2026-10-15\n\n")
        f.write("| File | Source | Description | Bytes | SHA256 |\n")
        f.write("|------|--------|-------------|-------|--------|\n")
        for r in results:
            sha = r["sha256"][:32] if r["sha256"] else "FAILED"
            f.write(f"| {r['filename']} | {r['source']} | {r['description']} | {r['bytes']} | {sha} |\n")
    
    print(f"\nWrote {SOURCES_MD}")
    print("Done.")

if __name__ == "__main__":
    main()