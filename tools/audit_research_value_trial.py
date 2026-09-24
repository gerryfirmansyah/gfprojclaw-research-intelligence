#!/usr/bin/env python3
import argparse,json,collections
def main():
 p=argparse.ArgumentParser();p.add_argument('--corpus',required=True);p.add_argument('--landscape',required=True);p.add_argument('--why',required=True);p.add_argument('--papers',required=True);p.add_argument('--coverage',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 c=json.load(open(a.corpus));l=json.load(open(a.landscape));w=json.load(open(a.why));pi=json.load(open(a.papers));cv=json.load(open(a.coverage))
 rows=c.get('records') or [];ids=[r.get('openalex_id') for r in rows];paper_ids=[r.get('openalex_id') for r in pi.get('papers') or []];member_ids=[m.get('openalex_id') for t in w.get('traces') or [] for m in t.get('members') or []]
 checks={
 'raw_coverage_complete':c.get('complete_against_reported_total') is True and c.get('raw_retrieved_count')==c.get('provider_reported_total'),
 'deduplicated_ids_unique':len(ids)==len(set(ids)),
 'landscape_count_matches_corpus':(l.get('coverage') or {}).get('retrieved_count')==len(rows),
 'paper_inspector_covers_corpus':set(paper_ids)==set(ids),
 'why_members_are_corpus_members':set(member_ids)<=set(ids),
 'why_has_provenance':all((t.get('verification') or {}).get('provider') and (t.get('verification') or {}).get('query') and (t.get('verification') or {}).get('time_boundary') for t in w.get('traces') or []),
 'blind_spot_statement_present':bool(cv.get('blind_spot_statement')),
 'human_decision_options_present':bool(cv.get('human_decision_options')),
 'no_scientific_decision':all(x.get('scientific_decision') is False for x in [c,l,w,pi,cv]),
 'no_canonical_write':all(x.get('canonical_write') is False for x in [c,l,w,pi,cv]),
 }
 out={'mode':'RESEARCH_VALUE_TRIAL_EXECUTABLE_AUDIT','checks':checks,'pass':all(checks.values()),'counts':{'raw_provider_total':c.get('provider_reported_total'),'deduplicated_members':len(rows),'why_traces':len(w.get('traces') or []),'why_unique_members':len(set(member_ids)),'paper_inspector_members':len(paper_ids)},'scientific_decision':False,'canonical_write':False}
 json.dump(out,open(a.output,'w'),ensure_ascii=False,indent=2);print(json.dumps(out,indent=2))
 raise SystemExit(0 if out['pass'] else 1)
if __name__=='__main__':main()
