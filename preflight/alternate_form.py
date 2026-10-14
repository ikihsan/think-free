"""C2 -- false-positive rate on correct output written in a different form.

Every cheap way to validate a verifier uses a control whose surface form already
matches the key: a value copied out of the key, or a value corrupted from it.
F118's finding is that those two controls cannot see the third question, which
is the one a verifier is actually asked. A model writes `49 CFR $2,600.
1150.31-1150.35` where the document says `49 CFR 2600.1150.31-1150.35`; both
are right, they are not the same string, and a string-matching verifier is
being asked something its controls never asked.

So: hand the check control items that carry an independent correctness label,
and let it report the rate at which the flagger condemns items known to be
right. Arms are reported separately. One instrument with a clean arm and a
condemned arm is a fact about the instrument; one average over both arms is not.
"""

from .stats import fmt_interval, wilson

FLAG_VERDICTS = ("ungrounded_value", "ungrounded_claim", "flagged", "wrong", "false")


def _is_flagged(verdict):
    """Treat an explicit negative verdict as the positive class.

    An item is condemned when the flagger does not clear it. Anything the
    flagger marks correct (or leaves empty) is not a false positive, so a
    missing verdict counts as silence rather than as condemnation -- otherwise
    a flagger that returns nothing condemns everything.
    """
    if verdict is None:
        return False
    return str(verdict).strip().lower() in FLAG_VERDICTS


def alternate_form_fp(items, flagger, fp_ceiling=0.02, arms=True):
    """Measure a flagger against labelled control items.

    `items`: [{"arm": str, "value": str, "correct": bool, ...}] -- `correct` is
    an independent label about whether the item should be cleared. `flagger`
    takes one item and returns a verdict string.
    """
    per_arm = {}
    everything = []
    for item in items:
        arm = item.get("arm", "default")
        bucket = per_arm.setdefault(arm, {"correct": [], "incorrect": []})
        bucket["correct" if item.get("correct") else "incorrect"].append(item)
        everything.append(item)

    def measure(rows):
        flagged = [r for r in rows if _is_flagged(flagger(r))]
        n = len(rows)
        return {"n": n, "flagged": len(flagged), "rate": round(float(len(flagged)) / n, 4) if n else 0.0,
                "examples": [{"value": r.get("value"), "verdict": str(flagger(r))} for r in flagged[:5]]}

    out = {}
    worst_lower = 0.0
    for arm, bucket in sorted(per_arm.items()):
        correct = measure(bucket["correct"])
        incorrect = measure(bucket["incorrect"])
        lo, _hi = wilson(correct["flagged"], correct["n"])
        out[arm] = {
            "correct_items": correct,
            "incorrect_items": incorrect,
            # Recall is the share of *wrong* items the flagger condemns. E134
            # found this field computing its complement, so a flagger that caught
            # every wrong item reported ``recall 0.0``; the miss rate is now
            # reported under its own name rather than inside the recall field.
            "recall_on_incorrect": (round(incorrect["rate"], 4) if incorrect["n"] else None),
            "miss_rate_on_incorrect": (round(1.0 - incorrect["rate"], 4) if incorrect["n"] else None),
            "fp_wilson_lower": round(lo, 4),
        }
        worst_lower = max(worst_lower, lo)

    condemned = [a for a in out if out[a]["correct_items"]["n"] > 0 and out[a]["fp_wilson_lower"] > fp_ceiling]
    if condemned:
        verdict = "ALTERNATE_FORM_FP"
        reason = ("the flagger condemns correct items beyond the declared ceiling "
                  "(Wilson lower bound > %.2f) on arm(s): %s" % (fp_ceiling, ", ".join(condemned)))
    elif not any(out[a]["correct_items"]["n"] for a in out):
        verdict = "NO_LABELLED_CORRECT_ITEMS"
        reason = "the control set holds no items labelled correct: this check measured nothing"
    elif not any(out[a]["incorrect_items"]["n"] for a in out):
        # E134 ran this check on 200 rows of a published lm-eval run, recomputed
        # the correct arm from the run's own shipped inputs, found every one of
        # them correct and not one incorrect, and the flagger scored a perfect
        # pass. A verifier with no wrong answers cannot fail: there is nothing in
        # the data for a false negative to be a false negative *of*.
        verdict = "NO_LABELLED_INCORRECT_ITEMS"
        reason = ("the control set holds no items labelled incorrect, so this check "
                  "measured only false positives. A flagger that condemns nothing "
                  "scores a perfect pass here, and a false-positive rate on correct "
                  "items is not evidence that the flagger finds wrong ones")
    else:
        verdict = "OK"
        reason = ""

    result = {
        "check": "C2_alternate_form_fp",
        "verdict": verdict,
        "reason": reason,
        "fp_ceiling": fp_ceiling,
        "worst_fp_wilson_lower": round(worst_lower, 4),
        "arms": out,
    }
    if not arms and len(out) == 1:
        only = list(out.values())[0]
        result["summary"] = fmt_interval(only["correct_items"]["flagged"], only["correct_items"]["n"])
    return result