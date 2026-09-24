import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);i=d/'i';o=d/'o';i.write_text(json.dumps({'papers':[{'review_status':'CHALLENGES'},{'review_status':'UNCLEAR'}]}));subprocess.run(['python3',str(r/'tools/assess_human_sufficiency.py'),'--review',str(i),'--criterion','methods checked','--human-verdict','INSUFFICIENT','--out',str(o)],check=True,capture_output=True);x=json.loads(o.read_text());assert x['human_verdict']=='INSUFFICIENT' and x['next_action']=='CONSIDER_NEXT_TARGETED_LOOP' and x['review_counts']['CHALLENGES']==1 and not x['scientific_decision']
print('HUMAN_SUFFICIENCY_ASSESSMENT_PASS')
