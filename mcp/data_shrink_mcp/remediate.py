"""propose_remediation — the second write tool.

Turns a finding into a candidate model edit, validates it through the gate, and
delegates the actual TMDL write to Microsoft's local server (via a pluggable
client). Gate-first like generate_module; refuses to apply an edit that doesn't
itself pass the rules.

v1 handles the patient_count_distinct remediation (rewrite COUNT/COUNTROWS to
DISTINCTCOUNT). Other findings return a described proposal without an automatic
edit.
"""
from __future__ import annotations

import re
from typing import Any, Optional

from .microsoft_bridge import FakeLocalServerClient, LocalServerClient
from .validate import validate_change

# Pull the column reference out of a COUNT/COUNTROWS(...) expression.
_COL = re.compile(r"\b(?:DISTINCTCOUNT|COUNTROWS|COUNT)\s*\(\s*(.+?)\s*\)", re.I | re.S)


def _distinctify(expression: str) -> Optional[str]:
    m = _COL.search(expression or "")
    if not m:
        return None
    return f"DISTINCTCOUNT({m.group(1).strip()})"


def propose_remediation(
    finding: dict[str, Any],
    measure: Optional[dict[str, Any]] = None,
    client: Optional[LocalServerClient] = None,
    apply: bool = False,
) -> dict[str, Any]:
    """Propose a candidate edit for a finding.

    Args:
        finding: {"rule": ...} — the rule to remediate.
        measure: the offending measure {"name", "expression"} (the target).
        client: local-server client; defaults to a Fake that records the edit.
        apply: if True, delegate the edit to the client (a branch write); else
            dry-run and return the proposal only.

    Returns {ok, proposal?, applied, violations}.
    """
    rule = finding.get("rule")
    client = client or FakeLocalServerClient()

    if rule != "patient_count_distinct":
        return {"ok": None, "applied": False, "violations": [],
                "message": f"No automatic remediation for rule {rule!r}; describe manually."}
    if not measure:
        return {"ok": None, "applied": False, "violations": [],
                "message": "patient_count_distinct remediation needs the target measure."}

    new_expr = _distinctify(measure.get("expression", ""))
    if not new_expr:
        return {"ok": None, "applied": False, "violations": [],
                "message": "Could not parse the count expression to rewrite."}

    proposal = {"name": measure.get("name"), "expression": new_expr}

    # Gate the *proposed* edit before doing anything.
    gate = validate_change({"kind": "measure", **proposal})
    if gate["ok"] is False:
        return {"ok": False, "applied": False, "violations": gate["violations"],
                "message": "proposed edit failed the gate — not applied."}

    applied = False
    result = None
    if apply:
        result = client.apply_tmdl({"op": "rewrite_measure", **proposal})
        applied = True

    return {"ok": True, "applied": applied, "proposal": proposal,
            "apply_result": result, "violations": []}
