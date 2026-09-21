from pathlib import Path
s=Path('docs/j16/research-scope-coverage-alert-contract-v0.md').read_text()
for x in ['Observation','Explanation','Uncertainty','Options','HUMAN decision','Re-observation','Scope Ladder','SCOPE_COVERAGE_ATTENTION','COUNTER_SEARCH_NOT_RUN','LANDSCAPE_CHANGE','A low paper count alone MUST NOT','Research Universe is UNKNOWN','counter-search is NOT_RUN','record-level discovery provenance','Preserve scientific decisions for HUMAN']:
    assert x in s, x
print('RESEARCH_SCOPE_ALERT_CONTRACT_PASS')
