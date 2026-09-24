from pathlib import Path
for f,required in {
 'tools/retrieve_openalex_bounded_universe.py':['TRIAL_NON_CANONICAL_WHOLE_BOUNDED_METADATA','complete_against_reported_total','checkpoint scope mismatch','scientific_decision'],
 'tools/analyze_bounded_universe.py':['MACHINE_OBSERVATION_NOT_SCIENTIFIC_TRUTH','duplicate_openalex_ids','title_terms','scientific_decision'],
 'tools/build_researcher_landscape.py':['RESEARCHER_VISIBLE_TRIAL_LANDSCAPE','human_next_actions','verify DOI/source','scientific_decision'],
 'tools/build_why_trace.py':['EVERY_WHY_INSPECTABLE_BACK_TO_WHAT','supporting_observation','members','scientific_decision'],
}.items():
 s=Path(f).read_text()
 for x in required: assert x in s,(f,x)
 for bad in ['INSERT INTO','UPDATE ','DELETE FROM','psycopg']:
  assert bad not in s,(f,bad)
print('BOUNDED_UNIVERSE_TRIAL_PIPELINE_PASS')
for f,required in {
 'tools/deduplicate_bounded_universe.py':['normalized exact DOI','deduplicated_count','scientific_decision'],
 'tools/build_paper_inspector.py':['HUMAN_PAPER_INSPECTOR_PAYLOAD_TRIAL','NOT_RETRIEVED_IN_THIS_TRIAL','INSPECT_BEFORE_SCIENTIFIC_USE'],
 'tools/build_coverage_learning.py':['Absence from this observed OpenAlex/query/time-bounded corpus is not evidence of absence from research.','RECONSIDER_QUERY','scientific_decision'],
}.items():
 s=Path(f).read_text()
 for x in required: assert x in s,(f,x)

server=Path("prototype/api/server.py").read_text();html=Path("prototype/explorer.html").read_text();js=Path("prototype/explorer.js").read_text()
for x in ["/api/trial/research-value/","deduplicated_researcher_landscape.json","deduplicated_why_trace.json","deduplicated_paper_inspector.json","deduplicated_coverage_learning.json"]:assert x in server,x
for x in ["Lanskap seluruh semesta terbatas yang teramati","Cakupan & pembelajaran HUMAN","HUMAN yang memutuskan"]:assert x in html,x
for x in ["showTrialArea","anggota tepat berdasarkan istilah pada judul","bukan keputusan ilmiah mesin"]:assert x in js,x
print("RESEARCHER_TRIAL_SURFACE_PASS")
audit=Path('tools/audit_research_value_trial.py').read_text()
for x in ['raw_coverage_complete','paper_inspector_covers_corpus','why_members_are_corpus_members','why_has_provenance','no_scientific_decision','no_canonical_write']:assert x in audit,x
print('RESEARCH_VALUE_EXECUTABLE_AUDIT_CONTRACT_PASS')
html=Path('prototype/explorer.html').read_text();js=Path('prototype/explorer.js').read_text();protocol=Path('docs/j16/research-value-trial-human-acceptance-protocol-v0.md').read_text()
for x in ['Gerbang Penerimaan HUMAN','accept-landscape','accept-why','accept-trace','accept-limits','accept-rationale']:assert x in html,x
for x in ['SIAP UNTUK CATATAN PENERIMAAN HUMAN','tidak dapat menyatakan sendiri bahwa dirinya bermanfaat secara ilmiah']:assert x in js,x
for x in ['ENGINE FREEZE EXCEPT ACCEPTANCE-BLOCKING DEFECTS','ACCEPT','PARTIAL','REJECT / REWORK','system MUST NOT assign the verdict automatically']:assert x in protocol,x
print('HUMAN_ACCEPTANCE_GATE_CONTRACT_PASS')
html=Path('prototype/explorer.html').read_text();js=Path('prototype/explorer.js').read_text();css=Path('prototype/styles.css').read_text()
for x in ['Saran Riset','MENGAPA → Saran → paper anggota yang tepat','trial-paper-count']:assert x in html,x
for x in ['Apa yang kami amati','Mengapa ini mungkin penting','Apa yang perlu diperiksa berikutnya','Pertanyaan untuk Anda','Frekuensi saja tidak membuktikan relevansi']:assert x in js,x
for x in ['trial-paper-box','max-height:560px','overflow:auto']:assert x in css,x
print('HUMAN_ADVICE_EXPERIMENT_CONTRACT_PASS')
