#!/usr/bin/env python3
"""E028's statistical primitives and the lexical index, as pure functions.

Split out of `stats.py` at the 300-line cap, by invariant: this module holds
the arithmetic — intervals, agreement, and the lexical index with its base rate
— and `stats.py` holds the loading, the gates and the verdict. The split is
also the reason the test file can import `wilson` and `agreement_note` without
running a measurement.
"""
import json
import math
import re


def read_jsonl(path):
    with open(path) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def wilson(k, n, z=1.959963985):
    """Wilson score interval. `n == 0` is None, not 0: an unmeasured
    population has no interval, and F017's defect is a gate that read one."""
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [max(0.0, centre - half), min(1.0, centre + half)]


def cohen_kappa(a, b, cats):
    """Cohen's kappa over the declared categories.

    Undefined on degenerate marginals (returns None) rather than 0.0 or 1.0.
    A scheme where one reader used one label is not agreement and is not
    disagreement; it is a scheme that separated nothing.
    """
    n = len(a)
    if n == 0:
        return None
    obs = sum(1 for x, y in zip(a, b) if x == y) / n
    pa = {c: sum(1 for x in a if x == c) / n for c in cats}
    pb = {c: sum(1 for x in b if x == c) / n for c in cats}
    exp = sum(pa[c] * pb[c] for c in cats)
    if exp >= 1.0:
        return None
    return (obs - exp) / (1 - exp)


def agreement_note(kappa):
    """κ = 1.0 is a warning, not agreement.

    Two readers who labelled every row identically have not measured the
    distinction the scheme exists to draw. Reporting 1.0 as a pass would
    certify an instrument for not discriminating.
    """
    if kappa is None:
        return "kappa not defined (marginals degenerate)"
    if kappa >= 0.999:
        return ("kappa is 1.0: the scheme separated nothing on this "
                "population, so this is a warning, not agreement")
    return None


STOP = set(
    "the a an and or of to in for with that this it its is are be not on at "
    "by from as so such which their there them they would could should will "
    "can then than when where while into your you our us if but has have had "
    "was were been being do does did more most other some any each per about "
    "over under after before between within without across only just also"
    .split())


def lexical_index(req, doc, attribute):
    """Attribute-term coverage of a product's own documentation.

    Deliberately crude, and reported only beside its base rate on mismatched
    pairs (F043's lesson: a rate read without a control means nothing). Terms
    are the content words of the Step A attribute. Feeds no gate; a test greps
    the gate table to hold that.
    """
    terms = {t for t in re.findall(r"[a-z][a-z0-9\-]{2,}", attribute.lower())
             if t not in STOP}
    if not terms:
        return None, 0, []
    low = doc.lower()
    hit = sorted(t for t in terms if t in low)
    return round(len(hit) / len(terms), 4), len(hit), sorted(terms)


def lexical_summary(view):
    """Best-coverage per (reader, row, pairing), then matched vs mismatched.

    `view` is {reader: {(row, pairing): view_entry}}.
    """
    lex = []
    for reader, entries in view.items():
        for (row, pairing), entry in entries.items():
            attr = entry["step_a"]["attribute"]
            best = None
            for artifact in entry["artifacts_shown"]:
                cov, hit, _terms = lexical_index(
                    entry["requirement_text"],
                    artifact.get("documentation_shown") or "", attr)
                if cov is not None and (best is None or cov > best[0]):
                    best = (cov, artifact["artifact"], hit)
            lex.append({"reader": reader, "row": row, "pairing": pairing,
                        "best_coverage": best[0] if best else None,
                        "artifact": best[1] if best else None,
                        "terms_hit": best[2] if best else None})

    def mean(xs):
        return round(sum(xs) / len(xs), 4) if xs else None

    base = [x["best_coverage"] for x in lex
            if x["pairing"] == "mismatched_with"
            and x["best_coverage"] is not None]
    real = [x["best_coverage"] for x in lex
            if x["pairing"] == "own" and x["best_coverage"] is not None]
    summary = {
        "own_mean_coverage": mean(real),
        "mismatched_mean_coverage": mean(base),
        "difference": (round(mean(real) - mean(base), 4)
                       if real and base else None),
        "n_own": len(real), "n_mismatched": len(base),
        "informative": None,
        "note": ("Reported with the mismatched base rate beside it, every "
                 "time. It feeds no gate."),
    }
    if real and base:
        summary["informative"] = (mean(real) - mean(base)) > 0.20
    return summary