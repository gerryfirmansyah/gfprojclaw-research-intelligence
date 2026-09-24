from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'tools/execute_targeted_openalex_retrieval.py').read_text()
for x in ["READY_FOR_HUMAN_EXECUTION","BLOCKED: plan lacks HUMAN authorization","exact_query","provider_reported_count","TRIAL_TARGETED_OPENALEX_RETRIEVAL","Targeted retrieval is not a complete literature universe.","scientific_decision':False","canonical_write':False"]: assert x in s
print('TARGETED_OPENALEX_RETRIEVAL_CONTRACT_PASS')
