# J16 Production & Replication Contract v0

Status: IN PROGRESS — BASELINE AUDIT

## Purpose
J16 makes the accepted J0–J15 GFPROJCLAW baseline safe to leave running as a production service and reproducible on a replacement environment without transferring scientific authority from HUMAN to machine.

## Scope
1. Deployment and restart behavior: deterministic start/restart/reboot behavior without canonical-state corruption.
2. Backup and recovery: PostgreSQL plus required configuration/state, with an executable restore test.
3. Secrets and permissions: credentials outside source control, ownership/least privilege, and separated runtime/DBA authority.
4. Health monitoring: API, database, service, scheduler/source-pilot, storage, and failure visibility.
5. Scheduler reliability: idempotency, retry/local-failure behavior, restart/reboot/missed-run semantics, and observability.
6. Replication/setup: documented setup on a replacement environment without undocumented server knowledge.
7. Operational runbook: install, deploy, restart, backup, restore, rollback, monitoring, troubleshooting, and emergency procedure.
8. Production acceptance: preserve Profile A/B behavior and all scientific-authority invariants.
9. Replication acceptance: demonstrate operational equivalence and preserved canonical/scientific boundaries on a clean/disposable target.
10. Final HUMAN production acceptance.

## Invariants
- J0–J15 HUMAN-accepted scientific behavior is the baseline and must not be silently changed by J16.
- HUMAN remains scientific authority; production automation may not create scientific acceptance/rejection or final scientific verdicts.
- Missing context remains UNKNOWN / NOT_AVAILABLE / NOT_RUN as applicable.
- ABSTRACT_ONLY must never be represented as FULL_TEXT.
- Failures remain local; no global scientific lock is introduced.
- Secrets must not be committed to Git.
- Runtime roles remain least-privileged; DBA authority is not granted to application workers.
- Backup success is not inferred from file creation alone; restore must be tested.
- Replication success requires executable evidence, not documentation alone.
- Continuous-pilot scheduler activation remains a separate controlled production action and is not authorized merely by entering J16.

## Non-goals
J16 does not add new scientific intelligence, prove gaps/novelty/significance/causality/relevance, rewrite accepted J0–J15 scientific semantics, or create synthetic committed production scientific history.

## Acceptance evidence
J16 is ready for final HUMAN production acceptance only when deployment/restart, backup/restore, secrets/permissions, health monitoring, scheduler reliability, replication/setup, operational runbook, Profile A/B regression, and scientific-boundary checks have executable evidence. Final production readiness is declared only by HUMAN.
