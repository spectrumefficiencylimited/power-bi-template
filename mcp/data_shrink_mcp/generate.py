"""generate_module — the first write tool.

Emits a governed module from a config, but only after the config passes
validate_change. Refuses (writes nothing) on any violation — the
"every write tool validates first" invariant. Mirrors the real
modules/scripts/module_generator.py output shape.

Per ADR 0003 it writes a file to the working tree (a branch); it never touches a
live workspace, and it does not commit — the PR/merge is the human gate.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from .validate import validate_change


def _build_kpi_strip(config: dict[str, Any]) -> dict[str, Any]:
    brand = (config.get("branding") or {}).get("primary_color", "#0066CC")
    return {
        "generated_from": config.get("_source", "config"),
        "module_type": "kpi_strip",
        "domain": (config.get("project") or {}).get("domain", "generic"),
        "cards": [
            {
                "field": k["field"],
                "display_name": k.get("display_name", k["field"]),
                "aggregation": k["aggregation"],   # already past the gate
                "format": k.get("format", "#,0"),
                "primary_color": brand,
            }
            for k in config.get("kpis") or []
        ],
    }


def generate_module(config: dict[str, Any], out_dir: Optional[str] = None) -> dict[str, Any]:
    """Generate a governed module from a config. Validates first; on any
    violation, writes nothing and returns the violations.

    Returns {ok, written, path?, module?, violations}.
    """
    gate = validate_change({"kind": "config", "kpis": config.get("kpis") or []})
    if gate["ok"] is False:
        return {"ok": False, "written": False, "violations": gate["violations"],
                "message": "config failed the governance gate — nothing written."}

    module = _build_kpi_strip(config)

    path = None
    if out_dir:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        path = str(out / "kpi_strip_generated.json")
        Path(path).write_text(json.dumps(module, indent=2))

    return {"ok": True, "written": bool(out_dir), "path": path, "module": module,
            "violations": []}
