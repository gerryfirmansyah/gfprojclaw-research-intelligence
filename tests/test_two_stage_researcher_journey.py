from pathlib import Path

text = Path('docs/j16/two-stage-researcher-journey-v0.md').read_text()
explorer = Path('docs/j16/pre-research-exploration-journey-contract-v0.md').read_text()

for token in [
    'GFPROJCLAW has exactly two researcher stages',
    '**Research Explorer** — **Explore → Understand → Decide**',
    '**Research Copilot** — **Research → Review → Observe → Reconsider**',
    'Admin Copilot is not a research stage',
    'Research Explorer → HUMAN Scope Decision → Create/Transition Research Project → Research Copilot',
    'Research Explorer SHOULD be a product entry surface before the current project workspace',
    'MUST NOT silently modify project scope or scientific decisions',
]:
    assert token in text, token

assert 'Research Explorer' in explorer
assert 'internal Phase 0 / Pre-Research Exploration' in explorer
print('TWO_STAGE_RESEARCHER_JOURNEY_PASS')
