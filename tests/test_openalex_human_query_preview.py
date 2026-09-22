from pathlib import Path
s=Path("tools/preview_openalex_human_query.py").read_text()
for x in ["--query","HUMAN_PROVIDED","provider_reported_total","requested_count","retrieved_count","READ_ONLY_PREVIEW","canonical_write","scientific_decision"]:assert x in s,x
for x in ["INSERT ","UPDATE ","DELETE ","project_work_relevance","human_decision"]:assert x not in s,x
print("OPENALEX_HUMAN_QUERY_PREVIEW_CONTRACT_PASS")
