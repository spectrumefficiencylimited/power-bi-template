"""Tests for validate_change — the governance gate."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_shrink_mcp.validate import validate_change  # noqa: E402


def test_measure_non_distinct_patient_count_is_rejected():
    r = validate_change({"kind": "measure", "name": "Number of Patients",
                         "expression": "COUNT('ER_Data'[Patient ID])"})
    assert r["ok"] is False
    assert any(v["rule"] == "patient_count_distinct" for v in r["violations"])


def test_measure_distinctcount_passes():
    r = validate_change({"kind": "measure", "name": "Number of Patients",
                         "expression": "DISTINCTCOUNT('ER_Data'[Patient ID])"})
    assert r["ok"] is True
    assert r["violations"] == []


def test_non_patient_measure_is_not_judged_by_this_rule():
    r = validate_change({"kind": "measure", "name": "Avg Wait Time",
                         "expression": "AVERAGE('ER_Data'[Patient Wait Time])"})
    assert r["ok"] is True


def test_config_aggregation_must_be_enforced():
    bad = {"kind": "config", "kpis": [
        {"field": "Patient ID", "aggregation": "COUNT",
         "validation": {"aggregation_must_be": "DISTINCTCOUNT"}},
    ]}
    assert validate_change(bad)["ok"] is False

    good = {"kind": "config", "kpis": [
        {"field": "Patient ID", "aggregation": "DISTINCTCOUNT",
         "validation": {"aggregation_must_be": "DISTINCTCOUNT"}},
    ]}
    assert validate_change(good)["ok"] is True


def test_unknown_kind_is_none_not_a_pass():
    assert validate_change({"kind": "what"})["ok"] is None


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok:", name)
    print("all validate tests passed")
