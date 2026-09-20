from pathlib import Path
s=Path('prototype/app.js').read_text()
for x in ['Observasi sumber canonical','Angka di atas adalah aggregate CoverageContext','Periksa relasi & sumber pada objek riset','Periksa evidence & sumber','Apa arti asesmen ini?','Yang perlu HUMAN periksa:','tidak membuktikan gap, novelty, signifikansi, atau penerimaan ilmiah','Detail teknis asesmen']:
    assert x in s,x
a=Path('docs/j16/screen-by-screen-human-verification-audit-2026-09-20.md').read_text()
for x in ['No scientifically meaningful machine interpretation','Research Copilot checklist','Admin Copilot checklist','Priority remediation queue']:
    assert x in a,x
print('HUMAN_VERIFICATION_SURFACE_PASS')
