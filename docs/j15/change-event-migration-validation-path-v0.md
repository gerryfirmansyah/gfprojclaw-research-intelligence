# J15 ChangeEvent Migration Validation Path v0

Date: 2026-09-20
Status: pre-migration validation checkpoint

## Findings

Production canonical tables are owned by postgres. The runtime role is gfproj_app and is intentionally not a superuser, role creator, or database creator. The failed ALTER TABLE dry-run therefore confirms the intended DDL authority boundary; gfproj_app must not be elevated for J15.

J2 already established the safe validation pattern:
1. disposable PostgreSQL 16 database;
2. migration apply as database owner;
3. production-safe schema verification;
4. deterministic fixture and negative integrity tests;
5. clean rebuild/re-apply checks;
6. only then production deployment as postgres.

The existing GitHub Actions workflow uses a PostgreSQL 16 service with POSTGRES_USER=postgres and creates disposable databases with createdb. This is the preferred place to validate the J15 migration proposal with owner-level DDL authority.

## J15 decision

Do not test owner-only J15 DDL by changing production runtime privileges.

Promote the proposal to an executable migration only together with J15-specific schema verification and negative tests in a disposable PostgreSQL 16 workflow.

Production application remains a separate HUMAN/deployment checkpoint after disposable tests pass.

## Current boundary

No production schema mutation is authorized by this checkpoint.
No historical evidence-trigger backfill is authorized.
No J15 HUMAN PASS is implied.
