#!/usr/bin/env python3
import argparse,collections,json,re
STOP={'the','and','for','with','from','this','that','using','use','into','based','study','analysis','research','artificial','intelligence','digital','government','public','services','service','of','in','on','to','a','an'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 x=json.load(open(a.input));rows=x.get('records') or []
 ids=[r.get('openalex_id') for r in rows if r.get('openalex_id')];dois=[r.get('doi') for r in rows if r.get('doi')]
 years=collections.Counter(str(r.get('publication_year') or 'UNKNOWN') for r in rows)
 types=collections.Counter(r.get('type') or 'UNKNOWN' for r in rows)
 venues=collections.Counter(r.get('venue') or 'UNKNOWN' for r in rows)
 terms=collections.Counter(w for r in rows for w in re.findall(r"[a-z][a-z-]{2,}",(r.get('title') or '').lower()) if w not in STOP)
 out={'mode':'TRIAL_NON_CANONICAL_LANDSCAPE_OBSERVATION','source':{'provider':x.get('provider'),'query':x.get('query'),'time_boundary':x.get('time_boundary'),'provider_reported_total':x.get('provider_reported_total'),'retrieved_count':len(rows),'raw_retrieved_count':x.get('raw_retrieved_count',len(rows)),'complete_against_reported_total':x.get('complete_against_reported_total')},'integrity':{'duplicate_openalex_ids':len(ids)-len(set(ids)),'duplicate_dois':len(dois)-len(set(dois)),'missing_title':sum(not r.get('title') for r in rows),'missing_doi':sum(not r.get('doi') for r in rows)},'landscape':{'years':years,'types':types,'top_venues':venues.most_common(30),'title_terms':terms.most_common(50)},'interpretation':'MACHINE_OBSERVATION_NOT_SCIENTIFIC_TRUTH','canonical_write':False,'scientific_decision':False}
 json.dump(out,open(a.output,'w'),ensure_ascii=False,indent=2)
 print(json.dumps({'records':len(rows),'integrity':out['integrity'],'years':years,'top_types':types.most_common(10)},indent=2))
if __name__=='__main__':main()
