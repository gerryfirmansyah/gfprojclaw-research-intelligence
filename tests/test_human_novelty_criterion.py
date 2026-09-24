from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'prototype/app.js').read_text()
for x in ['apa yang harus dianggap benar-benar baru?','retrieval-novelty-criterion','novelty_criterion:noveltyCriterion','baseline_subset:"smart → city → urban · 19 abstracts"']: assert x in s
print('HUMAN_NOVELTY_CRITERION_PASS')
