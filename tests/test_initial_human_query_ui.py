from pathlib import Path
h=Path("prototype/explorer.html").read_text();j=Path("prototype/explorer.js").read_text()
for x in ["Initial HUMAN Query","initial-human-query","digital government","Gunakan sebagai baseline preview","bukan penggantian query historis J14"]: assert x in h,x
for x in ["HUMAN_PROVIDED","LOCAL_PREVIEW","canonical write: false","scientific decision: false","historical J14 query unchanged"]: assert x in j,x
assert 'method:"POST"' not in j and 'method:"PUT"' not in j
print("INITIAL_HUMAN_QUERY_UI_PASS")
