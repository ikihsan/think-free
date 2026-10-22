#!/usr/bin/env python3
"""
fedmarket_dynamic — Dynamic USAspending API client for fedmarket prototype.

Queries the USAspending API v2 for fresh PSC code metrics and caches results
in a local SQLite database. Falls back to static lookup data when API is
unavailable, with clear provenance tracking.

This module is designed to be imported by fedmarket.py to add dynamic/refresh
capability while preserving the existing static-data API.
"""

import hashlib
import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# ── Configuration ──────────────────────────────────────────────────────────

API_BASE = "https://api.usaspending.gov/api/v2/search/"
AWARD_ENDPOINT = "spending_by_award/"
RECIPIENT_ENDPOINT = "spending_by_category/recipient/"

DEFAULT_HEADERS = {
    "User-Agent": "think-free-fedmarket/1.0 (+repository think-free E211-E212)",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# USAspending API pagination defaults (matching E211/E206 conventions)
AWARD_PAGE_LIMIT = 100
RECIPIENT_PAGE_LIMIT = 100
MAX_PAGES = 100  # ceiling matching E211's 50-page cohort + return window
SMALL_THRESHOLD = 100_000.0  # ≤$100k defines the "small award" cohort

# Cache configuration
CACHE_DB_NAME = ".fedmarket_cache.db"
CACHE_TTL_DAYS = 30  # refresh cache after 30 days


# ── SQLite Cache Management ────────────────────────────────────────────────

def _get_cache_db() -> sqlite3.Connection:
    """Get or create the SQLite cache database connection."""
    cache_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), CACHE_DB_NAME
    )
    conn = sqlite3.connect(cache_path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS caches (
            key TEXT PRIMARY KEY,
            endpoint TEXT NOT NULL,
            payload TEXT NOT NULL,
            response_data TEXT NOT NULL,
            response_status INTEGER,
            response_time TEXT NOT NULL,
            created_at TEXT NOT NULL,
            ttl_days INTEGER DEFAULT 30
        )"""
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_caches_endpoint ON caches(endpoint)"
    )
    conn.commit()
    return conn


def _is_cache_valid(key: str, conn: sqlite3.Connection) -> bool:
    """Check if cached data is still within TTL."""
    row = conn.execute(
        "SELECT created_at, ttl_days FROM caches WHERE key = ?", (key,)
    ).fetchone()
    if not row:
        return False
    created = datetime.fromisoformat(row[0])
    ttl = row[1] or CACHE_TTL_DAYS
    delta = datetime.now(timezone.utc) - created
    return delta.days < ttl


def _store_cache(
    conn: sqlite3.Connection,
    key: str,
    endpoint: str,
    payload: dict,
    response_data: str,
    response_status: int,
) -> None:
    """Store response in cache with timestamp."""
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """INSERT OR REPLACE INTO caches (key, endpoint, payload, response_data,
             response_status, response_time, created_at, ttl_days)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            key,
            endpoint,
            json.dumps(payload, sort_keys=True),
            response_data,
            response_status,
            time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            now,
            CACHE_TTL_DAYS,
        ),
    )
    conn.commit()


# ── API Query Functions ────────────────────────────────────────────────────

def _api_call(
    endpoint: str,
    payload: dict,
    conn: Optional[sqlite3.Connection] = None,
) -> Tuple[Optional[dict], int, str]:
    """Make a POST request to USAspending API with caching.

    Returns (parsed_json, status_code, raw_body) or (None, status, raw).
    """
    if conn is None:
        conn = _get_cache_db()

    # Check cache first
    payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    cache_key = f"{endpoint}:{payload_hash}"

    if _is_cache_valid(cache_key, conn):
        row = conn.execute(
            "SELECT response_data FROM caches WHERE key = ?", (cache_key,)
        ).fetchone()
        try:
            return json.loads(row[0]), 200, row[0]
        except Exception:
            pass  # fall through to fresh fetch

    # Make fresh API request
    url = API_BASE + endpoint
    body = json.dumps(payload).encode()
    status = None
    raw = b""
    parsed = None

    try:
        import urllib.request
        req = urllib.request.Request(url, data=body, headers=DEFAULT_HEADERS.copy())
        with urllib.request.urlopen(req, timeout=120) as r:
            status = r.status
            raw = r.read()
    except urllib.error.HTTPError as e:
        status = e.code
        raw = e.read()
    except Exception as e:
        status = 0
        raw = b"Request failed: %s" % str(e).encode()

    # Try to parse JSON
    try:
        parsed = json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        parsed = None

    # Store in cache
    store_key = cache_key
    _store_cache(conn, store_key, endpoint, payload, raw.decode("utf-8", "replace"), status or 0)

    return parsed, status or 0, raw.decode("utf-8", "replace") if raw else ""


def fetch_awards_by_code(
    psc_code: str,
    start_date: str = "2020-10-01",
    end_date: str = "2021-09-30",
    max_pages: int = MAX_PAGES,
    conn: Optional[sqlite3.Connection] = None,
) -> Tuple[List[dict], dict]:
    """Fetch small funded awards (≤$100k) for a PSC code, ascending by amount.

    Matches E211 cohort design: FY2020-10-01 to FY2021-09-30, award types A-D.
    Returns (awards_list, metadata_dict) where metadata includes page count,
    censored flag, and distinct UEI count.

    Parameters
    ----------
    psc_code : str
        PSC code to query (e.g. '7030', 'DA10')
    start_date : str
        Cohort window start (default: FY2020-10-01)
    end_date : str
        Cohort window end (default: FY2021-09-30)
    max_pages : int
        Maximum pages to fetch (default: 100, matching E211 ceiling)
    conn : sqlite3.Connection or None
        Optional cache connection

    Returns
    -------
    Tuple[List[dict], dict]
        Each award dict has: uei, name, amount, agency, award_id
        Metadata has: n_awards, n_distinct_uei, n_pages, censored
    """
    metadata = {
        "n_awards": 0,
        "n_distinct_uei": 0,
        "n_pages": 0,
        "censored": False,
        "start_date": start_date,
        "end_date": end_date,
        "psc_code": psc_code,
    }

    payload = {
        "filters": {
            "time_period": [{"start_date": start_date, "end_date": end_date}],
            "psc_codes": [psc_code],
            "award_type_codes": ["A", "B", "C", "D"],
        },
        "fields": ["Award ID", "Recipient Name", "Recipient UEI", "Award Amount", "Awarding Agency"],
        "page": 1,
        "limit": AWARD_PAGE_LIMIT,
        "sort": "Award Amount",
        "order": "asc",
    }

    all_rows: List[dict] = []
    page = 1
    censored = False

    while page <= max_pages:
        parsed, status, raw = _api_call(AWARD_ENDPOINT, payload, conn)

        if status != 200 or parsed is None:
            break

        results = parsed.get("results", [])
        if not results:
            break

        for r in results:
            amt = float(r.get("Award Amount") or 0.0)
            if amt <= 0:
                continue
            if amt > SMALL_THRESHOLD:
                censored = True
                break
            uei = (r.get("Recipient UEI") or "").strip()
            name = r.get("Recipient Name") or ""
            agency = r.get("Awarding Agency") or ""
            aid = r.get("Award ID") or ""
            all_rows.append(
                {
                    "uei": uei,
                    "name": name,
                    "amount": amt,
                    "agency": agency,
                    "award_id": aid,
                }
            )

        page_metadata = parsed.get("page_metadata", {})
        if not page_metadata.get("hasNext") or censored:
            break

        page += 1
        payload["page"] = page

    metadata["n_awards"] = len(all_rows)
    ueis = {r["uei"] for r in all_rows if r["uei"]}
    metadata["n_distinct_uei"] = len(ueis)
    metadata["n_pages"] = page
    metadata["censored"] = censored

    return all_rows, metadata


def fetch_recipients_by_code(
    psc_code: str,
    start_date: str = "2022-10-01",
    end_date: str = "2025-09-30",
    max_pages: int = MAX_PAGES,
    conn: Optional[sqlite3.Connection] = None,
) -> Tuple[List[dict], dict]:
    """Fetch recipient aggregates for the return window.

    Matches E211 return window: FY2022-10-01 to FY2025-09-30.
    Returns (recipients_list, metadata_dict) where each recipient has:
    uei, name, total_amount.

    Parameters
    ----------
    psc_code : str
        PSC code to query
    start_date : str
        Return window start (default: FY2022-10-01)
    end_date : str
        Return window end (default: FY2025-09-30)
    max_pages : int
        Maximum pages to fetch
    conn : sqlite3.Connection or None
        Optional cache connection

    Returns
    -------
    Tuple[List[dict], dict]
        Each recipient dict: uei, name, amount
        Metadata: n_recipients, n_pages, censored
    """
    metadata = {
        "n_recipients": 0,
        "n_pages": 0,
        "censored": False,
        "start_date": start_date,
        "end_date": end_date,
        "psc_code": psc_code,
    }

    payload = {
        "category": "recipient",
        "filters": {
            "time_period": [{"start_date": start_date, "end_date": end_date}],
            "psc_codes": [psc_code],
            "award_type_codes": ["A", "B", "C", "D"],
        },
        "page": 1,
        "limit": RECIPIENT_PAGE_LIMIT,
        "sort": "amount",
        "order": "desc",
    }

    all_rows: List[dict] = []
    page = 1

    while page <= max_pages:
        parsed, status, raw = _api_call(RECIPIENT_ENDPOINT, payload, conn)

        if status != 200 or parsed is None:
            break

        results = parsed.get("results", [])
        if not results:
            break

        for r in results:
            uei = (r.get("uei") or "").strip()
            name = r.get("name") or ""
            amt = float(r.get("amount") or 0.0)
            all_rows.append({"uei": uei, "name": name, "amount": amt})

        page_metadata = parsed.get("page_metadata", {})
        if not page_metadata.get("hasNext"):
            break

        page += 1
        payload["page"] = page

    metadata["n_recipients"] = len(all_rows)
    metadata["n_pages"] = page

    return all_rows, metadata


# ── Survival & Graduation Computation ──────────────────────────────────────

def compute_survival(
    cohort_awards: List[dict],
    return_recipients: List[dict],
) -> Dict[str, Any]:
    """Compute entry survival and graduation metrics.

    Matches E211 design: UEI-matched cohort from awards window (A)
    returning in return window (B).

    Parameters
    ----------
    cohort_awards : List[dict]
        List of award dicts from fetch_awards_by_code with uei field
    return_recipients : List[dict]
        List of recipient dicts from fetch_recipients_by_code with uei field

    Returns
    -------
    Dict[str, Any]
        survival: float (0-1)
        graduation: float (0-1)
        n_cohort: int (distinct UEIs in cohort)
        n_surviving: int (UEIs found in return window)
        n_graduates: int (surviving UEIs with >$100k aggregate)
        mean_awards_per_uei: float
        median_awards_per_uei: float
        survival_net_positive: float ( UEIs with >$0 net in return window)
        uei_amounts: dict mapping UEI -> total amount in return window
        uei_names: dict mapping UEI -> name in return window
    """
    # Build UEI set from return window
    surviving_ueis = set()
    for r in return_recipients:
        if r["uei"]:
            surviving_ueis.add(r["uei"])

    # Count cohort distinct UEIs
    cohort_ueis = {r["uei"] for r in cohort_awards if r["uei"]}
    n_cohort = len(cohort_ueis)
    n_surviving = len(cohort_ueis & surviving_ueis)

    survival = (n_surviving / n_cohort) if n_cohort else 0.0

    # Graduation: surviving UEIs with >$100k aggregate in return window
    uei_amounts: Dict[str, float] = {}
    uei_names: Dict[str, str] = {}
    for r in return_recipients:
        if r["uei"]:
            uei_amounts[r["uei"]] = uei_amounts.get(r["uei"], 0.0) + r["amount"]
            if r["name"] and r["name"] not in uei_names:
                uei_names[r["uei"]] = r["name"]

    n_graduates = sum(
        1 for u in (cohort_ueis & surviving_ueis) if uei_amounts.get(u, 0.0) > SMALL_THRESHOLD
    )

    graduation = (n_graduates / n_cohort) if n_cohort else 0.0

    # Mean awards per UEI in cohort
    uei_award_count: Dict[str, int] = {}
    for a in cohort_awards:
        if a["uei"]:
            uei_award_count[a["uei"]] = uei_award_count.get(a["uei"], 0) + 1

    mean_awards = (
        sum(uei_award_count.values()) / n_cohort if n_cohort else 0.0
    )
    median_awards = (
        sorted(uei_award_count.values())[len(uei_award_count) // 2]
        if uei_award_count
        else 0.0
    )

    # Net-positive return: surviving UEIs with >$0 aggregate
    n_net_positive = sum(
        1 for u in (cohort_ueis & surviving_ueis) if uei_amounts.get(u, 0.0) > 0
    )
    survival_net_positive = (n_net_positive / n_cohort) if n_cohort else 0.0

    return {
        "survival": survival,
        "graduation": graduation,
        "n_cohort": n_cohort,
        "n_surviving": n_surviving,
        "n_graduates": n_graduates,
        "mean_awards_per_uei": mean_awards,
        "median_awards_per_uei": median_awards,
        "survival_net_positive": survival_net_positive,
        "uei_amounts": uei_amounts,
        "uei_names": uei_names,
    }


def compute_cross_market(
    survivors_ueis: set,
    other_codes_data: Dict[str, dict],
) -> Dict[str, int]:
    """Compute cross-market return rates.

    For each other PSC code, counts how many 7030 survivors also appear
    in that code's return window.

    Parameters
    ----------
    survivors_ueis : set
        UEIs from the reference code's survival set
    other_codes_data : Dict[str, dict]
        Dict mapping PSC code -> compute_survival() output for that code

    Returns
    -------
    Dict[str, int]
        Mapping of PSC code -> count of cross-market returns
    """
    cross: Dict[str, int] = {}
    for code, data in other_codes_data.items():
        other_ueis = set(data.get("uei_amounts", {}).keys())
        cross[code] = len(survivors_ueis & other_ueis)
    return cross


# ── Two-Axis Recommendation Engine ─────────────────────────────────────────

