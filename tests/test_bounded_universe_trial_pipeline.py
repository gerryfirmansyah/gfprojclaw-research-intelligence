from pathlib import Path
for f,required in {
 'tools/retrieve_openalex_bounded_universe.py':['TRIAL_NON_CANONICAL_WHOLE_BOUNDED_METADATA','complete_against_reported_total','checkpoint scope mismatch','scientific_decision'],
 'tools/analyze_bounded_universe.py':['MACHINE_OBSERVATION_NOT_SCIENTIFIC_TRUTH','duplicate_openalex_ids','title_terms','scientific_decision'],
 'tools/build_researcher_landscape.py':['RESEARCHER_VISIBLE_TRIAL_LANDSCAPE','human_next_actions','verify DOI/source','scientific_decision'],
 'tools/build_why_trace.py':['EVERY_WHY_INSPECTABLE_BACK_TO_WHAT','supporting_observation','members','scientific_decision'],
}.items():
 s=Path(f).read_text()
 for x in required: assert x in s,(f,x)
 for bad in ['INSERT INTO','UPDATE ','DELETE FROM','psycopg']:
  assert bad not in s,(f,bad)
print('BOUNDED_UNIVERSE_TRIAL_PIPELINE_PASS')
for f,required in {
 'tools/deduplicate_bounded_universe.py':['normalized exact DOI','deduplicated_count','scientific_decision'],
 'tools/build_paper_inspector.py':['HUMAN_PAPER_INSPECTOR_PAYLOAD_TRIAL','NOT_RETRIEVED_IN_THIS_TRIAL','INSPECT_BEFORE_SCIENTIFIC_USE'],
 'tools/build_coverage_learning.py':['Absence from this observed OpenAlex/query/time-bounded corpus is not evidence of absence from research.','RECONSIDER_QUERY','scientific_decision'],
}.items():
 s=Path(f).read_text()
 for x in required: assert x in s,(f,x)
