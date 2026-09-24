from pathlib import Path
r=Path(__file__).resolve().parents[1]; j=(r/'prototype/explorer.js').read_text()
for x in ['advanced-evidence-detail','Supporting papers untuk diperiksa','Counter-evidence candidates (','Baca abstract','Bawa opportunity + evidence ke Research Copilot','selectedGapOpportunity={id:`ADV-','ketidakcocokan keyword bukan counter-evidence']: assert x in j
print('ADVANCED_EVIDENCE_INSPECTION_PASS')
