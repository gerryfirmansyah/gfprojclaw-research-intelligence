from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'prototype/app.js').read_text()
for x in ['discovery_role:"SUPPORTING_SIGNAL"','discovery_role:"CHALLENGE_CANDIDATE"','challenge candidate":"supporting signal','discovery_role:papers[i]?.discovery_role','ini bukan hasil review']: assert x in s
print('UNIFIED_HUMAN_EVIDENCE_MATRIX_PASS')
