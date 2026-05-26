"""Smoke test for reflect_estate against the bundled Project.Template.

Tests the logic module directly (no MCP SDK needed), so it runs anywhere Python
does. Verifies reflect_estate produces a well-formed topology over the real
analyzer, even on a near-empty template.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # mcp/ on path

from data_shrink_mcp.estate import reflect_estate  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_reflect_estate_shape():
    result = reflect_estate(str(REPO_ROOT))

    assert set(result) >= {"estate", "nodes", "edges", "counts"}
    assert isinstance(result["nodes"], list) and isinstance(result["edges"], list)

    # The report and model anchor nodes always exist, with the report->model edge.
    types = {n["type"] for n in result["nodes"]}
    assert "report" in types and "model" in types
    assert any(e["rel"] == "uses" for e in result["edges"])

    # Counts are present and non-negative integers.
    for key in ("tables", "measures", "data_sources", "pages", "visuals"):
        assert isinstance(result["counts"][key], int)
        assert result["counts"][key] >= 0


if __name__ == "__main__":
    test_reflect_estate_shape()
    print("ok: reflect_estate smoke test passed")
