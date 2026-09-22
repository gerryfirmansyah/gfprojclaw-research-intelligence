from pathlib import Path
s=Path("docs/j16/openalex-ui-api-query-semantics-observation-2026-09-22.md").read_text()
for x in ["NON_PARITY_COMPARISON","4 works","368329","requested_count: 10","retrieved_count: 10","canonical_write: false","scientific_decision: false","not the Research Universe","QUERY_PARITY"]:assert x in s,x
print("OPENALEX_UI_API_SEMANTICS_OBSERVATION_PASS")
