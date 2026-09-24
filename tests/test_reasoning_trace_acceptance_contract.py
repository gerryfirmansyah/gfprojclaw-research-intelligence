from pathlib import Path
r=Path(__file__).resolve().parents[1];a=(r/'prototype/app.js').read_text();l=(r/'tools/build_research_loop_ledger.py').read_text();u=(r/'tools/audit_closed_research_loop.py').read_text()
checks={'ui asks how arrived':'Bagaimana saya sampai di sini?' in a,'session trace noncanonical':'NON-CANONICAL · scientific_decision=false' in a,'ledger fingerprints':'sha256' in l,'audit no scientific decision':'no stage scientific decision' in u,'audit no canonical write':'no stage canonical write' in u,'ui distinguishes ledger':'fingerprint provenance' in a}
assert all(checks.values()),checks
print('REASONING_TRACE_ACCEPTANCE_CONTRACT_PASS')
