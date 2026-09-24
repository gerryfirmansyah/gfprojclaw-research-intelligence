#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--review',required=True);ap.add_argument('--criterion',required=True);ap.add_argument('--human-verdict',choices=['SUFFICIENT','INSUFFICIENT','UNCERTAIN'],required=True);ap.add_argument('--human-note',default='');ap.add_argument('--out',required=True);a=ap.parse_args();r=json.loads(Path(a.review).read_text());papers=r.get('papers',[]);counts={s:sum(p.get('review_status')==s for p in papers) for s in ['SUPPORTS','CHALLENGES','UNCLEAR','OUT_OF_SCOPE','NOT_REVIEWED']};next_action={'SUFFICIENT':'RETURN_TO_HUMAN_DECISION','INSUFFICIENT':'CONSIDER_NEXT_TARGETED_LOOP','UNCERTAIN':'REVIEW_MORE_EVIDENCE'}[a.human_verdict]
 out={'mode':'TRIAL_HUMAN_SUFFICIENCY_ASSESSMENT','criterion':a.criterion,'human_verdict':a.human_verdict,'human_note':a.human_note,'review_counts':counts,'next_action':next_action,'guardrails':['Verdict records HUMAN assessment; the system does not decide sufficiency.','SUFFICIENT does not mean a research gap, novelty, significance, or truth has been established.','Any next targeted loop requires fresh HUMAN authorization.'],'scientific_decision':False,'canonical_write':False}
 Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(next_action)
if __name__=='__main__':main()
