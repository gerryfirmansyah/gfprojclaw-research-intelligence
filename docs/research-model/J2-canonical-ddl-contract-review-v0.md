# J2 Canonical DDL Contract Review v0

Status: **J2 ACTIVE — Canonical DDL Contract Review**

## 1. Purpose

This review converts the accepted J2 persistence shape and minimum vertical slice into a **concrete PostgreSQL DDL contract** before any production migration is written.

The goal is to lock the durable database semantics that matter for scientific integrity:

- canonical table names;
- primary-key strategy;
- required vs optional columns;
- foreign-key direction;
- check and unique constraints;
- version and supersession semantics;
- deletion behavior;
- indexing expectations;
- bounded JSONB usage;
- append-oriented historical records;
- local failure/quarantine semantics;
- cross-domain compatibility.

The governing principle is:

> **DDL constraints protect evidence lineage and object identity; they must not encode scientific verdicts or global workflow gates.**

This document is the contract for the first migration design. It is not itself a migration file.

---

## 2. Inputs

This contract is derived from:

- J1 accepted UX and integration review;
- J2 Research Object Model;
- J2 Object Relationship & Cardinality Review;
- J2 Generic Identity & Association Model Review;
- J2 PostgreSQL Persistence Shape Review;
- J2 Minimum Canonical Schema / Vertical Slice Review.

The first-slice canonical trace remains:

```text
LiteratureSource
  → SourceRecord
  → Work
  → EvidenceFragment
  → Claim
  → EvidenceRelationship
  → GapCandidate
  → Assessment
  → ChangeEvent
  → HumanDecision
```

with `ResearchProfile`, `ResearchProject`, `ProjectWorkRelevance`, and `CoverageContext` providing scientific context.

---

## 3. Database Namespace

### Decision

For the first migration, use ordinary PostgreSQL tables in one application schema unless the existing deployment already has a safe, established application schema convention.

Do **not** create domain-specific schemas such as:

```text
it_governance.*
management.*
```

### Recommended logical grouping

Table names remain explicit and portable:

```text
research_profile
research_project
work
claim
gap_candidate
...
```

A separate schema namespace may be introduced later for deployment hygiene, but it must not encode research-domain semantics.

---

## 4. Identifier Contract

### Decision

All canonical first-slice primary keys use PostgreSQL `uuid`.

Recommended default direction:

```sql
id uuid PRIMARY KEY DEFAULT gen_random_uuid()
```

This assumes `pgcrypto` is available. If the existing installation already uses a different approved UUID generator, the migration may adapt without changing the logical contract.

### Rules

- natural identifiers are never universal primary keys;
- DOI remains a Work identifier, not a row identity;
- IDs exposed to Dashboard/Telegram must remain stable;
- supersession never changes the stable identity of an historical row.

---

## 5. Timestamp Contract

Use `timestamptz` for system/retrieval/decision timestamps.

Default creation timestamp:

```sql
created_at timestamptz NOT NULL DEFAULT now()
```

The schema must distinguish where relevant:

```text
publication_date   external publication time/date
retrieved_at       source retrieval time
observed_at        scientific/coverage observation time
assessed_at        machine assessment time
decided_at         HUMAN decision time
created_at         database record creation time
```

Do not reuse `created_at` to mean all of these.

---

## 6. Vocabulary Storage Contract

### Decision

For v0, use `text` columns plus `CHECK` constraints for small stable vocabularies rather than PostgreSQL ENUM types.

Reason:

- vocabularies may evolve during J2/J3;
- `CHECK` constraints are easier to migrate;
- the core must remain domain-agnostic.

Example:

```sql
access_level text NOT NULL
CHECK (access_level IN ('FULL_TEXT','ABSTRACT_ONLY','METADATA_ONLY'))
```

PostgreSQL ENUM may be reconsidered only after vocabularies prove stable.

---

## 7. JSONB Contract

JSONB is allowed only where structure is genuinely provider/configuration/snapshot-flexible.

Allowed first-slice uses include:

- Profile/Project configuration;
- provider raw metadata;
- evidence locator;
- Claim scope/context;
- Gap scope/context;
- bounded ChangeEvent state snapshots;
- coverage query/access/extraction summaries.

JSONB must **not** replace canonical rows for:

- EvidenceRelationship;
- HumanDecision;
- AssessmentDimension;
- Work identifiers;
- Work-to-source normalization;
- Project-to-Work relevance;
- Gap evidence lineage.

---

## 8. Deletion Contract

### Core rule

Use `ON DELETE RESTRICT` or `NO ACTION` for canonical scientific/provenance chains unless a child is purely structural and cannot have independent historical meaning.

Avoid broad `ON DELETE CASCADE` across evidence and scientific history.

### Why

Deleting a Work must not silently destroy Claims, Assessments, ChangeEvents, or HumanDecisions that formed part of historical scientific reasoning.

### Permitted cascade candidates

Only narrowly structural rows may use cascade where loss has no independent scientific meaning, for example some version-owned configuration rows introduced later.

### Normal evolution

Scientific evolution is represented by:

- lifecycle state;
- supersedes links;
- review state;
- quarantine state;
- new historical records.

It is not represented by routine deletion.

---

## 9. Versioning Contract

Versioned entities use explicit immutable version rows.

For Profile and Project:

```text
stable identity table
+
version table
```

A version row should not be updated to represent a new scientific/configuration state. Create a new version row and link it through `supersedes_version_id`.

For assessments, decisions, relationships, and claims, historical change is also append-oriented using new rows and optional `supersedes_*_id` links.

No trigger may silently rewrite historical assessments or HumanDecisions.

---

# 10. Canonical First-Slice DDL Contracts

The first slice contains 20 canonical tables.

---

## 10.1 `research_profile`

Purpose: stable identity for reusable research context.

```text
id                  uuid PK
name                text NOT NULL
status              text NOT NULL
current_version_id  uuid NULL
created_at          timestamptz NOT NULL
created_by          text NULL
```

Constraints:

```text
status IN ('ACTIVE','INACTIVE','ARCHIVED')
name not blank
```

Foreign key:

`current_version_id → research_profile_version.id` is added after both tables exist and must reference a version belonging to the same profile. Same-profile validation may initially be enforced by service/integrity test if a simple FK cannot express it.

Deletion: RESTRICT if referenced by Projects, object identity, or coverage history.

Indexes:

- unique normalized Profile name is **not required** globally;
- index on `status` only if query plans later justify it.

---

## 10.2 `research_profile_version`

```text
id                      uuid PK
profile_id              uuid NOT NULL FK → research_profile.id
version_no              integer NOT NULL
summary                 text NULL
configuration_jsonb     jsonb NOT NULL DEFAULT '{}'
supersedes_version_id   uuid NULL FK → research_profile_version.id
created_at              timestamptz NOT NULL
created_by              text NULL
```

Constraints:

```text
version_no > 0
UNIQUE(profile_id, version_no)
supersedes_version_id <> id
```

Deletion: RESTRICT once referenced by CoverageContext or historical processing.

Indexes:

```text
(profile_id, version_no DESC)
```

---

## 10.3 `research_project`

```text
id                  uuid PK
profile_id          uuid NOT NULL FK → research_profile.id
name                text NOT NULL
status              text NOT NULL
current_version_id  uuid NULL
created_at          timestamptz NOT NULL
created_by          text NULL
```

Constraints:

```text
status IN ('ACTIVE','PAUSED','ARCHIVED')
name not blank
```

Deletion: RESTRICT if any scientific, evidence, assessment, coverage, or decision record exists.

Index:

```text
(profile_id, status)
```

---

## 10.4 `research_project_version`

```text
id                          uuid PK
project_id                  uuid NOT NULL FK → research_project.id
version_no                  integer NOT NULL
research_intent             text NULL
provisional_rq_text         text NULL
project_configuration_jsonb jsonb NOT NULL DEFAULT '{}'
supersedes_version_id       uuid NULL FK → research_project_version.id
created_at                  timestamptz NOT NULL
created_by                  text NULL
```

Constraints:

```text
version_no > 0
UNIQUE(project_id, version_no)
supersedes_version_id <> id
```

Index:

```text
(project_id, version_no DESC)
```

---

## 10.5 `literature_source`

```text
id                      uuid PK
source_key              text NOT NULL
name                    text NOT NULL
source_type             text NOT NULL
active                  boolean NOT NULL DEFAULT true
configuration_reference text NULL
created_at              timestamptz NOT NULL
```

Constraints:

```text
UNIQUE(source_key)
source_key not blank
```

`configuration_reference` must never contain credentials/secrets directly.

Deletion: RESTRICT when SourceRecords or coverage history exist.

---

## 10.6 `source_record`

```text
id                         uuid PK
literature_source_id       uuid NOT NULL FK → literature_source.id
source_record_identifier   text NOT NULL
retrieved_at               timestamptz NOT NULL
raw_metadata_jsonb         jsonb NOT NULL DEFAULT '{}'
content_access_state       text NOT NULL
normalization_state        text NOT NULL
provenance_hash            text NULL
created_at                 timestamptz NOT NULL
```

Constraints:

```text
content_access_state IN ('FULL_TEXT','ABSTRACT_ONLY','METADATA_ONLY')
normalization_state IN ('UNRESOLVED','MATCHED','NEW_WORK','AMBIGUOUS','QUARANTINED')
UNIQUE(literature_source_id, source_record_identifier, retrieved_at)
```

Important: repeated retrieval of the same external record is allowed at different retrieval times.

Indexes:

```text
(literature_source_id, source_record_identifier)
(retrieved_at DESC)
```

Deletion: RESTRICT once normalized or used for evidence provenance.

---

## 10.7 `work`

```text
id                    uuid PK
title                 text NOT NULL
publication_date      date NULL
publication_year      smallint NULL
venue                 text NULL
work_type             text NULL
current_access_level  text NOT NULL
created_at            timestamptz NOT NULL
updated_at            timestamptz NOT NULL
```

Constraints:

```text
current_access_level IN ('FULL_TEXT','ABSTRACT_ONLY','METADATA_ONLY')
publication_year IS NULL OR publication_year BETWEEN 1000 AND 3000
title not blank
```

Do not make `(title, year)` unique.

Deletion: RESTRICT once linked to evidence, source records, or projects.

Index:

```text
(publication_year DESC)
```

---

## 10.8 `work_identifier`

```text
id                uuid PK
work_id           uuid NOT NULL FK → work.id
identifier_type   text NOT NULL
identifier_value  text NOT NULL
is_primary        boolean NOT NULL DEFAULT false
created_at        timestamptz NOT NULL
```

Constraints:

```text
identifier_type IN ('DOI','OPENALEX','SEMANTIC_SCHOLAR','PMID','ISBN','OTHER')
UNIQUE(identifier_type, identifier_value)
UNIQUE(work_id, identifier_type, identifier_value)
```

Identifier normalization must occur before persistence where applicable, especially DOI.

Index:

```text
(work_id)
```

Deletion: RESTRICT unless administrative correction is explicit and provenance remains intact.

---

## 10.9 `work_source_record`

```text
id                uuid PK
work_id           uuid NOT NULL FK → work.id
source_record_id  uuid NOT NULL FK → source_record.id
match_method      text NOT NULL
match_state       text NOT NULL
matched_at        timestamptz NOT NULL
```

Constraints:

```text
UNIQUE(source_record_id)
UNIQUE(work_id, source_record_id)
match_state IN ('MATCHED','PROVISIONAL','HUMAN_REVIEWED')
```

Rationale: in the canonical state, one SourceRecord resolves to at most one Work. Ambiguous records remain unresolved rather than being linked to multiple Works.

Indexes:

```text
(work_id)
```

Deletion: RESTRICT after evidence lineage depends on the normalization.

---

## 10.10 `project_work_relevance`

```text
id                  uuid PK
project_id          uuid NOT NULL FK → research_project.id
work_id             uuid NOT NULL FK → work.id
relevance_state     text NOT NULL
relevance_advice    numeric(5,2) NULL
rationale           text NULL
origin              text NOT NULL
human_review_state  text NULL
first_seen_at       timestamptz NOT NULL
last_seen_at        timestamptz NOT NULL
created_at          timestamptz NOT NULL
```

Constraints:

```text
UNIQUE(project_id, work_id)
relevance_state IN ('CANDIDATE','RELEVANT','LOW_RELEVANCE','EXCLUDED','NEEDS_REVIEW')
relevance_advice IS NULL OR relevance_advice BETWEEN 0 AND 100
```

`relevance_advice` is ranking advice, not truth probability.

Indexes:

```text
(project_id, relevance_state)
(project_id, last_seen_at DESC)
```

Deletion: prefer state transition to `EXCLUDED`; do not delete merely because relevance decreased.

---

## 10.11 `evidence_fragment`

```text
id                  uuid PK
work_id             uuid NOT NULL FK → work.id
source_record_id    uuid NULL FK → source_record.id
access_level        text NOT NULL
fragment_type       text NOT NULL
locator_jsonb       jsonb NOT NULL DEFAULT '{}'
text_or_reference   text NOT NULL
content_hash        text NULL
extraction_version  text NULL
quarantine_state    text NOT NULL DEFAULT 'ACTIVE'
quarantine_reason   text NULL
created_at          timestamptz NOT NULL
```

Constraints:

```text
access_level IN ('FULL_TEXT','ABSTRACT_ONLY')
fragment_type IN ('PASSAGE','ABSTRACT_SEGMENT','STRUCTURED_RECORD_EXCERPT')
quarantine_state IN ('ACTIVE','QUARANTINED')
(quarantine_state = 'ACTIVE' AND quarantine_reason IS NULL)
 OR quarantine_state = 'QUARANTINED'
```

Critical rule: `METADATA_ONLY` cannot create passage-level EvidenceFragments.

Indexes:

```text
(work_id)
(source_record_id) where source_record_id is not null
(content_hash) where content_hash is not null
```

Deletion: RESTRICT when Claims exist.

---

## 10.12 `claim`

```text
id                    uuid PK
evidence_fragment_id  uuid NOT NULL FK → evidence_fragment.id
claim_text            text NOT NULL
claim_type            text NULL
scope_jsonb           jsonb NOT NULL DEFAULT '{}'
extraction_origin     text NOT NULL
review_state          text NOT NULL
supersedes_claim_id   uuid NULL FK → claim.id
quarantine_state      text NOT NULL DEFAULT 'ACTIVE'
quarantine_reason     text NULL
created_at            timestamptz NOT NULL
```

Constraints:

```text
review_state IN ('MACHINE_EXTRACTED','NEEDS_REVIEW','HUMAN_REVIEWED','CONTESTED','QUARANTINED')
quarantine_state IN ('ACTIVE','QUARANTINED')
supersedes_claim_id <> id
claim_text not blank
```

Critical invariant:

> Every canonical atomic Claim has exactly one primary EvidenceFragment.

Indexes:

```text
(evidence_fragment_id)
(review_state)
```

Deletion: RESTRICT if EvidenceRelationships exist. Correction uses supersession/quarantine.

---

## 10.13 `research_object_identity`

```text
id               uuid PK
object_type      text NOT NULL
profile_id       uuid NULL FK → research_profile.id
project_id       uuid NULL FK → research_project.id
canonical_label  text NOT NULL
lifecycle_state  text NOT NULL
origin           text NOT NULL
created_at       timestamptz NOT NULL
created_by       text NULL
```

For first slice:

```text
object_type IN ('GAP_CANDIDATE')
```

The migration structure must make future extension straightforward; do not embed domain labels into the constraint.

Scope constraint:

A Project-scoped GapCandidate must have `project_id` set. A future general scope model may add shared/profile objects.

Lifecycle vocabulary v0:

```text
ACTIVE
INACTIVE
SUPERSEDED
QUARANTINED
```

Index:

```text
(project_id, object_type, lifecycle_state)
```

Deletion: RESTRICT when referenced by evidence, assessments, change events, or decisions.

---

## 10.14 `gap_candidate`

Shared-primary-key typed table:

```text
id                       uuid PK/FK → research_object_identity.id
project_id               uuid NOT NULL FK → research_project.id
gap_type                 text NOT NULL
statement                text NOT NULL
scope_jsonb              jsonb NOT NULL DEFAULT '{}'
current_evolution_state  text NOT NULL
created_at               timestamptz NOT NULL
```

Constraints:

```text
gap_type IN ('EXPLICIT_GAP','EMPIRICAL_GAP','THEORETICAL_GAP','SYNTHESIS_GAP')
current_evolution_state IN ('CANDIDATE','STRENGTHENING','WEAKENING','CONTESTED','POSSIBLY_CLOSED','REOPENED')
statement not blank
```

Application/integrity test invariant:

```text
research_object_identity.object_type = 'GAP_CANDIDATE'
research_object_identity.project_id = gap_candidate.project_id
```

Machine evolution state is not HumanDecision.

Index:

```text
(project_id, current_evolution_state)
(project_id, gap_type)
```

Deletion: RESTRICT; use lifecycle/supersession semantics.

---

## 10.15 `evidence_relationship`

```text
id                         uuid PK
claim_id                   uuid NOT NULL FK → claim.id
target_research_object_id  uuid NOT NULL FK → research_object_identity.id
semantic_type              text NOT NULL
rationale                  text NULL
origin                     text NOT NULL
review_state               text NOT NULL
supersedes_relationship_id uuid NULL FK → evidence_relationship.id
created_at                 timestamptz NOT NULL
```

Constraints:

```text
semantic_type IN ('SUPPORTS','CHALLENGES','EXTENDS','REPLICATES','CONTRADICTS','ADDRESSES')
review_state IN ('MACHINE_SUGGESTED','NEEDS_REVIEW','HUMAN_REVIEWED','CONTESTED','QUARANTINED')
supersedes_relationship_id <> id
```

Do not impose uniqueness on `(claim_id, target_research_object_id)` because one Claim may have more than one distinct semantic interpretation over time or under review. Historical/superseded rows must remain possible.

Indexes:

```text
(target_research_object_id, semantic_type)
(claim_id)
(review_state)
```

Deletion: RESTRICT; correction uses supersession/quarantine.

---

## 10.16 `coverage_context`

```text
id                       uuid PK
project_id               uuid NOT NULL FK → research_project.id
profile_version_id       uuid NOT NULL FK → research_profile_version.id
project_version_id       uuid NULL FK → research_project_version.id
observed_at              timestamptz NOT NULL
query_context_jsonb      jsonb NOT NULL DEFAULT '{}'
temporal_window_jsonb    jsonb NOT NULL DEFAULT '{}'
access_summary_jsonb     jsonb NOT NULL DEFAULT '{}'
extraction_summary_jsonb jsonb NOT NULL DEFAULT '{}'
counter_search_state     text NOT NULL
limitations              text NULL
created_at               timestamptz NOT NULL
```

Constraints:

```text
counter_search_state IN ('NOT_RUN','PARTIAL','RUN','DEGRADED')
```

CoverageContext is a snapshot; do not update historical snapshots to reflect later improvements.

Indexes:

```text
(project_id, observed_at DESC)
(profile_version_id)
```

Deletion: RESTRICT once referenced by Assessment, ChangeEvent, or HumanDecision.

---

## 10.17 `coverage_source_state`

```text
id                     uuid PK
coverage_context_id    uuid NOT NULL FK → coverage_context.id
literature_source_id   uuid NOT NULL FK → literature_source.id
health_state           text NOT NULL
attempted_record_count integer NULL
observed_record_count  integer NULL
access_limitations     text NULL
degradation_reason     text NULL
created_at             timestamptz NOT NULL
```

Constraints:

```text
UNIQUE(coverage_context_id, literature_source_id)
health_state IN ('HEALTHY','DEGRADED','BACKOFF','DISABLED','ATTENTION')
attempted_record_count IS NULL OR attempted_record_count >= 0
observed_record_count IS NULL OR observed_record_count >= 0
```

No constraint requires every configured source to be HEALTHY.

This table must never become a global gate.

Index:

```text
(literature_source_id, created_at DESC)
```

---

## 10.18 `assessment`

```text
id                         uuid PK
project_id                 uuid NOT NULL FK → research_project.id
target_research_object_id  uuid NOT NULL FK → research_object_identity.id
coverage_context_id        uuid NULL FK → coverage_context.id
assessment_type            text NOT NULL
model_or_agent             text NULL
model_version              text NULL
explanation_summary        text NULL
assessed_at                timestamptz NOT NULL
supersedes_assessment_id   uuid NULL FK → assessment.id
created_at                 timestamptz NOT NULL
```

Constraints:

```text
supersedes_assessment_id <> id
```

No `accepted`, `passed`, or final-scientific-verdict column is permitted.

Indexes:

```text
(target_research_object_id, assessed_at DESC)
(project_id, assessed_at DESC)
```

Deletion: RESTRICT once referenced by HumanDecision or historical ChangeEvent context.

---

## 10.19 `assessment_dimension`

```text
id              uuid PK
assessment_id   uuid NOT NULL FK → assessment.id
dimension_type  text NOT NULL
value_numeric   numeric(6,2) NULL
value_text      text NULL
explanation     text NULL
created_at      timestamptz NOT NULL
```

Constraints:

```text
UNIQUE(assessment_id, dimension_type)
(value_numeric IS NOT NULL) OR (value_text IS NOT NULL)
```

Initial controlled dimensions:

```text
GAP_EVIDENCE_STRENGTH
COUNTER_EVIDENCE_RISK
EVIDENCE_COVERAGE_CONTEXT
REVIEW_PRIORITY
NOVELTY_POTENTIAL
THEORETICAL_SIGNIFICANCE
METHODOLOGICAL_FEASIBILITY
```

Not all dimensions are required on every Assessment.

Numeric values are advice scales, not probabilities.

No check such as `value_numeric >= threshold → accepted` is allowed.

Index:

```text
(assessment_id)
```

---

## 10.20 `change_event`

```text
id                          uuid PK
project_id                  uuid NOT NULL FK → research_project.id
primary_research_object_id  uuid NOT NULL FK → research_object_identity.id
coverage_context_id         uuid NULL FK → coverage_context.id
change_type                 text NOT NULL
observed_at                 timestamptz NOT NULL
previous_state_jsonb        jsonb NULL
current_state_jsonb         jsonb NULL
reasoning_delta             text NOT NULL
created_at                  timestamptz NOT NULL
```

Initial `change_type` examples:

```text
EVIDENCE_ADDED
EVIDENCE_CHALLENGED
EVIDENCE_CONTRADICTED
GAP_STRENGTHENED
GAP_WEAKENED
GAP_CONTESTED
GAP_POSSIBLY_CLOSED
GAP_REOPENED
ASSESSMENT_CHANGED
COVERAGE_CHANGED
```

Do not create a row merely for crawler/job success.

Indexes:

```text
(project_id, observed_at DESC)
(primary_research_object_id, observed_at DESC)
(change_type, observed_at DESC)
```

Deletion: RESTRICT; historical knowledge evolution must remain inspectable.

---

## 10.21 `human_decision`

The minimum vertical slice actually requires this table in addition to the previous 20-item grouping; therefore the canonical count is normalized here to **21 tables**. The earlier “20 tables” count is treated as a counting defect, not a semantic change.

```text
id                          uuid PK
project_id                  uuid NOT NULL FK → research_project.id
primary_research_object_id  uuid NOT NULL FK → research_object_identity.id
assessment_id               uuid NULL FK → assessment.id
coverage_context_id         uuid NULL FK → coverage_context.id
decision_type               text NOT NULL
rationale                   text NOT NULL
actor                       text NOT NULL
decided_at                  timestamptz NOT NULL
supersedes_decision_id      uuid NULL FK → human_decision.id
created_at                  timestamptz NOT NULL
```

Constraints:

```text
decision_type IN ('REVIEW','MODIFY','ACCEPT_DIRECTION','REJECT_CANDIDATE','NEED_MORE_EVIDENCE')
supersedes_decision_id <> id
rationale not blank
actor not blank
```

No FK or trigger may require a HumanDecision before:

- new crawling;
- new ingestion;
- new extraction;
- new Assessment;
- unrelated Project processing.

Indexes:

```text
(primary_research_object_id, decided_at DESC)
(project_id, decided_at DESC)
```

Deletion: RESTRICT; supersession preserves history.

---

## 11. Canonical Count Correction

The prior Minimum Canonical Schema review referred to **20 tables** while also listing `human_decision` as required. The concrete DDL enumeration above resolves the inconsistency.

### Decision

The correct first-slice canonical count is **21 tables**:

```text
1  research_profile
2  research_profile_version
3  research_project
4  research_project_version
5  literature_source
6  source_record
7  work
8  work_identifier
9  work_source_record
10 project_work_relevance
11 evidence_fragment
12 claim
13 research_object_identity
14 gap_candidate
15 evidence_relationship
16 coverage_context
17 coverage_source_state
18 assessment
19 assessment_dimension
20 change_event
21 human_decision
```

This is a documentation normalization, not scope expansion.

---

## 12. Foreign-Key Direction Contract

Canonical provenance must be traversable in both query direction and human navigation direction.

Core FK path:

```text
literature_source
  ← source_record
  ← work_source_record → work
                      ← evidence_fragment
                      ← claim
                      ← evidence_relationship → research_object_identity
                                             → gap_candidate
```

Project/scientific context:

```text
research_profile
  ← research_project
  ← project_work_relevance → work
  ← gap_candidate
  ← assessment
  ← change_event
  ← human_decision
```

Coverage context:

```text
coverage_context
  ← coverage_source_state
  ← assessment / change_event / human_decision
```

No reverse-denormalized ID arrays are canonical.

---

## 13. Required Integrity Tests Beyond Plain FKs

Some cross-table invariants are difficult to express with simple PostgreSQL foreign keys. They must therefore be enforced by service validation, migration-time tests, or a narrowly scoped database function/trigger if later justified.

Required integrity checks:

1. `research_profile.current_version_id` belongs to that Profile.
2. `research_project.current_version_id` belongs to that Project.
3. `gap_candidate.id` has `research_object_identity.object_type = GAP_CANDIDATE`.
4. `gap_candidate.project_id = research_object_identity.project_id`.
5. Assessment target belongs to an object visible in the same Project context.
6. ChangeEvent primary object belongs to/participates in the same Project context.
7. HumanDecision primary object belongs to/participates in the same Project context.
8. CoverageContext Profile version belongs to the Project’s Profile lineage.
9. `METADATA_ONLY` does not yield passage EvidenceFragments.
10. Quarantined Claims/relationships are excluded from evidence-backed promotion unless explicitly reviewed/reinstated.

These integrity checks must not become global processing locks. Violations quarantine or reject the local write.

---

## 14. Indexing Contract

Indexes must serve accepted cockpit/navigation and pipeline access paths, not speculative optimization.

Mandatory first-slice query paths:

```text
Project → recent Works
Project → GapCandidates
GapCandidate → EvidenceRelationships → Claims → EvidenceFragments → Works
GapCandidate → latest Assessments
Project → recent ChangeEvents
GapCandidate → HumanDecision history
Project → recent CoverageContext
CoverageContext → source states
```

Avoid blanket GIN indexes on every JSONB column in the first migration.

Add JSONB indexes only after a real query pattern exists.

---

## 15. Transaction Boundary Contract

The database must support local atomicity without requiring one giant transaction for an entire daily run.

Preferred transaction scopes:

```text
one SourceRecord normalization unit
one Work + identifier normalization unit
one EvidenceFragment + Claim extraction unit
one EvidenceRelationship creation/review unit
one Assessment snapshot
one ChangeEvent
one HumanDecision
one CoverageContext snapshot
```

A failure in one unit must not roll back unrelated healthy work from other sources/papers/projects.

This directly enforces the project principle:

> **LOCAL FAILURE, NO GLOBAL LOCK.**

---

## 16. Quarantine Contract

Quarantine is local and explicit.

In the first slice it is carried directly on:

```text
evidence_fragment
claim
```

and via review state on:

```text
evidence_relationship
```

A dedicated quarantine-event table may be added later if operational/audit needs justify it.

Rules:

- quarantined evidence is preserved;
- quarantine reason is inspectable;
- unrelated evidence continues;
- quarantine does not mark the entire Project invalid;
- quarantine does not stop crawling.

---

## 17. HUMAN Authority Contract

The schema must structurally separate:

```text
Assessment = machine/system advice
HumanDecision = HUMAN scientific judgment
```

Forbidden schema patterns include:

```text
assessment.is_accepted
assessment.final_verdict
score >= 80 → ACCEPT_DIRECTION
project.is_scientifically_approved
```

HumanDecision may reference an Assessment, but it does not derive mechanically from it.

---

## 18. Coverage Contract

CoverageContext is a first-class historical snapshot.

Forbidden patterns:

```text
project.coverage_score = 83
source_failure → project_status = FAILED
all_sources_healthy required before assessment
```

Permitted:

```text
CoverageContext COV-14
OpenAlex = HEALTHY
Semantic Scholar = DEGRADED
Counter-search = PARTIAL
```

and an Assessment/HumanDecision can explicitly reference `COV-14`.

---

## 19. Cross-Domain Validation

This DDL contract was checked against both reference Profiles.

### Profile A — Computer / Information Systems

Examples can be represented as data:

- IT governance capability;
- digital government;
- enterprise architecture;
- governance frameworks;
- design/evaluation methods.

### Profile B — Management / Organization Studies

Examples can be represented as data:

- organizational resilience;
- human capability;
- adaptive behaviour;
- theoretical gaps;
- survey/case/longitudinal methods.

No table name, FK, check constraint, or primary-key design depends on either discipline.

### Result

**PASS — same canonical schema shape for A and B.**

No Generality Exception is required at this stage.

---

## 20. Explicit Non-Goals of First DDL

Do not add yet unless required by implementation evidence:

- Theory table;
- Method table;
- Concept/Construct table;
- ScientificRelationship and participants;
- ExistingSolution / GapSolutionAssociation;
- CandidateContribution;
- Synthesis;
- R0–R16 persistence;
- crawler/run/job tables;
- generalized plugin/add-in registry;
- universal graph edge table;
- vector store schema;
- journal/Q1 positioning tables;
- composite research score.

These remain forward-compatible extensions.

---

## 21. Migration Ordering Recommendation

A safe first migration can be ordered by dependency:

```text
1. extension/UUID prerequisite if needed
2. research_profile
3. research_profile_version
4. research_project
5. research_project_version
6. literature_source
7. source_record
8. work
9. work_identifier
10. work_source_record
11. project_work_relevance
12. evidence_fragment
13. claim
14. research_object_identity
15. gap_candidate
16. evidence_relationship
17. coverage_context
18. coverage_source_state
19. assessment
20. assessment_dimension
21. change_event
22. human_decision
23. deferred current_version FKs / cross-table integrity helpers if used
24. indexes
```

This ordering is implementation guidance, not a workflow gate.

---

## 22. DDL Acceptance Tests

Before a migration is accepted, automated schema/integration tests must prove at minimum:

```text
A. One Profile can have multiple Projects.
B. Profile/Project versions preserve history.
C. One Work can normalize from multiple SourceRecords.
D. One SourceRecord cannot canonically map to multiple Works.
E. METADATA_ONLY Work can exist with zero EvidenceFragments.
F. Claim cannot exist without EvidenceFragment.
G. EvidenceRelationship cannot exist without Claim and target ResearchObjectIdentity.
H. GapCandidate uses generic research identity.
I. Assessment can be versioned without overwriting prior Assessment.
J. HumanDecision remains separate from Assessment.
K. Coverage can be DEGRADED without blocking new SourceRecords/Works/Claims.
L. Quarantining one Claim does not affect unrelated Claims.
M. New evidence can create ChangeEvent without changing prior HumanDecision.
N. Same schema fixtures work for Profile A and Profile B.
```

---

## 23. UI Mapping After DDL

Once the schema is implemented, dummy UI replacement proceeds incrementally:

```text
Profile / Project selectors
→ research_profile / research_project

Latest Papers
→ project_work_relevance / work

Evidence Explorer
→ evidence_fragment / claim / work

Research Opportunities
→ gap_candidate / evidence_relationship

Advice dimensions
→ assessment / assessment_dimension

Today / What Changed?
→ change_event

Human Review
→ human_decision

Coverage & Health
→ coverage_context / coverage_source_state
```

No separate UI-only scientific state should be introduced.

---

## 24. Review Result

### ACCEPTED BASELINE

The J2 canonical DDL contract is accepted as the design baseline for the first migration, subject to implementation-level syntax verification against the actual PostgreSQL 16 environment.

The core decisions are:

1. UUID stable identities.
2. `timestamptz` for system temporal semantics.
3. text + CHECK vocabularies for v0.
4. bounded JSONB only.
5. strongly typed provenance tables.
6. generic `research_object_identity` only for research-semantic objects.
7. typed `gap_candidate` as the first research object.
8. atomic Claim provenance.
9. typed EvidenceRelationship.
10. append-oriented Assessment, ChangeEvent, HumanDecision, and version history.
11. explicit CoverageContext.
12. RESTRICT-first deletion policy.
13. local quarantine/local failure, no global lock.
14. no score/assessment → HUMAN verdict constraint.
15. same DDL for both reference domains.

### Documentation normalization

The prior first-slice review’s “20 tables” count is corrected to **21 canonical tables** because `human_decision` was semantically included but omitted from the numeric total.

This is not scope growth.

---

## 25. J2 Status After This Review

```text
J2 Research Object Model                    ACTIVE
Relationship & Cardinality Review          ACCEPTED
Generic Identity & Association Review      ACCEPTED
PostgreSQL Persistence Shape Review        ACCEPTED
Minimum Canonical Schema / Vertical Slice  ACCEPTED
Canonical DDL Contract Review              ACCEPTED BASELINE
```

Next recommended J2 artifact:

> **J2 Migration 001 Design & Fixture Contract v0**

That artifact should translate this DDL contract into the first executable migration plan plus small cross-domain fixtures, but still separate schema design from legacy-data migration.