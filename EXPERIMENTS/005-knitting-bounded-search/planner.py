#!/usr/bin/env python3
"""Knitting Stage A, follow-up: the bounded-neighbourhood planner.  SYNTHETIC.

T-0010 (`EXPERIMENTS/004-knitting-stage-a/`) showed that the candidate's naive
per-error rule is valid but suboptimal exactly when one release covers several
errors. This module implements the repair that experiment named as the next
test: *close releases before deciding patches*, and search only inside bounded
neighbourhoods instead of the whole case.

The grid model and the exhaustive oracle are imported unchanged from 004 so the
comparison is apples-to-apples with T-0010.

Planner
-------
1. Group errors whose individual release closures intersect (union-find). Two
   errors that can never share a released loop are independent problems.
2. Split each group into chunks of at most `cap` errors. `cap=None` keeps whole
   neighbourhoods; a small cap is the honest way to bound the work when one
   neighbourhood is large.
3. Inside each chunk, enumerate every patch/release choice that covers the chunk,
   rank by local cost, and keep the best `beam` of them.
4. Combine one candidate per chunk: take the union of the releases, re-close it
   once so the plan is a legal closure, charge the union once, and drop patched
   cells that the closure already covers.

Why this is bounded, and where it can fail
-----------------------------------------
Enumerated patch subsets are `sum(2**|chunk|)` rather than the oracle's
`2**|errors|`, and the combination search is `prod(beam ** chunks)` rather than
`prod(|candidates|)`. Coverage is structural, so the plan is valid by
construction: every error is either patched or inside its chunk's closure, and
every chunk closure is inside the union's closure.

It can still be cost-suboptimal. Charging the union once is only additive when
distinct neighbourhoods have disjoint release closures; that holds by
construction here (overlapping closures would have merged the groups) and is
*checked*, not assumed. Splitting one neighbourhood into several chunks breaks
that additivity, so a small `cap` can cost more than it saves. Both are measured
by `run.py` rather than argued about.
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL_PATH = HERE.parent / "004-knitting-stage-a" / "planner.py"


def load_model():
    """Import 004's model and oracle unchanged, so costs stay comparable."""
    spec = importlib.util.spec_from_file_location("knitting004", MODEL_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("knitting004", module)
    spec.loader.exec_module(module)
    return module


MODEL = load_model()
Patch = MODEL.Patch


def patch_cost() -> int:
    """Read the shared model constant at call time so sweeps can vary it."""
    return MODEL.PATCH_COST


def neighbourhoods(patch):
    """Union-find over errors whose individual release closures overlap.

    Errors in different groups can never share a released loop, which is what
    makes the per-group costs separable.
    """
    parent = {e: e for e in patch.errors}

    def find(e):
        while parent[e] != e:
            parent[e] = parent[parent[e]]
            e = parent[e]
        return e

    closures = {e: patch.release_closure({e}) for e in patch.errors}
    for a, b in itertools.combinations(sorted(patch.errors), 2):
        if closures[a] & closures[b]:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
    groups = {}
    for e in sorted(patch.errors):
        groups.setdefault(find(e), []).append(e)
    return list(groups.values())


def split_chunks(group, cap):
    """A neighbourhood is one chunk unless `cap` forces it to be split."""
    ordered = sorted(group)
    if cap is None or cap >= len(ordered):
        return [tuple(ordered)]
    size = max(1, int(cap))
    return [tuple(ordered[i : i + size]) for i in range(0, len(ordered), size)]


def chunk_candidates(patch, chunk):
    """Every (patched, released, local_cost) choice that covers the chunk."""
    out = []
    for k in range(len(chunk) + 1):
        for combo in itertools.combinations(chunk, k):
            patched = frozenset(combo)
            released = patch.release_closure(set(chunk) - patched)
            if not set(chunk) <= (released | patched):
                continue
            local = patch_cost() * len(patched) + len(released)
            out.append((local, patched, frozenset(released)))
    return out


def keep_beam(candidates, beam):
    """Cheapest candidates first, deterministic tie-breaks so runs reproduce."""
    ranked = sorted(
        candidates,
        key=lambda c: (c[0], len(c[2]), len(c[1]), sorted(c[1]), sorted(c[2])),
    )
    return ranked[: max(1, int(beam))]


def bounded_plan(patch, cap=None, beam=1, budget=20000):
    """Search only inside closure-overlap neighbourhoods; return the best plan.

    Returns a dict with the plan, its cost, and the work actually done, so the
    caller can compare planner effort against the oracle's `2**|errors|`.

    `beam` keeps that many candidates per chunk, so the combination phase is
    `prod(|candidates per chunk|)`, which is *not* bounded: on 24 independent
    chunks a beam of 2 already asks for 2**24 combinations. When that exceeds
    `budget` the planner falls back to each chunk's local best and records that
    it did, rather than silently spending unbounded work.

    A state outside the supported vocabulary is refused here, not by the
    experiment driver: refusing is part of what this planner is being tested on.
    """
    if patch.unsupported:
        return {"plan": None, "refused": patch.unsupported, "work": {}}
    groups = neighbourhoods(patch)
    chunks = [c for g in groups for c in split_chunks(g, cap)]
    per_chunk = [keep_beam(chunk_candidates(patch, c), beam) for c in chunks]
    required = 1
    for choices in per_chunk:
        required *= len(choices)
    budget_applied = required > budget
    if budget_applied:
        per_chunk = [keep_beam(chunk_candidates(patch, c), 1) for c in chunks]
    subsets = sum(1 << len(c) for c in chunks)

    best = None
    combos = 0
    for combo in itertools.product(*per_chunk):
        combos += 1
        patched = set()
        released = set()
        for _, p_i, r_i in combo:
            patched |= p_i
            released |= r_i
        closed = patch.release_closure(released)
        # Separability: the union costs exactly what the chunks charged, i.e.
        # no two chunks shared a released loop. False means the per-chunk costs
        # over-count and the combination search was necessary.
        separable = len(closed) == sum(len(r) for _, _, r in combo)
        patched -= closed
        if not patch.errors <= (closed | patched):
            continue
        cost = patch_cost() * len(patched) + len(closed)
        key = (cost, len(patched), sorted(patched), sorted(closed))
        if best is None or key < best[0]:
            best = (key, frozenset(patched), frozenset(closed), separable)

    work = {
        "neighbourhoods": len(groups),
        "group_sizes": sorted(len(g) for g in groups),
        "chunks": len(chunks),
        "subsets_enumerated": subsets,
        "combinations_evaluated": combos,
        "combinations_required": required,
        "budget_applied": budget_applied,
        "oracle_subsets": 1 << len(patch.errors),
    }
    if best is None:
        return {"plan": None, "work": work}
    (cost, _, _, _), patched, released, separable = best
    work["separable"] = separable
    return {
        "cost": cost,
        "patched": patched,
        "released": released,
        "valid": patch.errors <= (set(patched) | set(released)),
        "checkable": patch.verify_sequence(patched, released),
        "work": work,
    }