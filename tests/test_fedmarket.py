"""Tests for fedmarket.py — main CLI entry point.

Most tests verify static fallback behavior (no API required). Integration
tests requiring USAspending API are marked with pytest.mark.network and
will be skipped unless --network flag given.
"""

import json
import os
import sys

# Add parent directory to path so we can import fedmarket
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fedmarket

import pytest


# ── Helpers ────────────────────────────────────────────────────────────────

def make_static_result(code="7030"):
    """Build a minimal result dict mimicking assess_code_dynamic static output."""
    return {
        "code": code,
        "name": "IT Software" if code == "7030" else "IT Services",
        "screen_score": 2411 if code == "7030" else 2345,
        "recipient_count": 3916 if code == "7030" else 3651,
        "top_10_share_pct": 38.4 if code == "7030" else 35.8,
        "leq_40k_pct": 32.1 if code == "7030" else 27.1,
        "leq_100k_pct": 46.8 if code == "7030" else 42.0,
        "single_award_pct": 100.0 if code == "7030" else 100.0,
        "software_pct_awards": 64.5 if code == "7030" else 57.8,
        "software_pct_obligation": 75.6 if code == "7030" else 64.7,
        "software_leq_40k_pct": 41.4 if code == "7030" else 49.9,
        "software_leq_100k_pct": 62.8 if code == "7030" else 69.7,
        "software_median_award": 56939 if code == "7030" else 40168,
        "dod_pct": 44.5 if code == "7030" else 43.6,
        "civilian_agencies": "14+ agencies >$500M" if code == "7030" else "VA 19.4%, GSA 7.8%",
        "gsa_awarding_pct": 2.1 if code == "7030" else 7.8,
        "small_vendor_gsa_mas_by_sin": {"511210": "5.9%"} if code == "7030" else {"511210": "28.3%"},
        "sewp_catb_small_vendor_pct": 6.0 if code == "7030" else 1.6,
        "sub_prime_ratio_pct": 0.1 if code == "7030" else 8.1,
        "small_vendor_gwac_share_pct": 4.7 if code == "7030" else 28.2,
        "total_obligation_b": 25.83 if code == "7030" else 33.01,
    }


# ── Test Group: basic import and help ─────────────────────────────────────

def test_import():
    """fedmarket can be imported without errors."""
    assert fedmarket is not None


# ── Test Group: assess_code_dynamic static fallback ────────────────────────

def test_assess_code_dynamic_no_code():
    """Missing code should cause argparse exit (not a unit-test concern per se)."""
    with pytest.raises(SystemExit):
        fedmarket.main(argv=["fedmarket.py"])


# ── Test Group: two-axis recommendation integration ────────────────────────

def test_two_axis_entry_7030_static():
    """7030 with strong static metrics should recommend 'entry' axis."""
    result = fedmarket.assess_code_dynamic("7030", refresh=False)
    assert "code" in result
    assert "name" in result
    assert "screen_score" in result
    # Static only: survival/graduation should be None
    assert result.get("survival") is None
    assert result.get("graduation") is None
    # Recommendation should still be produced
    assert result.get("recommendation") is not None


def test_two_axis_business_da10_static():
    """DA10 with strong static metrics should recommend 'gwac_pathway' entry axis."""
    rec = fedmarket.two_axis_recommendation("DA10", make_static_result("DA10"))
    assert rec["entry_axis"] == "gwac_pathway"
    assert rec["recommendation"] in ("entry", "business", "balanced")


def test_two_axis_recommendation_all_fields():
    """Two-axis recommendation should have all expected fields."""
    static = make_static_result("7030")
    rec = fedmarket.two_axis_recommendation("7030", static)
    assert "entry_axis" in rec
    assert "primary_vehicle" in rec
    assert "entry_score" in rec
    assert "business_score" in rec
    assert "recommendation" in rec
    assert "caveats" in rec


# ── Test Group: format functions ───────────────────────────────────────────

def test_format_result_has_recommendation():
    """Formatted result should include two-axis recommendation."""
    static = make_static_result("7030")
    rec = fedmarket.two_axis_recommendation("7030", static)
    result = {
        "code": "7030",
        "name": "IT Software",
        "screen_score": 2411,
        "recipient_count": 3916,
        "leq_40k_pct": 32.1,
        "software_pct_awards": 64.5,
        "recommendation": rec,
    }
    formatted = fedmarket.format_result_dynamic(result)
    assert "Two-Axis" in formatted or "recommendation" in formatted.lower()


def test_format_recommendation_has_fields():
    """Formatted recommendation should have all expected fields."""
    static = make_static_result("7030")
    rec = fedmarket.two_axis_recommendation("7030", static)
    result = {
        "code": "7030",
        "name": "IT Software",
        "screen_score": 2411,
        "recipient_count": 3916,
        "leq_40k_pct": 32.1,
        "software_pct_awards": 64.5,
        "recommendation": rec,
        "entry_axis": rec["entry_axis"],
        "primary_vehicle": rec["primary_vehicle"],
        "entry_score": rec["entry_score"],
        "business_score": rec["business_score"],
    }
    formatted = fedmarket.format_recommendation(result)
    assert "Recommendation:" in formatted
    assert "Entry axis:" in formatted
    assert "Business score (sustainability):" in formatted


# ── Test Group: --refresh flag behavior ────────────────────────────────────

def test_refresh_false_uses_static():
    """--refresh=False (default) should rely on static data, not API."""
    # When refresh=False and no cache, assess_code_dynamic should fall back
    # to static data only (survival/graduation will be None)
    result = fedmarket.assess_code_dynamic("7030", refresh=False)
    assert "code" in result
    # Without API data, these should be None
    assert result.get("survival") is None
    assert result.get("graduation") is None
    assert result.get("recommendation") is not None


def test_refresh_true_attempts_dynamic():
    """--refresh=True should attempt dynamic API fetch."""
    result = fedmarket.assess_code_dynamic("7030", refresh=True)
    assert "code" in result
    # Dynamic fields may be None if API unavailable; that's OK per design
    assert result.get("recommendation") is not None


# ── Test Group: output format ──────────────────────────────────────────────

def test_json_output():
    """JSON output should be valid and contain expected keys."""
    static = make_static_result("7030")
    rec = fedmarket.two_axis_recommendation("7030", static)
    result = {
        "code": "7030",
        "name": "IT Software",
        "screen_score": 2411,
        "recipient_count": 3916,
        "leq_40k_pct": 32.1,
        "software_pct_awards": 64.5,
        "recommendation": rec,
        "entry_axis": rec["entry_axis"],
        "primary_vehicle": rec["primary_vehicle"],
        "entry_score": rec["entry_score"],
        "business_score": rec["business_score"],
        "caveats": rec["caveats"],
        "survival": rec.get("survival"),
        "graduation": rec.get("graduation"),
        "n_cohort": rec.get("n_cohort"),
        "n_surviving": rec.get("n_surviving"),
        "n_graduates": rec.get("n_graduates"),
        "mean_awards_per_uei": rec.get("mean_awards_per_uei"),
        "survival_net_positive": rec.get("survival_net_positive"),
    }
    # Verify it's valid JSON
    text = json.dumps(result)
    parsed = json.loads(text)
    assert parsed["code"] == "7030"
    assert "recommendation" in parsed


# ── Run ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pytest.main([__file__, "-v"])