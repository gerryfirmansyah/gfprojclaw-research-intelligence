from pathlib import Path
c=Path('prototype/api/context.py').read_text(); s=Path('prototype/api/server.py').read_text()
for x in ['def get_project_exploration(project_id):',"'stage':'RESEARCH_EXPLORER'","'state':'AVAILABLE' if sessions else 'NOT_RECORDED'",'This does not mean exploration did not occur or that coverage is complete.',"'scientific_decision':False",'research_scope_node','discovery_query_family','discovery_query','discovery_observation','source_key']:
    assert x in c,x
assert 'parts[3] == "exploration"' in s
assert 'get_project_exploration(parts[2])' in s
print('RESEARCH_EXPLORER_PROJECTION_PASS')
