#!/usr/bin/env python3
"""Shared estimator, action menu, and the adaptive rule.  SYNTHETIC.

One estimator serves every protocol on purpose. If the protocols differed in how
well they *fit*, the comparison would measure the fitter instead of the
measurement design. What differs is only which sensors were read and which
action was taken when.

Fitter: grid maximum likelihood over the outdoor exchange in A, the inter-room
exchange, and zone B's outdoor exchange as a nuisance, with each read sensor's
offset solved in closed form, because for fixed flows the residual sum of squares
is a quadratic in the offset. Intervals are profile-likelihood intervals at 90%
level: a value is inside when the best residual sum of squares reachable at that
value is within `LR90 * sigma-hat^2` of the minimum, the standard
one-degree-of-freedom likelihood-ratio threshold.

Protocols, all at the same budget (12 sample slots, one decision):

* `passive`  — twelve slots, room A only, no intervention.
* `fixed`    — the same twelve slots, with a prescribed door-open window.
* `adaptive` — the same twelve slots; the action is chosen from the menu to
               maximise the worst-case separation between the two hypotheses
               still standing.

The adaptive rule is allowed to know which two hypotheses are still standing. A
field system would also have to *generate* that pair from data; this experiment
starts after that step, which is a ceiling on what any result here can mean.
"""

from __future__ import annotations

from simulate import MENU, Schedule, simulate_schedule, trace_rms

# One-degree-of-freedom 90% likelihood-ratio threshold: chi2(0.90, 1) / 2.
LR90 = 1.353

EXT_GRID = [round(0.2 * i, 2) for i in range(0, 8)]
AB_GRID = [round(0.4 * i, 2) for i in range(0, 4)]
Q_EXT_B_GRID = [0.0, 0.6, 1.2]
FITTED_PARAMS = 5  # three flows plus two solved offsets


def channel_mask(schedule):
    """Which sensor is read at each sample time, as a list of (use_a, use_b)."""
    return [((True, True) if schedule.channels(t) == "ab" else (True, False))
            for t in schedule.times]


def residuals(cand, schedule, env, readings, mask):
    """Signed residual vectors per read sensor for one candidate."""
    truth = simulate_schedule(cand, schedule, env)
    ra = [truth[i][0] - readings[i][0] for i in range(len(readings))]
    rb = [truth[i][1] - readings[i][1] for i in range(len(readings))]
    return ra, rb, mask


def rss_with_offsets(ra, rb, mask):
    """Residual sum of squares, solving each read sensor's offset in closed form.

    A sensor that was never read is skipped rather than given a fake zero
    reading: reading room B is a choice, and it must cost something.
    """
    total = 0.0
    for column, used in ((ra, 0), (rb, 1)):
        res = [r for r, (a, b) in zip(column, mask) if (a, b)[used]]
        if not res:
            continue
        mean = sum(res) / len(res)
        total += sum((r - mean) ** 2 for r in res)
    return total


def profile_interval(table, best_rss, n):
    """90% profile-likelihood interval for the outdoor exchange in room A.

    The profile lives on a grid, so the interval is widened by half a grid step
    on each side. Without that widening an interval collapses onto the grid point
    that won, and every true value between two grid points is scored as a miss:
    a measurement artefact that would look exactly like overconfidence.
    """
    sigma2 = best_rss / max(1, n - FITTED_PARAMS)
    threshold = best_rss + LR90 * sigma2
    best_per_ext = {}
    for (q_ext_a, _q_ab, _q_b), score in table.items():
        if q_ext_a not in best_per_ext or score < best_per_ext[q_ext_a]:
            best_per_ext[q_ext_a] = score
    inside = sorted(q for q, score in best_per_ext.items() if score <= threshold)
    if not inside:
        return None
    step = (EXT_GRID[1] - EXT_GRID[0]) / 2.0
    return (max(EXT_GRID[0], min(inside) - step), min(EXT_GRID[-1], max(inside) + step))


def fit(schedule, env, readings):
    """Grid maximum likelihood; sensor offsets solved analytically.

    The fitter always uses its own well-mixed model and knows nothing about
    weather or stratification, so both holdouts are misspecified by
    construction.
    """
    mask = channel_mask(schedule)
    table = {}
    best = None
    for q_ext_a in EXT_GRID:
        for q_ab in AB_GRID:
            for q_ext_b in Q_EXT_B_GRID:
                cand = {"q_ext_a": q_ext_a, "q_ab": q_ab, "q_ext_b": q_ext_b}
                ra, rb, m = residuals(cand, schedule, env, readings, mask)
                score = rss_with_offsets(ra, rb, m)
                table[(q_ext_a, q_ab, q_ext_b)] = score
                if best is None or score < best["rss"]:
                    best = {"q_ext_a": q_ext_a, "q_ab": q_ab,
                            "q_ext_b": q_ext_b, "rss": score}
    n = sum(1 for a, _b in mask if a) + sum(1 for _a, b in mask if b)
    inside = profile_interval(table, best["rss"], n)
    result = dict(best)
    result["ci"] = inside if inside else (best["q_ext_a"], best["q_ext_a"])
    result["ci_width"] = result["ci"][1] - result["ci"][0]
    return result


def score_hypothesis(hypo, schedule, env, readings):
    """Best residual sum of squares for a hypothesis whose flows are fixed.

    Read-sensor offsets are still solved, so a hypothesis is never penalised for
    a sensor that simply reads high.
    """
    mask = channel_mask(schedule)
    cand = {"q_ext_a": hypo["q_ext_a"], "q_ab": hypo["q_ab"], "q_ext_b": hypo["q_ext_b"]}
    ra, rb, m = residuals(cand, schedule, env, readings, mask)
    return rss_with_offsets(ra, rb, m)


def choose_action(hypos, action_start, post_times, env, nuisances=(0.8, 0.9, 1.0, 1.1, 1.2)):
    """Pick the menu action with the largest worst-case separation.

    Separation is the RMS difference between the two hypotheses' predicted
    readings over the post-decision slots, on the channels that action would
    read, minimised over a nuisance scaling of the outdoor exchange. Taking the
    worst case stops the rule from choosing an action that separates the pair
    only when the flows happen to be exact.
    """
    scores = {}
    for action in MENU:
        post = Schedule(post_times, [(action_start, action)])
        channels = post.channels(post_times[0])
        worst = None
        for scale in nuisances:
            trace_a = simulate_schedule(
                dict(hypos[0], q_ext_a=hypos[0]["q_ext_a"] * scale), post, env)
            trace_b = simulate_schedule(
                dict(hypos[1], q_ext_a=hypos[1]["q_ext_a"] * scale), post, env)
            sep = trace_rms(trace_a, trace_b)
            if channels == "ab":
                # Pooled over the channels this action would read, so reading a
                # second sensor is rewarded in proportion to what it adds rather
                # than because one lucky channel separates.
                sep = ((sep ** 2 + _rms_b(trace_a, trace_b) ** 2) / 2.0) ** 0.5
            worst = sep if worst is None else min(worst, sep)
        scores[action.name] = round(worst, 3)
    best_name = max(scores, key=lambda key: scores[key])
    return {"action": best_name, "separation": scores[best_name], "scores": scores}


def _rms_b(a, b):
    total = sum((x[1] - y[1]) ** 2 for x, y in zip(a, b))
    return (total / len(a)) ** 0.5


def schedule_for(protocol, times, action_start, action_name=None):
    """Build a schedule. The sample times are identical for all three protocols."""
    if protocol == "passive":
        return Schedule(times, [])
    action = next(a for a in MENU if a.name == (action_name or "door_open"))
    return Schedule(times, [(action_start, action)])