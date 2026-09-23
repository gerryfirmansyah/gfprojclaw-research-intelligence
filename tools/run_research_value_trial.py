#!/usr/bin/env python3
import argparse,hashlib,json,time,urllib.parse,urllib.request
def fetch(url,ua):
 req=urllib.request.Request(url,headers={"User-Agent":ua})
 with urllib.request.urlopen(req,timeout=25) as r:return json.loads(r.read())
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--query",required=True);ap.add_argument("--limit",type=int,default=100);ap.add_argument("--output",required=True);a=ap.parse_args()
 if not 1<=a.limit<=200:raise SystemExit("limit 1..200")
 q=a.query.strip(); started=time.time()
 ox=fetch("https://api.openalex.org/works?"+urllib.parse.urlencode({"search":q,"per-page":a.limit}),"GFPROJCLAW-Research-Value-Trial/0.1")
 cx=fetch("https://api.crossref.org/works?"+urllib.parse.urlencode({"query.bibliographic":q,"rows":a.limit}),"GFPROJCLAW-Research-Value-Trial/0.1")
 o=[{"provider":"openalex","provider_id":z.get("id"),"doi":(z.get("doi") or "").lower().removeprefix("https://doi.org/") or None,"title":z.get("title"),"year":z.get("publication_year"),"venue":((z.get("primary_location") or {}).get("source") or {}).get("display_name"),"source_url":z.get("id"),"doi_url":z.get("doi")} for z in ox.get("results",[])]
 c=[]
 for z in (cx.get("message") or {}).get("items",[]):
  doi=(z.get("DOI") or "").lower() or None
  c.append({"provider":"crossref","provider_id":doi,"doi":doi,"title":(z.get("title") or [None])[0],"year":(((z.get("published") or {}).get("date-parts") or [[None]])[0][0]),"venue":(z.get("container-title") or [None])[0],"source_url":z.get("URL"),"doi_url":("https://doi.org/"+doi) if doi else None})
 by={}
 for z in o+c:
  key=("doi:"+z["doi"]) if z["doi"] else "title:"+(" ".join((z["title"] or "").lower().split()))
  by.setdefault(key,[]).append(z)
 members=[{"key":k,"providers":sorted({x["provider"] for x in v}),"record":v[0]} for k,v in by.items()]
 out={"mode":"TRIAL_NON_CANONICAL","query":q,"query_fingerprint":hashlib.sha256(q.encode()).hexdigest(),"retrieved_at_epoch":time.time(),"providers":{"openalex":{"provider_reported_total":(ox.get("meta") or {}).get("count"),"retrieved":len(o)},"crossref":{"provider_reported_total":(cx.get("message") or {}).get("total-results"),"retrieved":len(c)}},"retrieved_records":len(o)+len(c),"unique_members":len(members),"overlap_members":sum(len(x["providers"])>1 for x in members),"members":members,"canonical_write":False,"scientific_decision":False,"elapsed_ms":round((time.time()-started)*1000)}
 open(a.output,"w").write(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({k:out[k] for k in ["mode","query","providers","retrieved_records","unique_members","overlap_members"]},indent=2))
if __name__=="__main__":main()
