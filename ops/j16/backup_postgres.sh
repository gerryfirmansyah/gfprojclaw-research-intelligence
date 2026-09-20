#!/bin/bash
set -euo pipefail
umask 077
source /opt/gfprojclaw/config/runtime.env
out="/opt/gfprojclaw/backups/gfprojclaw-$(date +%Y%m%dT%H%M%S%z).dump"
export PGPASSWORD="$GFPROJ_DB_PASSWORD"
pg_dump -h "$GFPROJ_DB_HOST" -p "$GFPROJ_DB_PORT" -U "$GFPROJ_DB_USER" -d "$GFPROJ_DB_NAME" -Fc --no-owner --no-acl -f "$out"
pg_restore --list "$out" >/dev/null
sha256sum "$out" > "$out.sha256"
printf 'GFPROJCLAW_BACKUP_OK %s\n' "$out"
