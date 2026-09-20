from pathlib import Path
s=Path('prototype/app.js').read_text()
for x in ['data-today-object','openObjectVerification','data-radar-object','Identifier eksternal canonical belum tersedia','Contoh tindakan HUMAN — ILUSTRATIF','Bukan tombol tindakan dan tidak menulis state apa pun']:
    assert x in s,x
assert 'onclick="showView(\'opportunities\')"' not in s
print('HUMAN_VERIFICATION_NAVIGATION_PASS')
