#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--reflection',required=True);ap.add_argument('--review',required=True);ap.add_argument('--plan',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();ref=json.loads(Path(a.reflection).read_text());rev=json.loads(Path(a.review).read_text());plan=json.loads(Path(a.plan).read_text())
 if not any(str(ref.get(k,'')).strip() for k in ['clearer','uncertain','evidence_that_changed_understanding']):raise SystemExit('BLOCKED: HUMAN reflection content required')
 evidence_ids=[x.get('openalex_id') for x in rev.get('reviews',rev.get('papers',[])) if x.get('openalex_id')]
 out={'mode':'TRIAL_HUMAN_LEARNING_RECORD','human_authored':True,'clearer':ref.get('clearer',''),'uncertain':ref.get('uncertain',''),'evidence_that_changed_understanding':ref.get('evidence_that_changed_understanding',''),'intended_next_action':ref.get('intended_next_action',''),'investigation_question':plan.get('question'),'sufficiency_criterion':plan.get('sufficiency_criterion'),'reviewed_evidence_ids':evidence_ids,'evidence_trace_count':len(evidence_ids),'source_fingerprints':{},'limitations':['This record preserves HUMAN reflection; it does not validate the reflection as a scientific conclusion.','Evidence IDs establish traceability, not evidentiary sufficiency or truth.'],'scientific_decision':False,'canonical_write':False}
 for k,p in [('reflection',a.reflection),('review',a.review),('plan',a.plan)]:out['source_fingerprints'][k]=hashlib.sha256(Path(p).read_bytes()).hexdigest()
 Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('HUMAN_LEARNING_RECORD_READY')
if __name__=='__main__':main()
