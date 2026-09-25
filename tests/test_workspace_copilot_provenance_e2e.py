from pathlib import Path
w=Path("prototype/research-workspace.js").read_text(); a=Path("prototype/app.js").read_text(); c=Path("prototype/styles.css").read_text()
for x in ["openalex_url:p.source_url", "doi:rawDoi", "doi_url:doiUrl"]: assert x in w,x
for x in ["function evidenceLinks(a)", "OpenAlex ↗", "DOI ↗", "DOI tidak tersedia", 'paperHeading.textContent="Evidence Aktif"'] : assert x in a,x
assert '.evidence-links' in c
print("WORKSPACE_COPILOT_PROVENANCE_E2E_PASS")
