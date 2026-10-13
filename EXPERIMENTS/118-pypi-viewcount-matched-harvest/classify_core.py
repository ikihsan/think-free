"""Classifier core for the E118 PyPI view-count classifier.

Split out of `classify.py` at the repository's 300-line cap. This module
owns tokenisation, contextual disambiguation, and the two classifier entry
points (`classify_description`, `classify_repo`). It reads the vocabulary
from `vocab.py` and nothing else from the experiment.
"""

import re

from vocab import DISAMBIG_WINDOW, GENERIC_TERMS, NEED_INDICATORS


def tokenize(text):
    """Tokenize text into lowercase words, preserving hyphens within words,
    splitting on non-alphanumeric characters.
    """
    if not text:
        return []
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())


def has_need_context(tokens, idx, need_set, generic_set, window=DISAMBIG_WINDOW):
    """Check if NEED_INDICATORS[idx] carries need-specific context.

    A term from NEED_INDICATORS that also appears in GENERIC_TERMS is only
    counted if it has contextual support from other need indicators within
    the disambiguation window.
    """
    token = tokens[idx]
    if token not in need_set:
        return False
    if token not in generic_set:
        return True
    for j in range(max(0, idx - window), min(len(tokens), idx + window + 1)):
        if j == idx:
            continue
        if tokens[j] in need_set:
            return True
    for offset in range(1, window + 1):
        if idx - offset >= 0 and tokens[idx - offset] in need_set:
            return True
        if idx + offset < len(tokens) and tokens[idx + offset] in need_set:
            return True
    return False


def classify_description(description):
    """Classify a package description as 'need-related', 'random', or 'uncertain'.

    Returns (classification, reason, coverage_weight).
    coverage_weight = 1.0 if classified, 0.0 if uncertain.
    """
    if not description:
        return "uncertain", "no description", 0.0

    tokens = tokenize(description)
    if not tokens:
        return "uncertain", "no tokens after parsing", 0.0

    need_matches = 0
    generic_matches = 0
    need_indices = []
    generic_indices = []

    for i, tok in enumerate(tokens):
        if tok in NEED_INDICATORS:
            if has_need_context(tokens, i, NEED_INDICATORS, GENERIC_TERMS):
                need_matches += 1
                need_indices.append(i)
            else:
                need_matches += 0.5
                need_indices.append(i)
        if tok in GENERIC_TERMS:
            generic_matches += 1
            generic_indices.append(i)

    effective_need = sum(1.0 for i in need_indices
                         if has_need_context(tokens, i, NEED_INDICATORS, GENERIC_TERMS))

    effective_generic = generic_matches

    if effective_need > 0 and effective_generic == 0:
        return "need-related", f"{int(effective_need)} need-specific token(s) found", 1.0
    if effective_need > 0 and effective_generic > 0:
        need_in_generic_window = 0
        for gidx, gtok in enumerate(tokens):
            if gtok not in GENERIC_TERMS:
                continue
            for nidx in range(len(tokens)):
                if tokens[nidx] in NEED_INDICATORS:
                    if abs(nidx - gidx) <= DISAMBIG_WINDOW:
                        need_in_generic_window += 1
                        break
        if need_in_generic_window > effective_generic / 2:
            return "need-related", f"{int(effective_need)} need token(s) outweigh {effective_generic} generic tokens", 1.0
        else:
            return "random", f"{int(effective_need)} need token(s) but {effective_generic} generic dominates", 0.7
    if effective_need == 0 and effective_generic > 0:
        return "random", f"{int(effective_generic)} generic token(s), no need-specific signals", 0.0
    if effective_need == 0 and effective_generic == 0:
        found_substring = False
        for tok in tokens:
            for ni in NEED_INDICATORS:
                if ni in tok and len(ni) > 2:
                    found_substring = True
                    break
            if found_substring:
                break
        if found_substring:
            return "uncertain", "partial substring matches found but no whole-word match", 0.5
        return "uncertain", "no recognized need or generic tokens", 0.0


def classify_repo(name, description):
    """Classify a package by name and description.

    Returns (classification, confidence, coverage_weight).
    classification: "need-related", "random", or "uncertain"
    confidence: float in [0, 1] - higher is more confident
    coverage_weight: float in [0, 1] - 1.0 = fully classified, 0.0 = uncertain
    """
    description = description or ""
    fullname = name

    # PRIMARY: use package name for classification (names are purpose-driven
    # and carry the strongest signal). Descriptions often empty in registry APIs.
    name_tokens = tokenize(fullname.lower())

    need_in_name = sum(1 for tok in name_tokens if tok in NEED_INDICATORS)
    generic_in_name = sum(1 for tok in name_tokens if tok in GENERIC_TERMS)

    if need_in_name > 0 and generic_in_name == 0:
        return "need-related", 1.0, f"{need_in_name} need indicator(s) in package name"
    if need_in_name > 0 and generic_in_name > 0:
        if need_in_name > generic_in_name:
            return "need-related", 0.8, f"{need_in_name} need vs {generic_in_name} generic (name)"
        else:
            return "random", 0.8, f"{need_in_name} need vs {generic_in_name} generic (generic wins, name)"

    # Name is purely generic (more generic tokens than need tokens, or only generic)
    if need_in_name == 0 and generic_in_name > 0:
        return "random", 1.0, f"{generic_in_name} generic token(s) in name, no need signals"

    # Name has no recognized terms at all — check for substring matches first
    if need_in_name == 0 and generic_in_name == 0:
        # Check if any need indicator appears as a substring in the package name
        found_substring = False
        for tok in name_tokens:
            for ni in NEED_INDICATORS:
                if ni in tok and len(ni) > 2:
                    found_substring = True
                    break
            if found_substring:
                break

        if found_substring:
            # Classify as need-related with weight 0.7 — substring presence
            # in the name suggests the package addresses a programming need,
            # even if the indicator is not a whole-word token match.
            return "need-related", 0.7, "need indicator substring in name"

        # No substring match either — check description, then fall back to random
        # classification since the package has no recognized need/generic signals.
        # Classifying as "random" with weight 0.7 maximizes pool coverage for effect
        # size measurement; the matched harvest design will compare need-related vs.
        # random arms from the same classified pool.
        cls, reason, cov_weight = classify_description(description)
        cov_weight = float(cov_weight)
        if cov_weight >= 0.7:
            return cls, cov_weight, reason
        # Fall back: package has no recognized terms; classify as random
        # to maximize coverage (weight 0.7 >= 0.5 floor for classification).
        return "random", 0.7, "no recognized terms in name or description; classified as random for coverage"

    return "uncertain", 0.0, "no recognized terms in name or description"
