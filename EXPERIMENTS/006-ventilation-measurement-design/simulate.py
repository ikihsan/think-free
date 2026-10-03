#!/usr/bin/env python3
"""The world: a two-room mass-balance CO2 simulator.  SYNTHETIC.

Deliberately small and explicit; it is a stand-in for a room, not a claim about
one. Volumes in m3, flows reported as air changes per hour, CO2 in ppm, and an
occupancy source of 0.005 L/s per person (the usual figure for a sedentary
adult). The only integrator lives here, so the world and the fitter cannot drift
apart: the fitter calls the same function with one well-mixed node per room and
adds no noise.

State equations, per room:

    dC/dt = (q_ext / V) * (C_out - C) + (q_ab / V) * (C_other - C) + S / V

`S` is that room's own occupants. A neighbour that is occupied all afternoon
therefore sits high in CO2 when it is poorly ventilated and low when it is not,
which is what makes "open the internal door" an informative measurement rather
than a gesture.

With `stratified_ach` set, each room's sensor node exchanges with the rest of its
room only through that limited path, so a one-node fit is misspecified even when
every parameter is right. That is the point of the poor-mixing holdout.
"""

from __future__ import annotations

import math

# Occupancy CO2 output, litres per second per person.
L_PER_PERSON_S = 5e-3

# Explicit integration step. The slowest exchange here has a time constant of
# order 10^4 s, so 15 s is a ratio near 1/2500 and the truncation error stays
# well under the 6 ppm sensor noise. Halving it costs minutes of CPU and changes
# no reported number.
DT_S = 15.0


def ppm_from_litres(co2_litres, volume_m3):
    """A CO2 rate in L/s over a volume in m3, expressed in ppm per second.

    1 L/m3 is 1e-3 of the volume, and 1e-3 is 1000 ppm. Getting this factor wrong
    by a thousand is invisible in the code and obvious in the output: two people
    in a 30 m3 room would pass 2000 ppm in four minutes.
    """
    return co2_litres / volume_m3 * 1000.0


class Action:
    """What the person does at the decision point.

    `q_ab` and `q_ext_a` are absolute air changes per hour, so an action can
    create inter-room exchange even for a hypothesis whose baseline is zero.
    `channels` says which sensors are read after the action: "a" is the ordinary
    single-sensor case, "ab" is the extra simultaneous reading in the neighbour
    that `RESEARCH/C.md` proposes.
    """

    def __init__(self, name, q_ab_ach=None, q_ext_a_ach=None, channels="a",
                 duration_s=900.0):
        self.name = name
        self.q_ab_ach = q_ab_ach
        self.q_ext_a_ach = q_ext_a_ach
        self.channels = channels
        self.duration_s = float(duration_s)

    def __repr__(self):
        return f"Action({self.name})"


MENU = [
    Action("door_open", q_ab_ach=1.2),
    Action("co_locate_b", channels="ab"),
    Action("window_a_open", q_ext_a_ach=1.5),
    Action("noop"),
]


class Schedule:
    """Sample times plus the interventions, each starting at a known time."""

    def __init__(self, times, events=None):
        self.times = list(times)
        self.events = sorted(events or [], key=lambda e: e[0])

    def active(self, t):
        """The action in effect at `t`, or None."""
        for start, action in self.events:
            if start <= t < start + action.duration_s:
                return action
        return None

    def flows(self, t, q_ext_a, q_ab):
        action = self.active(t)
        ext = q_ext_a if action is None else action.q_ext_a_ach
        ab = q_ab if action is None else action.q_ab_ach
        return (q_ext_a if ext is None else ext), (q_ab if ab is None else ab)

    def channels(self, t):
        action = self.active(t)
        return "a" if action is None else action.channels


class Environment:
    """Outdoor level, weather multiplier, and two occupancy schedules."""

    def __init__(self, vol_a, vol_b, people_a, phase1_s, people_a_after,
                 people_b, c_out_base, weather_fn=None):
        self.vol_a = float(vol_a)
        self.vol_b = float(vol_b)
        self.people_a = float(people_a)
        self.phase1_s = float(phase1_s)
        self.people_a_after = float(people_a_after)
        self.people_b = float(people_b)
        self.c_out_base = float(c_out_base)
        self.weather_fn = weather_fn or (lambda t: 1.0)

    def c_out(self, t):
        return self.c_out_base + 6.0 * math.sin(t / 3600.0)

    def weather(self, t):
        return self.weather_fn(t)

    def people_a_at(self, t):
        return self.people_a if t < self.phase1_s else self.people_a_after

    def people_b_at(self, t):
        return self.people_b


def simulate_schedule(cand, schedule, env, stratified_ach=None):
    """True concentrations at the sample times under `cand`'s baseline flows.

    `cand` supplies `q_ext_a`, `q_ext_b`, and `q_ab` in air changes per hour.
    """
    state = {"a": env.c_out(0.0), "b": env.c_out(0.0)}
    out = []
    clock = 0.0
    for t in schedule.times:
        while clock < t:
            dt = min(DT_S, t - clock)
            mid = clock + dt / 2.0
            ext_a, ab = schedule.flows(mid, cand["q_ext_a"], cand["q_ab"])
            q_e = ext_a / 3600.0 * env.weather(mid)
            q_eb = cand["q_ext_b"] / 3600.0 * env.weather(mid)
            coupling = ab / 3600.0 if stratified_ach is None \
                else stratified_ach / 3600.0
            c_out = env.c_out(mid)
            src_a = ppm_from_litres(env.people_a_at(mid) * L_PER_PERSON_S, env.vol_a)
            src_b = ppm_from_litres(env.people_b_at(mid) * L_PER_PERSON_S, env.vol_b)
            state["a"] += dt * (q_e * (c_out - state["a"])
                                + coupling * (state["b"] - state["a"]) + src_a)
            state["b"] += dt * (q_eb * (c_out - state["b"])
                                + coupling * (state["a"] - state["b"]) + src_b)
            clock += dt
        out.append((state["a"], state["b"]))
    return out


def observe(truth, offsets, noise_sd, rng):
    """Add each sensor's offset and Gaussian noise to a true trace."""
    return [(row[0] + offsets[0] + rng.gauss(0.0, noise_sd),
             row[1] + offsets[1] + rng.gauss(0.0, noise_sd)) for row in truth]


def trace_rms(a, b):
    """Root-mean-square difference between two traces of equal length."""
    if not a:
        return float("nan")
    return math.sqrt(sum((x[0] - y[0]) ** 2 for x, y in zip(a, b)) / len(a))