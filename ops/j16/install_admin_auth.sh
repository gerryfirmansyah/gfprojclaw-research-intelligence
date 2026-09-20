#!/usr/bin/env bash
set -euo pipefail
: "${GFPROJ_ADMIN_USER:?set GFPROJ_ADMIN_USER out-of-band}"
: "${GFPROJ_ADMIN_PASSWORD:?set GFPROJ_ADMIN_PASSWORD out-of-band}"
install -d -m 0700 -o root -g root /etc/gfprojclaw
hash="$(caddy hash-password --plaintext "$GFPROJ_ADMIN_PASSWORD")"
printf 'GFPROJ_ADMIN_USER=%s\nGFPROJ_ADMIN_PASSWORD_HASH=%s\n' "$GFPROJ_ADMIN_USER" "$hash" > /etc/gfprojclaw/admin-auth.env
chmod 0600 /etc/gfprojclaw/admin-auth.env
unset GFPROJ_ADMIN_PASSWORD
printf '%s\n' 'Credential material installed outside Git. Configure Caddy service EnvironmentFile before activation.'
