import math
import sys
import unittest
from pathlib import Path


MOTION_LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MOTION_LAB))

import compose  # noqa: E402
import primitives  # noqa: E402
import preview  # noqa: E402


class PrimitiveTests(unittest.TestCase):
    def test_defaults_pass_documented_sampled_clearance_check(self):
        for name, (fn, _description, _kind) in primitives.PRIMITIVES.items():
            with self.subTest(primitive=name):
                amplitude = fn.__defaults__[0]
                ok, overlap = primitives.collision_safe(fn, amplitude, preview.GAP)
                self.assertTrue(ok, f"sampled overlap for {name}: {overlap:.2f}px")

    def test_sampled_clearance_check_detects_overlap(self):
        def overlapping_rows(_col, row, _t, _amplitude):
            return row * 20.0

        ok, overlap = primitives.collision_safe(
            overlapping_rows, amp_test=1.0, gap=18.0
        )
        self.assertFalse(ok)
        self.assertAlmostEqual(overlap, 2.0)

    def test_cyclic_primitives_return_to_start(self):
        cyclic = [
            "traveling_wave",
            "ripple",
            "standing_wave",
            "column_cascade",
            "row_sweep",
            "elevator_reveal",
            "breathing",
        ]
        for name in cyclic:
            fn = primitives.PRIMITIVES[name][0]
            amplitude = fn.__defaults__[0]
            for col in range(primitives.COLS):
                for row in range(primitives.ROWS):
                    with self.subTest(primitive=name, col=col, row=row):
                        self.assertAlmostEqual(
                            fn(col, row, 0.0, amplitude),
                            fn(col, row, 1.0, amplitude),
                            places=7,
                        )


class ChoreographyTests(unittest.TestCase):
    def test_example_choreographies_cover_one_normalized_loop(self):
        for name, choreography in compose.CHOREOS.items():
            beats = choreography["beats"]
            with self.subTest(choreography=name):
                self.assertEqual(beats[0]["t0"], 0.0)
                self.assertEqual(beats[-1]["t1"], 1.0)
                for current, following in zip(beats, beats[1:]):
                    self.assertEqual(current["t1"], following["t0"])
                for beat in beats:
                    self.assertIn(beat["primitive"], primitives.PRIMITIVES)
                    self.assertGreater(beat["t1"], beat["t0"])

    def test_composed_offsets_are_finite(self):
        for name, choreography in compose.CHOREOS.items():
            for t in (0.0, 0.25, 0.5, 0.75, 0.999):
                with self.subTest(choreography=name, t=t):
                    value = compose.compose_dy(2, 1, t, choreography)
                    self.assertTrue(math.isfinite(value))


if __name__ == "__main__":
    unittest.main()
