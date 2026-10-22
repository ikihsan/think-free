"""
Dynamic USAspending API module for fedmarket.

Queries USAspending API for current metrics and caches results locally.
Falls back to static lookup when API is unavailable, with clear provenance tracking.

API endpoints used:
- /api/v2/spending_by_category/recipient/ — recipient analysis
- /api/v2/spending_by_award/ — award categorization
- /api/v2/spending_by_category/funding_agency/ — funding agencies
- /api/v2/spending_by_category/awarding_agency/ — awarding agencies
- /api/v2/spending_by_category/federal_account/ — federal accounts
- /api/v2/subawards/ — subaward trace (prime-specific)

All data provenance tracked: [Observed] = live API, [Cached] = local cache, [Static] = fallback
"""

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx

# Base URL for USAspending API
USA_SPENDING_BASE = "https://api.usaspending.gov/api/v2"

# Cache directory
CACHE_DIR = Path(__file__).parent.parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# Default timeout and limits
DEFAULT_TIMEOUT = 30.0
MAX_PAGES = 50
PAGE_SIZE = 100


class USAspendingClient:
    """HTTP client for USAspending API with caching and rate limiting."""

    def __init__(self, cache_dir: Optional[Path] = None, timeout: float = DEFAULT_TIMEOUT):
        self.base_url = USA_SPENDING_BASE
        self.cache_dir = cache_dir or CACHE_DIR
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)
        self._last_request_time = 0.0
        self._min_interval = 0.1  # 10 requests/second max

    def _rate_limit(self) -> None:
        """Enforce minimum interval between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)

    def _cache_path(self, endpoint: str, params: Dict[str, Any], prefix: str = "") -> Path:
        """Generate cache file path from endpoint and params."""
        # Create a deterministic filename from endpoint + sorted params
        param_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        cache_key = f"{prefix}_{endpoint.replace('/', '_')}_{param_str}"
        # Truncate if too long
        if len(cache_key) > 200:
            cache_key = cache_key[:200]
        return self.cache_dir / f"{cache_key}.json"

    def get(self, endpoint: str, params: Dict[str, Any], use_cache: bool = True, cache_prefix: str = "") -> Tuple[Dict[str, Any], str]:
        """GET request with caching. Returns (data, provenance)."""
        cache_path = self._cache_path(endpoint, params, cache_prefix)

        # Check cache first
        if use_cache and cache_path.exists():
            with open(cache_path, "r") as f:
                data = json.load(f)
            return data, f"[Cached] {cache_path.name}"

        # Rate limit
        self._rate_limit()

        # Make request
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.client.post(url, json=params)
            response.raise_for_status()
            data = response.json()

            # Save to cache
            if use_cache:
                with open(cache_path, "w") as f:
                    json.dump(data, f)
            provenance = f"[Observed] {url}"

        except httpx.HTTPError as e:
            # Try cache as fallback
            if cache_path.exists():
                with open(cache_path, "r") as f:
                    data = json.load(f)
                provenance = f"[Cached-Fallback] {cache_path.name} (API error: {e})"
            else:
                raise

        self._last_request_time = time.time()
        return data, provenance

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "USAspendingClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


def fetch_recipients(client: USAspendingClient, psc_code: str, max_pages: int = MAX_PAGES) -> Tuple[List[Dict], List[str]]:
    """Fetch recipient data for a PSC code."""
    all_results = []
    provenances = []

    for page in range(1, max_pages + 1):
        params = {
            "category": "recipient",
            "filters": {
                "psc_codes": [psc_code],
                "award_type_codes": ["A", "B", "C", "D"],
            },
            "page": page,
            "limit": PAGE_SIZE,
            "sort": "obligation",
            "order": "desc",
        }

        data, prov = client.get("/spending_by_category/recipient/", params, cache_prefix=f"recip_{psc_code}")
        provenances.append(prov)

        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)

        if not data.get("page_metadata", {}).get("hasNext", False):
            break

    return all_results, provenances


def fetch_awards(
    client: USAspendingClient,
    psc_code: str,
    max_pages: int = MAX_PAGES,
    date_range: Optional[Dict[str, str]] = None,
    cache_prefix: str = "award"
) -> Tuple[List[Dict], List[str]]:
    """Fetch award data for a PSC code."""
    all_results = []
    provenances = []

    for page in range(1, max_pages + 1):
        filters: Dict[str, Any] = {
            "psc_codes": [psc_code],
            "award_type_codes": ["A", "B", "C", "D"],
        }
        if date_range:
            filters["time_period"] = [date_range]

        params = {
            "filters": filters,
            "page": page,
            "limit": PAGE_SIZE,
            "sort": "Award Amount",
            "order": "asc",
        }

        data, prov = client.get("/spending_by_award/", params, cache_prefix=f"{cache_prefix}_{psc_code}")
        provenances.append(prov)

        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)

        if not data.get("page_metadata", {}).get("hasNext", False):
            break

    return all_results, provenances


def fetch_agencies(
    client: USAspendingClient,
    psc_code: str,
    category: str  # "funding_agency", "awarding_agency", "federal_account"
) -> Tuple[List[Dict], str]:
    """Fetch agency distribution for a PSC code."""
    params = {
        "category": category,
        "filters": {
            "psc_codes": [psc_code],
            "award_type_codes": ["A", "B", "C", "D"],
        },
        "page": 1,
        "limit": 100,
        "sort": "obligation",
        "order": "desc",
    }

    data, prov = client.get(f"/spending_by_category/{category}/", params, cache_prefix=f"{category}_{psc_code}")
    results = data.get("results", [])
    return results, prov


def fetch_subawards_for_prime(
    client: USAspendingClient,
    prime_award_piid: str,
    max_pages: int = 20
) -> Tuple[List[Dict], List[str]]:
    """Fetch subawards for a specific prime award PIID."""
    all_results = []
    provenances = []

    for page in range(1, max_pages + 1):
        params = {
            "filters": {
                "prime_award_piid": prime_award_piid,
            },
            "page": page,
            "limit": PAGE_SIZE,
            "sort": "sub_award_amount",
            "order": "desc",
        }

        data, prov = client.get("/subawards/", params, cache_prefix=f"subaward_{prime_award_piid}")
        provenances.append(prov)

        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)

        if not data.get("page_metadata", {}).get("hasNext", False):
            break

    return all_results, provenances


# ── Keyword classification (from E203) ────────────────────────────────────────

SOFTWARE_KEYWORDS = [
    "software", "saas", "license", "subscription", "cloud", "platform",
    "application", "app", "system", "development", "programming",
    "database", "analytics", "dashboard", "portal", "interface",
    "api", "sdk", "middleware", "firmware", "operating system",
    "devops", "ci/cd", "container", "kubernetes", "docker",
    "artificial intelligence", "machine learning", "ml", "ai",
    "cybersecurity", "security", "encryption", "authentication",
]

SERVICES_KEYWORDS = [
    "services", "support", "maintenance", "integration", "implementation",
    "consulting", "advisory", "training", "help desk", "operations",
    "management", "engineering", "technical", "staffing", "labor",
    "professional", "managed", "outsourcing", "sustainment",
]

HARDWARE_KEYWORDS = [
    "hardware", "equipment", "server", "storage", "network", "router",
    "switch", "firewall", "appliance", "device", "workstation",
    "laptop", "desktop", "peripheral", "component", "procurement",
    "purchase", "acquisition", "installation", "deployment",
]

TELECOM_KEYWORDS = [
    "telecom", "telecommunications", "voice", "data", "internet",
    "bandwidth", "circuit", "fiber", "cable", "satellite", "wireless",
    "5g", "4g", "lte", "mobile", "phone", "communication",
]

OTHER_KEYWORDS = [
    "research", "study", "analysis", "evaluation", "assessment",
    "plan", "strategy", "policy", "compliance", "audit",
]


def classify_award_description(description: str) -> str:
    """Classify award description into software/service/hardware/telecom/other."""
    if not description:
        return "other"

    desc_lower = description.lower()

    # Count keyword matches
    scores = {
        "software": sum(1 for kw in SOFTWARE_KEYWORDS if kw in desc_lower),
        "services": sum(1 for kw in SERVICES_KEYWORDS if kw in desc_lower),
        "hardware": sum(1 for kw in HARDWARE_KEYWORDS if kw in desc_lower),
        "telecom": sum(1 for kw in TELECOM_KEYWORDS if kw in desc_lower),
    }

    # Return category with highest score, default to "other"
    max_score = max(scores.values())
    if max_score == 0:
        return "other"

    # Tie-breaking: prefer software > services > hardware > telecom
    for cat in ["software", "services", "hardware", "telecom"]:
        if scores[cat] == max_score:
            return cat

    return "other"


def analyze_awards(awards: List[Dict]) -> Dict[str, Any]:
    """Analyze award data for categorization and size distribution."""
    if not awards:
        return {}

    total = len(awards)
    total_obligation = 0
    categories = {"software": 0, "services": 0, "hardware": 0, "telecom": 0, "other": 0}
    cat_obligation = {"software": 0, "services": 0, "hardware": 0, "telecom": 0, "other": 0}
    amounts = []

    for award in awards:
        amount = award.get("Award Amount", 0) or 0
        total_obligation += amount
        amounts.append(amount)

        desc = award.get("Description", "") or award.get("description", "") or ""
        cat = classify_award_description(desc)
        categories[cat] += 1
        cat_obligation[cat] += amount

    amounts_sorted = sorted(amounts)
    median_idx = len(amounts_sorted) // 2
    median_award = amounts_sorted[median_idx] if amounts_sorted else 0

    leq_40k = sum(1 for a in amounts if a <= 40000) / total * 100
    leq_100k = sum(1 for a in amounts if a <= 100000) / total * 100

    return {
        "total_awards": total,
        "total_obligation": total_obligation,
        "median_award": median_award,
        "categories": categories,
        "category_obligation": cat_obligation,
        "category_pct": {k: v / total * 100 for k, v in categories.items()},
        "category_obligation_pct": {k: v / total_obligation * 100 if total_obligation else 0 for k, v in cat_obligation.items()},
        "leq_40k_pct": leq_40k,
        "leq_100k_pct": leq_100k,
        "amounts": amounts,  # For downstream use
    }


def analyze_recipients(recipients: List[Dict]) -> Dict[str, Any]:
    """Analyze recipient data for screen metrics."""
    if not recipients:
        return {}

    total = len(recipients)
    obligations = [r.get("obligation", 0) or 0 for r in recipients]
    total_obligation = sum(obligations)

    # Top 10 share
    sorted_obligations = sorted(obligations, reverse=True)
    top_10_sum = sum(sorted_obligations[:10])
    top_10_share = top_10_sum / total_obligation * 100 if total_obligation else 0

    # Award count distribution
    # Note: recipient endpoint doesn't give award count directly
    # Use obligation as proxy for now
    leq_40k_count = sum(1 for o in obligations if o <= 40000)
    leq_100k_count = sum(1 for o in obligations if o <= 100000)

    return {
        "distinct_recipients": total,
        "total_obligation": total_obligation,
        "top_10_share_pct": top_10_share,
        "leq_40k_pct": leq_40k_count / total * 100,
        "leq_100k_pct": leq_100k_count / total * 100,
        "screen_score": int(total * (1 - top_10_share / 100)),
    }


# ── High-level assessment functions ──────────────────────────────────────────

def assess_code_dynamic(
    psc_code: str,
    refresh: bool = False,
    max_pages: int = MAX_PAGES,
    include_survival: bool = True,
) -> Dict[str, Any]:
    """Assess a PSC code using live USAspending API data.

    Parameters
    ----------
    psc_code : str
        PSC code to assess (e.g., '7030', 'DA10').
    refresh : bool
        If True, bypass cache and fetch fresh data.
    max_pages : int
        Maximum pages to fetch per endpoint.
    include_survival : bool
        If True, include survival analysis (requires recipient + award data).

    Returns
    -------
    dict
        Assessment results with provenance tracking.
    """
    with USAspendingClient() as client:
        # Fetch recipient data
        recipients, recip_prov = fetch_recipients(client, psc_code, max_pages)
        recip_analysis = analyze_recipients(recipients)

        # Fetch award data (full period)
        awards, award_prov = fetch_awards(client, psc_code, max_pages, cache_prefix=f"award_full_{psc_code}")
        award_analysis = analyze_awards(awards)

        # Fetch recent period awards (last 12 months)
        from datetime import datetime, timedelta
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        recent_awards, recent_prov = fetch_awards(
            client, psc_code, max_pages,
            date_range={"start_date": start_date, "end_date": end_date},
            cache_prefix=f"award_recent_{psc_code}"
        )
        recent_analysis = analyze_awards(recent_awards)

        # Fetch agency data
        funding_agencies, funding_prov = fetch_agencies(client, psc_code, "funding_agency")
        awarding_agencies, awarding_prov = fetch_agencies(client, psc_code, "awarding_agency")
        federal_accounts, fa_prov = fetch_agencies(client, psc_code, "federal_account")

        # Build result
        result = {
            "psc_code": psc_code,
            "provenance": {
                "recipient": recip_prov,
                "award_full": award_prov,
                "award_recent": recent_prov,
                "funding_agency": funding_prov,
                "awarding_agency": awarding_prov,
                "federal_account": fa_prov,
            },
            "recipient": recip_analysis,
            "award_full": award_analysis,
            "award_recent": recent_analysis,
            "funding_agencies": funding_agencies,
            "awarding_agencies": awarding_agencies,
            "federal_accounts": federal_accounts,
        }

        # Add survival analysis if requested (simplified - would need full E211 logic)
        if include_survival:
            result["survival_note"] = "Survival analysis requires cohort tracking across fiscal years. Use static lookup for E211 validated metrics."

        return result


def two_axis_recommendation(
    psc_code: str,
    static_metrics: Dict[str, Any],
    dynamic_result: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate two-axis recommendation combining static and dynamic data."""
    # This is a placeholder for the full dynamic two-axis logic
    # For now, return the static recommendation with dynamic provenance
    from .decision import decide_code

    # Use static graduation as axis 2 (dynamic survival not implemented)
    grad = static_metrics.get("graduation_cleaned_pct", 0)
    survival = static_metrics.get("survival_cleaned_pct", 0)

    return {
        "code": psc_code,
        "entry_axis": static_metrics.get("recommendation", {}).get("entry_axis"),
        "primary_vehicle": static_metrics.get("recommendation", {}).get("primary_vehicle"),
        "accessibility_score": static_metrics.get("screen_score"),
        "sustainability_score": grad,
        "survival_pct": survival,
        "graduation_pct": grad,
        "provenance": dynamic_result.get("provenance"),
        "note": "Dynamic survival analysis not yet implemented; using E211 static data for Axis 2.",
    }


def format_dynamic_result(result: Dict[str, Any]) -> str:
    """Format dynamic assessment result for display."""
    prov = result.get("provenance", {})
    recip = result.get("recipient", {})
    award = result.get("award_full", {})
    recent = result.get("award_recent", {})

    lines = [
        f"\n=== Dynamic Assessment: {result.get('psc_code')} ===",
        "",
        "PROVENANCE:",
        f"  Recipients: {prov.get('recipient', 'N/A')}",
        f"  Awards (full): {prov.get('award_full', 'N/A')}",
        f"  Awards (recent): {prov.get('award_recent', 'N/A')}",
        "",
        "RECIPIENT METRICS:",
        f"  Distinct recipients: {recip.get('distinct_recipients', 'N/A')}",
        f"  Top-10 share: {recip.get('top_10_share_pct', 0):.1f}%",
        f"  ≤$40k: {recip.get('leq_40k_pct', 0):.1f}%",
        f"  ≤$100k: {recip.get('leq_100k_pct', 0):.1f}%",
        f"  Screen score: {recip.get('screen_score', 'N/A')}",
        "",
        "AWARD CATEGORIZATION (full period):",
        f"  Total awards: {award.get('total_awards', 'N/A')}",
        f"  Software: {award.get('category_pct', {}).get('software', 0):.1f}%",
        f"  Services: {award.get('category_pct', {}).get('services', 0):.1f}%",
        f"  Hardware: {award.get('category_pct', {}).get('hardware', 0):.1f}%",
        f"  Telecom: {award.get('category_pct', {}).get('telecom', 0):.1f}%",
        f"  Median award: ${award.get('median_award', 0):,}",
        f"  ≤$40k: {award.get('leq_40k_pct', 0):.1f}%",
        f"  ≤$100k: {award.get('leq_100k_pct', 0):.1f}%",
    ]

    if recent:
        lines += [
            "",
            "AWARD CATEGORIZATION (recent 12mo):",
            f"  Total awards: {recent.get('total_awards', 'N/A')}",
            f"  Software: {recent.get('category_pct', {}).get('software', 0):.1f}%",
            f"  Median award: ${recent.get('median_award', 0):,}",
            f"  ≤$40k: {recent.get('leq_40k_pct', 0):.1f}%",
        ]

    return "\n".join(lines)


def format_recommendation_dynamic(rec: Dict[str, Any]) -> str:
    """Format dynamic two-axis recommendation for display."""
    lines = [
        "",
        "=== Two-Axis Recommendation (Dynamic) ===",
        f"PSC Code: {rec.get('code')}",
        f"Entry Axis: {rec.get('entry_axis')}",
        f"Primary Vehicle: {rec.get('primary_vehicle')}",
        f"Accessibility Score: {rec.get('accessibility_score')}",
        f"Sustainability Score (graduation): {rec.get('sustainability_score')}%",
        f"Survival (cleaned): {rec.get('survival_pct')}%",
        f"Graduation (cleaned): {rec.get('graduation_pct')}%",
        rec.get('note', ''),
    ]
    return "\n".join(lines)