"""Tests for propose_remediation — gate-first, client-delegated edit."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_shrink_mcp.remediate import propose_remediation  # noqa: E402
from data_shrink_mcp.microsoft_bridge import FakeLocalServerClient  # noqa: E402

FINDING = {"rule": "patient_count_distinct"}
BAD_MEASURE = {"name": "Number of Patients", "expression": "COUNT('ER_Data'[Patient ID])"}


def test_proposes_distinctcount_rewrite_and_passes_gate():
    r = propose_remediation(FINDING, measure=BAD_MEASURE)
    assert r["ok"] is True
    assert r["proposal"]["expression"] == "DISTINCTCOUNT('ER_Data'[Patient ID])"
    assert r["applied"] is False          # dry-run by default


def test_apply_delegates_to_client():
    client = FakeLocalServerClient()
    r = propose_remediation(FINDING, measure=BAD_MEASURE, client=client, apply=True)
    assert r["ok"] is True and r["applied"] is True
    assert client.applied and client.applied[0]["op"] == "rewrite_measure"
    assert client.applied[0]["expression"] == "DISTINCTCOUNT('ER_Data'[Patient ID])"


def test_unhandled_rule_returns_none():
    assert propose_remediation({"rule": "require_calendar"}, measure=BAD_MEASURE)["ok"] is None


def test_missing_measure_returns_none():
    assert propose_remediation(FINDING)["ok"] is None


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok:", name)
    print("all remediate tests passed")
