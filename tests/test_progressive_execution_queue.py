from pathlib import Path
r=Path(__file__).resolve().parents[1];a=(r/'prototype/app.js').read_text();h=(r/'prototype/index.html').read_text()
assert 'handoff-execution' in h
for x in ['Progressive Execution Queue · HUMAN controlled','allow-expand-retrieval','gfprojclaw-progressive-execution','REVIEW_PRIORITY_PAPERS','PREPARE_TARGETED_RETRIEVAL','RETURN_TO_HUMAN','Tidak ada retrieval tambahan sampai HUMAN mengizinkan','allow_expand_retrieval:allow']: assert x in a
print('PROGRESSIVE_EXECUTION_QUEUE_PASS')
