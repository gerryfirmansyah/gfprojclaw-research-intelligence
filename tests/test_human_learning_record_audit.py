import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);i=d/'i';o=d/'o';i.write_text(json.dumps({'human_authored':True,'clearer':'x','source_fingerprints':{'reflection':'a'*64,'review':'b'*64,'plan':'c'*64},'scientific_decision':False,'canonical_write':False}));z=subprocess.run(['python3',str(r/'tools/audit_human_learning_record.py'),'--record',str(i),'--out',str(o)],check=True,capture_output=True,text=True);x=json.loads(o.read_text());assert x['pass'] and len(x['checks'])==5 and 'does not score learning quality' in x['warning'];assert 'AUDIT_PASS' in z.stdout
print('HUMAN_LEARNING_RECORD_AUDIT_PASS')
