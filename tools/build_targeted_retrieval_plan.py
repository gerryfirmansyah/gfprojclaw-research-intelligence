from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--brief',required=True);p.add_argument('--out',required=True);a=p.parse_args();b=json.loads(Path(a.brief).read_text())
 authorized=bool(b.get('expansion_authorized'))
 plan={'mode':'TRIAL_TARGETED_RETRIEVAL_PLAN','status':'READY_FOR_HUMAN_EXECUTION' if authorized else 'BLOCKED_NO_HUMAN_AUTHORIZATION','opportunity':b.get('opportunity'),'question':b.get('question'),'sufficiency_criterion':b.get('sufficiency_criterion'),'human_context':b.get('human_context'),'unresolved_titles':b.get('unresolved_titles',[]),'provider':'OpenAlex' if authorized else 'NOT_SELECTED','query_strategy':{'type':'HUMAN_QUESTION_BOUNDED','instruction':'Construct a narrow query from the HUMAN question/context; preserve exact query and provider response count.'} if authorized else None,'stop_rule':'Stop expansion and return to HUMAN when sufficiency criterion can be assessed; do not infer gap from retrieval count.','scientific_decision':False,'canonical_write':False}
 Path(a.out).write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');print(plan['status'])
if __name__=='__main__':main()
