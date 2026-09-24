import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);i=d/'i';o=d/'o';i.write_text(json.dumps({'exact_query':'q','new_candidate_papers':[{'openalex_id':'W2','title':'B'}]}));subprocess.run(['python3',str(r/'tools/build_targeted_candidate_review.py'),'--comparison',str(i),'--out',str(o)],check=True,capture_output=True);x=json.loads(o.read_text());assert x['candidate_count']==1 and x['papers'][0]['review_status']=='NOT_REVIEWED' and x['papers'][0]['machine_classification'] is None and not x['scientific_decision']
print('TARGETED_CANDIDATE_REVIEW_PASS')
