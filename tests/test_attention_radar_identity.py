from pathlib import Path
s=Path('tools/send_attention_radar.py').read_text()
assert "f'{API}/api/context'" in s
assert "c['profile_name']" in s and "c['project_name']" in s
assert "c.get('research_intent') or c.get('profile_summary')" in s
assert "PROJECTS=" not in s
assert 'scientific' not in s.lower() or 'keputusan ilmiah tetap milik HUMAN' in s
print('ATTENTION_RADAR_IDENTITY_PASS')
