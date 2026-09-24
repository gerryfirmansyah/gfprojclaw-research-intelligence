#!/usr/bin/env python3
import argparse,json
def main():
 p=argparse.ArgumentParser();p.add_argument('--corpus',required=True);p.add_argument('--why',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 corpus=json.load(open(a.corpus));why=json.load(open(a.why));reasons={}
 for t in why.get('traces') or []:
  for m in t.get('members') or []:
   reasons.setdefault(m.get('openalex_id'),[]).append({'area':t.get('area'),'why_shown':t.get('why_shown')})
 papers=[]
 for r in corpus.get('records') or []:
  papers.append({'openalex_id':r.get('openalex_id'),'title':r.get('title'),'publication_year':r.get('publication_year'),'venue':r.get('venue'),'type':r.get('type'),'doi':r.get('doi'),'doi_url':r.get('doi_url'),'source_url':r.get('source_url'),'is_oa':r.get('is_oa'),'why_shown':reasons.get(r.get('openalex_id'),[]),'abstract_state':'NOT_RETRIEVED_IN_THIS_TRIAL','full_text_state':'NOT_CHECKED','provenance':{'provider':corpus.get('provider'),'query':corpus.get('query'),'time_boundary':corpus.get('time_boundary')},'human_action':'INSPECT_BEFORE_SCIENTIFIC_USE'})
 out={'mode':'HUMAN_PAPER_INSPECTOR_PAYLOAD_TRIAL','paper_count':len(papers),'papers':papers,'limitations':['Abstracts were not retrieved in the bounded metadata pass.','Full text availability was not checked.','WHY signals are title-term observations only.'],'canonical_write':False,'scientific_decision':False}
 json.dump(out,open(a.output,'w'),ensure_ascii=False,indent=2);print(json.dumps({'paper_count':len(papers),'with_why':sum(bool(p['why_shown']) for p in papers),'with_doi':sum(bool(p['doi']) for p in papers)},indent=2))
if __name__=='__main__':main()
