#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,urllib.parse,urllib.request
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--plan',required=True);ap.add_argument('--query',required=True);ap.add_argument('--out',required=True);ap.add_argument('--max-results',type=int,default=25);a=ap.parse_args();plan=json.loads(Path(a.plan).read_text())
 if plan.get('status')!='READY_FOR_HUMAN_EXECUTION': raise SystemExit('BLOCKED: plan lacks HUMAN authorization')
 q=a.query.strip()
 if not q: raise SystemExit('BLOCKED: exact targeted query required')
 cap=max(1,min(a.max_results,100));params={'search':q,'per-page':cap,'select':'id,doi,title,publication_year,type,primary_location,abstract_inverted_index'}
 url='https://api.openalex.org/works?'+urllib.parse.urlencode(params);req=urllib.request.Request(url,headers={'User-Agent':'GFPROJCLAW-Targeted-HUMAN-Verification/0.1'})
 with urllib.request.urlopen(req,timeout=30) as r:data=json.loads(r.read())
 rows=[]
 for x in data.get('results',[]):
  rows.append({'openalex_id':x.get('id'),'doi':x.get('doi'),'title':x.get('title'),'publication_year':x.get('publication_year'),'type':x.get('type'),'source_url':x.get('id'),'abstract_available':bool(x.get('abstract_inverted_index'))})
 out={'mode':'TRIAL_TARGETED_OPENALEX_RETRIEVAL','status':'RETRIEVED_FOR_HUMAN_REVIEW','provider':'OpenAlex','exact_query':q,'provider_reported_count':data.get('meta',{}).get('count'),'retrieved_count':len(rows),'max_results':cap,'bounded':True,'question':plan.get('question'),'sufficiency_criterion':plan.get('sufficiency_criterion'),'papers':rows,'limitations':['Targeted retrieval is not a complete literature universe.','Retrieved count is not evidence of relevance, gap, novelty, or significance.','Abstract/method/full text require HUMAN verification.'],'scientific_decision':False,'canonical_write':False}
 Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'reported':out['provider_reported_count'],'retrieved':len(rows),'query':q}))
if __name__=='__main__':main()
