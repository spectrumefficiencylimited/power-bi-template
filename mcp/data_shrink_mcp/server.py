"""The Data Shrink MCP server (Engine Runtime).

Thin FastMCP wrapper. Each tool delegates to a tested module so the logic runs
without the MCP SDK in tests. v1 exposes reflect_estate; score_baseline,
validate_change, generate_module, and propose_remediation follow.
"""
from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .estate import reflect_estate as _reflect_estate
from .baseline import score_baseline as _score_baseline
from .validate import validate_change as _validate_change

mcp = FastMCP("data-shrink")


@mcp.tool()
def reflect_estate(project_path: str) -> dict[str, Any]:
    """Build the semantic topology (reports -> model -> tables/measures/sources)
    of a PBIP project from metadata only. Read-only; reads no business data.

    Args:
        project_path: path to a PBIP project folder (containing *.SemanticModel
            and *.Report).
    """
    return _reflect_estate(project_path)


@mcp.tool()
def score_baseline(project_path: str) -> dict[str, Any]:
    """Score a PBIP estate against the governance rules and return the capability
    baseline: per-axis scores (0-5), an overall, and findings tagged by rule and
    severity. Read-only. Axes with no judgeable signal are null, not faked.

    Args:
        project_path: path to a PBIP project folder.
    """
    return _score_baseline(project_path)


@mcp.tool()
def validate_change(change: dict[str, Any], project_path: str | None = None) -> dict[str, Any]:
    """Validate a proposed change against the estate's governance rules before
    anything is written. Read-only; the gate every write tool calls first.

    Returns {ok, violations}. ok is True (clean), False (violations), or None
    (unknown change kind).

    Args:
        change: {"kind": "measure", "name": ..., "expression": ...} or
            {"kind": "config", "kpis": [...]}.
        project_path: optional PBIP path, enables drift checks against the
            existing estate.
    """
    return _validate_change(change, project_path)


def main() -> None:
    """Console entrypoint — runs the server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
