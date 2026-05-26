"""validate_change — the shared governance gate.

Checks a *proposed* change against the estate's rules before anything is written.
Read-only. This is the seam every write tool (generate_module,
propose_remediation) calls first, so the Engine can never write a change that
fails the rules. It is also exposed as a standalone tool.

Supported change kinds:
  - "measure": {name, expression}  — a measure being added/edited
  - "config":  {kpis: [...]}        — a generation config (hospital_er.yaml shape)
"""
from __future__ import annotations

import re
from typing import Any, Optional

from .analyzer_bridge import analyze
from .rules import Finding, _expr, _is_patient_count, gather_measures


def _norm(name: str) -> str:
    return re.sub(r"\s+", " ", str(name or "")).strip().lower()


def _check_measure(change: dict[str, Any], project_path: Optional[str]) -> list[dict[str, Any]]:
    name = str(change.get("name") or "")
    expr = str(change.get("expression") or "")
    out: list[Finding] = []

    if _is_patient_count({"name": name, "expression": expr}):
        distinct = re.search(r"\bDISTINCTCOUNT\b", expr, re.I)
        counts = re.search(r"\bCOUNTROWS\b|\bCOUNT\b", expr, re.I)
        if counts and not distinct:
            out.append(Finding("patient_count_distinct", "Semantic governance", "error", False,
                               f"Measure '{name}' must use DISTINCTCOUNT, not COUNT/COUNTROWS."))

    if project_path:
        for ex in gather_measures(analyze(project_path)):
            if _norm(ex.get("name")) == _norm(name) and _expr(ex).strip() and _expr(ex).strip() != expr.strip():
                out.append(Finding("measure_drift", "Semantic governance", "warning", False,
                                   f"'{name}' already exists with a different definition — would create drift."))
                break
    return [f.to_dict() for f in out]


def _check_config(change: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[Finding] = []
    for k in change.get("kpis") or []:
        must = (k.get("validation") or {}).get("aggregation_must_be")
        if must and k.get("aggregation") != must:
            out.append(Finding("patient_count_distinct", "Semantic governance", "error", False,
                               f"{k.get('field') or k.get('display_name')}: aggregation must be {must}, "
                               f"got {k.get('aggregation')}."))
    return [f.to_dict() for f in out]


def validate_change(change: dict[str, Any], project_path: Optional[str] = None) -> dict[str, Any]:
    """Validate a proposed change. Returns {ok, violations}. ok is True (clean),
    False (violations), or None (unknown change kind — nothing checked)."""
    kind = change.get("kind")
    if kind == "measure":
        violations = _check_measure(change, project_path)
    elif kind == "config":
        violations = _check_config(change)
    else:
        return {"ok": None, "violations": [], "message": f"unknown change kind: {kind!r}"}
    return {"ok": len(violations) == 0, "violations": violations}
