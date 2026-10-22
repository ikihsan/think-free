#!/usr/bin/env python3
"""fedmarket Subaward trace module — prime-specific subaward analysis.

Queries USAspending API to trace subawards from specific large primes
in a given PSC code. Uses:
1. spending_by_category/recipient (awards) to get top primes
2. spending_by_transaction with recipient_id to get prime award IDs
3. /api/v2/subawards/ with award_id to get subawards for each prime award
"""

import os
import sys
import json
import urllib.request
import urllib.error
import ssl
import hashlib
import time

from .api import call, base_filters, RECENT_WINDOW, AWARD_TYPES
from .output import print_subaward_trace


PRIME_RECIPIENT_FIELDS = ["name", "amount", "recipient_id", "uei", "code"]


def fetch_top_primes(psc_code, limit=20, max_pages=5, capture_prefix="prime_trace"):
    """Fetch top prime recipients for a PSC code."""
    all_results = []
    page = 1
    while page <= max_pages:
        payload = {
            "filters": base_filters(psc_codes=[psc_code], time_period=RECENT_WINDOW),
            "limit": limit,
            "page": page,
            "spending_level": "awards",
        }
        capture_name = f"{capture_prefix}_awards_{psc_code}_p{page}"
        st, parsed, meta = call("spending_by_category/recipient/", payload, capture_name)
        if st != 200 or not isinstance(parsed, dict):
            print(f"  Page {page}: status {st}")
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        if not parsed.get("page_metadata", {}).get("hasNext", False):
            break
        page += 1
    return all_results


def fetch_awards_for_recipient(recipient_id, limit=50, capture_prefix="prime_trace"):
    """Fetch award IDs for a specific recipient using spending_by_transaction."""
    all_results = []
    page = 1
    while page <= 10:  # Max 10 pages = 500 awards
        payload = {
            "fields": [
                "Transaction Amount",
                "Award ID",
                "Recipient Name",
                "Awarding Agency",
                "Recipient UEI",
            ],
            "filters": {
                "award_type_codes": AWARD_TYPES,
                "recipient_id": recipient_id,
            },
            "page": page,
            "limit": limit,
            "sort": "Transaction Amount",
            "order": "desc",
        }
        capture_name = f"{capture_prefix}_txn_{recipient_id[:8]}_p{page}"
        st, parsed, meta = call("spending_by_transaction/", payload, capture_name)
        if st != 200 or not isinstance(parsed, dict):
            print(f"    Transaction page {page}: status {st}")
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        if not parsed.get("page_metadata", {}).get("hasNext", False):
            break
        page += 1
    return all_results


def fetch_subawards_for_award(award_id, limit=100, capture_prefix="prime_trace"):
    """Fetch subawards for a specific prime award using /api/v2/subawards/."""

    HERE = os.path.dirname(os.path.abspath(__file__))
    RAW = os.path.join(HERE, "raw")
    UA = "think-free-research/0.1 (+repository think-free fedmarket)"
    BASE = "https://api.usaspending.gov/api/v2/"

    os.makedirs(RAW, exist_ok=True)
    url = BASE + "subawards/"
    payload = {
        "award_id": award_id,
        "page": 1,
        "limit": limit,
    }
    body = json.dumps(payload).encode()
    capture_name = f"{capture_prefix}_sub_{award_id[:32]}"

    # Check cache
    meta_path = os.path.join(RAW, capture_name + ".meta.json")
    for suffix in (".json", ".body"):
        body_path = os.path.join(RAW, capture_name + suffix)
        if os.path.exists(body_path) and os.path.exists(meta_path):
            try:
                prior = json.load(open(meta_path))
                if prior.get("request") == payload and prior.get("response", {}).get("endpoint") == url:
                    with open(body_path, "rb") as fh:
                        cached = fh.read()
                    meta = dict(prior["response"], reused=True)
                    try:
                        return json.loads(cached.decode("utf-8", "replace"))
                    except Exception:
                        break
            except Exception:
                break

    # Fetch from API
    for attempt in range(3):
        req = urllib.request.Request(
            url, data=body,
            headers={"User-Agent": UA, "Content-Type": "application/json",
                     "Accept": "application/json"})
        try:
            with urllib.request.urlopen(
                    req, timeout=180,
                    context=ssl.create_default_context()) as r:
                status, raw = r.status, r.read()
            break
        except urllib.error.HTTPError as e:
            status, raw = e.code, e.read()
            if e.code not in (429, 500, 502, 503, 504):
                break
        except Exception as e:
            status, raw = None, str(e).encode()
        time.sleep(0.5 * (attempt + 1))
    else:
        return {"page_metadata": {"hasNext": False}, "results": []}

    # Save to cache
    with open(os.path.join(RAW, capture_name + ".json"), "wb") as fh:
        fh.write(raw or b"")
    meta = {"endpoint": url, "status": status,
            "bytes": len(raw or b""),
            "sha256": hashlib.sha256(raw or b"").hexdigest()}
    with open(meta_path, "w") as fh:
        json.dump({"request": payload, "response": meta}, fh, indent=1, sort_keys=True)

    try:
        return json.loads((raw or b"").decode("utf-8", "replace"))
    except Exception:
        return {"page_metadata": {"hasNext": False}, "results": []}


def analyze_prime_subawards(psc_code, top_n=5, max_awards_per_prime=3):
    """Analyze subawards for top N primes in a PSC code."""
    print(f"\n{'#'*60}")
    print(f"# MODULE: Prime-Specific Subaward Trace (fedmarket Extension)")
    print(f"{'#'*60}")
    print(f"PSC Code: {psc_code}")
    print(f"Top primes to analyze: {top_n}")
    print(f"Max awards per prime: {max_awards_per_prime}")

    # Step 1: Get top primes
    print(f"\nFetching top prime recipients for {psc_code}...")
    primes = fetch_top_primes(psc_code)
    print(f"Found {len(primes)} prime recipients")

    if not primes:
        print("No prime recipients found")
        return None

    results = {
        "psc_code": psc_code,
        "primes_analyzed": [],
        "total_subawards_found": 0,
        "total_subaward_amount": 0.0,
    }

    # Step 2: For each top prime, get their awards and subawards
    for i, prime in enumerate(primes[:top_n]):
        prime_name = prime.get("name", "Unknown")
        prime_obligation = float(prime.get("amount", 0) or 0)
        prime_uei = prime.get("uei", "")
        recipient_id = prime.get("recipient_id", "")

        print(f"\n  [{i+1}/{min(top_n, len(primes))}] {prime_name} (${prime_obligation:,.0f})")

        if not recipient_id:
            print(f"    No recipient_id, skipping")
            continue

        # Get award IDs for this prime
        print(f"    Fetching awards...")
        awards = fetch_awards_for_recipient(recipient_id)
        print(f"    Found {len(awards)} award transactions")

        # Deduplicate by award ID (generated_internal_id)
        seen_award_ids = set()
        unique_awards = []
        for award in awards:
            award_id = award.get("generated_internal_id", "")
            if award_id and award_id not in seen_award_ids:
                seen_award_ids.add(award_id)
                unique_awards.append(award)

        print(f"    Unique awards: {len(unique_awards)}")

        prime_result = {
            "prime_name": prime_name,
            "prime_uei": prime_uei,
            "prime_recipient_id": recipient_id,
            "prime_total_obligation": prime_obligation,
            "awards_analyzed": 0,
            "total_subawards": 0,
            "total_subaward_amount": 0.0,
            "unique_subawardees": set(),
            "subawardees": [],
            "awards": [],
        }

        # Analyze up to max_awards_per_prime awards
        for j, award in enumerate(unique_awards[:max_awards_per_prime]):
            award_id = award.get("generated_internal_id", "")
            award_amount = float(award.get("Transaction Amount", 0) or 0)
            awarding_agency = award.get("Awarding Agency", "")

            print(f"      Award {j+1}: {award_id} (${award_amount:,.0f}, {awarding_agency})")

            # Fetch subawards for this award
            subaward_response = fetch_subawards_for_award(award_id)
            subawards = subaward_response.get("results", [])

            award_subaward_total = sum(float(s.get("amount", 0) or 0) for s in subawards)
            award_unique_subs = set(s.get("recipient_name", "") for s in subawards if s.get("recipient_name"))

            print(f"        Subawards: {len(subawards)} entries, ${award_subaward_total:,.0f} total, {len(award_unique_subs)} unique subawardees")

            # Track subawardees
            for sub in subawards:
                sub_name = sub.get("recipient_name", "")
                sub_amount = float(sub.get("amount", 0) or 0)
                if sub_name:
                    prime_result["unique_subawardees"].add(sub_name)
                    prime_result["subawardees"].append({
                        "name": sub_name,
                        "amount": sub_amount,
                        "description": sub.get("description", ""),
                        "action_date": sub.get("action_date", ""),
                        "subaward_number": sub.get("subaward_number", ""),
                        "prime_award_id": award_id,
                    })

            prime_result["awards_analyzed"] += 1
            prime_result["total_subawards"] += len(subawards)
            prime_result["total_subaward_amount"] += award_subaward_total

            prime_result["awards"].append({
                "award_id": award_id,
                "award_amount": award_amount,
                "awarding_agency": awarding_agency,
                "subaward_count": len(subawards),
                "subaward_total": award_subaward_total,
                "unique_subawardees": list(award_unique_subs),
            })

        prime_result["unique_subawardees"] = list(prime_result["unique_subawardees"])
        results["primes_analyzed"].append(prime_result)
        results["total_subawards_found"] += prime_result["total_subawards"]
        results["total_subaward_amount"] += prime_result["total_subaward_amount"]

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="fedmarket Prime-specific subaward trace")
    parser.add_argument("--code", required=True, help="PSC code (e.g., 7030, DA10)")
    parser.add_argument("--top", type=int, default=5, help="Number of top primes to analyze (default: 5)")
    parser.add_argument("--max-awards", type=int, default=3, help="Max awards per prime (default: 3)")
    parser.add_argument("--output", help="Output JSON file")
    args = parser.parse_args()

    result = analyze_prime_subawards(args.code, top_n=args.top, max_awards_per_prime=args.max_awards)

    if result:
        print_subaward_trace(args.code, result)

        if args.output:
            out_dir = os.path.dirname(args.output)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
            with open(args.output, "w") as f:
                json.dump(result, f, indent=2, default=str)
            print(f"\nJSON output saved to {args.output}")