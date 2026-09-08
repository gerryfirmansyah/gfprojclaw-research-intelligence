# J2 Migration 001 SQL Draft v0

Status: **J2 ACTIVE — SQL DRAFT CREATED / NOT APPLIED**

## 1. Purpose

This checkpoint converts the accepted Migration 001 Design & Fixture Contract into executable PostgreSQL draft artifacts without applying them to the production database.

The governing principle remains:

> **Prove the canonical evidence-to-judgment path with strong provenance, local failure semantics, explicit coverage, and separate HUMAN authority before expanding the research object model.**

## 2. Draft Artifacts

```text
db/migrations/001_canonical_vertical_slice.sql
db/fixtures/001_vertical_slice_reference.sql
db/verify/001_vertical_slice_verify.sql
```

The migration creates the accepted **21-table canonical first slice**. The fixture provides deterministic synthetic data for both reference Profiles. The verification script checks structural and scientific-integrity invariants and emits inspectable end-to-end traces.

## 3. Migration Draft Decisions

The SQL draft implements:

- PostgreSQL `uuid` primary keys with `gen_random_uuid()`;
- `timestamptz` for retrieval, observation, assessment, decision, and creation times;
- `text + CHECK` controlled vocabularies rather than PostgreSQL ENUM;
- explicit `ON DELETE RESTRICT` along scientific/provenance history;
- bounded JSONB only for provider/configuration/scope/locator/snapshot context;
- append-oriented supersession links for Claim, EvidenceRelationship, Assessment, and HumanDecision;
- strongly typed provenance tables plus `research_object_identity` and the first typed object `gap_candidate`;
- no scientific acceptance threshold and no global workflow gate.

## 4. Integrity Strengthening in the Draft

Two invariants that were previously listed as service/integrity-test candidates are enforced directly with ordinary relational constraints where possible.

### 4.1 Current-version ownership

Composite foreign keys ensure:

```text
research_profile.current_version_id belongs to the same research_profile
research_project.current_version_id belongs to the same research_project
```

This avoids a trigger while retaining strong identity integrity.

### 4.2 Project alignment for generic research-object targets

`research_object_identity` exposes a composite candidate key `(id, project_id)`. The first-slice typed and temporal tables use this to ensure:

```text
gap_candidate.project_id = research_object_identity.project_id
assessment.project_id matches target object project
change_event.project_id matches primary object project
human_decision.project_id matches primary object project
```

The remaining typed-object invariant:

```text
gap_candidate.id → research_object_identity.object_type = GAP_CANDIDATE
```

is verified by the verification script in v0 rather than by a trigger.

## 5. Quarantine Draft Behavior

The draft keeps quarantine local.

For `evidence_fragment` and `claim`:

- `ACTIVE` requires no quarantine reason;
- `QUARANTINED` requires an inspectable reason;
- a quarantined Claim also uses the canonical `QUARANTINED` review state.

Verification additionally rejects fixture states where an active Claim depends on a quarantined fragment or a non-quarantined EvidenceRelationship depends on a quarantined Claim.

This is local-write integrity only. It does not stop unrelated ingestion, extraction, assessment, or crawling.

## 6. Cross-Domain Fixture Contract Implemented

The deterministic fixture contains:

### Profile A — Computer / Information Systems

One synthetic Project, one synthetic contested GapCandidate, two synthetic Works, two EvidenceFragments, two atomic Claims, and both `SUPPORTS` and `CHALLENGES` EvidenceRelationships.

### Profile B — Management / Organization Studies

The same canonical mechanics are used: one synthetic Project, one synthetic contested GapCandidate, two synthetic Works, two EvidenceFragments, two atomic Claims, and both `SUPPORTS` and `CHALLENGES` EvidenceRelationships.

There is no domain-specific table, migration path, Gap engine, or evidence mechanism.

All fixture content is explicitly synthetic and must not be interpreted as real literature or real scientific evidence.

## 7. Advice, Change, Coverage, and HUMAN Authority Fixture

Each reference Project includes:

- one immutable CoverageContext snapshot;
- source-level `HEALTHY` and `DEGRADED` coverage states;
- one Assessment with decomposed dimensions;
- one meaningful `GAP_CONTESTED` ChangeEvent;
- one HUMAN `NEED_MORE_EVIDENCE` decision.

The fixture deliberately demonstrates that:

```text
machine advice ≠ HUMAN decision
source degradation ≠ project failure
support evidence + challenge evidence ≠ automatic verdict
```

## 8. Verification Contract Implemented

The verification SQL checks:

1. all 21 canonical tables exist;
2. current Profile/Project versions belong to the correct owner;
3. GapCandidate identity type and Project alignment are correct;
4. Claim → EvidenceFragment → Work provenance is intact;
5. `METADATA_ONLY` records do not create EvidenceFragments;
6. Assessment, ChangeEvent, and HumanDecision targets match Project context;
7. CoverageContext uses the correct Profile and Project version lineage;
8. both Profile A and Profile B contain supporting and challenging evidence;
9. each reference Gap traces to at least two Works;
10. local quarantine dependencies remain consistent.

It then emits three inspectable views:

```text
Gap → EvidenceRelationship → Claim → EvidenceFragment → Work → SourceRecord → LiteratureSource
Assessment → HumanDecision
CoverageContext → CoverageSourceState
```

## 9. Deliberately Not Implemented

Migration 001 still does not introduce:

- Theory;
- Method;
- Concept/Construct;
- ExistingSolution;
- CandidateContribution;
- Synthesis;
- R0–R16 persistence;
- scheduler/run/job tables;
- crawler orchestration;
- add-in/plugin runtime;
- production Dashboard queries;
- Telegram delivery logic.

These remain later vertical extensions.

## 10. Production Safety Status

**The SQL draft has been committed to GitHub but has not been executed against the production PostgreSQL database.**

No legacy table, trigger, service, gate, or historical artifact is modified by this drafting step.

Before application, the SQL should receive a focused executable review for:

- PostgreSQL 16 syntax;
- existing-name collisions;
- `pgcrypto` availability/permissions;
- migration-runner convention;
- legacy-schema coexistence;
- fixture isolation from production data;
- verification behavior on a clean test database.

## 11. J2 Checkpoint

```text
Research Object Model                      ACTIVE
Relationship & Cardinality                 ACCEPTED
Generic Identity & Association             ACCEPTED
PostgreSQL Persistence Shape               ACCEPTED
Minimum Canonical Vertical Slice           ACCEPTED
Canonical DDL Contract                     ACCEPTED BASELINE
Migration 001 Design & Fixture Contract    ACCEPTED BASELINE
Migration 001 SQL Draft                    CREATED — REVIEW REQUIRED
```

## 12. Recommended Next Step

The next step is:

> **J2 Migration 001 Executable Review & Test Plan v0**

That review should inspect these exact SQL files for dependency order, constraint behavior, migration safety, fixture determinism, and expected verification outputs before any server execution.
