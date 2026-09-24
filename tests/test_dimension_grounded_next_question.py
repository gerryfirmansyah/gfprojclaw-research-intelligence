from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'prototype/app.js').read_text()
for x in ['dimSummary=contrast.map','Perbedaan yang dicatat HUMAN','Isi dimensi evidence agar pertanyaan berikutnya','Periksa khusus perbedaan yang dicatat HUMAN']: assert x in s
print('DIMENSION_GROUNDED_NEXT_QUESTION_PASS')
