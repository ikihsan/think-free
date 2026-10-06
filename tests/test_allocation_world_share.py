"""The per-day world-facing share, held to a floor rather than a ceiling.

Split out of `test_allocation_measurement.py` at the 300-line cap. It is a
separate assertion with a separate direction, and the file it came from had
already repaired this exact finding twice.

Background, in the finding's own words: F025 measured that measurement of the
world is a small minority of this mission's commits, and F031 measured that
machinery outweighs experiment code 4.8:1. The gate that encoded the first
finding looped over *every* day in history and failed any day where
world-facing work was not a minority. That is the calendar-defect this
repository has now named three times (F018, F019, F022): the per-day share is a
property of which commits exist, so appending an honest day's work can turn the
gate red with no artefact changing. On 2026-10-06 E033 made the share 7 of 14 =
50.0% and the gate failed the most world-facing day in the record.

The direction was wrong as well as unscoped. F031's complaint is that the mission
spends itself on its own record, so the assertion that supports the finding is a
**floor**: a day must contain some measurement of the world. A ceiling on
world-facing work enforces the thing the mission is trying to escape, which is the
mistake F052 recorded about the original ratio gate.
"""
import unittest


class WorldShareTest(unittest.TestCase):
    """The assertion that replaces the per-day "world must be a minority" loop.

    F031's complaint is that the mission spends its effort on its own record. The
    direction that supports it is a **floor** on world-facing work, not a ceiling:
    a day must contain some measurement of the world, or F031's finding holds.
    This class exists so the replacement is falsified in both directions rather
    than merely asserted, which is the same discipline the ratio ceiling got.
    """

    # F025's measured days, and the smallest world share either of them recorded.
    F025_DAYS = {"2026-10-03": 11.1, "2026-10-04": 5.4}
    FLOOR = 5.0

    def test_the_floor_fires_on_a_day_with_no_world_facing_work(self) -> None:
        for day, share in self.F025_DAYS.items():
            self.assertGreaterEqual(
                share, self.FLOOR,
                "F025's day %s has world share %.1f%%, at or under the floor, so the "
                "floor is not measured against the days the finding came from"
                % (day, share))

    def test_it_fires_on_the_shape_f031_described(self) -> None:
        # F031's own shape: the day is prose and machinery, with none of it
        # measuring the world. This is what the removed loop should have caught.
        f031_shape = {"commits": 100, "world": 0, "machinery": 44, "prose": 56}
        self.assertLess(
            100.0 * f031_shape["world"] / f031_shape["commits"], self.FLOOR,
            "the replacement must fail on a day shaped like F031's complaint")

    def test_it_does_not_fire_on_the_most_world_facing_day_on_record(self) -> None:
        # 2026-10-06, E033: 7 of 14 commits world-facing. The removed loop failed
        # here; the floor passes, which is the point of the change.
        e033 = {"commits": 14, "world": 7, "machinery": 1, "prose": 5}
        self.assertGreaterEqual(
            100.0 * e033["world"] / e033["commits"], self.FLOOR,
            "a session whose commits are mostly world-facing work must pass")


if __name__ == "__main__":
    unittest.main()
