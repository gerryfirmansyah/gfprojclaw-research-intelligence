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
        evidence=scalar(cur, 'SELECT count(*) FROM evidence_fragment ef JOIN project_work_relevance pwr ON pwr.work_id=ef.work_id WHERE ef.created_at >= %s AND ef.created_at < %s'+(' AND pwr.project_id=%s' if project else ''), p)
        runs=scalar(cur, 'SELECT count(*) FROM continuous_pilot_run WHERE started_at >= %s AND started_at < %s'+filt, p)
        failed=scalar(cur, "SELECT count(*) FROM continuous_pilot_run WHERE started_at >= %s AND started_at < %s AND status='FAILED'"+filt, p)
        auto=scalar(cur, "SELECT count(*) FROM continuous_pilot_run WHERE started_at >= %s AND started_at < %s AND machine_actions_jsonb @> '[{\"scientific_decision\":true}]'::jsonb"+filt, p)
        stage_filt=(' AND pr.project_id=%s' if project else '')
        stage_p=(start,end,project) if project else (start,end)
        source_failures=scalar(cur, "SELECT count(*) FROM continuous_pilot_stage_run ps JOIN continuous_pilot_run pr ON pr.id=ps.pilot_run_id WHERE ps.started_at >= %s AND ps.started_at < %s AND ps.status='FAILED'"+stage_filt, stage_p)
        recoveries=scalar(cur, "SELECT count(*) FROM continuous_pilot_stage_run ps JOIN continuous_pilot_run pr ON pr.id=ps.pilot_run_id WHERE ps.started_at >= %s AND ps.started_at < %s AND ps.status='COMPLETED' AND ps.attempt > 1"+stage_filt, stage_p)
        cur.execute('SELECT ef.id::text FROM evidence_fragment ef JOIN project_work_relevance pwr ON pwr.work_id=ef.work_id WHERE ef.created_at >= %s AND ef.created_at < %s'+(' AND pwr.project_id=%s' if project else '')+' ORDER BY ef.created_at', p); evidence_ids=[r['id'] for r in cur.fetchall()]
        cur.execute("SELECT id::text FROM continuous_pilot_run WHERE started_at >= %s AND started_at < %s AND status='FAILED'"+filt+' ORDER BY started_at', p); failed_ids=[r['id'] for r in cur.fetchall()]
    out={'window_start':start.isoformat(),'window_end':end.isoformat(),'project_id':project,'new_works':works,'change_events':changes,'human_decisions':decisions,'pending_human_review_backlog':pending,'new_evidence_fragments':evidence,'pilot_runs':runs,'failed_pilot_runs':failed,'local_source_failures':source_failures,'local_source_recoveries':recoveries,'scientific_decisions_made_automatically':auto,'drilldown':{'new_evidence_fragment_ids':evidence_ids,'failed_pilot_run_ids':failed_ids},'query_basis':{'window':'[window_start, window_end)','pending_human_review_backlog':'current backlog; not window-scoped','local_source_failures':'stage attempts status=FAILED within window','local_source_recoveries':'stage attempts status=COMPLETED with attempt>1 within window','automatic_scientific_decisions':'pilot machine_actions_jsonb scientific_decision=true'}}
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
