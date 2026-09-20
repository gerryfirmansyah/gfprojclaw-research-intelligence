from pathlib import Path
c=Path('ops/Caddyfile').read_text(); i=Path('ops/j16/install_admin_auth.sh').read_text(); v=Path('ops/j16/verify_admin_auth.sh').read_text()
assert '@admin_api path /api/admin/*' in c and c.index('@admin_api') < c.index('handle /api/*')
assert '{$GFPROJ_ADMIN_USER} {$GFPROJ_ADMIN_PASSWORD_HASH}' in c
assert '/etc/gfprojclaw/admin-auth.env' in i and 'chmod 0600' in i
assert 'GFPROJ_ADMIN_PASSWORD=' not in i
assert 'admin_unauth=401' in v
print('ADMIN_AUTH_ASSETS_PASS')
