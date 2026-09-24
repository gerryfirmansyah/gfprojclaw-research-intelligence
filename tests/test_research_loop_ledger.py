import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);p=d/'p';o=d/'o';p.write_text(json.dumps({'mode':'TRIAL_TARGETED_RETRIEVAL_PLAN','status':'READY','scientific_decision':False,'canonical_write':False}));subprocess.run(['python3',str(r/'tools/build_research_loop_ledger.py'),'--plan',str(p),'--out',str(o)],check=True,capture_output=True);x=json.loads(o.read_text());assert x['stage_count']==1 and x['trace_complete'] and len(x['stages'][0]['sha256'])==64 and not x['scientific_decision']
print('RESEARCH_LOOP_LEDGER_PASS')
