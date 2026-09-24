#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--delta',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();x=json.loads(Path(a.delta).read_text());g=' '.join(x.get('guardrails',[])).lower();checks=[('descriptive only',x.get('interpretation')=='DESCRIPTIVE_ONLY'),('no improvement inference','not evidence of improvement' in g),('no competence scoring','competence' in g and ('not score' in g or 'must not score' in g)),('no scientific decision',x.get('scientific_decision') is False),('no canonical write',x.get('canonical_write') is False)]
 out={'mode':'TRIAL_HUMAN_AGENCY_BOUNDARY_AUDIT','checks':[{'name':n,'pass':bool(v)} for n,v in checks],'pass':all(v for _,v in checks),'principle':'System may preserve and compare HUMAN-authored learning states, but may not turn them into a score, ranking, competence judgment, or scientific decision.','scientific_decision':False,'canonical_write':False};Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('HUMAN_AGENCY_BOUNDARY_AUDIT_'+('PASS' if out['pass'] else 'FAIL'))
if __name__=='__main__':main()
