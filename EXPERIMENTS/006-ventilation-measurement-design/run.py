#!/usr/bin/env python3
"""Run C2's ventilation measurement-design kill gate.  SYNTHETIC.

Compares three protocols at one budget on paired hypotheses whose passive trace
in the measured room is, by construction, the same; plus holdouts whose weather
and mixing violate the fitter's model. The kill gate is in `README.md` and was
fixed before this ran. Says nothing about a real room or a real sensor.
"""

from __future__ import annotations

import json
import math
import random
import time
from pathlib import Path

from estimator import choose_action, fit, schedule_for, score_hypothesis
from simulate import Environment, Schedule, observe, simulate_schedule, trace_rms

HERE = Path(__file__).resolve().parent
OUT = HERE / "results.json"

# One schedule for every protocol: six slots, one decision, six more slots.
BASELINE_TIMES = [300.0, 600.0, 900.0, 1200.0, 1500.0, 1800.0]
POST_TIMES = [2400.0, 2700.0, 3000.0, 3300.0, 3600.0, 4200.0]
ALL_TIMES = BASELINE_TIMES + POST_TIMES
ACTION_START = 1800.0
PHASE1_S = 1800.0

PROTOCOLS = ["passive", "fixed", "adaptive"]
NOISE_SD = 6.0
SEEDS = 8
# An interval no wider than this counts as "precise": the grid step is 0.2 ACH,
# so this is two grid points, and it is a resolution a household could act on.
PRECISE_WIDTH_ACH = 0.4


def pair_families():
    """Paired hypotheses that room A alone cannot tell apart.

    Each pair holds the air change out of room A (`q_ext_a + q_ab`) fixed, so the
    passive trace in the measured room is the same in both, and moves the
    difference into where the air actually goes: outdoors, or through an occupied
    neighbouring room. `off_a` is the sensor offset, which is the third story in
    `RESEARCH/C.md`.
    """
    return [
        {"name": "neighbour_stuffy", "total": 0.9,
         "a": {"q_ext_a": 0.9, "q_ab": 0.0, "q_ext_b": 0.1, "off_a": 45.0},
         "b": {"q_ext_a": 0.9, "q_ab": 0.0, "q_ext_b": 1.4, "off_a": 0.0}},
        {"name": "neighbour_mild", "total": 0.6,
         "a": {"q_ext_a": 0.6, "q_ab": 0.0, "q_ext_b": 0.3, "off_a": 30.0},
         "b": {"q_ext_a": 0.6, "q_ab": 0.0, "q_ext_b": 0.9, "off_a": -10.0}},
        {"name": "coupled_vs_outdoor", "total": 1.0,
         "a": {"q_ext_a": 0.2, "q_ab": 0.8, "q_ext_b": 0.7, "off_a": 20.0},
         "b": {"q_ext_a": 1.0, "q_ab": 0.0, "q_ext_b": 0.7, "off_a": 0.0}},
        {"name": "near_degenerate", "total": 1.0,
         "a": {"q_ext_a": 0.9, "q_ab": 0.1, "q_ext_b": 0.7, "off_a": 0.0},
         "b": {"q_ext_a": 1.0, "q_ab": 0.0, "q_ext_b": 0.7, "off_a": 0.0}},
        {"name": "deep_seal", "total": 1.3,
         "a": {"q_ext_a": 1.3, "q_ab": 0.0, "q_ext_b": 0.15, "off_a": 40.0},
         "b": {"q_ext_a": 1.3, "q_ab": 0.0, "q_ext_b": 1.1, "off_a": 0.0}},
        # Control: identical flows, different sensor offset. Nothing separates
        # these, and no protocol is allowed to succeed here.
        {"name": "offset_only", "total": 0.8,
         "a": {"q_ext_a": 0.8, "q_ab": 0.0, "q_ext_b": 0.7, "off_a": 45.0},
         "b": {"q_ext_a": 0.8, "q_ab": 0.0, "q_ext_b": 0.7, "off_a": -45.0}},
    ]


def conditions():
    """The specified condition and the two violations the fitter cannot model."""
    return [
        {"name": "specified", "weather_fn": None, "stratified_ach": None},
        {"name": "changing_weather",
         "weather_fn": lambda t: 1.0 + 0.6 * math.sin(t / 2400.0),
         "stratified_ach": None},
        {"name": "poor_mixing", "weather_fn": None, "stratified_ach": 0.35},
    ]


def make_env(cond):
    return Environment(
        vol_a=30.0, vol_b=25.0, people_a=2.0, phase1_s=PHASE1_S,
        people_a_after=0.0, people_b=1.0, c_out_base=420.0,
        weather_fn=(lambda t: 1.0) if cond["weather_fn"] is None else cond["weather_fn"],
    )


def run_case(pair, cond, seed):
    """One pair, one condition, one noise seed: all three protocols on one world."""
    rng = random.Random(seed)
    env = make_env(cond)
    hypos = [dict(pair["a"]), dict(pair["b"])]
    truth_index = 0 if rng.random() < 0.5 else 1
    truth = hypos[truth_index]
    offsets = (truth["off_a"], 0.0)

    passive = Schedule(BASELINE_TIMES, [])
    separation = trace_rms(
        simulate_schedule(truth, passive, env, cond["stratified_ach"]),
        simulate_schedule(hypos[1 - truth_index], passive, env, cond["stratified_ach"]))

    row = {"case": f"{pair['name']}|{cond['name']}|seed{seed:02d}",
           "pair": pair["name"], "condition": cond["name"], "seed": seed,
           "total_ach": pair["total"],
           "passive_trace_rms_ppm": round(separation, 2),
           "protocols": {}}
    for protocol in PROTOCOLS:
        action_name = None
        if protocol == "adaptive":
            decision = choose_action(hypos, ACTION_START, POST_TIMES, env)
            action_name = decision["action"]
            row["action_choice"] = decision
        schedule = schedule_for(protocol, ALL_TIMES, ACTION_START, action_name)
        clean = simulate_schedule(truth, schedule, env, cond["stratified_ach"])
        readings = observe(clean, offsets, NOISE_SD, rng)
        score_true = score_hypothesis(truth, schedule, env, readings)
        score_other = score_hypothesis(hypos[1 - truth_index], schedule, env, readings)
        estimated = fit(schedule, env, readings)
        low, high = estimated["ci"]
        covered = low <= truth["q_ext_a"] <= high
        precise = estimated["ci_width"] <= PRECISE_WIDTH_ACH
        row["protocols"][protocol] = {
            "action": action_name or ("none" if protocol == "passive" else "door_open"),
            "picked_true": score_true < score_other,
            "rss_margin": round(score_other - score_true, 1),
            "q_ext_a_hat": estimated["q_ext_a"],
            "q_ext_a_true": truth["q_ext_a"],
            "abs_error_ach": round(abs(estimated["q_ext_a"] - truth["q_ext_a"]), 2),
            "ci": [low, high],
            "ci_width": round(estimated["ci_width"], 2),
            "covered": covered,
            "false_precise": bool(precise and not covered),
        }
    return row


def aggregate(rows, protocol, condition=None):
    picked = [r for r in rows
              if not r.get("refused") and r["protocols"].get(protocol)
              and (condition is None or r["condition"] == condition)]
    if not picked:
        return {}
    errors = sorted(r["protocols"][protocol]["abs_error_ach"] for r in picked)
    total = len(picked)
    return {
        "cases": total,
        "discrimination_accuracy": round(
            sum(1 for r in picked if r["protocols"][protocol]["picked_true"]) / total, 3),
        "median_abs_error_ach": errors[total // 2],
        "max_abs_error_ach": errors[-1],
        "coverage_90": round(
            sum(1 for r in picked if r["protocols"][protocol]["covered"]) / total, 3),
        "false_precise_rate": round(
            sum(1 for r in picked if r["protocols"][protocol]["false_precise"]) / total, 3),
        "mean_margin": round(
            sum(r["protocols"][protocol]["rss_margin"] for r in picked) / total, 1),
    }


def by_pair(rows, protocol):
    out = {}
    for pair in sorted({r["pair"] for r in rows}):
        subset = [r for r in rows if r["pair"] == pair
                  and r["condition"] == "specified" and r["protocols"].get(protocol)]
        if subset:
            out[pair] = round(sum(1 for r in subset
                                  if r["protocols"][protocol]["picked_true"])
                              / len(subset), 3)
    return out


def main() -> int:
    started = time.time()
    rows = []
    for pair in pair_families():
        for cond in conditions():
            for seed in range(SEEDS):
                rows.append(run_case(pair, cond, 1000 + seed))

    names = [c["name"] for c in conditions()]
    by_protocol = {p: aggregate(rows, p) for p in PROTOCOLS}
    by_condition = {p: {c: aggregate(rows, p, c) for c in names} for p in PROTOCOLS}
    separations = [r["passive_trace_rms_ppm"] for r in rows
                   if r["pair"] != "offset_only"]
    actions = {}
    for row in rows:
        choice = row.get("action_choice")
        if choice:
            actions[choice["action"]] = actions.get(choice["action"], 0) + 1
    specified = {p: by_condition[p]["specified"] for p in PROTOCOLS}
    holdout_false = {
        p: round(sum(by_condition[p][c]["false_precise_rate"]
                     for c in names if c != "specified") / 2, 3)
        for p in PROTOCOLS
    }
    gate_1 = specified["adaptive"]["discrimination_accuracy"] > \
        specified["fixed"]["discrimination_accuracy"]
    gate_2 = holdout_false["adaptive"] < holdout_false["fixed"]

    results = {
        "schema": "origin.experiment.ventilation-measurement-design/1",
        "experiment": "006-ventilation-measurement-design",
        "synthetic": True,
        "note": (
            "Two-room mass-balance world, one shared grid fitter, three protocols "
            "at one budget (12 slots, one decision). Establishes nothing about a "
            "real room, a real sensor, or usefulness."
        ),
        "budget": {
            "slots_per_protocol": len(ALL_TIMES),
            "decisions_per_protocol": 1,
            "baseline_times_s": BASELINE_TIMES,
            "post_times_s": POST_TIMES,
            "action_start_s": ACTION_START,
            "menu": ["door_open", "co_locate_b", "window_a_open", "noop"],
        },
        "estimator": {
            "kind": "grid maximum likelihood, read-sensor offsets solved in closed form",
            "q_ext_a_grid": "0.0-1.4 ACH step 0.2",
            "q_ab_grid": "0.0-1.2 ACH step 0.4",
            "q_ext_b_nuisance_grid": "0.0, 0.6, 1.2 ACH",
            "interval": "90% profile likelihood, chi2(0.90,1)/2 = 1.353",
            "noise_sd_ppm": NOISE_SD,
            "precise_width_ach": PRECISE_WIDTH_ACH,
        },
        "pairs_tested": len(pair_families()),
        "cases_run": len(rows),
        "seeds_per_case": SEEDS,
        "passive_trace_separation_ppm": {
            "min": min(separations), "max": max(separations),
            "mean": round(sum(separations) / len(separations), 2),
        },
        "adaptive_action_choices": actions,
        "by_protocol": by_protocol,
        "by_protocol_and_condition": by_condition,
        "specified_pair_accuracy": {p: by_pair(rows, p) for p in PROTOCOLS},
        "holdout_false_precise_rate": holdout_false,
        "false_precise_rate": holdout_false["adaptive"],
        "adaptive_better_than_fixed": bool(gate_1),
        "kill_gate": {
            "1_discrimination_on_specified_cases": {
                "required": "adaptive > fixed",
                "adaptive": specified["adaptive"]["discrimination_accuracy"],
                "fixed": specified["fixed"]["discrimination_accuracy"],
                "met": bool(gate_1),
            },
            "2_false_precise_on_violations": {
                "required": "adaptive < fixed",
                "adaptive": holdout_false["adaptive"],
                "fixed": holdout_false["fixed"],
                "met": bool(gate_2),
            },
        },
        "cases": rows,
    }
    OUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"cases run: {len(rows)} over {results['pairs_tested']} pairs, {SEEDS} seeds each")
    print("passive room-A separation between paired hypotheses: "
          f"{results['passive_trace_separation_ppm']['min']}-"
          f"{results['passive_trace_separation_ppm']['max']} ppm RMS "
          "(0 by construction, noise remains)")
    print(f"adaptive actions chosen: {actions}")
    print()
    print(f"  {'protocol':<10} {'condition':<17} {'discrim':>8} {'medErr':>7} "
          f"{'cov90':>6} {'falsePrec':>10} {'margin':>9}")
    for protocol in PROTOCOLS:
        for condition in names:
            a = by_condition[protocol][condition]
            print(f"  {protocol:<10} {condition:<17} {a['discrimination_accuracy']:>8} "
                  f"{a['median_abs_error_ach']:>7} {a['coverage_90']:>6} "
                  f"{a['false_precise_rate']:>10} {a['mean_margin']:>9}")
    print()
    print("  specified-case accuracy per pair:")
    for pair in results["specified_pair_accuracy"]["passive"]:
        line = " ".join(
            f"{p}={results['specified_pair_accuracy'][p][pair]:.2f}" for p in PROTOCOLS)
        print(f"    {pair:<22} {line}")
    print()
    for name, gate in results["kill_gate"].items():
        print(f"  kill gate {name}: met={gate['met']} ({gate['required']}) "
              f"adaptive={gate['adaptive']} fixed={gate['fixed']}")
    print()
    print(f"wrote {OUT}  (wall {time.time() - started:.1f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())