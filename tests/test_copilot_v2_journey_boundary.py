from pathlib import Path
s=Path("prototype/research-copilot-v2.js").read_text()
for x in ["RESEARCH WORKSPACE","RESEARCH COPILOT v2","W8","C8","Research Reasoning Package","journey:renderJourney"]: assert x in s
assert "Validated gap, novelty, Research Question" in s
print("COPILOT_V2_JOURNEY_BOUNDARY_PASS")
