from pathlib import Path
c=Path('ops/Caddyfile').read_text(); j=Path('prototype/admin.js').read_text(); h=Path('prototype/admin.html').read_text()
assert '@admin_ui path /admin /admin/ /admin/*' in c
assert 'root * /opt/gfprojclaw/admin-web' in c
assert c.count('basicauth') >= 2
assert 'location.hostname === "api.116.212.72.79.nip.io" ? ""' in j
assert 'https://gerryfirmansyah.github.io/gfprojclaw-research-intelligence/prototype/' in h
print('ADMIN_SAME_ORIGIN_PASS')
