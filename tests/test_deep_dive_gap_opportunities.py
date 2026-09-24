from pathlib import Path
root=Path(__file__).resolve().parents[1]
html=(root/'prototype/explorer.html').read_text()
js=(root/'prototype/explorer.js').read_text()
assert 'deep-dive-opportunities' in html
assert 'Gap Opportunities' in html
assert 'function gapOpportunities' in js
assert 'Evidence Summary' in js
assert 'PRELIMINARY' in js
assert 'Opportunity bukan research gap' in js
assert 'Yang belum diketahui' in js
assert 'Verifikasi berikutnya' in js
assert 'Pilih opportunity ini' in js
assert 'updateDeepDive({...root,area:path.join' in js
assert 'scientific decision: false' in js
print('DEEP_DIVE_GAP_OPPORTUNITIES_PASS')
