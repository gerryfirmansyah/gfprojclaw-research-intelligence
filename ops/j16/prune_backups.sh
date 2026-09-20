#!/bin/bash
set -euo pipefail
backup_dir=/opt/gfprojclaw/backups
retention_days="${GFPROJ_BACKUP_RETENTION_DAYS:-14}"
[[ "$retention_days" =~ ^[0-9]+$ ]] || { echo 'invalid retention days' >&2; exit 2; }
find "$backup_dir" -maxdepth 1 -type f \( -name 'gfprojclaw-*.dump' -o -name 'gfprojclaw-*.dump.sha256' \) -mtime "+$retention_days" -print -delete
printf 'GFPROJCLAW_BACKUP_RETENTION_OK days=%s\n' "$retention_days"
