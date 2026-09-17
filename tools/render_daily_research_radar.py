#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from datetime import datetime, timedelta, timezone
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prototype" / "api"))
from db import db

def scalar(cur, sql, params):
    cur.execute(sql, params); return next(iter(cur.fetchone().values()))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--project-id'); ap.add_argument('--hours',type=int,default=24); args=ap.parse_args()
    end=datetime.now(timezone.utc); start=end-timedelta(hours=args.hours); project=args.project_id
    with db() as conn, conn.cursor() as cur:
        filt=' AND project_id=%s' if project else ''; p=(start,end,project) if project else (start,end)
        works=scalar(cur, 'SELECT count(DISTINCT work_id) FROM project_work_relevance WHERE first_seen_at >= %s AND first_seen_at < %s'+filt, p)
        changes=scalar(cur, 'SELECT count(*) FROM change_event WHERE observed_at >= %s AND observed_at < %s'+filt, p)
        decisions=scalar(cur, 'SELECT count(*) FROM human_decision WHERE decided_at >= %s AND decided_at < %s'+filt, p)
        pending=scalar(cur, "SELECT count(*) FROM project_work_relevance WHERE relevance_state IN ('CANDIDATE','NEEDS_REVIEW')"+(' AND project_id=%s' if project else ''), (project,) if project else ())
    out={'window_start':start.isoformat(),'window_end':end.isoformat(),'project_id':project,'new_works':works,'change_events':changes,'human_decisions':decisions,'pending_human_review':pending,'scientific_decisions_made_automatically':0}
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
