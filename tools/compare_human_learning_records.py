#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--before',required=True);ap.add_argument('--after',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();b=json.loads(Path(a.before).read_text());n=json.loads(Path(a.after).read_text())
 fields=['clearer','uncertain','evidence_that_changed_understanding','intended_next_action','investigation_question','sufficiency_criterion'];changes=[{'field':f,'before':b.get(f,''),'after':n.get(f,''),'changed':b.get(f)!=n.get(f)} for f in fields]
 old=set(b.get('reviewed_evidence_ids',[]));new=set(n.get('reviewed_evidence_ids',[]));out={'mode':'TRIAL_HUMAN_LEARNING_DELTA','changes':changes,'changed_field_count':sum(x['changed'] for x in changes),'newly_reviewed_evidence_ids':sorted(new-old),'no_longer_referenced_evidence_ids':sorted(old-new),'interpretation':'DESCRIPTIVE_ONLY','guardrails':['A changed reflection records HUMAN-authored change; it is not evidence of improvement.','More reviewed evidence does not imply better research or greater correctness.','The system must not score, rank, or infer researcher competence from this delta.'],'scientific_decision':False,'canonical_write':False};Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('HUMAN_LEARNING_DELTA_READY')
if __name__=='__main__':main()
