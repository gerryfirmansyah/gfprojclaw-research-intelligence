from pathlib import Path
s=Path('prototype/app.js').read_text()
for x in ['corpus-layers','Peta lapisan corpus','Research Universe','Discovery Corpus (source-record observations; dapat overlap)','Deduplicated Corpus','Screening Corpus','Project Corpus','Evidence Corpus','HUMAN-reviewed Evidence','Project Corpus bukan ukuran seluruh literatur']:
 assert x in s,x
print('CORPUS_LAYERS_UI_PASS')
