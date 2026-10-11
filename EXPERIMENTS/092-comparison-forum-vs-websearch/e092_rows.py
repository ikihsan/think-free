#!/usr/bin/env python3
"""
E092 — the hand-read forum rows the comparison runs on.

Split out of `compare_data_formats.py` at the 300-line cap. These are the 9
MrPLC and 7 MedWrench practitioner rows transcribed from E090/OBSERVATIONS.md,
where each was read by hand from a public forum listing (session
2026-10-10-006). They are the treatment arm of the comparison; the web-search
control arm is read from E083's committed JSONL at run time.
"""


# MrPLC rows from E090 OBSERVATIONS.md
mrplc_rows = [
    {"query_text": "GuardLogix fault 125/120 on 1734-IE4S", "title": "GuardLogix fault 125/120 on 1734-IE4S", "body": "Specific fault codes on 1734-IE4S analog module; Rockwell unsure of cause; practitioner seeks root cause after module replacement failed to prevent recurrence"},
    {"query_text": "Timer not counting", "title": "Timer not counting", "body": "Timer instruction not incrementing"},
    {"query_text": "Gx Work 2 software error", "title": "Gx Work 2 software error", "body": "\"System stop failed\" - Software launch error; practitioner doesn't know reason"},
    {"query_text": "Mitsubishi iQ-R communication error", "title": "Mitsubishi iQ-R communication error", "body": "Communication error on iQ-R series with codes 1134, C0B2, C709"},
    {"query_text": "HMI TP1200 Comfort Panel error", "title": "HMI TP1200 Comfort Panel error", "body": "Specific application crash error message HMIRTM.EXE"},
    {"query_text": "Why is my PLC analog input fluctuating", "title": "Why is my PLC analog input fluctuating", "body": "Intermittent analog input fluctuation"},
    {"query_text": "Studio 5000 Install Error 1606", "title": "Studio 5000 Install Error 1606", "body": "Windows installer error codes during software installation"},
    {"query_text": "Error -10 No system program", "title": "Error -10 No system program", "body": "Specific error code; \"No system program\""},
    {"query_text": "NX1P2 and 3rd Party HMI timeout errors", "title": "NX1P2 and 3rd Party HMI timeout errors", "body": "Communication timeout errors with 3rd party HMI"},
]

# MedWrench rows from E090 OBSERVATIONS.md
medwrench_rows = [
    {"query_text": "Error 10901 with FlashIIP station", "title": "Error 10901 with FlashIIP station", "body": "Specific error code on computed radiography system"},
    {"query_text": "How to access Service Mode", "title": "How to access Service Mode", "body": "Practitioner needs service manual/mode access"},
    {"query_text": " troubleshooting how to test the patient cable", "title": "troubleshooting how to test the patient cable", "body": "Procedural troubleshooting"},
    {"query_text": "Image file for Compact flash which holds the unit", "title": "Image file for Compact flash which holds the unit", "body": "Needs firmware/image file for CF card"},
    {"query_text": "Show error E06 and led INHIBIT light", "title": "Show error E06 and led INHIBIT light", "body": "Specific error code E06 + LED indicator"},
    {"query_text": "REPLACEMENT FAN PART NUMBER", "title": "REPLACEMENT FAN PART NUMBER", "body": "Parts identification request"},
    {"query_text": "during processing loud screech audible", "title": "during processing loud screech audible", "body": "Audible fault symptom"},
]

