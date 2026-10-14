"""Adapter for XML harness format with ``<row>`` elements containing ``id``,
``prediction``, and ``answer`` child elements.

Uses ``xml.etree.ElementTree`` for generic loading (free). Adapter-specific
lines: extract the ``id`` field and produce the output rows dicts.
"""

import csv
import json
import os
import sys

import xml.etree.ElementTree as ET


def adapt_xml(filepath):
    """Adapter for XML harness format with ``<row>`` elements.

    Returns ``(key_rows, out_rows)`` where:

    - ``key_rows``: list of ``{"id": "..."}`` dicts, one per ``<row>`` element.
    - ``out_rows``: list of ``{"id": "...", "prediction": "...", "answer": "..."}`` dicts,
      one per ``<row>`` element.

    Adapter tax: 3 lines. ``ElementTree.iter`` provides generic loading (parse
    XML file); the 3 adapter lines extract the ``id`` field and produce the
    output-row shape.
    """
    key_rows = []
    out_rows = []
    tree = ET.parse(filepath)
    root = tree.getroot()
    for row in root.iter("row"):
        row_id = row.get("id")
        if row_id is not None:
            prediction = row.findtext("prediction", "")
            answer = row.findtext("answer", "")
            key_rows.append({"id": str(row_id)})
            out_rows.append({
                "id": str(row_id),
                "prediction": str(prediction) if prediction is not None else "",
                "answer": str(answer) if answer is not None else "",
            })
    return key_rows, out_rows