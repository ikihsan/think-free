#!/usr/bin/env python3
"""Need classification rules for E067 view-count framework."""

import re


def classify_need(title):
    """Classify a need title into one of five categories.

    Returns one of: registry-lookup, diagnose-own-artifact,
    purchase-source, judgement, technique-or-expertise
    """
    if not title:
        return "technique-or-expertise"

    t = title.lower()

    # registry-lookup: needs requiring a published registry or spec sheet
    registry_rx = re.compile(
        r"\b(serial number|vin)\b"
        r"|\\bwhat year\\b"
        r"|\\bmodel (and|number|year)\\b"
        r"|\\bwhat size .*should i buy\\b"
        r"|\\bwhat size (screw|capacitor|bolt)\\b"
        r"|\\bamp rating\\b"
        r"|\\bhorsepower\\b"
        r"|\\bwhat (kind|type) .*(should|do) i buy\\b"
        r"|\\bidentify my\\b"
        r"|\\bid my\\b",
        re.I,
    )
    if registry_rx.search(t):
        return "registry-lookup"

    # diagnose-own-artifact: needs requiring the requester's own physical artifact
    diagnose_rx = re.compile(
        r"\b(this (plant|tree|weed|bug|mushroom|pan|board|outlet|washer|"
        r"furnace|refrigerator|boiler|light|fan|blotch|stain|job))\b"
        r"|\\bmy (plant|tree|weed|bug|mushroom|rose|bike|pan|washer|furnace|"
        r"refrigerator|boiler|outlet|outlets|dishwasher|pump|boiler|cyclone)\\b"
        r"|\\b(dead|dying|limp|drooping|discolored|brown|burnt|burned|sagging|"
        r"spreading|rotting|rust)\\b"
        r"|\\bwhat (is|kind of) (this|that)\\b"
        r"|\\binform me what\\b",
        re.I,
    )
    if diagnose_rx.search(t):
        return "diagnose-own-artifact"

    # purchase-source: needs asking where to buy, what brand, etc.
    purchase_rx = re.compile(
        r"\bwhere can (i|one|we)\\b"
        r"|\\bwhere (do|can) (i|one|we) (buy|get|purchase)\\b"
        r"|\\bwhat (hinge system|permanent grasses|screw|bolt|size|kind) .*"
        r"(can|should|do) i (buy|use|get)\\b",
        re.I,
    )
    if purchase_rx.search(t):
        return "purchase-source"

    # judgement: needs asking for safety/quality reassurance
    judgement_rx = re.compile(
        r"\b(is it (safe|ok|okay|bad|good|normal|possible)|safe to eat|"
        r"should i|am i (wrong|crazy)|anyone know if)\\b",
        re.I,
    )
    if judgement_rx.search(t):
        return "judgement"

    # default: technique-or-expertise
    return "technique-or-expertise"


def classify_need_title(title):
    """Public API: classify a need title string."""
    return classify_need(title)