#!/usr/bin/env python3
"""
E209: Fetch USAspending recipient data for 5 IT PSC codes.

Current window: FY2023. Prior window: FY2018-2022 (5 years).
Writes raw/ with one file per page per code per window.
Uses cached responses from tools/raw/ if available (fetched in this session).
"""

import json
import os
import hashlib
import shutil

CODES = ["DA01", "DA10", "7A21", "7030", "D304"]
WINDOWS = ["current", "prior"]
TOOLS_RAW = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tools", "raw")
EXP_RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")

os.makedirs(EXP_RAW, exist_ok=True)

def copy_cached():
    """Copy cached responses from tools/raw to experiment raw."""
    copied = 0
    for window in WINDOWS:
        for code in CODES:
            page = 1
            while True:
                src_json = os.path.join(TOOLS_RAW, f"{window}_{code}_p{page}.json")
                src_meta = os.path.join(TOOLS_RAW, f"{window}_{code}_p{page}.meta.json")
                if not os.path.exists(src_json):
                    break
                dst_json = os.path.join(EXP_RAW, f"{window}_{code}_p{page}.json")
                dst_meta = os.path.join(EXP_RAW, f"{window}_{code}_p{page}.meta.json")
                shutil.copy2(src_json, dst_json)
                shutil.copy2(src_meta, dst_meta)
                copied += 1
                page += 1
    return copied

def verify_integrity():
    """Verify SHA-256 of all copied files matches meta.json."""
    verified = 0
    mismatched = 0
    for fname in sorted(os.listdir(EXP_RAW)):
        if fname.endswith(".json") and not fname.endswith(".meta.json"):
            meta_path = os.path.join(EXP_RAW, fname.replace(".json", ".meta.json"))
            if not os.path.exists(meta_path):
                continue
            with open(meta_path) as f:
                meta = json.load(f)
            expected_sha = meta["response"]["sha256"]
            with open(os.path.join(EXP_RAW, fname), "rb") as f:
                actual_sha = hashlib.sha256(f.read()).hexdigest()
            if expected_sha == actual_sha:
                verified += 1
            else:
                mismatched += 1
                print(f"MISMATCH: {fname} expected {expected_sha} got {actual_sha}")
    return verified, mismatched

def summarize():
    """Print summary of fetched data."""
    print("=" * 72)
    print("E209 FETCH SUMMARY")
    print("=" * 72)
    for window in WINDOWS:
        for code in CODES:
            pages = []
            page = 1
            while True:
                fpath = os.path.join(EXP_RAW, f"{window}_{code}_p{page}.json")
                if not os.path.exists(fpath):
                    break
                with open(fpath) as f:
                    data = json.load(f)
                pages.append(len(data.get("results", [])))
                page += 1
            if pages:
                total_rows = sum(pages)
                print(f"  {code} {window}: {len(pages)} pages, {total_rows} rows")

def main():
    print("Copying cached responses from tools/raw/ ...")
    copied = copy_cached()
    print(f"Copied {copied} response files.")
    
    print("\nVerifying SHA-256 integrity...")
    verified, mismatched = verify_integrity()
    print(f"Verified: {verified}, Mismatched: {mismatched}")
    
    if mismatched > 0:
        print("ERROR: Integrity check failed")
        return 1
    
    summarize()
    print("\nFetch complete. Raw data committed to experiment directory.")
    return 0

if __name__ == "__main__":
    exit(main())