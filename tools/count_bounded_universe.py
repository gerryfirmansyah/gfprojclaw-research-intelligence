#!/usr/bin/env python3
import argparse,json,urllib.parse,urllib.request
def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":"GFPROJCLAW-Research-Value-Trial/0.1"})
 with urllib.request.urlopen(req,timeout=25) as r:return json.loads(r.read())
def main():
 p=argparse.ArgumentParser();p.add_argument("--query",required=True);p.add_argument("--from-year",type=int,required=True);p.add_argument("--to-year",type=int,required=True);a=p.parse_args()
 if not 1900<=a.from_year<=a.to_year<=2100:raise SystemExit("invalid year window")
 q=a.query.strip()
 oa=get("https://api.openalex.org/works?"+urllib.parse.urlencode({"search":q,"filter":f"from_publication_date:{a.from_year}-01-01,to_publication_date:{a.to_year}-12-31","per-page":1}))
 cr=get("https://api.crossref.org/works?"+urllib.parse.urlencode({"query.bibliographic":q,"filter":f"from-pub-date:{a.from_year}-01-01,until-pub-date:{a.to_year}-12-31","rows":0}))
 print(json.dumps({"mode":"TRIAL_COUNT_ONLY","query":q,"time_boundary":{"from_year":a.from_year,"to_year":a.to_year},"counts":{"openalex":(oa.get("meta") or {}).get("count"),"crossref":(cr.get("message") or {}).get("total-results")},"records_retrieved_for_landscape":0,"ranking_used_for_landscape":False,"canonical_write":False,"scientific_decision":False},ensure_ascii=False))
if __name__=="__main__":main()
