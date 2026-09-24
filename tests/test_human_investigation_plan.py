from pathlib import Path
r=Path(__file__).resolve().parents[1];a=(r/'prototype/app.js').read_text();h=(r/'prototype/index.html').read_text()
assert 'handoff-investigation-plan' in h
for x in ['Investigation Plan · DRAFT untuk HUMAN','Kriteria cukup menurut HUMAN','gfprojclaw-human-investigation-plan','review challenging/unclear evidence','expand retrieval only if needed','return to HUMAN decision','tidak menulis ke canonical project state']: assert x in a
print('HUMAN_INVESTIGATION_PLAN_PASS')
