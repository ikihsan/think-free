"""Adapter for CSV format with header ``id,prediction,answer``.

Uses ``csv.DictReader`` for generic loading (free). Adapter-specific lines:
extract the ``id`` field and produce the output rows dicts.
"""

import csv


def adapt_csv(filepath):
    """Adapter for CSV harness format with header ``id,prediction,answer``.

    Returns ``(key_rows, out_rows)`` where:

    - ``key_rows``: list of ``{"id": "..."}`` dicts, one per input row.
    - ``out_rows``: list of ``{"id": "...", "prediction": "...", "answer": "..."}`` dicts,
      one per input row.

    Adapter tax: 3 lines. ``csv.DictReader`` provides generic loading (read
    CSV with header row); the 3 adapter lines extract the ``id`` field and
    produce the output-row shape.
    """
    key_rows = []
    out_rows = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_id = row.get("id")
            if row_id is not None:
                key_rows.append({"id": str(row_id)})
                out_rows.append({
                    "id": str(row_id),
                    "prediction": row.get("prediction", ""),
                    "answer": row.get("answer", ""),
                })
    return key_rows, out_rows