# J2 Generic Identity & Association Model Review v0

Status: **J2 ACTIVE — Generic Identity & Association Review**

## 1. Purpose

This review decides how GFPROJCLAW should represent reusable research objects and typed relationships **without** falling into either of two architectural extremes:

1. a rigid design with dozens of bespoke pairwise link structures that become difficult to extend across domains; or
2. an unconstrained universal graph/EAV model where everything can link to everything and scientific semantics become opaque.

The review is derived from the accepted J1 UX, the J2 Research Object Model, and the accepted Object Relationship & Cardinality Review.

The governing principle is:

> **Use generic identity where cross-cutting behavior is genuinely shared, and typed associations where scientific meaning, provenance, validation, or history matters.**

The goal is not maximum genericity. The goal is **disciplined genericity**.

## 2. Review Questions

This review answers:

- Which objects need a common stable identity?
- Which objects should remain strongly typed and outside a generic research-object registry?
- How should cross-type relationships be represented?
- When should a relationship become a first-class object?
- How do we preserve domain generality without losing scientific meaning?
- How do we avoid polymorphic-reference chaos?
- How should history/versioning and HUMAN review attach to relationships?
- Can Profile A and Profile B use the same identity and association mechanics?

## 3. Architectural Decision Summary

J2 adopts a **hybrid typed-core + generic research identity model**.

Conceptually:

```text
Strongly Typed Provenance / Context Objects
-------------------------------------------
ResearchProfile
ResearchProject
LiteratureSource
SourceRecord
Work
EvidenceFragment
Claim
CoverageContext
Assessment
ChangeEvent
HumanDecision
RStageDefinition / RStageState

                    ↓ may reference

Generic Research Object Identity
--------------------------------
ResearchObjectIdentity
    ├── Concept / Construct
    ├── Definition
    ├── Scientific Relationship
    ├── Mechanism
    ├── BoundaryCondition
    ├── LevelOfAnalysis
    ├── Theory
    ├── Model / Framework
    ├── Method
    ├── Operationalization / Measurement
    ├── GapCandidate
    ├── ExistingSolution
    ├── Alternative
    ├── CandidateContribution
    └── Synthesis

                    ↕

Typed Association Families
--------------------------
EvidenceRelationship
ResearchObjectAssociation
RelationshipParticipant
ConceptMeasurementAssociation
GapSolutionAssociation
GapContributionAssociation
ContributionAssociation
SynthesisMembership
RStageImpact
ProjectWorkRelevance
AssessmentReason
```

This is a conceptual decision. J2 is still **not** selecting final PostgreSQL tables.

## 4. Why Not Put Everything Behind One Generic ID?

A universal `Object(id, type, json)` model would make persistence superficially simple but would weaken important invariants.

For example:

- a Claim must originate from an EvidenceFragment;
- an EvidenceFragment must belong to a Work;
- a SourceRecord must originate from a LiteratureSource;
- a HumanDecision has an actor, rationale, evidence context, and temporal semantics;
- an Assessment has machine-advice semantics and versioning;
- RStageState belongs to a Project and a fixed RStageDefinition.

These are not arbitrary graph nodes. Their structural rules are part of scientific integrity.

### Decision

**Do not place all system objects into one universal object table conceptually.**

Generic identity is reserved for research-semantic objects that benefit from cross-type association and shared navigation behavior.

## 5. Why Have a Generic Research Object Identity at All?

Several J1/J2 capabilities need to refer to different scientific object types through the same UX mechanisms:

- Today / What Changed? can point to Gap, Theory, Method, Construct, Contribution, Synthesis, etc.;
- EvidenceRelationship can target different scientific object types;
- Assessment can evaluate different research objects;
- ChangeEvent can describe changes to different research objects;
- HumanDecision can concern different research objects;
- RStageImpact can point to objects affecting one or more stages;
- Human Review can queue different kinds of scientific attention items.

Without a shared research-object identity, every cross-cutting feature would need separate link logic for every object type.

### Decision

Introduce a conceptual `ResearchObjectIdentity` for objects that participate in generic research reasoning, navigation, assessment, temporal change, and HUMAN judgment.

## 6. ResearchObjectIdentity

### Purpose

Provides a stable identity and common cross-cutting metadata for a scientific/research-semantic object.

### Minimum conceptual fields

```text
ResearchObjectIdentity
- object_id
- object_type
- project_scope or profile/global scope where applicable
- canonical label/title
- lifecycle visibility state
- created_at
- created_by / created_origin
- version lineage reference where needed
```

The exact fields will be refined later.

### Critical rule

`ResearchObjectIdentity` is **not** the scientific content record itself.

Example:

```text
ResearchObjectIdentity RO-014
Type: GAP_CANDIDATE
        ↓
GapCandidate GAP-014
Statement: ...
Gap type: THEORETICAL_GAP
Evolution: CONTESTED
...
```

The typed object retains its own scientific fields.

## 7. Candidate Research Object Types

The initial generic identity family should include objects that are meaningful targets of evidence, assessment, change, review, and navigation:

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
GAP_CANDIDATE
EXISTING_SOLUTION
ALTERNATIVE
CANDIDATE_CONTRIBUTION
SYNTHESIS
```

This list is extensible through deliberate J2/J3+ evolution, not arbitrary runtime invention.

## 8. Objects That Should Remain Outside ResearchObjectIdentity v0

The following should remain strongly typed infrastructure/provenance/context objects in v0:

```text
ResearchProfile
ResearchProject
Watchlist
LiteratureSource
SourceRecord
Work
EvidenceFragment
Claim
EvidenceRelationship
Assessment
ChangeEvent
HumanDecision
RStageDefinition
RStageState
CoverageContext
SourceHealth / CapabilityHealth
Run / Job / Quarantine context
```

### Why?

They have strong structural semantics and are not interchangeable scientific concepts.

For example, a Work is a bibliographic entity, not a theory/gap/method object. A Claim is an atomic proposition with strict evidence provenance. A ChangeEvent is a temporal reasoning record, not the thing being reasoned about.

## 9. Claim Is Deliberately Not a Generic Research Object

A Claim is central but should remain strongly typed.

Reason:

```text
EvidenceFragment → Claim → EvidenceRelationship → ResearchObjectIdentity
```

This chain gives Claim a distinct epistemic role: it is the atomic proposition extracted from one primary fragment.

If Claim were treated exactly like every other generic object, the system could accidentally obscure the difference between:

- source-derived proposition;
- project interpretation;
- theory object;
- synthesis;
- gap candidate.

### Decision

**Claim remains a first-class provenance-aware object and acts as the source side of EvidenceRelationship.**

## 10. Work Is Deliberately Not a Generic Research Object

A Work participates in many research contexts, but it is bibliographic/provenance infrastructure.

A Work can still be referenced from:

- ProjectWorkRelevance;
- ExistingSolution underlying references;
- Theory/Method evidence provenance;
- search/discovery results;
- EvidenceFragment/Claim.

But it should not become an interchangeable target in generic scientific reasoning merely for convenience.

Where the HUMAN says “this paper is an existing solution,” that should be modeled as:

```text
Work
  ↓ underlying reference
ExistingSolution
  ↓ project interpretation
GapSolutionAssociation
  ↓
GapCandidate
```

rather than turning Work itself into a Gap/solution semantic object.

## 11. Association Design Principle

A relationship should be first-class if it carries one or more of:

- scientific semantics;
- role/polarity;
- evidence basis;
- scope/context;
- HUMAN review state;
- machine-vs-HUMAN origin;
- confidence/advice explanation observations;
- temporal validity/history;
- rationale;
- qualifiers;
- multiple participants.

A relationship that carries none of these may remain simple structural linkage.

## 12. Generic Association Envelope

J2 adopts the concept of a **generic association envelope with typed association families**, rather than one unconstrained `edges` structure.

Conceptually:

```text
AssociationIdentity
- association_id
- association_family
- semantic_type
- scope
- created_at
- origin
- review_state
- version/history
```

Then each family carries its own required structure.

Example:

```text
AssociationIdentity AR-001
Family: GAP_SOLUTION
Semantic type: PARTIALLY_ADDRESSES
        ↓
GapSolutionAssociation
Gap: GAP-014
Solution: SOL-008
Residual limitation: ...
Evidence basis: ...
```

### Decision

A generic envelope may be useful for cross-cutting history/navigation, but **family-specific validation remains mandatory**.

## 13. Why Not One Universal `subject_id / predicate / object_id` Edge?

A universal triple store would allow:

```text
A --RELATES_TO--> B
```

but would fail to encode important constraints cleanly:

- EvidenceRelationship must start from Claim;
- RelationshipParticipant belongs to one ScientificRelationship and has a role;
- SynthesisMembership has polarity and contribution-to-synthesis semantics;
- GapSolutionAssociation may carry residual limitation;
- AssessmentReason links a dimension/reason to evidence;
- RStageImpact is an attention relation, not a scientific evidence relation.

### Decision

**Reject universal untyped edge as the primary model.**

A graph projection can be produced later for visualization/search, but it should be derived from typed canonical associations.

## 14. EvidenceRelationship Family

### Structure

```text
Claim 1
   ↓
EvidenceRelationship
- semantic type
- rationale
- review state
- origin
- version/history
   ↓
ResearchObjectIdentity 1
```

Initial semantics:

`SUPPORTS | CHALLENGES | EXTENDS | REPLICATES | CONTRADICTS | ADDRESSES`

### Rules

- exactly one source Claim;
- exactly one target research object;
- evidence semantics are explicit;
- one Claim can create multiple EvidenceRelationships;
- each relation can be independently reviewed/versioned.

### Decision

**First-class typed family.**

## 15. ResearchObjectAssociation Family

A generic scientific association between two research objects is useful for relations that are not direct evidence semantics and do not merit a more specialized family.

Examples:

```text
Theory COMPETES_WITH Theory
Mechanism EXPLAINS ScientificRelationship
BoundaryCondition QUALIFIES Theory
BoundaryCondition QUALIFIES GapCandidate
Method SUITABLE_FOR CandidateContribution
Definition DEFINES Concept
```

### Constraints

The association must use a controlled semantic type appropriate to the object categories.

Do not allow arbitrary free-text predicates to become canonical semantics.

### Decision

**Accept as a controlled generic family for cross-type research semantics.**

Specialized families override this when they carry richer structure.

## 16. RelationshipParticipant Family

Scientific relationships among constructs need participant roles rather than pairwise columns.

Conceptually:

```text
ScientificRelationship SR-017

Participants:
Concept A      role=PREDICTOR
Concept B      role=OUTCOME
Concept M      role=MEDIATOR
Concept Z      role=MODERATOR
```

Potential roles:

`PREDICTOR | OUTCOME | MEDIATOR | MODERATOR | CONTROL | ANTECEDENT | CONSEQUENCE | CONTEXT | OTHER`

The vocabulary should remain extensible and scientifically neutral.

### Decision

**Mediator/Moderator are roles, not mandatory top-level entity types.**

## 17. Definition Association

A Definition remains a research object because definitions can themselves be evidenced, contested, compared, and changed.

But ownership semantics are narrow:

```text
Definition 1 → 1 Concept/Construct
Concept 1 → 0..* Definition
```

This can be represented as a specialized semantic association or a typed parent relation later.

### Decision

**Retain narrow semantic relationship; do not make Definition an arbitrary many-to-many concept link.**

## 18. ConceptMeasurementAssociation

This must remain first-class because measurement choice carries scientific meaning.

Conceptually:

```text
Concept/Construct * ↔ * Measurement/Operationalization
```

Possible metadata:

- operationalization role;
- scale/instrument version;
- level of analysis;
- validity/reliability observations;
- context/population;
- source/evidence references;
- review state.

### Decision

**Specialized typed association.**

Do not reduce it to generic `RELATED_TO`.

## 19. GapSolutionAssociation

This is a core reasoning association.

Conceptually:

```text
GapCandidate * ↔ * ExistingSolution
```

Possible semantic types:

`POTENTIALLY_ADDRESSES | PARTIALLY_ADDRESSES | STRONGLY_OVERLAPS | CHALLENGES_GAP | LEAVES_RESIDUAL_GAP`

Possible metadata:

- addressed aspect;
- residual limitation;
- evidence basis;
- contextual difference;
- current interpretation;
- HUMAN review;
- temporal history.

### Decision

**Specialized typed association.**

This association is essential to the UX rule “Existing Solutions before Novelty.”

## 20. GapContributionAssociation

Conceptually:

```text
GapCandidate * ↔ * CandidateContribution
```

Semantic possibilities:

- RESPONDS_TO;
- NARROWS;
- INTEGRATES;
- REFRAMES;
- ADDRESSES_RESIDUAL;
- DEPENDS_ON.

The association may carry rationale and scope.

### Decision

**Specialized association or controlled ResearchObjectAssociation subtype.**

For v0, treat it as a named family because it is central to Opportunity/Novelty reasoning.

## 21. ContributionAssociation

CandidateContribution may connect to Theory, Mechanism, Construct, Method, BoundaryCondition, or ScientificRelationship.

Examples:

```text
Contribution EXTENDS Theory
Contribution INTEGRATES Theory A + Theory B
Contribution CLARIFIES Mechanism
Contribution REFINES Construct
Contribution INTRODUCES_BOUNDARY BoundaryCondition
Contribution IMPROVES Method
```

### Decision

Use a controlled typed association family with target ResearchObjectIdentity.

No domain-specific contribution tables.

## 22. ExistingSolution Underlying Reference

ExistingSolution is a project-scoped interpretive object, not a duplicate of the underlying literature/scientific entity.

It may reference one or more underlying entities:

- Work;
- Theory;
- Model/Framework;
- Method;
- Mechanism;
- ScientificRelationship;
- other supported research object.

Because Work is outside ResearchObjectIdentity, the underlying-reference mechanism must support a small set of strongly typed source categories.

### Decision

Do not solve this with arbitrary polymorphic strings.

Use an explicit typed underlying-reference association concept with an allowed target category list.

## 23. SynthesisMembership

A Synthesis aggregates Claims but each membership has a role.

Conceptually:

```text
Synthesis * ↔ * Claim
```

Membership roles may include:

`SUPPORTING | CHALLENGING | CONTRADICTORY | BOUNDARY | UNRESOLVED | CONTEXTUAL`

Possible metadata:

- relevance/weight observation;
- rationale;
- context;
- inclusion/exclusion state;
- HUMAN review;
- version/history.

### Decision

**First-class typed membership.**

A synthesis must not be represented as a comma-separated list of Claim IDs.

## 24. ProjectWorkRelevance

A Work can be relevant to many Projects, and one Project uses many Works.

Conceptually:

```text
ResearchProject * ↔ * Work
```

Association metadata may include:

- discovery/watchlist origin;
- relevance rationale;
- machine relevance advice;
- HUMAN relevance state;
- project-specific tags/context;
- first/last seen;
- exclusion reason.

### Decision

**First-class contextual association.**

The Work remains globally normalized; project interpretation is local.

## 25. RStageImpact

RStageImpact is not a scientific evidence relation. It is a project reasoning/attention relation.

Conceptually:

```text
ChangeEvent / ResearchObject / Assessment
       ↓
RStageImpact
       ↓
RStageState
```

Metadata may include:

- impact type;
- reason;
- suggested attention;
- severity/priority advice;
- temporal context.

### Decision

**First-class typed association.**

It must never automatically gate or transition another stage.

## 26. Assessment Target Identity

Assessment needs to evaluate different research object types with one generic mechanism.

Conceptually:

```text
Assessment
  → one primary ResearchObjectIdentity
```

Examples:

- GapCandidate assessment;
- Theory positioning assessment;
- Method feasibility assessment;
- CandidateContribution novelty assessment;
- Synthesis evidence-coverage assessment.

### Decision

This is a strong justification for `ResearchObjectIdentity`.

Assessment remains a typed temporal object; its target is generic.

## 27. AssessmentReason

An Assessment must explain itself.

Conceptually:

```text
Assessment
  ↓
AssessmentReason 1..*
  ├── dimension
  ├── reason text / structured observation
  ├── supporting Claim/EvidenceRelationship references
  ├── challenging references
  └── coverage observations
```

### Decision

**First-class reasoning component.**

Do not store only a score and opaque explanation string.

## 28. ChangeEvent Target Identity

A ChangeEvent should have one primary focal ResearchObjectIdentity for clarity.

Examples:

```text
CE-0048 → GAP-014
CE-0051 → THEORY-006
CE-0052 → METHOD-012
```

It may also link to secondary affected objects through association records.

### Decision

**One primary target + zero or more secondary impacts.**

This avoids an event with many targets becoming impossible to explain.

## 29. HumanDecision Target Identity

A HumanDecision should similarly have one primary focal research object in v0.

Example:

```text
HD-0031
Decision: MODIFY
Primary object: GAP-014
Affected: Theory-006, Contribution-003, R5, R12
```

Secondary affected objects can be linked separately.

### Decision

**One primary ResearchObjectIdentity target, optional secondary affected objects.**

This preserves clear HUMAN rationale.

## 30. Scope Model

Not every research object has the same scope.

J2 distinguishes conceptually:

### Global/corpus-reusable scientific objects

Examples:

- Concept/Construct;
- Theory;
- Model/Framework;
- Method;
- Measurement;
- LevelOfAnalysis.

These may be reused across Profiles/Projects while labels/interpretations can still vary.

### Profile-context objects

Examples may include:

- profile terminology mapping;
- domain-specific synonym/search configuration;
- profile-level synthesis/watchlist context.

### Project-scoped reasoning objects

Examples:

- GapCandidate;
- ExistingSolution interpretation;
- Alternative;
- CandidateContribution;
- project Synthesis;
- Assessment;
- HumanDecision.

### Decision

`ResearchObjectIdentity` must expose scope rather than assuming every object is globally reusable.

## 31. Identity vs Equivalence

Stable identity must not accidentally assert scientific equivalence.

Examples:

- two search terms may map to one discovery vocabulary group but remain distinct constructs;
- two Theory names may refer to the same theory only after normalization/review;
- two Measurements with similar labels may be different instruments;
- two gaps with similar wording in different Projects are not automatically the same GapCandidate.

### Decision

Identity normalization and scientific equivalence are separate operations.

Potential future relation types include:

`SAME_AS_CANDIDATE | ALIAS_OF | RELATED_TO | OVERLAPS_WITH | DISTINCT_FROM`

with HUMAN review where scientifically consequential.

## 32. Stable IDs and Human-Readable IDs

J2 conceptually distinguishes:

- immutable internal stable identity;
- optional human-readable type-prefixed display identity.

Examples:

```text
internal: [stable UUID-like identity]
display:  GAP-014
```

The display label may be project-relative and should not be treated as the globally unique persistence key.

### Decision

Use stable internal identity conceptually; human-readable IDs are UX aids.

## 33. Versioning Model

Not every edit should create a new identity.

Recommended conceptual distinction:

```text
Object Identity
    ↓
Object Version(s)
```

A change in wording, assessment state, or interpretation may produce a new version while retaining identity.

A genuinely different scientific object receives a new identity.

Examples:

- narrowing GAP-014 may remain the same identity if it is a tracked reformulation;
- splitting GAP-014 into two independent gaps should create new identities linked by lineage;
- a HumanDecision never gets rewritten; a new HumanDecision supersedes the earlier decision.

### Decision

**Identity continuity + versioned state + explicit lineage where objects split/merge/supersede.**

## 34. Association Versioning

Relationships also change.

Example:

```text
v1  CLM-142 SUPPORTS GAP-014
v2  HUMAN review narrows scope
v3  relationship becomes CHALLENGES GAP-014
```

There are two valid conceptual approaches:

1. same association identity with versions; or
2. superseding association records.

### Decision for J2

Require **history-preserving association evolution**, but defer exact persistence technique.

Canonical current state must never erase old semantics.

## 35. Deletion and Retention Semantics

Scientific objects and associations should rarely be hard-deleted once they have influenced assessment, change history, or HUMAN decisions.

Preferred conceptual states:

- active;
- superseded;
- rejected by HUMAN for current project;
- quarantined;
- archived/inactive.

### Decision

History-bearing research objects use lifecycle state rather than destructive deletion by default.

## 36. Quarantine and Generic Identity

Quarantine applies to the smallest affected unit.

Examples:

- EvidenceFragment quarantined;
- Claim quarantined;
- EvidenceRelationship quarantined;
- one association quarantined;
- one research object interpretation quarantined.

Quarantine does not invalidate unrelated objects sharing the same Work or Project.

### Decision

Lifecycle/review state may exist on both objects and first-class associations where needed.

## 37. Controlled Semantic Vocabularies

Genericity must not mean unrestricted strings.

J2 recommends controlled vocabularies per association family.

Examples:

### EvidenceRelationship
`SUPPORTS | CHALLENGES | EXTENDS | REPLICATES | CONTRADICTS | ADDRESSES`

### GapSolutionAssociation
`POTENTIALLY_ADDRESSES | PARTIALLY_ADDRESSES | STRONGLY_OVERLAPS | CHALLENGES_GAP | LEAVES_RESIDUAL_GAP`

### ContributionAssociation
`EXTENDS | INTEGRATES | CLARIFIES | REFINES | BOUNDS | IMPROVES`

### RelationshipParticipant
`PREDICTOR | OUTCOME | MEDIATOR | MODERATOR | CONTROL | CONTEXT | OTHER`

Exact vocabularies can evolve, but every semantic value must have documented meaning.

## 38. Validation Strategy

Association validation should occur by **family and object category**, not by domain.

Example:

```text
EvidenceRelationship
source must be Claim
 target must be allowed ResearchObjectIdentity type
```

```text
GapSolutionAssociation
left must be GapCandidate
right must be ExistingSolution
```

```text
RelationshipParticipant
parent must be ScientificRelationship
participant must be Concept/Construct
role must be allowed participant role
```

### Anti-pattern

```text
if domain == "management": allow MEDIATOR
if domain == "it_governance": disallow MEDIATOR
```

The generic scientific model decides validity, not the discipline name.

## 39. Cross-Domain Test — Profile A

Illustrative identity/association trace:

```text
Concept: Governance Capability
Concept: Cross-agency Coordination
ScientificRelationship: Governance Capability → Cross-agency Coordination
Theory: Institutional Theory
Mechanism: Institutional Coordination Mechanism
GapCandidate: GAP-A014
ExistingSolution: SOL-A008
CandidateContribution: CON-A003

Claims from Work/EvidenceFragments
   ↓ EvidenceRelationship
GAP-A014 / Theory / Mechanism

GAP-A014
   ↔ GapSolutionAssociation ↔ SOL-A008
   ↔ GapContributionAssociation ↔ CON-A003
```

No Profile-A-specific association engine is required.

## 40. Cross-Domain Test — Profile B

Illustrative identity/association trace:

```text
Concept: Human Capability
Concept: Adaptive Behaviour
Concept: Organizational Resilience
ScientificRelationship:
Human Capability → Adaptive Behaviour → Organizational Resilience
Participant role: mediator where scientifically appropriate
Theory: Dynamic Capabilities / competing theory candidate
Mechanism: Adaptive Behaviour Mechanism
GapCandidate: GAP-B014
ExistingSolution: SOL-B009
CandidateContribution: CON-B003

Claims from Work/EvidenceFragments
   ↓ EvidenceRelationship
GAP-B014 / Theory / Mechanism

GAP-B014
   ↔ GapSolutionAssociation ↔ SOL-B009
   ↔ GapContributionAssociation ↔ CON-B003
```

The same object identity and association families work unchanged.

## 41. Generality Review Result

The proposed model passes the current A/B test because differences are represented by:

- object instances;
- controlled semantics;
- participant roles;
- Profile/Project configuration;
- optional specialized add-ins if genuinely needed.

No domain-specific core identity table or association engine is required.

If a future domain requires a relationship that cannot be represented, classify it through ADR-001:

`PROFILE_CONFIG | CORE_GENERALIZATION | ADD_IN_CANDIDATE | UNRESOLVED_GENERALITY`

The project continues while the exception is studied.

## 42. UI Mapping

The model maps cleanly to the accepted J1 UI.

### Today / What Changed?

```text
ChangeEvent → primary ResearchObjectIdentity
```

### Research Opportunities

```text
GapCandidate
↔ GapSolutionAssociation
↔ GapContributionAssociation
↔ EvidenceRelationship
```

### Evidence Explorer

```text
Work → EvidenceFragment → Claim → EvidenceRelationship → ResearchObjectIdentity
```

### Knowledge Evolution

```text
ResearchObjectIdentity → object versions / ChangeEvents / association history
```

### Human Review

```text
Review attention → ResearchObjectIdentity
→ EvidenceRelationships
→ previous Assessment / HumanDecision
```

### R0–R16

```text
RStageState ↔ RStageImpact ↔ ResearchObjectIdentity / ChangeEvent
```

This is the primary acceptance test: the model exists to support the HUMAN-facing cockpit.

## 43. Progressive UI Data Integration

The identity model supports the previously accepted incremental UI strategy:

```text
Phase 1
ResearchProfile + ResearchProject

Phase 2
Work + ProjectWorkRelevance

Phase 3
EvidenceFragment + Claim

Phase 4
Concept/Theory/Method ResearchObjectIdentity
+ EvidenceRelationship

Phase 5
GapCandidate + ExistingSolution + CandidateContribution
+ typed associations

Phase 6
Assessment + AssessmentReason + ChangeEvent

Phase 7
HumanDecision + RStageImpact + CoverageContext
```

The mockup can therefore replace dummy sections with real data incrementally rather than waiting for the entire intelligence system.

## 44. Anti-Patterns Rejected

J2 explicitly rejects:

### Universal EAV object model

```text
object(id, type, key, value)
```

as the primary scientific model.

### Unrestricted graph edges

```text
edge(subject, free_text_predicate, object)
```

as canonical scientific relationships.

### One table per domain

```text
management_gap
it_governance_gap
```

### One pairwise table for every conceivable object combination

This creates schema explosion and discourages generality.

### JSON-only scientific state

Important evidence semantics, decisions, and relationships must remain queryable, inspectable, and constrainable.

### Polymorphic foreign key without validation

```text
target_type + target_id
```

by itself is insufficient if no controlled target registry/family validation exists.

## 45. J2 Acceptance Criteria

The Generic Identity & Association Model is accepted when:

1. cross-cutting features can point to different scientific object types through one stable identity mechanism;
2. provenance objects remain strongly typed;
3. Claim retains atomic evidence provenance;
4. scientific associations remain semantically explicit;
5. rich associations can store rationale, evidence, review state, scope, and history;
6. genericity does not become arbitrary `RELATES_TO` edges;
7. Project-scoped and globally reusable objects remain distinguishable;
8. versioning does not overwrite scientific history;
9. Assessment, ChangeEvent, HumanDecision, and RStageImpact can share target identity mechanics;
10. Profile A and Profile B use the same model without domain-specific branching;
11. the model can populate J1 UI incrementally with real data;
12. the design remains implementable in PostgreSQL without requiring a graph database as canonical storage.

## 46. Review Result

**ACCEPTED FOR J2 v0.**

The recommended pattern is:

> **Strongly typed provenance and temporal objects + stable generic ResearchObjectIdentity + controlled typed association families.**

This gives GFPROJCLAW enough flexibility for cross-domain research intelligence while preserving scientific semantics, traceability, HUMAN authority, and queryable structure.

## 47. Consequence for PostgreSQL Design

The next persistence design should test a structure conceptually similar to:

```text
Typed core entities
+
research_object_identity
+
typed scientific object tables
+
association identity/envelope where useful
+
typed association tables/families
+
version/history strategy
```

However, the next step must still resist table proliferation.

Before writing migrations, PostgreSQL design should answer:

- which typed objects deserve independent tables;
- which can share a generic typed-content structure safely;
- how ResearchObjectIdentity enforces real referential integrity;
- how association families preserve FK constraints;
- how version/history is represented economically;
- how legacy evidence assets map into the new model.

## 48. Recommended Next J2 Artifact

**J2 PostgreSQL Persistence Shape Review v0**

Purpose:

Translate the accepted conceptual model into a minimal PostgreSQL persistence shape **without yet implementing migrations**.

That review should compare at least:

- fully normalized typed tables;
- generic identity + typed subtype tables;
- selective JSONB for extensible attributes;
- typed association tables;
- history/version patterns;
- legacy-to-new mapping.

The output should select the smallest persistence model that preserves J1/J2 scientific contracts.

---

**Checkpoint:** `Version 0 — J0 PINNED / J1 ACCEPTED / J2 ACTIVE`  
**Review:** Generic Identity & Association Model — **ACCEPTED**  
**Scientific authority:** HUMAN  
**Generality:** continuously tested using Profile A and Profile B.
