from pathlib import Path
h=Path('prototype/explorer.html').read_text(); i=Path('prototype/index.html').read_text()
for x in ['Research Explorer','Stage 1 · Explore → Understand → Decide','Mulai dari ide riset, bukan dari kesimpulan.','Discovery bukan Evidence.','HUMAN Scope Decision','Research Copilot','NOT_RECORDED','belum menulis canonical scientific state','disabled aria-disabled="true"','Admin Copilot remains an operational plane, not a research stage']:
    assert x in h,x
assert 'href="explorer.html">← Research Explorer</a>' in i
assert 'href="index.html">Lanjutkan Research Copilot</a>' in h
print('RESEARCH_EXPLORER_ENTRY_UI_PASS')
