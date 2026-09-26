from pathlib import Path
a=Path("prototype/app.js").read_text();c=Path("prototype/styles.css").read_text()
for x in ["OBSERVATION","COMPARE SIGNAL","RECLASSIFICATION","COUNTER-EVIDENCE","Apa arti pola ini?","Cari counter-evidence nyata","Uji context sensitivity","Uji method dependence","Periksa batas evidence","Evidence yang mendasari (${rows.length})","validated research gap"]: assert x in a,x
assert 'challenge candidate → SUPPORTS oleh HUMAN' in a
assert '.io-impact' in c and '.io-evidence-details' in c
print("OPPORTUNITY_REASONING_SURFACE_PASS")
