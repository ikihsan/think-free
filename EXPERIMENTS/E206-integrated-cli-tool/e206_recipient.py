#!/usr/bin/env python3
"""E206 Recipient analysis module (E202)."""

from collections import Counter
from e206_api import call, base_filters, FULL_WINDOW, unused_filter_messages


def recipient_page(psc_code, page, limit=100, capture_prefix="recip"):
    payload = {
        "filters": base_filters(psc_codes=[psc_code], time_period=FULL_WINDOW),
        "limit": limit,
        "page": page,
        "spending_level": "awards"
    }
    capture_name = "%s_%s_p%d" % (capture_prefix, psc_code, page)
    return call("spending_by_category/recipient/", payload, capture_name)


def recipient_all(psc_code, capture_prefix="recip"):
    all_results = []
    page = 1
    statuses = []
    unused_filters = []
    while True:
        st, parsed, meta = recipient_page(psc_code, page, capture_prefix=capture_prefix)
        statuses.append({"page": page, "status": st, "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        unused_filters.extend(unused_filter_messages(parsed))
        page += 1
        if page > 100:
            print("WARNING: Reached page limit of 100, stopping")
            break
    return all_results, statuses, unused_filters


def analyze_recipients(all_recipients):
    total_recipients = len(all_recipients)
    recipient_ids = [r.get('recipient_id', '') for r in all_recipients]
    unique_recipient_ids = set(recipient_ids)
    num_unique = len(unique_recipient_ids)

    amounts = [r.get('amount', 0) or 0 for r in all_recipients]
    total_obligation = sum(amounts)
    median_obligation = sorted(amounts)[len(amounts) // 2] if amounts else 0

    under_40k = sum(1 for a in amounts if a <= 40000)
    under_100k = sum(1 for a in amounts if a <= 100000)
    over_100k = sum(1 for a in amounts if a > 100000)

    id_counts = Counter(recipient_ids)
    single_award_recipients = sum(1 for count in id_counts.values() if count == 1)
    multi_award_recipients = sum(1 for count in id_counts.values() if count > 1)

    top10 = sorted(all_recipients, key=lambda r: r.get('amount', 0) or 0, reverse=True)[:10]
    top10_total = sum(r.get('amount', 0) or 0 for r in top10)
    top10_share = top10_total / total_obligation if total_obligation > 0 else 0

    screen_score = num_unique * (1 - top10_share)

    return {
        "total_recipients": total_recipients,
        "unique_recipients": num_unique,
        "total_obligation": total_obligation,
        "median_obligation": median_obligation,
        "under_40k": under_40k,
        "under_100k": under_100k,
        "over_100k": over_100k,
        "top10_share": top10_share,
        "single_award_recipients": single_award_recipients,
        "multi_award_recipients": multi_award_recipients,
        "screen_score": screen_score,
        "amounts": amounts
    }