from pathlib import Path
s=Path("docs/j16/research-value-trial-map-v0.md").read_text()
for x in ["HUMAN Research Augmentation System","Reduce the universe by explicit research boundaries","top-N provider result","2022–2026","NOT INCLUDED IN CURRENT EXPLORATION WINDOW","scientifically correct"]: assert x in s,x
print("RESEARCH_VALUE_TRIAL_MAP_PASS")
