# J2 Minimum Canonical Schema / Vertical Slice Review v0

Status: **J2 ACTIVE — Minimum Canonical Schema / Vertical Slice Review**

## 1. Purpose

This review selects the **minimum canonical PostgreSQL schema** needed to support one real end-to-end research-intelligence flow without prematurely implementing the full J2 object model.

The goal is not to build every object, association, score, research stage feature, source connector, or UI screen at once. The goal is to prove that GFPROJCLAW can move a small amount of real literature through a traceable path into the Research Cockpit while preserving the project constitution.

The governing principle is:

> **Build the smallest canonical slice that can produce real, traceable, change-aware research intelligence for a HUMAN, then extend outward without breaking the evidence chain.**

This document defines the minimum persistence contract for the first working vertical slice. It does **not** yet define production SQL DDL or a complete migration set.

---

## 2. Inputs to This Review

This review is derived from:

- J1 accepted UX and integration review;
- J2 Research Object Model;
- J2 Object Relationship & Cardinality Review;
- J2 Generic Identity & Association Model Review;
- J2 PostgreSQL Persistence Shape Review.

The accepted epistemic trace remains:

```text
Source
  → SourceRecord
  → Work
  → EvidenceFragment
  → Claim
  → EvidenceRelationship
  → ResearchObject
  → Assessment / ChangeEvent
  → HumanDecision
```

with:

```text
ResearchProfile → ResearchProject
```

providing context, and `CoverageContext` explaining what the system did and did not observe.

---

## 3. Vertical Slice Objective

The first canonical slice must be able to demonstrate the following real flow:

```text
ResearchProfile
  ↓
ResearchProject
  ↓
LiteratureSource
  ↓
SourceRecord
  ↓ normalization
Work
  ↓
ProjectWorkRelevance
  ↓
EvidenceFragment
  ↓
Claim
  ↓
EvidenceRelationship
  ↓
GapCandidate
  ↓
Assessment
  ↓
ChangeEvent
  ↓
Research Cockpit: Today / Opportunities / Evidence
  ↓
HumanDecision
```

Coverage context must be inspectable around the same run.

This flow is enough to prove the core promises:

1. literature can enter incrementally;
2. provenance is preserved;
3. claims are traceable to bounded evidence;
4. candidate research opportunities can be related to claims;
5. machine advice remains distinct from HUMAN judgment;
6. meaningful change can be surfaced;
7. coverage limitations can be disclosed;
8. UI can progressively replace dummy data with canonical data.

---

## 4. What the First Slice Is Not

The first slice is **not** intended to implement the complete research knowledge model.

Not required yet:

- every Theory/Method/Concept relationship;
- Model/Framework intelligence;
- Measurement/Operationalization intelligence;
- Mechanism/BoundaryCondition/LevelOfAnalysis persistence;
- full Gap–Solution association family;
- full CandidateContribution model;
- Synthesis engine;
- all R0–R16 persistence detail;
- complete Critic/Falsification engine;
- composite scoring;
- journal positioning;
- adversarial reviewer;
- generalized add-in runtime;
- full operational queue/run schema;
- every Telegram message class.

These remain compatible extension targets, not prerequisites for proving the first slice.

---

## 5. Minimum Canonical Table Set

The recommended **minimum canonical set** is grouped into seven functional clusters.

### A. Research Context

```text
research_profile
research_profile_version
research_project
research_project_version
```

### B. Source & Literature Provenance

```text
literature_source
source_record
work
work_identifier
work_source_record
project_work_relevance
```

### C. Evidence & Claims

```text
evidence_fragment
claim
```

### D. Generic Research Identity + One Opportunity Type

```text
research_object_identity
gap_candidate
```

### E. Evidence Semantics

```text
evidence_relationship
```

### F. Advice, Change & HUMAN Authority

```text
assessment
assessment_dimension
change_event
human_decision
```

### G. Coverage

```text
coverage_context
coverage_source_state
```

This produces a minimum set of **20 canonical tables**.

The number 20 is not a target in itself. It is the smallest set found that preserves the accepted scientific semantics without collapsing critical concepts into JSON or overloaded generic tables.

---

## 6. Why Each Minimum Table Is Needed

### `research_profile`

Stable identity for configurable research-domain context.

Without it, the system would begin hardcoding domain assumptions.

### `research_profile_version`

Preserves the search/terminology/configuration context under which literature was discovered and assessments were generated.

### `research_project`

Represents one HUMAN research effort.

Gap candidates, decisions, and interpretation belong primarily here.

### `research_project_version`

Preserves changing intent, provisional RQs, and project configuration without overwriting historical context.

### `literature_source`

Represents provider identity independently from scholarly Work identity.

### `source_record`

Preserves exactly what a provider returned, including retrieval provenance and raw metadata.

### `work`

Canonical normalized scholarly item.

### `work_identifier`

Supports DOI and other identifiers without making one identifier universal.

### `work_source_record`

Preserves many-provider-to-one-Work normalization lineage.

### `project_work_relevance`

Prevents globally normalized Works from becoming project-specific copies.

### `evidence_fragment`

Provides the bounded evidence unit required by the evidence trace.

### `claim`

Provides the atomic scientific proposition extracted from one primary EvidenceFragment.

### `research_object_identity`

Provides stable generic identity for cross-cutting UI, Assessment, ChangeEvent, HumanDecision, and EvidenceRelationship targets.

### `gap_candidate`

Chosen as the first typed scientific object because the first cockpit slice needs a defensible research-opportunity target.

This does **not** mean Gap is more fundamental than Theory/Method/Concept. It is simply the first project-facing object required by the accepted UX.

### `evidence_relationship`

Creates the explicit semantic bridge:

```text
Claim → SUPPORTS / CHALLENGES / CONTRADICTS / ADDRESSES → GapCandidate
```

This table is essential. A direct `gap.paper_ids[]` representation would violate traceability.

### `assessment`

Stores versioned machine advice about the gap candidate.

### `assessment_dimension`

Prevents one opaque score from becoming the canonical assessment.

The first slice may use only a subset such as:

```text
GAP_EVIDENCE_STRENGTH
COUNTER_EVIDENCE_RISK
EVIDENCE_COVERAGE_CONTEXT
REVIEW_PRIORITY
```

### `change_event`

Stores meaningful scientific or coverage change rather than raw crawler activity.

### `human_decision`

Stores HUMAN scientific authority separately from machine state.

### `coverage_context`

Records the bounded observation context for discovery/assessment/change.

### `coverage_source_state`

Explains source-level availability/degradation within a coverage snapshot.

---

## 7. Minimum Table Dependencies

The canonical dependency shape is:

```text
research_profile
    ↓
research_profile_version
    ↓
research_project
    ↓
research_project_version

literature_source
    ↓
source_record ───────────────┐
                            ↓
work_source_record → work → work_identifier
                         ↓
               project_work_relevance
                         ↓
                 evidence_fragment
                         ↓
                       claim
                         ↓
              evidence_relationship
                         ↓
            research_object_identity
                         ↓
                   gap_candidate
                         ↓
                    assessment
                         ↓
               assessment_dimension
                         ↓
                   change_event
                         ↓
                  human_decision

coverage_context
    ↓
coverage_source_state

assessment / change_event / human_decision
    → coverage_context where relevant
```

This is a reasoning dependency map, not necessarily migration ordering in every detail.

---

## 8. Minimum Research Object Scope

For the first slice, `research_object_identity.object_type` only needs to support:

```text
GAP_CANDIDATE
```

However, the schema must be intentionally extensible to later support:

```text
CONCEPT
DEFINITION
SCIENTIFIC_RELATIONSHIP
MECHANISM
BOUNDARY_CONDITION
LEVEL_OF_ANALYSIS
THEORY
MODEL_FRAMEWORK
METHOD
MEASUREMENT
EXISTING_SOLUTION
ALTERNATIVE
CANDIDATE_CONTRIBUTION
SYNTHESIS
```

### Important rule

Do not build domain-specific object tables simply because only GapCandidate exists in the first slice.

The identity mechanism must already reflect the accepted generic architecture.

---

## 9. Minimum GapCandidate Shape

A first-slice `gap_candidate` needs only the fields necessary to drive the Opportunity Board and Gap workspace.

Conceptually:

```text
gap_candidate
- id PK/FK → research_object_identity
- project_id
- gap_type
- statement
- scope_jsonb
- current_evolution_state
- created_at
```

Canonical gap types:

```text
EXPLICIT_GAP
EMPIRICAL_GAP
THEORETICAL_GAP
SYNTHESIS_GAP
```

Canonical machine evidence-dynamics states:

```text
CANDIDATE
STRENGTHENING
WEAKENING
CONTESTED
POSSIBLY_CLOSED
REOPENED
```

### Rule

`current_evolution_state` is a machine/evidence interpretation state, **not** HUMAN acceptance.

---

## 10. Minimum Claim & Evidence Integrity

The first migration must preserve these invariants conceptually:

```text
EvidenceFragment belongs to exactly one Work.
Claim belongs to exactly one primary EvidenceFragment.
EvidenceRelationship belongs to exactly one Claim.
EvidenceRelationship targets exactly one ResearchObjectIdentity.
```

This gives the core trace:

```text
GapCandidate
    ↑
EvidenceRelationship
    ↑
Claim
    ↑
EvidenceFragment
    ↑
Work
    ↑
SourceRecord
    ↑
LiteratureSource
```

### Acceptance rule

If any evidence-backed Gap assertion cannot traverse this path, it must not be treated as canonical evidence-backed knowledge.

---

## 11. Minimum EvidenceRelationship Vocabulary

For the first slice, use the already accepted vocabulary:

```text
SUPPORTS
CHALLENGES
EXTENDS
REPLICATES
CONTRADICTS
ADDRESSES
```

Not all values need to be generated immediately.

For GapCandidate specifically, the first real pipeline may primarily produce:

```text
SUPPORTS
CHALLENGES
CONTRADICTS
ADDRESSES
```

### Rule

Do not create a special `gap_evidence` table with a separate semantic system.

Gap evidence must use the same EvidenceRelationship mechanism that later serves Theory, Method, Contribution, and other research objects.

---

## 12. Minimum Assessment Contract

The first slice should avoid a single composite score.

`assessment` stores:

- target GapCandidate;
- project/context;
- assessment timestamp;
- model/agent/version identity where relevant;
- explanation summary;
- coverage context;
- supersession/version linkage.

`assessment_dimension` stores individual advice dimensions.

Minimum first-slice dimensions:

```text
GAP_EVIDENCE_STRENGTH
COUNTER_EVIDENCE_RISK
EVIDENCE_COVERAGE_CONTEXT
REVIEW_PRIORITY
```

Optional if readily supported:

```text
NOVELTY_POTENTIAL
THEORETICAL_SIGNIFICANCE
METHODOLOGICAL_FEASIBILITY
```

### Rules

- values are advice, not probabilities;
- no threshold determines HumanDecision;
- explanation must remain inspectable;
- historical assessments are preserved;
- re-assessment creates a new version/snapshot rather than rewriting history.

---

## 13. Minimum ChangeEvent Contract

A ChangeEvent should be created only when there is a meaningful delta.

Minimum examples:

```text
new claim materially supports GAP-014
new paper challenges GAP-014
an existing solution appears to address GAP-014
coverage degraded for a source relevant to GAP-014
assessment dimension changed materially after new evidence
```

Do **not** create ChangeEvents for every:

- HTTP request;
- crawler page;
- raw record insertion;
- successful worker job;
- retry;
- metadata refresh.

### Minimum conceptual fields

```text
change_event
- id
- project_id
- primary_research_object_id
- change_type
- observed_at
- previous_state_jsonb nullable
- current_state_jsonb nullable
- reasoning_delta
- coverage_context_id nullable
- created_at
```

Bounded JSONB is acceptable here for state snapshots because the canonical scientific objects and evidence relations remain normalized elsewhere.

---

## 14. Minimum HumanDecision Contract

The first slice must persist HUMAN authority from day one rather than adding it later.

Canonical v0 decision vocabulary:

```text
REVIEW
MODIFY
ACCEPT_DIRECTION
REJECT_CANDIDATE
NEED_MORE_EVIDENCE
```

UI may display `ACCEPT DIRECTION` while persistence uses a safe normalized token such as `ACCEPT_DIRECTION`.

Minimum fields:

```text
human_decision
- id
- project_id
- primary_research_object_id
- decision_type
- rationale
- actor
- decided_at
- assessment_id nullable
- coverage_context_id nullable
- supersedes_decision_id nullable
- created_at
```

### Rules

- new evidence never deletes prior decisions;
- machine assessment cannot overwrite HumanDecision;
- a new decision may supersede an old one while preserving lineage;
- no HumanDecision is required before crawling or unrelated analysis continues.

---

## 15. Minimum Coverage Contract

The first slice must make coverage visible even if coverage measurement is initially coarse.

`coverage_context` should at minimum capture:

```text
- id
- project_id
- profile_version_id
- observed_at
- query/watchlist context
- temporal window
- access summary
- extraction summary
- counter-search state
- notes / limitations
```

`coverage_source_state` should capture:

```text
- coverage_context_id
- literature_source_id
- health_state
- attempted / observed record counts
- access limitations
- degradation reason
```

Initial operational vocabulary:

```text
HEALTHY
DEGRADED
BACKOFF
DISABLED
ATTENTION
```

### Scientific rule

A degraded source modifies the interpretation of coverage. It does **not** automatically invalidate existing evidence or halt other source processing.

---

## 16. Minimum Source Ingestion Contract

The first slice does not need a fully generalized scheduler schema yet.

It must, however, preserve enough information to answer:

- which provider produced this SourceRecord?
- when was it retrieved?
- under which Profile/Project discovery context was it considered?
- how was it normalized to Work?
- what access level was available?

A later `crawl_run`, `source_job`, and `extraction_job` model can be added without changing the scientific evidence chain.

### Decision

Operational run/job tables are **deferred from the canonical first slice**, unless existing legacy assets can be safely adapted with minimal effort.

---

## 17. UI Replacement Sequence

The existing mockup should be converted from dummy data to real canonical data progressively.

Recommended order:

```text
Step 1
Profile selector + Project selector
→ research_profile / research_project

Step 2
Latest Papers / New Papers
→ work + project_work_relevance

Step 3
Evidence Explorer
→ work → evidence_fragment → claim

Step 4
Research Opportunities
→ gap_candidate + evidence_relationship

Step 5
Opportunity dimensions
→ assessment + assessment_dimension

Step 6
Today / What Changed?
→ change_event

Step 7
Human Review actions
→ human_decision

Step 8
Coverage & Health
→ coverage_context + coverage_source_state
```

This allows the cockpit to become real incrementally instead of requiring a big-bang UI rewrite.

---

## 18. Telegram Vertical Slice

Telegram should consume the same canonical state rather than maintain separate research logic.

For the first slice, Telegram only needs to surface bounded messages derived from ChangeEvent, for example:

```text
GAP CHANGE
Project: Organizational Resilience Study

What changed:
New evidence challenges GAP-014.

Why it matters:
The current evidence basis is now contested.

Evidence:
2 new claims from 1 newly discovered Work.

Coverage:
Semantic Scholar degraded; OpenAlex healthy.

Action:
Open Research Cockpit → GAP-014
```

### Rule

Telegram delivery failure is local and does not affect canonical research processing.

---

## 19. First-Slice End-to-End Acceptance Scenario

The vertical slice is accepted when the following scenario works for both reference profiles with the same code path.

### Profile A example

Profile:

`Computer / Information Systems`

Project context may involve:

`IT Governance / Digital Government / Enterprise Architecture`

### Profile B example

Profile:

`Management / Organization Studies`

Project context may involve:

`Organizational Resilience / Human Behaviour / Human Capability`

### Same technical flow

```text
1. HUMAN selects Profile and Project.
2. At least one configured source returns literature records.
3. SourceRecord is persisted with raw provenance.
4. Records normalize to Work.
5. Work is linked to Project through ProjectWorkRelevance.
6. Available abstract/full-text evidence produces EvidenceFragment.
7. At least one atomic Claim is extracted.
8. Claim is linked through EvidenceRelationship to a GapCandidate.
9. Assessment generates separate advice dimensions.
10. New evidence or reassessment generates a ChangeEvent.
11. Today / Opportunities / Evidence screens display the canonical data.
12. HUMAN records a decision and rationale.
13. The HumanDecision remains distinct from machine state.
14. CoverageContext shows what sources/access were actually observed.
15. Failure of another source does not block this healthy flow.
```

### Cross-domain acceptance

No source-code branch may be required of the form:

```text
if domain == "it_governance"
if domain == "management"
```

Differences must come from ResearchProfile / Project configuration or generic object data.

---

## 20. Minimum Test Categories

Before calling the slice durable, at least the following tests should exist.

### A. Provenance integrity

A Claim cannot exist as canonical evidence-backed content without an EvidenceFragment.

### B. Evidence relationship integrity

An EvidenceRelationship must have one Claim and one valid ResearchObject target.

### C. Work normalization integrity

Several SourceRecords may map to one Work without losing source provenance.

### D. Project locality

One Work can belong to several Projects with different relevance state.

### E. HUMAN authority separation

Assessment updates cannot alter HumanDecision rows.

### F. Temporal preservation

New Assessment / ChangeEvent does not overwrite previous history.

### G. Coverage degradation

A degraded source changes CoverageContext but does not stop healthy sources.

### H. Cross-domain fixture

The same schema and service functions work for Profile A and Profile B.

---

## 21. Deferred Tables After First Slice

The following tables are intentionally deferred but already have a place in the accepted J2 model:

```text
watchlist
concept
definition
theory
model_framework
method
measurement
scientific_relationship
relationship_participant
mechanism
boundary_condition
level_of_analysis
existing_solution
alternative
candidate_contribution
synthesis
research_object_association
concept_measurement_association
gap_solution_association
gap_contribution_association
contribution_association
existing_solution_reference
synthesis_membership
assessment_reason
change_event_evidence
rstage_definition
rstage_state
rstage_impact
source_health_event
crawl_run
source_job
extraction_job
quarantine_event
```

Deferred does not mean rejected.

They should be added when a concrete Dashboard decision, Telegram signal, evidence trace, research action, scientific integrity requirement, or operational need demands them.

---

## 22. Existing Solution Before Novelty — Vertical Slice Implication

The accepted UX requires:

> **Existing Solutions must be examined before Novelty.**

The minimum schema does not yet require `existing_solution` and `gap_solution_association` tables because the first goal is proving provenance-to-gap-to-change-to-human-decision.

However, this is a deliberate short-lived deferral.

### Required follow-up

Once the first GapCandidate flow is working, the **next scientific expansion** should add:

```text
existing_solution
gap_solution_association
```

before implementing a mature Novelty Potential workflow.

### Rule

Do not ship a prominent novelty recommendation feature on top of the minimum slice without first implementing Existing Solution reasoning.

---

## 23. R0–R16 Implication

The first canonical slice does not require the full RStage persistence model to prove evidence traceability.

The UI can initially display the accepted R0–R16 structure as static definitions while canonical scientific data begins populating Evidence, Opportunity, Change, and Human Review.

The next persistence expansion should add:

```text
rstage_definition
rstage_state
rstage_impact
```

when the system is ready to persist project-specific reasoning maturity and change impacts.

### Rule

Do not replace R0–R16 with a project progress percentage while persistence is incomplete.

The canonical statuses remain:

```text
NOT STARTED
DEVELOPING
EVIDENCE GROWING
NEEDS ATTENTION
HUMAN REVIEWED
MATURE
```

---

## 24. Migration Strategy from Legacy System

The first slice should be introduced **alongside** the legacy schema rather than rewriting legacy tables in place.

Recommended approach:

```text
legacy schema/data
    ↓ read-only / audit / selective adaptation
new canonical research-intelligence schema
    ↓
new services / pipeline
    ↓
new Research Cockpit
```

### Reuse candidates

Legacy assets may be adapted if they already provide:

- normalized DOI/source identifiers;
- raw source metadata;
- provenance hashes;
- search manifests;
- bounded evidence artifacts;
- Telegram delivery components.

### Do not migrate blindly

Do not carry forward:

- global gate states;
- global PASS/FAIL semantics;
- engineering authorization gates;
- source-wide blocking semantics;
- score thresholds that decide scientific acceptance;
- frozen global knowledge state.

---

## 25. Vertical Slice Service Boundary

A useful first application/service shape is:

```text
Profile / Project Service
        ↓
Discovery Adapter
        ↓
Normalization Service
        ↓
Evidence Extraction Service
        ↓
Claim / Evidence Relationship Service
        ↓
Gap Candidate Service
        ↓
Assessment / Change Detection Service
        ↓
Cockpit Read Model
        ↓
Human Decision Service
        ↓
Telegram Projection
```

These are logical boundaries, not necessarily separate processes or microservices.

### Rule

Do not create microservices merely because the logical boundaries exist.

A modular monolith is acceptable and likely preferable for Version 0.

---

## 26. Read Models for the Existing UI

The first slice should avoid making the UI reconstruct complex scientific relationships from raw tables.

Recommended read-model/query shapes:

```text
cockpit_today_changes
cockpit_recent_works
cockpit_gap_candidates
cockpit_gap_detail
cockpit_evidence_trace
cockpit_human_review
cockpit_coverage_summary
```

These may initially be:

- SQL views;
- service queries;
- repository-layer projections.

They should not become a second source of truth.

### Principle

> PostgreSQL canonical tables store scientific state; cockpit read models project that state for HUMAN reasoning.

---

## 27. Local Failure Semantics in the Slice

The first implementation must already obey the non-global-lock principle.

Examples:

```text
Source A fails
→ CoverageContext records degradation
→ Source B continues

One SourceRecord cannot normalize
→ record remains unresolved/quarantined
→ other Works continue

One EvidenceFragment fails extraction
→ that fragment/item is contained locally
→ other evidence continues

One Claim lacks defensible provenance
→ Claim quarantined/not promoted
→ unrelated Claims continue

Assessment fails for GAP-014
→ GAP-014 assessment unavailable/stale
→ ingestion and other gaps continue

Telegram fails
→ canonical ChangeEvent remains available in Dashboard
```

### Acceptance rule

No vertical-slice component may depend on a global “all sources/all jobs/all analyses PASS” condition.

---

## 28. Data Volume Philosophy for the First Slice

The first working slice should prefer a **small real corpus with excellent traceability** over a large corpus with ambiguous provenance.

Suggested initial scale:

- a small number of configured source queries;
- dozens rather than thousands of Works;
- enough EvidenceFragments and Claims to test contradictions;
- a handful of GapCandidates;
- several ChangeEvents over multiple runs;
- actual HumanDecision records.

The exact counts are not acceptance thresholds.

The acceptance criterion is the quality of the end-to-end evidence chain and update behavior.

---

## 29. Generality Review

### Profile A

The slice supports:

- digital governance / EA / IT governance Works;
- extracted claims;
- candidate empirical/theoretical/synthesis gaps;
- evidence support/challenge;
- machine advice;
- HUMAN decisions.

### Profile B

The same slice supports:

- organizational resilience / behaviour / capability Works;
- extracted claims;
- candidate empirical/theoretical/synthesis gaps;
- evidence support/challenge;
- machine advice;
- HUMAN decisions.

### Result

No schema difference is required.

If a later domain need cannot be represented, classify it as:

```text
PROFILE_CONFIG
CORE_GENERALIZATION
ADD_IN_CANDIDATE
UNRESOLVED_GENERALITY
```

and continue the project while addressing it.

---

## 30. Risks and Controls

### Risk: Gap becomes the whole system too early

Control:

Treat GapCandidate as only the **first typed research object** in the vertical slice. Preserve generic identity so Theory/Method/Concept/Contribution can be added naturally.

### Risk: JSONB becomes a shortcut around modeling

Control:

Use JSONB only for raw metadata, configuration, scope/locator, and bounded state snapshots. Do not hide Claim, EvidenceRelationship, HumanDecision, or key scientific associations inside JSONB.

### Risk: UI starts treating scores as truth

Control:

Expose assessment dimensions with explanation and evidence trace. No global composite requirement.

### Risk: novelty appears before existing solutions

Control:

Do not promote mature Novelty Potential until ExistingSolution + GapSolutionAssociation are implemented.

### Risk: source failures become global failures

Control:

CoverageContext and local failure state absorb degradation while unrelated work continues.

### Risk: first schema becomes permanent by accident

Control:

Keep the J2 full object model as the architectural envelope and explicitly document deferred tables.

---

## 31. Acceptance Criteria for This Review

The Minimum Canonical Schema / Vertical Slice Review is accepted when the team agrees that:

1. the minimum tables preserve the evidence chain;
2. the slice can populate meaningful parts of the accepted UI with real data;
3. HumanDecision is persisted from the first working version;
4. CoverageContext is persisted from the first working version;
5. Assessment remains advice rather than verdict;
6. ChangeEvent represents meaningful change, not raw crawler activity;
7. Work normalization preserves multi-source provenance;
8. source failure is local and non-blocking;
9. the same schema supports Profile A and B;
10. deferred objects have explicit extension points;
11. Existing Solution reasoning is scheduled before mature novelty logic;
12. no J0/J1 principle is weakened for implementation convenience.

---

## 32. Review Result

**ACCEPTED as J2 baseline for the first implementable canonical vertical slice.**

The first slice will implement the minimum canonical chain:

```text
Profile / Project
→ SourceRecord / Work
→ EvidenceFragment / Claim
→ EvidenceRelationship
→ GapCandidate
→ Assessment
→ ChangeEvent
→ HumanDecision
→ CoverageContext
→ Research Cockpit / Telegram projection
```

This is deliberately narrow enough to implement and broad enough to prove the architecture.

---

## 33. J2 Checkpoint

Current J2 state:

```text
Research Object Model                         ACTIVE
Object Relationship & Cardinality Review      ACCEPTED
Generic Identity & Association Model Review   ACCEPTED
PostgreSQL Persistence Shape Review            ACCEPTED
Minimum Canonical Schema / Vertical Slice     ACCEPTED
```

The next appropriate J2 step is:

> **J2 Canonical DDL Contract Review v0**

That step should turn this accepted persistence slice into a concrete schema contract: table names, columns, types, foreign keys, check constraints, unique constraints, indexes, versioning rules, deletion rules, and migration boundaries — still reviewed before applying anything to the server.
