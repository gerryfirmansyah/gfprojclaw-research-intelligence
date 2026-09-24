from pathlib import Path
r=Path(__file__).resolve().parents[1];a=(r/'prototype/app.js').read_text();h=(r/'prototype/index.html').read_text()
assert 'handoff-next-question' in h
for x in ['Susun pertanyaan verifikasi berikutnya','Next Verification Question · HUMAN decides','human-next-question','gfprojclaw-human-next-investigation','based_on_human_review:true','bukan research question final','canonical_write:false']: assert x in a
print('HUMAN_NEXT_INVESTIGATION_PASS')
