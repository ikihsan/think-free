#!/usr/bin/env python3
"""fedmarket Agency distribution module (E205)."""

from collections import Counter, defaultdict
from .api import call, base_filters, FULL_WINDOW
from .keywords import is_software


def category_all(category, psc_code, max_pages=100, capture_prefix="cat"):
    """Fetch all pages of a spending_by_category endpoint."""
    all_results = []
    page = 1
    statuses = []
    while page <= max_pages:
        payload = {
            "filters": base_filters(psc_codes=[psc_code], time_period=FULL_WINDOW),
            "limit": 100,
            "page": page,
            "spending_level": "awards"
        }
        capture_name = "%s_%s_%s_p%d" % (capture_prefix, category, psc_code, page)
        st, parsed, meta = call(f"spending_by_category/{category}/", payload, capture_name)
        statuses.append({"page": page, "status": st, "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        if not parsed.get("page_metadata", {}).get("hasNext", False):
            break
        page += 1
    return all_results, statuses


def analyze_recipient_stats(all_awards):
    """Analyze awards for recipient patterns (E205 style)."""
    recipient_stats = defaultdict(lambda: {
        "awards": 0, "obligation": 0,
        "software_awards": 0, "software_obligation": 0,
        "small_awards": 0, "small_obligation": 0,
    })

    for award in all_awards:
        recip = award.get("Recipient Name") or "Unknown"
        amount = award.get("Award Amount", 0) or 0
        desc = award.get("Description", "") or ""
        is_sw = is_software(desc)
        is_small = amount <= 100000

        r = recipient_stats[recip]
        r["awards"] += 1
        r["obligation"] += amount
        if is_sw:
            r["software_awards"] += 1
            r["software_obligation"] += amount
        if is_small:
            r["small_awards"] += 1
            r["small_obligation"] += amount

    return dict(recipient_stats)