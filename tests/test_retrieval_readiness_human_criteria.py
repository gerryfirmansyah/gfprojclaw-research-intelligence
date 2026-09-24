from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'prototype/app.js').read_text()
for x in ['const ready=allow&&exactQuery&&noveltyCriterion','QUERY + NOVELTY CRITERION HUMAN','LENGKAPI OTORISASI, QUERY, DAN KRITERIA BARU']: assert x in s
print('RETRIEVAL_READINESS_HUMAN_CRITERIA_PASS')
