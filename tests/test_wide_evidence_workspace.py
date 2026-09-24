from pathlib import Path
css=(Path(__file__).resolve().parents[1]/'prototype/styles.css').read_text();js=(Path(__file__).resolve().parents[1]/'prototype/explorer.js').read_text()
for x in ['min-width:1540px','max-height:68vh','position:sticky','width:390px','width:calc(100vw - 72px)']: assert x in css
for x in ['— belum diverifikasi','Scroll horizontal untuk membandingkan kolom','judul paper tetap di kiri']: assert x in js
print('WIDE_EVIDENCE_WORKSPACE_PASS')
