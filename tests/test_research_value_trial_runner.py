from pathlib import Path
s=Path("tools/run_research_value_trial.py").read_text()
for x in ["TRIAL_NON_CANONICAL","canonical_write\":False","scientific_decision\":False","openalex","crossref","provider_reported_total","unique_members","overlap_members","doi_url","source_url"]:assert x in s,x
for bad in ["INSERT INTO","UPDATE ","DELETE FROM","psycopg","project_work_relevance","evidence_relationship"]:assert bad not in s,bad
print("RESEARCH_VALUE_TRIAL_RUNNER_PASS")
