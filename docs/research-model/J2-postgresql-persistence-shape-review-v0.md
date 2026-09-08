# J2 PostgreSQL Persistence Shape Review v0

Status: **J2 ACTIVE — Persistence Shape Review**

## 1. Purpose

This review translates the accepted J2 conceptual model into a **PostgreSQL persistence shape** without yet writing production migrations.

The purpose is to decide:

- which conceptual objects deserve strongly typed tables;
- where a shared `research_object_identity` registry is useful;
- which associations deserve dedicated first-class tables;
- where JSONB is acceptable and where it would weaken scientific integrity;
- how to preserve provenance, temporal history, HUMAN authority, coverage context, and local-failure semantics;
- how to avoid both an over-normalized table explosion and an unconstrained EAV/graph schema;
- how Profile A and Profile B can use the same persistence model.

The governing principle is:

> **PostgreSQL should preserve scientific meaning and traceability first; convenience and compactness are secondary.**

This document defines **shape**, not final DDL.

---

## 2. Inputs to This Review

This review is derived from:

- J1 accepted UX;
- J2 Research Object Model;
- J2 Object Relationship & Cardinality Review;
- J2 Generic Identity & Association Model Review.

The core reasoning trace remains:

```text
LiteratureSource
    ↓
SourceRecord
    ↓
Work
    ↓
EvidenceFragment
    ↓
Claim
    ↓
EvidenceRelationship
    ↓
ResearchObjectIdentity + typed research object
    ↓
Assessment
    ↓
ChangeEvent
    ↓
HumanDecision
```

with `ResearchProfile`, `ResearchProject`, `RStageState`, and `CoverageContext` providing context around the chain.

---

## 3. Architectural Decision Summary

J2 adopts a **hybrid relational persistence model**:

```text
Strongly Typed Core Tables
+
Generic Research Object Identity Registry
+
Typed Scientific Object Tables
+
Typed Association Tables
+
Append-oriented Temporal Records
+
Bounded JSONB for flexible metadata only
```

The canonical PostgreSQL model must **not** be:

```text
one table: object(id, type, jsonb)
```

and must **not** be:

```text
one universal edges(subject_id, predicate, object_id)
```

Those approaches are too weak for the project's scientific integrity requirements.

---

## 4. Persistence Layers

The proposed persistence shape is organized into eight layers.

### Layer A — Research Context

- `research_profile`
- `research_profile_version`
- `research_project`
- `research_project_version`
- `watchlist`
- optional watchlist term/config tables later

### Layer B — Literature & Provenance

- `literature_source`
- `source_record`
- `work`
- `work_identifier`
- `work_source_record`
- `project_work_relevance`
- `evidence_fragment`
- `claim`

### Layer C — Generic Research Identity

- `research_object_identity`

### Layer D — Typed Scientific Research Objects

Potential tables:

- `concept`
- `definition`
- `scientific_relationship`
- `mechanism`
- `boundary_condition`
- `level_of_analysis`
- `theory`
- `model_framework`
- `method`
- `measurement`
- `gap_candidate`
- `existing_solution`
- `alternative`
- `candidate_contribution`
- `synthesis`

### Layer E — Scientific Associations

- `evidence_relationship`
- `research_object_association`
- `relationship_participant`
- `concept_measurement_association`
- `gap_solution_association`
- `gap_contribution_association`
- `contribution_association`
- `existing_solution_reference`
- `synthesis_membership`

### Layer F — Assessment, Time & HUMAN Authority

- `assessment`
- `assessment_dimension`
- `assessment_reason`
- `change_event`
- `change_event_evidence`
- `human_decision`
- `human_decision_context`

### Layer G — Research Journey

- `rstage_definition`
- `rstage_state`
- `rstage_impact`

### Layer H — Coverage & Operational Context

- `coverage_context`
- `coverage_source_state`
- `source_health_event` or later operational event tables
- optional job/run/quarantine tables later

Not every table above is required in the first migration. This review defines the durable shape from which an MVP subset can be selected.

---

## 5. Primary Key Strategy

### Decision

Use stable opaque identifiers as primary keys.

Recommended implementation direction:

```text
UUID
```

or another stable globally unique identifier available in PostgreSQL.

### Why

The system will:

- ingest incrementally;
- merge provider records;
- evolve objects over time;
- expose stable links in Dashboard/Telegram;
- potentially import/export research state;
- preserve references through migrations.

Natural identifiers such as DOI remain unique identifiers where available but should not serve as universal primary keys.

### Rule

A DOI identifies a Work candidate, not every scientific object.

---

## 6. Timestamp Strategy

Canonical records should use timezone-aware timestamps.

Conceptually:

```text
created_at
updated_at
observed_at
valid_from / superseded_at where needed
```

The persistence model should distinguish:

- when external evidence was published;
- when the system discovered/retrieved it;
- when an extraction or assessment occurred;
- when a HUMAN decision occurred.

These are scientifically different times.

---

## 7. Soft Deletion vs Scientific History

### Decision

Do not rely on generic soft deletion as the main history mechanism.

Scientific objects may become:

- superseded;
- rejected for a Project;
- quarantined;
- no longer active;
- possibly closed;
- replaced by a refined formulation.

These are not equivalent to “deleted.”

### Recommended pattern

Use explicit lifecycle/history semantics where scientifically meaningful.

Physical deletion should be reserved for administrative/data-retention needs, not normal research evolution.

---

## 8. Research Profile Persistence

### `research_profile`

Represents stable Profile identity.

Candidate columns:

```text
id
name
status
current_version_id
created_at
created_by
```

### `research_profile_version`

Represents mutable scientific/configuration content over time.

Candidate columns:

```text
id
profile_id
version_no
summary / description
configuration_jsonb
created_at
created_by
supersedes_version_id
```

### Why version separately?

Because Profile changes influence discovery and coverage interpretation.

Historical assessments must be able to say:

> this assessment was generated under Profile v3.

### JSONB allowance

Profile configuration is a reasonable place for bounded JSONB because watchlist/search preference structures may evolve.

But important entities such as Projects, Works, Claims, and Decisions must not live only inside profile JSON.

---

## 9. Research Project Persistence

### `research_project`

Stable project identity.

Candidate columns:

```text
id
profile_id
name
status
current_version_id
created_at
created_by
```

### `research_project_version`

Candidate mutable content:

```text
id
project_id
version_no
research_intent
provisional_rq_text
project_configuration_jsonb
created_at
supersedes_version_id
```

### Decision

Profile and Project both use stable identity + explicit version records.

This supports Knowledge Evolution without treating configuration changes as destructive updates.

---

## 10. Watchlist Persistence

Recommended v0 shape:

```text
watchlist
- id
- scope_type: PROFILE | PROJECT
- profile_id nullable
- project_id nullable
- name
- active
- configuration_jsonb
- created_at
```

### Constraint

Exactly one scope owner must be set.

This can be enforced by a check constraint later.

### Why JSONB here?

Watchlist targeting may include combinations of terms, concepts, authors, venues, methods, etc. The detailed query-generation representation is implementation-specific and should remain evolvable.

However, important linked research objects can later gain normalized association rows where required.

---

## 11. Literature Source Persistence

### `literature_source`

Candidate fields:

```text
id
source_key
name
source_type
active
configuration_reference
created_at
```

Secrets must not be stored casually in research-facing config tables.

Operational credentials belong in secure configuration outside ordinary scientific records.

---

## 12. Source Record Persistence

### `source_record`

Represents exactly what one provider returned or one provider-facing normalized retrieval record.

Candidate fields:

```text
id
literature_source_id
source_record_identifier
retrieved_at
raw_metadata_jsonb
content_access_state
normalization_state
provenance_hash
created_at
```

### JSONB decision

Raw provider metadata is an appropriate JSONB use case.

Reason:

- providers differ;
- field sets change;
- raw provenance should be preserved;
- not every provider field belongs in normalized canonical columns.

### Rule

Scientific reasoning should not query arbitrary raw JSON as its primary evidence model.

Normalized Work/Evidence/Claim tables remain canonical for research reasoning.

---

## 13. Work Persistence

### `work`

Candidate normalized fields:

```text
id
title
publication_date
publication_year
venue
work_type
current_access_level
created_at
updated_at
```

### `work_identifier`

Instead of many nullable identifier columns:

```text
id
work_id
identifier_type
identifier_value
is_primary
```

Examples:

- DOI
- PMID
- OpenAlex ID
- Semantic Scholar ID
- ISBN where applicable

### Constraint

Uniqueness should generally apply to normalized identifier type/value pairs where appropriate.

### `work_source_record`

Many source records may normalize to one Work.

```text
work_id
source_record_id
match_method
match_state
matched_at
```

### Decision

This separation is important and should survive into production.

---

## 14. Project ↔ Work Persistence

### `project_work_relevance`

This is a first-class association.

Candidate fields:

```text
id
project_id
work_id
relevance_state
relevance_advice
rationale
first_seen_at
last_seen_at
human_review_state
origin
```

### Why not put `project_id` on Work?

Because one Work can be relevant to many Projects and interpretation is project-specific.

---

## 15. Evidence Fragment Persistence

### `evidence_fragment`

Candidate fields:

```text
id
work_id
source_record_id nullable
access_level
fragment_type
locator_jsonb
text_or_reference
content_hash
extraction_version
created_at
quarantine_state
quarantine_reason
```

### Locator JSONB

An acceptable flexible field because source location varies:

- page;
- section;
- paragraph;
- abstract segment;
- structured record path.

### Rights boundary

The persistence model must support storing either:

- bounded text when permitted;
- a source reference/locator when full storage is not permitted.

J2 does not define copyright storage implementation.

---

## 16. Claim Persistence

### `claim`

Candidate fields:

```text
id
evidence_fragment_id
claim_text
claim_type
scope_jsonb
extraction_origin
review_state
created_at
supersedes_claim_id nullable
quarantine_state
quarantine_reason
```

### Critical integrity rule

Every atomic evidence-backed Claim must reference exactly one primary EvidenceFragment.

This should become a non-null foreign key in the production schema.

### Consequence

Multi-paper interpretation belongs in `synthesis`, not in a floating claim detached from provenance.

---

## 17. Research Object Identity Persistence

### `research_object_identity`

This is the generic registry for reusable scientific/research-semantic objects.

Candidate fields:

```text
id
object_type
profile_id nullable
project_id nullable
canonical_label
lifecycle_state
origin
created_at
created_by
```

### Scope rule

Some research objects may be global/profile-shared; others are project-specific.

The scope model should therefore support:

- shared/global scientific object;
- profile-scoped object;
- project-scoped interpretation/candidate.

### Important rule

`research_object_identity` does not hold all typed scientific content.

Each object type has a corresponding typed table whose primary key is also the research object identity.

Recommended pattern:

```text
research_object_identity.id
        1:1
concept.id
```

or equivalent shared-primary-key structure.

---

## 18. Typed Research Object Tables

The preferred shape is **class-table inheritance by convention**, not PostgreSQL table inheritance.

Example:

```text
research_object_identity
  id = RO-014
  object_type = GAP_CANDIDATE

            ↓ 1:1

gap_candidate
  id = RO-014
  gap_type = THEORETICAL_GAP
  statement = ...
  evolution_state = CONTESTED
```

### Why avoid PostgreSQL table inheritance?

Because ordinary foreign-key behavior, tooling, migrations, and ORM/query semantics are generally clearer with explicit tables.

### Decision

Use ordinary typed tables sharing/referencing the generic identity key.

---

## 19. Candidate Typed Table Shapes

### `concept`

```text
id PK/FK research_object_identity
preferred_term
description
```

### `definition`

```text
id PK/FK research_object_identity
concept_id FK research_object_identity/concept
definition_text
source_kind
```

### `theory`

```text
id PK/FK research_object_identity
name
description
```

### `method`

```text
id PK/FK research_object_identity
method_category
name
description
```

### `mechanism`

```text
id PK/FK research_object_identity
statement / description
```

### `gap_candidate`

```text
id PK/FK research_object_identity
project_id
gap_type
statement
current_evolution_state
scope_jsonb
```

### `existing_solution`

```text
id PK/FK research_object_identity
project_id
summary
interpretation_state
```

### `candidate_contribution`

```text
id PK/FK research_object_identity
project_id
contribution_type
statement
```

### `synthesis`

```text
id PK/FK research_object_identity
project_id
synthesis_type
summary
current_version_no
```

These are shape examples, not final columns.

---

## 20. Object Type Enforcement

A typed row should agree with its generic identity type.

Example:

A row in `gap_candidate` must reference a `research_object_identity` with:

```text
object_type = GAP_CANDIDATE
```

### Enforcement options later

- application/service validation;
- trigger/check helper;
- constrained insert functions;
- migration-generated integrity tests.

### Decision

This invariant is important, but J2 does not yet choose the enforcement mechanism.

---

## 21. Evidence Relationship Persistence

### `evidence_relationship`

Candidate fields:

```text
id
claim_id
target_research_object_id
semantic_type
rationale
origin
review_state
created_at
supersedes_relationship_id nullable
```

### Hard structural constraints

- source must be one Claim;
- target must be one ResearchObjectIdentity;
- relationship semantics are explicit;
- no arbitrary subject type.

### Initial semantic vocabulary

```text
SUPPORTS
CHALLENGES
EXTENDS
REPLICATES
CONTRADICTS
ADDRESSES
```

This table is central to traceability.

---

## 22. Generic Research Object Association Persistence

### `research_object_association`

Used only for controlled scientific semantics not covered by richer specialized families.

Candidate fields:

```text
id
source_object_id
target_object_id
semantic_type
rationale
scope_jsonb
origin
review_state
created_at
supersedes_association_id nullable
```

### Important restriction

`semantic_type` must come from a controlled vocabulary, not arbitrary free text.

### Examples

```text
Theory COMPETES_WITH Theory
Mechanism EXPLAINS ScientificRelationship
BoundaryCondition QUALIFIES GapCandidate
```

### Rule

Do not use this table when a specialized family has richer semantics.

---

## 23. Scientific Relationship Persistence

### `scientific_relationship`

Represents the relationship object itself.

Candidate fields:

```text
id PK/FK research_object_identity
relationship_kind
statement
scope_jsonb
```

### `relationship_participant`

Candidate fields:

```text
id
scientific_relationship_id
concept_id
participant_role
ordinal
qualifier_jsonb
```

### Why

This supports:

```text
A → B
A → M → B
A × Z → B
```

without hardcoded `concept_a_id`, `concept_b_id`, `mediator_id`, `moderator_id` columns.

---

## 24. Concept ↔ Measurement Persistence

### `concept_measurement_association`

Candidate fields:

```text
id
concept_id
measurement_id
association_role
context_jsonb
level_of_analysis_id nullable
validity_observations_jsonb
review_state
created_at
```

### Decision

Keep first-class because measurement differences can explain scientific disagreement.

---

## 25. Gap ↔ Solution Persistence

### `gap_solution_association`

Candidate fields:

```text
id
gap_id
solution_id
semantic_type
addressed_aspect
residual_limitation
context_difference
evidence_summary
review_state
origin
created_at
supersedes_association_id nullable
```

Potential semantic types:

```text
POTENTIALLY_ADDRESSES
PARTIALLY_ADDRESSES
STRONGLY_OVERLAPS
CHALLENGES_GAP
LEAVES_RESIDUAL_GAP
```

### Critical UX consequence

This table directly supports:

> Existing Solutions before Novelty.

---

## 26. Existing Solution Underlying References

Because an ExistingSolution may refer to either a Work or another ResearchObjectIdentity, this is one of the few places where a mixed target model is needed.

### Rejected shape

```text
target_type text
target_id uuid
```

with no referential integrity.

### Preferred shape for v0

Use a constrained table with separate nullable FK columns for the small allowed target set, for example:

```text
existing_solution_reference
- id
- existing_solution_id
- work_id nullable
- research_object_id nullable
- reference_role
```

with a constraint that exactly one target is populated.

### Rationale

This preserves real foreign keys while supporting the two required identity families.

### Decision

Prefer small explicit polymorphism over unrestricted generic polymorphic references.

---

## 27. Gap ↔ Contribution Persistence

### `gap_contribution_association`

Candidate fields:

```text
id
gap_id
contribution_id
semantic_type
rationale
scope_jsonb
review_state
created_at
```

This is many-to-many and project-scoped in meaning.

---

## 28. Contribution Association Persistence

### `contribution_association`

Candidate fields:

```text
id
contribution_id
target_research_object_id
semantic_type
rationale
created_at
```

Semantic examples:

```text
EXTENDS
INTEGRATES
CLARIFIES
REFINES
INTRODUCES_BOUNDARY
IMPROVES
```

Validation should later restrict valid target object categories per semantic type.

---

## 29. Synthesis Persistence

### `synthesis`

A current interpretive research object.

### `synthesis_membership`

Candidate fields:

```text
id
synthesis_id
claim_id
membership_role
rationale
inclusion_state
review_state
created_at
supersedes_membership_id nullable
```

Membership roles:

```text
SUPPORTING
CHALLENGING
CONTRADICTORY
BOUNDARY
UNRESOLVED
CONTEXTUAL
```

### Critical rule

A Synthesis is not a JSON array of Claim IDs.

Membership is scientifically meaningful and must be queryable/history-aware.

---

## 30. Assessment Persistence

Assessment must remain separate from research object current state.

### `assessment`

Candidate fields:

```text
id
project_id
target_research_object_id
assessment_type
assessment_version
model_or_rule_version
coverage_context_id
created_at
supersedes_assessment_id nullable
```

### `assessment_dimension`

Candidate fields:

```text
id
assessment_id
dimension_key
numeric_value nullable
categorical_value nullable
explanation
```

Possible dimensions:

- Gap Evidence Strength
- Novelty Potential
- Counter-Evidence Risk
- Theoretical Significance
- Methodological Feasibility
- RQ–Theory–Method Alignment
- Review Priority

### Why separate dimensions?

Avoid a rigid wide assessment table whose columns must change whenever advice dimensions evolve.

This is a controlled key/value structure, not generic EAV for the whole domain.

### Decision

A scoped dimension table is acceptable because the semantic universe is explicitly limited to one Assessment.

---

## 31. Assessment Reason Persistence

### `assessment_reason`

Candidate fields:

```text
id
assessment_dimension_id
claim_id nullable
research_object_id nullable
change_event_id nullable
reason_type
rationale
polarity
```

### Constraint

The allowed reason target categories should be explicit and limited.

### Purpose

Enables UI navigation:

```text
Novelty Potential 52
    ↓ Why?
Existing Solution SOL-008
    ↓
Claim CLM-142
    ↓
Evidence Fragment
```

---

## 32. ChangeEvent Persistence

### `change_event`

Candidate fields:

```text
id
project_id
primary_research_object_id
change_type
occurred_at
previous_state_jsonb
current_state_jsonb
reasoning_delta
coverage_context_id
attention_state
created_at
```

### JSONB decision

`previous_state_jsonb` and `current_state_jsonb` may be appropriate snapshot fields because different object types have different state shapes.

However, they do not replace canonical typed object/assessment records.

They are historical snapshots/explanations.

### Rule

A ChangeEvent represents meaningful reasoning change, not every crawler action.

---

## 33. ChangeEvent Evidence Persistence

### `change_event_evidence`

Candidate fields:

```text
id
change_event_id
claim_id nullable
evidence_relationship_id nullable
research_object_id nullable
role
```

### Purpose

Capture what caused the change without embedding an opaque list in JSON.

Examples:

- newly added claim;
- discovered solution;
- changed evidence relationship;
- coverage change.

---

## 34. HumanDecision Persistence

### `human_decision`

Candidate fields:

```text
id
project_id
primary_research_object_id
decision_type
rationale
actor_id / actor_reference
decided_at
coverage_context_id
assessment_id nullable
supersedes_decision_id nullable
```

Primary v0 decisions:

```text
REVIEW
MODIFY
ACCEPT_DIRECTION
REJECT_CANDIDATE
NEED_MORE_EVIDENCE
```

### Critical rule

A machine assessment update never updates this row in place to another decision.

A later HUMAN judgment creates a new decision row that may supersede the earlier decision.

---

## 35. Human Decision Context

HumanDecision may need to preserve more context than one target object.

### `human_decision_context`

Candidate fields:

```text
id
human_decision_id
research_object_id nullable
claim_id nullable
context_role
```

Examples of roles:

```text
AFFECTED_OBJECT
COUNTER_EVIDENCE
SUPPORTING_OBJECT
ALTERNATIVE
```

This avoids stuffing important scientific context into a JSON blob.

---

## 36. RStage Definition Persistence

### `rstage_definition`

Seeded canonical reference data:

```text
id / stage_code
ordinal
name
description
```

Exactly 17 canonical definitions:

`R0` through `R16`.

This table should not be duplicated per project.

---

## 37. RStage State Persistence

### `rstage_state`

Candidate fields:

```text
id
project_id
rstage_definition_id
status
why_summary
risk_summary
learning_summary
current_version_no
updated_at
```

Constraint:

```text
unique(project_id, rstage_definition_id)
```

### Important nuance

The current state can be one row per stage/project, but temporal history must be preserved elsewhere or through version records.

Two viable later options:

1. `rstage_state` current + `rstage_state_history`; or
2. append-only `rstage_state_version` with a current pointer.

### J2 preference

Favor explicit version/history rather than destructive overwrites.

Exact implementation deferred to schema review/migration design.

---

## 38. RStage Impact Persistence

### `rstage_impact`

Candidate fields:

```text
id
project_id
rstage_state_id
change_event_id nullable
research_object_id nullable
assessment_id nullable
impact_type
reason
attention_priority
created_at
```

### Rule

RStageImpact never automatically enforces stage transitions.

It is an attention/reasoning association only.

---

## 39. Coverage Context Persistence

Coverage must be snapshot-able because assessments and decisions need historical context.

### `coverage_context`

Candidate fields:

```text
id
profile_id nullable
project_id nullable
captured_at
corpus_work_count
full_text_count
abstract_only_count
metadata_only_count
query_coverage_summary_jsonb
freshness_summary_jsonb
notes
```

### `coverage_source_state`

Candidate fields:

```text
id
coverage_context_id
literature_source_id
health_state
search_state
last_success_at
coverage_effect
```

### Why separate source rows?

So the system can reconstruct:

> Which source was degraded when this Assessment/HumanDecision was made?

without embedding provider state only in a snapshot JSON document.

---

## 40. Source Health Persistence

Operational health is temporal.

A later table may use:

### `source_health_event`

```text
id
literature_source_id
health_state
observed_at
reason_code
detail_jsonb
```

### Important rule

Health history does not itself alter scientific object state.

It may create or alter CoverageContext and may trigger a ChangeEvent only when the scientific coverage implication is meaningful.

---

## 41. Quarantine Persistence

J2 should avoid one universal blocking flag controlling whole pipelines.

### Recommended v0 strategy

Objects that can be locally quarantined receive local state fields where natural:

- EvidenceFragment;
- Claim;
- EvidenceRelationship;
- SourceRecord/extraction artifact where needed.

A later generic `quarantine_event` table may preserve reasons/history.

### Principle

```text
quarantine scope = smallest affected object
```

No global `research_locked = true` field belongs in the new schema.

---

## 42. JSONB Policy

JSONB is useful but must be disciplined.

### Appropriate JSONB uses

- raw provider metadata;
- Profile/Project flexible configuration;
- source locator structures;
- bounded contextual qualifiers;
- ChangeEvent before/after snapshots;
- operational details whose schema legitimately varies.

### Inappropriate JSONB uses

Do not hide these inside JSON only:

- Work identity;
- EvidenceFragment provenance;
- Claim provenance;
- EvidenceRelationship;
- Gap–Solution relationships;
- HumanDecision;
- RStage impact;
- Synthesis membership;
- core assessment dimensions/reasons if they need querying/navigation;
- source health snapshot per provider when historical comparison matters.

### Rule

> **If HUMAN must navigate, audit, compare, version, or query a relationship scientifically, it should usually be relationally explicit.**

---

## 43. Enum vs Lookup Table Policy

Not all vocabularies should become PostgreSQL enums.

### Stable vocabularies suitable for strong constraints

Potential candidates:

- evidence access level;
- primary HUMAN decision vocabulary;
- R-stage status;
- source health state;
- gap evolution state.

### Evolving vocabularies better as lookup/reference tables or constrained text

Potential candidates:

- association semantic types;
- contribution types;
- method categories;
- participant roles;
- assessment dimensions.

### Why

PostgreSQL enums are strong but cumbersome when semantics evolve frequently.

### Decision

Use hard enums only for truly stable constitutional vocabulary.

---

## 44. Append-Oriented History Policy

Scientific history should generally be append-oriented.

Examples:

```text
Assessment v1 → Assessment v2
HumanDecision HD-1 → superseded by HD-2
EvidenceRelationship v1 → revised relation v2
GapSolutionAssociation interpretation v1 → v2
```

### Rule

Avoid silent in-place mutation of historically important interpretation.

Not every typo correction needs a new scientific version; implementation may distinguish administrative corrections from meaning-changing revisions.

---

## 45. Current-State Convenience

The UI needs fast access to current state.

Append-oriented history should not force expensive reconstruction on every page load.

### Future implementation options

- `current_*_id` pointer on parent objects;
- current-state materialized views;
- partial indexes on non-superseded records;
- denormalized read models later.

### Decision

Canonical history remains primary; optimized current-state projections may be introduced later.

Do not make a denormalized dashboard table the canonical source of truth.

---

## 46. Referential Integrity Policy

Strong foreign keys are desirable wherever object families are known.

Examples:

```text
claim.evidence_fragment_id → evidence_fragment.id
source_record.literature_source_id → literature_source.id
gap_solution_association.gap_id → gap_candidate.id
human_decision.primary_research_object_id → research_object_identity.id
```

### Avoid

```text
target_type text
target_id uuid
```

unless the allowed target family is genuinely small and constrained by an explicit pattern.

### Decision

Prefer real FKs over polymorphic convenience.

---

## 47. Unique Constraint Policy

Potential high-value uniqueness constraints include:

```text
work_identifier(identifier_type, normalized_identifier_value)
rstage_state(project_id, rstage_definition_id)
source_record(literature_source_id, source_record_identifier)
```

Many scientific associations should **not** be globally unique simply by endpoint pair, because different semantic versions/context may legitimately coexist.

Example:

Two EvidenceRelationships between the same Claim and Gap may differ across interpretation versions or relation type.

---

## 48. Indexing Direction

J2 does not specify final indexes but identifies important access paths.

Likely high-value index families:

- identifiers/DOIs → Work;
- project → Work relevance;
- Work → EvidenceFragments;
- EvidenceFragment → Claims;
- Claim → EvidenceRelationships;
- target ResearchObject → EvidenceRelationships;
- Project → GapCandidates;
- GapCandidate → GapSolutionAssociations;
- ResearchObject → Assessments;
- ResearchObject → ChangeEvents;
- ResearchObject → HumanDecisions;
- Project/RStage → RStageImpact;
- captured_at/observed_at for temporal screens;
- source + health state for Coverage & Health.

Full-text/vector indexes are explicitly outside this persistence-shape decision.

---

## 49. Search / Embedding Boundary

J2 persistence should not make embeddings canonical scientific state.

A future search layer may attach:

- embeddings to Work;
- EvidenceFragment;
- Claim;
- Synthesis;
- ResearchObjectIdentity.

But vector representations are derived indexes.

### Rule

> **Embedding similarity is discovery/retrieval infrastructure, not evidence provenance.**

No scientific claim becomes evidence-backed because two vectors are close.

---

## 50. Graph Projection Boundary

The relational schema can later produce a graph projection such as:

```text
Claim → EvidenceRelationship → Gap
Gap → GapSolutionAssociation → ExistingSolution
Gap → GapContributionAssociation → Contribution
Contribution → Theory
ChangeEvent → RStageImpact → RStage
```

A graph database is not required as canonical storage for v0.

### Decision

PostgreSQL remains canonical. Graph views/exports may be derived later if useful.

---

## 51. Profile A Persistence Walkthrough

Illustrative path:

```text
research_profile
Profile A — Computer / Information Systems

research_project
Cross-agency Digital Government Governance

work
Prior EA capability paper

source_record
OpenAlex record + Crossref record

project_work_relevance
Relevant to active project

evidence_fragment
Full-text passage

claim
Prior EA capability mechanism addresses part of cross-agency governance issue

evidence_relationship
CLM-142 ADDRESSES GAP-014

gap_candidate
GAP-014

gap_solution_association
SOL-008 PARTIALLY_ADDRESSES GAP-014

assessment
Novelty Potential 81 → 52

change_event
Gap STRENGTHENING → CONTESTED

rstage_impact
R5 / R11 / R12 need attention

human_decision
Existing ACCEPT_DIRECTION remains until HUMAN acts
```

No Profile-A-specific table is required.

---

## 52. Profile B Persistence Walkthrough

Illustrative path:

```text
research_profile
Profile B — Management / Organization Studies

research_project
Human Capability & Organizational Resilience

work
Prior organizational-behaviour paper

source_record
OpenAlex record + Crossref record

project_work_relevance
Relevant to active project

evidence_fragment
Abstract/full-text fragment

claim
Established behavioural construct explains part of resilience mechanism

evidence_relationship
CLM-142 CHALLENGES GAP-014

gap_candidate
GAP-014

gap_solution_association
SOL-009 STRONGLY_OVERLAPS GAP-014

assessment
Novelty Potential decreases

change_event
Gap STRENGTHENING → CONTESTED

rstage_impact
R5 / R6 / R8 / R11 / R12 need attention

human_decision
Previous judgment remains historical until HUMAN changes it
```

The persistence shape is identical.

---

## 53. Generality Review

| Persistence Concern | Profile A | Profile B | Decision |
|---|---|---|---|
| Profile/Project | same tables | same tables | generic |
| Work/SourceRecord | same | same | generic |
| EvidenceFragment/Claim | same | same | generic |
| Concept/Theory/Method | same typed object family | same | generic |
| Mediator/Moderator | relationship participant role | relationship participant role | generic |
| Gap/Solution | same tables | same tables | generic |
| Assessment | same | same | generic |
| ChangeEvent | same | same | generic |
| HumanDecision | same | same | generic |
| R0–R16 | same reference definitions | same | generic |
| Coverage | same | same | generic |

No domain-specific database schema is required for the two reference profiles.

If a future domain needs a genuinely specialized persistence object, apply ADR-001:

`PROFILE_CONFIG | CORE_GENERALIZATION | ADD_IN_CANDIDATE | UNRESOLVED_GENERALITY`

and do not globally stop the project.

---

## 54. MVP Persistence Subset

The full durable shape does not need to be implemented at once.

A smallest useful vertical slice can begin with:

```text
research_profile
research_profile_version
research_project
research_project_version
literature_source
source_record
work
work_identifier
work_source_record
project_work_relevance
evidence_fragment
claim
research_object_identity
gap_candidate
evidence_relationship
assessment
assessment_dimension
change_event
rstage_definition
rstage_state
rstage_impact
coverage_context
coverage_source_state
human_decision
```

Then add:

```text
concept / theory / method / measurement
existing_solution
gap_solution_association
candidate_contribution
gap_contribution_association
synthesis / synthesis_membership
assessment_reason
human_decision_context
```

as the research-intelligence slice becomes richer.

### Principle

> Implement tables when they enable a validated UX decision/evidence trace, not merely because they appear in the conceptual model.

---

## 55. Mapping to Incremental UI Activation

This persistence plan aligns with gradual replacement of dummy UI.

### Step 1 — Real Profile / Project

Tables:

```text
research_profile
research_profile_version
research_project
research_project_version
```

UI enabled:

- Profile selector;
- Project selector;
- profile/project configuration.

### Step 2 — Real Literature

Tables:

```text
literature_source
source_record
work
work_identifier
project_work_relevance
```

UI enabled:

- recent papers;
- corpus counts;
- source provenance.

### Step 3 — Real Evidence

Tables:

```text
evidence_fragment
claim
```

UI enabled:

- Evidence Explorer basic trace.

### Step 4 — Real Scientific Reasoning

Tables:

```text
research_object_identity
gap_candidate
evidence_relationship
```

UI enabled:

- gap candidate;
- supporting/challenging evidence;
- Opportunity Board baseline.

### Step 5 — Real Change Intelligence

Tables:

```text
assessment
assessment_dimension
change_event
rstage_state
rstage_impact
coverage_context
```

UI enabled:

- Today / What Changed?;
- Knowledge Evolution;
- R0–R16 attention.

### Step 6 — Real HUMAN Authority

Tables:

```text
human_decision
```

UI enabled:

- Human Review;
- decision history.

### Step 7 — Rich Opportunity Reasoning

Tables:

```text
existing_solution
gap_solution_association
candidate_contribution
synthesis
```

UI enabled:

- full Gap–Solution Workspace;
- Novelty Challenge;
- richer Telegram Radar.

---

## 56. Migration from Legacy Database — Shape Principle

The old PostgreSQL database should not be forced directly into this shape in one big-bang migration.

Preferred strategy:

```text
Legacy tables remain read-only/auditable
        ↓
New v0 research-intelligence schema created alongside
        ↓
Selected durable assets mapped/imported incrementally
        ↓
New UI reads new canonical model as data becomes available
```

Prioritize migration of:

- normalized paper identity;
- DOI/source records;
- raw artifact/provenance references;
- search manifests where useful;
- evidence fragments/claims that can be validated;
- HUMAN decisions worth preserving.

Do not migrate old global gates merely because they exist.

---

## 57. Rejected Persistence Shapes

### A. Universal JSON object table

Rejected because it weakens structural invariants and queryability.

### B. Universal triple/edge table as canonical model

Rejected because scientific association families carry different required semantics.

### C. Domain-specific schemas

Rejected for normal onboarding.

Examples not allowed as core strategy:

```text
management_gap
it_governance_gap
management_method
enterprise_architecture_method
```

### D. One project_id column on Work

Rejected because Works are reusable across Projects.

### E. One mutable assessment row per object

Rejected because historical assessment evolution is essential.

### F. HumanDecision field embedded in GapCandidate

Rejected because HUMAN decisions need rationale, temporal context, supersession, and evidence snapshots.

### G. One global pipeline status / research lock row

Rejected because local failure semantics are constitutional.

---

## 58. J2 Persistence Integrity Invariants

The eventual schema should preserve at least these invariants:

1. Every SourceRecord has exactly one LiteratureSource.
2. Every atomic Claim has exactly one primary EvidenceFragment.
3. Every EvidenceFragment belongs to exactly one Work.
4. Metadata-only Work may exist without EvidenceFragment.
5. Every EvidenceRelationship has exactly one Claim and one ResearchObject target.
6. HumanDecision is separate from machine Assessment.
7. Historical Assessments are preserved.
8. Historical HumanDecisions are preserved.
9. Coverage context can be attached to Assessment/Decision/ChangeEvent.
10. RStageImpact cannot act as a database workflow gate.
11. ProjectWorkRelevance supports many Projects per Work.
12. Research object types remain domain-agnostic.
13. Existing Solutions precede novelty interpretation in the data path.
14. Quarantine is local.
15. No source outage invalidates unrelated valid evidence rows.

---

## 59. J2 Acceptance Criteria

This PostgreSQL persistence shape is acceptable when it can support the following without domain-specific branching:

1. Trace a candidate gap to Claim → EvidenceFragment → Work → SourceRecord → LiteratureSource.
2. Retain contradictory evidence simultaneously.
3. Represent one Work in multiple Projects with different relevance.
4. Represent Profile A and Profile B with the same tables.
5. Preserve machine Assessment history separately from HUMAN decisions.
6. Preserve CoverageContext at the time of assessment/decision.
7. Support gap → existing solution → residual limitation reasoning.
8. Support R0–R16 impacts without gates.
9. Support Today / Knowledge Evolution from versioned changes.
10. Support Telegram as a projection, not canonical state.
11. Allow partial implementation so UI can move from dummy to real data incrementally.
12. Avoid universal EAV/graph ambiguity.
13. Avoid uncontrolled table proliferation.
14. Preserve local quarantine/failure semantics.

### Review result

**ACCEPTED AS J2 PERSISTENCE SHAPE BASELINE.**

This is not yet approval of final SQL DDL.

---

## 60. Not Building Yet

This review intentionally does not define:

- final schema name;
- production SQL migrations;
- exact column types for every field;
- every constraint/trigger;
- partitioning;
- vector extension/pgvector;
- full-text indexes;
- event sourcing framework;
- ORM choice;
- API endpoints;
- queue/job tables;
- authentication/user schema;
- multi-researcher conflict resolution;
- archival/retention policy;
- rights-management implementation.

These should be decided only when needed by the next vertical slice.

---

## 61. Recommended Next J2 Step

The next step should be:

> **J2 Minimum Canonical Schema / Vertical Slice Review v0**

Its goal is not to implement the entire durable model. It should select the smallest subset of tables needed to produce one real end-to-end path:

```text
Profile / Project
→ Work
→ EvidenceFragment
→ Claim
→ GapCandidate
→ EvidenceRelationship
→ Assessment
→ ChangeEvent
→ RStageImpact
→ HumanDecision
→ Dashboard / Telegram projection
```

This would convert the accepted persistence shape into a migration-ready minimal schema while preserving room for Theory, Method, ExistingSolution, Synthesis, and richer associations in subsequent increments.

---

## 62. Pinned Persistence Principle Candidate

> **PostgreSQL is the canonical evidence and research-state store: provenance is strongly typed, scientific objects have stable generic identity plus typed content, meaningful relationships are explicit, history is append-oriented, coverage is preserved as context, and HUMAN judgment is never collapsed into machine state.**
