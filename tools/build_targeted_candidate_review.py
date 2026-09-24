#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--comparison',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();x=json.loads(Path(a.comparison).read_text());papers=[]
 for p in x.get('new_candidate_papers',[]):papers.append({'openalex_id':p.get('openalex_id'),'title':p.get('title'),'doi':p.get('doi'),'source_url':p.get('source_url'),'review_status':'NOT_REVIEWED','human_note':'','allowed_statuses':['SUPPORTS','CHALLENGES','UNCLEAR','OUT_OF_SCOPE'],'machine_classification':None})
 out={'mode':'TRIAL_TARGETED_CANDIDATE_HUMAN_REVIEW','exact_query':x.get('exact_query'),'candidate_count':len(papers),'papers':papers,'instructions':['HUMAN reads evidence before assigning a review status.','OUT_OF_SCOPE is a HUMAN scope judgment, not an automated relevance label.','SUPPORTS/CHALLENGES/UNCLEAR refer only to the current investigation question.'],'completion_rule':'Return to sufficiency assessment after HUMAN reviews candidates; do not infer gap from status counts.','scientific_decision':False,'canonical_write':False}
 Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'candidates':len(papers),'status':'READY_FOR_HUMAN_REVIEW'}))
if __name__=='__main__':main()
