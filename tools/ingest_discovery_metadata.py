#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"prototype"/"api"))
ALLOWED={"openalex","crossref"}
def parse_args():
 p=argparse.ArgumentParser();p.add_argument("--envelope",type=Path,required=True);p.add_argument("--retrieved-at",required=True);p.add_argument("--apply",action="store_true");return p.parse_args()
def load_envelope(path):
 x=json.loads(path.read_text()); src=x.get("source_key"); pid=x.get("project_id"); vid=x.get("project_version_id"); rows=x.get("records")
 if src not in ALLOWED or not pid or not vid or not isinstance(rows,list) or not 1<=len(rows)<=25 or x.get("status")=="FAILED": raise SystemExit("fail closed: invalid discovery envelope")
 return x
def normalize_doi(v):
 if not v:return None
 v=v.strip().lower()
 for p in ("https://doi.org/","http://doi.org/","doi:"):
  if v.startswith(p):v=v[len(p):]
 return v
def openalex_id(v): return v.rsplit("/",1)[-1].strip() if v else None
def assert_boundary(c):
 r=c.execute("SELECT session_user,current_user,has_table_privilege(current_user,'source_record','INSERT') AS can_source_insert,has_table_privilege(current_user,'human_decision','INSERT') AS can_human_insert,has_table_privilege(current_user,'literature_source','INSERT') AS can_registry_insert").fetchone()
 if r["session_user"]!="gfproj_pilot_executor" or r["current_user"]!="gfproj_pilot_metadata_ingestor" or not r["can_source_insert"] or r["can_human_insert"] or r["can_registry_insert"]: raise SystemExit("metadata database authority boundary check failed")
def validate_context(c,x):
 r=c.execute("SELECT p.current_version_id::text FROM research_project p JOIN literature_source s ON s.source_key=%s AND s.active WHERE p.id=%s AND p.status='ACTIVE'",(x["source_key"],x["project_id"])).fetchone()
 if not r or r[0]!=x["project_version_id"]: raise SystemExit("fail closed: stale project version or inactive provider/project")
def title(r): return (r.get("title") or "").strip()
def dates(r):
 if r.get("publication_date"): return r.get("publication_date"),r.get("publication_year")
 parts=((r.get("published") or {}).get("date-parts") or [[None]])[0]; y=parts[0] if parts else None; return None,y
def identifiers(src,r):
 out=[]
 if src=="openalex" and openalex_id(r.get("openalex_id")):out.append(("OPENALEX",openalex_id(r["openalex_id"]),True))
 d=normalize_doi(r.get("doi"));
 if d:out.append(("DOI",d,src=="crossref"))
 return out
def source_identifier(src,r):
 ids=identifiers(src,r); return next((v for t,v,_ in ids if t==("OPENALEX" if src=="openalex" else "DOI")),None)
def find_work(c,ids):
 found=set()
 for t,v,_ in ids:
  z=c.execute("SELECT work_id::text FROM work_identifier WHERE identifier_type=%s AND identifier_value=%s",(t,v)).fetchone()
  if z:found.add(z[0])
 if len(found)>1:raise SystemExit("identifier collision")
 return next(iter(found),None)
def ingest(c,x,retrieved):
 sid=c.execute("SELECT id::text FROM literature_source WHERE source_key=%s AND active",(x["source_key"],)).fetchone()[0]; out=[]
 for r in x["records"]:
  ids=identifiers(x["source_key"],r); ident=source_identifier(x["source_key"],r)
  if not ident or not title(r) or not ids: raise SystemExit("fail closed: malformed provider record")
  sr=c.execute("SELECT id::text FROM source_record WHERE literature_source_id=%s AND source_record_identifier=%s AND retrieved_at=%s",(sid,ident,retrieved)).fetchone()
  if sr: srid=sr[0]
  else: srid=c.execute("INSERT INTO source_record(literature_source_id,source_record_identifier,retrieved_at,raw_metadata_jsonb,content_access_state,normalization_state,provenance_hash) VALUES(%s,%s,%s,%s::jsonb,%s,'UNRESOLVED',%s) RETURNING id::text",(sid,ident,retrieved,json.dumps(r),"ABSTRACT_ONLY" if r.get("has_abstract") else "METADATA_ONLY",r.get("payload_hash"))).fetchone()[0]
  wid=find_work(c,ids); pubdate,pubyear=dates(r)
  if not wid: wid=c.execute("INSERT INTO work(title,publication_date,publication_year,venue,work_type,current_access_level) VALUES(%s,%s,%s,%s,%s,%s) RETURNING id::text",(title(r),pubdate,pubyear,r.get("container_title") or ((r.get("primary_location") or {}).get("source") or {}).get("display_name"),r.get("type"),"ABSTRACT_ONLY" if r.get("has_abstract") else "METADATA_ONLY")).fetchone()[0]
  for t,v,primary in ids:c.execute("INSERT INTO work_identifier(work_id,identifier_type,identifier_value,is_primary) VALUES(%s,%s,%s,%s) ON CONFLICT(identifier_type,identifier_value) DO NOTHING",(wid,t,v,primary))
  c.execute("INSERT INTO work_source_record(work_id,source_record_id,match_method,match_state,matched_at) VALUES(%s,%s,%s,'MATCHED',%s) ON CONFLICT(source_record_id) DO NOTHING",(wid,srid,x["source_key"]+"_identifier_resolution",retrieved))
  c.execute("UPDATE source_record SET normalization_state='MATCHED' WHERE id=%s",(srid,))
  c.execute("INSERT INTO project_work_relevance(project_id,work_id,relevance_state,relevance_advice,rationale,origin,human_review_state,first_seen_at,last_seen_at) VALUES(%s,%s,'CANDIDATE',NULL,%s,%s,NULL,%s,%s) ON CONFLICT(project_id,work_id) DO UPDATE SET last_seen_at=GREATEST(project_work_relevance.last_seen_at,EXCLUDED.last_seen_at)",(x["project_id"],wid,"Discovered metadata; awaiting HUMAN relevance review.",x["source_key"]+"_pilot_ingest",retrieved,retrieved));out.append({"source_record_id":srid,"work_id":wid})
 return out
def main():
 a=parse_args();x=load_envelope(a.envelope)
 if not a.apply: print(json.dumps({"mode":"DRY_RUN","source_key":x["source_key"],"project_id":x["project_id"],"record_count":len(x["records"]),"scientific_decisions_made_automatically":0},indent=2));return
 import psycopg
 from psycopg.rows import dict_row
 dsn=os.environ.get("GFPROJ_PILOT_DSN")
 if not dsn: raise SystemExit("GFPROJ_PILOT_DSN required for apply")
 with psycopg.connect(dsn,row_factory=dict_row) as c:
  if c.execute("SELECT session_user").fetchone()["session_user"]!="gfproj_pilot_executor":raise SystemExit("pilot executor session identity check failed")
  c.execute("SET ROLE gfproj_pilot_metadata_ingestor");assert_boundary(c);validate_context(c,x);rows=ingest(c,x,a.retrieved_at)
 print(json.dumps({"mode":"APPLY","source_key":x["source_key"],"persisted":rows,"scientific_decisions_made_automatically":0},indent=2))
if __name__=="__main__":main()
