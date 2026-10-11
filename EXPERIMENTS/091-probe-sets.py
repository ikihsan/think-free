#!/usr/bin/env python3
"""
E091 Discrimination Test — the labelled probe sets.

Split out of `091-discrimination-harness.py` at the 300-line cap. These are the
instrument's own reference labels, not measurements: 20 known-served and 20
known-unserved queries from E090/OBSERVATIONS.md and E088/probes.jsonl, plus
five MrPLC-domain served probes. They are kept apart from the runner so that
changing a probe set cannot silently change the run that reports its gates.
"""

# ============================================================================
# Default probe sets (known-served and known-unserved)
# These are the same probes from E090/OBSERVATIONS.md and E088/probes.jsonl
# ============================================================================

DEFAULT_KNOWN_SERVED = [
    {"probe_id": "S01", "query": "Python ImportError: No module named 'requests'"},
    {"probe_id": "S02", "query": "python unittest assertRaises example"},
    {"probe_id": "S03", "query": "sqlite3 primary key syntax"},
    {"probe_id": "S04", "query": "tar extract a single file from archive"},
    {"probe_id": "S05", "query": "difference between TCP and UDP"},
    {"probe_id": "S06", "query": "how to sort a list of dictionaries by key"},
    {"probe_id": "S07", "query": "git undo last commit keep changes"},
    {"probe_id": "S08", "query": "how to calculate standard deviation in excel"},
    {"probe_id": "S09", "query": "what causes a segfault in C"},
    {"probe_id": "S10", "query": "convert UTC to local time in javascript"},
    {"probe_id": "S11", "query": "how to replace a brake rotor"},
    {"probe_id": "S12", "query": "sourdough starter not rising"},
    {"probe_id": "S13", "query": "how to jump start a car"},
    {"probe_id": "S14", "query": "photosynthesis equation explanation"},
    {"probe_id": "S15", "query": "how to tie a bowline knot"},
    {"probe_id": "S16", "query": "what is the difference between weather and climate"},
    {"probe_id": "S17", "query": "how to change a flat bicycle tire"},
    {"probe_id": "S18", "query": "setting up nginx reverse proxy"},
    {"probe_id": "S19", "query": "how to read a resistor color code"},
    {"probe_id": "S20", "query": "first aid for a minor burn"},
]

DEFAULT_KNOWN_UNSERVED = [
    {"probe_id": "U01", "query": "Zorbex-4400 manifold gasket torque specification"},
    {"probe_id": "U02", "query": "Kellundar VX-7 pump calibration procedure"},
    {"probe_id": "U03", "query": "Brantmore Trellis-9 startup checklist"},
    {"probe_id": "U04", "query": "Quilvane HX-3 coil cleaning interval"},
    {"probe_id": "U05", "query": "Marnot Deltrix-88 firmware update notes"},
    {"probe_id": "U06", "query": "Ostrander Pellix-2 filter replacement interval"},
    {"probe_id": "U07", "query": "Vandermolen Cristar-45 belt tension specification"},
    {"probe_id": "U08", "query": "Halberdix Ferrolux-6 coolant mixing ratio"},
    {"probe_id": "U09", "query": "Pemberton Algrid-31 firmware changelog"},
    {"probe_id": "U10", "query": "Corvane Stellarium-19 bearing tolerance"},
    {"probe_id": "U11", "query": "Wexbridge Tolliver-2 firmware flashing guide"},
    {"probe_id": "U12", "query": "Nyxhollow Perigee-27 maintenance schedule"},
    {"probe_id": "U13", "query": "Ashgrove Windermere-5 alignment procedure"},
    {"probe_id": "U14", "query": "Pellworth Draymar-13 pressure relief setting"},
    {"probe_id": "U15", "query": "Selbrand Illuvion-4 error code list"},
    {"probe_id": "U16", "query": "Thornbury Vexmoor-8 lubricant specification"},
    {"probe_id": "U17", "query": "Calderon Quintrix-12 troubleshooting guide"},
    {"probe_id": "U18", "query": "Ravensmoor Yelworth-6 cycle time data"},
    {"probe_id": "U19", "query": "Penhurst Amberlok-3 retrofit instructions"},
    {"probe_id": "U20", "query": "Strathmore Dovetail-9 commissioning report"},
]

# Known-served probes with expected to be found on MrPLC (fault/error code domains)
# These are mapped to actual MrPLC thread titles for the harness test
MRPLC_SERVED_PROBE_MAP = [
    # These probe queries should match MrPLC threads with error codes
    {"probe_id": "S01", "query": "Allen Bradley PLC error code 125", "expected_served": True},
    {"probe_id": "S02", "query": "Mitsubishi fault code 1134", "expected_served": True},
    {"probe_id": "S03", "query": "Siemens HMI error code", "expected_served": True},
    {"probe_id": "S04", "query": "Omron error -10 no system program", "expected_served": True},
    {"probe_id": "S05", "query": "Modbus exception code 03", "expected_served": True},
]
