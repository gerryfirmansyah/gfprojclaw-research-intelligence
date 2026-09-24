#!/usr/bin/env python3
import argparse,json
def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 x=json.load(open(a.input));src=x.get('source') or {};land=x.get('landscape') or {};integ=x.get('integrity') or {}
 complete=src.get('complete_against_reported_total') is True
 areas=[{'term':t,'observed_count':n,'why_shown':f'Term appears in {n} titles inside this bounded corpus.','verification':{'query':src.get('query'),'provider':src.get('provider'),'time_boundary':src.get('time_boundary')},'status':'MACHINE_OBSERVATION'} for t,n in (land.get('title_terms') or [])[:20]]
 out={'mode':'RESEARCHER_VISIBLE_TRIAL_LANDSCAPE','coverage':{'provider_reported_total':src.get('provider_reported_total'),'retrieved_count':src.get('retrieved_count'),'complete':complete},'integrity':integ,'year_landscape':land.get('years') or {},'type_landscape':land.get('types') or {},'venue_landscape':land.get('top_venues') or [],'observed_areas':areas,'limitations':['Title-term frequency is a navigation signal, not a scientific topic classification.','Observed areas are not evidence, gaps, novelty, or relevance decisions.'],'human_next_actions':['inspect area members','inspect papers and abstracts','verify DOI/source','narrow scope','broaden scope','branch scope','keep current scope'],'canonical_write':False,'scientific_decision':False}
 json.dump(out,open(a.output,'w'),ensure_ascii=False,indent=2)
 print(json.dumps({'coverage':out['coverage'],'observed_area_count':len(areas),'human_next_actions':out['human_next_actions']},indent=2))
if __name__=='__main__':main()
