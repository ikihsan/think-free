"""Error introduction and detection for knit graphs."""

from typing import Any, Dict, List
from graph_model import KnitGraph, Loop, LoopType, PullDirection, loop_id
from graph_fabrics import *  # noqa: F401,F403

def introduce_error(graph: KnitGraph, error_type: str, **params) -> KnitGraph:
    """Introduce a specific error into a copy of the graph."""
    g = graph.copy()

    if error_type == "dropped_stitch":
        row, col = params.get('row', 1), params.get('col', 1)
        lid = loop_id(row, col)
        if lid in g.loops:
            # Remove the loop - this simulates a dropped stitch
            # But first, update neighbors to mark the gap
            loop = g.loops[lid]
            for dir_name, neighbor_id in loop.neighbors.items():
                if neighbor_id and neighbor_id in g.loops:
                    neighbor = g.loops[neighbor_id]
                    # Find reverse direction
                    reverse_dir = {'left': 'right', 'right': 'left', 'above': 'below', 'below': 'above', 'cable_partner': 'cable_partner'}.get(dir_name)
                    if reverse_dir and neighbor.neighbors.get(reverse_dir) == lid:
                        neighbor.neighbors[reverse_dir] = None  # Mark as gap
            g.remove_loop(lid)

    elif error_type == "twisted_stitch":
        row, col = params.get('row', 1), params.get('col', 1)
        lid = loop_id(row, col)
        if lid in g.loops:
            # A twisted stitch has wrong pull direction
            loop = g.loops[lid]
            loop.pull_direction = PullDirection.BACK_TO_FRONT if loop.pull_direction == PullDirection.FRONT_TO_BACK else PullDirection.FRONT_TO_BACK

    elif error_type == "wrong_cable_crossing":
        row, col = params.get('row', 1), params.get('col', 1)
        lid = loop_id(row, col)
        if lid in g.loops:
            loop = g.loops[lid]
            # Make BOTH loops in the pair have the same (wrong) type
            partner_id = loop.neighbors.get('cable_partner')
            if partner_id and partner_id in g.loops:
                partner = g.loops[partner_id]
                # Force both to be CABLE_LEFT (wrong crossing)
                loop.loop_type = LoopType.CABLE_LEFT
                partner.loop_type = LoopType.CABLE_LEFT

    elif error_type == "extra_yarnover":
        row, col = params.get('row', 1), params.get('col', 1)
        lid = loop_id(row, col)
        if lid in g.loops:
            # Change to yarnover type
            loop = g.loops[lid]
            loop.loop_type = LoopType.YARNOVER
            loop.pull_direction = PullDirection.FRONT_TO_BACK  # yarnover is neutral

    elif error_type == "wrong_stitch_type":
        row, col = params.get('row', 1), params.get('col', 1)
        lid = loop_id(row, col)
        if lid in g.loops:
            loop = g.loops[lid]
            # Flip knit<->purl BUT keep the original pull direction (making it twisted)
            if loop.loop_type == LoopType.KNIT:
                loop.loop_type = LoopType.PURL
                # Keep FRONT_TO_BACK pull direction -> twisted purl
            elif loop.loop_type == LoopType.PURL:
                loop.loop_type = LoopType.KNIT
                # Keep BACK_TO_FRONT pull direction -> twisted knit

    elif error_type == "two_adjacent_dropped":
        row, col = params.get('row', 1), params.get('col', 1)
        for dc in [0, 1]:
            lid = loop_id(row, col + dc)
            if lid in g.loops:
                g.remove_loop(lid)

    elif error_type == "mis_crossed_cable_3":
        row, col = params.get('row', 1), params.get('col', 1)
        # 3-stitch cable: make the crossing wrong by making adjacent pairs match
        lid = loop_id(row, col)
        if lid in g.loops:
            loop = g.loops[lid]
            partner_id = loop.neighbors.get('cable_partner')
            if partner_id and partner_id in g.loops:
                partner = g.loops[partner_id]
                # Force both to be CABLE_LEFT (wrong crossing)
                loop.loop_type = LoopType.CABLE_LEFT
                partner.loop_type = LoopType.CABLE_LEFT

    elif error_type == "dropped_stitch_edge":
        row, col = params.get('row', 0), params.get('col', 0)
        lid = loop_id(row, col)
        if lid in g.loops:
            g.remove_loop(lid)

    return g


def detect_errors(graph: KnitGraph) -> List[Dict[str, Any]]:
    """Detect errors in a graph. Returns list of error descriptions."""
    errors = []

    # Check for missing loops (gaps in grid)
    rows = max((loop.row for loop in graph.loops.values()), default=0) + 1
    cols = max((loop.col for loop in graph.loops.values()), default=0) + 1

    for r in range(rows):
        for c in range(cols):
            lid = loop_id(r, c)
            if lid not in graph.loops:
                # Check if neighbors exist - if so, this is a dropped stitch
                has_neighbors = False
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    n_lid = loop_id(r + dr, c + dc)
                    if n_lid in graph.loops:
                        has_neighbors = True
                        break
                if has_neighbors:
                    errors.append({
                        'type': 'dropped_stitch',
                        'location': (r, c),
                        'loop_id': lid,
                    })

    # Check for twisted stitches (wrong pull direction for type)
    for loop in graph.loops.values():
        expected_pull = PullDirection.FRONT_TO_BACK if loop.loop_type in (LoopType.KNIT, LoopType.CABLE_LEFT, LoopType.CABLE_RIGHT, LoopType.YARNOVER, LoopType.INCREASE) else PullDirection.BACK_TO_FRONT
        if loop.loop_type == LoopType.DECREASE:
            expected_pull = PullDirection.FRONT_TO_BACK  # decreases are typically knit-wise
        if loop.pull_direction != expected_pull and loop.loop_type not in (LoopType.YARNOVER,):
            errors.append({
                'type': 'twisted_stitch',
                'location': (loop.row, loop.col),
                'loop_id': loop.id,
            })

    # Check for yarnover errors (extra loop that shouldn't be there)
    for loop in graph.loops.values():
        if loop.loop_type == LoopType.YARNOVER:
            errors.append({
                'type': 'extra_yarnover',
                'location': (loop.row, loop.col),
                'loop_id': loop.id,
            })

    # Check for wrong cable crossings
    for loop in graph.loops.values():
        if loop.loop_type in (LoopType.CABLE_LEFT, LoopType.CABLE_RIGHT):
            partner_id = loop.neighbors.get('cable_partner')
            if partner_id and partner_id in graph.loops:
                partner = graph.loops[partner_id]
                # CABLE_LEFT should pair with CABLE_RIGHT
                if loop.loop_type == partner.loop_type:
                    errors.append({
                        'type': 'wrong_cable_crossing',
                        'location': (loop.row, loop.col),
                        'loop_id': loop.id,
                    })

    return errors


# Fixture definitions
