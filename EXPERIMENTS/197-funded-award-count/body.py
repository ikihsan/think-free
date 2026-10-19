#!/usr/bin/env python3
"""Read one block's rows straight from its capture on disk.

G6 and `recompute.py` both need rows rather than the min/max summary a panel
keeps, and both must read the bytes the panel read -- not refetch. Kept in one
file so the capture path is written once.
"""
import json
import os

import client

FIELDS = ["Award ID", "Award Amount", "Description",
          "generated_unique_award_id", "Awarding Agency"]


def read_block_rows(prefix, page, order):
    """Every row of the named block, or `[]` if the capture is unreadable.

    An unreadable capture returns an empty list on purpose: the callers report
    the emptiness, because an empty list that a ratio is computed over is
    indistinguishable from a cell with no awards in it.
    """
    path = os.path.join(client.RAW, "%s_p%d_%s.json" % (prefix, page, order))
    try:
        with open(path, "rb") as fh:
            parsed = json.loads(fh.read().decode("utf-8", "replace"))
    except Exception:
        return []
    rows = parsed.get("results") if isinstance(parsed, dict) else None
    return rows if isinstance(rows, list) else []


def capture_meta(prefix, page, order):
    """The recorded status and sha256 of one capture, or `None`."""
    path = os.path.join(client.RAW, "%s_p%d_%s.meta.json"
                        % (prefix, page, order))
    try:
        with open(path) as fh:
            return json.load(fh)["response"]
    except Exception:
        return None