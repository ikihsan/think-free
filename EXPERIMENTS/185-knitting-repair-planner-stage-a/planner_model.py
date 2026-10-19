"""Planner data model: operations and repair state (E185 arm A1/A2 shared)."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any, Deque
from collections import deque
from enum import Enum
import copy
import heapq
import time

from knitting_graph import (
    KnitGraph, Loop, LoopType, PullDirection, loop_id,
    detect_errors,
)

class OperationType(Enum):
    RELEASE = "release"
    REKNIT = "reknit"
    SECURE = "secure"


@dataclass
class Operation:
    op_type: OperationType
    loop_id: str
    # For REKNIT: the new loop properties
    new_loop_type: Optional[LoopType] = None
    new_pull_direction: Optional[PullDirection] = None
    # For SECURE: just marks as boundary
    cost: int = 1

    def __lt__(self, other):
        return self.cost < other.cost


@dataclass
class RepairState:
    graph: KnitGraph
    operations: List[Operation] = field(default_factory=list)
    live_yarn_positions: List[int] = field(default_factory=list)  # yarn_order positions where yarn is live

    def copy(self) -> 'RepairState':
        return RepairState(
            graph=self.graph.copy(),
            operations=self.operations.copy(),
            live_yarn_positions=self.live_yarn_positions.copy(),
        )

    def total_cost(self) -> int:
        return sum(op.cost for op in self.operations)

    def loops_released(self) -> int:
        return sum(1 for op in self.operations if op.op_type == OperationType.RELEASE)

    def loops_reknit(self) -> int:
        return sum(1 for op in self.operations if op.op_type == OperationType.REKNIT)

    def holders_placed(self) -> int:
        return sum(1 for op in self.operations if op.op_type == OperationType.SECURE)


