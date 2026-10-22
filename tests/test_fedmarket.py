"""Tests for fedmarket package."""

import pytest
from fedmarket import assess_code, compare_codes, decide_code, budget_accessible_pct, CODES, KNOWN_GRADUATION


def test_codes_exist():
    """All expected PSC codes are in the lookup."""
    expected = {"7030", "DA10", "7A21", "DA01", "D304"}
    assert set(CODES.keys()) == expected


def test_assess_code_7030():
    """7030 assessment returns expected structure."""
    r = assess_code("7030")
    assert r["code"] == "7030"
    assert r["name"] == "IT Software"
    assert r["screen_score"] == 2411
    assert r["recipient_count"] == 3916
    assert r["leq_40k_pct"] == 32.1
    assert "recommendation" in r
    assert r["recommendation"]["entry_axis"] == "direct_sales"


def test_assess_code_da10():
    """DA10 assessment returns expected structure."""
    r = assess_code("DA10")
    assert r["code"] == "DA10"
    assert r["name"] == "IT Services"
    assert r["screen_score"] == 2345
    assert r["recommendation"]["entry_axis"] == "gwac_pathway"
    assert r["recommendation"]["primary_vehicle"] == "gsa_mas_schedule_70"


def test_assess_code_invalid():
    """Invalid code raises KeyError."""
    with pytest.raises(KeyError):
        assess_code("INVALID")


def test_compare_codes():
    """Compare codes returns ranked results."""
    comp = compare_codes(["7030", "DA10", "7A21"])
    assert "by_code" in comp
    assert "ranked_by_screen_score" in comp
    assert "ranked_by_leq_40k_access" in comp
    # 7030 should be top by screen score
    assert comp["ranked_by_screen_score"][0] == "7030"
    # D304 not in list but 7030 should be top of these three


def test_decide_code_profiles():
    """Profile-based recommendations match expectations."""
    # Profile 1: leq_40k + direct + software -> 7030
    rec = decide_code("leq_40k", "direct", "software")
    assert rec["recommended_code"] == "7030"
    assert rec["entry_axis"] == "direct_sales"

    # Profile 2: leq_100k + gsa_mas + saas -> DA10
    rec = decide_code("leq_100k", "gsa_mas", "saas")
    assert rec["recommended_code"] == "DA10"
    assert rec["entry_axis"] == "gwac_pathway"

    # Profile 3: enterprise + services -> DA01
    rec = decide_code("enterprise", "direct", "services")
    assert rec["recommended_code"] == "DA01"
    assert rec["entry_axis"] == "services_market"

    # Profile 4: subcontract -> DA10
    rec = decide_code("leq_100k", "subcontract", "software")
    assert rec["recommended_code"] == "DA10"


def test_known_graduation():
    """Known graduation rates have expected values."""
    assert KNOWN_GRADUATION["7030"] == 1.2
    assert KNOWN_GRADUATION["DA10"] == 23.7
    assert KNOWN_GRADUATION["DA01"] == 21.4


def test_budget_accessible_pct():
    """Budget accessible percentage interpolation works."""
    # At boundaries
    assert budget_accessible_pct("7030", 25000) == 41.4  # software_leq_40k
    assert budget_accessible_pct("7030", 150000) == 62.8  # software_leq_100k
    # Interpolation
    mid = budget_accessible_pct("7030", 70000)
    assert 41.4 < mid < 62.8


def test_assess_code_includes_survival():
    """Assessment includes E211 survival data."""
    r = assess_code("7030")
    assert "survival_pct" in r
    assert "graduation_pct" in r
    assert "survival_cleaned_pct" in r
    assert "graduation_cleaned_pct" in r
    assert r["survival_cleaned_pct"] == 13.8
    assert r["graduation_cleaned_pct"] == 1.2


def test_assess_code_includes_trend():
    """Assessment includes E204 trend data."""
    r = assess_code("7030")
    assert "trend" in r
    assert r["trend"]["direction"] == "concentrating"

    r = assess_code("DA10")
    assert r["trend"]["direction"] == "diversifying"

    r = assess_code("7A21")
    assert r["trend"]["direction"] == "hardening"


def test_assess_code_includes_e213_note():
    """Assessment includes E213 validation notes."""
    r = assess_code("7030")
    assert "e213_validation_note" in r
    assert "falsified" in r["e213_validation_note"].lower()

    r = assess_code("DA10")
    assert "e213_validation_note" in r
    assert "ONLY code" in r["e213_validation_note"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])