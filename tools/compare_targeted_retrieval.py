#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path

def key(p):
 d=(p.get('doi') or '').lower().replace('https://doi.org/','').strip()
 if d:return 'doi:'+d
 oid=(p.get('openalex_id') or p.get('source_url') or '').rsplit('/',1)[-1].lower()
 if oid:return 'oa:'+oid
 return 'title:'+re.sub(r'\W+',' ',p.get('title') or '').strip().lower()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--retrieval',required=True);ap.add_argument('--baseline',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();r=json.loads(Path(a.retrieval).read_text());b=json.loads(Path(a.baseline).read_text());bp=b.get('papers',b if isinstance(b,list) else []);base={key(x) for x in bp};seen=set();new=[];over=[];dups=[]
 for p in r.get('papers',[]):
  k=key(p)
  if k in seen:dups.append(p);continue
  seen.add(k);(over if k in base else new).append(p)
 out={'mode':'TRIAL_TARGETED_RETRIEVAL_COMPARISON','exact_query':r.get('exact_query'),'baseline_count':len(bp),'retrieved_count':len(r.get('papers',[])),'overlap_count':len(over),'new_candidate_count':len(new),'within_retrieval_duplicate_count':len(dups),'overlap_papers':over,'new_candidate_papers':new,'limitations':['New candidate means not matched to this baseline by DOI/OpenAlex ID/title fallback; it does not mean novel research.','Overlap/non-overlap is not supporting or counter-evidence classification.'],'next_action':'HUMAN_REVIEW_NEW_CANDIDATES','scientific_decision':False,'canonical_write':False}
 Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['overlap_count','new_candidate_count','within_retrieval_duplicate_count']}))
if __name__=='__main__':main()
