"""score_baseline — the capability baseline as code (Episode 3).

Runs the estate-level rules and aggregates findings into per-axis scores (0–5)
plus an overall. An axis with no judgeable signal is reported `null`, not a
fabricated number. Read-only.
"""
from __future__ import annotations

from typing import Any, Optional

from .analyzer_bridge import analyze
from .rules import Finding, evaluate

_PENALTY = {"critical": 3.0, "error": 2.0, "warning": 1.0}


def _score_axis(findings: list[Finding]) -> Optional[float]:
    """5.0 minus weighted violations; None if no finding had judgeable signal."""
    judged = [f for f in findings if f.ok is not None]
    if not judged:
        return None
    score = 5.0
    for f in judged:
        if f.ok is False:
            score -= _PENALTY.get(f.severity, 1.0)
    return max(0.0, round(score, 1))


def score_baseline(project_path: str) -> dict[str, Any]:
    """Score a PBIP estate against the governance rules. Returns axes, overall,
    and the full findings list (each tagged with its rule and severity)."""
    structure = analyze(project_path)
    findings = evaluate(structure)

    axes: dict[str, dict[str, Any]] = {}
    for f in findings:
        axes.setdefault(f.axis, {"findings": []})["findings"].append(f.to_dict())
    for axis, data in axes.items():
        fs = [Finding(**{k: v for k, v in d.items()}) for d in data["findings"]]
        data["score"] = _score_axis(fs)

    scored = [d["score"] for d in axes.values() if d["score"] is not None]
    overall = round(sum(scored) / len(scored), 1) if scored else None

    return {
        "estate": structure.get("project_name") or project_path,
        "overall": overall,
        "axes": axes,
        "findings": [f.to_dict() for f in findings],
        "note": "Axes with no judgeable signal are null, not zero. Metadata only.",
    }
