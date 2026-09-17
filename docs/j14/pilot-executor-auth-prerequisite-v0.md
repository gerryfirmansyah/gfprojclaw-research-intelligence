# J14 Pilot Executor Authentication Prerequisite v0

## Required OS boundary
Production scheduling requires a dedicated operating-system service identity named `gfproj-pilot` (or a reviewed equivalent). It must not reuse the Cockpit runtime identity.

## PostgreSQL mapping
The dedicated OS identity should authenticate over the local Unix socket through PostgreSQL peer/map authentication to `gfproj_pilot_executor`. The executor then explicitly activates `gfproj_pilot_worker` capability authority for operational pilot writes.

## Required invariants
- session identity: `gfproj_pilot_executor`
- effective worker role: `gfproj_pilot_worker`
- no HumanDecision INSERT/UPDATE authority
- no superuser, database creation, role creation, replication, or bypass-RLS authority
- no Cockpit credential reuse
- scheduler remains disabled until the identity chain is verified end-to-end

## Current infrastructure boundary
The remote administration safety layer does not permit creation of the required OS service account. Therefore pg_ident/pg_hba activation must not occur until that account is provisioned through an authorized infrastructure path.
