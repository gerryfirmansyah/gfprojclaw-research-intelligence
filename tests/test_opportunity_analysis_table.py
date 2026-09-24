from pathlib import Path
h=(Path(__file__).resolve().parents[1]/'prototype/explorer.html').read_text();j=(Path(__file__).resolve().parents[1]/'prototype/explorer.js').read_text()
for x in ['opportunity-analysis']: assert x in h
for x in ['ANALYSIS AWAL','Compare & Contrast','Metodologi','Unit analisis','Hasil/temuan','Mekanisme','— belum diverifikasi','showOpportunityAnalysis(o,path,members)']: assert x in j
print('OPPORTUNITY_ANALYSIS_TABLE_PASS')
