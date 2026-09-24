from pathlib import Path
r=Path(__file__).resolve().parents[1];a=(r/'prototype/app.js').read_text();checks={'human authors reflection':'Sistem tidak mengisi jawaban ini.' in a,'captures clearer':'reflection-clearer' in a,'captures uncertainty':'reflection-uncertain' in a,'captures changing evidence':'reflection-evidence' in a,'captures intended action':'reflection-next' in a,'noncanonical':'canonical_write:false' in a,'nonscientific':'scientific_decision:false' in a,'review basis':'based_on_human_review:true' in a};assert all(checks.values()),checks
print('HUMAN_LEARNING_LOOP_CONTRACT_PASS')
