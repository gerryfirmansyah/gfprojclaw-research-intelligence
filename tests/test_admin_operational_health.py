from pathlib import Path
s=Path('prototype/api/server.py').read_text(); a=Path('prototype/admin.js').read_text(); h=Path('prototype/admin.html').read_text()
assert '/api/admin/operational-health' in s and 'scientific_decision":False' in s
for unit in ['gfprojclaw-cockpit-api.service','gfprojclaw-status-telegram.timer','gfprojclaw-backup.timer','gfprojclaw-g6-g9.service','gfprojclaw-continuous-pilot.timer']: assert unit in s
assert 'admin-ops-health' in h and 'Production Health' in h
assert 'loadOperationalHealth' in a and 'Latest backup' in a and 'Legacy G6–G9' in a
print('ADMIN_OPERATIONAL_HEALTH_PASS')
