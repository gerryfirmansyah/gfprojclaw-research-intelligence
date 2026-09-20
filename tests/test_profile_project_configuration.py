from pathlib import Path
c=Path('prototype/api/context.py').read_text(); s=Path('prototype/api/server.py').read_text(); a=Path('prototype/app.js').read_text(); admin=Path('prototype/admin.js').read_text()
assert 'update_profile_project_configuration' in c
assert 'supersedes_version_id' in c and "'scientific_decision':False" in c and "'atomic':True" in c
assert '/api/admin/profile-project-configuration' in admin and 'profile-project-configuration' in s
profile_view=a[a.index('function renderProfiles()'):a.index('function renderTelegram()')]
assert 'save-profile-config' not in profile_view and 'save-project-config' not in profile_view
assert 'hanya dapat dikonfigurasi melalui Admin Copilot' in profile_view
assert 'Preview changes' in admin and 'Reason for configuration change' in admin
assert 'DATA DUMMY' not in profile_view
print('PROFILE_PROJECT_CONFIGURATION_PASS')
