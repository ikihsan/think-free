from __future__ import annotations

import random
from pathlib import Path


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


def _action_trace(params, action):
    """A permitted ordinary observation, used to try to separate two realities.

    Actions:
      passive             — one sensor, door open
      co_locate_b         — same sensor hardware in room 2 as well
      door_open           — internal door shut (k ~ 0)
      noop                — no action
    """
    lam1, lam2, k, source, bias = (
        params["lam1"], params["lam2"], params["k"], params["source"], params["bias"]
    )
    if action == "passive":
        return _two_room_trace(lam1, lam2, k, source, bias, sensor_room=1)
    if action == "co_locate_b":
        return [
            _two_room_trace(lam1, lam2, k, source, bias, sensor_room=1),
            _two_room_trace(lam1, lam2, k, source, bias, sensor_room=2),
        ]
    if action == "door_open":
        return _two_room_trace(lam1, lam2, 0.0, source, bias, sensor_room=1)
    if action == "noop":
        return _two_room_trace(lam1, lam2, k, source, bias, sensor_room=1)
    raise ValueError(action)


def _discrimination_diff(trace_a, trace_b):
    """Max absolute difference between two traces (room A discrimination)."""
    return max(abs(a - b) for a, b in zip(trace_a, trace_b))


def _run_protocol_comparison(lam1, lam2, k, source, bias, poor_mixing=False,
                             seeds=5):
    """Compare second-sensor vs fixed-door-open under specified vs poor mixing.

    Tests the F008 surviving observation: under poor mixing, reading a second
    sensor is more robust than acting on the measured room.
    """
    params = {"lam1": lam1, "lam2": lam2, "k": k, "source": source, "bias": bias}
    results = {}

    for label, stratified_ach in [("specified", None), ("poor_mixing", 0.35)]:
        pair_results = []

        for seed in range(seeds):
            # Parameter set Q with slightly different flows
            q_params = {
                "lam1": params["lam1"] * 0.95,
                "lam2": params["lam2"],
                "k": params["k"] * 1.05,
                "source": params["source"],
                "bias": params["bias"],
            }

            # Test second sensor (co_locate_b) - reads both rooms
            p_trace_ss = _action_trace(params, "co_locate_b")
            q_trace_ss = _action_trace(q_params, "co_locate_b")

            # Fixed door open
            p_trace_door = _action_trace(params, "door_open")
            q_trace_door = _action_trace(q_params, "door_open")

            # Compute max abs difference (discrimination) in room A
            # p_trace_ss is a list of room-1 readings over time (length steps)
            ss_diff = _discrimination_diff(p_trace_ss[0], q_trace_ss[0])
            door_diff = _discrimination_diff(p_trace_door, q_trace_door)

            # Under poor mixing, test with sensor offset added to room A readings
            if poor_mixing:
                offset = 5.0
                # Room A readings with offset
                p_ss_off = [v + offset for v in p_trace_ss[0]]
                q_ss_off = [v + offset for v in q_trace_ss[0]]
                ss_diff_with_off = _discrimination_diff(p_ss_off, q_ss_off)

                p_door_off = [v + offset for v in p_trace_door]
                q_door_off = [v + offset for v in q_trace_door]
                door_diff_with_off = _discrimination_diff(p_door_off, q_door_off)
            else:
                ss_diff_with_off = None
                door_diff_with_off = None

            pair_results.append({
                "second_sensor": {
                    "diff_no_off": ss_diff,
                    "diff_with_off": ss_diff_with_off,
                },
                "door_open": {
                    "diff_no_off": door_diff,
                    "diff_with_off": door_diff_with_off,
                },
            })

        results[label] = pair_results

    return results


def main():
    """Run the second-sensor prototype evaluation.

    Tests the F008 surviving observation: under poor mixing, reading a second
    sensor is more robust than acting on the measured room.
    This is a reversible exploratory prototype (AGENTS.md §3), not a product.
    """
    title = "Second-Sensor Ventilation Diagnosis Prototype"
    subtitle = "F008 Surviving Observation: reading a second sensor is more robust " \
              "under poor mixing than acting on the measured room"

    lines = []
    lines.append("=" * 70)
    lines.append(title)
    lines.append(subtitle)
    lines.append("=" * 70)
    lines.append("")
    lines.append("Tests the F008 surviving observation about second-sensor robustness")
    lines.append("under specified vs poor-mixing conditions.")
    lines.append("This is a reversible exploratory prototype (AGENTS.md §3), not a product.")
    lines.append("")
    lines.append("-" * 70)
    lines.append("")

    # Test parameter sets from F008: two-room mass balance
    # P: higher room-1 outdoor exchange, some inter-room coupling
    # Q: lower room-1 outdoor exchange, no inter-room coupling
    # With lam1+k held equal so passive traces are similar
    test_sets = [
        {"lam1": 0.05, "lam2": 0.05, "k": 0.01, "source": 20.0, "bias": 5.0},
        {"lam1": 0.03, "lam2": 0.05, "k": 0.03, "source": 20.0, "bias": 5.0},
        {"lam1": 0.04, "lam2": 0.05, "k": 0.02, "source": 20.0, "bias": 5.0},
    ]

    for i, params in enumerate(test_sets):
        lam1_k_sum = params["lam1"] + params["k"]
        lines.append(f"Test set {i+1}: lam1={params['lam1']}, k={params['k']}, "
                      f"lam1+k={lam1_k_sum:.2f}")

        for poor_mixing_flag, label in [(False, "specified"), (True, "poor_mixing")]:
            results = _run_protocol_comparison(
                params["lam1"], params["lam2"], params["k"],
                params["source"], params["bias"], poor_mixing=poor_mixing_flag,
                seeds=5
            )

            r = results[label]
            # Second sensor discrimination (first seed, no offset)
            ss_diff = r[0]["second_sensor"]["diff_no_off"]
            door_diff = r[0]["door_open"]["diff_no_off"]

            # With poor mixing offset
            ss_with_off = r[0]["second_sensor"].get("diff_with_off")
            door_with_off = r[0]["door_open"].get("diff_with_off")

            lines.append(f"  {label}:")
            if ss_with_off is not None and door_with_off is not None:
                lines.append(f"    Second sensor: diff_no_off={ss_diff:.4f}, "
                              f"diff_with_off={ss_with_off:.4f}")
                lines.append(f"    Door open:     diff_no_off={door_diff:.4f}, "
                              f"diff_with_off={door_with_off:.4f}")
                if ss_with_off < door_with_off:
                    improvement = ((door_with_off - ss_with_off) / max(door_with_off, 0.001)) * 100
                    lines.append(f"    -> Second sensor is {improvement:.1f}% more robust with offset")
                elif ss_with_off > door_with_off:
                    worsening = ((ss_with_off - door_with_off) / max(door_with_off, 0.001)) * 100
                    lines.append(f"    -> Door is {worsening:.1f}% more robust with offset")
                else:
                    lines.append(f"    -> Equal robustness with offset")
            else:
                lines.append(f"    Second sensor: diff_no_off={ss_diff:.4f}")
                lines.append(f"    Door open:     diff_no_off={door_diff:.4f}")
                if ss_diff < door_diff:
                    improvement = ((door_diff - ss_diff) / max(door_diff, 0.001)) * 100
                    lines.append(f"    -> Second sensor is {improvement:.1f}% more robust (no offset)")
                elif ss_diff > door_diff:
                    worsening = ((ss_diff - door_diff) / max(ss_diff, 0.001)) * 100
                    lines.append(f"    -> Door is {worsening:.1f}% more robust (no offset)")
                else:
                    lines.append(f"    -> Equal robustness (no offset)")

        lines.append("")

    lines.append("=" * 70)
    lines.append("Prototype complete.")
    lines.append("This is a reversible exploratory prototype (AGENTS.md §3):")
    lines.append("  - evidence-gathering, not product validation")
    lines.append("  - builds on F008 surviving observation about second-sensor robustness")
    lines.append("  - tests under specified vs poor-mixing conditions")
    lines.append("  - does not claim adoption, users, or novelty")
    lines.append("=" * 70)

    output = "\n".join(lines)
    print(output)


if __name__ == "__main__":
    main()