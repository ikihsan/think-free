#!/usr/bin/env python3
"""
fedmarket.dynamic — Dynamic USAspending API client and recommendation engine.

This module re-exports the public API from the split implementation modules.
"""

from fedmarket.dynamic_api import (
    fetch_awards_by_code,
    fetch_recipients_by_code,
    compute_survival,
    compute_cross_market,
    API_BASE,
    AWARD_ENDPOINT,
    RECIPIENT_ENDPOINT,
    DEFAULT_HEADERS,
    AWARD_PAGE_LIMIT,
    RECIPIENT_PAGE_LIMIT,
    MAX_PAGES,
    SMALL_THRESHOLD,
    CACHE_DB_NAME,
    CACHE_TTL_DAYS,
    _get_cache_db,
    _is_cache_valid,
    _store_cache,
    _api_call,
)

from fedmarket.dynamic_rec import (
    two_axis_recommendation,
    assess_code_dynamic,
    format_result_dynamic,
    format_recommendation,
    survival_from_e211_raw,
)

__all__ = [
    # API client
    "fetch_awards_by_code",
    "fetch_recipients_by_code",
    "compute_survival",
    "compute_cross_market",
    "API_BASE",
    "AWARD_ENDPOINT",
    "RECIPIENT_ENDPOINT",
    "DEFAULT_HEADERS",
    "AWARD_PAGE_LIMIT",
    "RECIPIENT_PAGE_LIMIT",
    "MAX_PAGES",
    "SMALL_THRESHOLD",
    "CACHE_DB_NAME",
    "CACHE_TTL_DAYS",
    "_get_cache_db",
    "_is_cache_valid",
    "_store_cache",
    "_api_call",
    # Recommendation engine
    "two_axis_recommendation",
    "assess_code_dynamic",
    "format_result_dynamic",
    "format_recommendation",
    "survival_from_e211_raw",
]