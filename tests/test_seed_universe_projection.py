from pathlib import Path
c=Path("prototype/api/context.py").read_text(); s=Path("prototype/api/server.py").read_text()
for x in ["def get_project_seed_universe(project_id):","PROJECT_CORPUS_SEED","observed_universe_state","seeds_are_universe","discovery_is_evidence","gap_proven","novelty_proven","scientific_decision","terminology_candidates","LEXICAL_FROM_SEED_TITLES_V1","MACHINE_DERIVED_NOT_HUMAN_APPROVED","phrase_candidates","query_family_candidates","EXACT_PHRASE_IN_SEED_TITLE","OPTION_NOT_HUMAN_APPROVED","offered as a discovery option"]:
    assert x in c,x
assert 'parts[3] == "seed-universe"' in s
assert 'get_project_seed_universe(parts[2])' in s
print("SEED_UNIVERSE_PROJECTION_PASS")
