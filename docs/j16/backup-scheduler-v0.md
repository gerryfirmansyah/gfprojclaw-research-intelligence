# J16 Backup Scheduler v0

- `gfprojclaw-backup.timer` runs daily at approximately 02:30 Asia/Jakarta with up to 10 minutes randomized delay and `Persistent=true` for missed-run recovery.
- `gfprojclaw-backup.service` runs as `gfproj:gfproj`, creates a PostgreSQL custom-format dump plus SHA-256 sidecar, validates the archive list, then applies retention.
- Default local retention is 14 days (`GFPROJ_BACKUP_RETENTION_DAYS` may override with a non-negative integer).
- Backup files remain mode 0600 in `/opt/gfprojclaw/backups`.
- Manual service execution on 2026-09-20 completed with `Result=success`, `ExecMainStatus=0`, creating `gfprojclaw-20260920T150558+0700.dump`.
- This scheduler is operational backup automation only. It does not activate the continuous research pilot or make scientific decisions.
