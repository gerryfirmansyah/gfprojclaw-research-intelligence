#!/usr/bin/env python3
import argparse,json,re
def main():
 p=argparse.ArgumentParser();p.add_argument('--corpus',required=True);p.add_argument('--landscape',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 corpus=json.load(open(a.corpus));view=json.load(open(a.landscape));rows=corpus.get('records') or []
 traces=[]
 for area in view.get('observed_areas') or []:
  term=area['term'];members=[r for r in rows if re.search(r'(?i)(?<![a-z])'+re.escape(term)+r'(?![a-z])',r.get('title') or '')]
  traces.append({'area':term,'why_shown':area['why_shown'],'supporting_observation':{'observed_title_count':len(members)},'members':[{'title':r.get('title'),'openalex_id':r.get('openalex_id'),'doi':r.get('doi'),'source_url':r.get('source_url'),'publication_year':r.get('publication_year'),'venue':r.get('venue')} for r in members],'verification':area.get('verification'),'limitations':['Membership is based on observed title terminology only.','HUMAN must inspect abstract/method/context before scientific use.'],'status':'MACHINE_OBSERVATION'})
 out={'mode':'WHY_TO_WHAT_TRACE_TRIAL','traces':traces,'invariant':'EVERY_WHY_INSPECTABLE_BACK_TO_WHAT','canonical_write':False,'scientific_decision':False}
 json.dump(out,open(a.output,'w'),ensure_ascii=False,indent=2);print(json.dumps({'trace_count':len(traces),'member_counts':{t['area']:len(t['members']) for t in traces}},indent=2))
if __name__=='__main__':main()
