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


def main() -> None:
    """Console entrypoint — runs the server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
