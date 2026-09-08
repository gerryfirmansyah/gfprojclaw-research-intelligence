# J2 Production Migration Deployment Checkpoint v0

Status: **ACCEPTED / PASS**

## Purpose

Record the auditable production deployment checkpoint for the J2 canonical vertical-slice schema and runtime privileges.

## Governing constraints

- Scientific evidence integrity and HUMAN authority remain unchanged.
- No global research lock or score-to-verdict mechanism is introduced.
- Synthetic A/B fixture data is never loaded into production.
- Canonical schema is deployed alongside the legacy schema; this is not a big-bang legacy migration.
- Runtime privileges follow semantic mutability and do not grant DELETE on canonical tables.

## Production target

Database: `gfprojclaw`

PostgreSQL: 16.15

Canonical migrations:

1. `db/migrations/001_canonical_vertical_slice.sql`
2. `db/migrations/002_runtime_privileges.sql`

## Pre-deployment evidence

Before Migration 001, production contained **0 of the 21 canonical tables**. Previous VPS read-only preflight had also established no canonical-name collision with the legacy production tables.

Migration 001 had already passed the disposable PostgreSQL 16 test cycle and isolated VPS preflight-database test before production deployment.

## Migration 001 production result

`001_canonical_vertical_slice.sql` executed as PostgreSQL superuser `postgres` and completed with `COMMIT`.

The production-safe verifier:

`db/verify/001_schema_verify.sql`

completed successfully with:

`J2 Migration 001 production-safe schema verification passed`

No synthetic fixture was loaded into production.

## Migration 002 production result

`002_runtime_privileges.sql` executed successfully and completed with `COMMIT`.

Effective privileges for `gfproj_app` across the 21 canonical tables were verified as:

- SELECT: **21**
- INSERT: **21**
- UPDATE: **11**
- DELETE: **0**

This matches the accepted runtime privilege contract:

- Mutable/runtime-update tables: SELECT, INSERT, UPDATE.
- Append-oriented/historical tables: SELECT, INSERT.
- No DELETE privilege on canonical tables in v0.

## Ownership verification

All **21 canonical tables** are owned by `postgres`.

Observed result:

`postgres|21`

This is consistent with the accepted deployment decision and existing legacy table-ownership pattern.

## Production deployment conclusion

**PASS.**

Migration 001 and Migration 002 are deployed and verified in production. The canonical J2 vertical slice now exists in PostgreSQL with the intended ownership and bounded runtime privileges, while synthetic fixture evidence remains excluded from production.

This checkpoint establishes the persistence foundation for subsequent real Profile/Project integration and the smallest J5–J7 vertical slice. It does not itself claim completion of the wider J2 model or authorize autonomous scientific judgment.

## Next direction

Proceed from canonical persistence toward real configurable Research Profile / Research Project data and the first traceable real-work path:

`ResearchProfile → ResearchProject → Work → EvidenceFragment → Claim → EvidenceRelationship → GapCandidate → Assessment → ChangeEvent → HumanDecision`

Any domain difference discovered between reference Profile A and Profile B remains non-blocking and must be classified as PROFILE_CONFIG, CORE_GENERALIZATION, ADD_IN_CANDIDATE, or UNRESOLVED_GENERALITY rather than converted into a global project gate.
