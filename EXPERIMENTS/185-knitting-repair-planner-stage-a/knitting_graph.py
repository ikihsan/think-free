"""Knitting graph representation and operations for repair planning."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
import json
import copy


class LoopType(Enum):
    KNIT = "knit"
    PURL = "purl"
    CABLE_LEFT = "cable_left"      # cable crossing left over right
    CABLE_RIGHT = "cable_right"    # cable crossing right over left
    YARNOVER = "yarnover"
    INCREASE = "increase"          # kfb, m1, etc.
    DECREASE = "decrease"          # k2tog, ssk, etc.


class PullDirection(Enum):
    FRONT_TO_BACK = "front_to_back"   # knit
    BACK_TO_FRONT = "back_to_front"   # purl


@dataclass
class Loop:
    id: str
    row: int
    col: int
    loop_type: LoopType
    yarn_order: int
    pull_direction: PullDirection
    neighbors: Dict[str, Optional[str]] = field(default_factory=dict)  # left, right, above, below, cable_partner
    is_boundary: bool = False
    is_live: bool = False  # yarn is live (released, available for re-knitting)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "row": self.row,
            "col": self.col,
            "type": self.loop_type.value,
            "yarn_order": self.yarn_order,
            "pull_direction": self.pull_direction.value,
            "neighbors": self.neighbors,
            "is_boundary": self.is_boundary,
            "is_live": self.is_live,
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'Loop':
        return cls(
            id=d["id"],
            row=d["row"],
            col=d["col"],
            loop_type=LoopType(d["type"]),
            yarn_order=d["yarn_order"],
            pull_direction=PullDirection(d["pull_direction"]),
            neighbors=d.get("neighbors", {}),
            is_boundary=d.get("is_boundary", False),
            is_live=d.get("is_live", False),
        )


@dataclass
class KnitGraph:
    loops: Dict[str, Loop] = field(default_factory=dict)
    yarn_sequence: List[str] = field(default_factory=list)  # loop IDs in yarn order
    next_loop_id: int = 0

    def add_loop(self, loop: Loop) -> None:
        self.loops[loop.id] = loop
        # Maintain yarn_sequence sorted by yarn_order
        self.yarn_sequence = sorted(self.loops.keys(), key=lambda lid: self.loops[lid].yarn_order)
        self.next_loop_id = max(self.next_loop_id, int(loop.id.split('_')[-1]) + 1) if '_' in loop.id else self.next_loop_id + 1

    def remove_loop(self, loop_id: str) -> None:
        if loop_id in self.loops:
            del self.loops[loop_id]
            self.yarn_sequence = [lid for lid in self.yarn_sequence if lid != loop_id]

    def get_loop(self, loop_id: str) -> Optional[Loop]:
        return self.loops.get(loop_id)

    def set_boundary(self, loop_id: str, is_boundary: bool = True) -> None:
        if loop_id in self.loops:
            self.loops[loop_id].is_boundary = is_boundary

    def set_live(self, loop_id: str, is_live: bool = True) -> None:
        if loop_id in self.loops:
            self.loops[loop_id].is_live = is_live

    def neighbors_of(self, loop_id: str) -> Dict[str, Optional[str]]:
        return self.loops[loop_id].neighbors.copy() if loop_id in self.loops else {}

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate graph structure. Returns (is_valid, list_of_errors)."""
        errors = []

        # Check all referenced neighbors exist
        for loop_id, loop in self.loops.items():
            for dir_name, neighbor_id in loop.neighbors.items():
                if neighbor_id and neighbor_id not in self.loops:
                    errors.append(f"Loop {loop_id} references missing neighbor {neighbor_id} in direction {dir_name}")

        # Check yarn sequence consistency
        for i, loop_id in enumerate(self.yarn_sequence):
            if loop_id not in self.loops:
                errors.append(f"Yarn sequence references missing loop {loop_id}")
            elif self.loops[loop_id].yarn_order != i:
                errors.append(f"Loop {loop_id} yarn_order {self.loops[loop_id].yarn_order} != position {i}")

        # Check no duplicate yarn_orders
        orders = [loop.yarn_order for loop in self.loops.values()]
        if len(orders) != len(set(orders)):
            errors.append("Duplicate yarn_order values")

        # Check connectivity: every loop should have at least left/right or above/below
        for loop_id, loop in self.loops.items():
            has_horizontal = loop.neighbors.get('left') or loop.neighbors.get('right')
            has_vertical = loop.neighbors.get('above') or loop.neighbors.get('below')
            if not has_horizontal and not has_vertical and loop.loop_type not in (LoopType.YARNOVER, LoopType.INCREASE):
                errors.append(f"Loop {loop_id} is isolated (no neighbors)")

        return len(errors) == 0, errors

    def to_dict(self) -> dict:
        return {
            "loops": {lid: loop.to_dict() for lid, loop in self.loops.items()},
            "yarn_sequence": self.yarn_sequence,
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'KnitGraph':
        g = cls()
        for lid, loop_dict in d["loops"].items():
            g.add_loop(Loop.from_dict(loop_dict))
        g.yarn_sequence = d.get("yarn_sequence", [])
        return g

    def copy(self) -> 'KnitGraph':
        return copy.deepcopy(self)


def loop_id(row: int, col: int) -> str:
    return f"r{row}c{col}"


def create_stockinette_graph(rows: int, cols: int) -> KnitGraph:
    """Create a stockinette fabric: knit rows (odd), purl rows (even)."""
    g = KnitGraph()
    yarn_order = 0

    for r in range(rows):
        is_knit_row = (r % 2 == 0)  # 0-indexed: row 0, 2, 4... are knit
        for c in range(cols):
            lid = loop_id(r, c)
            loop_type = LoopType.KNIT if is_knit_row else LoopType.PURL
            pull_dir = PullDirection.FRONT_TO_BACK if is_knit_row else PullDirection.BACK_TO_FRONT

            loop = Loop(
                id=lid,
                row=r,
                col=c,
                loop_type=loop_type,
                yarn_order=yarn_order,
                pull_direction=pull_dir,
                neighbors={}
            )
            g.add_loop(loop)
            yarn_order += 1

    # Set up neighbor connections
    for r in range(rows):
        for c in range(cols):
            lid = loop_id(r, c)
            loop = g.loops[lid]
            # Horizontal neighbors (same row)
            if c > 0:
                loop.neighbors['left'] = loop_id(r, c-1)
            if c < cols - 1:
                loop.neighbors['right'] = loop_id(r, c+1)
            # Vertical neighbors (row above/below)
            if r > 0:
                loop.neighbors['above'] = loop_id(r-1, c)
            if r < rows - 1:
                loop.neighbors['below'] = loop_id(r+1, c)

    # Mark boundary loops (edges)
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                g.set_boundary(loop_id(r, c), True)

    return g


def create_rib_graph(rows: int, cols: int, rib_width: int = 1) -> KnitGraph:
    """Create a rib fabric: alternating knit/purl columns."""
    g = KnitGraph()
    yarn_order = 0

    for r in range(rows):
        for c in range(cols):
            lid = loop_id(r, c)
            # Rib pattern: groups of rib_width knit, rib_width purl
            group = (c // rib_width) % 2
            is_knit = (group == 0)
            loop_type = LoopType.KNIT if is_knit else LoopType.PURL
            pull_dir = PullDirection.FRONT_TO_BACK if is_knit else PullDirection.BACK_TO_FRONT

            loop = Loop(
                id=lid,
                row=r,
                col=c,
                loop_type=loop_type,
                yarn_order=yarn_order,
                pull_direction=pull_dir,
                neighbors={}
            )
            g.add_loop(loop)
            yarn_order += 1

    # Neighbor connections
    for r in range(rows):
        for c in range(cols):
            lid = loop_id(r, c)
            loop = g.loops[lid]
            if c > 0:
                loop.neighbors['left'] = loop_id(r, c-1)
            if c < cols - 1:
                loop.neighbors['right'] = loop_id(r, c+1)
            if r > 0:
                loop.neighbors['above'] = loop_id(r-1, c)
            if r < rows - 1:
                loop.neighbors['below'] = loop_id(r+1, c)

    # Boundaries
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                g.set_boundary(loop_id(r, c), True)

    return g


def create_cable_graph(rows: int, cols: int, cable_interval: int = 4) -> KnitGraph:
    """Create a fabric with cable crossings every cable_interval rows."""
    g = KnitGraph()
    yarn_order = 0

    for r in range(rows):
        for c in range(cols):
            lid = loop_id(r, c)
            # Default to stockinette
            is_knit_row = (r % 2 == 0)
            loop_type = LoopType.KNIT if is_knit_row else LoopType.PURL
            pull_dir = PullDirection.FRONT_TO_BACK if is_knit_row else PullDirection.BACK_TO_FRONT

            # Cable crossings on specific rows
            if r > 0 and r % cable_interval == 0 and c < cols - 1 and c % 2 == 0:
                # This row has cable crossings
                if is_knit_row:
                    loop_type = LoopType.CABLE_LEFT if c % 4 == 0 else LoopType.CABLE_RIGHT
                    # Cable loops are still knit-type pulls
                    pull_dir = PullDirection.FRONT_TO_BACK

            loop = Loop(
                id=lid,
                row=r,
                col=c,
                loop_type=loop_type,
                yarn_order=yarn_order,
                pull_direction=pull_dir,
                neighbors={}
            )
            g.add_loop(loop)
            yarn_order += 1

    # Neighbor connections
    for r in range(rows):
        for c in range(cols):
            lid = loop_id(r, c)
            loop = g.loops[lid]
            if c > 0:
                loop.neighbors['left'] = loop_id(r, c-1)
            if c < cols - 1:
                loop.neighbors['right'] = loop_id(r, c+1)
            if r > 0:
                loop.neighbors['above'] = loop_id(r-1, c)
            if r < rows - 1:
                loop.neighbors['below'] = loop_id(r+1, c)
            # Cable partners
            if loop.loop_type in (LoopType.CABLE_LEFT, LoopType.CABLE_RIGHT):
                if c < cols - 1:
                    loop.neighbors['cable_partner'] = loop_id(r, c+1)

    # Boundaries
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                g.set_boundary(loop_id(r, c), True)

    return g


def create_garter_graph(rows: int, cols: int) -> KnitGraph:
    """Create garter stitch: knit every row."""
    g = KnitGraph()
    yarn_order = 0

    for r in range(rows):
        for c in range(cols):
            lid = loop_id(r, c)
            loop = Loop(
                id=lid,
                row=r,
                col=c,
                loop_type=LoopType.KNIT,
                yarn_order=yarn_order,
                pull_direction=PullDirection.FRONT_TO_BACK,
                neighbors={}
            )
            g.add_loop(loop)
            yarn_order += 1

    # Neighbor connections
    for r in range(rows):
        for c in range(cols):
            lid = loop_id(r, c)
            loop = g.loops[lid]
            if c > 0:
                loop.neighbors['left'] = loop_id(r, c-1)
            if c < cols - 1:
                loop.neighbors['right'] = loop_id(r, c+1)
            if r > 0:
                loop.neighbors['above'] = loop_id(r-1, c)
            if r < rows - 1:
                loop.neighbors['below'] = loop_id(r+1, c)

    # Boundaries
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                g.set_boundary(loop_id(r, c), True)

    return g


def create_seed_stitch_graph(rows: int, cols: int) -> KnitGraph:
    """Create seed stitch: alternating knit/purl every stitch, every row."""
    g = KnitGraph()
    yarn_order = 0

    for r in range(rows):
        for c in range(cols):
            lid = loop_id(r, c)
            is_knit = ((r + c) % 2 == 0)
            loop_type = LoopType.KNIT if is_knit else LoopType.PURL
            pull_dir = PullDirection.FRONT_TO_BACK if is_knit else PullDirection.BACK_TO_FRONT

            loop = Loop(
                id=lid,
                row=r,
                col=c,
                loop_type=loop_type,
                yarn_order=yarn_order,
                pull_direction=pull_dir,
                neighbors={}
            )
            g.add_loop(loop)
            yarn_order += 1

    # Neighbor connections
    for r in range(rows):
        for c in range(cols):
            lid = loop_id(r, c)
            loop = g.loops[lid]
            if c > 0:
                loop.neighbors['left'] = loop_id(r, c-1)
            if c < cols - 1:
                loop.neighbors['right'] = loop_id(r, c+1)
            if r > 0:
                loop.neighbors['above'] = loop_id(r-1, c)
            if r < rows - 1:
                loop.neighbors['below'] = loop_id(r+1, c)

    # Boundaries
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                g.set_boundary(loop_id(r, c), True)

    return g


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
FIXTURES = [
    {
        'name': 'F1_stockinette_dropped',
        'description': '4x4 stockinette with one dropped stitch at (1,1)',
        'factory': lambda: introduce_error(create_stockinette_graph(4, 4), "dropped_stitch", row=1, col=1),
        'correct_factory': lambda: create_stockinette_graph(4, 4),
        'expected_error': 'dropped_stitch',
    },
    {
        'name': 'F2_rib_twisted',
        'description': '4x4 1x1 rib with one twisted stitch at (1,2)',
        'factory': lambda: introduce_error(create_rib_graph(4, 4, 1), "twisted_stitch", row=1, col=2),
        'correct_factory': lambda: create_rib_graph(4, 4, 1),
        'expected_error': 'twisted_stitch',
    },
    {
        'name': 'F3_cable_wrong_cross',
        'description': '7x7 cable fabric with wrong crossing at row 4 (not at boundary)',
        'factory': lambda: introduce_error(create_cable_graph(7, 7, 4), "wrong_cable_crossing", row=4, col=2),
        'correct_factory': lambda: create_cable_graph(7, 7, 4),
        'expected_error': 'wrong_cable_crossing',
    },
    {
        'name': 'F4_stockinette_yarnover',
        'description': '5x5 stockinette with unresolved yarnover at (2,2)',
        'factory': lambda: introduce_error(create_stockinette_graph(5, 5), "extra_yarnover", row=2, col=2),
        'correct_factory': lambda: create_stockinette_graph(5, 5),
        'expected_error': 'extra_yarnover',
    },
    {
        'name': 'F5_stockinette_wrong_type',
        'description': '5x5 stockinette with one wrong stitch type at (2,2) - purl in knit row',
        'factory': lambda: introduce_error(create_stockinette_graph(5, 5), "wrong_stitch_type", row=2, col=2),
        'correct_factory': lambda: create_stockinette_graph(5, 5),
        'expected_error': 'twisted_stitch',
    },
    {
        'name': 'F6_stockinette_two_dropped',
        'description': '4x4 stockinette with two adjacent dropped stitches at (1,1) and (1,2)',
        'factory': lambda: introduce_error(create_stockinette_graph(4, 4), "two_adjacent_dropped", row=1, col=1),
        'correct_factory': lambda: create_stockinette_graph(4, 4),
        'expected_error': 'dropped_stitch',
    },
    {
        'name': 'F7_cable_mis_cross_3',
        'description': '7x7 cable fabric with mis-crossed cable at row 4 (not at boundary)',
        'factory': lambda: introduce_error(create_cable_graph(7, 7, 4), "mis_crossed_cable_3", row=4, col=2),
        'correct_factory': lambda: create_cable_graph(7, 7, 4),
        'expected_error': 'wrong_cable_crossing',
    },
    {
        'name': 'F8_garter_dropped_edge',
        'description': '4x4 garter stitch with dropped stitch at edge (0,0)',
        'factory': lambda: introduce_error(create_garter_graph(4, 4), "dropped_stitch_edge", row=0, col=0),
        'correct_factory': lambda: create_garter_graph(4, 4),
        'expected_error': 'dropped_stitch',
    },
]


if __name__ == "__main__":
    # Test fixture creation
    for fix in FIXTURES:
        g = fix['factory']()
        valid, errors = g.validate()
        detected = detect_errors(g)
        print(f"{fix['name']}: valid={valid}, errors={errors}, detected={len(detected)}")
        for d in detected:
            print(f"  - {d}")