#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'prototype'/'api'))
def assert_worker_boundary(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT current_user AS role, has_table_privilege(current_user,'continuous_pilot_run','INSERT') AS can_insert_run, has_table_privilege(current_user,'continuous_pilot_stage_run','UPDATE') AS can_update_stage, has_table_privilege(current_user,'human_decision','INSERT') AS can_insert_human, has_table_privilege(current_user,'human_decision','UPDATE') AS can_update_human")
        row=cur.fetchone(); role=row['role']; can_insert_run=row['can_insert_run']; can_update_stage=row['can_update_stage']; can_insert_human=row['can_insert_human']; can_update_human=row['can_update_human']
    if role != 'gfproj_pilot_worker' or not can_insert_run or not can_update_stage or can_insert_human or can_update_human:
        raise SystemExit('worker database authority boundary check failed')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--project-id'); ap.add_argument('--simulate-failure'); ap.add_argument('--dry-run',action='store_true'); ap.add_argument('--max-attempts',type=int,default=2); ap.add_argument('--idempotency-key'); a=ap.parse_args()
    stages=['OpenAlex','Crossref']; rid=str(uuid.uuid4()); outcomes=[]
    for source in stages:
        failed=source==a.simulate_failure
        if failed:
            outcomes.append({'source':source,'status':'FAILED','attempt':1,'error':'SIMULATED_LOCAL_FAILURE'})
            if a.max_attempts > 1:
                outcomes.append({'source':source,'status':'COMPLETED','attempt':2,'error':None})
        else:
            outcomes.append({'source':source,'status':'COMPLETED','attempt':1,'error':None})
    final_by_source={x['source']:x for x in outcomes}
    final_statuses=[x['status'] for x in final_by_source.values()]
    status='PARTIAL' if 'FAILED' in final_statuses and 'COMPLETED' in final_statuses else ('FAILED' if final_statuses and all(x=='FAILED' for x in final_statuses) else 'COMPLETED')
    result={'run_id':rid,'project_id':a.project_id,'status':status,'stages':outcomes,'scientific_decisions_made_automatically':0}
    if a.dry_run: print(json.dumps(result,indent=2)); return
    from db import db
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT session_user AS session_role")
            if cur.fetchone()['session_role'] != 'gfproj_pilot_executor': raise SystemExit('pilot executor session identity check failed')
            cur.execute("SET ROLE gfproj_pilot_worker")
        assert_worker_boundary(conn)
        with conn.cursor() as cur:
            cur.execute("INSERT INTO continuous_pilot_run (id,trigger_type,project_id,started_at,status,machine_actions_jsonb,idempotency_key) VALUES (%s,'MANUAL',%s,now(),'RUNNING','[]'::jsonb,%s) ON CONFLICT (idempotency_key) WHERE idempotency_key IS NOT NULL DO NOTHING RETURNING id", (rid,a.project_id,a.idempotency_key))
            row=cur.fetchone()
            if row is None: raise SystemExit('idempotent pilot run already exists')
            for x in outcomes:
                cur.execute("INSERT INTO continuous_pilot_stage_run (id,pilot_run_id,stage_key,source_key,attempt,status,started_at,finished_at,error_class,error_summary,metrics_jsonb) VALUES (%s,%s,'SOURCE_DISCOVERY',%s,%s,%s,now(),now(),%s,%s,'{}'::jsonb)", (str(uuid.uuid4()),rid,x['source'],x['attempt'],x['status'],x['error'],x['error']))
            cur.execute("UPDATE continuous_pilot_run SET status=%s,finished_at=now(),machine_actions_jsonb=%s::jsonb WHERE id=%s", (status,json.dumps([{'action':'SIMULATED_SOURCE_DISCOVERY','scientific_decision':False}]),rid))
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
