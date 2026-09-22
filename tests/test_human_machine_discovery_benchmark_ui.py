from pathlib import Path
h=Path("prototype/explorer.html").read_text();j=Path("prototype/explorer.js").read_text()
for x in ["Discovery Verification","Bandingkan pencarian HUMAN dengan mesin","bench-source","bench-time","bench-total","bench-captured","bench-query","bench-members","Preview benchmark"]: assert x in h,x
for x in ["HUMAN observation draft","NON_PARITY_COMPARISON","PARITY_REQUIRES_REVIEW","Overlap / HUMAN-only / Machine-only","NOT_AVAILABLE","no canonical write","scientific decision: false"]: assert x in j,x
assert 'method:"POST"' not in j and 'method:"PUT"' not in j
print("HUMAN_MACHINE_DISCOVERY_BENCHMARK_UI_PASS")
