import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);i=d/'i';o=d/'o';i.write_text(json.dumps({'human_verdict':'INSUFFICIENT'}));subprocess.run(['python3',str(r/'tools/build_human_decision_checkpoint.py'),'--assessment',str(i),'--human-action','AUTHORIZE_NEXT_LOOP','--human-rationale','Need context evidence','--out',str(o)],check=True,capture_output=True);x=json.loads(o.read_text());assert x['status']=='AUTHORIZED_HUMAN_ACTION' and x['next_loop_authorized'] and not x['scientific_decision'];i.write_text(json.dumps({'human_verdict':'SUFFICIENT'}));subprocess.run(['python3',str(r/'tools/build_human_decision_checkpoint.py'),'--assessment',str(i),'--human-action','AUTHORIZE_NEXT_LOOP','--human-rationale','x','--out',str(o)],check=True,capture_output=True);assert json.loads(o.read_text())['status']=='BLOCKED_ACTION_MISMATCH'
print('HUMAN_DECISION_CHECKPOINT_PASS')
