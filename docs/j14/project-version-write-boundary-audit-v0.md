# J14 ProjectVersion Write-Boundary Audit v0

## Observed
Migration 002 intends `gfproj_app` to have SELECT+INSERT on `research_project_version` and SELECT+INSERT+UPDATE on `research_project`. The runtime environment identifies the Cockpit DB user as `gfproj_app` (credential value not recorded here).

A HUMAN-approved ProjectVersion v2 application attempt failed on the initial SELECT with PostgreSQL `permission denied for table research_project_version`; the transaction therefore made no canonical change.

A subsequent direct runtime privilege-probe command was blocked by the remote execution safety boundary, so this audit does not claim the live grant matrix has been verified.

## Interpretation
Repository intent and observed production authority are inconsistent or the production privilege state cannot currently be demonstrated through the permitted path. Do not bypass this with `postgres`, credential substitution, ownership changes, or ad-hoc GRANTs.

## Required closure
1. Verify production migration/grant state through an authorized database-administration path.
2. Reconcile production privileges to the reviewed migration/role model, with least privilege.
3. Re-run the HUMAN-approved versioning operation only after the expected role authority is independently verified.
4. Verify v1 -> v2 lineage and exact approved discovery configuration for both projects.

This is an operational authorization issue, not a scientific decision. The HUMAN query acceptance remains valid; it has simply not yet been applied to canonical ProjectVersion state.
