#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path

def load(p):return json.loads(Path(p).read_text()) if p else None
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--plan');ap.add_argument('--retrieval');ap.add_argument('--comparison');ap.add_argument('--review');ap.add_argument('--assessment');ap.add_argument('--checkpoint');ap.add_argument('--out',required=True);a=ap.parse_args();items=[]
 for kind,path in [('plan',a.plan),('retrieval',a.retrieval),('comparison',a.comparison),('review',a.review),('assessment',a.assessment),('checkpoint',a.checkpoint)]:
  if not path:continue
  x=load(path);raw=json.dumps(x,sort_keys=True,ensure_ascii=False).encode();items.append({'stage':kind,'mode':x.get('mode'),'status':x.get('status') or x.get('next_action') or x.get('human_verdict'),'sha256':hashlib.sha256(raw).hexdigest(),'scientific_decision':x.get('scientific_decision',False),'canonical_write':x.get('canonical_write',False)})
 out={'mode':'TRIAL_RESEARCH_LOOP_LEDGER','stages':items,'stage_count':len(items),'trace_complete':all(i['mode'] for i in items),'guardrails':['Ledger records provenance/state transitions only.','Ledger does not convert HUMAN workflow states into scientific conclusions.'],'scientific_decision':False,'canonical_write':False};Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'stages':len(items),'trace_complete':out['trace_complete']}))
if __name__=='__main__':main()
