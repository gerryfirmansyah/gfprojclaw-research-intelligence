#!/usr/bin/env python3
import argparse,json,time,random,urllib.error,urllib.parse,urllib.request
def main():
 p=argparse.ArgumentParser();p.add_argument("--query",required=True);p.add_argument("--from-year",type=int,required=True);p.add_argument("--to-year",type=int,required=True);p.add_argument("--output",required=True);p.add_argument("--per-page",type=int,default=200);p.add_argument("--mailto");p.add_argument("--api-key");p.add_argument("--checkpoint");p.add_argument("--max-retries",type=int,default=8);p.add_argument("--delay",type=float,default=0.15);a=p.parse_args()
 if not 1<=a.per_page<=200:raise SystemExit("per-page 1..200")
 if a.to_year<a.from_year:raise SystemExit("to-year must be >= from-year")
 filt=f"from_publication_date:{a.from_year}-01-01,to_publication_date:{a.to_year}-12-31"
 cursor="*"; rows=[]; pages=0; reported=None
 if a.checkpoint:
  try:
   c=json.load(open(a.checkpoint))
   if c.get("query")!=a.query or c.get("time_boundary")!={"from_year":a.from_year,"to_year":a.to_year}:raise SystemExit("checkpoint scope mismatch")
   rows=c.get("records") or [];pages=c.get("pages") or 0;reported=c.get("provider_reported_total");cursor=c.get("next_cursor")
   if cursor is None:raise SystemExit("checkpoint already complete")
   print(f"resume checkpoint pages={pages} records={len(rows)}",flush=True)
  except FileNotFoundError:pass
 while cursor:
  u="https://api.openalex.org/works?"+urllib.parse.urlencode({**{"search":a.query,"filter":filt,"per-page":a.per_page,"cursor":cursor},**({"mailto":a.mailto} if a.mailto else {}),**({"api_key":a.api_key} if a.api_key else {})})
  req=urllib.request.Request(u,headers={"User-Agent":("GFPROJCLAW-Research-Value-Trial/0.2"+(f" (mailto:{a.mailto})" if a.mailto else ""))})
  attempt=0
  while True:
   try:
    with urllib.request.urlopen(req,timeout=30) as r:x=json.loads(r.read())
    break
   except urllib.error.HTTPError as e:
    if e.code not in (429,500,502,503,504):raise
    attempt+=1
    if e.code!=429 and attempt>a.max_retries:raise
    retry=e.headers.get("Retry-After")
    wait=float(retry) if retry and retry.isdigit() else min(60.0,2**min(attempt-1,6)+random.random())
    print(f"retry page={pages+1} attempt={attempt} status={e.code} wait={wait:.1f}s",flush=True);time.sleep(wait)
  time.sleep(a.delay)
  if reported is None:reported=(x.get("meta") or {}).get("count")
  batch=x.get("results") or []; pages+=1
  for z in batch:
   loc=z.get("primary_location") or {}; src=loc.get("source") or {}
   rows.append({"openalex_id":z.get("id"),"doi":z.get("doi"),"title":z.get("title"),"publication_year":z.get("publication_year"),"type":z.get("type"),"cited_by_count":z.get("cited_by_count"),"venue":src.get("display_name"),"source_url":z.get("id"),"doi_url":z.get("doi"),"is_oa":(z.get("open_access") or {}).get("is_oa")})
  cursor=(x.get("meta") or {}).get("next_cursor") if batch else None
  if a.checkpoint:
   json.dump({"provider":"openalex","query":a.query,"time_boundary":{"from_year":a.from_year,"to_year":a.to_year},"provider_reported_total":reported,"retrieved_count":len(rows),"pages":pages,"next_cursor":cursor,"records":rows,"canonical_write":False},open(a.checkpoint,"w"),ensure_ascii=False)
  if not batch:break
 out={"mode":"TRIAL_NON_CANONICAL_WHOLE_BOUNDED_METADATA","provider":"openalex","query":a.query,"time_boundary":{"from_year":a.from_year,"to_year":a.to_year},"provider_reported_total":reported,"retrieved_count":len(rows),"pages":pages,"complete_against_reported_total":len(rows)==reported,"records":rows,"canonical_write":False,"scientific_decision":False}
 open(a.output,"w").write(json.dumps(out,ensure_ascii=False,indent=2))
 print(json.dumps({k:out[k] for k in ["mode","provider","query","time_boundary","provider_reported_total","retrieved_count","pages","complete_against_reported_total"]},indent=2))
if __name__=="__main__":main()
