"""Client seam to Microsoft's local Power BI MCP server.

propose_remediation delegates the actual TMDL/model write to Microsoft's *local*
server (model authoring). That server isn't always connected, and we test without
it, so the dependency is a pluggable client behind a Protocol. The real client
(an MCP stdio client to microsoft/powerbi-modeling-mcp) is wired later; the
FakeLocalServerClient records intended edits for tests and dry runs.

Per ADR 0003, any real apply targets PBIP files on a branch, never a live
workspace.
"""
from __future__ import annotations

from typing import Any, Protocol


class LocalServerClient(Protocol):
    def apply_tmdl(self, edit: dict[str, Any]) -> dict[str, Any]:
        """Apply a TMDL/model edit (e.g. rewrite a measure). Returns a result."""
        ...


class FakeLocalServerClient:
    """Records edits instead of calling Microsoft's server. Default in tests and
    dry runs. `applied` lets a caller assert what *would* be written."""

    def __init__(self) -> None:
        self.applied: list[dict[str, Any]] = []

    def apply_tmdl(self, edit: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(edit)
        return {"applied": True, "fake": True, "edit": edit}
