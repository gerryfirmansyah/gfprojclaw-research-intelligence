from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'prototype/app.js').read_text()
for x in ['Evidence contrast yang memicu investigasi','evidence_contrasts:dimSummary,sufficiency_criterion','question:q,evidence_contrasts:dimSummary']: assert x in s
print('EVIDENCE_CONTRAST_INVESTIGATION_PLAN_PASS')
