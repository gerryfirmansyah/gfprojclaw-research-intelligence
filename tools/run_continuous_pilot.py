#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'prototype'/'api'))
def assert_worker_boundary(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT current_user, has_table_privilege(current_user,'continuous_pilot_run','INSERT'), has_table_privilege(current_user,'continuous_pilot_stage_run','UPDATE'), has_table_privilege(current_user,'human_decision','INSERT'), has_table_privilege(current_user,'human_decision','UPDATE')")
        role, can_insert_run, can_update_stage, can_insert_human, can_update_human = cur.fetchone()
    if role != 'gfproj_pilot_worker' or not can_insert_run or not can_update_stage or can_insert_human or can_update_human:
        raise SystemExit('worker database authority boundary check failed')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--project-id'); ap.add_argument('--simulate-failure'); ap.add_argument('--dry-run',action='store_true'); ap.add_argument('--max-attempts',type=int,default=2); a=ap.parse_args()
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
        assert_worker_boundary(conn)
    raise SystemExit('write mode boundary verified; persisted writes remain intentionally disabled pending execution identity provisioning')
if __name__=='__main__': main()
