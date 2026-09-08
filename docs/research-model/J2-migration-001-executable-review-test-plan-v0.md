# J2 Migration 001 Executable Review & Test Plan v0

Status: **J2 ACTIVE — Executable Review & Test Plan**

## 1. Purpose

This review evaluates whether the current Migration 001 SQL draft is safe to move from repository design into an executable PostgreSQL test cycle, and defines the test sequence that must be completed before any canonical schema is applied to the GFPROJCLAW production database.

Inputs reviewed:

- `db/migrations/001_canonical_vertical_slice.sql`
- `db/fixtures/001_vertical_slice_reference.sql`
- `db/verify/001_vertical_slice_verify.sql`
- J2 Canonical DDL Contract Review v0
- J2 Migration 001 Design & Fixture Contract v0

Governing principle:

> **The first executable migration must fail locally when engineering integrity is violated, but it must never create a global scientific lock, collapse HUMAN authority into machine state, or contaminate production with synthetic fixture evidence.**

---

## 2. Review Verdict

**Verdict: CONDITIONALLY ACCEPTED FOR TEST PREPARATION — NOT YET APPROVED FOR PRODUCTION/VPS APPLY.**

The SQL draft is structurally coherent and is suitable as the basis for an executable test cycle. It correctly establishes the 21-table first slice, uses PostgreSQL transactions, keeps provenance strongly typed, separates Assessment from HumanDecision, represents CoverageContext explicitly, and uses the same schema mechanics for Profile A and Profile B.

However, several executable-integrity issues must be corrected or explicitly covered by stronger verification before the migration is allowed to touch the production database.

This is not a failure of J2. It is the intended purpose of the executable review stage.

---

## 3. What Already Passes Review

### 3.1 Canonical scope

The migration creates the accepted **21 canonical first-slice tables** and does not introduce Theory, Method, Concept, ExistingSolution, Synthesis, R0–R16, queue/job, or domain-specific tables prematurely.

### 3.2 Transaction semantics

The migration is wrapped in one engineering transaction:

```text
BEGIN → DDL → COMMIT
```

This is appropriate atomicity for one migration unit and is not a research workflow gate.

### 3.3 Provenance chain

The relational shape supports:

```text
LiteratureSource
  → SourceRecord
  → Work
  → EvidenceFragment
  → Claim
  → EvidenceRelationship
  → GapCandidate
```

and the current verification script demonstrates traversal of that path.

### 3.4 HUMAN authority

`assessment` and `human_decision` are separate tables. No trigger or threshold automatically converts an Assessment into a scientific decision.

### 3.5 Coverage semantics

`coverage_context` and `coverage_source_state` are historical context, not global pipeline gates. A source may be `DEGRADED` while unrelated scientific work remains valid.

### 3.6 Local quarantine

EvidenceFragment and Claim carry local quarantine state. The verification script checks that active downstream rows do not silently depend on quarantined upstream evidence.

### 3.7 Cross-domain generality

The deterministic fixture uses Profile A and Profile B through the same tables, same evidence relationship mechanism, same assessment machinery, same ChangeEvent machinery, and same HumanDecision machinery.

No domain-specific schema branch is present.

---

# 4. Pre-VPS Blocking Findings

The following findings must be resolved before production/VPS apply approval.

## B1 — Production verification must be separated from fixture verification

Current file:

```text
db/verify/001_vertical_slice_verify.sql
```

contains both generic schema/integrity verification and fixture-specific assertions using deterministic Profile A/B UUIDs.

That means the file is appropriate for a disposable fixture database, but **must not be used as the production post-migration verifier**, because production should not contain the synthetic fixture rows.

### Required correction

Split verification responsibilities conceptually into:

```text
001_schema_verify.sql
    production-safe structural and generic invariant checks

001_fixture_verify.sql
    deterministic Profile A/B fixture assertions and evidence trace
```

The existing verify file may be retained as the fixture verifier if renamed or clearly marked test-only.

### Constitutional reason

Synthetic fixture data must never become canonical scientific evidence simply to satisfy a deployment test.

---

## B2 — Production must never load the reference fixture

`001_vertical_slice_reference.sql` is explicitly synthetic and correctly labels itself as such.

### Required deployment rule

The production sequence is:

```text
Migration SQL
→ production-safe schema verification
```

not:

```text
Migration SQL
→ synthetic fixture
→ verification
```

The fixture is used only in a disposable test database/environment.

---

## B3 — Cross-project context alignment needs stronger protection

The DDL already protects the Project alignment of:

- GapCandidate identity;
- Assessment target object;
- ChangeEvent primary object;
- HumanDecision primary object.

But optional contextual references can still point across Projects unless application logic prevents it.

Examples requiring protection or verification:

```text
assessment.coverage_context_id
change_event.coverage_context_id
human_decision.coverage_context_id
human_decision.assessment_id
```

A HumanDecision for Project A must not accidentally cite an Assessment or CoverageContext belonging to Project B.

### Required correction

Before VPS apply, choose one of:

1. composite relational FKs where practical; or
2. explicit generic verification/integrity tests that reject the local write.

For `human_decision.assessment_id`, verification should also ensure the referenced Assessment concerns the same Project and, when scientifically intended as the decision basis, the same primary research object.

No global lock is required; invalid writes are rejected locally.

---

## B4 — ResearchObject Profile/Project lineage must be verified

`research_object_identity` stores both optional `profile_id` and `project_id`.

For a project-scoped GapCandidate, if `profile_id` is populated, it must agree with the Profile owning the Project.

### Required invariant

```text
research_object_identity.project_id → research_project.profile_id
must agree with
research_object_identity.profile_id
```

for project-scoped objects carrying a Profile reference.

This can be enforced by a composite FK after adding a suitable unique key to `research_project`, or by a production-safe integrity check in v0.

---

## B5 — EvidenceFragment source provenance must agree with Work normalization

An EvidenceFragment carries both:

```text
work_id
source_record_id
```

but the current DDL does not guarantee that the referenced SourceRecord is the SourceRecord normalized to that same Work through `work_source_record`.

Without this check, an accidental row could claim:

```text
EvidenceFragment.work_id = Work A
EvidenceFragment.source_record_id = SourceRecord normalized to Work B
```

while all simple FKs still pass.

### Required invariant

When `source_record_id` is non-null:

```text
EvidenceFragment(work_id, source_record_id)
```

must correspond to a valid `work_source_record` mapping.

Preferred direction for the first slice: enforce or verify this explicitly before VPS apply.

This is a provenance integrity issue, not a scientific gate.

---

## B6 — Supersession lineage requires same-context verification

The schema correctly prevents self-supersession, but simple self-FKs do not guarantee that a new row supersedes a row from the same scientific/context lineage.

At minimum, test these cases:

```text
research_profile_version.supersedes_version_id → same profile
research_project_version.supersedes_version_id → same project
assessment.supersedes_assessment_id → same project + same target object
human_decision.supersedes_decision_id → same project + same primary object
```

For Claim and EvidenceRelationship, v0 should at least document and test the intended same-lineage rule before those supersession links are used by the application.

---

## B7 — Current-version verification must detect missing pointers where expected

The current verifier checks wrong ownership only when a `current_version_id` joins to a version row. A NULL current version can therefore escape that particular test.

For production, NULL may be legal during creation. For active reference fixtures, however, both Profile and Project must have a current version.

### Required test distinction

- generic production verifier: validate ownership whenever pointer is present;
- fixture verifier: additionally require current version pointers for both A and B fixtures.

---

# 5. Non-Blocking Review Notes

These do not block preparation of the disposable test cycle but should be watched during J2 implementation.

### N1 — `pgcrypto` creation is an operational prerequisite

`CREATE EXTENSION IF NOT EXISTS pgcrypto` is reasonable in the draft, but VPS preflight must determine whether the extension/function already exists and whether the deployment role may create extensions.

If extension creation is restricted, UUID generation may move to the application while retaining `uuid` columns.

### N2 — Versioned migration is intentionally not broadly idempotent

A second execution of Migration 001 against the same schema should not silently succeed by skipping existing tables. This is correct. Migration bookkeeping must determine whether 001 has already been applied.

### N3 — No fixture idempotency requirement

The deterministic fixture may fail on second load because its UUIDs are fixed. This is acceptable for a disposable test database that is recreated for each clean test cycle.

### N4 — JSONB indexes remain deferred

No blanket JSONB GIN indexes are needed until real cockpit/discovery query patterns justify them.

### N5 — Assessment numeric ranges remain advisory semantics

No database threshold may convert numeric advice into ACCEPT/PASS/TRUE. Any later numeric range standardization must remain distinct from scientific judgment.

---

# 6. Executable Test Architecture

The migration must be tested in increasing levels of realism.

```text
GitHub static review
        ↓
Disposable PostgreSQL 16 test database
        ↓
Migration apply
        ↓
Catalog / constraint verification
        ↓
Synthetic Profile A/B fixture
        ↓
Fixture verification
        ↓
Negative integrity tests
        ↓
Clean rebuild / repeatability test
        ↓
VPS read-only preflight
        ↓
VPS isolated test database if needed
        ↓
Production migration
        ↓
Production-safe verification
```

Do not jump from GitHub SQL draft directly to production apply.

---

# 7. Test Phase T0 — Static SQL Review

Objective: verify source-level consistency without touching PostgreSQL.

Checks:

```text
21 expected CREATE TABLE statements
no domain-specific table names
no DROP of legacy objects
no ALTER of legacy objects
no global research lock/status table
no automatic scientific acceptance trigger
all evidence/history FKs use restrictive deletion semantics
fixture explicitly labeled synthetic
time-zone-aware timestamps used where required
```

Expected result:

```text
PASS before database execution begins
```

---

# 8. Test Phase T1 — Clean PostgreSQL 16 Migration Apply

Environment:

```text
disposable database
PostgreSQL 16.x
no legacy GFPROJCLAW data
no production application connection
```

Test:

```text
apply 001_canonical_vertical_slice.sql once
```

Expected:

- one transaction commits;
- exactly 21 canonical tables exist;
- all declared indexes and constraints are created;
- no unexpected extension/schema objects are introduced;
- no partial tables remain after a deliberately failed copy of the migration in a disposable failure test.

The primary migration file itself should not be intentionally corrupted; rollback behavior can be tested with a temporary modified copy in the disposable environment.

---

# 9. Test Phase T2 — Catalog Contract Verification

Check PostgreSQL catalogs for:

```text
PK presence
FK direction
ON DELETE behavior
UNIQUE constraints
CHECK constraints
column nullability
uuid types
timestamptz types
jsonb types
required indexes
```

Key structural assertions:

```text
Claim.evidence_fragment_id NOT NULL
EvidenceFragment.work_id NOT NULL
EvidenceRelationship.claim_id NOT NULL
EvidenceRelationship.target_research_object_id NOT NULL
Assessment separate from HumanDecision
GapCandidate shared identity key intact
CoverageContext historical rows independently identifiable
```

---

# 10. Test Phase T3 — Deterministic Fixture Apply

Apply only in the disposable test database:

```text
001_vertical_slice_reference.sql
```

Expected fixture shape:

```text
2 Profiles
2 Projects
same canonical table mechanics
support evidence + challenge evidence for each Profile
GapCandidate for each Project
Assessment for each GapCandidate
ChangeEvent for each GapCandidate
HumanDecision separate from Assessment
CoverageContext with healthy and degraded source states
```

All fixture scientific text remains synthetic and must never be interpreted as real literature evidence.

---

# 11. Test Phase T4 — Fixture Verification

Run the fixture verifier.

Required positive assertions:

### Evidence trace

For both Profile A and B:

```text
GapCandidate
← EvidenceRelationship
← Claim
← EvidenceFragment
← Work
← SourceRecord
← LiteratureSource
```

must be navigable.

### Contradiction retention

Each reference Gap must have at least:

```text
1 SUPPORTS relationship
1 CHALLENGES or CONTRADICTS relationship
```

The challenging evidence must not be deleted merely because support evidence exists.

### HUMAN authority

Each fixture decision must remain a `human_decision` row separate from Assessment dimensions.

### Coverage

At least one source degradation is retained as coverage context without invalidating healthy-source evidence.

### Cross-domain symmetry

A and B must pass equivalent integrity checks using the same schema and verifier logic.

---

# 12. Test Phase T5 — Negative Integrity Tests

Each negative test runs in its own short transaction and is rolled back after confirming the expected local rejection.

Required negative cases:

```text
N01 invalid Profile status
N02 current Profile version from another Profile
N03 current Project version from another Project
N04 duplicate Work identifier type/value
N05 EvidenceFragment with METADATA_ONLY access
N06 Claim with nonexistent EvidenceFragment
N07 GapCandidate with Project inconsistent with ResearchObjectIdentity
N08 Assessment target from another Project
N09 ChangeEvent object from another Project
N10 HumanDecision object from another Project
N11 HumanDecision with invalid decision_type
N12 quarantined EvidenceFragment without reason
N13 active Claim depending on quarantined EvidenceFragment
N14 non-quarantined EvidenceRelationship depending on quarantined Claim
N15 CoverageContext Profile version from wrong Profile
N16 EvidenceFragment SourceRecord normalized to a different Work
N17 HumanDecision citing Assessment from another Project/object
N18 Assessment/ChangeEvent/HumanDecision citing CoverageContext from another Project
N19 supersession link crossing Profile/Project/object lineage
```

Tests N13–N19 may be caught by verification rather than a plain DDL constraint in v0, but **the bad state must be detected before production approval**.

Failure semantics:

> Reject/quarantine the local invalid unit. Do not lock unrelated research processing.

---

# 13. Test Phase T6 — Clean Rebuild Test

Purpose: prove reproducibility.

Procedure in disposable environment:

```text
create clean database
apply Migration 001
apply fixture
run fixture verification
```

Repeat from another clean database.

Expected:

- same schema contract;
- deterministic fixture identities;
- same logical verification result;
- no dependence on hidden state from an earlier run.

The test is a rebuild, not a second execution of Migration 001 against an already-migrated schema.

---

# 14. Test Phase T7 — Migration Re-apply Safety

Attempting Migration 001 again against an already migrated schema should produce an engineering conflict rather than silently pretending success.

This confirms the design decision:

> versioned migration state is explicit; broad `IF NOT EXISTS` must not hide schema drift.

A migration-history mechanism must record that Migration 001 has already been applied before production operation begins.

The exact migration runner/ledger implementation remains a deployment decision, but it must be settled before recurring migrations are introduced.

---

# 15. VPS Preflight — Read-Only First

Only after T0–T7 pass do we inspect the VPS.

The first VPS phase is **read-only**. It must establish:

```text
PostgreSQL major/minor version
current database and application role
existing schema/search_path convention
whether pgcrypto/gen_random_uuid() is available
whether any of the 21 canonical table names already exist
whether a migration-history convention already exists
whether legacy tables use names that could collide
available permissions for an isolated test database/schema
```

No Migration 001 SQL is applied during preflight.

### Interaction rule

VPS work follows the established operator pattern:

> **one short command per step → inspect output → continue.**

No long heredoc or multi-command terminal paste is required.

---

# 16. VPS Isolated Test Environment

Preferred option after successful preflight:

```text
dedicated disposable PostgreSQL test database
```

rather than applying the migration directly into the production database.

Why a separate database is preferred:

- unqualified table names cannot collide with legacy canonical names;
- fixture data is physically isolated from production research state;
- extension/search_path behavior is easier to inspect;
- clean rebuild is simple;
- fixture cleanup cannot accidentally delete production state.

If database creation is operationally unavailable, a dedicated isolated schema may be considered, but only after explicit search-path review.

---

# 17. Production Apply Entry Criteria

Migration 001 may be considered **VPS production-ready** only when all of the following are true:

```text
T0 static review PASS
T1 clean PG16 migration PASS
T2 catalog verification PASS
T3 fixture apply PASS
T4 Profile A/B fixture verification PASS
T5 negative integrity tests PASS
T6 clean rebuild PASS
T7 re-apply behavior understood
B1–B7 resolved
VPS read-only preflight PASS
isolated VPS test PASS if used
production-safe verifier exists
fixture is excluded from production deployment
migration bookkeeping approach is known
```

Production readiness is an engineering deployment determination, not a scientific approval gate.

---

# 18. Production Apply Sequence

When eventually approved, the intended deployment sequence is:

```text
1. confirm production target and backup/recovery posture
2. apply Migration 001 only
3. run production-safe structural/integrity verifier
4. confirm existing legacy research assets/services were not modified
5. leave synthetic fixture unloaded
6. begin incremental import/integration only through later reviewed steps
```

No big-bang legacy migration occurs in Migration 001.

---

# 19. Rollback and Recovery Policy

### Before COMMIT

If DDL fails inside the Migration 001 transaction:

```text
ROLLBACK the migration transaction
```

No partial canonical schema should remain.

### After COMMIT

Migration 001 is forward-only. Do not casually drop canonical tables to simulate rollback after production commit.

If a post-commit defect is discovered:

```text
stop new writes to the affected new canonical component if necessary
preserve existing data
create a corrective forward migration
keep unrelated legacy and research processing available where safe
```

This is local engineering recovery, not scientific authorization.

---

# 20. Legacy Safety Contract

Migration 001 must not:

```text
DROP legacy tables
ALTER legacy evidence tables
restart the failed legacy g6-g9 service
re-enable old global G1–G13 gate behavior
convert legacy PASS/FAIL states into canonical research truth
load synthetic fixtures into production
```

Legacy assets remain read-only/auditable until explicitly transformed in later J stages.

---

# 21. Cross-Domain Acceptance Test

The executable test is only general enough if:

```text
Profile A and Profile B use identical migration objects
Profile A and Profile B use identical EvidenceRelationship semantics
Profile A and Profile B use identical Assessment/HumanDecision separation
Profile A and Profile B use identical CoverageContext mechanics
neither fixture requires domain-specific table/column/trigger code
```

Any future difference follows ADR-001:

```text
PROFILE_CONFIG
→ CORE_GENERALIZATION
→ ADD_IN_CANDIDATE
→ UNRESOLVED_GENERALITY
```

A generality exception is architectural learning, not a project stop.

---

# 22. Review Result

**J2 Migration 001 Executable Review & Test Plan v0 is ACCEPTED as the testing contract.**

The current SQL Draft v0 is **not yet approved for production VPS apply**. It is approved as the basis for a corrected/tested executable candidate.

The immediate next implementation step is:

> **J2 Migration 001 SQL Draft v1 — Pre-Test Corrections**

That revision should address B1–B7, most importantly:

```text
production-safe vs fixture verification separation
cross-project contextual reference checks
ResearchObject Profile/Project lineage
evidence-fragment Work/SourceRecord provenance agreement
supersession lineage tests
current-version test distinction
```

After Draft v1 is committed, run the disposable PostgreSQL 16 test cycle before entering VPS preflight.

---

## 23. Checkpoint

```text
Version 0
J0 PINNED
J1 ACCEPTED
J2 ACTIVE

Research Object Model — ACCEPTED
Relationship & Cardinality — ACCEPTED
Generic Identity & Association — ACCEPTED
PostgreSQL Persistence Shape — ACCEPTED BASELINE
Minimum Canonical Schema / Vertical Slice — ACCEPTED
Canonical DDL Contract — ACCEPTED BASELINE
Migration 001 Design & Fixture Contract — ACCEPTED BASELINE
Migration 001 SQL Draft v0 — CREATED
Migration 001 Executable Review & Test Plan v0 — ACCEPTED
Production VPS Apply — NOT YET APPROVED
```
