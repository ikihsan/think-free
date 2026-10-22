        # Linear interpolation between 40k and 100k
        # e.g. at $60k roughly halfway between 40k and 100k
        fraction = (threshold_dollars - 40000) / (100000 - 40000)
        projected = leq_40k + fraction * (leq_100k - leq_40k)
        return float(round(projected, 1))


def decide_code(team_budget: str, team_gtm: str, team_focus: str) -> Dict[str, Any]:
    """Recommend a PSC code and entry strategy based on team characteristics.

    Uses the project's two-axis framework: Axis 1 (accessibility) vs Axis 2
    (business sustainability). Matches team profile to the code that best
    supports their goals.

    Parameters
    ----------
    team_budget : str
        "leq_40k" — targeting deals under $40k (easier entry, faster cycles)
        "leq_100k" — targeting deals under $100k (moderate ambition)
        "enterprise" — targeting enterprise deals ($100k+)
    team_gtm : str
        "direct" — building direct sales capability
        "gsa_mas" — pursuing GSA Schedule/MAS contracting
        "subcontract" — subcontracting to large primes
    team_focus : str
        "software" — pure software product
        "saas" — SaaS or cloud service
        "services" — integration, consulting, IT services

    Returns
    -------
    dict with keys: recommended_code, entry_axis, primary_vehicle,
        rationale, next_steps
    """
    # Assess all codes — static lookup data (screen metrics only)
    results: Dict[str, Any] = {}
    for code in _CODES:
        try:
            results[code] = assess_code(code)
        except KeyError:
            pass

    # Axis 1 scores (accessibility): screen score, <=40k access, recipients, software %
    axis1: Dict[str, float] = {}
    # Axis 2 scores (sustainability): use known graduation rates as proxy
    axis2: Dict[str, float] = {}

    for code in results:
        r = results[code]
        leq_40k = r["leq_40k_pct"]
        screen = r["screen_score"]
        recipients = r["recipient_count"]
        software = r["software_pct_awards"]

        # Normalize axis 1 (0-100 scale)
        score_min, score_max = 490, 2411
        n_norm = ((screen - score_min) / (score_max - score_min)) * 100 if screen else 0
        access_norm = leq_40k
        software_norm = software

        axis1[code] = round(0.4 * n_norm + 0.3 * access_norm + 0.3 * software_norm, 1)

        # Axis 2: use known graduation rates from E211 data
        axis2[code] = known_graduation.get(code, 0)

    # Score each code against the team profile
    code_scores: Dict[str, float] = {}

    for code, a1 in axis1.items():
        a2 = axis2.get(code, 0)
        score = a1 * 0.5 + a2 * 0.5  # Equal weight
        code_scores[code] = score

    # Sort by score (descending)
    sorted_codes = sorted(code_scores.items(), key=lambda item: item[1], reverse=True)

    top_code = sorted_codes[0][0] if sorted_codes else None
    top_score = sorted_codes[0][1] if sorted_codes else 0

    # Team-profile-driven selection overrides
    budget = team_budget.lower().strip()
    gtm = team_gtm.lower().strip()
    focus = team_focus.lower().strip()

    # Apply profile preferences to override pure scoring
    if budget == "leq_40k" and gtm == "direct" and focus in ("software", "saas"):
        if "7030" in code_scores:
            top_code = "7030"
            code_scores["7030"] = code_scores.get("7030", 0) + 20
    elif budget == "leq_100k" and gtm == "gsa_mas" and focus in ("software", "saas"):
        if "DA10" in code_scores:
            top_code = "DA10"
            code_scores["DA10"] = code_scores.get("DA10", 0) + 20
    elif budget == "enterprise" and focus == "services":
        if "DA01" in code_scores:
            top_code = "DA01"
            code_scores["DA01"] = code_scores.get("DA01", 0) + 20
    elif gtm == "subcontract":
        if "DA10" in code_scores:
            top_code = "DA10"
            code_scores["DA10"] = code_scores.get("DA10", 0) + 15
        elif "7A21" in code_scores:
            top_code = "7A21"
            code_scores["7A21"] = code_scores.get("7A21", 0) + 15

    if top_code and top_code in results:
        r = results[top_code]
        rec_entry = r["recommendation"]
        rec = {
            "entry_axis": rec_entry["entry_axis"],
            "primary_vehicle": rec_entry["primary_vehicle"],
            "caveats": rec_entry["caveats"],
        }

        # Generate rationale based on code
        leq_40k = r["leq_40k_pct"]
        screen = r["screen_score"]
        recipients = r["recipient_count"]
        software = r["software_pct_awards"]

        if top_code == "7030":
            rationale = (
                f"7030 is your best entry point: {recipients} distinct recipients, "
                f"{leq_40k}% of software awards ≤ $40k, 64.5% software awards. "
                f"Small vendors sell direct (88.7%). Ideal for teams prioritizing "
                f"quick market entry and early revenue. This code has the lowest "
                f"sustainability rate — only 13.8% graduation after 3 years — so "
                f"use it as a beachhead to build case studies and references, then "
                f"consider migrating to a sustainability-favorable code like DA10."
            )
            next_steps = [
                "Build direct sales capability targeting 3,916 small-recipient organizations",
                "Identify Carahsoft/DLT/CDW/Four LLC as initial subcontract partners",
                "Target agencies: DOD (44.5%), DHS (10.2%), SSA (7.4%)",
                "Start with ≤$40k awards to build case studies and references",
                "After 12-18 months, reassess moving to DA10 for sustained business",
            ]
        elif top_code == "DA10":
            rationale = (
                f"DA10 offers the best balance of entry accessibility and business "
                f"sustainability: 41.2% graduation rate after 3 years, 28.2% small "
                f"vendor GSA MAS share in 511210/511210S/518210C (~$1.5B+ market), "
                f"GSA Schedule channel at 7.8% (VA 19.4% funding). Software median "
                f"award ${r['software_median_award']:,}. VA Franchise Fund and "
                f"Medical Care channels provide $4.5B+ in civilian funding. "
                f"8.1% sub/prime ratio offers both prime and subcontracting pathways."
            )
            next_steps = [
                "Get on GSA MAS Schedule 70 (SINs 511210/511210S/518210C)",
                "Pursue VA Franchise Fund and Medical Care awards",
                "Target subcontract opportunities with Peraton, Highlight, Carahsoft",
                "Build pipeline through VA and GSA Schedule channels",
                "DA10 combines GSA MAS prime opportunities with subcontracting path",
            ]
        elif top_code == "7A21":
            rationale = (
                f"7A21 has the highest software % (71.8%) and obligation ($29.2B), "
                f"but extreme concentration: Carahsoft 27.1% of sampled obligation. "
                f"GSA MAS small vendor share only ~4%. Subcontracting 2.8% (23 "
                f"subawardees). Best if you already have a Carahsoft or Dell "
                f"relationship, or are targeting niche Army/Navy hardware/software "
                f"requirements. Not recommended as a first code for new teams."
            )
            next_steps = [
                "Leverage existing Carahsoft/Dell relationships for entry if available",
                "Target subcontract opportunities with Dell, WWTech, Emergent",
                "Avoid prime GWAC positions — dominated by large incumbents",
                "Consider subcontracting as the most viable pathway",
                "Not recommended for teams without existing GSA relationships",
            ]
        elif top_code == "DA01":
            rationale = (
                f"DA01 has the largest market ($94.9B obligation) but is "
                f"services-dominated: only 12.8% software awards, median software "
                f"award $383k. Not suitable for software product teams. Best for "
                f"services integration firms. GSA Schedule strong (13.6% awarding), "
                f"and 85% small vendor share in SIN 54151S."
            )
            next_steps = [
                "Target GSA Schedule (SIN 54151S) for services subcontracting",
                "Position as integration/consulting, not software product sales",
                "Target VA (16.6%) and HHS (12.6%) as civilian agencies",
                "Expect large enterprise licenses, not small-award opportunities",
                "Do not target for software product sales — 12.8% software rate",
            ]
        else:
            rationale = (
                f"Not a software market (8.1% software, telecom-dominated). "
                f"High GSA MAS shares are inflated by tiny software market slice. "
                f"Avoid for software product teams."
            )
            next_steps = [
                "Avoid for software product sales — this is a telecom/services market",
            ]

        recommendation = {
            "recommended_code": top_code,
            "entry_axis": rec["entry_axis"],
            "primary_vehicle": rec["primary_vehicle"],
            "rationale": rationale,
            "next_steps": next_steps,
        }
    else:
        rationale = (
            "Could not match your profile to a PSC code. Consider broadening "
            "your criteria or contacting us for personalized guidance."
        )
        next_steps = [
            "Review the full code comparison (python3 fedmarket.py 7030 DA10 7A21 DA01)",
            "Identify which axis matters most: entry accessibility or sustainability",
            "Consider a pilot study in your top-choice code",
        ]

    return recommendation


def format_result(r: Dict[str, Any]) -> str:
    """Format an assessment result as a readable string."""
    rec = r["recommendation"]
    # Use f-strings to avoid Python % formatter issues with parentheses
    lines = [
        f"\n=== Fedmarket Assessment: {r['code']} -- {r['name']} ===",
        f"Screen score: {r['screen_score']}",
        f"Distinct recipients: {r['recipient_count']},",
        f"Top-10 share: {r['top_10_share_pct']}%",
        f"<=$40k fraction: {r['leq_40k_pct']}%",
        f"<=$100k fraction: {r['leq_100k_pct']}%",
        f"Single-award recipients: {r['single_award_pct']}%",
        f"Software (% of awards): {r['software_pct_awards']}%",
        f"Software (% of obligation): {r['software_pct_obligation']}%",
        f"Software <= $40k: {r['software_leq_40k_pct']}%",
        f"Software <= $100k: {r['software_leq_100k_pct']}%",
        f"Software median award: ${r['software_median_award']},",
        f"DOD %: {r['dod_pct']}%",
        f"GSA awarding agency: {r['gsa_awarding_pct']}%",
        "Small vendor GSA MAS by SIN:",
    ]
    sv_mas = r.get("small_vendor_gsa_mas_by_sin", {})
    for sin, pct in sv_mas.items():
        lines.append(f"  {sin}: {pct}%")
    lines += [
        f"SEWP Cat B small vendor: {r['sewp_catb_small_vendor_pct']}%",
        f"Sub/prime ratio: {r['sub_prime_ratio_pct']}%",
        f"Small vendor GWAC share: {r['small_vendor_gwac_share_pct']}%",
        f"Total obligation: ${r['total_obligation_b']:.2f}B",
        "",
        f"Entry axis: {rec['entry_axis']}",
        f"Primary vehicle: {rec['primary_vehicle']}",
        f"Caveats: {rec['caveats']}",
    ]
    return "\n".join(lines)


def format_comparison(comparison: Dict[str, Any]) -> str:
    """Format a comparison of multiple PSC codes."""
    results = comparison["by_code"]
    if not results:
        return "No codes found in lookup."

    widths = [10, 8, 11, 6, 9, 7, 15, 55]

    def header_line():
        print("  ".join(h.ljust(w) for h, w in zip(
            ["PSC Code", "Screen", "Recipients", "<=$40k", "Software%",
             "GWCAC%", "GSA% awarding", "Caveat"], widths)))

    def row_line(code: str, r: dict, caveat: str) -> None:
        sv_gwac = r["small_vendor_gwac_share_pct"]
        gsa_aw = r["gsa_awarding_pct"]
        print(
            f"{code.ljust(widths[0])}"
            f"{str(r['screen_score']).rjust(widths[1])}"
            f"{str(r['recipient_count']).rjust(widths[2]):>11}"
            f"{r['leq_40k_pct']:>6.1f}"
            f"{r['software_pct_awards']:>9.1f}"
            f"{sv_gwac:>7.1f}"
            f"{gsa_aw:>15.1f}"
            f"{caveat}"
        )

    header_line()
    print("-" * sum(w + 2 for w in widths))

    for code in sorted(results.keys()):
        r = results[code]
        caveat = r["recommendation"]["caveats"][:60] + "..."
        row_line(code, r, caveat)

    print("\n--- Rankings ---")
    print(f"By screen score (desc): {' '.join(comparison['ranked_by_screen_score'])}")
    print(f"By <=$40k access (desc): {' '.join(comparison['ranked_by_leq_40k_access'])}")


def main() -> None:
    """CLI entry point."""
    # Handle --help early
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    # Determine flags
    refresh = "--refresh" in sys.argv
    decision = "--decision" in sys.argv

    if decision:
        # Remove --decision from args so it doesn't interfere
        args = [a for a in sys.argv[1:] if a != "--decision"]
    else:
        args = sys.argv[1:]

    if len(args) < 1:
        print("Usage: python3 fedmarket.py <PSC_code> [PSC_code ...]", file=sys.stderr)
        print("Example: python3 fedmarket.py 7030 DA10", file=sys.stderr)
        print("       python3 fedmarket.py --decision", file=sys.stderr)
        print("       python3 fedmarket.py 7030 --refresh", file=sys.stderr)
        sys.exit(1)

    if decision:
        # Decision mode
        if len(args) == 1 and args[0] in _CODES:
            # If a code is provided, assess it and show two-axis recommendation
            try:
                r = assess_code(args[0])
                import fedmarket_dynamic as dm

                dyn_result = dm.assess_code_dynamic(args[0], refresh=True)
                rec = dm.two_axis_recommendation(args[0], {
                    "screen_score": r["screen_score"],
                    "leq_40k_pct": r["leq_40k_pct"],
                    "recipients": r["recipient_count"],
                    "software_pct_awards": r["software_pct_awards"],
                }, dyn_result)
                lines = [format_result(r), "", "=== Two-Axis Recommendation (dynamic) ===",
                         dm.format_recommendation(rec)]
                print("\n".join(lines))
                # Also show decision guidance
                print("\n--- Decision Guidance ---")
                print(f"This code '{args[0]}' has been assessed. Use the two-axis")
                print(f"framework: entry accessibility (high screen score, ≤$40k access)")
                print(f"vs business sustainability (graduation % survival %).")
                print(f"Entry axis: {rec.get('entry_axis')}, Business score: {rec.get('business_score', 0)}")
                print(f"Entry score: {rec.get('entry_score', 0)}")
            except KeyError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error running dynamic assessment: {e}", file=sys.stderr)
                # Fall back to static only
                try:
                    r = assess_code(args[0])
                    print(format_result(r))
                except KeyError:
                    sys.exit(1)
        else:
            # Run decision mode with team profile questions
            print("=" * 60)
            print("FEDMARKET DECISION GUIDE")
            print("=" * 60)
            print()
            print("Answer 3 questions about your team so we can recommend")
            print("the best PSC code and entry strategy using our two-axis")
            print("framework (entry accessibility vs. business sustainability).")
            print()

            # Question 1: Budget focus
            print("Q1. What is your primary budget focus?")
            print("  a) ≤ $40k per award — quick entry, faster revenue cycles")
            print("  b) ≤ $100k per award — moderate ambition")
            print("  c) Enterprise deals ($100k+) — larger deals, longer cycles")
            budget_q = input("  Your choice (a/b/c): ").strip().lower()
            budget_map = {"a": "leq_40k", "b": "leq_100k", "c": "enterprise"}
            budget = budget_map.get(budget_q, "leq_40k")

            # Question 2: Go-to-market approach
            print()
            print("Q2. What is your preferred go-to-market approach?")
            print("  a) Direct sales — build your own sales capability")
            print("  b) GSA Schedule/MAS — pursue government contracting")
            print("  c) Subcontracting — partner with large primes (Carahsoft, Dell, etc.)")
            gtm_q = input("  Your choice (a/b/c): ").strip().lower()
            gtm_map = {"a": "direct", "b": "gsa_mas", "c": "subcontract"}
            gtm = gtm_map.get(gtm_q, "direct")

            # Question 3: Technical focus
            print()
            print("Q3. What is your product's technical focus?")
            print("  a) Pure software product (offline/installed software)")
            print("  b) SaaS / Cloud service (web-based, subscription)")
            print("  c) IT services / Integration (consulting, implementation)")
            focus_q = input("  Your choice (a/b/c): ").strip().lower()
            focus_map = {"a": "software", "b": "saas", "c": "services"}
            focus = focus_map.get(focus_q, "software")

            print()
            print("=" * 60)
            print("Analyzing your profile against all 5 PSC codes...")
            print()

            # Run decision
            rec = decide_code(budget, gtm, focus)

            # Output results
            print()
            print("=" * 60)
            print("RECOMMENDATION")
            print("=" * 60)
            print()
            print(f"Recommended PSC code: {rec.get('recommended_code', 'N/A')}")
            print(f"Entry axis: {rec.get('entry_axis', 'N/A')}")
            print(f"Primary vehicle: {rec.get('primary_vehicle', 'N/A')}")
            print()
            print("RATIONALE:")
            print(rec.get('rationale', 'N/A'))
            print()
            print("NEXT STEPS:")
            for i, step in enumerate(rec.get('next_steps', []), 1):
                print(f"  {i}. {step}")
            print()
            print("=" * 60)
            print("TWO-AXIS FRAMEWORK CONTEXT")
            print("=" * 60)
            print()
            print("• Axis 1 (Accessibility): How easy is it to enter the market?")
            print("  Measured by: screen score, ≤$40k award fraction, recipient count,")
            print("  software award percentage. HIGH → 7030 best, then DA10, 7A21, DA01, D304.")
            print()
            print("• Axis 2 (Business Sustainability): How likely are recipients to return")
            print("  and grow? Measured by: survival % (UEI match), graduation % (>$100k aggregate).")
            print("  HIGH → DA10 best (41.2%), DA01 (44.9%), 7A21 (43.1%), 7030 weakest (13.8%).")
            print()
            print("• TRADEOFF: 7030 maximizes entry ease but has weak sustainability")
            print("  (median returning UEI aggregates ~$2,000 over 3 years).")
            print("  • DA10/DA01/7A21 offer stronger sustainability but have entry challenges.")
            print()
            print("• YOUR PROFILE just now emphasized:", budget, gtm, focus)
            print("  → Recommended code:", rec.get('recommended_code', 'N/A'))
    else:
        # Original mode: assess PSC codes
        if len(args) == 1:
            try:
                r = assess_code(args[0])
                if refresh:
                    # Also run dynamic assessment and show two-axis recommendation
                    import fedmarket_dynamic as dm
                    dyn_result = dm.assess_code_dynamic(args[0], refresh=True)
                    rec = two_axis_recommendation(args[0], {
                        "screen_score": r["screen_score"],
                        "leq_40k_pct": r["leq_40k_pct"],
                        "recipients": r["recipient_count"],
                        "software_pct_awards": r["software_pct_awards"],
                    }, dyn_result)
                    lines = [format_result(r), "", "=== Two-Axis Recommendation (dynamic) ===", dm_format_recommendation(dyn_result)]
                    print("\n".join(lines))
                else:
                    print(format_result(r))
            except KeyError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            comparison = compare_codes(args)
            if refresh:
                # Show dynamic comparison if any codes have dynamic data
                for code in args:
                    try:
                        r = assess_code(code)
                        import fedmarket_dynamic as dm
                        dyn_result = dm.assess_code_dynamic(code, refresh=True)
                        rec = two_axis_recommendation(code, {
                            "screen_score": r["screen_score"],
                            "leq_40k_pct": r["leq_40k_pct"],
                            "recipients": r["recipient_count"],
                            "software_pct_awards": r["software_pct_awards"],
                        }, dyn_result)
                        print("%s: %s" % (code, dm_format_recommendation(dyn_result)))
                        print()
                    except KeyError:
                        pass
            format_comparison(comparison)


if __name__ == "__main__":
    main()