from pathlib import Path
r=Path(__file__).resolve().parents[1];s=(r/'prototype/explorer.js').read_text()
for x in ['counterCandidates:available.filter','counter_evidence_candidates:o.counterCandidates.map','Counter-evidence candidates (','Baca abstract untuk challenge','ketidakcocokan keyword bukan counter-evidence']:assert x in s
print('ADVANCED_COUNTER_EVIDENCE_FLOW_PASS')
