from pathlib import Path
h=Path('prototype/admin.html').read_text(); j=Path('prototype/admin.js').read_text(); css=Path('prototype/styles.css').read_text()
views=['overview','configuration','pilot','sources','failures','quarantine','services','audit','appearance']
for v in views:
 assert f'data-admin-view="{v}"' in h and f'data-admin-panel="{v}"' in h
assert 'setAdminView' in j and "location.hash=`admin-${name}`" in j
assert '.admin-view{display:none}' in css
assert 'NOT_AVAILABLE — no canonical quarantine projection' in h
assert 'NOT_AVAILABLE — richer canonical activity/audit projection' in h
print('ADMIN_NAVIGATION_PASS')
