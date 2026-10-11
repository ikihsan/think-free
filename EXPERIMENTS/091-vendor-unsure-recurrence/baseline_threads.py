#!/usr/bin/env python3
"""
E091 — the baseline thread population, transcribed from E090.

Split out of `run_measurement.py` at the 300-line cap. These are 9 practitioner
rows hand-read from MrPLC listings in session 2026-10-10-006 and recorded in
E090/OBSERVATIONS.md; each `vendor_unsure` and `recurrence_observed` flag carries
the row it was read from. They are the instrument's only labelled population at
this size, which is why they live apart from the code that scores them: a
change to the scorer cannot silently rewrite the data it is scored against.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ThreadEntry:
    title: str
    forum: str
    replies: int
    views: int
    error_codes: List[str]
    vendor_unsure: bool  # explicit statement vendor couldn't diagnose
    recurrence_observed: bool  # fault recurred after repair/replacement
    expected_label: str  # 'served' or 'unserved' (from E090 classifier)


# Baseline data from E090: 9 practitioner rows from MrPLC
# These were collected by hand from forum listings in session 2026-10-10-006
BASELINE_THREADS = [
    ThreadEntry(
        title="1747-NI8 Open Circuit",
        forum="Allen Bradley",
        replies=9,
        views=4900,
        error_codes=["1747-NI8"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="Migration Support Needed: Honeywell HC900 to Rockwell ControlLogix",
        forum="Allen Bradley",
        replies=1,
        views=236,
        error_codes=["migration"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="Kinetix 5500 , Studio 5000",
        forum="Allen Bradley",
        replies=1,
        views=197,
        error_codes=["Kinetix 5500"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="USR-N540",
        forum="Allen Bradley",
        replies=3,
        views=301,
        error_codes=["USR-N540"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="Rockwell 1756-L81E ↔ Omron DRT1-COM via 1756-DNB – Analog I/O Scaling Issue",
        forum="Allen Bradley",
        replies=0,
        views=163,
        error_codes=["1756-L81E", "Omron DRT1-COM"],
        vendor_unsure=True,  # "Rockwell unsure of cause" — from E090 OBSERVATIONS.md Row 1
        recurrence_observed=True,  # "same fault on different module" — from E090 OBSERVATIONS.md Row 1
        expected_label="served",
    ),
    ThreadEntry(
        title="CompactLogix Ethernet/IP timing",
        forum="Allen Bradley",
        replies=17,
        views=1400,
        error_codes=["Ethernet/IP timing"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="panelview 600",
        forum="Allen Bradley",
        replies=11,
        views=8200,
        error_codes=["panelview 600"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="FactoryTalkView Project Comparator HTML App",
        forum="Allen Bradley",
        replies=2,
        views=308,
        error_codes=["FactoryTalkView"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="To convert .rss to .pdf",
        forum="Allen Bradley",
        replies=1,
        views=244,
        error_codes=[".rss to .pdf"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
]
