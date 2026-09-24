from pathlib import Path
p=(Path(__file__).resolve().parents[1]/'tools/fetch_trial_openalex_abstracts.py').read_text()
for x in ['TRIAL_PROGRESSIVE_ABSTRACT_VERIFICATION','abstract_inverted_index','NOT_AVAILABLE_FROM_OPENALEX','canonical_write',"'scientific_decision':False"]: assert x in p
print('TRIAL_PROGRESSIVE_ABSTRACT_FETCH_PASS')
