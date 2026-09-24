from pathlib import Path
r=Path(__file__).resolve().parents[1]; e=(r/'prototype/explorer.js').read_text(); a=(r/'prototype/app.js').read_text(); h=(r/'prototype/index.html').read_text()
for x in ['supporting_papers:o.papers.map(','counter_evidence_instruction','evidence_level:"ABSTRACT_ONLY"']: assert x in e
for x in ['handoff-evidence','Baca abstract evidence','Counter-evidence protocol','Evidence ini belum canonical']: assert x in a+h
print('ADVANCED_EVIDENCE_COPILOT_HANDOFF_PASS')
