#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--record',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();x=json.loads(Path(a.record).read_text());fps=x.get('source_fingerprints',{});checks=[('human authored',x.get('human_authored') is True),('reflection present',any(str(x.get(k,'')).strip() for k in ['clearer','uncertain','evidence_that_changed_understanding'])),('source fingerprints',all(len(fps.get(k,''))==64 for k in ['reflection','review','plan'])),('non scientific',x.get('scientific_decision') is False),('non canonical',x.get('canonical_write') is False)]
 out={'mode':'TRIAL_HUMAN_LEARNING_RECORD_AUDIT','checks':[{'name':n,'pass':bool(v)} for n,v in checks],'pass':all(v for _,v in checks),'warning':'Audit verifies authorship/provenance invariants only; it does not score learning quality or scientific correctness.','scientific_decision':False,'canonical_write':False};Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('HUMAN_LEARNING_RECORD_AUDIT_'+('PASS' if out['pass'] else 'FAIL'))
if __name__=='__main__':main()
