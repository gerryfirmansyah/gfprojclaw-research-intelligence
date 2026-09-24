#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ledger',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();x=json.loads(Path(a.ledger).read_text());st=x.get('stages',[]);modes=[i.get('mode') for i in st];checks=[('traceable stages',x.get('trace_complete') is True),('no stage scientific decision',all(i.get('scientific_decision') is False for i in st)),('no stage canonical write',all(i.get('canonical_write') is False for i in st)),('hashes present',all(len(i.get('sha256',''))==64 for i in st)),('ledger noncanonical',x.get('canonical_write') is False)]
 out={'mode':'TRIAL_CLOSED_RESEARCH_LOOP_AUDIT','checks':[{'name':n,'pass':bool(v)} for n,v in checks],'pass':all(v for _,v in checks),'observed_modes':modes,'limitations':['This audit verifies workflow/provenance invariants, not scientific validity or research quality.'],'scientific_decision':False,'canonical_write':False};Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('CLOSED_RESEARCH_LOOP_AUDIT_'+('PASS' if out['pass'] else 'FAIL'))
if __name__=='__main__':main()
