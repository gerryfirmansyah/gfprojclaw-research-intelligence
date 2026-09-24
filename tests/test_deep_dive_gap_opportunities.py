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

assert 'selectedGapOpportunity' in js
assert 'selected_gap_opportunity:selectedGapOpportunity' in js
app=(root/'prototype/app.js').read_text()
assert 'selected_gap_opportunity' in app
assert 'Gap Opportunity dipilih HUMAN' in app
