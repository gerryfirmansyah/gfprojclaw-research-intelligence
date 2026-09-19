from __future__ import annotations
import argparse,hashlib,json,os,sys,time,urllib.error,urllib.parse,urllib.request
ROOT=__import__('pathlib').Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'prototype'/'api'))
from db import db
SOURCE='crossref'; BASE='https://api.crossref.org/works'
def args():
 p=argparse.ArgumentParser();p.add_argument('--project-id',required=True);p.add_argument('--limit',type=int,default=10);p.add_argument('--timeout',type=float,default=15);p.add_argument('--max-attempts',type=int,default=2);p.add_argument('--retry-delay-seconds',type=float,default=1);return p.parse_args()
def approved_query(pid):
 dsn=os.environ.get("GFPROJ_PILOT_DSN")
 if dsn:
  import psycopg
  from psycopg.rows import dict_row
  with psycopg.connect(dsn,row_factory=dict_row) as c:
   if c.execute("SELECT session_user").fetchone()["session_user"]!="gfproj_pilot_executor": raise SystemExit("pilot executor session identity check failed")
   c.execute("SET ROLE gfproj_pilot_metadata_ingestor")
   r=c.execute("SELECT v.id::text,v.version_no,v.project_configuration_jsonb->'discovery_overrides'->'human_approved_query_v1' AS approved FROM research_project p JOIN research_project_version v ON v.id=p.current_version_id WHERE p.id=%s AND p.status='ACTIVE'",(pid,)).fetchone()
 else:
  with db() as c:
   r=c.execute("SELECT v.id::text,v.version_no,v.project_configuration_jsonb->'discovery_overrides'->'human_approved_query_v1' AS approved FROM research_project p JOIN research_project_version v ON v.id=p.current_version_id WHERE p.id=%s AND p.status='ACTIVE'",(pid,)).fetchone()
 if not r or not r['approved'] or not r['approved'].get('expression'): raise SystemExit('fail closed: no HUMAN-approved discovery query')
 return r
def canonical_hash(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def main():
 a=args()
 if not 1<=a.limit<=25 or not 1<=a.timeout<=30 or not 1<=a.max_attempts<=3 or not 0<=a.retry_delay_seconds<=300: raise SystemExit('bounded args violated')
 cfg=approved_query(a.project_id); expr=cfg['approved']['expression']; fp=hashlib.sha256(expr.encode()).hexdigest(); started=time.time(); last=None; history=[]
 url=BASE+'?'+urllib.parse.urlencode({'query.bibliographic':expr,'rows':a.limit})
 req=urllib.request.Request(url,headers={'User-Agent':'GFPROJCLAW-Research-Pilot/0.1'})
 for attempt in range(1,a.max_attempts+1):
  try:
   with urllib.request.urlopen(req,timeout=a.timeout) as r:
    raw=r.read(2_000_001)
    if len(raw)>2_000_000: raise ValueError('response exceeds 2MB bound')
    payload=json.loads(raw); rows=(payload.get('message') or {}).get('items')
    if not isinstance(rows,list): raise ValueError('malformed Crossref items')
    records=[{'doi':x.get('DOI'),'title':(x.get('title') or [None])[0],'published':x.get('published-print') or x.get('published-online') or x.get('published'),'type':x.get('type'),'publisher':x.get('publisher'),'container_title':(x.get('container-title') or [None])[0],'url':x.get('URL'),'has_abstract':bool(x.get('abstract')),'payload_hash':canonical_hash(x)} for x in rows[:a.limit]]
    print(json.dumps({'source_key':SOURCE,'project_id':a.project_id,'project_version_id':cfg['id'],'project_version_no':cfg['version_no'],'query_fingerprint':fp,'attempt':attempt,'attempt_history':history+[{'attempt':attempt,'status':'COMPLETED','error':None}],'http_status':getattr(r,'status',200),'record_count':len(records),'elapsed_ms':round((time.time()-started)*1000),'records':records},ensure_ascii=False,indent=2));return
  except (urllib.error.URLError,urllib.error.HTTPError,TimeoutError,ValueError,json.JSONDecodeError) as e:
   last=f'{type(e).__name__}: {e}'
   history.append({'attempt':attempt,'status':'FAILED','error':last})
   if attempt<a.max_attempts: time.sleep(a.retry_delay_seconds)
 print(json.dumps({'source_key':SOURCE,'project_id':a.project_id,'project_version_id':cfg['id'],'query_fingerprint':fp,'status':'FAILED','attempts':a.max_attempts,'attempt_history':history,'error':last,'elapsed_ms':round((time.time()-started)*1000)},indent=2));raise SystemExit(2)
if __name__=='__main__': main()
