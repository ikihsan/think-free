"""Adapter for single JSONL format: each line is {"id": "...", "prediction": "...", "answer": "..."}.

Reads a JSONL file and produces ``key_rows`` and ``out_rows`` for
``preflight.concordance``. Generic loading is free (read JSON, extract fields);
adapter-specific lines are the ``id`` extraction and row-type normalisation.
"""

import json


def adapt_jsonl(filepath):
    """Adapter for single JSONL harness format.

    Returns ``(key_rows, out_rows)`` where:

    - ``key_rows``: list of ``{"id": "..."}`` dicts, one per input row.
    - ``out_rows``: list of ``{"id": "...", "prediction": "...", "answer": "..."}`` dicts,
      one per input row.

    Adapter tax: 4 lines. Generic loading (read JSON array, read JSON-Lines,
    read CSV with header) is free; nested reshaping, custom serialisation and
    schema mapping are counted.
    """
    key_rows = []
    out_rows = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            row_id = row.get("id")
            if row_id is not None:
                key_rows.append({"id": str(row_id)})
                out_rows.append({
                    "id": str(row_id),
                    "prediction": row.get("prediction", ""),
                    "answer": row.get("answer", ""),
                })
    return key_rows, out_rows