from pathlib import Path
h=Path("prototype/explorer.html").read_text();j=Path("prototype/explorer.js").read_text()
for x in ["Seed → Research Universe","seed-universe-state","seed-paper-list","seed-query-options","explorer.js"]: assert x in h,x
for x in ["/seed-universe","seed_count","observed_universe_state","query_family_candidates","seed_work_ids","Scientific decision: false","Seed ≠ Universe","Discovery ≠ Evidence","NOT APPROVED"]: assert x in j,x
assert 'method:"POST"' not in j and 'method:"PUT"' not in j
print("RESEARCH_EXPLORER_SEED_UI_PASS")
