from pathlib import Path
r=Path(__file__).resolve().parents[1]
h=(r/'prototype/index.html').read_text(); j=(r/'prototype/app.js').read_text()
for x in ['handoff-gap','handoff-verification','handoff-start','Kembali ke Explorer']: assert x in h
for x in ['Hipotesis kerja untuk diuji','Verifikasi berikutnya','supporting evidence','counter-evidence','Scientific decision tetap milik HUMAN']: assert x in j
assert 'Pilih Gap Opportunity di Explorer terlebih dahulu' in j
print('GAP_OPPORTUNITY_COPILOT_VERIFICATION_PASS')
