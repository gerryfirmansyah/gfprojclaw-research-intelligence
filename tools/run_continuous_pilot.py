#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,subprocess,sys,tempfile,uuid
from contextlib import contextmanager
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'prototype'/'api'))
SOURCES={'OpenAlex':'fetch_openalex_discovery.py','Crossref':'fetch_crossref_discovery.py'}
@contextmanager
def pilot_db():
 dsn=os.environ.get('GFPROJ_PILOT_DSN')
 if not dsn: raise SystemExit('GFPROJ_PILOT_DSN required for non-dry-run execution')
 import psycopg
 from psycopg.rows import dict_row
 with psycopg.connect(dsn,row_factory=dict_row) as conn:
  yield conn
def assert_worker_boundary(conn):
 r=conn.execute("SELECT current_user AS role,has_table_privilege(current_user,'continuous_pilot_run','INSERT') AS ins,has_table_privilege(current_user,'continuous_pilot_stage_run','UPDATE') AS upd,has_table_privilege(current_user,'human_decision','INSERT') AS human_ins,has_table_privilege(current_user,'human_decision','UPDATE') AS human_upd").fetchone()
 if r['role']!='gfproj_pilot_worker' or not r['ins'] or not r['upd'] or r['human_ins'] or r['human_upd']: raise SystemExit('worker database authority boundary check failed')
def source_run(source,a,retrieved_at):
 if a.simulate_failure==source: return {'source':source,'status':'FAILED','attempt':1,'attempt_history':[{'attempt':1,'status':'FAILED','error':'SIMULATED_LOCAL_FAILURE'}],'error':'SIMULATED_LOCAL_FAILURE','record_count':0}
 if a.simulate_retry_recovery==source:
  saved_attempts=a.max_attempts;saved_retry=a.simulate_retry_recovery
  a.max_attempts=1;a.simulate_retry_recovery=None
  try: out=source_run(source,a,retrieved_at)
  finally: a.max_attempts=saved_attempts;a.simulate_retry_recovery=saved_retry
  if out['status']!='COMPLETED': return out
  out['attempt']=2;out['attempt_history']=[{'attempt':1,'status':'FAILED','error':'SIMULATED_TRANSIENT_FAILURE'}, {'attempt':2,'status':'COMPLETED','error':None}]
  return out
 cmd=[sys.executable,str(ROOT/'tools'/SOURCES[source]),'--project-id',a.project_id,'--limit',str(a.limit),'--timeout',str(a.timeout),'--max-attempts',str(a.max_attempts),'--retry-delay-seconds',str(a.retry_delay_seconds)]
 try:
  p=subprocess.run(cmd,capture_output=True,text=True,env=os.environ.copy(),timeout=a.timeout*a.max_attempts+a.retry_delay_seconds*max(a.max_attempts-1,0)+10)
 except subprocess.TimeoutExpired:
  return {'source':source,'status':'FAILED','attempt':a.max_attempts,'attempt_history':[{'attempt':a.max_attempts,'status':'FAILED','error':'SOURCE_TIMEOUT'}],'error':'SOURCE_TIMEOUT','record_count':0}
 except Exception as e:
  return {'source':source,'status':'FAILED','attempt':1,'attempt_history':[{'attempt':1,'status':'FAILED','error':'SOURCE_EXEC_FAILED: '+type(e).__name__}],'error':'SOURCE_EXEC_FAILED: '+type(e).__name__,'record_count':0}
 try: env=json.loads(p.stdout)
 except Exception:
  return {'source':source,'status':'FAILED','attempt':a.max_attempts if p.returncode else 1,'attempt_history':[{'attempt':a.max_attempts if p.returncode else 1,'status':'FAILED','error':'SOURCE_INVALID_JSON'}],'error':'SOURCE_INVALID_JSON','record_count':0}
 if p.returncode or env.get('status')=='FAILED': return {'source':source,'status':'FAILED','attempt':env.get('attempts',a.max_attempts),'attempt_history':env.get('attempt_history') or [{'attempt':env.get('attempts',a.max_attempts),'status':'FAILED','error':env.get('error') or 'SOURCE_FAILED'}],'error':env.get('error') or p.stderr.strip() or 'SOURCE_FAILED','record_count':0}
 if a.dry_run: return {'source':source,'status':'COMPLETED','attempt':env.get('attempt',1),'attempt_history':env.get('attempt_history') or [{'attempt':env.get('attempt',1),'status':'COMPLETED','error':None}],'error':None,'record_count':env.get('record_count',0)}
 with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False) as f: json.dump(env,f); path=f.name
 try:
  try:
   q=subprocess.run([sys.executable,str(ROOT/'tools'/'ingest_discovery_metadata.py'),'--envelope',path,'--retrieved-at',retrieved_at,'--apply'],capture_output=True,text=True,env=os.environ.copy(),timeout=30)
  except subprocess.TimeoutExpired:
   return {'source':source,'status':'FAILED','attempt':env.get('attempt',1),'attempt_history':env.get('attempt_history'),'error':'INGEST_TIMEOUT','record_count':0}
  except Exception as e:
   return {'source':source,'status':'FAILED','attempt':env.get('attempt',1),'attempt_history':env.get('attempt_history'),'error':'INGEST_EXEC_FAILED: '+type(e).__name__,'record_count':0}
  if q.returncode: return {'source':source,'status':'FAILED','attempt':env.get('attempt',1),'attempt_history':env.get('attempt_history'),'error':q.stderr.strip() or q.stdout.strip() or 'INGEST_FAILED','record_count':0}
  try: out=json.loads(q.stdout)
  except Exception: return {'source':source,'status':'FAILED','attempt':env.get('attempt',1),'attempt_history':env.get('attempt_history'),'error':'INGEST_INVALID_JSON','record_count':0}
  return {'source':source,'status':'COMPLETED','attempt':env.get('attempt',1),'attempt_history':env.get('attempt_history') or [{'attempt':env.get('attempt',1),'status':'COMPLETED','error':None}],'error':None,'record_count':len(out.get('persisted',[]))}
 finally: Path(path).unlink(missing_ok=True)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project-id',required=True);ap.add_argument('--simulate-failure',choices=tuple(SOURCES));ap.add_argument('--simulate-retry-recovery',choices=tuple(SOURCES));ap.add_argument('--dry-run',action='store_true');ap.add_argument('--max-attempts',type=int,default=2);ap.add_argument('--retry-delay-seconds',type=float,default=5);ap.add_argument('--idempotency-key');ap.add_argument('--trigger-type',choices=('MANUAL','SCHEDULED','RETRY'),default='MANUAL');ap.add_argument('--limit',type=int,default=3);ap.add_argument('--timeout',type=float,default=15);a=ap.parse_args()
 if not 1<=a.max_attempts<=3 or not 0<=a.retry_delay_seconds<=300 or not 1<=a.limit<=25 or not 1<=a.timeout<=30: raise SystemExit('bounded args violated')
 if (a.simulate_failure or a.simulate_retry_recovery) and os.environ.get('GFPROJ_ALLOW_PILOT_SIMULATION')!='1': raise SystemExit('simulation flags require GFPROJ_ALLOW_PILOT_SIMULATION=1')

 if a.dry_run:
  retrieved_at=datetime.now(timezone.utc).isoformat()
  outcomes=[source_run(source,a,retrieved_at) for source in SOURCES]
  states=[x['status'] for x in outcomes]
  status='PARTIAL' if 'FAILED' in states and 'COMPLETED' in states else ('FAILED' if all(x=='FAILED' for x in states) else 'COMPLETED')
  print(json.dumps({'run_id':str(uuid.uuid4()),'project_id':a.project_id,'status':status,'stages':outcomes,'scientific_decisions_made_automatically':0},indent=2))
  return

 if not a.idempotency_key:
  raise SystemExit('--idempotency-key required for non-dry-run execution')

 rid=str(uuid.uuid4())
 resumed=False

 with pilot_db() as conn:
  if conn.execute('SELECT session_user AS u').fetchone()['u']!='gfproj_pilot_executor': raise SystemExit('pilot executor session identity check failed')
  conn.execute('SET ROLE gfproj_pilot_worker');assert_worker_boundary(conn)
  row=conn.execute("INSERT INTO continuous_pilot_run(id,trigger_type,project_id,started_at,status,machine_actions_jsonb,idempotency_key) VALUES(%s,%s,%s,now(),'RUNNING','[]'::jsonb,%s) ON CONFLICT(idempotency_key) WHERE idempotency_key IS NOT NULL DO NOTHING RETURNING id::text AS id,started_at",(rid,a.trigger_type,a.project_id,a.idempotency_key)).fetchone()
  if row is None:
   existing=conn.execute("SELECT id::text AS id,status,started_at FROM continuous_pilot_run WHERE idempotency_key=%s",(a.idempotency_key,)).fetchone()
   if existing is None or existing['status']!='RUNNING': raise SystemExit('idempotent pilot run already terminal')
   row=existing
   resumed=True
  rid=row['id']
  retrieved_at=row['started_at'].isoformat()

 outcomes=[source_run(source,a,retrieved_at) for source in SOURCES]
 states=[x['status'] for x in outcomes]
 status='PARTIAL' if 'FAILED' in states and 'COMPLETED' in states else ('FAILED' if all(x=='FAILED' for x in states) else 'COMPLETED')
 result={'run_id':rid,'project_id':a.project_id,'status':status,'stages':outcomes,'scientific_decisions_made_automatically':0}
 if resumed: result['resumed']=True

 with pilot_db() as conn:
  if conn.execute('SELECT session_user AS u').fetchone()['u']!='gfproj_pilot_executor': raise SystemExit('pilot executor session identity check failed')
  conn.execute('SET ROLE gfproj_pilot_worker');assert_worker_boundary(conn)
  for x in outcomes:
   for h in x.get('attempt_history') or [{'attempt':x['attempt'],'status':x['status'],'error':x['error']}]:
    is_final=h['attempt']==x['attempt']
    conn.execute("INSERT INTO continuous_pilot_stage_run(id,pilot_run_id,stage_key,source_key,attempt,status,started_at,finished_at,error_class,error_summary,metrics_jsonb) VALUES(%s,%s,'SOURCE_DISCOVERY',%s,%s,%s,now(),now(),%s,%s,%s::jsonb) ON CONFLICT (pilot_run_id,stage_key,source_key,attempt) DO UPDATE SET status=EXCLUDED.status,finished_at=EXCLUDED.finished_at,error_class=EXCLUDED.error_class,error_summary=EXCLUDED.error_summary,metrics_jsonb=EXCLUDED.metrics_jsonb",(str(uuid.uuid4()),rid,x['source'],h['attempt'],h['status'],None if not h.get('error') else 'SOURCE_LOCAL_FAILURE',h.get('error'),json.dumps({'record_count':x['record_count'] if is_final and h['status']=='COMPLETED' else 0})))
  cur=conn.execute("UPDATE continuous_pilot_run SET status=%s,finished_at=now(),machine_actions_jsonb=%s::jsonb WHERE id=%s AND status='RUNNING'",(status,json.dumps([{'action':'BOUNDED_SOURCE_METADATA_INGEST','scientific_decision':False,'source':x['source'],'status':x['status'],'record_count':x['record_count']} for x in outcomes]),rid))
  if cur.rowcount!=1: raise SystemExit('pilot terminal transition lost RUNNING state')

 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
