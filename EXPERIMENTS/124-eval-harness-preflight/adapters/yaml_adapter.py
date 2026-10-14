"""Adapter for YAML harness format with keys ``id``, ``prediction``, ``answer``.

Uses ``yaml.SafeLoader`` for generic loading (free). Adapter-specific lines:
extract the ``id`` field and produce the output rows dicts.
"""

import csv
import json
import os
import sys

import yaml


def adapt_yaml(filepath):
    """Adapter for YAML harness format with keys ``id``, ``prediction``, ``answer``.

    Returns ``(key_rows, out_rows)`` where:

    - ``key_rows``: list of ``{"id": "..."}`` dicts, one per input row.
    - ``out_rows``: list of ``{"id": "...", "prediction": "...", "answer": "..."}`` dicts,
      one per input row.

    Adapter tax: 3 lines. ``yaml.safe_load_all`` provides generic loading (read
    YAML stream); the 3 adapter lines extract the ``id`` field and produce the
    output-row shape.
    """
    key_rows = []
    out_rows = []
    with open(filepath) as f:
        for chunk in yaml.safe_load_all(f):
            if chunk is None:
                continue
            if isinstance(chunk, dict):
                row_id = chunk.get("id")
                if row_id is not None:
                    key_rows.append({"id": str(row_id)})
                    out_rows.append({
                        "id": str(row_id),
                        "prediction": chunk.get("prediction", ""),
                        "answer": chunk.get("answer", ""),
                    })
            elif isinstance(chunk, list):
                for item in chunk:
                    if isinstance(item, dict):
                        row_id = item.get("id")
                        if row_id is not None:
                            key_rows.append({"id": str(row_id)})
                            out_rows.append({
                                "id": str(row_id),
                                "prediction": item.get("prediction", ""),
                                "answer": item.get("answer", ""),
                            })
    return key_rows, out_rows