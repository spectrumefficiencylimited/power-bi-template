"""The Data Shrink MCP server — the Engine Runtime.

An MCP aggregator: a server to the host (Copilot or a local model) and a client
of Microsoft's local Power BI MCP server. It adds the Data Shrink intelligence —
reflection, baseline scoring, governed generation — on top of Microsoft's
plumbing.

Tool surface (v1): reflect_estate, score_baseline, validate_change,
generate_module, propose_remediation. Read tools never touch files; write tools
run validate_change first and only write to a git branch.

See ../../docs/strategy/mcp-continuation.md in the TheDataShrink docs for the
architecture and ADRs 0003–0005.
"""

__version__ = "0.0.1"
