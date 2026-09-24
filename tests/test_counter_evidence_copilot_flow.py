from pathlib import Path
r=Path(__file__).resolve().parents[1];s=(r/'prototype/app.js').read_text()
for x in ['o.counter_evidence_candidates?.length','Counter-evidence candidates · HUMAN challenge','belum otomatis menantang opportunity','Baca abstract challenge']:assert x in s
print('COUNTER_EVIDENCE_COPILOT_FLOW_PASS')
