from pathlib import Path
a=Path("prototype/app.js").read_text(); c=Path("prototype/styles.css").read_text()
assert 'Focused Investigation: ${incoming} evidence dibawa · NON-CANONICAL' in a
assert 'Project Corpus tetap ${papers.length} persisted Works' in a
assert 'Belum ada canonical ChangeEvent dari Focused Investigation ini' in a
assert 'copilot-evidence-scroll' in a and 'copilot-evidence-table' in a
assert 'Scroll kanan–kiri di dalam frame' in a
assert '#explorer-handoff .copilot-evidence-table' in c
assert 'min-width:1500px' in c and 'overflow:auto' in c
print("COPILOT_HUMAN_UI_ACCEPTANCE_PASS")
