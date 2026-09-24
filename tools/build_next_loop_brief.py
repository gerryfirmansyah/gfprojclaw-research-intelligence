#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--checkpoint',required=True);ap.add_argument('--previous-plan',required=True);ap.add_argument('--new-question',required=True);ap.add_argument('--new-context',default='');ap.add_argument('--out',required=True);a=ap.parse_args();c=json.loads(Path(a.checkpoint).read_text());p=json.loads(Path(a.previous_plan).read_text())
 if not c.get('next_loop_authorized'):raise SystemExit('BLOCKED: fresh HUMAN next-loop authorization required')
 if not a.new_question.strip():raise SystemExit('BLOCKED: HUMAN next-loop question required')
 out={'mode':'TRIAL_NEXT_LOOP_BRIEF','loop_scope':'ONE_TARGETED_LOOP','previous_question':p.get('question'),'human_next_question':a.new_question,'human_context':a.new_context,'previous_sufficiency_criterion':p.get('sufficiency_criterion'),'authorization_rationale':c.get('human_rationale'),'provider':'NOT_SELECTED','exact_query':'NOT_EXECUTED','status':'READY_FOR_TARGETED_PLANNING','requirements':['Build a fresh bounded plan from this HUMAN question; do not silently reuse or broaden the prior query.','Preserve provider/query/count provenance if executed.','Return new candidates to HUMAN review and reassess sufficiency before any further loop.'],'scientific_decision':False,'canonical_write':False}
 Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
