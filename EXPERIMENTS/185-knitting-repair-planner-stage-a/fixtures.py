"""E185 fixtures: eight single-error knit fabrics."""

from graph_model import *  # noqa: F401,F403
from graph_fabrics import *  # noqa: F401,F403
from graph_errors import *  # noqa: F401,F403

FIXTURES = [
    {
        'name': 'F1_stockinette_dropped',
        'description': '4x4 stockinette with one dropped stitch at (1,1)',
        'factory': lambda: introduce_error(create_stockinette_graph(4, 4), "dropped_stitch", row=1, col=1),
        'correct_factory': lambda: create_stockinette_graph(4, 4),
        'expected_error': 'dropped_stitch',
    },
    {
        'name': 'F2_rib_twisted',
        'description': '4x4 1x1 rib with one twisted stitch at (1,2)',
        'factory': lambda: introduce_error(create_rib_graph(4, 4, 1), "twisted_stitch", row=1, col=2),
        'correct_factory': lambda: create_rib_graph(4, 4, 1),
        'expected_error': 'twisted_stitch',
    },
    {
        'name': 'F3_cable_wrong_cross',
        'description': '7x7 cable fabric with wrong crossing at row 4 (not at boundary)',
        'factory': lambda: introduce_error(create_cable_graph(7, 7, 4), "wrong_cable_crossing", row=4, col=2),
        'correct_factory': lambda: create_cable_graph(7, 7, 4),
        'expected_error': 'wrong_cable_crossing',
    },
    {
        'name': 'F4_stockinette_yarnover',
        'description': '5x5 stockinette with unresolved yarnover at (2,2)',
        'factory': lambda: introduce_error(create_stockinette_graph(5, 5), "extra_yarnover", row=2, col=2),
        'correct_factory': lambda: create_stockinette_graph(5, 5),
        'expected_error': 'extra_yarnover',
    },
    {
        'name': 'F5_stockinette_wrong_type',
        'description': '5x5 stockinette with one wrong stitch type at (2,2) - purl in knit row',
        'factory': lambda: introduce_error(create_stockinette_graph(5, 5), "wrong_stitch_type", row=2, col=2),
        'correct_factory': lambda: create_stockinette_graph(5, 5),
        'expected_error': 'twisted_stitch',
    },
    {
        'name': 'F6_stockinette_two_dropped',
        'description': '4x4 stockinette with two adjacent dropped stitches at (1,1) and (1,2)',
        'factory': lambda: introduce_error(create_stockinette_graph(4, 4), "two_adjacent_dropped", row=1, col=1),
        'correct_factory': lambda: create_stockinette_graph(4, 4),
        'expected_error': 'dropped_stitch',
    },
    {
        'name': 'F7_cable_mis_cross_3',
        'description': '7x7 cable fabric with mis-crossed cable at row 4 (not at boundary)',
        'factory': lambda: introduce_error(create_cable_graph(7, 7, 4), "mis_crossed_cable_3", row=4, col=2),
        'correct_factory': lambda: create_cable_graph(7, 7, 4),
        'expected_error': 'wrong_cable_crossing',
    },
    {
        'name': 'F8_garter_dropped_edge',
        'description': '4x4 garter stitch with dropped stitch at edge (0,0)',
        'factory': lambda: introduce_error(create_garter_graph(4, 4), "dropped_stitch_edge", row=0, col=0),
        'correct_factory': lambda: create_garter_graph(4, 4),
        'expected_error': 'dropped_stitch',
    },
]


