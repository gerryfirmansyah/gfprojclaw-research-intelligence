import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);i=d/'i';o=d/'o';i.write_text(json.dumps({'interpretation':'DESCRIPTIVE_ONLY','guardrails':['A changed reflection is not evidence of improvement.','System must not score researcher competence.'],'scientific_decision':False,'canonical_write':False}));subprocess.run(['python3',str(r/'tools/audit_human_agency_boundaries.py'),'--delta',str(i),'--out',str(o)],check=True,capture_output=True);x=json.loads(o.read_text());assert x['pass'] and len(x['checks'])==5 and 'may not turn them into a score' in x['principle']
print('HUMAN_AGENCY_BOUNDARY_AUDIT_PASS')
