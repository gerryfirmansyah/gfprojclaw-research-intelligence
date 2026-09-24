#!/usr/bin/env python3
import argparse,json
def normdoi(x):return (x or '').lower().removeprefix('https://doi.org/').strip() or None
def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args();x=json.load(open(a.input));rows=x.get('records') or []
 seen_id=set();doi_groups={};unique=[];duplicates=[]
 for r in rows:
  oid=r.get('openalex_id');doi=normdoi(r.get('doi'))
  if oid in seen_id:duplicates.append({'reason':'OPENALEX_ID','record':r});continue
  seen_id.add(oid)
  if doi and doi in doi_groups:
   duplicates.append({'reason':'DOI','canonical_openalex_id':doi_groups[doi].get('openalex_id'),'record':r});continue
  unique.append(r)
  if doi:doi_groups[doi]=r
 out={k:v for k,v in x.items() if k!='records'};out.update({'mode':'TRIAL_NON_CANONICAL_DEDUPLICATED_BOUNDED_METADATA','raw_retrieved_count':len(rows),'deduplicated_count':len(unique),'duplicate_record_count':len(duplicates),'deduplication_rules':['exact OpenAlex ID','normalized exact DOI'],'records':unique,'duplicates':duplicates,'canonical_write':False,'scientific_decision':False})
 json.dump(out,open(a.output,'w'),ensure_ascii=False,indent=2);print(json.dumps({k:out[k] for k in ['raw_retrieved_count','deduplicated_count','duplicate_record_count']},indent=2))
if __name__=='__main__':main()
