"""C1 -- concordance: do the key's identifiers and the output's identifiers
name the same entities?

The defect this catches (F121) is a join that matches nothing. A scorer that
does `key[rec["account_id"]]` against answers keyed `"R001"` finds no row,
falls through to its empty case, and prints 0.0000 for a reader that answered
every item correctly. Nothing raises. The number is indistinguishable from a
reader that failed.

The check reports the match rate of every candidate pairing the two files share
-- each shared field alone, then every ordered concatenation of two -- and
fires when none of them reaches a nonzero rate while both sides are non-empty.
It does not assert which pairing the harness intends. A harness whose key uses
a synthetic id has no shared field with its outputs at all, and the report
should make that visible rather than pick a winner for it.
"""

from .stats import fmt_interval


def _norm(value):
    """Compare identifiers as they would be compared by a dict lookup.

    Type matters: 1 and "1" are different keys. A harness that coerces
    (`"%s%03d" % (arm, account_id)`) is visible as a composed pairing.
    """
    return value if isinstance(value, str) else str(value)


def _candidates(key_rows, out_rows):
    """Shared field names, and composed pairs, in a stable order."""
    key_fields = []
    for row in key_rows:
        for field in row:
            if field not in key_fields:
                key_fields.append(field)
    out_fields = []
    for row in out_rows:
        for field in row:
            if field not in out_fields:
                out_fields.append(field)
    shared = [f for f in key_fields if f in out_fields]
    pairs = []
    for i, a in enumerate(shared):
        for b in shared[i + 1:]:
            pairs.append([a, b])
    return shared, pairs


def _types(rows, field):
    return sorted(set(type(r.get(field)).__name__ for r in rows))


def type_conflicts(key_rows, out_rows):
    """Shared field names that hold different types on the two sides.

    `1` and `"1"` are different dict keys. A join on them matches nothing and
    raises nothing, which is why F121's scorer reported a recall of 0.0000 for
    a reader that answered every item. Naming the conflict is more useful than
    reporting only the zero.
    """
    key_fields = []
    for row in key_rows:
        for field in row:
            if field not in key_fields:
                key_fields.append(field)
    out_fields = []
    for row in out_rows:
        for field in row:
            if field not in out_fields:
                out_fields.append(field)
    out = []
    for field in [f for f in key_fields if f in out_fields]:
        left, right = _types(key_rows, field), _types(out_rows, field)
        if left != right:
            out.append({"field": field, "key_types": left, "output_types": right})
    return out


def _match_rate(key_rows, out_rows, fields):
    def key_of(row):
        return tuple(_norm(row.get(f, "")) for f in fields)

    keys = set(key_of(r) for r in key_rows)
    if not keys:
        return 0, 0
    hits = 0
    for row in out_rows:
        if key_of(row) in keys:
            hits += 1
    return hits, len(out_rows)


def concordance(key_rows, out_rows, min_match=1):
    """Measure the join space between a key file and an output file.

    `min_match` is the smallest number of matched output rows that counts as
    "the join works". Zero is the verdict that matters: a join matching nothing
    over a non-empty output file is not a low score, it is a harness that never
    looked at the answers.
    """
    shared, pairs = _candidates(key_rows, out_rows)
    conflicts = type_conflicts(key_rows, out_rows)
    out_rows_n = len(out_rows)
    key_rows_n = len(key_rows)
    table = []
    degenerate = []
    for fields in [[f] for f in shared] + pairs:
        hits, total = _match_rate(key_rows, out_rows, fields)
        distinct = len(set(tuple(_norm(r.get(f, "")) for f in fields) for r in key_rows))
        row = {
            "pairing": "+".join(fields),
            "matched": hits,
            "outputs": total,
            "rate": round(float(hits) / total, 4) if total else 0.0,
        }
        # A field that is constant across the key cannot distinguish one output
        # row from another, so a high match rate on it says nothing about the
        # join. Report it separately rather than letting it look like a clean run.
        if distinct < 2:
            row["degenerate"] = True
            degenerate.append(row["pairing"])
            continue
        table.append(row)
    best = max([r["rate"] for r in table]) if table else 0.0
    if degenerate and not table:
        # Every candidate pairing was constant on the key side: the join may
        # well work, and this check cannot see it.
        return {
            "check": "C1_concordance",
            "verdict": "NO_DISCRIMINATING_PAIRING",
            "reason": ("the only field names the two files share (%s) are constant "
                       "across the key, so no pairing here can distinguish a matched "
                       "output row from an unmatched one" % ", ".join(degenerate)),
            "key_rows": key_rows_n,
            "output_rows": out_rows_n,
            "best_rate": 0.0,
            "summary": "no discriminating pairing",
            "type_conflicts": conflicts,
            "pairings": table,
            "degenerate_pairings": degenerate,
        }
    verdict = "OK"
    reason = ""
    if key_rows_n and out_rows_n and best == 0.0:
        verdict = "SILENT_NO_MATCH"
        if conflicts:
            reason = ("%d key rows and %d output rows, and no pairing shared by the "
                      "two files matches a single output row. The shared field(s) %s "
                      "hold different types on each side (%s), so the join compares "
                      "%s and matches nothing: the scorer never reads the answers."
                      % (key_rows_n, out_rows_n,
                         ", ".join(c["field"] for c in conflicts),
                         "; ".join("%s key=%s output=%s" % (c["field"], c["key_types"], c["output_types"]) for c in conflicts),
                         _examples(key_rows, out_rows, conflicts)))
        else:
            reason = ("%d key rows and %d output rows, and none of the %d candidate "
                      "pairings shared by the two files matches a single output row: "
                      "the join sees nothing." % (key_rows_n, out_rows_n, len(table)))
    elif key_rows_n and out_rows_n and best < 1.0:
        verdict = "PARTIAL_MATCH"
        reason = "best pairing matches %d of %d output rows" % (
            int(round(best * out_rows_n)), out_rows_n)
    if not shared:
        reason = ("the key file and the output file share no field name, so "
                  "the join is by something this check cannot see")
        verdict = "SILENT_NO_MATCH" if key_rows_n and out_rows_n else verdict
    return {
        "check": "C1_concordance",
        "verdict": verdict,
        "reason": reason,
        "key_rows": key_rows_n,
        "output_rows": out_rows_n,
        "best_rate": round(best, 4),
        "summary": fmt_interval(int(round(best * out_rows_n)), out_rows_n) if out_rows_n else "no output rows",
        "type_conflicts": conflicts,
        "pairings": table,
        "degenerate_pairings": degenerate,
    }


def _examples(key_rows, out_rows, conflicts, limit=3):
    """The offending values, verbatim, so the conflict is not merely asserted."""
    field = conflicts[0]["field"]
    left = [r.get(field) for r in key_rows[:limit]]
    right = [r.get(field) for r in out_rows[:limit]]
    return "key %r against output %r" % (left, right)