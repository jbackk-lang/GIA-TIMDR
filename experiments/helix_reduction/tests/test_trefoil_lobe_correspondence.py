import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from trefoil_lobe_correspondence_audit import trefoil_torsion_sector_audit


def test_trefoil_torsion_distribution_repeats_in_three_sectors():
    r = trefoil_torsion_sector_audit(samples=6000)
    assert r["threefold_torsion_symmetry"]
    assert r["sector_mean_spread"] < 1e-10


def test_each_trefoil_sector_contains_both_torsion_signs():
    r = trefoil_torsion_sector_audit(samples=6000)
    assert r["each_sector_contains_both_torsion_signs"]


def test_scalar_plus_minus_plus_is_not_torsion_plus_minus_plus():
    r = trefoil_torsion_sector_audit(samples=6000)
    assert r["scalar_signal_lobe_word"] == [1, -1, 1]
    assert len(r["trefoil_sector_torsion"]) == 3
    assert all(x["positive_fraction"] > 0.5 for x in r["trefoil_sector_torsion"])
