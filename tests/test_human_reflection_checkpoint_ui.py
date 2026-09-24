from pathlib import Path
r=Path(__file__).resolve().parents[1];h=(r/'prototype/index.html').read_text();a=(r/'prototype/app.js').read_text()
assert 'handoff-reflection' in h
for x in ['HUMAN Reflection Checkpoint','Apa yang sekarang lebih jelas?','Apa yang masih belum pasti?','Evidence apa yang paling mengubah pemahaman Anda?','gfprojclaw-human-reflection','HUMAN AUTHORED','scientific_decision:false','canonical_write:false']:assert x in a
print('HUMAN_REFLECTION_CHECKPOINT_UI_PASS')
