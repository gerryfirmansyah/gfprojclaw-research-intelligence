from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'prototype/explorer.html').read_text()
for x in ['Alur review HUMAN','Pilih area → 2. Perdalam konteks','Batas yang perlu Anda ketahui','Evaluasi sistem — buka setelah selesai melakukan flow riset','apa yang harus dianggap benar-benar baru']: assert x in s
print('RESEARCH_FLOW_REVIEW_SURFACE_PASS')
