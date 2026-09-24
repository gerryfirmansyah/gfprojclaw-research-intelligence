from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'prototype/app.js').read_text()
for x in ['Evidence contrast yang harus dijawab retrieval','question:q,evidence_contrasts:dimSummary','dimensions:r.dimensions','discovery_role:r.discovery_role']: assert x in s
print('CONTRAST_GROUNDED_RETRIEVAL_BRIEF_PASS')
