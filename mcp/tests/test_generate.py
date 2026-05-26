"""Tests for generate_module — gate-first write tool."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_shrink_mcp.generate import generate_module  # noqa: E402

GOOD = {
    "project": {"domain": "healthcare"},
    "branding": {"primary_color": "#0066CC"},
    "kpis": [
        {"field": "Patient ID", "display_name": "Number of Patients",
         "aggregation": "DISTINCTCOUNT", "format": "#,0",
         "validation": {"aggregation_must_be": "DISTINCTCOUNT"}},
        {"field": "Patient Wait Time", "display_name": "Avg Wait Time (min)",
         "aggregation": "AVERAGE", "format": "#,0.0"},
    ],
}

BAD = {
    "project": {"domain": "healthcare"},
    "kpis": [
        {"field": "Patient ID", "aggregation": "COUNT",
         "validation": {"aggregation_must_be": "DISTINCTCOUNT"}},
    ],
}


def test_bad_config_writes_nothing():
    with tempfile.TemporaryDirectory() as d:
        r = generate_module(BAD, out_dir=d)
        assert r["ok"] is False and r["written"] is False
        assert r["violations"]
        assert list(Path(d).iterdir()) == []   # gate refused — no file


def test_good_config_generates_and_writes():
    with tempfile.TemporaryDirectory() as d:
        r = generate_module(GOOD, out_dir=d)
        assert r["ok"] is True and r["written"] is True
        module = json.loads(Path(r["path"]).read_text())
        assert module["module_type"] == "kpi_strip"
        assert len(module["cards"]) == 2
        assert module["cards"][0]["aggregation"] == "DISTINCTCOUNT"
        assert module["cards"][0]["primary_color"] == "#0066CC"


def test_dry_run_without_out_dir():
    r = generate_module(GOOD)
    assert r["ok"] is True and r["written"] is False and r["path"] is None
    assert r["module"]["cards"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok:", name)
    print("all generate tests passed")
