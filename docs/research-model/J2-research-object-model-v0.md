# J2 Research Object Model v0

Status: **J2 ACTIVE — Conceptual Object Model**

## 1. Purpose

J2 translates the accepted J1 UX into a minimum, domain-agnostic research object model.

This stage does **not** begin from database tables. It begins from the HUMAN-facing questions already accepted in J1:

- What changed?
- What evidence leads us here?
- What challenges it?
- What research opportunity is emerging?
- What existed before?
- Which R0–R16 stages are affected?
- What did the HUMAN decide, and in what evidence context?
- How complete was coverage at that time?

The governing principle is:

> **Objects exist because they support research reasoning, evidence traceability, temporal understanding, or HUMAN judgment.**

## 2. J2 Design Rules

1. The core remains domain-agnostic.
2. Profile A and Profile B must use the same object types and relationship mechanics.
3. Domain vocabulary belongs in Research Profiles and object instances, not core class names.
4. Evidence provenance is mandatory for evidence-backed scientific claims.
5. Machine assessment and HUMAN judgment remain separate objects/concepts.
6. Historical states are versioned; important scientific state is not silently overwritten.
7. Local failure/quarantine affects the smallest relevant object scope.
8. Coverage is explicit context, not hidden inside one confidence score.
9. R0–R16 is represented as research reasoning context, not a workflow gate chain.
10. J2 defines conceptual objects and relationships; persistence technology belongs later.

## 3. Top-Level Conceptual Map

```text
ResearchProfile
    ↓
ResearchProject
    ↓
ResearchJourney / RStage

LiteratureSource → SourceRecord → Work/Paper → EvidenceFragment → Claim
                                             ↓                 ↓
                                      Method / Theory / Concept / Context
                                                               ↓
                                                     EvidenceRelationship
                                                               ↓
                                                     ResearchObject
                                                               ↓
                                                        Assessment
                                                               ↓
                                                        ChangeEvent
                                                               ↓
                                                    HumanDecision

CoverageContext surrounds discovery, evidence, assessment, and decision context.
```

## 4. Object Families

J2 organizes objects into seven conceptual families:

### A. Research Context
- ResearchProfile
- ResearchProject
- Watchlist
- ResearchPolicy / Preference

### B. Literature & Provenance
- LiteratureSource
- SourceRecord
- Work / Paper
- EvidenceFragment

### C. Scientific Content
- Claim
- Concept / Construct
- Definition
- Relationship
- Mechanism
- Mediator
- Moderator
- BoundaryCondition
- LevelOfAnalysis
- Theory
- Model / Framework
- Method
- Operationalization / Measurement

### D. Research Opportunity & Contribution
- GapCandidate
- ExistingSolution / SolutionCandidate
- Alternative
- CandidateContribution

### E. Evidence Semantics
- EvidenceRelationship
- Synthesis

### F. Reasoning, Time & Human Authority
- Assessment
- ChangeEvent
- HumanDecision
- RStage / RStageState / RStageImpact

### G. Coverage & Operations Context
- CoverageContext
- SourceHealth / CapabilityHealth
- Run / Job / Quarantine context as later operational objects

Not every conceptual item must become a standalone table or class.

## 5. ResearchProfile

### Purpose

Defines a reusable knowledge context for a domain or thematic area.

### Minimum conceptual attributes

- stable identifier;
- name;
- description;
- domain/discipline context;
- terminology and search vocabulary;
- concepts/constructs of interest;
- seed works;
- watchlists;
- theory/framework interests;
- method/measurement interests;
- source preferences;
- advice/prioritization preferences;
- version/history.

### Key rule

A profile provides discovery and interpretation context, but does not itself contain one project's scientific conclusions.

## 6. ResearchProject

### Purpose

Represents a specific HUMAN research effort inside a ResearchProfile.

### Minimum conceptual attributes

- stable identifier;
- parent ResearchProfile;
- project name;
- research intent;
- provisional RQs/interests;
- project-specific watchlists;
- active research objects;
- R0–R16 state;
- HumanDecision history;
- version/history.

### Key rule

Literature may be shared at profile level while gaps, RQs, contribution candidates, assessments, and HUMAN judgments remain project-specific.

## 7. Watchlist

### Purpose

Represents a recurring research-attention target.

May refer to:

- topic/concept;
- construct;
- theory/framework;
- method/measurement;
- candidate gap;
- existing solution;
- relationship of concepts;
- author/venue where useful.

A Watchlist may be Profile-level or Project-level.

## 8. LiteratureSource

### Purpose

Represents a configured literature/discovery provider or source system.

Examples may include OpenAlex, Crossref, Semantic Scholar, specialized databases, or future add-ins.

### Key rule

Source identity is not the same as paper/work identity.

## 9. SourceRecord

### Purpose

Represents a record as obtained from one LiteratureSource.

It may contain:

- source-specific identifier;
- metadata as retrieved;
- retrieval time;
- access information;
- provenance;
- normalization status;
- source-specific quality/availability observations.

Several SourceRecords may refer to one normalized Work.

## 10. Work / Paper

### Purpose

Represents the normalized scholarly work independent of provider-specific records.

### Minimum conceptual attributes

- stable work identifier;
- title;
- authors;
- publication date/year;
- DOI/other identifiers;
- venue;
- linked SourceRecords;
- access level;
- project/profile relevance links;
- discovery provenance;
- extraction state/history.

### Access vocabulary

`FULL_TEXT | ABSTRACT_ONLY | METADATA_ONLY`

This access state must remain visible downstream.

## 11. EvidenceFragment

### Purpose

Represents the bounded source material that supports an extracted scientific proposition.

Examples:

- full-text passage;
- abstract segment;
- structured source record when appropriate.

### Minimum conceptual attributes

- parent Work;
- source/provenance reference;
- location within source where available;
- access level;
- extraction/version metadata;
- bounded text/representation subject to rights policy.

### Rule

METADATA_ONLY cannot be promoted as passage-level evidence.

## 12. Claim

### Purpose

Represents a scientific proposition extracted or recorded from evidence.

A Claim is not truth.

### Minimum conceptual attributes

- proposition text;
- source EvidenceFragment;
- Work;
- scope/context;
- linked concepts/constructs;
- linked theory/method where relevant;
- extraction/review state;
- version/history.

Potential conceptual review states:

`MACHINE_EXTRACTED | NEEDS_REVIEW | HUMAN_REVIEWED | CONTESTED | QUARANTINED`

Exact enum remains subject to later refinement.

## 13. EvidenceRelationship

### Purpose

Connects a Claim/EvidenceFragment to another research object using explicit scientific semantics.

Initial relationship vocabulary:

`SUPPORTS | CHALLENGES | EXTENDS | REPLICATES | CONTRADICTS | ADDRESSES`

Examples:

```text
CLM-142 CHALLENGES GAP-014
CLM-166 ADDRESSES GAP-014
CLM-180 EXTENDS THEORY-006
CLM-193 CHALLENGES METHOD-012
```

### Rule

The relationship itself is inspectable and versionable. It may be machine-suggested and HUMAN-reviewed.

## 14. Concept / Construct

### Purpose

Represents a scientific concept or construct without tying the core to a discipline.

Examples:

Profile A: governance capability, enterprise architecture capability.

Profile B: human capability, adaptive behaviour, organizational resilience.

### Important rule

Search synonyms do not imply construct equivalence.

## 15. Definition

### Purpose

Represents a particular definition or interpretation of a Concept/Construct from literature or HUMAN synthesis.

This allows conflicting definitions to coexist rather than forcing one canonical definition prematurely.

## 16. Relationship

### Purpose

Represents a proposed or observed scientific relationship among concepts/constructs.

Examples:

```text
A → B
A → M → B
A × Moderator → B
```

This is generic across disciplines.

## 17. Mechanism

### Purpose

Represents an explanatory process linking phenomena or constructs.

A Mechanism is not identical to a statistical relationship.

It may connect to Theory, Claim, GapCandidate, CandidateContribution, and R6/R8/R11.

## 18. Mediator / Moderator

### Purpose

Represent generic relationship roles where scientifically relevant.

These are not Management-specific objects. They are reusable scientific roles applicable across domains.

## 19. BoundaryCondition

### Purpose

Represents a condition under which a claim, mechanism, theory, or relationship may differ.

Examples:

- institutional context;
- organization size;
- country/regulatory environment;
- disruption intensity;
- level of analysis.

Boundary conditions are especially important for gap refinement and contribution formation.

## 20. LevelOfAnalysis

### Purpose

Makes explicit the analytical level relevant to claims and constructs.

Examples:

- individual;
- team;
- organization;
- inter-organizational;
- system;
- institution;
- ecosystem.

Vocabulary may be profile-configurable while the concept remains generic.

## 21. Theory

### Purpose

Represents an explanatory theory used, challenged, integrated, extended, or compared.

A Theory object should support links to:

- mechanisms;
- constructs;
- claims;
- supporting/challenging evidence;
- boundary conditions;
- competing theories;
- candidate contributions;
- R6 Theory Positioning.

The system may recommend theory candidates but never selects scientific direction automatically.

## 22. Model / Framework

### Purpose

Represents models/frameworks that may be explanatory, organizing, normative, operational, or prior solutions.

Theory and Model/Framework remain conceptually distinguishable because not every framework is a theory.

## 23. Method

### Purpose

Represents a research design, data collection method, analytical method, validation approach, or comparable methodological choice.

A generic Method object may contain dimensions such as:

- research design;
- sample/context;
- unit of analysis;
- data collection;
- analysis technique;
- validation;
- limitations.

## 24. Operationalization / Measurement

### Purpose

Represents how a construct is operationalized or measured.

This is essential for identifying whether contradictory findings may arise from different measurements rather than true substantive disagreement.

## 25. GapCandidate

### Purpose

Represents a defensible candidate insufficiency in current knowledge.

Gap types:

`EXPLICIT_GAP | EMPIRICAL_GAP | THEORETICAL_GAP | SYNTHESIS_GAP`

Machine evidence-dynamics states:

`CANDIDATE | STRENGTHENING | WEAKENING | CONTESTED | POSSIBLY_CLOSED | REOPENED`

### Minimum conceptual content

- gap statement;
- gap type;
- scope/context;
- evidence basis;
- known counter-evidence;
- existing solutions;
- affected concepts/theories;
- coverage context;
- evolution state/history;
- affected R-stages;
- HUMAN decision history.

### Rule

Gap state is not HUMAN acceptance.

## 26. ExistingSolution / SolutionCandidate

### Purpose

Represents previously discovered work, theory, framework, method, mechanism, model, intervention, or adjacent-domain solution that may already address all or part of a GapCandidate.

### Key role

ExistingSolution must be examined before novelty is promoted.

## 27. Alternative

### Purpose

Represents an alternative scientific interpretation or path, such as:

- competing explanation;
- different theory;
- different mechanism;
- different method;
- different construct formulation;
- different boundary condition.

Alternatives remain first-class so the system does not collapse reasoning too early.

## 28. CandidateContribution

### Purpose

Represents a possible contribution that could arise if the study succeeds.

Possible categories:

- theoretical extension;
- theory integration;
- boundary condition;
- mechanism clarification;
- construct refinement;
- empirical contribution;
- methodological contribution;
- synthesis/integration;
- practical/policy contribution.

It remains a candidate until HUMAN scientific judgment.

## 29. Synthesis

### Purpose

Represents a current evidence-aware interpretation assembled from multiple Claims and EvidenceRelationships.

Examples:

- What We Know;
- What We Don't Know;
- current gap synthesis;
- current theory comparison;
- current method landscape.

### Rule

A Synthesis must expose supporting and challenging evidence and coverage context.

## 30. Assessment

### Purpose

Represents a machine-generated or system-generated advice assessment about a research object.

Potential dimensions:

- Gap Evidence Strength;
- Novelty Potential;
- Counter-Evidence Risk;
- Evidence Coverage Context;
- Theoretical Significance;
- Methodological Feasibility;
- RQ–Theory–Method Alignment;
- Practical/Policy Significance;
- Review Priority.

### Rules

- scores are advice/ranking;
- not probabilities;
- not publication/Q1 probabilities;
- no score threshold decides HUMAN acceptance;
- assessments are versioned;
- decomposed reasons/evidence must remain inspectable.

## 31. ChangeEvent

### Purpose

Represents a meaningful change in research understanding or coverage context.

Core trace:

`Previous State → ChangeEvent → New/Changed Evidence → Reasoning Delta → Current State`

### Minimum conceptual content

- affected research object;
- timestamp;
- previous state/assessment;
- current state/assessment;
- trigger/new evidence;
- reasoning delta;
- affected R-stages;
- coverage context;
- HUMAN attention implication.

### Rule

Raw crawler activity is not automatically a scientific ChangeEvent.

## 32. HumanDecision

### Purpose

Represents HUMAN scientific authority.

Primary v0 decisions:

`REVIEW | MODIFY | ACCEPT DIRECTION | REJECT CANDIDATE | NEED MORE EVIDENCE`

### Minimum conceptual content

- decision;
- rationale;
- actor;
- timestamp;
- affected object(s);
- evidence state at decision time;
- known counter-evidence;
- coverage context;
- affected R-stages;
- superseded decision link where relevant.

### Rules

- machine assessment cannot silently rewrite HumanDecision;
- new evidence may request re-review;
- old decisions remain historically visible.

## 33. RStage

### Purpose

Represents one of the R0–R16 HUMAN research reasoning stages.

Canonical stage definitions remain those accepted in J1.

R-stage statuses:

`NOT STARTED | DEVELOPING | EVIDENCE GROWING | NEEDS ATTENTION | HUMAN REVIEWED | MATURE`

### Rule

Status is not percentage completion and does not gate other stages.

## 34. RStageImpact

### Purpose

Represents how a ChangeEvent, research object, or assessment affects one or more R-stages.

Example:

```text
CE-0048 Existing Solution discovered
→ R4 review formulation
→ R5 new falsification evidence
→ R11 contribution scope affected
→ R12 novelty challenge
```

This is an attention relationship, not automatic stage transition.

## 35. CoverageContext

### Purpose

Represents the observable limits under which evidence, assessment, or HUMAN decision was made.

Possible dimensions:

- source coverage;
- query/watchlist coverage;
- temporal coverage;
- evidence access coverage;
- extraction coverage;
- counter-search coverage;
- project relevance coverage;
- freshness;
- known degraded/disabled sources.

### Rule

Coverage should not be collapsed into one opaque certainty score.

## 36. SourceHealth / CapabilityHealth

Operational state vocabulary:

`HEALTHY | DEGRADED | BACKOFF | DISABLED | ATTENTION`

This state describes operation, not scientific validity.

A degraded source may reduce CoverageContext while existing valid evidence remains valid.

## 37. Quarantine Concept

Quarantine is a local state/relationship applied when provenance, extraction, evidence mapping, or another item cannot currently be trusted for evidence-backed promotion.

Example:

```text
CLM-204 QUARANTINED
Reason: passage provenance unresolved
Affected synthesis: GAP-021 coverage reduced
Unrelated claims: continue
```

Quarantine must never imply a global project lock.

## 38. Core Relationship Inventory

The minimum conceptual relationship families include:

```text
ResearchProfile CONTAINS ResearchProject
ResearchProfile DEFINES Watchlist
ResearchProject USES Watchlist
ResearchProject HAS RStage

LiteratureSource PROVIDES SourceRecord
SourceRecord REPRESENTS Work
Work HAS EvidenceFragment
EvidenceFragment SUPPORTS_EXTRACTION_OF Claim

Claim REFERS_TO Concept/Construct
Claim USES / DISCUSSES Theory
Claim REPORTS Method
Claim HAS_CONTEXT LevelOfAnalysis / BoundaryCondition

Claim/EvidenceFragment --EvidenceRelationship--> ResearchObject

GapCandidate HAS ExistingSolution
GapCandidate HAS Alternative
GapCandidate MAY_LEAD_TO CandidateContribution

Assessment ASSESSES ResearchObject
ChangeEvent CHANGES ResearchObject / Assessment / RStageState
ChangeEvent IMPACTS RStage
HumanDecision JUDGES ResearchObject
HumanDecision REFERENCES EvidenceState / CoverageContext
```

Exact cardinalities belong to later refinement.

## 39. Domain-Agnostic Validation — Profile A

Example instances:

```text
Concept: IT Governance Capability
Theory: Institutional Theory
Method: Longitudinal Case Study
GapCandidate: Cross-agency governance mechanism uncertainty
ExistingSolution: Enterprise Architecture capability framework
BoundaryCondition: Institutional fragmentation
LevelOfAnalysis: Inter-organizational
```

All use generic J2 objects.

## 40. Domain-Agnostic Validation — Profile B

Example instances:

```text
Concept: Human Capability
Theory: Dynamic Capabilities / Behavioural Explanation
Method: Multilevel Longitudinal Study
GapCandidate: Mechanism linking human capability to resilience
ExistingSolution: Established adaptive-behaviour model
BoundaryCondition: Environmental turbulence
LevelOfAnalysis: Individual / Team / Organization
```

Again, no new core object family is required.

## 41. Generality Exceptions

If A and B need different behavior:

`A ≠ B → Generic Abstraction → Profile/Project Configuration → Optional Add-in → Unresolved Generality`

Classify as:

`PROFILE_CONFIG | CORE_GENERALIZATION | ADD_IN_CANDIDATE | UNRESOLVED_GENERALITY`

The difference does not globally stop J2.

## 42. What J2 Does Not Define Yet

J2 v0 intentionally does not define:

- PostgreSQL table names;
- primary/foreign key implementation;
- graph database choice;
- vector database choice;
- ORM classes;
- API endpoints;
- event-sourcing technology;
- extraction prompts;
- LLM providers;
- queue topology;
- retry algorithms;
- source adapter contracts;
- UI component code.

Those follow after the conceptual model is accepted and tested against legacy data and the vertical slice.

## 43. UI / UX Incremental Update Principle

The accepted J1 mockup remains the target interaction model.

As real data becomes available, the UI should be connected **incrementally**, not rebuilt at the end.

Recommended progression:

```text
Dummy UI
   ↓
Real Profile / Project data
   ↓
Real Work / SourceRecord data
   ↓
Real EvidenceFragment / Claim data
   ↓
Real Gap / Theory / Method objects
   ↓
Real Assessment / ChangeEvent data
   ↓
Real HumanDecision / Coverage data
```

At every step:

- preserve the accepted navigation model;
- replace dummy cards/tables with real data progressively;
- keep unavailable areas visibly partial rather than inventing data;
- expose provenance and coverage as soon as evidence becomes real;
- avoid waiting for the entire backend before validating the cockpit.

This creates a continuous end-to-end feedback loop between data model, pipeline, and HUMAN UX.

## 44. J2 Acceptance Criteria

J2 v0 is acceptable when:

1. Every major J1 screen can be explained using the conceptual objects above.
2. Evidence traceability is representable end-to-end.
3. Change history is representable without overwriting previous state.
4. HUMAN decisions are separate from machine assessments.
5. Coverage context can be attached to assessments and decisions.
6. R0–R16 impacts are representable without gate semantics.
7. Profile A and Profile B use the same core object model.
8. No core object is named for one reference discipline.
9. Existing solutions and counter-evidence are first-class.
10. The model supports incremental connection of real data into the accepted UI.

## 45. J2 Pinned Principle Candidate

> **GFPROJCLAW models research as traceable, evolving relationships among evidence, scientific objects, assessments, change events, and HUMAN judgments—under explicit coverage context and without domain-specific core branches.**
