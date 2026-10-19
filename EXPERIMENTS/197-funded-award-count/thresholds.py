#!/usr/bin/env python3
"""E197 declared constants. One file, so no panel can drift from the protocol.

Nothing here is tuned after a result is seen. `G4_CODEBOOK` is copied from
E196's committed `raw/panel2.json` and checked against those bytes at run time
by control C6, so a silent edit to the population shows up as a failed control
rather than as a different denominator.
"""

# The six amount thresholds. Declared in PROTOCOL.md §4 before panel1.py was
# written. `t=1` is the mission-critical one: amounts are in cents, so
# `amount >= $1` is the cheapest expression of "carries money" the data
# supports, and `t=0` separates deobligations from everything else.
THRESHOLDS = [0, 1, 100, 1000, 10000, 100000]

# The funded threshold, named so a panel cannot quote a different one.
FUNDED_T = 1

# E196's addressability cutoff, carried forward unchanged.
SMALL_CUTOFF = 100000.0

# E196's cell-total bar ($1B), carried forward so G4 measures the same thing
# E196's G4 measured, with the zero-record population removed.
CELL_BAR = 1e9

# PROTOCOL.md §4: `spending_by_award` answers 200 for page 500 and 422 for page
# 501 (E196 F143). Carried forward as a constant, not re-measured here.
MAX_PAGE = 500

# PROTOCOL.md §5 panel A: the geometric scan of ascending blocks. Rank r is
# covered by page ceil(r/100); these are the powers of two plus the ceiling.
SCAN_RANKS = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 50000]

# PROTOCOL.md §7 gate thresholds.
G1_MIN_MEASURED = 98
G2_MAX_POPULATION = 100
G3_FIRED = 0.50          # two-sided: >= survives, < kills
G4_SURVIVES = 10
G4_KILLS = 5
G4_UNRESOLVED_BAND = (6, 9)
G5_MIN_AGREE = 23        # of 25 panel-B codes
G6_MIN_RATIO = 2.0
G6_MIN_ROWS = 20         # emptiness clause, declared before the run

# E196's 25 G4-clearing codes, from E196 `raw/panel2.json`
# G4.codes_clearing_rank_and_total. Verified against those bytes by C6.
G4_CODEBOOK = [
    "1560", "1680", "2320", "2840", "4220", "5342", "6505", "6515", "6640",
    "7030", "7A21", "8905", "8915", "9130", "D304", "DA01", "DA10", "Q999",
    "R425", "R499", "R706", "S206", "S216", "U099", "Z2AA",
]

# The five IT/software cells E196 §2 called the densest cluster, and the ones
# G6 and panel D are declared over.
IT_CODES = ["DA01", "DA10", "7A21", "7030", "D304"]

# E196 §6 defect 2: a cell's smallest awards are its deobligations. The share of
# them is a reported number here, not a correction to the count.