# J16 Backup / Restore Evidence — 2026-09-20

Production backup `/opt/gfprojclaw/backups/gfprojclaw-20260920T144036+0700.dump` was created by `gfproj` with mode 0600. SHA-256 verification passed and `pg_restore --list` parsed the archive.

A temporary copy owned by PostgreSQL was restored into disposable database `gfprojclaw_j16_restore_20260920`; the protected original backup permissions were not relaxed. Restore completed without `pg_restore` error.

Post-restore invariants matched production: 76 public tables; `research_object_identity` 2; `work` 9; `claim` 5; `evidence_fragment` 5; `research_profile` 2; `research_project` 2.

The temporary restore copy and disposable database were deleted after verification. Production database was never a restore target. This evidence verifies executable recovery for this backup; retention/scheduling policy remains a separate J16 operational item.
