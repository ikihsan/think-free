#!/usr/bin/env python3
"""E196 declared constants -- one place, so no file can drift from a threshold.

Every value below is quoted from PROTOCOL.md or AMENDMENT-1/2 verbatim. Nothing
here was chosen after a result was seen; if a value ever needs to move, the
amendment that moves it must name this file.
"""

SMALL_CUTOFF = 100000.0        # PROTOCOL.md instruments table; unchanged in AMENDMENT-1
G4_BAR_USD = 1_000_000_000.0   # PROTOCOL.md G4; unchanged in AMENDMENT-1
KW_ALPHA = 0.01                # PROTOCOL.md G3
G5_MIN_DESCRIBED = 20          # AMENDMENT-2 section 2
G5_RATIO = 2.0                 # PROTOCOL.md G5
# AMENDMENT-3: the ascending-rank checkpoints. Round powers of ten and the
# median, declared before any systematic measurement, none tuned to a result.
RANK_CHECKPOINTS = (100, 1000, 10000, 100000, 1000000)
G4_MIN_RANK = 10000            # AMENDMENT-3: "at least this many awards"
G4_MIN_TOTAL_USD = 1_000_000_000.0   # PROTOCOL.md G4 bar, unchanged
POSITIVE_CONTROL_FAMILIES = {
    "Y1": {"construct", "repair", "renovat", "rehabilitat", "remodel"},
    "3": {"construct", "repair", "renovat", "rehabilitat", "remodel"},
    "S2": {"housekeep", "janitor", "custodial", "cleaning", "guard"},
}
STOPWORDS = set("""a an the and or of for to in on at by with from as is are be was were
this that these those it its be been being have has had do does did not no nor so than then
there here when where which who whom what how all any each per via use used using also more
most other others such only own same too very s t don now""".split())
