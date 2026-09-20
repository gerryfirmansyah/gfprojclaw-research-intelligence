#!/usr/bin/env bash
set -euo pipefail
src="${1:-/opt/gfprojclaw-research-intelligence/prototype}"
dst="/opt/gfprojclaw/admin-web"
install -d -o root -g caddy -m 0750 "$dst"
for f in admin.html admin.js styles.css i18n.js; do
  install -o root -g caddy -m 0640 "$src/$f" "$dst/$f"
done
printf 'Admin static assets installed at %s\n' "$dst"
