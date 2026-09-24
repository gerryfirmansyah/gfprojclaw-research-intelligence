import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);i=d/'i';o=d/'o';i.write_text(json.dumps({'trace_complete':True,'canonical_write':False,'stages':[{'mode':'X','sha256':'a'*64,'scientific_decision':False,'canonical_write':False}]}));z=subprocess.run(['python3',str(r/'tools/audit_closed_research_loop.py'),'--ledger',str(i),'--out',str(o)],check=True,capture_output=True,text=True);x=json.loads(o.read_text());assert x['pass'] and len(x['checks'])==5 and not x['scientific_decision'];assert 'CLOSED_RESEARCH_LOOP_AUDIT_PASS' in z.stdout
print('CLOSED_RESEARCH_LOOP_AUDIT_PASS')
