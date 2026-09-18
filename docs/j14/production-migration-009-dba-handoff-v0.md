# J14 Production Migration 009 DBA Handoff v0

## Purpose
Apply the already-reviewed metadata-ingestion capability boundary to production PostgreSQL without granting migration authority to `gfproj_app` or bypassing the reviewed role model.

## Current facts
- Disposable PostgreSQL run `35329529637` passed Migration 009, Verifier 019, and bounded ingestion fixture tests on commit `738cd3e`.
- Production `gfproj_pilot_executor` exists and is LOGIN.
- Production `gfproj_pilot_metadata_ingestor` is absent.
- Applying Migration 009 as `gfproj_app` failed with `permission denied to create role`; the transaction rolled back.
- Migration 010 source registry is already deployed; OpenAlex and Crossref are canonical ACTIVE bibliographic providers.

## Authorized DBA action
From repository commit `738cd3e` or later, connect to the GFPROJCLAW production database using the existing authorized database-administration migration identity and execute exactly:

`psql -v ON_ERROR_STOP=1 -d <GFPROJCLAW_DB> -f db/migrations/009_pilot_metadata_ingestor_role.sql`

Then execute exactly:

`psql -v ON_ERROR_STOP=1 -d <GFPROJCLAW_DB> -f db/verify/019_pilot_metadata_ingestor_role_verify.sql`

Do not grant CREATEROLE to `gfproj_app`, do not alter table ownership, do not broaden UPDATE/DELETE authority, and do not create scientific-write privileges.

## Expected result
- `gfproj_pilot_metadata_ingestor`: NOLOGIN, NOSUPERUSER, NOCREATEDB, NOCREATEROLE, NOINHERIT, NOREPLICATION, NOBYPASSRLS.
- `gfproj_pilot_executor` is a member of the metadata capability role.
- Metadata role can read canonical project/provider configuration and insert bounded bibliographic metadata.
- SourceRecord UPDATE remains column-scoped; project relevance UPDATE remains `last_seen_at` only.
- No INSERT authority on HumanDecision, Claim, EvidenceFragment, GapCandidate, or InvestigationDirection.

## Stop conditions
Stop immediately on any verifier failure, unexpected ownership/privilege requirement, or need for an ad-hoc GRANT outside Migration 009. Do not run real-source ingestion until GFPROJCLAW verifies the resulting production boundary.
