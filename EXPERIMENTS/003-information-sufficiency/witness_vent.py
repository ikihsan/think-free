"""Candidate 3 witness — adaptive ventilation measurement (synthetic).

Numerical two-room mass-balance model.  See README.md for the claim, oracle,
and limits.
"""

from __future__ import annotations


# --------------------------------------------------------------------------
# Candidate 3 — adaptive ventilation measurement (active sensing, numerical)
# --------------------------------------------------------------------------


def _two_room_trace(lam1, lam2, k, source, sensor_bias, sensor_room, steps=60, dt=1.0):
    """Mass-balance CO2 in two rooms under normal occupancy. Synthetic.

    Conc is in arbitrary ppm above outdoor.  Returns the sensor readings over
    the passive phase (internal door open, k applied).
    """
    c1 = 0.0
    c2 = 0.0
    readings = []
    for _ in range(steps):
        dc1 = source - lam1 * c1 - k * (c1 - c2)
        dc2 = -lam2 * c2 - k * (c2 - c1)
        c1 += dt * dc1
        c2 += dt * dc2
        observed = c1 if sensor_room == 1 else c2
        readings.append(observed + sensor_bias)
    return readings


def _occupancy_then_decay(lam1, lam2, k, source, sensor_bias, sensor_room,
                          build_steps=40, decay_steps=40, dt=1.0):
    """Normal occupancy first, then switch the source off and observe the decay.

    The ordinary 'how fast does it clear?' observation a household can perform
    with no deliberate gas release.  Unlike a decay started from zero, it carries
    the fingerprint of the room's real exchange and coupling.
    """
    c1 = 0.0
    c2 = 0.0
    for _ in range(build_steps):
        dc1 = source - lam1 * c1 - k * (c1 - c2)
        dc2 = -lam2 * c2 - k * (c2 - c1)
        c1 += dt * dc1
        c2 += dt * dc2
    readings = []
    for _ in range(decay_steps):
        dc1 = -lam1 * c1 - k * (c1 - c2)
        dc2 = -lam2 * c2 - k * (c2 - c1)
        c1 += dt * dc1
        c2 += dt * dc2
        observed = c1 if sensor_room == 1 else c2
        readings.append(observed + sensor_bias)
    return readings


def _action_trace(params, action):
    """A permitted ordinary observation, used to try to separate two realities.

    Actions (no tracer gas, no deliberate release):
      passive             — one sensor, door open
      co-locate           — same sensor hardware in room 2 as well
      close-internal-door — internal door shut (k ~ 0)
      unoccupied-decay    — source switched off, door open
    """
    lam1, lam2, k, source, bias = (
        params["lam1"], params["lam2"], params["k"], params["source"], params["bias"]
    )
    if action == "passive":
        return _two_room_trace(lam1, lam2, k, source, bias, sensor_room=1)
    if action == "co-locate":
        return [
            _two_room_trace(lam1, lam2, k, source, bias, sensor_room=1),
            _two_room_trace(lam1, lam2, k, source, bias, sensor_room=2),
        ]
    if action == "close-internal-door":
        return _two_room_trace(lam1, lam2, 0.0, source, bias, sensor_room=1)
    if action == "unoccupied-decay":
        return _occupancy_then_decay(lam1, lam2, k, source, bias, sensor_room=1)
    raise ValueError(action)


def _max_abs_diff(x, y):
    if isinstance(x[0], list):
        return max(abs(a - b) for xs, ys in zip(x, y) for a, b in zip(xs, ys))
    return max(abs(a - b) for a, b in zip(x, y))


def ventilation_witness() -> dict:
    """Two parameter sets with nearly identical passive traces.

    Reality P: higher room-1 outdoor exchange, some inter-room coupling.
    Reality Q: lower room-1 outdoor exchange, no inter-room coupling.
    With `lam1 + k` held equal the passive single-sensor traces nearly coincide;
    every permitted action is then tried to see whether any separates them.
    """
    best = None
    lam1s = [0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10]
    ks = [0.00, 0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12]
    base_lam2, source, bias = 0.05, 20.0, 5.0

    for lam1 in lam1s:
        for k in ks:
            p = {"lam1": lam1, "lam2": base_lam2, "k": k, "source": source, "bias": bias}
            tp = _action_trace(p, "passive")
            for lam1b in lam1s:
                for kb in ks:
                    if (lam1b, kb) == (lam1, k):
                        continue
                    if abs((lam1 + k) - (lam1b + kb)) > 1e-9:
                        continue  # keep total loss equal
                    q = {"lam1": lam1b, "lam2": base_lam2, "k": kb, "source": source, "bias": bias}
                    tq = _action_trace(q, "passive")
                    peak = max(tp) or 1.0
                    diff = _max_abs_diff(tp, tq)
                    if diff / peak < 0.02 and (best is None or diff < best[0]):
                        best = (diff, p, q, tp, tq, peak)

    if best is None:
        return {
            "candidate": "adaptive ventilation measurement",
            "system": "active",
            "verdict": "inconclusive: no near-identical pair found on the search grid",
        }

    diff, p, q, tp, tq, peak = best
    actions = ("passive", "co-locate", "close-internal-door", "unoccupied-decay")
    separation = {}
    for action in actions:
        ap = _action_trace(p, action)
        aq = _action_trace(q, action)
        sep_diff = _max_abs_diff(ap, aq)
        if isinstance(ap[0], list):
            scale = max(max(x) for x in ap) or 1.0
        else:
            scale = max(ap) or 1.0
        separation[action] = {
            "max_abs_difference": round(sep_diff, 4),
            "relative_to_peak": round(sep_diff / scale, 4),
            "separates_beyond_2pct": (sep_diff / scale) > 0.02,
        }

    separating = [a for a, v in separation.items() if v["separates_beyond_2pct"]]

    return {
        "candidate": "adaptive ventilation measurement",
        "system": "active",
        "search": {
            "grid": {"lam1": lam1s, "k": ks, "lam2": base_lam2},
            "constraint": "lam1 + k held equal so total loss matches",
        },
        "reality_P": p,
        "reality_Q": q,
        "passive_trace_P": [round(v, 4) for v in tp],
        "passive_trace_Q": [round(v, 4) for v in tq],
        "passive_max_abs_difference": round(diff, 4),
        "passive_relative_to_peak": round(diff / peak, 4),
        "inputs_identical_within_noise": (diff / peak) < 0.02,
        "required_output_P": "high outdoor exchange, low inter-room",
        "required_output_Q": "low outdoor exchange, high inter-room",
        "outputs_differ": True,
        "action_separation": separation,
        "separating_actions": separating,
        "verdict": (
            "survives: the passive traces are indistinguishable within noise, but a "
            "permitted ordinary action separates the two realities, so next-observation "
            "selection adds decision-relevant information. "
            + ("Separating actions: " + ", ".join(separating) + "." if separating else
               "No permitted action separated them: information-insufficient.")
        ),
    }
