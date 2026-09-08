# J2 Object Relationship & Cardinality Review v0

Status: **J2 ACTIVE — Relationship & Cardinality Review**

## 1. Purpose

This review tests whether the conceptual object model derived from J1 can support the full evidence-to-judgment flow without forcing premature database design.

The review focuses on five questions:

1. Which relationships are structurally essential?
2. Which objects are truly one-to-one, one-to-many, or many-to-many?
3. Which relationships need to become first-class objects because they carry scientific meaning, provenance, review state, or history?
4. Which cardinalities must remain flexible to support both reference domains?
5. Which relationships are dangerous to encode as hard constraints because they would reintroduce workflow gates or false scientific certainty?

The governing principle is:

> **Cardinality should represent how research reasoning actually behaves, not how we wish a database to look.**

## 2. Review Scope

The review covers the current J2 object families:

- Research Context
- Literature & Provenance
- Scientific Content
- Research Opportunity & Contribution
- Evidence Semantics
- Reasoning, Time & Human Authority
- Coverage & Operations Context

The target reasoning trace remains:

`Source → Work → Evidence Fragment → Claim → Evidence Relationship → Research Object → Assessment → ChangeEvent → HumanDecision`

with `ResearchProfile`, `ResearchProject`, `RStage`, and `CoverageContext` surrounding that flow.

## 3. Cardinality Notation

This document uses:

```text
1      exactly one
0..1   optional one
1..*   one or more
0..*   zero or more
*..*   many-to-many
```

These are conceptual cardinalities. They are not yet SQL foreign-key definitions.

## 4. Relationship Classification

Relationships are classified into four implementation-shape categories.

### A. Structural parent-child

Simple containment/ownership is likely sufficient.

Examples:

- ResearchProfile → ResearchProject
- Work → EvidenceFragment

### B. Scientific semantic relationship

The relationship itself carries meaning and should be inspectable/versionable.

Examples:

- Claim SUPPORTS GapCandidate
- Claim CHALLENGES Theory

These should usually become first-class relationship records rather than bare foreign keys.

### C. Contextual membership/association

Objects may be reused across Projects or Profiles while interpretation remains local.

Examples:

- Work relevance to multiple Projects
- Concept participation in multiple Projects

### D. Temporal/contextual snapshot relationship

The association is meaningful only in a particular time/evidence context.

Examples:

- Assessment → CoverageContext at assessment time
- HumanDecision → evidence state at decision time

These must preserve history rather than point only to mutable current state.

## 5. ResearchProfile → ResearchProject

### Proposed cardinality

`ResearchProfile 1 → 0..* ResearchProject`

`ResearchProject 1 → 1 ResearchProfile`

### Rationale

A Profile can exist before any Project is created. One Profile may support many Projects. A Project belongs to one primary Profile in v0.

### Important note

Cross-profile projects are intentionally not required in v0. If future research requires combining multiple Profiles, that should be introduced deliberately rather than making every Project multi-profile now.

### Decision

**ACCEPT for v0.**

## 6. ResearchProfile ↔ Watchlist

### Proposed cardinality

`ResearchProfile 1 → 0..* Watchlist`

A Watchlist may be:

- Profile-level; or
- Project-level.

For v0, one Watchlist has one scope owner:

`Watchlist → exactly one of ResearchProfile or ResearchProject`

### Rationale

This preserves clear context while allowing the same conceptual mechanism at both levels.

### Decision

**ACCEPT with scoped ownership.**

Avoid making one Watchlist simultaneously owned by Profile and Project. A Project may inherit/copy/use Profile-level intent without mutating the original.

## 7. ResearchProject → RStage

### Proposed cardinality

`ResearchProject 1 → 17 RStage instances/context slots`

R0 through R16 are fixed stage definitions, but project-specific state is separate.

Recommended conceptual distinction:

```text
RStageDefinition
RStageState
```

Where:

`RStageDefinition 1 → 0..* RStageState`

`ResearchProject 1 → 17 RStageState`

### Rationale

The stage identity is global and stable; the project-specific status, WHY, evidence, risk, change history, and HumanDecision context vary by Project.

### Decision

**ACCEPT distinction: definition vs project state.**

Do not duplicate the R0–R16 definitions inside every project.

## 8. LiteratureSource → SourceRecord

### Proposed cardinality

`LiteratureSource 1 → 0..* SourceRecord`

`SourceRecord 1 → 1 LiteratureSource`

### Rationale

Every SourceRecord originates from one provider/source context. One source yields many records.

### Decision

**ACCEPT.**

## 9. SourceRecord ↔ Work

### Proposed cardinality

`Work 1 → 1..* SourceRecord` for discovered normalized works

`SourceRecord 1 → 0..1 Work` during normalization

### Rationale

Multiple providers can describe the same scholarly work. A SourceRecord may temporarily be unresolved before normalization.

### Scientific consequence

Source identity must remain separate from Work identity. Provider disagreement must not overwrite bibliographic provenance.

### Decision

**ACCEPT asymmetric cardinality.**

This is a key dedup/provenance relationship.

## 10. Work → EvidenceFragment

### Proposed cardinality

`Work 1 → 0..* EvidenceFragment`

`EvidenceFragment 1 → 1 Work`

### Rationale

A metadata-only Work may have zero EvidenceFragments suitable for scientific evidence. A full-text Work may yield many passages/fragments.

### Critical rule

A Work must **not** be required to have an EvidenceFragment.

This preserves:

`METADATA_ONLY` as a valid discovery state.

### Decision

**ACCEPT.**

## 11. EvidenceFragment → Claim

### Proposed cardinality

`EvidenceFragment 1 → 0..* Claim`

`Claim 1 → 1..* EvidenceFragment?`

This requires careful review.

### Option A — one Claim comes from exactly one EvidenceFragment

Simple, strong provenance.

### Option B — one Claim may be synthesized directly from several EvidenceFragments

More flexible but risks mixing extraction and synthesis.

### Recommended decision

For **atomic extracted claims**:

`Claim 1 → 1 EvidenceFragment`

For multi-paper or multi-fragment interpretation, use `Synthesis` rather than allowing an extracted Claim to float across multiple fragments.

### Rationale

This preserves a sharp distinction:

```text
EvidenceFragment → Atomic Claim
Multiple Claims → Synthesis
```

### Decision

**ACCEPT atomic provenance rule.**

One EvidenceFragment may yield several Claims; each atomic Claim originates from one primary EvidenceFragment.

## 12. Claim ↔ Work

### Proposed cardinality

`Work 1 → 0..* Claim`

`Claim 1 → 1 Work`

This is derived through EvidenceFragment but may be materialized conceptually for navigation/performance later.

### Decision

**DERIVED relationship, not independent scientific semantics.**

Avoid maintaining two contradictory provenance paths.

## 13. Claim ↔ Concept / Construct

### Proposed cardinality

`Claim * ↔ * Concept/Construct`

### Rationale

A Claim may involve multiple concepts; a Concept appears across many Claims.

### Relationship metadata may include

- role in claim;
- subject/predicate/object role where useful;
- mention vs substantive use;
- HUMAN review state.

### Decision

**MANY-TO-MANY.**

Likely relationship object or association record rather than comma-separated IDs.

## 14. Concept ↔ Definition

### Proposed cardinality

`Concept/Construct 1 → 0..* Definition`

`Definition 1 → 1 Concept/Construct`

### Rationale

Multiple literature definitions can coexist. A Definition should not simultaneously define unrelated constructs.

If one passage compares constructs, represent that as separate definitions/claims/relationships rather than one Definition belonging to many constructs.

### Decision

**ACCEPT.**

## 15. Concept ↔ Operationalization / Measurement

### Proposed cardinality

`Concept/Construct * ↔ * Operationalization/Measurement`

### Rationale

One construct may be operationalized in many ways; one instrument or measurement approach may operationalize multiple constructs/subscales.

### Scientific importance

This many-to-many relation is essential for explaining apparent contradiction caused by different measurements.

### Decision

**MANY-TO-MANY, first-class association.**

## 16. Claim ↔ Theory

### Proposed cardinality

`Claim * ↔ * Theory`

Relationship roles may include:

- USES
- SUPPORTS
- CHALLENGES
- EXTENDS
- DISCUSSES
- TESTS

### Rationale

A paper claim may invoke more than one theory, and one theory connects to many claims.

### Decision

**MANY-TO-MANY, semantic relationship required.**

Do not reduce to `claim.theory_id`.

## 17. Claim ↔ Method

### Proposed cardinality

`Claim * ↔ * Method`

### Rationale

A claim may be tied to several methodological features: research design, analysis method, instrument, validation strategy. A Method object recurs across many claims/works.

### Recommended nuance

Separate `REPORTS_METHOD` / `DERIVED_UNDER_METHOD` semantics later if useful.

### Decision

**MANY-TO-MANY.**

## 18. Scientific Relationship among Concepts

The current generic `Relationship` object should not be confused with `EvidenceRelationship`.

### Proposed model

A scientific `Relationship` may link:

- source concept(s);
- target concept(s);
- direction;
- role;
- optional mediator/moderator/mechanism;
- scope/context;
- evidence links.

### Cardinality

`Relationship 1 → 2..* Concept/Construct roles`

A Concept participates in `0..* Relationship`.

### Decision

**Relationship must be first-class.**

Do not encode scientific relationships merely as columns like `concept_a_id`, `concept_b_id`, because mediator/moderator/multivariate forms will break that design.

## 19. Mediator / Moderator

### Review result

Mediator and Moderator are better represented as **roles in a scientific Relationship** rather than mandatory standalone top-level entities in every case.

Recommended conceptual model:

```text
RelationshipParticipant
- concept
- role: predictor / outcome / mediator / moderator / control / boundary
```

### Rationale

This remains generic and avoids unnecessary object proliferation.

A dedicated object is still possible later if role-specific metadata warrants it.

### Decision

**NORMALIZE toward role-based relationship participation.**

## 20. Mechanism ↔ Relationship / Theory / Claim

### Proposed cardinalities

`Mechanism * ↔ * Claim`

`Mechanism * ↔ * Theory`

`Mechanism * ↔ * scientific Relationship`

### Rationale

Mechanism is explanatory and may be supported by multiple claims, linked to multiple theories, and explain one or more relationships.

### Decision

**MANY-TO-MANY.**

Mechanism should remain first-class because it is central to theory contribution and gap refinement.

## 21. BoundaryCondition ↔ Research Objects

### Proposed cardinality

`BoundaryCondition * ↔ * Claim / Relationship / Mechanism / Theory / GapCandidate / CandidateContribution`

### Rationale

Boundary conditions may qualify many scientific objects and one object may have several boundary conditions.

### Decision

**MANY-TO-MANY, generic qualification association.**

Avoid a domain-specific boundary-condition column on GapCandidate only.

## 22. LevelOfAnalysis ↔ Scientific Objects

### Proposed cardinality

`LevelOfAnalysis * ↔ * Claim / Concept / Relationship / Method / GapCandidate`

### Rationale

Level of analysis is contextual and reusable. Conflicts can arise precisely because the same concept appears at multiple levels.

### Decision

**MANY-TO-MANY contextual association.**

## 23. Claim → EvidenceRelationship → ResearchObject

This is one of the most important structures in the model.

### Proposed cardinality

`Claim 1 → 0..* EvidenceRelationship`

`EvidenceRelationship 1 → 1 Claim`

`EvidenceRelationship 1 → 1 Target ResearchObject`

A target ResearchObject may have `0..* EvidenceRelationship`.

### Why not many targets per EvidenceRelationship?

Because each semantic assertion should remain individually inspectable.

Example:

```text
CLM-142 CHALLENGES GAP-014
CLM-142 SUPPORTS THEORY-006
```

These should be two relationship records, not one overloaded relation.

### Decision

**ACCEPT single-source-claim / single-target semantic relationship.**

This supports provenance, review state, reasoning, and history cleanly.

## 24. EvidenceRelationship Semantics

Canonical initial vocabulary remains:

`SUPPORTS | CHALLENGES | EXTENDS | REPLICATES | CONTRADICTS | ADDRESSES`

### Review finding

Not every semantic relation applies equally to every object type.

Example:

- `REPLICATES` is natural for findings/claims/studies;
- `ADDRESSES` is especially useful for gaps/solutions;
- `EXTENDS` is natural for theory/model/framework/contribution.

### Decision

Do **not** create separate domain-specific relationship engines.

Instead allow generic relationship types with validation guidance by target object category later.

## 25. GapCandidate ↔ EvidenceRelationship

### Proposed cardinality

`GapCandidate 1 → 0..* EvidenceRelationship`

Through these relations, one gap may have many supporting/challenging/addressing claims.

### Rule

GapCandidate should not directly own raw papers as its scientific evidence.

Preferred trace:

`GapCandidate ← EvidenceRelationship ← Claim ← EvidenceFragment ← Work`

### Decision

**ACCEPT evidence-mediated relation.**

Direct Work↔Gap links may exist for navigation/relevance but should not substitute for evidence semantics.

## 26. GapCandidate ↔ ExistingSolution

### Proposed cardinality

`GapCandidate * ↔ * ExistingSolution`

### Rationale

One solution may address several gaps. One gap may have several existing solutions.

The relationship itself may need metadata:

- degree/scope of address;
- which aspect is addressed;
- remaining limitation;
- evidence basis;
- review state;
- temporal history.

### Decision

**MANY-TO-MANY, first-class association.**

Likely concept name later: `GapSolutionRelationship` or generic `ResearchObjectRelationship` with typed semantics.

## 27. ExistingSolution ↔ Work / Theory / Method / Framework

### Review finding

`ExistingSolution` is likely better treated as a project-level interpretation/reference to one or more existing research objects rather than a duplicate copy of them.

A solution can be:

- a Work;
- a Theory;
- a Model/Framework;
- a Method;
- a Mechanism;
- an intervention/approach.

### Proposed approach

`ExistingSolution 1 → 1..* underlying ResearchObject references`

### Decision

**KEEP ExistingSolution as project-level interpretive object, not a duplicate scientific content object.**

This preserves the meaning “this existing thing is being considered as a solution to this candidate gap.”

## 28. GapCandidate ↔ Alternative

### Proposed cardinality

`GapCandidate 1 → 0..* Alternative`

An Alternative may also relate to other project-level research objects.

### Review finding

Alternative is contextual, not necessarily globally reusable.

### Decision

**Project-scoped object, one-to-many from focal research object for v0.**

If the same underlying Theory/Method/etc. is reused, the Alternative references those objects.

## 29. GapCandidate ↔ CandidateContribution

### Proposed cardinality

`GapCandidate * ↔ * CandidateContribution`

### Rationale

One gap may support several possible contribution forms. One contribution candidate may respond to several related gaps.

### Decision

**MANY-TO-MANY.**

Do not force one gap = one contribution.

## 30. CandidateContribution ↔ Theory / Mechanism / Construct / Method

### Proposed cardinality

All are potentially many-to-many.

Examples:

- one contribution integrates two theories;
- one contribution refines one construct and one mechanism;
- one methodological contribution may affect several methods;
- one theory may be involved in several contribution candidates.

### Decision

**MANY-TO-MANY typed associations.**

## 31. Synthesis ↔ Claim

### Proposed cardinality

`Synthesis * ↔ * Claim`

But the relationship must carry polarity/role, such as:

- supporting;
- challenging;
- contradictory;
- boundary;
- unresolved;
- included/excluded with reason.

### Rationale

A Claim may contribute to several syntheses; each synthesis uses many claims.

### Decision

**MANY-TO-MANY, first-class membership relationship.**

Do not store a simple list of claim IDs without role/context.

## 32. Synthesis ↔ ResearchObject

### Proposed cardinality

`ResearchObject 1 → 0..* Synthesis`

A Synthesis usually has one primary focal ResearchObject/context.

Examples:

- current synthesis for GAP-014;
- theory comparison synthesis for THEORY cluster;
- method landscape synthesis for project/R9.

### Decision

**One primary focal context per Synthesis in v0, versioned over time.**

Cross-object synthesis can reference secondary objects separately.

## 33. Assessment ↔ ResearchObject

### Proposed cardinality

`ResearchObject 1 → 0..* Assessment`

`Assessment 1 → 1 primary ResearchObject`

### Rationale

Assessments are versioned over time. Each assessment should have a clear focal object.

### Multi-dimensional assessment

One Assessment may carry several decomposed dimensions rather than creating one Assessment object per score.

### Decision

**One focal object, many assessment versions.**

## 34. Assessment ↔ Evidence / Reasons

Assessment reasoning should not directly point only to a mutable aggregate.

### Proposed model

`Assessment 1 → 0..* AssessmentReason`

Each reason may reference:

- Claim;
- EvidenceRelationship;
- ExistingSolution;
- Synthesis;
- CoverageContext;
- prior Assessment.

### Decision

**Assessment explanation must be first-class enough to remain inspectable.**

Exact object name can be deferred, but cardinality must support many reasons per assessment.

## 35. Assessment ↔ CoverageContext

### Proposed cardinality

`Assessment 1 → 1 CoverageContext snapshot/reference`

A CoverageContext may be reused across multiple assessments generated under the same observation state.

### Critical rule

Assessment should reference the coverage state **at assessment time**, not “current coverage”.

### Decision

**Snapshot/reference required.**

## 36. ChangeEvent ↔ ResearchObject

### Proposed cardinality

`ResearchObject 1 → 0..* ChangeEvent`

`ChangeEvent 1 → 1 primary affected ResearchObject`

### Secondary impacts

A ChangeEvent may affect many related objects/stages.

Use separate impact relations rather than giving one ChangeEvent many primary identities.

### Decision

**One primary object + many impact associations.**

This improves explainability in Today and Knowledge Evolution.

## 37. ChangeEvent ↔ Trigger Evidence

### Proposed cardinality

`ChangeEvent 1 → 1..* trigger references`

Possible trigger references:

- new Claim;
- new EvidenceRelationship;
- ExistingSolution discovered;
- Assessment changed;
- CoverageContext changed;
- HumanDecision changed;
- Profile/Project configuration changed.

### Decision

**Many triggers allowed.**

Do not force one paper = one ChangeEvent.

## 38. ChangeEvent ↔ Assessment

### Proposed cardinality

A ChangeEvent may connect:

- `0..1 previous Assessment`
- `0..1 current Assessment`

for the focal assessment type.

But a complex event may affect multiple assessment dimensions/objects.

### Decision

Use explicit before/after references where relevant, plus impact relations for secondary assessments.

## 39. ChangeEvent ↔ RStageImpact

### Proposed cardinality

`ChangeEvent 1 → 0..* RStageImpact`

`RStageState 1 → 0..* RStageImpact`

### Rationale

One evidence event can affect many R-stages; one R-stage accumulates many impacts over time.

### Decision

**MANY-TO-MANY resolved through RStageImpact.**

RStageImpact is definitely a first-class association object.

## 40. HumanDecision ↔ ResearchObject

### Proposed cardinality

A HumanDecision should have:

- one primary focal object;
- optionally several affected/related objects.

### Rationale

A HUMAN usually makes a decision *about something specific* even if that decision has consequences elsewhere.

### Decision

**One primary object + many related objects.**

This avoids ambiguous decisions that cannot later be interpreted.

## 41. HumanDecision ↔ Evidence Context

### Proposed cardinality

`HumanDecision 1 → 1 evidence-state reference/snapshot`

This evidence state may include many Claims, EvidenceRelationships, Syntheses, Assessments, and CoverageContext references.

### Critical rule

A HumanDecision must remain understandable even after the current corpus changes.

### Decision

**Historical evidence context required.**

The eventual implementation may use snapshot manifests/version references rather than copying all evidence.

## 42. HumanDecision ↔ Previous HumanDecision

### Proposed cardinality

`HumanDecision 0..1 → supersedes 0..1 previous HumanDecision`

A decision can also be superseded by `0..1` later decision in a linear decision chain for the same focal context.

### Why linear for v0?

It simplifies temporal interpretation.

If future collaborative decisions require branching/merging, that can be generalized later.

### Decision

**Accept linear supersession chain for v0.**

## 43. HumanDecision ↔ RStage

### Proposed cardinality

`HumanDecision 1 → 0..* affected RStageState`

A stage may have many HumanDecisions over time.

### Decision

**MANY-TO-MANY contextual association.**

A HumanDecision must not be the same object as RStage status.

## 44. RStageState ↔ Evidence / Research Objects

### Proposed cardinality

`RStageState * ↔ * ResearchObject`

`RStageState * ↔ * Synthesis/Assessment`

### Rationale

A stage such as R6 may depend on multiple theories, claims, mechanisms, and assessments. One object can affect multiple stages.

### Decision

**MANY-TO-MANY.**

Do not put a single `gap_id`, `theory_id`, or `method_id` on RStageState.

## 45. CoverageContext ↔ Scope

CoverageContext may be scoped to:

- Profile;
- Project;
- Watchlist/query;
- Run;
- Assessment;
- HumanDecision;
- ChangeEvent.

### Proposed model

Each CoverageContext has one primary scope and can be referenced by many historical objects.

### Decision

**Use reusable immutable/versioned coverage snapshots with clear scope.**

Avoid one mutable global coverage row.

## 46. SourceHealth ↔ LiteratureSource

### Proposed cardinality

`LiteratureSource 1 → 0..* SourceHealth history entries`

Each health entry applies to one source at a time.

### Decision

**One-to-many temporal history.**

Current health is derived from latest relevant entry/state, not by overwriting history only.

## 47. Quarantine Relationships

Quarantine should not automatically become a top-level research object unless implementation proves it useful.

### Recommended conceptual shape

A `QuarantineRecord` may reference exactly one primary affected item:

- SourceRecord;
- EvidenceFragment;
- Claim;
- EvidenceRelationship;
- extraction result;
- Work in rare cases.

One item may have multiple quarantine/history events over time.

### Decision

**Quarantine as local contextual record/state, not a global gate entity.**

## 48. Project Relevance of Shared Works

### Proposed cardinality

`Work * ↔ * ResearchProject`

Relationship metadata may include:

- relevance status/advice;
- discovery reason/watchlist;
- inclusion/exclusion state;
- HUMAN relevance review;
- first seen / last evaluated.

### Rationale

A Work can be relevant to several projects under one Profile, and a Project uses many works.

### Decision

**MANY-TO-MANY, first-class project relevance association.**

Do not duplicate the Work per Project.

## 49. Profile Relevance of Shared Works

### Proposed cardinality

`Work * ↔ * ResearchProfile`

This may sometimes be derivable from project links or discovery context, but Profile-level intelligence requires explicit relevance even before any project exists.

### Decision

**MANY-TO-MANY allowed.**

## 50. Profile / Project ↔ Concept, Theory, Method Interests

### Proposed cardinality

All are many-to-many.

The relationship itself may indicate:

- seed;
- watch;
- preferred;
- excluded;
- suggested;
- accepted by HUMAN;
- source of suggestion.

### Decision

**Use typed configuration associations, not columns on core objects.**

## 51. Object Ownership Review

A useful separation emerges.

### Globally/Corpus-oriented objects

- LiteratureSource
- SourceRecord
- Work
- EvidenceFragment
- atomic Claim
- Concept/Construct
- Theory
- Model/Framework
- Method
- Operationalization/Measurement

These may be reused across Profiles/Projects where scientifically appropriate.

### Context/Project-oriented objects

- GapCandidate
- ExistingSolution interpretation
- Alternative
- CandidateContribution
- project Synthesis
- Assessment
- ChangeEvent
- HumanDecision
- RStageState

These are usually contextual to a ResearchProject.

### Mixed/contextual objects

- Watchlist
- CoverageContext
- Definition
- scientific Relationship
- Mechanism
- BoundaryCondition
- LevelOfAnalysis

Their scope depends on usage.

### Decision

**ACCEPT corpus-vs-project separation as a major J2 design principle.**

## 52. Critical Anti-Patterns Identified

The following relational shortcuts would break the accepted UX or scientific model:

```text
Work.gap_id
```

because one Work can relate to many gaps and relationship semantics matter.

```text
Claim.theory_id
```

because theory relationships are many-to-many and typed.

```text
GapCandidate.solution_id
```

because gap–solution mapping is many-to-many and historically interpretable.

```text
Project.current_human_decision
```

because decisions are object-specific, contextual, and versioned.

```text
RStage.previous_stage_id / next_stage_id as gate dependency
```

because R0–R16 is not a waterfall.

```text
GlobalCoverage.percent
```

because coverage is multidimensional and scoped.

```text
EvidenceRelationship.target_gap_id only
```

because evidence must support/challenge theories, methods, contributions, claims, relationships, and other research objects generically.

## 53. First-Class Relationship Objects Confirmed

This review confirms that several relationships should likely become explicit objects/records in later implementation:

1. **EvidenceRelationship** — Claim → ResearchObject with semantic type and provenance.
2. **ResearchObjectRelationship / typed associations** — e.g. GapCandidate ↔ ExistingSolution, CandidateContribution ↔ Theory.
3. **SynthesisMembership** — Claim ↔ Synthesis with supporting/challenging role.
4. **RStageImpact** — ChangeEvent/ResearchObject ↔ RStageState with reason/impact.
5. **ProjectWorkRelevance** — Work ↔ Project with relevance/discovery context.
6. **ConceptRelationshipParticipant** — Concept participation/role in scientific Relationship.
7. **ConfigurationInterest** — Profile/Project ↔ Concept/Theory/Method/etc. with HUMAN/suggested semantics.
8. **AssessmentReason** — Assessment ↔ evidence/reasoning components.

Exact table/class names remain deferred.

## 54. Cardinalities That Must Stay Flexible

The following must not be over-constrained in J2:

- Claim ↔ Concept;
- Claim ↔ Theory;
- Claim ↔ Method;
- Concept ↔ Measurement;
- Gap ↔ ExistingSolution;
- Gap ↔ CandidateContribution;
- Contribution ↔ Theory/Mechanism/Method;
- RStageState ↔ ResearchObject;
- Work ↔ Project/Profile;
- BoundaryCondition ↔ scientific objects;
- Mechanism ↔ Theory/Claim/Relationship.

These are naturally many-to-many in real research.

## 55. Cardinalities That Should Stay Narrow

The following should remain deliberately narrow in v0:

- ResearchProject → one primary ResearchProfile;
- SourceRecord → one LiteratureSource;
- EvidenceFragment → one Work;
- atomic Claim → one primary EvidenceFragment;
- EvidenceRelationship → one Claim and one target ResearchObject;
- Assessment → one primary focal ResearchObject;
- ChangeEvent → one primary focal ResearchObject;
- HumanDecision → one primary focal ResearchObject;
- HumanDecision supersedes at most one previous decision in v0.

This narrowness improves provenance and explainability without restricting scientific plurality.

## 56. Cross-Domain Validation — Profile A

Example trace:

```text
ResearchProfile A
  → Project: Cross-agency Digital Government Governance

OpenAlex
  → SourceRecord OA-100
  → Work W-042
  → EvidenceFragment EVF-0092
  → Claim CLM-142
  → EvidenceRelationship: CHALLENGES GAP-014

GAP-014
  ↔ ExistingSolution SOL-008
      → underlying Framework/Work
  ↔ CandidateContribution CC-003
  → Assessment A-017
  → ChangeEvent CE-0048
  → HumanDecision HD-0031

CE-0048
  → RStageImpact R5
  → RStageImpact R6
  → RStageImpact R11
  → RStageImpact R12
```

No Profile-A-specific cardinality is required.

## 57. Cross-Domain Validation — Profile B

Example trace:

```text
ResearchProfile B
  → Project: Human Capability & Organizational Resilience

Crossref
  → SourceRecord CR-205
  → Work W-118
  → EvidenceFragment EVF-0211
  → Claim CLM-322
  → EvidenceRelationship: CHALLENGES GAP-014

CLM-322
  ↔ Concept: Human Capability
  ↔ Concept: Adaptive Behaviour
  ↔ Theory: T-006
  ↔ Method: M-012
  ↔ LevelOfAnalysis: Team / Organization

GAP-014
  ↔ ExistingSolution SOL-009
  ↔ CandidateContribution CC-007
  → Assessment A-044
  → ChangeEvent CE-0091
  → HumanDecision HD-0080
```

The same relationship architecture works without domain-specific core branches.

## 58. Generality Review Result

No relationship identified in this review requires a separate Management core or Computing/IS core.

Domain differences are representable through:

- object instances;
- Profile/Project configuration;
- generic relationship roles;
- generic evidence semantics;
- optional specialized source/add-in mechanisms later.

### Result

**Cross-domain cardinality model: ACCEPTED for continued J2 refinement.**

## 59. Open Questions for the Next J2 Step

The following remain intentionally open before PostgreSQL schema design:

1. Should all scientific targets implement one generic `ResearchObject` identity, or should polymorphism be handled through typed references?
2. Should `Theory`, `Model`, and `Framework` remain separate persisted types or one typed scholarly-concept family?
3. Should `Method` be one polymorphic object or split into Design / DataCollection / Analysis / Validation while retaining a shared method family?
4. Should `ExistingSolution` become a generic contextual role over other ResearchObjects rather than its own persisted object?
5. Should `Alternative` remain a standalone contextual object or become a typed research-object relationship?
6. How should immutable evidence-state snapshots be represented without duplicating large evidence sets?
7. What is the minimum generic association model that supports flexibility without turning the entire database into an untyped graph?

These are architectural choices, not blockers.

## 60. Acceptance Decision

The object relationship model is acceptable for moving to the next J2 refinement step because it satisfies the required end-to-end trace:

```text
ResearchProfile
  → ResearchProject
  → Work
  → EvidenceFragment
  → Claim
  → EvidenceRelationship
  → Gap / Theory / Method / Contribution / other ResearchObject
  → Synthesis / Assessment
  → ChangeEvent
  → RStageImpact
  → HumanDecision
```

while preserving:

- evidence provenance;
- contradictory evidence;
- many-to-many scientific reality;
- temporal history;
- HUMAN authority;
- coverage context;
- local failure semantics;
- Profile A / Profile B generality;
- non-gating R0–R16.

## 61. Pinned J2 Relationship Principle Candidate

> **Keep provenance paths narrow, keep scientific relationships plural, make meaningful relationships inspectable, and never encode workflow convenience as scientific truth.**

## 62. Recommended Next Step

Proceed to **J2 Generic Identity & Association Model Review** before PostgreSQL schema design.

That review should resolve how generic ResearchObject identities, typed relationships, contextual roles, and polymorphic associations are represented without creating either:

- dozens of brittle domain-specific link tables; or
- one untyped everything-to-everything graph.

Only after that should J2 produce the first candidate PostgreSQL schema.
