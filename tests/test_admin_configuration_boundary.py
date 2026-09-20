from pathlib import Path
app=Path('prototype/app.js').read_text(); admin=Path('prototype/admin.js').read_text(); ctx=Path('prototype/api/context.py').read_text(); server=Path('prototype/api/server.py').read_text(); i18n=Path('prototype/i18n.js').read_text()
assert 'save-profile-config' not in app and 'save-project-config' not in app
assert 'hanya dapat dikonfigurasi melalui Admin Copilot' in app
assert 'Preview changes' in admin and 'Reason for configuration change' in admin
assert '/api/admin/profile-project-configuration' in admin and 'update_profile_project_configuration' in server
assert "FOR UPDATE" in ctx and "'atomic':True" in ctx and "'scientific_decision':False" in ctx
assert 'stageDescriptions' in i18n and 'stageDescription(index)' in app
assert 'Status dapat berubah kembali' not in app
print('ADMIN_CONFIGURATION_BOUNDARY_PASS')
