from pathlib import Path
s=Path('prototype/app.js').read_text()
for d in ['ACCESS_COMPLETENESS','PROVENANCE_COMPLETENESS','EXTRACTION_REVIEW_STATE','METHODOLOGICAL_CONTEXT_AVAILABILITY','CORROBORATION_CONTEXT','CONTRADICTION_CONTEXT','RECENCY_CONTEXT','SOURCE_COVERAGE_LIMITATIONS']:
    assert d in s
for phrase in ['Apa artinya?','Kondisi saat ini','Mengapa penting?','Yang perlu HUMAN periksa','Detail teknis / canonical','bukan skor kualitas riset','Keterlacakan tidak berarti Claim otomatis benar','counter-search NOT_RUN']:
    assert phrase in s, phrase
assert 'traceable_relationships??0' in s and 'linked_relationships??0' in s
assert 'scientific_decision=' in s
print('QUALITY_HUMAN_EXPLANATION_PASS')
