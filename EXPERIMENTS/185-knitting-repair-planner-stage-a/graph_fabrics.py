"""Fabric constructors: stockinette, rib, cable, garter, seed stitch."""

from typing import Any, List
from graph_model import KnitGraph, Loop, LoopType, PullDirection, loop_id

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


