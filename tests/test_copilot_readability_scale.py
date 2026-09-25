from pathlib import Path
c=Path("prototype/styles.css").read_text()
for x in ['.page-heading h1{font-size:32px}', '.metric-card span{font-size:14px}', '.panel-header h2{font-size:17px}', '.table{font-size:14px}', 'max-height:62vh;overflow:auto']:
 assert x in c,x
print("COPILOT_READABILITY_SCALE_PASS")
