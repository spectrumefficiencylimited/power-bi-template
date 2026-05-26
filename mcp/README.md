# Data Shrink MCP server — the Engine Runtime

An MCP **aggregator**: a server to the host (GitHub Copilot or a local model) and
a client of Microsoft's *local* Power BI MCP server. It adds the Data Shrink
intelligence — reflection, baseline scoring, governed generation — on top of
Microsoft's plumbing, operating on **PBIP files in a git branch** (never a live
workspace).

Architecture and decisions live in the TheDataShrink docs:
`docs/strategy/mcp-continuation.md`, ADR 0003 (branch-writes), ADR 0004
(host-agnostic reasoning), ADR 0005 (files-only), `.out-of-scope/0004` (local
server only).

## Tool surface (v1)

| Tool | Status | Does |
| --- | --- | --- |
| `reflect_estate` | **built** | PBIP metadata → semantic topology (read-only) |
| `score_baseline` | **built** | estate → capability baseline (per-axis 0-5 + findings) vs the rules |
| `validate_change` | **built** | check a proposed change (measure/config) against the rules — the gate write tools call first |
| `generate_module` | **built** | validate-gate, then emit a governed module to a branch (refuses on violation) |
| `propose_remediation` | **built** (fake client) | candidate TMDL edit, gated, delegated to Microsoft's local server, to a branch |

Read tools never touch files. Write tools run `validate_change` first and only
write to a branch.

> `propose_remediation` delegates the actual model write to Microsoft's *local*
> MCP server via a pluggable client (`microsoft_bridge.py`). The real stdio
> client to `microsoft/powerbi-modeling-mcp` is not wired yet; the default
> `FakeLocalServerClient` records the intended edit, so the gate, the proposal,
> and the delegation are all tested without the server connected.

## Run

```bash
cd mcp
pip install -e .
data-shrink-mcp          # serves over stdio
```

Register it with an MCP host (e.g. VS Code `mcp.json`) like any stdio server.

## Test

No MCP SDK required — the logic modules are tested directly:

```bash
python mcp/tests/test_reflect.py
```

## How it wires to the repo

`reflect_estate` reuses the real `PBIPProjectAnalyzer`
(`docs/advanced/automation-scripts/pbip_project_analyzer.py`) via
`analyzer_bridge.py` — we reflect with the same parser the automation already
uses, not a reimplementation.
