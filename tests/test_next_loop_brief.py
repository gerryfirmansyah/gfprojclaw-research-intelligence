import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);c=d/'c';p=d/'p';o=d/'o';c.write_text(json.dumps({'next_loop_authorized':True,'human_rationale':'Need more'}));p.write_text(json.dumps({'question':'old','sufficiency_criterion':'crit'}));subprocess.run(['python3',str(r/'tools/build_next_loop_brief.py'),'--checkpoint',str(c),'--previous-plan',str(p),'--new-question','new human question','--out',str(o)],check=True,capture_output=True);x=json.loads(o.read_text());assert x['loop_scope']=='ONE_TARGETED_LOOP' and x['exact_query']=='NOT_EXECUTED' and x['human_next_question']=='new human question' and not x['scientific_decision']
print('NEXT_LOOP_BRIEF_PASS')
