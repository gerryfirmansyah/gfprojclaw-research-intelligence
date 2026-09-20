from pathlib import Path
c=Path('prototype/api/context.py').read_text(); s=Path('prototype/api/server.py').read_text(); a=Path('prototype/app.js').read_text()
assert 'update_research_profile' in c and 'update_research_project' in c
assert 'supersedes_version_id' in c and "'scientific_decision':False" in c
assert 'def do_PUT' in s and '/api/profiles/' in a and '/api/projects/' in a
assert 'Simpan versi Profil baru' in a and 'Simpan versi Proyek baru' in a
assert 'DATA DUMMY' not in a[a.index('function renderProfiles()'):a.index('function renderTelegram()')]
print('PROFILE_PROJECT_CONFIGURATION_PASS')
