"""Estate-level governance rules — the checks behind the capability baseline.

These operate on the structure returned by PBIPProjectAnalyzer (metadata only).
Each rule returns a Finding. `ok` is True (pass), False (violation), or None
(insufficient signal — the estate doesn't expose enough to judge; never faked as
a pass or a fail).

Rules mirror the real validation_rules in config/examples/hospital_er.yaml and
the five axes from Episode 3 of the applied series.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any, Optional


@dataclass
class Finding:
    rule: str
    axis: str
    severity: str          # "critical" | "error" | "warning"
    ok: Optional[bool]     # True pass, False violation, None insufficient signal
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def gather_measures(structure: dict[str, Any]) -> list[dict[str, Any]]:
    """All measures, whether top-level or nested under tables."""
    sm = structure.get("semantic_model") or {}
    out: list[dict[str, Any]] = list(sm.get("measures") or [])
    for t in sm.get("tables") or []:
        out.extend(t.get("measures") or [])
    return out


def _tables(structure: dict[str, Any]) -> list[dict[str, Any]]:
    return (structure.get("semantic_model") or {}).get("tables") or []


def _expr(measure: dict[str, Any]) -> str:
    return str(measure.get("expression") or measure.get("dax") or "")


def _is_patient_count(m: dict[str, Any]) -> bool:
    name = str(m.get("name") or "")
    expr = _expr(m)
    name_hit = re.search(r"patient", name, re.I) and re.search(r"count|number|volume", name, re.I)
    expr_hit = re.search(r"patient\s*id", expr, re.I)
    return bool(name_hit or expr_hit)


# --- rules -----------------------------------------------------------------

def rule_patient_count_distinct(structure: dict[str, Any]) -> Finding:
    measures = [m for m in gather_measures(structure) if _is_patient_count(m)]
    if not measures:
        return Finding("patient_count_distinct", "Semantic governance", "error", None,
                       "No patient-count measure found to check.")
    bad = []
    for m in measures:
        e = _expr(m)
        if re.search(r"\bDISTINCTCOUNT\b", e, re.I):
            continue
        if re.search(r"\bCOUNTROWS\b|\bCOUNT\b", e, re.I):
            bad.append(m.get("name") or "(unnamed)")
    if bad:
        return Finding("patient_count_distinct", "Semantic governance", "error", False,
                       f"Patient count must use DISTINCTCOUNT; non-distinct in: {', '.join(bad)}.")
    return Finding("patient_count_distinct", "Semantic governance", "error", True,
                   "All patient-count measures use DISTINCTCOUNT.")


def rule_measure_drift(structure: dict[str, Any]) -> Finding:
    by_name: dict[str, set[str]] = {}
    for m in gather_measures(structure):
        name = re.sub(r"\s+", " ", str(m.get("name") or "")).strip().lower()
        if name:
            by_name.setdefault(name, set()).add(_expr(m).strip())
    drifted = [n for n, exprs in by_name.items() if len(exprs) > 1]
    if not by_name:
        return Finding("measure_drift", "Semantic governance", "warning", None,
                       "No measures found to check for drift.")
    if drifted:
        return Finding("measure_drift", "Semantic governance", "warning", False,
                       f"Same measure name, different definitions: {', '.join(drifted)}.")
    return Finding("measure_drift", "Semantic governance", "warning", True,
                   "No measure-name drift detected.")


def rule_require_calendar(structure: dict[str, Any]) -> Finding:
    tables = _tables(structure)
    if not tables:
        return Finding("require_calendar", "Time intelligence", "error", None,
                       "No tables found to check for a calendar.")
    has_cal = any(re.search(r"calendar|date", str(t.get("name") or ""), re.I) for t in tables)
    return Finding("require_calendar", "Time intelligence", "error", bool(has_cal),
                   "Calendar/date table present." if has_cal else "No calendar table found.")


def rule_no_datetime_joins(structure: dict[str, Any]) -> Finding:
    rels = (structure.get("semantic_model") or {}).get("relationships") or []
    if not rels:
        return Finding("no_datetime_joins", "Time intelligence", "error", None,
                       "No relationships exposed; cannot verify datetime joins.")
    bad = [r for r in rels if isinstance(r, dict) and re.search(
        r"datetime", " ".join(str(v) for v in r.values()), re.I)]
    return Finding("no_datetime_joins", "Time intelligence", "error", not bool(bad),
                   "No DateTime join keys." if not bad else f"{len(bad)} relationship(s) join on DateTime.")


def rule_rls_on_pii(structure: dict[str, Any]) -> Finding:
    # The analyzer does not currently extract RLS roles, so this is honestly
    # unverifiable from the metadata we have. Never fake a pass on a critical rule.
    return Finding("patient_details_security", "Compliance & shadow-IT", "critical", None,
                   "RLS roles not exposed by the analyzer — verify Patient Details RLS manually.")


ALL_RULES = (
    rule_patient_count_distinct,
    rule_measure_drift,
    rule_require_calendar,
    rule_no_datetime_joins,
    rule_rls_on_pii,
)


def evaluate(structure: dict[str, Any]) -> list[Finding]:
    return [rule(structure) for rule in ALL_RULES]
