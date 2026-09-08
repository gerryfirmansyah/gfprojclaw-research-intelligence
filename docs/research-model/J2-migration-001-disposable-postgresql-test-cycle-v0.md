# J2 Migration 001 Disposable PostgreSQL Test Cycle v0

Status: **J2 ACTIVE — Disposable PostgreSQL Test Cycle COMPLETE**

## 1. Purpose

This stage executes Migration 001 for the first time against a disposable PostgreSQL 16 environment, without touching the GFPROJCLAW VPS or production database.

The governing principle is:

> **Prove executable integrity in an isolated database before any VPS interaction; failures remain engineering-local and never become scientific gates.**

The cycle uses GitHub Actions with a disposable `postgres:16` service container.

---

## 2. Inputs Tested

```text
db/migrations/001_canonical_vertical_slice.sql
db/fixtures/001_vertical_slice_reference.sql
db/verify/001_schema_verify.sql
db/verify/001_fixture_verify.sql
db/verify/001_negative_integrity_tests.sql
.github/workflows/j2-migration-001-disposable-postgres.yml
```

Synthetic Profile A/B fixtures are test-only and are not production evidence.

---

## 3. Disposable Environment

The successful test run used:

```text
GitHub-hosted Ubuntu runner
PostgreSQL 16 service container
PostgreSQL server observed in logs: 16.15
Disposable databases only
No VPS access
No production connection
```

Workflow:

`J2 Migration 001 Disposable PostgreSQL Test`

Successful run:

https://github.com/gerryfirmansyah/gfprojclaw-research-intelligence/actions/runs/34206307054

Head commit:

`bfefd0d0793d8b456d8d6cbbe9ea8c56b992266c`

---

## 4. First Positive Cycle

An earlier workflow run proved the main positive path before the negative suite was added.

The following passed:

```text
T1 Migration apply
T2 production-safe schema verification
T3 synthetic cross-domain fixture apply
T4 fixture verification
21-table canonical count
T6 clean rebuild
T7 re-apply conflict behavior
```

This established that Migration 001 is executable on PostgreSQL 16 and that Profile A/B use the same canonical mechanics.

---

## 5. Negative-Test Learning Event

The first expanded T5 run intentionally tested invalid states.

It discovered that:

```text
CoverageContext.profile_version_id
```

can be updated to a Profile version outside the Project's Profile lineage without a direct DDL rejection.

This was not hidden or treated as a project failure.

The test correctly surfaced the distinction between:

```text
DDL-enforced invariant
vs
production-verifier-enforced invariant
```

The accepted J2 executable plan permits selected N13–N19 cases to be caught by the production-safe verifier rather than by a plain FK when a clean relational constraint would require unnecessary schema duplication or complexity.

Therefore N15 was reclassified as a verifier-level negative case. The test cycle now mutates a cloned disposable database into the invalid lineage state and confirms that `001_schema_verify.sql` rejects it.

This preserves the project principle:

> **Strict evidence integrity without unnecessary machinery.**

---

## 6. Successful Final Cycle

Final run result: **PASS**.

All workflow steps completed successfully:

```text
Initialize PostgreSQL 16 container                  PASS
Checkout                                             PASS
Install PostgreSQL client                           PASS
Create disposable test database                     PASS
T1 apply Migration 001                              PASS
T2 production-safe schema verification              PASS
T3 apply synthetic Profile A/B fixture              PASS
T4 fixture verification                             PASS
Canonical table count = 21                          PASS
T5 hard negative integrity tests                    PASS
T5 wrong CoverageContext Profile lineage detection PASS
T5 quarantined upstream evidence detection          PASS
T6 clean rebuild database                           PASS
T7 migration re-apply rejection                     PASS
```

No production/VPS database was modified.

---

## 7. What the Positive Tests Proved

### 7.1 Migration atomicity and PostgreSQL compatibility

`001_canonical_vertical_slice.sql` executes successfully as one migration on PostgreSQL 16.

### 7.2 Canonical first slice

Exactly the accepted 21 canonical tables are present.

### 7.3 Production-safe verification

The generic verifier passes without requiring synthetic fixture identities.

### 7.4 Cross-domain symmetry

Profile A — Computer / Information Systems and Profile B — Management / Organization Studies pass the same schema, evidence trace, Assessment, ChangeEvent, CoverageContext, and HumanDecision mechanics.

### 7.5 Evidence trace

Both fixture domains support navigation through:

```text
GapCandidate
← EvidenceRelationship
← Claim
← EvidenceFragment
← Work
← SourceRecord
← LiteratureSource
```

### 7.6 Contradictory evidence retention

Both fixture GapCandidates retain supporting and challenging evidence simultaneously.

### 7.7 HUMAN authority

Machine Assessment and HumanDecision remain structurally separate.

### 7.8 Coverage degradation is non-gating

Fixture source health includes both `HEALTHY` and `DEGRADED` states while evidence from healthy sources remains usable.

### 7.9 Rebuild reproducibility

A second clean disposable database can be built from the same migration + fixture + verifier sequence.

### 7.10 Re-apply safety

Applying Migration 001 a second time to an already migrated database produces the expected engineering conflict rather than silently skipping schema objects.

---

## 8. Negative Integrity Results

Direct DDL rejection was confirmed for representative invalid writes including:

```text
invalid Profile status
cross-Profile current Profile version
cross-Project current Project version
duplicate Work identifier
METADATA_ONLY EvidenceFragment
GapCandidate identity/Project mismatch
Assessment target/Project mismatch
ChangeEvent target/Project mismatch
HumanDecision target/Project mismatch
invalid HumanDecision type
quarantined EvidenceFragment without reason
EvidenceFragment SourceRecord normalized to another Work
HumanDecision referencing foreign Assessment lineage
Assessment referencing foreign CoverageContext Project
cross-lineage Profile version supersession
cross-lineage Project version supersession
cross-target Assessment supersession
cross-target HumanDecision supersession
```

Verifier-level rejection was also confirmed for:

```text
CoverageContext Profile-version lineage mismatch
active Claim depending on quarantined EvidenceFragment
```

These failures are local integrity failures only. They do not imply a global research lock.

---

## 9. Generality Review

### Profile A

PASS.

### Profile B

PASS.

### Domain-specific schema assumption found

None.

### Generality exception

None required in this stage.

The same migration, fixtures structure, evidence semantics, temporal machinery, and HumanDecision separation work for both reference domains.

---

## 10. VPS Status

```text
VPS accessed: NO
Production PostgreSQL changed: NO
Legacy schema changed: NO
Legacy service restarted: NO
Synthetic fixture loaded to production: NO
```

The failed legacy `gfprojclaw-g6-g9.service` remains untouched.

---

## 11. Stage Verdict

**J2 Migration 001 Disposable PostgreSQL Test Cycle v0 — ACCEPTED / PASS.**

Migration 001 has now moved from:

```text
SQL Draft
→ pre-test corrections
→ executable disposable PostgreSQL validation
```

The evidence is sufficient to proceed to a read-only VPS preflight, but not yet to production apply.

---

## 12. Next Step

Recommended next artifact:

**J2 Migration 001 VPS Read-Only Preflight v0**

Purpose:

- inspect PostgreSQL version and current database context;
- inspect schema/search_path conventions;
- confirm `pgcrypto` / `gen_random_uuid()` availability;
- detect collisions with the 21 canonical table names;
- inspect migration-history conventions;
- determine whether an isolated disposable VPS database can be created safely;
- make no schema changes during preflight.

Operational interaction rule remains:

> **one short command per step → inspect output → continue.**
