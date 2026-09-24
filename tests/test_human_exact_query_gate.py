from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'prototype/app.js').read_text()
for x in ['Exact targeted query · HUMAN','kosong = jangan eksekusi','retrieval-exact-query','allow&&exactQuery?"OpenAlex":"NOT_SELECTED"','MENUNGGU EKSEKUSI HUMAN']: assert x in s
print('HUMAN_EXACT_QUERY_GATE_PASS')
