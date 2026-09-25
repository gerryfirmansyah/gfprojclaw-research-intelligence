from pathlib import Path
h=Path("prototype/research-workspace.html").read_text()
assert 'id="discovery-benchmark"' not in h
assert 'id="start"' not in h
assert 'Bandingkan pencarian HUMAN dengan mesin' not in h
assert 'Apa yang ingin Anda pahami?' not in h
assert 'href="#start"' not in h
assert '>Lanjutkan Research Copilot</a>' not in h
assert 'Trial aktif:' in h
print("WORKSPACE_LEGACY_ENTRY_PHYSICALLY_REMOVED_PASS")
