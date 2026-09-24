import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);ref=d/'r';rev=d/'v';plan=d/'p';out=d/'o';ref.write_text(json.dumps({'clearer':'c','uncertain':'u','evidence_that_changed_understanding':'e','intended_next_action':'REVIEW_MORE_EVIDENCE'}));rev.write_text(json.dumps({'reviews':[{'openalex_id':'W1'}]}));plan.write_text(json.dumps({'question':'q','sufficiency_criterion':'s'}));subprocess.run(['python3',str(r/'tools/build_human_learning_record.py'),'--reflection',str(ref),'--review',str(rev),'--plan',str(plan),'--out',str(out)],check=True,capture_output=True);x=json.loads(out.read_text());assert x['human_authored'] and x['evidence_trace_count']==1 and len(x['source_fingerprints'])==3 and not x['scientific_decision'] and not x['canonical_write']
print('HUMAN_LEARNING_RECORD_PASS')
