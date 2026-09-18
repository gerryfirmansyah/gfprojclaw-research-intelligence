# J14 Pilot Production Activation Runbook v0

## Scope
Deterministic activation procedure after an authorized infrastructure path provisions the dedicated OS identity `gfproj-pilot`. This runbook does not authorize account creation, PostgreSQL auth changes, or scheduler activation by itself.

## Preconditions
1. `gfproj-pilot` exists as a non-login/system service identity and is not reused by Cockpit.
2. Repository is clean and the reviewed templates under `ops/` match this runbook.
3. Legacy `gfprojclaw-status-telegram.timer` remains disabled/inactive.
4. PostgreSQL roles `gfproj_pilot_executor` and `gfproj_pilot_worker` exist with the reviewed least-privilege boundary.
5. A rollback operator and maintenance window are explicitly identified before auth-file changes.

## Activation sequence
1. Record baseline: OS identity, PostgreSQL auth-file checksums, scheduler state, and HumanDecision row count.
2. Add the reviewed `gfproj_pilot_map` line from `ops/pg_ident.gfproj-pilot.example`.
3. Add the dedicated HBA rule from `ops/pg_hba.gfproj-pilot.example` before generic `local all all peer`.
4. Validate PostgreSQL configuration before reload; if validation fails, restore baseline and stop.
5. Reload PostgreSQL only; do not restart unrelated services.
6. As OS identity `gfproj-pilot`, verify Unix-socket login resolves to session user `gfproj_pilot_executor`.
7. Verify explicit `SET ROLE gfproj_pilot_worker` succeeds and fail-closed privilege assertions pass.
8. Verify HumanDecision INSERT/UPDATE remain false and no broad scientific write authority was introduced.
9. Run one bounded MANUAL canonical pilot with a unique idempotency key; verify stage history, local failure/recovery semantics, and automatic scientific decisions = 0.
10. Verify Cockpit/Radar operational observability and HumanDecision count unchanged by the pilot.
11. Obtain explicit HUMAN acceptance of the end-to-end manual production-identity trial.
12. Only after acceptance, install the reviewed canonical service/timer with real project-scoped invocation and reviewed schedule. Do not repurpose the legacy timer.
13. Validate unit files, daemon-reload, start one service invocation manually, inspect canonical results, then obtain HUMAN acceptance before enabling the timer.

## Fail-closed / rollback
- Any unexpected database identity or privilege: stop; do not schedule.
- Any HumanDecision write authority: guardrail breach; restore auth/configuration and investigate.
- Any auth validation failure: restore original pg_ident/pg_hba and reload the previously valid configuration.
- Any pilot failure remains source/project local; do not globally lock unrelated research projects.
- Never delete failed pilot envelopes/stage history merely to make acceptance pass.

## Acceptance evidence
Capture: OS identity facts; session_user/current_user; privilege matrix; auth-file checksums before/after; MANUAL run id/idempotency key; per-source stage attempts; Radar failure/recovery metrics; automatic scientific decisions metric; HumanDecision count before/after; legacy timer state; HUMAN acceptance statement.

## Current status
BLOCKED: `gfproj-pilot` has not yet been provisioned through an authorized infrastructure path. Offline templates are review artifacts only; production auth and scheduler remain unchanged.
