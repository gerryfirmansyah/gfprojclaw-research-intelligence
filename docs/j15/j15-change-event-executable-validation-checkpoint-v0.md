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

## 2026-09-20 production-like DBA disposable rerun

Candidate commit: `b47f456683b6b66dd8d956ab7bd743cdf6655a89`.

An authorized DBA (`postgres`) ran the full disposable PostgreSQL 16 suite on the GFPROJCLAW VPS using a separate `gfprojclaw_j15_test` database. Result: `J15_DISPOSABLE_FULL_SUITE_PASS`.

The rerun reproduced the pre-migration historical `ASSESSMENT_CHANGED` condition and confirmed deterministic backfill with `UPDATE 1`. Migration 011 committed successfully, Migration 012 applied in the disposable database, the schema verifier passed, and the bounded runtime privilege assertions passed.

Integrity cases confirmed by executable test:
- `ASSESSMENT_CHANGED` without current Assessment is rejected;
- invalid evidence role is rejected;
- cross-object EvidenceRelationship is rejected;
- a current Assessment that canonically supersedes another Assessment cannot omit that predecessor from the ChangeEvent transition;
- the exact canonical predecessor -> current Assessment transition succeeds as a positive control;
- cross-object current Assessment is rejected;
- historical `change_event_evidence` remains empty rather than being inferred from current evidence.

This rerun also validates the historical UUID guard correction: GFPROJCLAW canonical hexadecimal UUIDs are accepted without imposing RFC version/variant nibbles that the canonical schema does not require.

### Deployment boundary after rerun

The executable blocker for Migration 011 is cleared for controlled production deployment. This is not J15 HUMAN PASS and does not authorize continuous-pilot timer activation. Production Migration 011 must be applied first and verified in production before Migration 012 is considered.

## 2026-09-20 controlled production deployment result

Status: MIGRATIONS 011 + 012 PRODUCTION PASS — J15 remains IN PROGRESS / HUMAN TRIAL.

Using the authorized PostgreSQL DBA identity on production `gfprojclaw` (PostgreSQL 16.15), Migration 011 completed in one transaction. The deterministic historical Assessment backfill reported `UPDATE 1`; the exact-supersession integrity function and constraint trigger were created; semantic constraints were added; and the transaction committed.

The production schema verifier then returned `J15 change-event traceability schema verification passed`.

The existing historical `ASSESSMENT_CHANGED` event `10d5b1f3-5248-5bba-9400-d3dd1b2de146` now has canonical `current_assessment_id = dea6a217-e8ec-49e9-9bed-0101b20185c3`, with both `previous_assessment_id` and `current_supersedes_assessment_id` NULL, consistent with the canonical initial Assessment. `change_event_evidence` contained zero rows after migration; no historical evidence-trigger membership was inferred.

Migration 012 then committed. Explicit production privilege verification for `gfproj_app` returned `t|t|f|f`: SELECT and INSERT are allowed on `change_event_evidence`; UPDATE and DELETE are not.

This production PASS establishes the persistence and bounded-runtime-privilege deployment checkpoint only. It does not establish scientific truth or HUMAN acceptance, does not authorize continuous-pilot timer activation, and does not by itself make ChangeEvent member traceability available through the API/UI. Writer `--apply` remains unexecuted at this checkpoint.
