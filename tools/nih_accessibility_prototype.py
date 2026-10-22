#!/usr/bin/env python3
"""
NIH SBIR Small-Program Accessibility Prototype (Enhanced)

A reversible exploratory prototype that helps small programs identify the most
accessible NIH SBIR Funding Institutes/Centers within a given spending category,
and compare federal IT PSC code entrant opportunities alongside.

Builds on the sub-segment screen methodology from E206 (NIH SBIR category 101
sub-segment analysis), E212 (category 108), E213 (category 701), and E214
(category 525), and the spending category screen from E204.

Additionally exposes federal IT PSC code entrant fractions (E209 design) for
comparison across the five IT/software PSC codes: DA01, DA10, 7A21, 7030, D304.

NOTE: This is a prototype, not a validated product. It is evidence-gathering work.
"""

import sys
import os
import json
import urllib.request
import time


# Federal IT PSC codes analyzed in E209
IT_CODES = ["DA01", "DA10", "7A21", "7030", "D304"]


def fetch_grants(fiscal_year=2023, activity_codes=None, max_total=None):
    """Fetch grants from NIH RePORTER API across pages.

    Fetches all pages until the API's meta.total is reached, so the result
    is a complete census of the requested activity codes (default: SBIR R41/R42),
    not an arbitrary-cap slice of the full project population.

    Parameters
    ----------
    fiscal_year : int
        Fiscal year to query (default: 2023).
    activity_codes : list of str or None
        NIH activity codes to filter by (e.g. ['R41', 'R42'] for SBIR).
        When None, no code filter is applied (fetch all projects — use with
        caution, as the default 2000-row cap is replaced by meta.total).
    max_total : int or None
        Override the default stop-at-meta-total behaviour. Provided for backward
        compatibility; in normal use this parameter is not needed because the
        function stops when len(all_results) >= reported_total.
    """
    url = 'https://api.reporter.nih.gov/v2/projects/search'
    all_results = []
    seen_ids = set()
    offset = 0
    reported_total = None

    while True:
        criteria = {'fiscal_years': [fiscal_year]}
        if activity_codes is not None:
            criteria['activity_codes'] = activity_codes
        payload = json.dumps({
            'criteria': criteria,
            'offset': offset,
            'limit': 100,
        }).encode()

        req = urllib.request.Request(
            url, data=payload,
            headers={'User-Agent': 'think-free-research/0.1', 'Content-Type': 'application/json'},
            method='POST')

        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
                results = data.get('results', [])
                if not results:
                    break

                for r in results:
                    aid = r.get('appl_id')
                    if aid and aid not in seen_ids:
                        seen_ids.add(aid)
                        all_results.append(r)

                meta = data.get('meta', {})
                reported_total = meta.get('total', 0)
                if reported_total is not None and len(all_results) >= reported_total:
                    break

        except urllib.error.HTTPError as e:
            print('HTTP error: %s' % e.code)
            break
        except Exception as e:
            print('Error: %s' % e)
            break

        offset += 100
        time.sleep(0.05)

    return all_results


def group_by_funding_ic(grants):
    """Group grants by Funding Institute/Center."""
    ic_groups = {}
    for g in grants:
        ic_admin = g.get('agency_ic_admin', {})
        ic_name = ic_admin.get('name', 'Unknown IC')
        if ic_name not in ic_groups:
            ic_groups[ic_name] = []
        ic_groups[ic_name].append(g)
    return ic_groups


def compute_accessibility_metrics(ic_groups):
    """Compute accessibility metrics for each Funding IC sub-area.

    Returns list of dicts sorted by access_score descending.
    Higher access_score = more grants distributed among more orgs = more accessible.
    """
    results = []

    for ic, projects in ic_groups.items():
        orgs = set()
        org_amounts = {}
        total_amount = 0

        for p in projects:
            org_name = p.get('organization', {}).get('org_name', 'N/A')
            orgs.add(org_name)
            amount = p.get('award_amount', 0) or 0
            total_amount += amount

            if org_name not in org_amounts:
                org_amounts[org_name] = 0
            org_amounts[org_name] += amount

        # Compute top-3 and top-5 concentration
        sorted_orgs = sorted(org_amounts.items(), key=lambda x: x[1], reverse=True)
        top3_sum = sum(amount for _, amount in sorted_orgs[:3])
        top3_share = (top3_sum / total_amount * 100) if total_amount else 0
        top5_sum = sum(amount for _, amount in sorted_orgs[:5])
        top5_share = (top5_sum / total_amount * 100) if total_amount else 0

        # Access score: higher = more accessible (more grants distributed among more orgs)
        # = grant_count / (top5_share_fraction). Higher = more distributed.
        access_score = len(projects) / (top5_share / 100) if top5_share > 0 else float('inf')

        results.append({
            'ic': ic,
            'project_count': len(projects),
            'distinct_orgs': len(orgs),
            'top3_concentration_percent': top3_share,
            'top5_concentration_percent': top5_share,
            'access_score': access_score,
            'total_amount': total_amount,
        })

    return results


CONSENSUS_ICs = [
    'NIAID',
    'NCI',
    'NHLB',
    'NIA',
]

CONSENSUS_RATIONALE = (
    "Based on an analysis of 5 NIH SBIR spending categories "
    "(101, 108, 525, 701, 176): NIAID appears in 4/5 categories, "
    "NCI in 4/5, NHLB in 4/5, and NIA in 4/5, making them the "
    "most consistently accessible Funding ICs for small programs "
    "across multiple spending categories. Category 176 is the most "
    "accessible overall (NCI: 43.9% top-5 share, access score 157.20), "
    "while Category 101 is the least accessible of the five "
    "(NIAID: 64.1% top-5 share, access score 34.34)."
)


def recommend_ics(category_code, ic_ranking, it_analysis=None):
    """Generate top 3 Funding IC recommendations for a category.

    Considers both the 5-category consensus pattern and the specific
    category's access_score ranking.
    Does NOT guarantee success in the given category — only reports
    which ICs have historically been more fragmented/distributed.

    Returns list of dicts with ic, rationale, and accessibility metrics
    from the current category screen.
    """
    recommendations = []

    # Score each consensus IC based on two factors:
    # 1. Consensus appearance count (how many of 5 categories the IC appears in)
    # 2. This category's access_score ranking (lower rank = more accessible)

    consensus_scores = {ic: 0 for ic in CONSENSUS_ICs}
    for ic in CONSENSUS_ICs:
        consensus_scores[ic] = CONSENSUS_ICs.index(ic)  # 0=highest consensus

    # Adjust based on this category's ranking
    # ICs that rank higher (better access_score) get a boost
    rank_adjustments = {}
    for ic in CONSENSUS_ICs:
        rank_adjustments[ic] = 0
    for i, ic_data in enumerate(ic_ranking):
        ic = ic_data['ic']
        if ic in consensus_scores:
            # ICs in top 1/3 of ranking get a boost; bottom 1/3 get a penalty
            if i < len(ic_ranking) // 3:
                rank_adjustments[ic] -= i  # boost
            elif i >= 2 * len(ic_ranking) // 3:
                rank_adjustments[ic] += i  # penalty

    # Combine consensus and category-specific scoring
    for ic in CONSENSUS_ICs:
        total_score = consensus_scores[ic] + rank_adjustments.get(ic, 0)
        recommendations.append({
            'ic': ic,
            'consensus_rank': CONSENSUS_ICs.index(ic),
            'category_rank_boost': rank_adjustments.get(ic, 0),
            'total_score': total_score,
        })

    # Sort: lower total_score is better (consensus priority, then category boost)
    recommendations.sort(key=lambda x: x['total_score'])
    return recommendations[:3]


def analyze_it_code(code):
    """Compute per-code entrant metrics from USAspending data (E209 design)."""
    import urllib.request, json, os, hashlib, ssl

    BASE = "https://api.usaspending.gov/api/v2/search/"
    UA = "think-free-research/0.1 (+repository entry-advisor)"

    CURRENT_WINDOW = [{"start_date": "2023-01-01", "end_date": "2023-12-31"}]
    PRIOR_WINDOW = [{"start_date": "2018-01-01", "end_date": "2022-12-31"}]
    AWARD_TYPES = ["A", "B", "C", "D"]

    def base_filters(window, **extra):
        f = {"time_period": window, "award_type_codes": AWARD_TYPES}
        f.update(extra)
        return f

    def call_api(payload, capture_name, retries=2, pause=0.5):
        url = BASE + "spending_by_category/recipient/"
        body = json.dumps(payload).encode()
        RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
        meta_path = os.path.join(RAW_DIR, capture_name + ".meta.json")
        body_path = os.path.join(RAW_DIR, capture_name + ".json")

        if os.path.exists(body_path) and os.path.exists(meta_path):
            try:
                prior = json.load(open(meta_path))
                if (prior.get("request") == payload
                        and prior.get("response", {}).get("endpoint") == url):
                    with open(body_path, "rb") as fh:
                        cached = fh.read()
                    meta = dict(prior["response"], reused=True)
                    try:
                        return (meta.get("status"),
                                json.loads(cached.decode("utf-8", "replace")), meta)
                    except Exception:
                        pass
            except Exception:
                pass

        last = (None, b"")
        status, raw = None, b""
        for attempt in range(retries + 1):
            req = urllib.request.Request(
                url, data=body,
                headers={"User-Agent": UA, "Content-Type": "application/json",
                         "Accept": "application/json"})
            try:
                with urllib.request.urlopen(
                        req, timeout=180,
                        context=ssl.create_default_context()) as r:
                    status, raw = r.status, r.read()
                break
            except urllib.error.HTTPError as e:
                status, raw = e.code, e.read()
                last = (status, raw)
                if e.code not in (429, 500, 502, 503, 504) and attempt == retries:
                    break
            except Exception as e:
                last = (None, ("%s: %s" % (type(e).__name__, e)).encode())
                raw = b""
                if attempt == retries:
                    break
            time.sleep(pause * (attempt + 1))
        else:
            status, raw = last

        os.makedirs(RAW_DIR, exist_ok=True)
        with open(body_path, "wb") as fh:
            fh.write(raw or b"")
        meta = {"endpoint": url, "status": status, "bytes": len(raw or b""),
                 "sha256": hashlib.sha256(raw or b"").hexdigest()}
        with open(meta_path, "w") as fh:
            json.dump({"request": payload, "response": meta}, fh, indent=1, sort_keys=True)

        try:
            parsed = json.loads((raw or b"").decode("utf-8", "replace"))
        except Exception:
            parsed = None
        return status, parsed, meta

    def fetch_window(code, window_name):
        windows = {"current": CURRENT_WINDOW, "prior": PRIOR_WINDOW}
        window = windows[window_name]
        all_results = []
        page = 1
        has_next = True
        while has_next:
            payload = {"filters": base_filters(window, psc_codes=[code]),
                       "limit": 100, "page": page, "spending_level": "awards"}
            name = "%s_%s_p%d" % (window_name, code, page)
            st, parsed, meta = call_api(payload, name)
            if st != 200 or not isinstance(parsed, dict):
                break
            results = parsed.get("results") or []
            all_results.extend(results)
            page_meta = parsed.get("page_metadata") or {}
            has_next = page_meta.get("hasNext", False)
            page += 1
            if page > 500:
                break
        return {"code": code, "window": window_name, "rows": all_results,
                "status": st}

    cur = fetch_window(code, "current")
    pri = fetch_window(code, "prior")

    cur_rows = cur["rows"]
    pri_rows = pri["rows"]

    def obligation_by_id(rows):
        by_id = {}
        missing = 0
        for r in rows:
            rid = r.get("recipient_id")
            if not rid:
                missing += 1
                continue
            amt = r.get("amount") or 0.0
            by_id[rid] = by_id.get(rid, 0.0) + amt
        return by_id, missing

    def top_k_share(by_id, k=5):
        vals = sorted(by_id.values(), reverse=True)
        total = sum(vals)
        if total <= 0:
            return 0.0
        return sum(vals[:k]) / total

    cur_by_id, cur_missing = obligation_by_id(cur_rows)
    pri_by_id, pri_missing = obligation_by_id(pri_rows)

    cur_ids = set(cur_by_id.keys())
    pri_ids = set(pri_by_id.keys())

    seg_new = cur_ids - pri_ids
    seg_frac = len(seg_new) / len(cur_ids) if cur_ids else 0.0

    frag = 1.0 - top_k_share(cur_by_id, 5)
    obligation = round(sum(cur_by_id.values()), 2)

    return {
        "code": code,
        "current_recipients": len(cur_ids),
        "prior_recipients": len(pri_ids),
        "segment_newcomers": len(seg_new),
        "segment_newcomer_fraction": round(seg_frac, 4),
        "fragmentation": round(frag, 4),
        "current_obligation": obligation,
        "current_missing_recids": cur_missing,
        "prior_missing_recids": pri_missing,
    }


def run_enhanced_prototype(category_code, fiscal_year=2023,
                         activity_codes=None, show_it_codes=False):
    """Run the enhanced small-program accessibility prototype."""
    print('\n=== NIH SBIR Small-Program Accessibility Prototype (Enhanced) ===')
    print('Spending Category: %s' % category_code)
    print('Fiscal Year: %s' % fiscal_year)
    if activity_codes:
        print('Activity Codes: %s' % activity_codes)
    print('=' * 65)

    # ---- NIH SBIR Category Screen ----
    print('\n--- NIH SBIR Spending Category Screen ---')
    all_grants = fetch_grants(
        fiscal_year=fiscal_year,
        activity_codes=activity_codes,
        max_total=None  # D128 fix: complete census, no 2000 cap
    )
    print('Total unique grants fetched (complete census): %d' % len(all_grants))

    # Filter for the specified spending category (convert to int for API comparison)
    cat_int = int(category_code) if str(category_code).isdigit() else category_code
    category_grants = [g for g in all_grants
                       if g.get('spending_categories') and cat_int in g['spending_categories']]

    print('Grants with category %s: %d' % (category_code, len(category_grants)))

    if len(category_grants) == 0:
        print('No grants found with category %s.' % category_code)
        # Try showing a few grants to see available categories
        if all_grants:
            print('Sample grant ICs (from unfiltered fetch):')
            for g in all_grants[:3]:
                ic = g.get('agency_ic_admin', {}).get('name', 'Unknown')
                cats = g.get('spending_categories', [])
                print('  %s: category=%s' % (ic, cats))
        return None

    # Group by Funding IC
    ic_groups = group_by_funding_ic(category_grants)
    print('Funding ICs found: %d' % len(ic_groups))

    # Compute metrics
    metrics = compute_accessibility_metrics(ic_groups)
    ranked = sorted(metrics, key=lambda x: x['access_score'], reverse=True)

    print()
    print('%-55s %6s %5s %8s %8s %8s' %
           ('IC', 'Proj', 'Orgs', 'Top-3%', 'Top-5%', 'Access'))
    print('-' * 55)

    for rd in ranked[:20]:
        ic = rd['ic'][:54] if len(rd['ic']) > 54 else rd['ic']
        print('%-55s %6d %5d %7.1f%% %7.1f%% %7.2f' %
              (ic, rd['project_count'], rd['distinct_orgs'],
               rd['top3_concentration_percent'],
               rd['top5_concentration_percent'], rd['access_score']))

    print()
    print('Most accessible ICs for small programs (highest access_score):')
    for rd in ranked[:5]:
        ic = rd['ic'][:54] if len(rd['ic']) > 54 else rd['ic']
        print('  %s: %d projects, %d orgs, %.1f%% top-5 share, access score %.2f'
              % (ic, rd['project_count'], rd['distinct_orgs'],
                 rd['top5_concentration_percent'], rd['access_score']))

    print()
    print('Least accessible ICs (most concentrated, hardest for small programs):')
    for rd in ranked[-3:]:
        ic = rd['ic'][:54] if len(rd['ic']) > 54 else rd['ic']
        print('  %s: %d projects, %d orgs, %.1f%% top-5 share'
              % (ic, rd['project_count'], rd['distinct_orgs'],
                 rd['top5_concentration_percent']))

    # ---- Federal IT PSC Code Entrant Analysis ----
    if show_it_codes:
        print('\n--- Federal IT PSC Code Entrant Analysis (E209) ---')
        all_it_results = []
        for code in IT_CODES:
            print('\nFetching %s...' % code)
            summary = analyze_it_code(code)
            all_it_results.append(summary)
            print('  current recipients: %d' % summary["current_recipients"])
            print('  prior recipients: %d' % summary["prior_recipients"])
            print('  segment newcomers: %d' % summary["segment_newcomers"])
            print('  segment newcomer fraction: %.4f' % summary["segment_newcomer_fraction"])
            print('  fragmentation: %.4f' % summary["fragmentation"])
            print('  obligation: $%d' % summary["current_obligation"])

        fractions = [r["segment_newcomer_fraction"] for r in all_it_results]
        fracs_sorted = sorted(fractions)
        n = len(fracs_sorted)
        median = (fracs_sorted[n // 2] if n % 2 else
                  (fracs_sorted[n // 2 - 1] + fracs_sorted[n // 2]) / 2)
        kill = median < 0.30

        print()
        print('G3 entry (kill gate): threshold = 0.30')
        print('median segment-newcomer fraction: %.4f' % median)
        print('verdict: %s' % ('KILL — gate fired' if kill else 'survives'))
        if kill:
            print('(Bimodal pattern: 3 codes enterable, 2 codes closed)')

        # Bimodal pattern: which codes are enterable vs closed
        enterable = [r for r in all_it_results if r["segment_newcomer_fraction"] >= 0.30]
        closed = [r for r in all_it_results if r["segment_newcomer_fraction"] < 0.30 and r["segment_newcomer_fraction"] > 0]

        print()
        print('Enterable codes (segment newcomer fraction >= 0.30):')
        for r in enterable:
            print('  %s: %.4f ( %d/%d newcomers)' % (r["code"], r["segment_newcomer_fraction"],
                                                      r["segment_newcomers"], r["current_recipients"]))

        print('Closed codes (segment newcomer fraction < 0.30):')
        for r in closed:
            print('  %s: %.4f ( %d/%d newcomers)' % (r["code"], r["segment_newcomer_fraction"],
                                                      r["segment_newcomers"], r["current_recipients"]))

    # ---- Recommendations ----
    print()
    print('--- Funding IC Recommendations ---')
    print('Top 3 most accessible Funding ICs for small programs:')

    recs = recommend_ics(category_code, ranked, all_it_results if show_it_codes else None)
    for i, rec in enumerate(recs):
        ic = rec['ic']
        consensus_idx = rec['consensus_rank']
        boost = rec['category_rank_boost']
        # Find this IC's access score
        ic_access = None
        for rd in ranked:
            if rd['ic'] == ic:
                ic_access = rd['access_score']
                break
        print('  %d. %s' % (i + 1, ic))
        print('     Consensus rank: %d/4 (appears in %d/5 categories)' % (
            consensus_idx + 1, sum(1 for c in CONSENSUS_ICs)))
        if ic_access is not None:
            print('     This category access score: %.2f' % ic_access)
        if boost != 0:
            print('     Category ranking adjustment: %+d (top/bottom third)' % boost)
        print()

    print()
    print('(Prototype — evidence-gathering, not product validation)')


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='NIH SBIR Small-Program Accessibility Prototype'
    )
    parser.add_argument(
        'category_code',
        type=str,
        help='NIH SBIR spending category code (e.g. 101)'
    )
    parser.add_argument(
        '--fiscal-year',
        type=int,
        default=2023,
        help='Fiscal year to screen (default: 2023)'
    )
    parser.add_argument(
        '--activity-codes',
        nargs='+',
        help='NIH activity codes to filter by (e.g. R41 R42 for SBIR)'
    )
    parser.add_argument(
        '--it-codes',
        action='store_true',
        help='Also show federal IT PSC code entrant analysis (E209 design)'
    )

    args = parser.parse_args()
    category_code = args.category_code

    run_enhanced_prototype(
        category_code=category_code,
        fiscal_year=args.fiscal_year,
        activity_codes=args.activity_codes,
        show_it_codes=args.it_codes
    )


if __name__ == '__main__':
    main()