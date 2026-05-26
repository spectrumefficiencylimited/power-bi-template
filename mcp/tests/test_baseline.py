"""Tests for the rules engine and score_baseline.

Rules are tested with crafted estate structures (no real PBIP needed), so the
governance core is verified directly. score_baseline gets a smoke test over the
bundled template.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_shrink_mcp.rules import (  # noqa: E402
    rule_patient_count_distinct, rule_require_calendar, rule_measure_drift,
)
from data_shrink_mcp.baseline import score_baseline  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]


def _estate(tables):
    return {"semantic_model": {"tables": tables, "measures": [], "relationships": []}}


DRIFTY = _estate([
    {"name": "ER_Data", "measures": [
        {"name": "Number of Patients", "expression": "COUNT('ER_Data'[Patient ID])"},
    ]},
])

CLEAN = _estate([
    {"name": "Calendar", "measures": []},
    {"name": "ER_Data", "measures": [
        {"name": "Number of Patients", "expression": "DISTINCTCOUNT('ER_Data'[Patient ID])"},
    ]},
])

DUPLICATED = _estate([
    {"name": "ModelA", "measures": [{"name": "Number of Patients", "expression": "COUNT(x)"}]},
    {"name": "ModelB", "measures": [{"name": "Number of Patients", "expression": "DISTINCTCOUNT(x)"}]},
])


def test_patient_count_rule_catches_non_distinct():
    assert rule_patient_count_distinct(DRIFTY).ok is False
    assert rule_patient_count_distinct(CLEAN).ok is True


def test_require_calendar():
    assert rule_require_calendar(DRIFTY).ok is False
    assert rule_require_calendar(CLEAN).ok is True


def test_measure_drift_detects_same_name_different_def():
    assert rule_measure_drift(DUPLICATED).ok is False
    assert rule_measure_drift(CLEAN).ok is True


def test_insufficient_signal_is_none_not_a_fail():
    empty = {"semantic_model": {"tables": [], "measures": [], "relationships": []}}
    assert rule_patient_count_distinct(empty).ok is None
    assert rule_require_calendar(empty).ok is None


def test_score_baseline_smoke():
    result = score_baseline(str(REPO_ROOT))
    assert set(result) >= {"estate", "overall", "axes", "findings"}
    assert isinstance(result["findings"], list) and len(result["findings"]) == 5
    # Empty template → no judgeable signal → overall is null, not a fake 0 or 5.
    assert result["overall"] is None


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok:", name)
    print("all baseline tests passed")
