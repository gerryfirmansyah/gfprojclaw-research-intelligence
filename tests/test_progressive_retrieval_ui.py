from pathlib import Path
h=Path("prototype/explorer.html").read_text();j=Path("prototype/explorer.js").read_text();c=Path("prototype/styles.css").read_text()
for x in ["Progressive Retrieval Funnel","Provider reported","Retrieved","Not retrieved","Deduplicated","Screened","HUMAN reviewed","Project Corpus","bukan batas Research Universe","bukan berarti tidak relevan"]:assert x in h,x
for x in ["renderProgressiveFunnel","NOT_AVAILABLE","NOT_RECORDED","NOT_RUN"]:assert x in j,x
assert ".retrieval-funnel" in c
assert 'method:"POST"' not in j and 'method:"PUT"' not in j
print("PROGRESSIVE_RETRIEVAL_UI_PASS")
