# GFPROJCLAW J16 Operations Runbook v0

## Boundaries
Production operations do not grant scientific authority. Never infer scientific rejection/acceptance from service, scheduler, source, or backup state. Do not enable `gfprojclaw-continuous-pilot.timer` as part of ordinary J16 operations.

## Health
Check Admin Copilot Production Health or `GET /api/admin/operational-health`. Expected baseline: Cockpit API active; Telegram and backup timers enabled/active; Continuous Pilot timer absent/inactive. Legacy G6–G9 is historical, disabled, and must not be restarted without a separate architecture decision.

## Restart / deploy
Repository: `/opt/gfprojclaw-research-intelligence`. API unit runs as `gfproj:gfproj` with `Restart=on-failure`. After an approved deploy, syntax/regression checks precede `systemctl restart gfprojclaw-cockpit-api`; then verify `/api/context` and operational health.

## Secrets and permissions
Runtime DB credentials live outside Git at `/opt/gfprojclaw/config/runtime.env` (0600, gfproj:gfproj); config directory is 0700. Never print or commit credential values. Backup directory is 0700 and dumps are 0600.

## Backup
`gfprojclaw-backup.timer` runs daily around 02:30 Asia/Jakarta, Persistent=true. `gfprojclaw-backup.service` runs as gfproj and creates a custom-format dump, validates its archive listing, writes SHA-256, then prunes files older than the default 14-day retention.

## Restore
Never restore over production for a test. Copy a protected dump to a disposable PostgreSQL-readable temporary file, create a disposable database, restore with `pg_restore --no-owner --no-acl`, compare schema/key invariants, then delete the temporary copy and disposable DB. See `backup-restore-evidence-2026-09-20.md`.

## Troubleshooting
Keep failures local. Inspect the specific systemd unit/journal and canonical API projection. Missing data remains UNKNOWN / NOT_AVAILABLE / NOT_RUN. A provider or scheduler failure is operational evidence, not a scientific verdict.

## Emergency
Preserve PostgreSQL and `/opt/gfprojclaw/backups`; stop only the affected application/scheduler unit when isolation is required. Do not alter canonical scientific records to repair an operational incident. Record meaningful intervention in `/var/log/gfprojclaw-activity.log`.

## Admin access
Production Admin Copilot is served at `https://api.116.212.72.79.nip.io/admin/` behind HTTPS Basic Auth. The same credential boundary protects `/api/admin/*`. Credential material lives outside Git in `/etc/gfprojclaw/admin-auth.env` (0600, root:root). Deploy Admin static assets with `ops/j16/install_admin_static.sh`; never embed credentials in HTML/JavaScript. Public Research Copilot remains separate.

## Deployment rollback
Before replacing Caddy configuration, preserve the current `/etc/caddy/Caddyfile`, validate the candidate with the out-of-band environment, and reload only after validation. Existing pre-J16/Admin-auth copies are rollback evidence, but a rollback should use the immediately preceding known-good configuration. After reload verify Caddy active, public `/api/context` HTTP 200, unauthenticated `/admin/` and `/api/admin/*` HTTP 401, then HUMAN-authenticated Admin rendering.

## Current acceptance state
Local production hardening, backup/restore, scheduler visibility, Admin operational surface, Admin authentication, and production regressions have executable evidence. Replacement-environment replication is intentionally **DEFERRED — FINAL J16 GATE** until a disposable second Linux environment is provisioned. Documentation or another restore on this production host must not be called replication PASS. Final J16 HUMAN acceptance remains pending that executable replication evidence.
