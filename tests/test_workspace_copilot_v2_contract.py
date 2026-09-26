from pathlib import Path
w=Path("prototype/research-workspace.js").read_text(); v=Path("prototype/research-copilot-v2.js").read_text(); h=Path("prototype/research-copilot-v2.html").read_text(); d=Path("docs/j16/research-workspace-to-copilot-v2-contract.md").read_text()
assert "research-copilot-v2.html?from=workspace&view=handoff" in w
for x in ["evidence_balance","analysis_dimensions","compare_dimensions","uncertainty"]: assert x in w
assert "research-copilot-v2.js?v=0.1.0" in h
assert "RESEARCH COPILOT v2 · ACTIVE REASONING SESSION" in v
assert "PINNED design decision" in d and "must not merge legacy" in d
print("WORKSPACE_COPILOT_V2_CONTRACT_PASS")
