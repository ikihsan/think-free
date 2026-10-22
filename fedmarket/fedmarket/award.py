#!/usr/bin/env python3
"""fedmarket Award analysis module (E203/E204)."""

from collections import Counter
from .api import call, base_filters, FULL_WINDOW, RECENT_WINDOW, unused_filter_messages
from .keywords import AWARD_FIELDS, categorize_description, is_software


def award_page(psc_code, page, limit=100, time_window=FULL_WINDOW, capture_prefix="award"):
    payload = {
        "fields": AWARD_FIELDS,
        "filters": base_filters(psc_codes=[psc_code], time_period=time_window),
        "limit": limit,
        "page": page,
    }
    capture_name = "%s_%s_p%d" % (capture_prefix, psc_code, page)
    return call("spending_by_award/", payload, capture_name)


def award_all(psc_code, time_window=FULL_WINDOW, max_pages=50, capture_prefix="award"):
    all_results = []
    page = 1
    statuses = []
    unused_filters = []
    while page <= max_pages:
        st, parsed, meta = award_page(psc_code, page, time_window=time_window, capture_prefix=capture_prefix)
        statuses.append({"page": page, "status": st, "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        unused_filters.extend(unused_filter_messages(parsed))
        if not parsed.get("page_metadata", {}).get("hasNext", False):
            break
        page += 1
    return all_results, statuses, unused_filters


def analyze_awards(all_awards):
    total_awards = len(all_awards)
    amounts = [a.get("Award Amount", 0) or 0 for a in all_awards]
    total_obligation = sum(amounts)
    median_obligation = sorted(amounts)[len(amounts) // 2] if amounts else 0

    categories = []
    for award in all_awards:
        desc = award.get("Description", "") or ""
        cat = categorize_description(desc)
        categories.append(cat)
        award["_category"] = cat

    cat_counts = Counter(categories)

    under_40k = sum(1 for a in amounts if a <= 40000)
    under_100k = sum(1 for a in amounts if a <= 100000)
    over_100k = sum(1 for a in amounts if a > 100000)

    cat_by_size = {}
    for cat in ["software", "service", "hardware", "telecom", "other", "unknown"]:
        cat_awards = [a for a in all_awards if a.get("_category") == cat]
        cat_amounts = [a.get("Award Amount", 0) or 0 for a in cat_awards]
        cat_by_size[cat] = {
            "count": len(cat_awards),
            "total_obligation": sum(cat_amounts),
            "median_obligation": sorted(cat_amounts)[len(cat_amounts) // 2] if cat_amounts else 0,
            "under_40k": sum(1 for a in cat_amounts if a <= 40000),
            "under_100k": sum(1 for a in cat_amounts if a <= 100000),
        }

    recipient_obligations = {}
    for award in all_awards:
        recip = award.get("Recipient Name", "Unknown")
        amt = award.get("Award Amount", 0) or 0
        recipient_obligations[recip] = recipient_obligations.get(recip, 0) + amt
    top10_recipients = sorted(recipient_obligations.items(), key=lambda x: x[1], reverse=True)[:10]
    top10_total = sum(amt for _, amt in top10_recipients)
    top10_share = top10_total / total_obligation if total_obligation > 0 else 0
    unique_recipients = len(recipient_obligations)

    # New entrant analysis (for time-window)
    top50_recipients = set(r for r, _ in sorted(recipient_obligations.items(), key=lambda x: x[1], reverse=True)[:50])
    new_entrant_awards = [a for a in all_awards if a.get("Recipient Name", "Unknown") not in top50_recipients]
    new_entrant_count = len(new_entrant_awards)
    new_entrant_obligation = sum(a.get("Award Amount", 0) or 0 for a in new_entrant_awards)

    return {
        "total_awards": total_awards,
        "unique_recipients": unique_recipients,
        "total_obligation": total_obligation,
        "median_obligation": median_obligation,
        "under_40k": under_40k,
        "under_100k": under_100k,
        "over_100k": over_100k,
        "categories": dict(cat_counts),
        "category_breakdown": cat_by_size,
        "top10_share": top10_share,
        "top10_recipients": top10_recipients,
        "new_entrant_awards": new_entrant_count,
        "new_entrant_obligation": new_entrant_obligation,
        "new_entrant_share": new_entrant_obligation / total_obligation if total_obligation > 0 else 0,
        "amounts": amounts,
    }