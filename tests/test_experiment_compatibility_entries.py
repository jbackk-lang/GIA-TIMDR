"""Static integrity checks for the legacy experiment entry points.

Do not import the adapters here: executing them runs the full experiment.
"""
import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
ALLOWED_GROUPS = {"chronoprocess", "reflections", "rhombic_prism"}


def _group_map(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    assignments = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "_GROUP"
                for target in node.targets)
    ]
    assert len(assignments) == 1, f"{path}: expected exactly one _GROUP mapping"
    value = ast.literal_eval(assignments[0].value)
    assert isinstance(value, dict), f"{path}: _GROUP must be a literal dictionary"
    return value


def test_all_legacy_experiment_entries_resolve_to_canonical_files():
    adapters = sorted(EXPERIMENTS.glob("*.py"))
    assert adapters, "No legacy experiment adapters found"

    expected_map = _group_map(adapters[0])
    assert expected_map, "Compatibility map is empty"
    assert set(expected_map.values()) <= ALLOWED_GROUPS

    adapter_names = {path.name for path in adapters}
    assert set(expected_map) == adapter_names, (
        "Adapter files and compatibility map differ: "
        f"unmapped={sorted(adapter_names - set(expected_map))}, "
        f"missing={sorted(set(expected_map) - adapter_names)}"
    )

    for adapter in adapters:
        mapping = _group_map(adapter)
        assert mapping == expected_map, f"{adapter}: inconsistent compatibility map"
        assert adapter.name in mapping, f"{adapter}: no self mapping"
        target = EXPERIMENTS / mapping[adapter.name] / adapter.name
        assert target.is_file(), f"{adapter}: canonical target missing: {target}"
        assert target.resolve() != adapter.resolve()
