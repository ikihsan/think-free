#!/usr/bin/env python3
"""
Shared corpus loader for E072.

Why this file exists: E066's population came from one dataset with one schema.
E072's population is 47 real bank exports in ~20 different layouts, and two
real defects showed up while reading them:

  1. `amkchari/ExpenseManager` is `M/D/Y`. A naive `strptime` list tries
     `%d/%m/%Y` first and silently relabels 5 July as 7 May, which stretched a
     5-year account into a 2030-day span and would have counted one date twice.
  2. `mgmayaguari/...` is `YYYY/MM/DD`, which was not in the pattern list at
     all, so the date column was never found and the rows fell through to a
     different column.

So date formats are decided PER FILE, by which candidate parses the largest
fraction of that file's non-empty values, and a value that two candidates
would accept differently (a day ≤ 12) is treated as **ambiguous** and
excluded rather than guessed. That exclusion is reported, never silently
absorbed: it is the shape of D082, and the count is in results.json.

The loader never touches the merchant string. Adapters map columns only.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from datetime import date, datetime

CANDIDATE_FORMATS = ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y", "%m/%d/%y", "%d/%m/%y", "%m-%d-%Y"]
DATE_TOKEN = re.compile(r"(\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4})")
MERCHANT_HINT = ("original description", "description", "merchant", "payee",
                 "narrative", "beschreibung", "name")
AMOUNT_HINT = ("amount", "withdrawal", "outflow", "betrag", "sum", "debit")
DATE_HINT = ("transaction date", "posted date", "posting date", "date", "posted_date",
             "transaction_date", "datum")


def _detect_date_format(values):
    """Return (fmt, n_parsed, n_ambiguous, n_unparsed) for one file."""
    toks = []
    for v in values:
        if v:
            m = DATE_TOKEN.search(v)
            if m:
                toks.append(m.group(1))
    best = None
    for fmt in CANDIDATE_FORMATS:
        ok = amb = 0
        for t in toks:
            try:
                d = datetime.strptime(t, fmt).date()
            except ValueError:
                continue
            # A d/m/y and an m/d/y reading both exist whenever day <= 12.
            swap = {"%m/%d/%Y": "%d/%m/%Y", "%d/%m/%Y": "%m/%d/%Y",
                    "%m-%d-%Y": "%d-%m-%Y", "%d-%m-%Y": "%m-%d-%Y"}.get(fmt)
            if swap:
                try:
                    d2 = datetime.strptime(t, swap).date()
                    if d2 != d:
                        amb += 1
                        continue
                except ValueError:
                    pass
            ok += 1
        if best is None or ok > best[1]:
            best = (fmt, ok, amb)
    if best is None or best[1] == 0:
        return None, 0, len(toks), len(toks)
    return best[0], best[1], best[2], len(toks) - best[1]


# Headers that name a RAW bank descriptor rather than a tool's cleaned payee.
# A budget app writes "Payee"; a bank writes "Description", and when the app
# re-exports a statement it keeps BOTH columns side by side, app first.
RAW_DESCRIPTOR_HEADER = re.compile(r"description|narrative|beschreibung|memo")


def _pick_merchant_column(low, header):
    """
    Choose the merchant column. Preference order, and why:

      1. a header naming an ORIGINAL/RAW description -- "Original Description",
         which Mint, Monarch and Empower emit specifically to preserve the
         bank's string alongside their own cleaned `description`.
      2. a header naming a description/memo at all.
      3. a header naming merchant/payee/name.

    This order exists because of a defect found on 2026-10-09. `a04`
    (`jorb1/python_practice/coding-personal/jared-budget.csv`) is a budget
    app's export that CONCATENATES two tables: an Actual-style block
    (`Date,Payee,Outflow,Inflow`) and, to its right, the original Chase block
    (`Transaction Date,Post Date,Description,Amount`). A naive
    first-match-wins scan took `Payee`, column 1 -- the app's already-cleaned
    merchant name. The corpus then contained 49 rows of `Spotify` and 24 of
    `Chewy`, strings that no bank ever emits, and the merchant axis under test
    was measured on the cleanest possible input.

    It is worth stating the cost of getting this right in the wrong direction:
    the same file also gave the highest-looking under-grouping numbers in the
    first probe run, so the defect inflated the very finding it invalidated.
    """
    for pattern in (r"original description", RAW_DESCRIPTOR_HEADER):
        for i, h in enumerate(low):
            if re.search(pattern, h):
                return i
    for h in low:
        if any(x in h for x in MERCHANT_HINT):
            return low.index(h)
    return None


def ambiguous_merchant_columns(header):
    """
    Every column whose name could be the merchant column. A file with more than
    one of them, and no "original" one among them, is not a bank export of a
    single account and is excluded rather than guessed at.

    `a04` is the case that forced this. It is a budget app's export that
    concatenates two tables side by side -- an Actual-style block whose second
    column is `Payee`, and, eight columns to the right, the original Chase
    block whose fifth column is ALSO `Payee`. No header rule distinguishes
    them; only the file's provenance does, and this stage does not read
    provenance. First-match-wins quietly took the app's cleaned column, so the
    corpus held 49 rows of `Spotify` and 24 of `Chewy` -- strings no bank emits
    -- and the merchant axis under test was measured on already-cleaned input.
    That file also produced the best-looking under-grouping numbers in the
    first probe run, so the defect inflated the finding it invalidated.
    """
    low = [h.strip().lower() for h in header]
    cands = [i for i, h in enumerate(low) if any(x in h for x in MERCHANT_HINT)]
    if len(cands) <= 1:
        return []
    if any("original" in low[i] for i in cands):
        return []
    return cands


def _find_columns(header):
    low = [h.strip().lower() for h in header]
    mi = _pick_merchant_column(low, header)
    ai = di = None
    for i, h in enumerate(low):
        if ai is None and any(x in h for x in AMOUNT_HINT):
            ai = i
        if di is None and h in DATE_HINT:
            di = i
    return mi, ai, di


def _parse_amount(text):
    t = re.sub(r"[$\u20ac\u00a3£,\s]", "", text or "").strip()
    neg = t.startswith("(") and t.endswith(")")
    if neg:
        t = "-" + t[1:-1]
    if not re.fullmatch(r"-?\d+(\.\d+)?", t):
        return None
    return float(t)


def load_account(entry):
    """
    entry: {"file": path, ...}. Returns
      {"account", "rows": [{"date","amount","merchant","raw"}], "stats": {...}}
    """
    path = entry.get("file") or entry["local"]
    raw = open(path, "rb").read()
    text = raw.decode("utf-8", "ignore")
    dialect = csv.Sniffer().sniff(text[:5000], delimiters=",;\t|")
    table = list(csv.reader(io.StringIO(text), dialect))
    header = [c.strip().strip('"\ufeff') for c in table[0]]
    body = table[1:]
    ncols = max(len(r) for r in body)

    amb = ambiguous_merchant_columns(header)
    if amb:
        return {"account": entry.get("account_id"), "rows": [],
                "stats": {"error": "ambiguous merchant columns %s" % amb, "header": header}}

    mi, ai, di = _find_columns(header)
    if di is None:
        for i in range(ncols):
            fmt, ok, _, _ = _detect_date_format([r[i] for r in body[:400] if i < len(r)])
            if fmt and ok > 0.6 * min(len(body), 400):
                di = i
                break
    if mi is None or ai is None or di is None or len({mi, ai, di}) != 3:
        return {"account": entry.get("repo"), "rows": [], "stats": {"error": "column mapping failed"}}

    fmt, ok, ambiguous, unparsed = _detect_date_format([r[di] for r in body if di < len(r)])
    if fmt is None:
        return {"account": entry.get("repo"), "rows": [], "stats": {"error": "no date format"}}

    rows = []
    for r in body:
        if len(r) <= max(di, ai, mi):
            continue
        m = DATE_TOKEN.search(r[di] or "")
        if not m:
            continue
        try:
            d = datetime.strptime(m.group(1), fmt).date()
        except ValueError:
            continue
        amount = _parse_amount(r[ai])
        desc = (r[mi] or "").strip()
        if amount is None or not desc:
            continue
        rows.append({"date": d, "amount": amount, "merchant": desc, "raw": desc})
    return {"account": entry.get("account_id") or entry.get("repo") or path,
            "rows": rows,
            "stats": {"date_format": fmt, "header": header,
                      "cols": {"date": header[di], "amount": header[ai], "merchant": header[mi]},
                      "rows_parsed": len(rows), "rows_in_file": len(body),
                      "date_tokens_ambiguous": ambiguous,
                      "date_tokens_unparsed": unparsed,
                      "sha256": hashlib.sha256(raw).hexdigest()}}