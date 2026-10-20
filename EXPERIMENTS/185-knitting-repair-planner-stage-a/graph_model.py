"""Knit graph model: loops, fabric types, stitch topology."""


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
