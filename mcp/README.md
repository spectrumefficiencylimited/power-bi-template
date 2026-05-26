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
| `score_baseline` | planned | topology → capability baseline vs the rules |
| `validate_change` | planned | check a proposed change against the estate's rules |
| `generate_module` | planned | emit a governed module to a branch |
| `propose_remediation` | planned | candidate TMDL edits via Microsoft's local server, to a branch |

Read tools never touch files. Write tools run `validate_change` first and only
write to a branch.

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
