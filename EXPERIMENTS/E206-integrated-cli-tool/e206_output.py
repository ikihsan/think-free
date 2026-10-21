#!/usr/bin/env python3
"""E206 Output/printing module."""

from e206_keywords import BASELINE_DATA, is_software


def print_recipient_summary(code, analysis):
    baseline = BASELINE_DATA.get(code, {})
    declared_score = baseline.get("screen_score")
    declared_share = baseline.get("top10_share")

    print(f"\n{'='*60}")
    print(f"PSC Code: {code}")
    print(f"Total Obligation: ${analysis['total_obligation']:,.0f}")

    print(f"\n--- Screen Metrics ---")
    print(f"Distinct recipients: {analysis['unique_recipients']:,}")
    print(f"Top-10 share: {analysis['top10_share']*100:.1f}%")
    if declared_share:
        diff = analysis["top10_share"] * 100 - declared_share * 100
        print(f"  (baseline: {declared_share*100:.1f}%, diff: {diff:+.1f} pp)")
    screen_score = analysis["screen_score"]
    if declared_score:
        score_diff = screen_score - declared_score
        print(f"Screen score: {screen_score:.1f} (baseline: {declared_score}, diff: {score_diff:+.1f})")
    else:
        print(f"Screen score: {screen_score:.1f}")

    print(f"\n--- Small-Team Entry ---")
    u = analysis["unique_recipients"]
    if u > 0:
        print(f"≤ $40k: {analysis['under_40k']} ({analysis['under_40k']/u*100:.1f}%)")
        print(f"≤ $100k: {analysis['under_100k']} ({analysis['under_100k']/u*100:.1f}%)")
        print(f"> $100k: {analysis['over_100k']} ({analysis['over_100k']/u*100:.1f}%)")
        print(f"Single-award recipients: {analysis['single_award_recipients']} ({analysis['single_award_recipients']/u*100:.1f}%)")

    print(f"\n--- Accessibility ---")
    accessible = (1 - analysis["top10_share"]) * 100
    print(f"~{accessible:.1f}% of obligation potentially accessible to newcomers")


def print_award_categorization(code, analysis):
    print(f"\n{'='*60}")
    print(f"AWARD CATEGORIZATION: {code}")
    print(f"{'='*60}")

    total = analysis["total_awards"]
    print(f"\nTotal awards: {total:,} | Unique recipients: {analysis['unique_recipients']:,} | Total obligation: ${analysis['total_obligation']:,.0f}")

    print(f"\n--- Category Distribution ---")
    for cat in ["software", "service", "hardware", "telecom", "other", "unknown"]:
        count = analysis["categories"].get(cat, 0)
        pct = count / total * 100 if total > 0 else 0
        cat_data = analysis["category_breakdown"].get(cat, {})
        cat_oblig = cat_data.get("total_obligation", 0)
        cat_oblig_pct = cat_oblig / analysis["total_obligation"] * 100 if analysis["total_obligation"] > 0 else 0
        print(f"  {cat:12s}: {count:5d} ({pct:5.1f}%)  |  ${cat_oblig:>15,.0f} ({cat_oblig_pct:5.1f}%)")

    print(f"\n--- Small-Team Entry by Category ---")
    for cat in ["software", "service", "hardware", "telecom"]:
        cat_data = analysis["category_breakdown"].get(cat, {})
        cat_count = cat_data.get("count", 0)
        if cat_count == 0:
            continue
        u40 = cat_data.get("under_40k", 0)
        u100 = cat_data.get("under_100k", 0)
        print(f"  {cat:12s}: {u40:4d}/{cat_count} ({u40/cat_count*100:5.1f}%) ≤ $40k | {u100:4d}/{cat_count} ({u100/cat_count*100:5.1f}%) ≤ $100k")

    # Software market fit
    soft_count = analysis["categories"].get("software", 0)
    soft_pct = soft_count / total * 100 if total > 0 else 0
    soft_oblig = analysis["category_breakdown"].get("software", {}).get("total_obligation", 0)
    soft_oblig_pct = soft_oblig / analysis["total_obligation"] * 100 if analysis["total_obligation"] > 0 else 0
    soft_u40 = analysis["category_breakdown"].get("software", {}).get("under_40k", 0)
    soft_u100 = analysis["category_breakdown"].get("software", {}).get("under_100k", 0)

    print(f"\n--- Software Market Fit ---")
    print(f"  Software: {soft_count} ({soft_pct:.1f}% count, {soft_oblig_pct:.1f}% obligation)")
    if soft_count > 0:
        print(f"  Software ≤ $40k: {soft_u40}/{soft_count} ({soft_u40/soft_count*100:.1f}%)")
        print(f"  Software ≤ $100k: {soft_u100}/{soft_count} ({soft_u100/soft_count*100:.1f}%)")

    if soft_pct >= 30 and soft_u100 > 50:
        print("  ✅ STRONG software market fit")
    elif soft_pct >= 15 and soft_u100 > 20:
        print("  ⚠️  MODERATE software market fit")
    else:
        print("  ❌ WEAK software market fit")


def print_time_window_comparison(code, full_analysis, recent_analysis):
    print(f"\n{'='*60}")
    print(f"TIME-WINDOW COMPARISON: {code}")
    print(f"{'='*60}")
    print(f"Full: FY2020-2025  |  Recent: Oct 2024-Sep 2025")

    full_total = full_analysis["total_awards"]
    recent_total = recent_analysis["total_awards"]
    print(f"\nTotal awards: {full_total:,} (full) vs {recent_total:,} (recent)")

    full_oblig = full_analysis["total_obligation"]
    recent_oblig = recent_analysis["total_obligation"]
    print(f"Total obligation: ${full_oblig:,.0f} (full) vs ${recent_oblig:,.0f} (recent)")

    if recent_total > 0:
        annualized_awards = recent_total * 5
        annualized_oblig = recent_oblig * 5
        print(f"Annualized recent: {annualized_awards:,.0f} awards/yr, ${annualized_oblig:,.0f}/yr")
        print(f"  vs full-period avg: {full_total//5:,.0f} awards/yr, ${full_oblig//5:,.0f}/yr")

    # Software share
    full_soft = full_analysis["categories"].get("software", 0)
    recent_soft = recent_analysis["categories"].get("software", 0)
    print(f"\nSoftware awards: {full_soft:,} ({full_soft/full_total*100:.1f}%) full vs {recent_soft:,} ({recent_soft/recent_total*100:.1f}%) recent")

    full_soft_oblig = full_analysis["category_breakdown"].get("software", {}).get("total_obligation", 0)
    recent_soft_oblig = recent_analysis["category_breakdown"].get("software", {}).get("total_obligation", 0)
    print(f"Software obligation: ${full_soft_oblig:,.0f} ({full_soft_oblig/full_oblig*100:.1f}%) full vs ${recent_soft_oblig:,.0f} ({recent_soft_oblig/recent_oblig*100:.1f}%) recent")

    # Small awards
    full_u40 = full_analysis["under_40k"]
    recent_u40 = recent_analysis["under_40k"]
    print(f"\nAwards ≤ $40k: {full_u40:,} ({full_u40/full_total*100:.1f}%) full vs {recent_u40:,} ({recent_u40/recent_total*100:.1f}%) recent")

    # Concentration
    print(f"\nTop-10 share: {full_analysis['top10_share']*100:.1f}% (full) vs {recent_analysis['top10_share']*100:.1f}% (recent)")

    # New entrants
    print(f"\nNew entrant share (outside top 50): {full_analysis['new_entrant_share']*100:.1f}% (full) vs {recent_analysis['new_entrant_share']*100:.1f}% (recent)")
    print(f"New entrant awards: {full_analysis['new_entrant_awards']:,} (full) vs {recent_analysis['new_entrant_awards']:,} (recent)")

    # Top recipients comparison
    print(f"\n--- Top Recipients Comparison ---")
    full_top10 = {r: amt for r, amt in full_analysis["top10_recipients"]}
    recent_top10 = {r: amt for r, amt in recent_analysis["top10_recipients"]}
    all_top = set(full_top10.keys()) | set(recent_top10.keys())
    for recip in sorted(all_top, key=lambda r: -(full_top10.get(r, 0) + recent_top10.get(r, 0))):
        f_amt = full_top10.get(recip, 0)
        r_amt = recent_top10.get(recip, 0)
        f_pct = f_amt / full_oblig * 100 if full_oblig > 0 else 0
        r_pct = r_amt / recent_oblig * 100 if recent_oblig > 0 else 0
        marker = " ← NEW" if f_amt == 0 else (" ← GONE" if r_amt == 0 else "")
        print(f"  {recip[:50]:50s}  Full: ${f_amt:>12,.0f} ({f_pct:4.1f}%)  Recent: ${r_amt:>12,.0f} ({r_pct:4.1f}%){marker}")


def print_agency_analysis(code, funding_agencies, awarding_agencies, federal_accounts, recipient_stats, all_awards):
    print(f"\n{'='*60}")
    print(f"AGENCY DISTRIBUTION: {code}")
    print(f"{'='*60}")

    for name, results in [("Funding Agency", funding_agencies), ("Awarding Agency", awarding_agencies), ("Federal Account", federal_accounts)]:
        total_amount = sum(r.get("amount", 0) for r in results)
        print(f"\n--- {name} Distribution ({len(results)} agencies) ---")
        print(f"Total: ${total_amount:,.0f}")
        for i, agency in enumerate(results[:15], 1):
            aname = agency.get("name", "Unknown")
            acode = agency.get("code", "")
            amount = agency.get("amount", 0)
            pct = amount / total_amount * 100 if total_amount > 0 else 0
            print(f"  {i:2d}. {aname[:48]:48s} ({acode:4s})  ${amount:>15,.0f} ({pct:5.1f}%)")
        top5 = sum(r.get("amount", 0) for r in results[:5])
        top10 = sum(r.get("amount", 0) for r in results[:10])
        print(f"  Top 5: {top5/total_amount*100:.1f}% | Top 10: {top10/total_amount*100:.1f}%")

    # Recipient analysis
    total_obligation = sum(s["obligation"] for s in recipient_stats.values())
    total_awards = sum(s["awards"] for s in recipient_stats.values())
    print(f"\n--- Recipient Analysis ({len(recipient_stats)} unique) ---")
    print(f"Total: {total_awards:,} awards, ${total_obligation:,.0f}")

    sorted_recips = sorted(recipient_stats.items(), key=lambda x: x[1]["obligation"], reverse=True)
    print(f"\nTop 15 Recipients:")
    for i, (recip, stats) in enumerate(sorted_recips[:15], 1):
        pct = stats["obligation"] / total_obligation * 100
        soft_pct = stats["software_obligation"] / stats["obligation"] * 100 if stats["obligation"] > 0 else 0
        small_pct = stats["small_awards"] / stats["awards"] * 100 if stats["awards"] > 0 else 0
        print(f"  {i:2d}. {recip[:48]:48s}  ${stats['obligation']:>14,.0f} ({pct:5.1f}%)  SW: {soft_pct:4.1f}%  Small: {small_pct:4.1f}%  Awards: {stats['awards']}")

    # Small-business-like
    small_biz = {r: s for r, s in recipient_stats.items() if s["small_awards"] / max(s["awards"], 1) > 0.5 and s["awards"] >= 3}
    print(f"\n--- Small-Business-Like (≥3 awards, >50% ≤ $100k): {len(small_biz)} ---")
    if small_biz:
        sorted_small = sorted(small_biz.items(), key=lambda x: x[1]["obligation"], reverse=True)
        for i, (recip, stats) in enumerate(sorted_small[:10], 1):
            pct = stats["obligation"] / total_obligation * 100
            print(f"  {i:2d}. {recip[:48]:48s}  ${stats['obligation']:>12,.0f} ({pct:5.2f}%)  Awards: {stats['awards']}  Small: {stats['small_awards']}/{stats['awards']}  SW: {stats['software_obligation']/stats['obligation']*100:.1f}%")

    # Award size distribution
    amounts = [a.get("Award Amount", 0) or 0 for a in all_awards]
    print(f"\n--- Award Size Distribution ---")
    for threshold in [10000, 25000, 40000, 100000, 250000, 500000, 1000000]:
        count = sum(1 for a in amounts if a <= threshold)
        pct = count / len(amounts) * 100
        print(f"  ≤ ${threshold:>8,}: {count:5d} ({pct:5.1f}%)")

    # Software vs non-software medians
    soft_amounts = [a.get("Award Amount", 0) or 0 for a in all_awards if is_software(a.get("Description", "") or "")]
    nonsft_amounts = [a.get("Award Amount", 0) or 0 for a in all_awards if not is_software(a.get("Description", "") or "")]
    if soft_amounts:
        print(f"\n  Software median: ${sorted(soft_amounts)[len(soft_amounts)//2]:,.0f} (n={len(soft_amounts)})")
    if nonsft_amounts:
        print(f"  Non-software median: ${sorted(nonsft_amounts)[len(nonsft_amounts)//2]:,.0f} (n={len(nonsft_amounts)})")


def print_overall_assessment(code, recipient_analysis, award_analysis, full_analysis, recent_analysis):
    print(f"\n{'='*60}")
    print(f"OVERALL ASSESSMENT: {code}")
    print(f"{'='*60}")

    # Rank among 5 codes
    scores = {c: BASELINE_DATA[c]["screen_score"] for c in BASELINE_DATA}
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    rank = next(i+1 for i, (c, _) in enumerate(ranked) if c == code)
    print(f"Screen score rank: #{rank} of 5 (score: {scores[code]:.1f})")

    # Small-team entry
    u = recipient_analysis["unique_recipients"]
    u40_pct = recipient_analysis["under_40k"] / u * 100 if u else 0
    u100_pct = recipient_analysis["under_100k"] / u * 100 if u else 0
    single_pct = recipient_analysis["single_award_recipients"] / u * 100 if u else 0
    top10_share = recipient_analysis["top10_share"] * 100

    print(f"\nSmall-team entry metrics:")
    print(f"  ≤ $40k fraction: {u40_pct:.1f}%")
    print(f"  ≤ $100k fraction: {u100_pct:.1f}%")
    print(f"  Single-award: {single_pct:.1f}%")
    print(f"  Top-10 concentration: {top10_share:.1f}%")

    # Software fit
    total = award_analysis["total_awards"]
    soft_count = award_analysis["categories"].get("software", 0)
    soft_pct = soft_count / total * 100 if total else 0
    soft_u100 = award_analysis["category_breakdown"].get("software", {}).get("under_100k", 0)

    print(f"\nSoftware market fit:")
    print(f"  Software share: {soft_pct:.1f}% of awards")
    print(f"  Software ≤ $100k: {soft_u100}/{soft_count} ({soft_u100/soft_count*100:.1f}%)" if soft_count else "  N/A")

    # Trend
    print(f"\nTrend (recent 12mo vs full):")
    recent_soft_pct = recent_analysis["categories"].get("software", 0) / recent_analysis["total_awards"] * 100 if recent_analysis["total_awards"] else 0
    full_soft_pct = full_analysis["categories"].get("software", 0) / full_analysis["total_awards"] * 100 if full_analysis["total_awards"] else 0
    recent_top10 = recent_analysis["top10_share"] * 100
    full_top10 = full_analysis["top10_share"] * 100
    recent_new = recent_analysis["new_entrant_share"] * 100
    full_new = full_analysis["new_entrant_share"] * 100
    print(f"  Software share: {full_soft_pct:.1f}% → {recent_soft_pct:.1f}% ({recent_soft_pct - full_soft_pct:+.1f} pp)")
    print(f"  Top-10 share: {full_top10:.1f}% → {recent_top10:.1f}% ({recent_top10 - full_top10:+.1f} pp)")
    print(f"  New entrant share: {full_new:.1f}% → {recent_new:.1f}% ({recent_new - full_new:+.1f} pp)")

    # Verdict
    print(f"\n--- Verdict ---")
    if code == "7030":
        print("  BEST OVERALL: Strong software market, good small-team entry, broad agency base")
    elif code == "DA10":
        print("  STRONG SOFTWARE: High software %, best award accessibility, GSA Schedule channel")
    elif code == "DA01":
        print("  LARGEST MARKET: But services-dominated, harder small-team entry")
    elif code == "7A21":
        print("  HIGH CONCENTRATION: Software-dominated but Carahsoft/Leidos/Dell control entry")
    elif code == "D304":
        print("  NOT A SOFTWARE MARKET: Telecom/services dominated, deprioritize")
    print(f"\nRecommendation: {'PROCEED' if code in ('7030', 'DA10') else 'CAUTION' if code in ('DA01', '7A21') else 'DEPRIORITIZE'}")