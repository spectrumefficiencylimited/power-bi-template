"""reflect_estate — the first Engine Runtime tool.

Read a PBIP project's metadata and return a semantic topology: the nodes and
edges of reports -> model -> tables/measures -> sources. Read-only. This is the
machine form of "Reading the map" (Episode 1) and the foundation every other
tool builds on.
"""
from __future__ import annotations

from typing import Any

from .analyzer_bridge import analyze


def _name(item: Any, fallback: str) -> str:
    if isinstance(item, dict):
        return str(item.get("name") or item.get("displayName") or fallback)
    return str(item or fallback)


def reflect_estate(project_path: str) -> dict[str, Any]:
    """Build the semantic topology of a PBIP estate from metadata only.

    Returns a dict with `estate`, `nodes`, `edges`, and `counts`. Never reads
    business data — only the model/report structure.
    """
    s = analyze(project_path)
    model = s.get("semantic_model") or {}
    report = s.get("report") or {}

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []

    report_id = "report"
    model_id = "model"
    nodes.append({"id": report_id, "type": "report", "name": report.get("path") or "Report"})
    nodes.append({"id": model_id, "type": "model", "name": model.get("path") or "Semantic Model"})
    edges.append({"source": report_id, "target": model_id, "rel": "uses"})

    for i, t in enumerate(model.get("tables") or []):
        tid = f"table:{i}"
        nodes.append({"id": tid, "type": "table", "name": _name(t, tid)})
        edges.append({"source": model_id, "target": tid, "rel": "contains"})

    for i, m in enumerate(model.get("measures") or []):
        mid = f"measure:{i}"
        nodes.append({"id": mid, "type": "measure", "name": _name(m, mid)})
        edges.append({"source": mid, "target": model_id, "rel": "defined-in"})

    for i, d in enumerate(model.get("data_sources") or []):
        did = f"source:{i}"
        nodes.append({"id": did, "type": "source", "name": _name(d, did)})
        edges.append({"source": model_id, "target": did, "rel": "refreshes-from"})

    for rel in model.get("relationships") or []:
        if isinstance(rel, dict) and rel.get("fromTable") and rel.get("toTable"):
            edges.append({"source": str(rel["fromTable"]), "target": str(rel["toTable"]), "rel": "joins-with"})

    return {
        "estate": s.get("project_name") or s.get("project_path") or project_path,
        "nodes": nodes,
        "edges": edges,
        "counts": {
            "tables": len(model.get("tables") or []),
            "measures": len(model.get("measures") or []),
            "data_sources": len(model.get("data_sources") or []),
            "pages": len(report.get("pages") or []),
            "visuals": len(report.get("visuals") or []),
        },
    }
