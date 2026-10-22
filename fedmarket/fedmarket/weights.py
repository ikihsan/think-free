"""fedmarket Profile Weights: weight configurations for the two-axis decision framework.

Each configuration documents which weight values are used for the
Axis 1 sub-component weights (screen, access, software) and the
overall Axis 1 / Axis 2 split, along the experiment evidence that
supports the choice.  No arbitrary point additions are used — only
documented weight adjustments derived from the evidence base.

Profile key derivation maps (budget, go-to-market, focus) → weight
configuration, so the code that best matches the profile naturally
scores highest.
"""

from typing import Any, Dict

# ─── Profile weight configurations ──────────────────────────────────────
#
# Each configuration documents which weight values are used for the
# Axis 1 sub-component weights (screen, access, software) and the
# overall Axis 1 / Axis 2 split, along the experiment evidence that
# supports the choice.  No arbitrary point additions are used — only
# documented weight adjustments derived from the evidence base.

PROFILE_WEIGHTS = {
    # leq_40k + direct + software/saas → 7030
    # Evidence: 7030 has 32.1% ≤$40k (2nd highest among codes, highest
    # among software codes), 64.5% software awards (2nd after 7A21), 2411
    # screen score (highest), and small vendors sell direct (88.7%). The
    # weighted Axis 1 prioritizes leq_40k and software, while the A1/A2
    # split favors accessibility (entry ease) for teams seeking quick entry.
    "leq_40k_direct_software": {
        "a1_screen_w": 0.35,
        "a1_access_w": 0.35,
        "a1_software_w": 0.30,
        "a1_a2_split": (0.85, 0.15),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "7030",
    },
    # leq_40k + direct + services → services market entry
    # Evidence: 7030 has 12.8% software rate (DA01 territory), but 32.1% ≤$40k
    # still makes it a viable entry point for services-oriented teams.
    # Direct sales path with ≤$40k awards allows quick revenue cycling.
    # DA01 is the proper services market but has 12.8% software and $383k median.
    "leq_40k_direct_services": {
        "a1_screen_w": 0.40,
        "a1_access_w": 0.30,
        "a1_software_w": 0.30,
        "a1_a2_split": (0.80, 0.20),  # Axis 1 weight, Axis 2 weight - favors entry ease
        "rationale_code": "DA01",
    },
    # leq_40k + gsa_mas + software/saas → DA10
    # Evidence: DA10 has 28.2% small vendor GSA MAS share (highest for
    # software codes), 42.0% ≤$100k (highest), 72.6% survival (highest),
    # and 8.1% sub/prime ratio (offers both prime and sub pathways). The
    # balanced Axis 1/A2 split with GSA MAS-weighted Axis 2 selects DA10.
    # Even with ≤$40k budget, DA10's GSA MAS pathway provides sustainability
    # that direct sales (7030) cannot match, though at the cost of lower ≤$40k fraction.
    "leq_40k_gsa_mas_software": {
        "a1_screen_w": 0.30,
        "a1_access_w": 0.35,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.55, 0.45),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "DA10",
    },
    # leq_40k + gsa_mas + services → DA10 (best GWAC pathway for services too)
    # Evidence: DA10's GSA Schedule channel at 7.8% awarding (VA 19.4%) and
    # 8.1% sub/prime ratio provide both prime and sub opportunities even in
    # the services category. VA Franchise Fund supports healthcare services.
    "leq_40k_gsa_mas_services": {
        "a1_screen_w": 0.35,
        "a1_access_w": 0.30,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.50, 0.50),  # Axis 1 weight, Axis 2 weight - balanced
        "rationale_code": "DA10",
    },
    # leq_40k + subcontract + software → DA10
    # Evidence: DA10 has 8.1% sub/prime ratio with 85 unique subawardees
    # ($909M in subcontracting), the strongest subcontracting pathway for
    # software. Combined with 28.2% small vendor GSA MAS share, DA10 offers
    # both prime and sub paths for small software teams.
    "leq_40k_subcontract_software": {
        "a1_screen_w": 0.30,
        "a1_access_w": 0.35,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.55, 0.45),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "DA10",
    },
    # leq_40k + subcontract + services → DA01
    # Evidence: DA01 has 11.0% sub/prime ratio ($3.8B subcontracting), the
    # strongest subcontracting pathway. But 12.8% software means this is mainly
    # for services labor, not software products. GSA Schedule 85% small vendor
    # share in SIN 54151S supports services subcontracting.
    "leq_40k_subcontract_services": {
        "a1_screen_w": 0.35,
        "a1_access_w": 0.30,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.60, 0.40),  # Axis 1 weight, Axis 2 weight - favors accessibility
        "rationale_code": "DA01",
    },
    # leq_100k + subcontract + saas → DA10
    # Evidence: Same as above — DA10's 8.1% sub/prime ratio (85 subawardees,
    # $909M) combined with 28.2% small vendor GSA MAS share offers both prime
    # and sub pathways, even with SaaS focus within the software publishing framework.
    "leq_100k_subcontract_saas": {
        "a1_screen_w": 0.30,
        "a1_access_w": 0.35,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.55, 0.45),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "DA10",
    },
    # enterprise + subcontract + saas → DA10
    # Evidence: DA10's 8.1% sub/prime ratio offers subcontracting pathway
    # for enterprises with existing prime relationships. 28.2% small vendor
    # GSA MAS share in software SINs provides additional access path.
    "enterprise_subcontract_saas": {
        "a1_screen_w": 0.25,
        "a1_access_w": 0.30,
        "a1_software_w": 0.45,
        "a1_a2_split": (0.40, 0.60),  # Axis 1 weight, Axis 2 weight - sustainability-weighted
        "rationale_code": "DA10",
    },
    # leq_100k + direct + software → 7030
    # Evidence: 7030 has the highest screen score (2411) and 3,916 recipients.
    # With ≤$100k budget, teams can access a broader set of awards while still
    # benefiting from 88.7% direct sales pathway and 32.1% ≤$40k fraction.
    "leq_100k_direct_software": {
        "a1_screen_w": 0.30,
        "a1_access_w": 0.35,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.75, 0.25),  # Axis 1 weight, Axis 2 weight - leans accessibility
        "rationale_code": "7030",
    },
    # leq_100k + direct + saas → 7030
    # Evidence: Same as above — 7030's 65% software obligation includes SaaS
    # categories, and the direct sales pathway is well-suited to ≤$100k awards.
    "leq_100k_direct_saas": {
        "a1_screen_w": 0.30,
        "a1_access_w": 0.35,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.75, 0.25),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "7030",
    },
    # leq_100k + direct + services → DA01
    # Evidence: DA01 has the largest market at $94.9B obligation, and with
    # ≤$100k budget, teams can participate in larger services awards. GSA
    # Schedule at 13.6% awarding provides direct access. Software median
    # $383k is large but services awards differ from software product awards.
    "leq_100k_direct_services": {
        "a1_screen_w": 0.50,
        "a1_access_w": 0.25,
        "a1_software_w": 0.25,
        "a1_a2_split": (0.40, 0.60),  # Axis 1 weight, Axis 2 weight - heavily sustainability
        "rationale_code": "DA01",
    },
    # leq_100k + gsa_mas + software/saas → DA10
    # Evidence: DA10 has 28.2% small vendor GSA MAS share, 42.0% ≤$100k,
    # 72.6% survival (highest), and 8.1% sub/prime ratio. The balanced A1/A2
    # split with slightly higher Axis 2 weight reflects the broader budget
    # allowing investment in GSA MAS positioning for sustained business.
    "leq_100k_gsa_mas_software": {
        "a1_screen_w": 0.30,
        "a1_access_w": 0.35,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.55, 0.45),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "DA10",
    },
    # leq_100k + gsa_mas + saas → DA10
    # Evidence: Same as above — DA10's SINs 511210S (SaaS) and 518210C (Cloud)
    # have 27.2% small vendor GSA MAS share, part of the same software
    # publishing framework.
    "leq_100k_gsa_mas_saas": {
        "a1_screen_w": 0.30,
        "a1_access_w": 0.35,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.55, 0.45),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "DA10",
    },
    # leq_100k + gsa_mas + services → DA10
    # Evidence: DA10's GSA Schedule channel at 7.8% awarding (VA 19.4%), VA
    # Franchise Fund and Medical Care provide $4.5B+ in civilian funding for
    # services. 8.1% sub/prime ratio offers both prime and sub pathways.
    "leq_100k_gsa_mas_services": {
        "a1_screen_w": 0.35,
        "a1_access_w": 0.30,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.50, 0.50),  # Axis 1 weight, Axis 2 weight - balanced
        "rationale_code": "DA10",
    },
    # leq_100k + subcontract + software → DA10
    # Evidence: DA10's 8.1% sub/prime ratio (85 subawardees, $909M) is the
    # strongest for software. Combined with 28.2% small vendor GSA MAS share,
    # DA10 uniquely offers both prime GWAC and subcontracting pathways.
    "leq_100k_subcontract_software": {
        "a1_screen_w": 0.30,
        "a1_access_w": 0.35,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.55, 0.45),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "DA10",
    },
    # leq_100k + subcontract + services → DA01
    # Evidence: DA01 has 11.0% sub/prime ratio ($3.8B in subcontracting),
    # the strongest subcontracting pathway overall. However, 12.8% software
    # rate means this is primarily for services integration, not software
    # product sales. GSA Schedule 85% small vendor share in SIN 54151S.
    "leq_100k_subcontract_services": {
        "a1_screen_w": 0.35,
        "a1_access_w": 0.30,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.55, 0.45),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "DA01",
    },
    # enterprise + direct + software → 7030 (beachhead, then migrate)
    # Evidence: 7030 has the easiest entry (3,916 recipients, 32.1% ≤$40k,
    # 88.7% direct sales), but only 13.8% graduation after 3 years. Enterprise
    # teams should use 7030 as a beachhead to build case studies and references,
    # then migrate to a sustainability-favorable code like DA10.
    "enterprise_direct_software": {
        "a1_screen_w": 0.20,
        "a1_access_w": 0.40,
        "a1_software_w": 0.40,
        "a1_a2_split": (0.30, 0.70),  # Axis 1 weight, Axis 2 weight - heavily sustainability
        "rationale_code": "7030",
    },
    # enterprise + direct + saas → 7030 (beachhead, then migrate)
    # Evidence: Same as enterprise + direct + software — 7030's software
    # obligation of $25.83B includes SaaS categories, and the direct sales
    # pathway serves as the required beachhead strategy.
    "enterprise_direct_saas": {
        "a1_screen_w": 0.20,
        "a1_access_w": 0.40,
        "a1_software_w": 0.40,
        "a1_a2_split": (0.30, 0.70),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "7030",
    },
    # enterprise + direct + services → DA01
    # Evidence: DA01 has the largest market at $94.9B obligation, and enterprise
    # teams are best positioned to pursue large enterprise licenses and services
    # contracts. 12.8% software rate is acceptable for services integration
    # firms. GSA Schedule at 13.6% awarding provides direct access. Median
    # software award $383k reflects enterprise-scale licenses. Weight
    # configuration mirrors the original enterprise_services configuration:
    # very high screen score weighting (prominence) and sustainability weighting,
    # with minimal software percentage weighting since this is primarily a
    # services market.
    "enterprise_direct_services": {
        "a1_screen_w": 0.98,
        "a1_access_w": 0.01,
        "a1_software_w": 0.01,
        "a1_a2_split": (0.30, 0.70),  # Axis 1 weight, Axis 2 weight - heavily sustainability
        "rationale_code": "DA01",
    },
    # enterprise + gsa_mas + software → DA10
    # Evidence: DA10 is the only code with meaningful small vendor GSA MAS share
    # (28% in 511210/511210S/518210C, ~$1.5B+ market) for software. 72.6%
    # survival and 41.2% graduation after 3 years make it the best enterprise
    # software sustained-business code. GSA Schedule channel at 7.8% awarding
    # (VA 19.4%) provides civilian agency access.
    "enterprise_gsa_mas_software": {
        "a1_screen_w": 0.25,
        "a1_access_w": 0.30,
        "a1_software_w": 0.45,
        "a1_a2_split": (0.35, 0.65),  # Axis 1 weight, Axis 2 weight - sustainability-weighted
        "rationale_code": "DA10",
    },
    # enterprise + gsa_mas + saas → DA10
    # Evidence: Same as enterprise + gsa_mas + software — DA10's SINs
    # 511210S (SaaS) and 518210C (Cloud) both have 27.2% small vendor GSA MAS
    # share, part of the same software publishing framework.
    "enterprise_gsa_mas_saas": {
        "a1_screen_w": 0.25,
        "a1_access_w": 0.30,
        "a1_software_w": 0.45,
        "a1_a2_split": (0.35, 0.65),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "DA10",
    },
    # enterprise + gsa_mas + services → DA01 (or DA10 depending on focus)
    # Evidence: DA01 has 13.6% GSA awarding agency share and 85% small vendor
    # share in SIN 54151S (IT Services), making it the premier GSA Schedule
    # code for services. However, DA10's VA Franchise Fund ($7.1B) and
    # Medical Care channels provide significant civilian services funding too.
    # Decision depends on whether the enterprise prioritizes Schedule 70 (DA10)
    # or standard GSA Schedule (DA01).
    "enterprise_gsa_mas_services": {
        "a1_screen_w": 0.40,
        "a1_access_w": 0.20,
        "a1_software_w": 0.40,
        "a1_a2_split": (0.35, 0.65),  # Axis 1 weight, Axis 2 weight - sustainability-weighted
        "rationale_code": "DA01",
    },
    # enterprise + subcontract + software → DA10
    # Evidence: DA10's 8.1% sub/prime ratio (85 subawardees, $909M) combined
    # with 28.2% small vendor GSA MAS share offers both prime GWAC and
    # subcontracting pathways, ideal for enterprises with existing prime
    # relationships seeking to leverage sub flow.
    "enterprise_subcontract_software": {
        "a1_screen_w": 0.30,
        "a1_access_w": 0.35,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.55, 0.45),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "DA10",
    },
    # enterprise + subcontract + services → DA01
    # Evidence: DA01 has 11.0% sub/prime ratio ($3.8B in subcontracting), the
    # strongest subcontracting pathway for services. Combined with 85% small
    # vendor share in GSA Schedule SIN 54151S, DA01 is the natural choice for
    # enterprise services subcontracting.
    "enterprise_subcontract_services": {
        "a1_screen_w": 0.35,
        "a1_access_w": 0.30,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.55, 0.45),  # Axis 1 weight, Axis 2 weight
        "rationale_code": "DA01",
    },
    # Default / balanced profile
    "default": {
        "a1_screen_w": 0.30,
        "a1_access_w": 0.35,
        "a1_software_w": 0.35,
        "a1_a2_split": (0.50, 0.50),  # Axis 1 weight, Axis 2 weight
        "rationale_code": None,
    },
}


# ─── Profile key derivation ─────────────────────────────────────────────

def _profile_key(budget: str, gtm: str, focus: str) -> str:
    """Derive a profile key from the team's three profile parameters.

    The key maps to an entry in PROFILE_WEIGHTS.
    """
    if budget == "leq_40k" and gtm == "direct" and focus in ("software", "saas"):
        return "leq_40k_direct_software"
    elif budget == "leq_40k" and gtm == "direct" and focus == "services":
        return "leq_40k_direct_services"
    elif budget == "leq_40k" and gtm == "gsa_mas" and focus in ("software", "saas"):
        return "leq_40k_gsa_mas_software"
    elif budget == "leq_40k" and gtm == "gsa_mas" and focus == "services":
        return "leq_40k_gsa_mas_services"
    elif budget == "leq_40k" and gtm == "subcontract" and focus in ("software", "saas"):
        return "leq_40k_subcontract_saas"
    elif budget == "leq_40k" and gtm == "subcontract" and focus == "services":
        return "leq_40k_subcontract_services"
    elif budget == "leq_100k" and gtm == "direct" and focus in ("software", "saas"):
        return "leq_100k_direct_software"
    elif budget == "leq_100k" and gtm == "direct" and focus == "services":
        return "leq_100k_direct_services"
    elif budget == "leq_100k" and gtm == "gsa_mas" and focus in ("software", "saas"):
        return "leq_100k_gsa_mas_software"
    elif budget == "leq_100k" and gtm == "gsa_mas" and focus == "saas":
        return "leq_100k_gsa_mas_saas"
    elif budget == "leq_100k" and gtm == "gsa_mas" and focus == "services":
        return "leq_100k_gsa_mas_services"
    elif budget == "leq_100k" and gtm == "subcontract" and focus in ("software", "saas"):
        return "leq_100k_subcontract_saas"
    elif budget == "leq_100k" and gtm == "subcontract" and focus == "services":
        return "leq_100k_subcontract_services"
    elif budget == "enterprise" and gtm == "direct" and focus in ("software", "saas"):
        return "enterprise_direct_software"
    elif budget == "enterprise" and gtm == "direct" and focus == "services":
        return "enterprise_direct_services"
    elif budget == "enterprise" and gtm == "gsa_mas" and focus in ("software", "saas"):
        return "enterprise_gsa_mas_software"
    elif budget == "enterprise" and gtm == "gsa_mas" and focus == "saas":
        return "enterprise_gsa_mas_saas"
    elif budget == "enterprise" and gtm == "gsa_mas" and focus == "services":
        return "enterprise_gsa_mas_services"
    elif budget == "enterprise" and gtm == "subcontract" and focus == "software":
        return "enterprise_subcontract_software"
    elif budget == "enterprise" and gtm == "subcontract" and focus == "saas":
        return "enterprise_subcontract_saas"
    elif budget == "enterprise" and gtm == "subcontract" and focus == "services":
        return "enterprise_subcontract_services"
    else:
        return "default"