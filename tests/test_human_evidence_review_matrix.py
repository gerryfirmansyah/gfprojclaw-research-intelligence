from pathlib import Path
r=Path(__file__).resolve().parents[1]; a=(r/'prototype/app.js').read_text(); h=(r/'prototype/index.html').read_text()
for x in ['handoff-evidence-matrix','handoff-human-verdict']: assert x in h
for x in ['Evidence Review Matrix · HUMAN','SUPPORTS','CHALLENGES','UNCLEAR','HUMAN Evidence Balance','Evidence balance bukan truth probability','gfprojclaw-human-evidence-review','canonical_write:false']: assert x in a
print('HUMAN_EVIDENCE_REVIEW_MATRIX_PASS')
