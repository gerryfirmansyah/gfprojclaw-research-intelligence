# J15 ChangeEvent Executable Validation Checkpoint v0

Date: 2026-09-20
Status: EXECUTABLE DISPOSABLE TEST PASS — production deployment not authorized

## Candidate baseline

Commit: `13d3f5075921a1f547caef304981fdd0b3400f8f`

Artifacts under test:
- `db/migrations/011_change_event_canonical_traceability.sql`
- `db/migrations/012_change_event_traceability_privileges.sql`
- `db/verify/011_change_event_traceability_verify.sql`
- `db/verify/011_change_event_traceability_negative.sql`
- `.github/workflows/j15-change-event-traceability-postgres.yml`
- canonical Assessment ChangeEvent writer update.

## Executable evidence

GitHub Actions run `35480069252`, PostgreSQL 16 disposable service: PASS.

Passed steps:
- canonical baseline migration;
- deterministic cross-domain fixture;
- Migration 011;
- runtime role creation;
- Migration 012 bounded privileges;
- J15 schema verifier;
- J15 negative integrity tests;
- zero historical `change_event_evidence` backfill assertion;
- runtime privilege assertion: SELECT+INSERT, no UPDATE/DELETE.

Negative integrity rejections confirmed:
- ASSESSMENT_CHANGED without current Assessment;
- invalid evidence role;
- cross-object EvidenceRelationship;
- cross-object current Assessment.

## Correction history

The first executable run `35480019858` failed because `MATCH FULL` cannot represent the initial Assessment transition where current Assessment/project/object are non-null and supersedes is null. The candidate was corrected to `MATCH SIMPLE`, with independent current-Assessment lineage FK and transition checks retained. The second run passed.

## Scientific and deployment boundary

This checkpoint establishes executable persistence integrity only. It does not establish scientific truth, gap validity, novelty, significance, or HUMAN acceptance.

No production migration has been applied.
No historical evidence trigger membership has been inferred.
No continuous-pilot timer is authorized.
J15 remains IN PROGRESS / HUMAN TRIAL.
Production deployment of Migrations 011/012 requires a separate HUMAN deployment decision.
