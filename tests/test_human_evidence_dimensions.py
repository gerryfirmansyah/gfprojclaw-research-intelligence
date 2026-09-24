from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'prototype/app.js').read_text()
for x in ['data-dim="context"','data-dim="method"','data-dim="unit"','data-dim="outcome"','data-dim="mechanism"','dimensions:Object.fromEntries','bukan jumlah vote saja']: assert x in s
print('HUMAN_EVIDENCE_DIMENSIONS_PASS')
