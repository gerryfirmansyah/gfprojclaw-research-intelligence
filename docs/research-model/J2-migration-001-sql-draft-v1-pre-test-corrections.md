# J2 Migration 001 SQL Draft v1 — Pre-Test Corrections

Status: **J2 ACTIVE — SQL Draft v1 / Pre-Test Corrections**

## 1. Purpose

This checkpoint applies the blocking corrections identified in **J2 Migration 001 Executable Review & Test Plan v0** before any PostgreSQL execution cycle begins.

The governing principle remains:

> **Strengthen local relational integrity before execution, while preserving local-failure semantics, scientific traceability, domain generality, and HUMAN authority.**

This revision does not apply anything to the VPS or production PostgreSQL database.

---

## 2. Files in the v1 pre-test set

Canonical migration:

```text
db/migrations/001_canonical_vertical_slice.sql
```

Synthetic reference fixture, unchanged in scientific intent:

```text
db/fixtures/001_vertical_slice_reference.sql
```

Verification is now separated into:

```text
db/verify/001_schema_verify.sql
    production-safe structural/generic verification

db/verify/001_fixture_verify.sql
    disposable-test-only Profile A/B assertions
```

The previous combined verifier:

```text
db/verify/001_vertical_slice_verify.sql
```

has been removed to prevent accidental production dependence on synthetic fixture identifiers.

---

## 3. Blocking findings resolved

### B1 — Production and fixture verification separated

Resolved.

`001_schema_verify.sql` contains no deterministic A/B UUID dependency and can run against an empty-but-migrated production schema or later real canonical data.

`001_fixture_verify.sql` is explicitly marked TEST ONLY and requires the synthetic fixture.

### B2 — Production fixture contamination prevented by deployment contract

Resolved at repository/deployment-contract level.

Production sequence remains:

```text
Migration 001
→ 001_schema_verify.sql
```

Disposable test sequence is:

```text
Migration 001
→ synthetic fixture
→ 001_schema_verify.sql
→ 001_fixture_verify.sql
```

Synthetic fixtures are never a prerequisite for production verification.

### B3 — Cross-project contextual references strengthened

Resolved relationally where practical.

The migration now uses composite FKs so that:

```text
Assessment.coverage_context_id
ChangeEvent.coverage_context_id
HumanDecision.coverage_context_id
```

cannot point to CoverageContext rows from another Project.

`HumanDecision.assessment_id` is constrained to an Assessment with the same:

```text
Project
+
primary research object
```

This preserves HumanDecision as HUMAN authority while preventing accidental cross-project/context citation.

### B4 — ResearchObject Profile/Project lineage strengthened

Resolved relationally for the v0 object scope.

`research_project` exposes a unique `(id, profile_id)` key and `research_object_identity` uses a composite Project/Profile FK with `MATCH FULL`.

For the first slice, a project-scoped GapCandidate therefore cannot carry a Profile that disagrees with its Project.

### B5 — EvidenceFragment source provenance strengthened

Resolved relationally.

When `evidence_fragment.source_record_id` is non-null, the pair:

```text
(work_id, source_record_id)
```

must exist in `work_source_record`.

This prevents a fragment from claiming Work A while citing a SourceRecord normalized to Work B.

### B6 — Supersession lineage strengthened

Resolved for the first-slice supersession paths.

Composite self-FKs now keep supersession within lineage for:

```text
ResearchProfileVersion → same Profile
ResearchProjectVersion → same Project
Assessment → same Project + same target object
HumanDecision → same Project + same primary object
Claim → same EvidenceFragment
EvidenceRelationship → same Claim + same target object
```

This is historical integrity, not a scientific gate.

### B7 — Current-version verification distinction implemented

Resolved.

Production-safe verification checks ownership when a current-version pointer exists but does not require all rows to have a pointer.

Fixture verification additionally requires both reference Profiles and both reference Projects to have current-version pointers.

---

## 4. Additional verifier strengthening

The production-safe verifier now checks, without fixture assumptions:

```text
21 canonical tables exist
current version ownership
Profile/Project supersession lineage
ResearchObject Profile/Project alignment
Gap typed identity
EvidenceFragment → Work provenance
Claim → EvidenceFragment provenance
METADATA_ONLY prohibition
EvidenceFragment Work/SourceRecord normalization alignment
Coverage Profile/Project-version lineage
Assessment/ChangeEvent/HumanDecision target-project alignment
Assessment/ChangeEvent/HumanDecision CoverageContext alignment
HumanDecision → Assessment same-project/same-object lineage
Assessment/HumanDecision/Claim/EvidenceRelationship supersession lineage
quarantine dependency integrity
```

These checks reject or expose local invalid states. They do not create a global research lock.

---

## 5. Fixture verifier strengthening

The fixture verifier now requires:

```text
exactly two reference Profiles with current versions
exactly two reference Projects with current versions
support + challenge evidence for each reference Gap
at least two Works in each evidence trace
separate Assessment and HumanDecision rows per Project
same Project/object lineage between HumanDecision and cited Assessment
degraded-source coverage context for both reference Projects
```

It also emits inspectable evidence, HUMAN-decision, and coverage projections for Profile A and Profile B.

---

## 6. What remains deliberately unchanged

The first-slice scope remains **21 tables**.

Still deferred:

```text
Theory
Method
Concept
ExistingSolution
CandidateContribution
Synthesis
R0–R16 persistence
scheduler/run/job schema
add-in runtime
```

No domain-specific tables or branches were introduced.

No machine threshold becomes a HUMAN decision.

No source-health state becomes a global gate.

No legacy VPS object is changed.

---

## 7. Current execution status

```text
GitHub SQL v1 pre-test corrections     COMPLETE
Production database                    UNCHANGED
VPS preflight                          NOT STARTED
Disposable PostgreSQL test cycle       NEXT
Production apply                       NOT APPROVED YET
```

---

## 8. Next step

The next appropriate J2 step is:

> **J2 Migration 001 Disposable PostgreSQL Test Cycle v0**

Before entering the production VPS, execute T0–T6 from the accepted test plan in a disposable PostgreSQL 16 environment if available. If local disposable PostgreSQL is not available, perform the accepted VPS read-only preflight first and then create an isolated disposable PostgreSQL test database on the VPS only after inspection.

The operator rule remains:

> **one short command per step → inspect output → continue.**

---

## 9. Checkpoint decision

**J2 Migration 001 SQL Draft v1 — PRE-TEST CORRECTIONS COMPLETE.**

The SQL is now suitable to enter the executable disposable-test cycle. It is still **not approved for direct production migration** until the test cycle and VPS preflight pass.
