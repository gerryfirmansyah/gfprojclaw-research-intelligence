#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,time,urllib.parse,urllib.request
BASE="https://api.openalex.org/works"
def main():
 p=argparse.ArgumentParser();p.add_argument("--query",required=True);p.add_argument("--limit",type=int,default=10);p.add_argument("--timeout",type=float,default=15);a=p.parse_args()
 q=a.query.strip()
 if not q:raise SystemExit("query required")
 if not 1<=a.limit<=25 or not 1<=a.timeout<=30:raise SystemExit("bounded args violated")
 started=time.time();url=BASE+"?"+urllib.parse.urlencode({"search":q,"per-page":a.limit})
 req=urllib.request.Request(url,headers={"User-Agent":"GFPROJCLAW-Research-Explorer/0.1"})
 with urllib.request.urlopen(req,timeout=a.timeout) as r:
  raw=r.read(2_000_001)
  if len(raw)>2_000_000:raise SystemExit("response exceeds 2MB bound")
  x=json.loads(raw);rows=x.get("results");meta=x.get("meta") or {}
  if not isinstance(rows,list):raise SystemExit("malformed OpenAlex results")
  records=[{"openalex_id":z.get("id"),"doi":z.get("doi"),"title":z.get("title"),"publication_year":z.get("publication_year"),"type":z.get("type")} for z in rows[:a.limit]]
 print(json.dumps({"mode":"READ_ONLY_PREVIEW","source_key":"openalex","query_origin":"HUMAN_PROVIDED","query":q,"query_fingerprint":hashlib.sha256(q.encode()).hexdigest(),"provider_reported_total":meta.get("count"),"requested_count":a.limit,"retrieved_count":len(records),"records":records,"elapsed_ms":round((time.time()-started)*1000),"canonical_write":False,"scientific_decision":False},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
