# J3 Reference Profile Production Bootstrap Checkpoint v0

Status: **ACCEPTED / PASS**

## 1. Purpose

Record the controlled production bootstrap of the two J3 reference Research Profiles using the accepted `research-profile-v0` contract.

This checkpoint covers reference configuration only. It does not create ResearchProjects or any scientific evidence objects.

## 2. Production Bootstrap Artifact

Bootstrap SQL:

`db/fixtures/002_reference_profiles.sql`

Design properties:

- deterministic UUIDs;
- bounded single transaction;
- non-idempotent by design;
- duplicate execution fails locally;
- creates only `research_profile` and `research_profile_version` rows;
- sets `current_version_id` only after the referenced v1 exists;
- no ResearchProject, Claim, EvidenceFragment, GapCandidate, Assessment, ChangeEvent, or HumanDecision is created;
- no source credentials or secrets are present;
- reference configuration is explicitly not scientific evidence.

## 3. Reference Profiles

### Profile A

Name: `Computer / Information Systems Research Intelligence`

Domain: `Computer / Information Systems`

Initial version: `1`

### Profile B

Name: `Management / Organization Studies Research Intelligence`

Domain: `Management / Organization Studies`

Initial version: `1`

Both profiles use the same generic configuration contract and persistence mechanics. Domain differences remain configuration values rather than core source-code branches.

## 4. Pre-Production Test Results

Bootstrap was executed first against the existing PostgreSQL preflight database.

Observed result:

```text
BEGIN
INSERT 0 2
INSERT 0 2
UPDATE 2
COMMIT
```

Verification confirmed:

- exactly two reference profiles were present;
- each profile had version `1`;
- each `context.domain` matched its intended reference domain;
- each profile's `current_version_id` matched the corresponding v1 row.

A deliberate second execution was then performed to verify the non-idempotent integrity contract. The duplicate primary key caused the transaction to abort and finish with `ROLLBACK`. Post-rollback verification confirmed the preflight database still contained exactly two profiles with both current-version pointers intact.

Result: **PRE-PRODUCTION EXECUTABLE TEST PASS**.

## 5. Production Preflight

Immediately before deployment, production contained:

```text
profiles    = 0
current_set = 0
```

This confirmed a clean baseline for deterministic bootstrap IDs and no existing production Research Profile data requiring transformation.

## 6. Production Deployment Result

Production bootstrap execution completed successfully:

```text
BEGIN
INSERT 0 2
INSERT 0 2
UPDATE 2
COMMIT
```

Production verification returned:

```text
Computer / Information Systems Research Intelligence
version_no = 1
domain = Computer / Information Systems
current_ok = true

Management / Organization Studies Research Intelligence
version_no = 1
domain = Management / Organization Studies
current_ok = true
```

Result: **PRODUCTION BOOTSTRAP PASS**.

## 7. Scientific and Architectural Integrity

This deployment preserves the project constitution:

- profile configuration is context, not scientific evidence;
- no score or configuration value creates an automated scientific verdict;
- HUMAN scientific authority remains unchanged;
- no global workflow lock was introduced;
- both domains use the same canonical schema and bootstrap mechanics;
- no domain-specific core branch was required;
- no synthetic scientific evidence was inserted into production.

Current generality classification remains `PROFILE_CONFIG` for the observed A/B differences.

## 8. J3 State After This Checkpoint

J3 now has:

- accepted Research Profile contract;
- accepted A/B reference configurations;
- deterministic executable bootstrap;
- successful pre-production execution and rollback-integrity test;
- successful production deployment;
- successful current-version verification for both reference profiles.

This establishes the first real production Research Profile context for the Research Cockpit while keeping ResearchProject creation and scientific evidence ingestion as subsequent work.

## 9. Next Intended Work

The next J3 step should connect these real production profiles to the smallest project bootstrap / selection path needed by the Version 0 cockpit, while preserving the hierarchy:

`ResearchProfile → ResearchProject → Research Cockpit`

ResearchProject data must remain HUMAN research-effort context and must not be conflated with reusable Profile configuration.
