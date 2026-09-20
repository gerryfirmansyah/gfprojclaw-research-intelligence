from pathlib import Path
s=Path('prototype/api/server.py').read_text(); j=Path('prototype/admin.js').read_text()
assert '/api/admin/activity-audit' in s and 'gfprojclaw-activity.log' in s
assert 'scientific_decision":False' in s
assert 'loadAudit' in j and '/api/admin/activity-audit' in j
print('ADMIN_ACTIVITY_PASS')
