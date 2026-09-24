import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);b=d/'b';a=d/'a';o=d/'o';b.write_text(json.dumps({'clearer':'x','reviewed_evidence_ids':['W1']}));a.write_text(json.dumps({'clearer':'y','reviewed_evidence_ids':['W1','W2']}));subprocess.run(['python3',str(r/'tools/compare_human_learning_records.py'),'--before',str(b),'--after',str(a),'--out',str(o)],check=True,capture_output=True);x=json.loads(o.read_text());assert x['changed_field_count']==1 and x['newly_reviewed_evidence_ids']==['W2'] and x['interpretation']=='DESCRIPTIVE_ONLY' and not x['scientific_decision']
print('HUMAN_LEARNING_DELTA_PASS')
