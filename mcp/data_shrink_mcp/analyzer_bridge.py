"""Bridge to the existing PBIPProjectAnalyzer.

The analyzer is a standalone script (not a package) that ships in two places in
this repo. We load it by path with importlib so the MCP server can reuse the real
behaviour instead of reimplementing PBIP parsing — M1 (server) + M2 (wire to the
guts) in one move.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

# Candidate locations of pbip_project_analyzer.py, relative to the repo root.
_ANALYZER_CANDIDATES = (
    "docs/advanced/automation-scripts/pbip_project_analyzer.py",
    "modules/scripts/pbip_project_analyzer.py",
)


def _repo_root() -> Path:
    # mcp/data_shrink_mcp/analyzer_bridge.py -> repo root is two parents up from mcp/
    return Path(__file__).resolve().parents[2]


def _load_analyzer_class() -> type:
    root = _repo_root()
    for rel in _ANALYZER_CANDIDATES:
        path = root / rel
        if path.exists():
            spec = importlib.util.spec_from_file_location("pbip_project_analyzer", path)
            assert spec and spec.loader
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module.PBIPProjectAnalyzer
    raise FileNotFoundError(
        "pbip_project_analyzer.py not found in: "
        + ", ".join(str(root / c) for c in _ANALYZER_CANDIDATES)
    )


def analyze(project_path: str) -> dict[str, Any]:
    """Run the real analyzer over a PBIP project and return its raw structure."""
    analyzer_cls = _load_analyzer_class()
    analyzer = analyzer_cls(project_path)
    structure = analyzer.read_pbip_structure()
    # Lineage / data sources — best-effort; the analyzer may no-op on a bare template.
    try:
        structure["data_source_map"] = analyzer.map_data_sources()
    except Exception:  # noqa: BLE001 - lineage is additive, never fatal to a reflection
        structure["data_source_map"] = {}
    return structure
