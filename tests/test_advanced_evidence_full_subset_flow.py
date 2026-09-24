from pathlib import Path
r=Path(__file__).resolve().parents[1];s=(r/'prototype/explorer.js').read_text()
assert 'supporting_papers:o.papers.map(' in s
assert 'const support=o.papers;detail.innerHTML=' in s
assert 'supporting_papers:o.papers.slice(0,6)' not in s
assert 'const support=o.papers.slice(0,6)' not in s
print('ADVANCED_EVIDENCE_FULL_SUBSET_FLOW_PASS')
