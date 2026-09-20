from pathlib import Path
c=Path('prototype/api/context.py').read_text(); s=Path('prototype/api/server.py').read_text()
assert 'def get_project_daily_attention' in c
assert "pwr.first_seen_at >= now()" in c
assert "c.created_at >= now()" in c
assert "('CHALLENGES','CONTRADICTS')" in c
assert "a.assessed_at >= now()" in c
assert "c.review_state IN ('NEEDS_REVIEW','CONTESTED')" in c
assert "'scientific_decision':False" in c
assert 'daily-attention' in s
print('DAILY_ATTENTION_PROJECTION_PASS')
