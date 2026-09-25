from pathlib import Path
a=Path("prototype/app.js").read_text()
for label in ["IO aktif","Evidence set aktif","Current investigation context","Review aktif","Cakupan investigasi aktif","Konteks sesi aktif","Belum diproyeksikan ke Radar"]: assert label in a,label
assert 'function focusedHandoffState()' in a
assert 'function focusedEvidenceTable()' in a
print("COPILOT_IO_CONTEXT_ACROSS_MENUS_PASS")
