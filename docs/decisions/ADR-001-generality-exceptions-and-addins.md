# ADR-001 — Generality Exceptions and Add-ins

Status: **PINNED**  
Applies from: **Version 0 / J1**

## Context

GFPROJCLAW is a domain-agnostic Research Intelligence system developed and continuously validated against two reference profiles:

- **Profile A — Computer / Information Systems:** IT Governance, e-Government / Digital Government, Enterprise Architecture.
- **Profile B — Management / Organization Studies:** Resilient Organization / Organizational Resilience, Human Behaviour, Human Capability.

Cross-domain differences are expected. A capability that cannot initially be represented identically for both profiles is not a reason to stop the project, stop unrelated development, or create a second research core.

## Decision

A cross-domain mismatch is classified as a **Generality Exception**, not a global failure.

The project follows this resolution path:

`A ≠ B → Generic Abstraction → Research Profile/Project Configuration → Optional Add-in → Record Unresolved Exception`

The preferred resolution is the smallest mechanism that preserves a stable, domain-agnostic core.

## Generality Exception Classes

### PROFILE_CONFIG

The difference can be expressed through profile/project configuration, terminology, concepts, constructs, watchlists, seed literature, theories, frameworks, methods, research policies or priorities.

No core source-code change should be required.

### CORE_GENERALIZATION

The difference reveals that the core abstraction is too narrow, while the capability is genuinely useful across research domains.

The core may be generalized using domain-neutral research objects or relationships.

### ADD_IN_CANDIDATE

The capability is genuinely specialized and should not distort the generic core.

Possible examples include:

- specialized source connectors;
- domain ontologies;
- specialized parsers or notations;
- discipline-specific analytical engines;
- specialized method-support tools;
- external research-tool integrations.

An add-in may extend the core but must not redefine HUMAN scientific authority, evidence traceability, or the non-gating R0-R16 journey.

### UNRESOLVED_GENERALITY

The appropriate abstraction is not yet known.

The exception is recorded as architectural/research-design debt and may be investigated later. It does not halt healthy unrelated work.

## Non-Blocking Principle

> **A Generality Exception is an architectural learning signal, not a project stop condition.**

No Generality Exception may create a global development lock merely because one profile needs a capability that another profile does not.

Healthy stages and capabilities continue while the exception is classified and investigated.

This extends the project constitution:

- no global research lock;
- local failures stay local;
- engineering complexity must serve research;
- domain generality is continuously measured rather than assumed.

## Target Extension Architecture

```text
GFPROJCLAW
│
├── Research Intelligence Core
│   ├── Evidence / Claims
│   ├── Theory / Model / Framework
│   ├── Gap / Solution / Contribution
│   ├── Method Intelligence
│   ├── Change Intelligence
│   ├── R0–R16 Living Research Journey
│   └── Human Decision
│
├── Research Profiles / Projects
│   ├── A — Computer / IS
│   └── B — Management / Organization Studies
│
└── Optional Add-ins
    ├── Domain capability
    ├── Specialized analysis
    ├── Specialized source
    └── Specialized research method/tool
```

The add-in boundary is conceptual during J1. Plugin/add-in interfaces and implementation contracts belong to later architecture stages and must not be prematurely engineered.

## Core Protection Rules

An add-in must not:

1. create a separate scientific authority model;
2. bypass evidence provenance and traceability;
3. turn R0-R16 into a domain-specific gate chain;
4. introduce global PASS/FAIL research locks;
5. overwrite contradictory evidence or historical assessments;
6. make HUMAN decisions depend on an AI score threshold;
7. require unrelated healthy research processing to stop when the add-in fails.

An add-in failure must be contained to the smallest responsible scope and should degrade only the capability or coverage it provides.

## Decision Test at Every J-Stage

When Profile A and Profile B differ, ask in order:

1. Can the difference be represented by existing generic objects?
2. Can Research Profile or Research Project configuration represent it?
3. Does the difference reveal a useful cross-domain abstraction missing from core?
4. Is the capability intrinsically specialized enough to remain outside core?
5. If unresolved, can it be recorded without blocking unrelated progress?

The resulting classification is one of:

`PROFILE_CONFIG | CORE_GENERALIZATION | ADD_IN_CANDIDATE | UNRESOLVED_GENERALITY`

## Generality Measurement

Cross-domain validation remains required throughout J0-J16, but the purpose is learning and architectural fitness rather than creating another rigid gate system.

A Generality Exception should be visible in journey documentation with:

- affected J-stage / R-stage;
- Profile A behavior;
- Profile B behavior;
- exception classification;
- evidence/reason for the difference;
- proposed resolution;
- current status;
- impact on HUMAN research;
- whether unrelated work may continue — normally **YES**.

## Acceptance Principle

A domain-specific capability does not invalidate GFPROJCLAW's general architecture merely because an add-in is required.

Generality means the **core scientific reasoning, evidence traceability, knowledge evolution, HUMAN authority and extension mechanism remain stable across domains** — not that every discipline must have identical specialized capabilities.

## Pinned Principle

> **General core, configurable profiles, optional specialized add-ins, non-blocking generality exceptions.**

When a domain difference appears, GFPROJCLAW learns from it. The project generalizes the core when appropriate, configures the profile when sufficient, extends through an add-in when specialization is genuine, or records the exception when unresolved — while healthy development continues.
