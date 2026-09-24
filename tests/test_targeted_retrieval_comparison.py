import json,subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
 d=Path(d);base=d/'b.json';ret=d/'r.json';out=d/'o.json';base.write_text(json.dumps({'papers':[{'openalex_id':'https://openalex.org/W1','doi':'https://doi.org/10.1/a','title':'A'}]}));ret.write_text(json.dumps({'exact_query':'q','papers':[{'openalex_id':'https://openalex.org/W1','doi':'https://doi.org/10.1/a','title':'A'},{'openalex_id':'https://openalex.org/W2','title':'B'}]}));subprocess.run(['python3',str(r/'tools/compare_targeted_retrieval.py'),'--retrieval',str(ret),'--baseline',str(base),'--out',str(out)],check=True);x=json.loads(out.read_text());assert x['overlap_count']==1 and x['new_candidate_count']==1 and x['next_action']=='HUMAN_REVIEW_NEW_CANDIDATES' and not x['scientific_decision']
print('TARGETED_RETRIEVAL_COMPARISON_PASS')
