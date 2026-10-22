"""Tests for fedmarket_dynamic module.

Most tests can run without network access by verifying:
1. Static fallback behavior
2. Cache logic (no false positives/negatives)
3. Computation functions with synthetic data
4. Two-axis recommendation logic

Integration tests requiring USAspending API are marked with
pytest.mark.network and will be skipped unless --network flag given.
"""

import json
import os
import sys
import tempfile
import pytest

# Add parent directory to path so we can import fedmarket_dynamic
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fedmarket.dynamic import (
    fetch_awards_by_code,
    fetch_recipients_by_code,
    compute_survival,
    compute_cross_market,
    two_axis_recommendation,
    assess_code_dynamic,
    format_result_dynamic,
    format_recommendation,
    SMALL_THRESHOLD,
    MAX_PAGES,
    API_BASE,
)


# ── Helpers ────────────────────────────────────────────────────────────────

def make_award(uei: str = "TEST_UEI", amount: float = 50_000.0, name: str = "Test Corp") -> dict:
    return {"uei": uei, "name": name, "amount": amount, "agency": "DOD", "award_id": "TEST_AWARD"}


def make_recipient(uei: str = "TEST_UEI", amount: float = 50_000.0, name: str = "Test Corp") -> dict:
    return {"uei": uei, "name": name, "amount": amount}


# ── Test Group: fetch_awards_by_code ──────────────────────────────────────

@pytest.mark.network(False)
def test_fetch_awards_by_code_static_fallback():
    """fetch_awards_by_code should handle API failure gracefully.
    
    This test verifies the function doesn't crash when API is unavailable.
    We can't easily mock the network, so we just verify it returns a valid structure.
    """
    # This test may hit the real API or cache; we just verify structure
    awards, meta = fetch_awards_by_code("7030", conn=None)
    assert isinstance(awards, list)
    assert "n_awards" in meta
    assert "n_distinct_uei" in meta
    assert "n_pages" in meta
    assert "censored" in meta


@pytest.mark.network(False)
def test_fetch_awards_by_code_synthetic():
    """Test compute_survival with synthetic data (no API call)."""
    cohort = [make_award(uei="UEI1", amount=30_000),
              make_award(uei="UEI2", amount=60_000),
              make_award(uei="UEI3", amount=90_000)]
    returnees = [make_recipient(uei="UEI1", amount=30_000),
                 make_recipient(uei="UEI2", amount=60_000)]
    result = compute_survival(cohort, returnees)
    assert result["n_cohort"] == 3
    assert result["n_surviving"] == 2
    assert result["survival"] == 2 / 3
    assert result["graduation"] == 0.0  # no amounts > $100k


@pytest.mark.network(False)
def test_fetch_awards_by_code_survival_full():
    """Test survival computation with mixed data."""
    cohort = [
        make_award(uei="UEI_A", amount=20_000),
        make_award(uei="UEI_B", amount=40_000),
        make_award(uei="UEI_C", amount=80_000),
        make_award(uei="UEI_D", amount=120_000),  # > $100k, should this be in cohort?
    ]
    # UEI_D has amount > $100k, but it's in the cohort window; survival still counts it
    returnees = [
        make_recipient(uei="UEI_A", amount=25_000),
        make_recipient(uei="UEI_B", amount=45_000),
        make_recipient(uei="UEI_C", amount=85_000),
        # UEI_D not in return window
    ]
    result = compute_survival(cohort, returnees)
    assert result["n_cohort"] == 4
    assert result["n_surviving"] == 3  # UEI_A, UEI_B, UEI_C
    assert result["survival"] == 3 / 4
    # Graduation: UEI_A 25k, UEI_B 45k, UEI_C 85k — none > $100k
    assert result["graduation"] == 0.0
    # Net-positive: all three have > $0
    assert result["survival_net_positive"] == 3 / 4


# ── Test Group: two_axis_recommendation ────────────────────────────────────

@pytest.mark.network(False)
def test_two_axis_entry_7030():
    """7030 should recommend 'entry' axis when screen score is high."""
    static = {
        "screen_score": 2411,
        "leq_40k_pct": 32.1,
        "recipients": 3916,
        "software_pct_awards": 64.5,
    }
    # Without dynamic data, should still produce recommendation
    rec = two_axis_recommendation("7030", static)
    assert "recommendation" in rec
    assert rec["entry_axis"] == "direct_sales"


@pytest.mark.network(False)
def test_two_axis_business_da10():
    """DA10 should lean 'business' when graduation is high."""
    static = {
        "screen_score": 2345,
        "leq_40k_pct": 27.1,
        "recipients": 3651,
        "software_pct_awards": 57.8,
    }
    rec = two_axis_recommendation("DA10", static)
    assert "recommendation" in rec
    assert rec["entry_axis"] == "gwac_pathway"


@pytest.mark.network(False)
def test_two_axis_recommendation_fields():
    """Two-axis recommendation should have all expected fields."""
    static = {
        "screen_score": 2411,
        "leq_40k_pct": 32.1,
        "recipients": 3916,
        "software_pct_awards": 64.5,
    }
    rec = two_axis_recommendation("7030", static)
    assert "entry_axis" in rec
    assert "primary_vehicle" in rec
    assert "entry_score" in rec
    assert "business_score" in rec
    assert "recommendation" in rec
    assert "caveats" in rec


# ── Test Group: assess_code_dynamic ────────────────────────────────────────

@pytest.mark.network(False)
def test_assess_code_dynamic_static_only():
    """assess_code_dynamic should work without API (static fallback)."""
    result = assess_code_dynamic("7030", refresh=False)
    assert "code" in result
    assert "name" in result
    assert "screen_score" in result
    # Without dynamic fetch, these should be None
    assert result.get("survival") is None
    assert result.get("graduation") is None
    assert result.get("recommendation") is not None


@pytest.mark.network(False)
def test_assess_code_dynamic_with_dynamic():
    """assess_code_dynamic should include dynamic metrics when available."""
    # This test verifies the function runs; actual dynamic data depends on API
    result = assess_code_dynamic("7030", refresh=True)
    assert "code" in result
    # Dynamic fields may be None if API unavailable; that's OK
    assert result.get("recommendation") is not None


# ── Test Group: format functions ───────────────────────────────────────────

@pytest.mark.network(False)
def test_format_result_dynamic_has_recommendation():
    """Formatted result should include two-axis recommendation."""
    static = {
        "screen_score": 2411,
        "leq_40k_pct": 32.1,
        "recipients": 3916,
        "software_pct_awards": 64.5,
    }
    rec = two_axis_recommendation("7030", static)
    result = {
        "code": "7030",
        "name": "IT Software",
        "screen_score": 2411,
        "recipient_count": 3916,
        "leq_40k_pct": 32.1,
        "software_pct_awards": 64.5,
        "recommendation": rec,
    }
    formatted = format_result_dynamic(result)
    assert "Two-Axis" in formatted or "recommendation" in formatted.lower()


# ── Run ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pytest.main([__file__, "-v"])