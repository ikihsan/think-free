#!/usr/bin/env python3
"""E197 instrument: an exact count of a cell's awards relative to an amount.

`spending_by_award` sorted ascending is monotone, so `n_below(t)` is found by
reading ascending 100-row blocks until the first block containing a value at or
above `t`, and counting the rows below `t` in every block read. The count is
exact rather than interpolated because every row counted was read, and each
block's raw body is on disk with its sha256 before it is parsed.

`probe.py` finding 2 is why this is the instrument rather than a filter:
USAspending's `amount_requirement` is ignored silently by
`spending_by_award_count/` and refused loudly by `spending_by_award/`, so no
amount filter exists to use and the order statistic is the whole method.

`n_at_or_above` reads the same question from the descending end. Panel B runs it
as the independent arm, so a bisection off by one page has something to
contradict it.

**Two measured facts about the endpoint, both recorded because using them
wrongly produces a confident wrong answer:**

* `page_metadata.hasNext` turns **False at row 10,000** and stays False for
  every deeper page, whatever the cell's real size -- DA01 has 27,424 awards
  and 275 pages, and `hasNext` is False from page 100 on. It is a constant, not
  a statement about the cell, so it is **not** used here. "The cell ended" is
  read from a short block (`rows < 100`) or an empty one (`rows == 0`).
* The deepest readable page is 500 (E196 F143); page 500 of a smaller cell
  returns `200` with **zero rows** rather than `422`, and page 501+ returns
  `422`. Both count as "past the end" and neither counts as a value.
"""
import json
import math
import os

import client
import thresholds as TH

FIELDS = ["Award ID", "Award Amount", "Description",
          "generated_unique_award_id", "Awarding Agency"]


def page_of(rank):
    """Page index whose 100-row block contains 1-based `rank`."""
    return max(1, int(math.ceil(rank / 100.0)))


def read_block(filters, page, order, prefix):
    """One 100-row block, summarised; its raw body is captured by `client`.

    `fields` is required by the endpoint -- omitting it returns 422
    `Missing value: 'fields' is a required field`, which in the scan reads
    exactly like a depth ceiling.
    """
    payload = {"filters": filters, "subawards": False, "sort": "Award Amount",
               "order": order, "page": page, "limit": 100, "fields": FIELDS}
    st, parsed, meta = client.call("spending_by_award/",
                                   payload, "%s_p%d_%s" % (prefix, page, order))
    results = parsed.get("results") if isinstance(parsed, dict) else None
    rows = results if isinstance(results, list) else []
    amts = [r["Award Amount"] for r in rows
            if isinstance(r.get("Award Amount"), (int, float))]
    return {"page": page, "order": order, "status": st, "rows": len(amts),
            "min": min(amts) if amts else None, "max": max(amts) if amts else None,
            "unused_filters": client.unused_filter_messages(parsed), "meta": meta}


def _rows_matching(prefix, page, order, predicate):
    """Count rows in one block satisfying `predicate(amount)`, from its capture.

    A summary keeps min/max because most gates need only those, but an exact
    count needs every row, so the body is re-read from disk rather than
    re-fetched. A capture that cannot be read returns None and the caller
    reports it, because a quiet 0 is indistinguishable from a real count.
    """
    path = os.path.join(client.RAW, "%s_p%d_%s.json" % (prefix, page, order))
    try:
        with open(path, "rb") as fh:
            parsed = json.loads(fh.read().decode("utf-8", "replace"))
    except Exception:
        return None
    rows = parsed.get("results") if isinstance(parsed, dict) else None
    if not isinstance(rows, list):
        return None
    return sum(1 for r in rows
               if isinstance(r.get("Award Amount"), (int, float))
               and predicate(r["Award Amount"]))


def _last_page(total):
    """Highest page index that can hold a row, from the cell's own count."""
    return page_of(total) if total else TH.MAX_PAGE


def _search(filters, prefix, order, total, t, side):
    """First page whose block reaches the threshold, by binary search.

    `side` is `"max"` (ascending arm: the first block whose **max** is at or
    above `t`) or `"min"` (descending arm: the first block whose **min** falls
    below `t`). Either way the predicate is false for every page at or below
    the search's lower bound, and that is checked on each page rather than
    assumed.

    A geometric scan was tried first and is the wrong shape here: it returns the
    first *probe* that reaches, leaving the pages between two probes unexamined.
    On `DA01` it placed the descending turning page at 275 when the true page is
    273 -- a wrong count rather than a noisy one. Searching
    [1, min(500, pages the cell can fill)] is at most nine requests and has no
    such gap.

    Returns (read_pages, turn_page, word) with `word` one of `reached`,
    `whole_cell_below` or `censored`.
    """
    read = {}

    def blk(p):
        if p not in read:
            read[p] = read_block(filters, p, order, prefix)
        return read[p]

    def reached(b):
        if not b["rows"]:
            return False
        return (b[side] >= t) if side == "max" else (b[side] < t)

    top = min(TH.MAX_PAGE, _last_page(total))
    lo, hi = 0, top
    while hi - lo > 1:
        mid = (lo + hi) // 2
        b = blk(mid)
        if b["status"] != 200 or b["rows"] == 0:
            hi = mid          # the cell ends before `mid`; search (lo, mid)
        elif reached(b):
            hi = mid
        elif b["rows"] < 100:
            return read, None, "whole_cell_below"
        else:
            lo = mid
    b = blk(hi)
    if reached(b):
        return read, hi, "reached"
    if b["rows"] < 100:
        return read, None, "whole_cell_below"
    return read, None, "censored"

def _count(prefix, order, turn_page, predicate, total, t):
    """`100 * (turn_page - 1)` plus the rows of the turning block that match.

    Every page before the turning one is **entirely** on one side of `t`, by
    monotonicity of the sort and because it did not reach the threshold, so its
    contribution is exactly 100 -- no row-level read and no skipped page. Only
    the turning block must be read row by row. That is what makes the count
    exact *and* cheap: an earlier version summed whichever blocks the geometric
    scan happened to probe, which omits every page the scan skipped and
    understates the count.
    """
    n_prefix = 100 * (turn_page - 1) if turn_page else 0
    rowwise = _rows_matching(prefix, turn_page, order, predicate) \
        if turn_page else None
    if rowwise is None:
        return {"t": t, "order": order, "turn_page": turn_page, "n": None,
                "lower_bound": n_prefix, "censored": True,
                "reason": "the turning block could not be read from its capture"}
    n = n_prefix + rowwise
    out = {"t": t, "order": order, "turn_page": turn_page, "n": n,
           "lower_bound": n, "censored": False,
           "reason": "exact count over the turning block",
           "rows_in_turn_block": rowwise,
           "blocks_before_turn": turn_page - 1 if turn_page else 0}
    if total is not None and n > total:
        out.update(n=None, censored=True,
                   reason="count exceeds the endpoint total; suspect")
    return out


def _censored(t, order, read, bound_pages, reason):
    return {"t": t, "order": order, "turn_page": None, "n": None,
            "lower_bound": 100 * bound_pages, "censored": True,
            "reason": reason, "blocks_before_turn": bound_pages}


def _unread(read):
    """Every 'filter not used' message seen in the blocks this call read.

    E197's control C4 turns on this. `spending_by_award_count/` ignores an
    amount filter silently, so a filter that stops being honoured here would
    return a confident, well-formed answer about the wrong population, and the
    only thing standing between that and a result is this check.
    """
    msgs = []
    for b in read.values():
        msgs.extend(b.get("unused_filters") or [])
    return sorted(set(msgs))


def n_below(filters, total, t, prefix):
    """Exact count of awards with `Award Amount` < t. Ascending arm."""
    read, turn, word = _search(filters, prefix, "asc", total, t, "max")
    keep = lambda a: a < t                                          # noqa: E731
    out = None
    if word == "reached":
        out = _count(prefix, "asc", turn, keep, total, t)
    elif word == "whole_cell_below":
        out = {"t": t, "order": "asc", "turn_page": None, "n": total,
               "lower_bound": total, "censored": False,
               "reason": "the whole cell was read and every award is below the "
                         "threshold", "blocks_before_turn": None}
    else:
        lo = max([p for p in read if read[p]["status"] == 200
                  and read[p]["rows"] == 100 and read[p]["max"] < t], default=0)
        out = _censored(t, "asc", read, lo,
                        "the turning page lies past the 500-page ceiling, so "
                        "this is a lower bound on the count")
    out["unused_filters"] = _unread(read)
    return out


def n_at_or_above(filters, total, t, prefix):
    """Exact count of awards with `Award Amount` >= t. Descending arm.

    The independent instrument for panel B: it starts at the largest award and
    walks down, so a page-level defect in the ascending arm has to show up as a
    disagreement rather than as a second copy of the same mistake.
    """
    read, turn, word = _search(filters, prefix, "desc", total, t, "min")
    keep = lambda a: a >= t                                         # noqa: E731
    if word == "reached":
        out = _count(prefix, "desc", turn, keep, total, t)
    elif word == "whole_cell_below":
        out = {"t": t, "order": "desc", "turn_page": None, "n": total,
               "lower_bound": total, "censored": False,
               "reason": "the whole cell was read and every award is at or "
                         "above the threshold", "blocks_before_turn": None}
    else:
        lo = max([p for p in read if read[p]["status"] == 200
                  and read[p]["rows"] == 100 and read[p]["min"] >= t],
                 default=0)
        out = _censored(t, "desc", read, lo,
                        "the turning page lies past the 500-page ceiling, so "
                        "this is a lower bound on the count")
    out["unused_filters"] = _unread(read)
    return out
