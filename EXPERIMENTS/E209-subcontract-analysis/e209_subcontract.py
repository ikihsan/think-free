#!/usr/bin/env python3
"""E209 Subcontract Analysis: USAspending subawards for IT/software PSC codes.

Queries subaward data to understand how much small vendor $ flows as sub to large primes.
Uses spending_by_category/recipient with spending_level=subawards.
"""

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
import ssl

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-research/0.1 (+repository think-free E209)"
BASE = "https://api.usaspending.gov/api/v2/search/"

PSC_CODES = ["7030", "DA10", "7A21", "DA01", "D304"]
PSC_LABELS = {
    "7030": "IT Software",
    "DA10": "IT Services",
    "7A21": "IT Hardware/Software",
    "DA01": "IT Services (Mgmt)",
    "D304": "Telecom",
}

# Time window: recent 12 months
RECENT_WINDOW = [{"start_date": "2024-10-01", "end_date": "2025-09-30"}]

AWARD_TYPES = ["A", "B", "C", "D"]


def base_filters(**extra):
    f = {"award_type_codes": AWARD_TYPES}
    f.update(extra)
    return f


def call(endpoint, payload, capture_name, retries=3, pause=0.5):
    """POST to an endpoint, capture the body, return (status, parsed_or_text, meta)."""
    os.makedirs(RAW, exist_ok=True)
    url = BASE + endpoint
    body = json.dumps(payload).encode()
    meta_path = os.path.join(RAW, capture_name + ".meta.json")
    for suffix in (".json", ".body"):
        body_path = os.path.join(RAW, capture_name + suffix)
        if os.path.exists(body_path) and os.path.exists(meta_path):
            try:
                prior = json.load(open(meta_path))
                if (prior.get("request") == payload
                        and prior.get("response", {}).get("endpoint") == url):
                    with open(body_path, "rb") as fh:
                        cached = fh.read()
                    meta = dict(prior["response"], reused=True)
                    try:
                        return (meta.get("status"),
                                json.loads(cached.decode("utf-8", "replace")), meta)
                    except Exception:
                        break
            except Exception:
                break
    last = (None, "")
    for attempt in range(retries + 1):
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
            last = (status, raw)
            if e.code == 422 and attempt == retries:
                break
            if e.code not in (429, 500, 502, 503, 504) and attempt == retries:
                break
        except Exception as e:
            last = (None, ("%s: %s" % (type(e).__name__, e)).encode())
            raw = b""
            if attempt == retries:
                break
        time.sleep(pause * (attempt + 1))
    else:
        status, raw = last

    with open(os.path.join(RAW, capture_name + ".json"), "wb") as fh:
        fh.write(raw or b"")
    meta = {"endpoint": url, "status": status,
            "bytes": len(raw or b""),
            "sha256": hashlib.sha256(raw or b"").hexdigest()}
    with open(os.path.join(RAW, capture_name + ".meta.json"), "w") as fh:
        json.dump({"request": payload, "response": meta}, fh, indent=1,
                  sort_keys=True)
    try:
        parsed = json.loads((raw or b"").decode("utf-8", "replace"))
    except Exception:
        parsed = None
    return status, parsed, meta


def fetch_recipients(psc_code, spending_level="awards", limit=100, max_pages=100, capture_prefix="recip"):
    """Fetch all pages of a spending_by_category/recipient endpoint."""
    all_results = []
    page = 1
    while page <= max_pages:
        payload = {
            "filters": base_filters(psc_codes=[psc_code], time_period=RECENT_WINDOW),
            "limit": limit,
            "page": page,
            "spending_level": spending_level,
        }
        capture_name = f"{capture_prefix}_{spending_level}_{psc_code}_p{page}"
        st, parsed, meta = call(f"spending_by_category/recipient/", payload, capture_name)
        if st != 200 or not isinstance(parsed, dict):
            print(f"  Page {page}: status {st}")
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        if not parsed.get("page_metadata", {}).get("hasNext", False):
            break
        page += 1
    return all_results


def analyze_subawards(subawards, prime_name):
    """Analyze subaward data."""
    if not subawards:
        return {
            "prime": prime_name,
            "subaward_count": 0,
            "subaward_total": 0.0,
            "unique_subs": 0,
            "avg_subaward": 0.0,
            "max_subaward": 0.0,
        }
    
    amounts = [float(s.get("amount", 0) or 0) for s in subawards]
    unique_subs = set(s.get("name", "") for s in subawards if s.get("name"))
    
    return {
        "prime": prime_name,
        "subaward_count": len(subawards),
        "subaward_total": sum(amounts),
        "unique_subs": len(unique_subs),
        "avg_subaward": sum(amounts) / len(amounts) if amounts else 0.0,
        "max_subaward": max(amounts) if amounts else 0.0,
    }


def main():
    print("=== E209 Subcontract Analysis ===")
    print(f"PSC Codes: {', '.join(PSC_CODES)}")
    print(f"Time Window: Oct 2024 - Sep 2025")
    print()
    
    all_results = {}
    
    for psc_code in PSC_CODES:
        print(f"\n{'#'*60}")
        print(f"# PSC {psc_code} ({PSC_LABELS[psc_code]})")
        print(f"{'#'*60}")
        
        # Fetch top prime recipients (awards)
        print("  Fetching prime recipients (awards)...")
        primes = fetch_recipients(psc_code, spending_level="awards", limit=20, max_pages=5, capture_prefix="prime")
        print(f"  Found {len(primes)} prime recipients")
        
        # Fetch subaward recipients for same PSC
        print("  Fetching subaward recipients...")
        sub_recipients = fetch_recipients(psc_code, spending_level="subawards", limit=100, max_pages=20, capture_prefix="sub")
        print(f"  Found {len(sub_recipients)} subaward recipient entries")
        
        psc_results = {
            "psc_code": psc_code,
            "psc_label": PSC_LABELS[psc_code],
            "primes": [],
            "sub_recipients": sub_recipients,
        }
        
        # Analyze top 15 primes
        for i, prime in enumerate(primes[:15]):
            prime_name = prime.get("name", "Unknown")
            prime_id = prime.get("recipient_id", "")
            prime_obligation = float(prime.get("amount", 0) or 0)
            
            print(f"\n  [{i+1}/{min(15, len(primes))}] {prime_name} (${prime_obligation:,.0f})")
            
            # For subawards, we need to query by prime DUNS/UEI
            # The subawards endpoint with spending_level=subawards gives all subawardees
            # But we need subawards FOR a specific prime
            # Let's try the subawards search endpoint
            
            psc_results["primes"].append({
                "name": prime_name,
                "recipient_id": prime_id,
                "prime_obligation": prime_obligation,
                "code": prime.get("code"),
                "uei": prime.get("uei"),
            })
        
        # Aggregate subaward analysis
        sub_amounts = [float(s.get("amount", 0) or 0) for s in sub_recipients]
        sub_total = sum(sub_amounts)
        sub_unique = len(set(s.get("name", "") for s in sub_recipients if s.get("name")))
        
        all_results[psc_code] = psc_results
        all_results[psc_code]["subaward_summary"] = {
            "total_subaward_recipients": len(sub_recipients),
            "subaward_total": sub_total,
            "unique_subawardees": sub_unique,
            "avg_subaward": sub_total / len(sub_amounts) if sub_amounts else 0,
            "max_subaward": max(sub_amounts) if sub_amounts else 0,
        }
        
        print(f"\n  Subaward summary: {len(sub_recipients)} entries, "
              f"${sub_total:,.0f} total, {sub_unique} unique subawardees")
    
    # Save results
    output_path = os.path.join(HERE, "e209_results.json")
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults saved to {output_path}")
    
    # Print summary
    print("\n=== SUMMARY ===")
    for psc_code, data in all_results.items():
        s = data["subaward_summary"]
        prime_total = sum(p["prime_obligation"] for p in data["primes"])
        print(f"{psc_code} ({data['psc_label']}): "
              f"Sub entries: {s['total_subaward_recipients']}, "
              f"Sub total: ${s['subaward_total']:,.0f}, "
              f"Unique subs: {s['unique_subawardees']}, "
              f"Prime total (top 15): ${prime_total:,.0f}, "
              f"Sub/Prime ratio: {s['subaward_total']/prime_total*100:.1f}%" if prime_total > 0 else "N/A")


if __name__ == "__main__":
    main()