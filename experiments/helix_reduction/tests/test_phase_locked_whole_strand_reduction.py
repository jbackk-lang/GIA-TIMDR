import sys
import unittest
from pathlib import Path
import numpy as np

SRC=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SRC))
from phase_locked_whole_strand_reduction import run, circular_phase_sectors


class PhaseLockedWholeStrandTests(unittest.TestCase):
    def test_quarter_turn_partition(self):
        edges, centers=circular_phase_sectors(4)
        self.assertEqual(len(centers),4)
        self.assertTrue(np.allclose(np.diff(edges),np.pi/2))

    def test_whole_strand_removed_not_arc(self):
        r=run("sphere",samples=360,removed_strand=2)
        self.assertTrue(r["adaptation"]["removed_whole_strand"])
        self.assertTrue(r["adaptation"]["no_local_arc_bridge"])
        self.assertEqual(r["phase_partition"]["remaining_closed_strand_count"],3)

    def test_sphere_changes_90_to_120_degrees(self):
        r=run("sphere",samples=360)
        self.assertEqual(r["phase_partition"]["initial_sector_width_deg"],90.0)
        self.assertEqual(r["phase_partition"]["final_sector_width_deg"],120.0)

    def test_symmetric_sphere_does_not_select_unique_strand(self):
        r=run("sphere",samples=360,expansion=1.2,boundary_radius=1.0)
        self.assertFalse(r["boundary_event"]["first_crossing_is_unique"])

    def test_handedness_winding_is_preserved_both_signs(self):
        for sign in (-1,1):
            r=run("sphere",samples=360,handedness=sign)
            self.assertTrue(r["adaptation"]["handedness_preserved"])
            self.assertEqual(r["adaptation"]["phase_winding_after"],sign)

    def test_egg_arclength_partition_is_not_assumed_equal_phase(self):
        r=run("egg",samples=720)
        self.assertEqual(len(r["egg_arclength_partition_diagnostic_rad"]),5)
        self.assertTrue(r["primary_geometry"] is False)


if __name__=="__main__":
    unittest.main()
