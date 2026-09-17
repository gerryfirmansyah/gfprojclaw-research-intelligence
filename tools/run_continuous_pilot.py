#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'prototype'/'api'))
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
    raise SystemExit('write mode intentionally disabled until dedicated worker credentials are provisioned')
if __name__=='__main__': main()
