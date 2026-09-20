from pathlib import Path
c=Path('prototype/api/context.py').read_text(); s=Path('prototype/api/server.py').read_text()
for x in ['get_project_corpus_layers','research_universe','discovery_corpus','deduplicated_corpus','screening_corpus','project_corpus','evidence_corpus','human_reviewed_evidence','scientific_decision']:
 assert x in c,x
assert 'corpus-layers' in s
print('CORPUS_LAYERS_PROJECTION_PASS')
