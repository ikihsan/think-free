#!/usr/bin/env python3
"""Core assessment function for PSC code analysis.

Wraps E206 modules to provide a unified assessment of a PSC code
for small-team software entry into the federal marketplace.

Usage:
    from usaspending_assess.assess import assess_code
    result = assess_code("7030")
"""

import sys
import os

# Ensure the E206 modules are importable from this package context
_HERE = os.path.dirname(os.path.abspath(__file__))
_E206_DIR = os.path.join(os.path.dirname(_HERE), "EXPERIMENTS", "E206-integrated-cli-tool")
if os.path.isdir(_E206_DIR) and _E206_DIR not in sys.path:
    sys.path.insert(0, _E206_DIR)

from e206_api import call, base_filters, RECENT_WINDOW, FULL_WINDOW
from e206_recipient import recipient_all, analyze_recipients
from e206_output import print_recipient_summary, print_award_categorization, print_time_window_comparison
from e206_award import award_all, analyze_awards, categorize_description, is_software
from e206_agency import category_all
from e206_vehicle_sin import vehicle_sin_all, analyze_vehicle_sin
from e206_survival import main as survival_main, load_json


def _fetch_recipient(psc_code):
    """Run recipient analysis for a PSC code."""
    all_recipients, _, _ = recipient_all(psc_code)
    return analyze_recipients(all_recipients)


def _fetch_award(psc_code, max_pages):
    """Run full-period award analysis for a PSC code."""
    all_awards, _, _ = award_all(psc_code, max_pages=max_pages, capture_prefix="award_full")
    return analyze_awards(all_awards)


def _fetch_recent_award(psc_code, max_pages):
    """Run recent-period award analysis for a PSC code."""
    recent_awards, _, _ = award_all(psc_code, max_pages=max_pages, capture_prefix="award_recent")
    return analyze_awards(recent_awards)


def _fetch_agency(psc_code):
    """Run agency distribution analysis for a PSC code."""
    funding_agencies, _ = category_all("funding_agency", psc_code)
    awarding_agencies, _ = category_all("awarding_agency", psc_code)
    federal_accounts, _ = category_all("federal_account", psc_code)
    return funding_agencies, awarding_agencies, federal_accounts


def _fetch_vehicle_sin(psc_code, max_pages):
    """Run vehicle SIN/SEWP analysis for a PSC code."""
    all_awards, _ = vehicle_sin_all(psc_code, max_pages=max_pages, capture_prefix="vehicle_sin")
    return analyze_vehicle_sin(all_awards)


def _fetch_survival(psc_code):
    """Run entry survival analysis for a PSC code."""
    import_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "EXPERIMENTS", "E206-integrated-cli-tool", "raw")
    return survival_main(psc_code, import_path)


def assess_code(psc_code, max_pages=50):
    """Assess a PSC code for small-team software entry.

    Runs the full E206 assessment framework: recipient analysis,
    award categorization, time-window comparison, agency distribution,
    and vehicle SIN/SEWP analysis.

    Args:
        psc_code: PSC code string (e.g., "7030", "DA10")
        max_pages: Maximum API pages to fetch per query (default 50)

    Returns:
        dict with keys: recipient, award, time, agency, vehicle_sin, survival
    """
    psc_code = psc_code.strip()

    # Recipient analysis (E202)
    recipient_analysis = _fetch_recipient(psc_code)

    # Full-period award categorization (E203)
    full_analysis = _fetch_award(psc_code, max_pages)

    # Time-window comparison (E204)
    recent_analysis = _fetch_recent_award(psc_code, max_pages)

    # Agency distribution (E205)
    funding_agencies, awarding_agencies, federal_accounts = _fetch_agency(psc_code)

    # Vehicle SIN/SEWP analysis (E210)
    vehicle_sin_analysis = _fetch_vehicle_sin(psc_code, max_pages)

    # Entry survival analysis (E211)
    survival_result = _fetch_survival(psc_code)

    return {
        "recipient": recipient_analysis,
        "award": full_analysis,
        "time": recent_analysis,
        "agency": {
            "funding_agencies": funding_agencies,
            "awarding_agencies": awarding_agencies,
            "federal_accounts": federal_accounts,
        },
        "vehicle_sin": vehicle_sin_analysis,
        "survival": survival_result,
    }