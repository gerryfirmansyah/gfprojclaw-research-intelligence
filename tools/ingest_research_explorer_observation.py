#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

ALLOWED={"openalex","crossref"}

def args():
 p=argparse.ArgumentParser(); p.add_argument("--envelope",type=Path,required=True); p.add_argument("--research-interest",required=True); p.add_argument("--apply",action="store_true"); return p.parse_args()

def load(path):
 x=json.loads(path.read_text())
 if x.get("source_key") not in ALLOWED or not x.get("project_id") or not x.get("project_version_id") or not isinstance(x.get("records"),list) or not x["records"] or x.get("status")=="FAILED": raise SystemExit("fail closed: invalid discovery envelope")
 return x

def plan(x,interest):
 return {"mode":"DRY_RUN","project_id":x["project_id"],"project_version_id":x["project_version_id"],"source_key":x["source_key"],"research_interest":interest.strip(),"record_count":len(x["records"]),"writes":["research_exploration_session","discovery_query_family","discovery_query","source_record","discovery_observation"],"forbidden_writes":["project_work_relevance","evidence_fragment","claim","evidence_relationship","human_decision"],"scientific_decision":False}

def main():
 a=args(); x=load(a.envelope)
 if not a.research_interest.strip(): raise SystemExit("research interest required")
 if not a.apply: print(json.dumps(plan(x,a.research_interest),indent=2)); return
 raise SystemExit("apply disabled: Research Explorer observation writer requires dedicated least-privilege DB role and transactional regression before production persistence")

if __name__=="__main__": main()
