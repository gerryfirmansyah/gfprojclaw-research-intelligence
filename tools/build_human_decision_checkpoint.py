#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--assessment',required=True);ap.add_argument('--human-action',choices=['STOP_AND_REFLECT','REVISE_QUESTION','REQUEST_MORE_REVIEW','AUTHORIZE_NEXT_LOOP'],required=True);ap.add_argument('--human-rationale',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();x=json.loads(Path(a.assessment).read_text())
 if not a.human_rationale.strip():raise SystemExit('BLOCKED: HUMAN rationale required')
 allowed={'SUFFICIENT':{'STOP_AND_REFLECT','REVISE_QUESTION'},'INSUFFICIENT':{'REVISE_QUESTION','REQUEST_MORE_REVIEW','AUTHORIZE_NEXT_LOOP'},'UNCERTAIN':{'REVISE_QUESTION','REQUEST_MORE_REVIEW'}}
 verdict=x.get('human_verdict');ok=a.human_action in allowed.get(verdict,set())
 out={'mode':'TRIAL_HUMAN_DECISION_CHECKPOINT','sufficiency_verdict':verdict,'human_action':a.human_action,'human_rationale':a.human_rationale,'status':'AUTHORIZED_HUMAN_ACTION' if ok else 'BLOCKED_ACTION_MISMATCH','next_loop_authorized':bool(ok and a.human_action=='AUTHORIZE_NEXT_LOOP'),'guardrails':['This checkpoint records a HUMAN workflow action, not a scientific conclusion.','STOP_AND_REFLECT does not assert gap, novelty, relevance, significance, or truth.','AUTHORIZE_NEXT_LOOP authorizes one next planning loop only; it does not authorize unbounded retrieval.'],'scientific_decision':False,'canonical_write':False}
 Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
