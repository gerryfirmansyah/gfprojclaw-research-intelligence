from pathlib import Path
a=Path("prototype/app.js").read_text()
assert 'The Explorer handoff is an arrival stage' in a
assert 'handoff.hidden = true' in a
assert 'if (!view) return' in a
assert 'view.scrollIntoView({block:"start"})' in a
print("COPILOT_NAV_AFTER_HANDOFF_PASS")
