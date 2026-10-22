"""Tests for fedmarket package."""

import os


def test_imports():
    """Test that all modules can be imported."""
    from fedmarket import api, recipient, award, keywords, agency, output, survival, subaward, vehicle_sin, decide, cli
    print("✅ All modules imported successfully")


def test_assess_code():
    """Test the assess_code function."""
    from fedmarket.decide import assess_code
    
    result = assess_code("7030")
    assert result["code"] == "7030"
    assert result["name"] == "IT Software"
    assert result["screen_score"] == 2411
    assert result["recipient_count"] == 3916
    print("✅ assess_code(7030) works")
    
    result = assess_code("DA10")
    assert result["code"] == "DA10"
    assert result["name"] == "IT Services"
    print("✅ assess_code(DA10) works")


def test_decide_code():
    """Test the decide_code function."""
    from fedmarket.decide import decide_code
    
    # Test profile 1: leq_40k + direct + software -> 7030
    rec = decide_code("leq_40k", "direct", "software")
    assert rec["recommended_code"] == "7030"
    assert rec["entry_axis"] == "direct_sales"
    print("✅ decide_code(leq_40k, direct, software) -> 7030")
    
    # Test profile 2: leq_100k + gsa_mas + software -> DA10
    rec = decide_code("leq_100k", "gsa_mas", "software")
    assert rec["recommended_code"] == "DA10"
    assert rec["entry_axis"] == "gwac_pathway"
    print("✅ decide_code(leq_100k, gsa_mas, software) -> DA10")
    
    # Test profile 3: enterprise + services -> DA01
    rec = decide_code("enterprise", "direct", "services")
    assert rec["recommended_code"] == "DA01"
    assert rec["entry_axis"] == "services_market"
    print("✅ decide_code(enterprise, direct, services) -> DA01")
    
    # Test profile 4: subcontract -> DA10
    rec = decide_code("leq_100k", "subcontract", "software")
    assert rec["recommended_code"] == "DA10"
    print("✅ decide_code(leq_100k, subcontract, software) -> DA10")


def test_keywords():
    """Test keyword categorization."""
    from fedmarket.keywords import categorize_description, is_software
    
    assert is_software("Software license for Microsoft Office") == True
    assert is_software("Cloud SaaS subscription") == True
    assert is_software("IT consulting services") == False
    assert is_software("Hardware server purchase") == False
    print("✅ keyword categorization works")


def test_survival_data_exists():
    """Test that survival raw data exists."""
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "fedmarket", "raw")
    assert os.path.exists(os.path.join(raw_dir, "A_7030.json"))
    assert os.path.exists(os.path.join(raw_dir, "B_7030.json"))
    assert os.path.exists(os.path.join(raw_dir, "A_DA10.json"))
    assert os.path.exists(os.path.join(raw_dir, "B_DA10.json"))
    assert os.path.exists(os.path.join(raw_dir, "A_DA01.json"))
    assert os.path.exists(os.path.join(raw_dir, "B_DA01.json"))
    assert os.path.exists(os.path.join(raw_dir, "B_6810.json"))
    print("✅ Survival raw data files exist")


def _run(argv):
    """Run a fedmarket CLI entry point in a subprocess and return stdout."""
    import subprocess
    import sys
    proc = subprocess.run(
        [sys.executable, "-m"] + argv,
        capture_output=True, text=True, timeout=120,
        cwd=os.path.join(os.path.dirname(__file__), ".."),
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def test_decide_cli_scripted():
    """fedmarket-decide must work non-interactively with flags + --json."""
    import json
    cases = [
        (["--budget", "leq_40k", "--gtm", "direct", "--focus", "software", "--json"], "7030"),
        (["--budget", "leq_100k", "--gtm", "gsa_mas", "--focus", "saas", "--json"], "DA10"),
        (["--budget", "enterprise", "--gtm", "direct", "--focus", "services", "--json"], "DA01"),
        (["--budget", "leq_100k", "--gtm", "subcontract", "--focus", "software", "--json"], "DA10"),
    ]
    for argv, expected in cases:
        out = _run(["fedmarket.decide_cli"] + argv)
        rec = json.loads(out)
        assert rec["recommended_code"] == expected, (argv, rec["recommended_code"])
    print("✅ decide CLI scripted mode works")


def test_cli_survival_offline():
    """`fedmarket --code 7030 --survival` must run offline and reproduce E211."""
    out = _run(["fedmarket", "--code", "7030", "--survival"])
    assert "Survival (UEI match, raw cohort): 53.3%" in out
    assert "DEBUG" not in out
    print("✅ offline survival reproduces E211 baseline (53.3%)")


if __name__ == "__main__":
    test_imports()
    test_assess_code()
    test_decide_code()
    test_keywords()
    test_survival_data_exists()
    test_decide_cli_scripted()
    test_cli_survival_offline()
    print("\n✅ All tests passed!")