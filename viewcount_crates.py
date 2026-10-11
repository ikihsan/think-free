#!/usr/bin/env python3
"""
View-count principle generalization test on Rust crates.io.

Tests whether need-related crates are systematically more "active"
(have significant activity metadata) than random crates, extending
the E071 (PyPI) and E072 (NPM) findings to crates.io.

Status: draft. Prototype experiment, not a product. Attempted but
blocked by crates.io API rate limiting (429 Too Many Requests).
See SESSION_OUTCOME.md for full decision narrative.
"""

import json
import urllib.request
import urllib.error
import sys
import time
import random
from typing import List, Dict, Any, Optional, Tuple

CRATES_IO_API = "https://crates.io/api/v1"
API_SLEEP = 1.5


def crates_request(path, timeout=30):
    url = f"{CRATES_IO_API}{path}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "think-free-viewcount/1.0",
                      "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode('utf-8')
            return json.loads(body), resp.status
    except urllib.error.HTTPError as e:
        if e.code == 429:
            time.sleep(API_SLEEP)
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    body = resp.read().decode('utf-8')
                    return json.loads(body), resp.status
            except Exception:
                return None, e.code
        return None, e.code
    finally:
        time.sleep(API_SLEEP)


def get_crate_info(crate_name):
    data, status = crates_request(f"/crates/{crate_name}")
    if status == 200 and data and "crate" in data:
        return data["crate"]
    return None


def is_activity_present(crate_data):
    recent = crate_data.get("recent_downloads")
    if recent is not None and recent > 0:
        return True
    downloads = crate_data.get("downloads", 0)
    if downloads is not None and downloads > 0:
        return True
    return False


def classify_need_related(crate_name, crate_data):
    name = crate_name.lower()
    need_keywords = ["web", "http", "api", "client", "server", "framework",
                     "serde", "json", "protobuf", "thrift", "avro",
                     "clap", "structopt", "tokio", "async-std", "reqwest",
                     "diesel", "log", "tracing", "humantize", "slugify"]
    for kw in need_keywords:
        if kw in name:
            return "need-related"
    keywords = crate_data.get("keywords", [])
    if keywords:
        kw_lower = [k.lower() for k in keywords]
        for kw in need_keywords:
            if kw in kw_lower:
                return "need-related"
    downloads = crate_data.get("downloads", 0)
    if downloads is not None and downloads > 10000:
        return "need-related"
    return "random"


def run_experiment(sample_size=30, search_query="clap"):
    print(f"View-count test on crates.io, sample={sample_size}, query={search_query}")
    crates_sample = []
    seen = set()

    # Search-based sampling
    if search_query:
        data, status = crates_request(f"/crates?search={search_query}&per_page=25")
        if status == 200 and data:
            for entry in data.get("crates", []):
                name = entry.get("crate", "")
                if name and name not in seen:
                    seen.add(name)
                    detailed = get_crate_info(name)
                    if detailed:
                        crates_sample.append(detailed)
                    if len(crates_sample) >= sample_size:
                        break

    # Name-based fallback
    if len(crates_sample) < sample_size:
        patterns = ["clap", "serde", "tokio", "reqwest", "diesel", "log",
                    "tracing", "humantize", "once", "uuid", "base64"]
        for pattern in patterns:
            if len(crates_sample) >= sample_size:
                break
            for i in range(10):
                name = f"{pattern}{i}" if i > 0 else pattern
                if name not in seen:
                    seen.add(name)
                    detailed = get_crate_info(name)
                    if detailed:
                        crates_sample.append(detailed)
                    if len(crates_sample) >= sample_size:
                        break

    if len(crates_sample) == 0:
        print("  No crates sampled; API rate-limited.")
        return {"error": "no_crates_sampled"}

    need_related_active = need_related_total = 0
    random_active = random_total = 0

    for cd in crates_sample:
        cn = cd.get("name", "unknown")
        act = is_activity_present(cd)
        cls = classify_need_related(cn, cd)
        if cls == "need-related":
            need_related_total += 1
            if act:
                need_related_active += 1
        else:
            random_total += 1
            if act:
                random_active += 1

    need_rate = (need_related_active / need_related_total * 100) if need_related_total else 0
    random_rate = (random_active / random_total * 100) if random_total else 0
    diff = need_rate - random_rate

    if need_related_total > 0 and random_total > 0:
        strength = "strong" if diff >= 30 else "moderate" if diff >= 15 else "weak" if diff > 0 else ("reversed" if random_rate > need_related_rate + 10 else "neutral")
    else:
        strength = "unknown"

    return {
        "sample_size": len(crates_sample),
        "need_related_total": need_related_total,
        "need_related_active": need_related_active,
        "need_related_rate": need_rate,
        "random_total": random_total,
        "random_active": random_active,
        "random_rate": random_rate,
        "difference": diff,
        "strength": strength,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="View-count principle test on crates.io")
    parser.add_argument("--sample", type=int, default=30,
                        help="Number of crates to sample")
    parser.add_argument("--query", type=str, default="clap",
                        help="Search query fallback")
    parser.add_argument("--output", type=str, default=None,
                        help="Write results JSON file")
    args = parser.parse_args()
    results = run_experiment(sample_size=args.sample, search_query=args.query)
    print(f"\nNeed-related: {results['need_related_active']}/{results['need_related_total']} = {results['need_related_rate']:.1f}% active")
    print(f"Random:       {results['random_active']}/{results['random_total']} = {results['random_rate']:.1f}% active")
    print(f"Difference:   {results['difference']:.1f} pp  Strength: {results['strength']}")
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults written to {args.output}")


if __name__ == "__main__":
    main()