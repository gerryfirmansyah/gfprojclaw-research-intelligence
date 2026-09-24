from pathlib import Path
r=Path(__file__).resolve().parents[1];h=(r/'prototype/index.html').read_text();a=(r/'prototype/app.js').read_text()
assert 'handoff-reasoning-trace' in h
for x in ['Bagaimana saya sampai di sini? · HUMAN Reasoning Trace','gfprojclaw-human-evidence-review','gfprojclaw-human-investigation-plan','gfprojclaw-progressive-execution','gfprojclaw-targeted-retrieval-brief','NON-CANONICAL · scientific_decision=false','renderHumanReasoningTrace()']:assert x in a
print('HUMAN_REASONING_TRACE_UI_PASS')
