import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 b=Path(d)/'b.json';o=Path(d)/'o.json';b.write_text(json.dumps({'opportunity':'ADV-A','question':'q','sufficiency_criterion':'s','human_context':'Indonesia','unresolved_titles':['x'],'expansion_authorized':True}));subprocess.run(['python3',str(r/'tools/build_targeted_retrieval_plan.py'),'--brief',str(b),'--out',str(o)],check=True,capture_output=True,text=True);x=json.loads(o.read_text());assert x['status']=='READY_FOR_HUMAN_EXECUTION' and x['provider']=='OpenAlex' and not x['scientific_decision'] and not x['canonical_write'];b.write_text(json.dumps({'expansion_authorized':False}));subprocess.run(['python3',str(r/'tools/build_targeted_retrieval_plan.py'),'--brief',str(b),'--out',str(o)],check=True,capture_output=True,text=True);x=json.loads(o.read_text());assert x['status']=='BLOCKED_NO_HUMAN_AUTHORIZATION' and x['provider']=='NOT_SELECTED'
print('TARGETED_RETRIEVAL_PLAN_PASS')
