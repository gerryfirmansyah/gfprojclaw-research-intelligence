from pathlib import Path
s=Path('docs/j16/simple-end-to-end-research-trial-v0.md').read_text()
for x in ['## Ten-step HUMAN journey','Claim → EvidenceFragment → Work/source','ABSTRACT_ONLY','NOT_AVAILABLE','NOT_RUN','Writer `--apply`','Continuous Pilot','explicit HUMAN judgment','replacement-environment replication']:
    assert x in s,x
assert s.count('\n1. **Define intent**')==1 and '\n10. **Continue research**' in s
assert Path('docs/j16/simple-e2e-trial-observation-template.md').exists()
print('SIMPLE_E2E_TRIAL_CONTRACT_PASS')
