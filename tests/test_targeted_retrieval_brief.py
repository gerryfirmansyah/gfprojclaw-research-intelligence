from pathlib import Path
r=Path(__file__).resolve().parents[1];a=(r/'prototype/app.js').read_text();h=(r/'prototype/index.html').read_text()
assert 'handoff-retrieval-brief' in h
for x in ['Targeted Retrieval Brief · PRE-EXECUTION','NO EXPANSION AUTHORIZED','gfprojclaw-targeted-retrieval-brief','"OpenAlex":"NOT_SELECTED"','exactQuery?exactQuery:"NOT_EXECUTED"','Brief ini belum menjalankan pencarian']: assert x in a
print('TARGETED_RETRIEVAL_BRIEF_PASS')
