from pathlib import Path
s=Path("tools/count_bounded_universe.py").read_text()
for x in ["TRIAL_COUNT_ONLY","from_publication_date","to_publication_date","from-pub-date","until-pub-date","records_retrieved_for_landscape\":0","ranking_used_for_landscape\":False","canonical_write\":False","scientific_decision\":False"]:assert x in s,x
for bad in ["INSERT INTO","UPDATE ","DELETE FROM","psycopg"]:assert bad not in s,bad
print("BOUNDED_UNIVERSE_COUNT_PASS")
