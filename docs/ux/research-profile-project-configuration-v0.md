# Research Profile / Project Configuration v0

Status: **J1 ACTIVE — Low-Fidelity UX Specification**

## 1. Purpose

Research Profile / Project Configuration defines how a HUMAN tells GFPROJCLAW **what research world to observe** and **what specific research effort is currently being developed** without changing the Research Intelligence Core.

The hierarchy is:

`Research Profile → Research Project → Research Cockpit`

The governing principle is:

> **Profile provides knowledge context. Project provides scientific intent. The core provides reusable research intelligence.**

This screen is a central test of domain generality: onboarding a new discipline should primarily be configuration and evidence, not a new software-development project.

## 2. Research Profile vs Research Project

### Research Profile

A Research Profile is a living, reusable knowledge context for a research domain or thematic area.

It may contain:

- domain/discipline description;
- concepts and terminology;
- synonyms and related vocabulary;
- watchlists;
- seed papers/DOIs;
- theories/models/frameworks of interest;
- methods/measurements of interest;
- publication venues or scholarly communities of interest;
- source/search preferences;
- research policies/preferences;
- advice/scoring priorities;
- optional specialized add-ins.

A Profile is **not** one dissertation, paper, or research question.

### Research Project

A Research Project is a specific HUMAN research effort operating within a Profile.

It may contain:

- research intent/problem;
- provisional RQs;
- project-specific watchlists;
- concepts/constructs in focus;
- candidate gaps;
- theory positioning;
- conceptualization;
- method direction;
- contribution candidates;
- R0–R16 journey state;
- Human Decisions;
- project-specific evidence relevance.

One Profile may support multiple Projects.

## 3. Why This Separation Matters

Without this separation, the system risks mixing reusable domain knowledge with one researcher's current hypothesis or project decision.

Example:

```text
PROFILE
Management / Organization Studies

Shared knowledge context:
organizational resilience
human behaviour
human capability
relevant theories/methods/literature

PROJECT 1
Human capability mechanisms in organizational resilience

PROJECT 2
Leadership behaviour during organizational disruption
```

Literature intelligence can be shared while gaps, RQs, contribution claims, R-stage reasoning, and HUMAN decisions remain project-specific.

## 4. Cross-Domain Validation Profiles

Version 0 develops two profiles simultaneously.

### Profile A — Computer / Information Systems

Initial thematic scope:

- IT Governance
- e-Government / Digital Government
- Enterprise Architecture

### Profile B — Management / Organization Studies

Initial thematic scope:

- Resilient Organization / Organizational Resilience
- Human Behaviour
- Human Capability

These are reference configurations for testing generality, not hardcoded branches in the core.

## 5. Primary HUMAN Questions

The configuration experience should help answer:

- What domain/context is GFPROJCLAW currently observing?
- What concepts and terminology should it recognize?
- What literature should seed discovery?
- What topics/watchlists should receive continuing attention?
- What specific research project am I working on?
- What are my provisional research questions or interests?
- Which theories/methods should be watched without forcing their use?
- Which advice dimensions matter more to me?
- What is profile-level versus project-level?
- Can AI suggest configuration without silently changing my scientific intent?
- Can I add a new domain without modifying core source code?

## 6. Profile Creation Flow

The ideal onboarding flow is:

`Create Research Profile → Describe Domain → Add Seeds → Configure Watchlists → Review AI Suggestions → HUMAN Accept/Modify → Start Discovery`

Low-fidelity form:

```text
CREATE RESEARCH PROFILE

Name
[ Management / Organization Studies ]

Domain description
[ ................................................ ]

Core interests
[ Organizational Resilience ] [+]
[ Human Behaviour ] [+]
[ Human Capability ] [+]

Seed papers / DOI / title
[ ................................................ ]

Optional theories/frameworks to watch
[ ................................................ ]

Optional methods/measurements to watch
[ ................................................ ]

[Review Profile]  [Save]
```

No field should require the HUMAN to know an internal ontology or database schema.

## 7. Profile Is Living, Not Frozen

A Profile evolves as the research domain evolves.

The HUMAN may add/remove/refine:

- terminology;
- concepts;
- watchlists;
- seed literature;
- theory interests;
- method interests;
- source preferences;
- scholarly communities;
- priorities.

Profile changes should be versioned because they affect discovery and coverage interpretation.

Example:

```text
Profile v3
Added synonym: organizational adaptability
Added watchlist: resilience capability measurement

Effect:
Future discovery expands.
Historical evidence remains unchanged.
```

## 8. Concepts and Terminology

The core must not hardcode discipline vocabulary.

A Profile may express:

```text
Concept: Organizational Resilience
Terms:
- organizational resilience
- organisational resilience
- resilient organization
- resilient organisation

Related concepts:
- adaptive capacity
- organizational adaptability
```

Profile A may similarly express domain terminology around IT governance, digital government, or enterprise architecture.

These terms help discovery and interpretation but are not automatic declarations that concepts are scientifically equivalent.

## 9. Synonyms Are Not Construct Equivalence

A critical scientific distinction:

> **Search vocabulary expansion is not the same as construct equivalence.**

The Profile may suggest that two terms should both be searched. GFPROJCLAW must not therefore conclude that the underlying constructs are identical.

Construct equivalence/difference belongs to evidence-backed conceptual analysis and HUMAN judgment.

## 10. Seed Literature

A HUMAN may supply seed works through:

- DOI;
- title;
- bibliographic identifier;
- uploaded/available paper reference;
- other supported source identifier.

Seed literature may be used to:

- initialize domain discovery;
- discover related works/citations;
- extract terminology;
- suggest theories/methods/concepts;
- build initial evidence context.

Seed status must retain access-level semantics from Evidence Explorer.

## 11. AI-Assisted Profile Suggestions

AI may suggest profile content based on seeds and domain description.

Example:

```text
SUGGESTED FOR REVIEW

Concepts
+ adaptive capacity
+ institutional capability

Theory/Framework watch
+ dynamic capabilities
+ institutional theory

Method watch
+ longitudinal case study
+ structural equation modelling

Reason:
Frequently appears in current seed literature.

[Accept] [Modify] [Reject]
```

Suggestions do not silently become profile truth.

The HUMAN controls acceptance/modification.

## 12. Watchlists

Watchlists tell continuous discovery what deserves recurring attention.

A watchlist may target generic entities such as:

- topic/concept;
- construct;
- theory/model/framework;
- method/measurement;
- research question theme;
- candidate gap;
- existing solution;
- author/venue where scientifically useful;
- combination/relationship of concepts.

Examples:

```text
Profile A
- IT governance + digital government
- enterprise architecture capability
- cross-agency governance

Profile B
- organizational resilience + human capability
- adaptive behaviour
- resilience measurement
```

The watchlist mechanism remains generic.

## 13. Profile-Level vs Project-Level Watchlists

### Profile-level

Broad continuing intelligence shared across projects.

Example:

`organizational resilience`

### Project-level

Narrow attention tied to a specific research effort.

Example:

`human capability → adaptive behaviour → resilience under disruption`

Project-level watchlists may inherit or refine Profile context without mutating the Profile's shared scientific scope.

## 14. Research Project Creation

After selecting a Profile:

```text
CREATE RESEARCH PROJECT

Profile
[ Management / Organization Studies ]

Project name
[ Human Capability and Organizational Resilience ]

Research intent
[ Understand how human capabilities enable resilient responses ... ]

Provisional questions / interests
[ ................................................ ]

Concepts in focus
[ Human Capability ] [Adaptive Behaviour] [Resilience]

Optional initial theory interests
[ ................................................ ]

Optional method interests
[ ................................................ ]

[Create Project]
```

The HUMAN may begin with incomplete information. R0–R16 exists partly to develop it.

## 15. R0 Research Intent Integration

Project creation should seed, not complete, R0 Research Intent.

Example:

```text
Research intent entered during project creation
        ↓
R0 Research Intent — DEVELOPING
        ↓
Evidence and HUMAN reasoning refine intent over time
```

The configuration screen should not force the HUMAN to specify a finalized RQ, theory, or method before discovery starts.

## 16. Project Context

A Project supplies context for prioritization and interpretation.

It may influence:

- relevance ranking;
- Today / What Changed?;
- project-specific gap candidates;
- R0–R16 stage impacts;
- theory/method alternatives;
- Human Review priority;
- Telegram summaries.

It must not cause evidence from the wider Profile to disappear merely because it does not support the current preferred direction.

## 17. Evidence Sharing and Project Interpretation

A normalized Paper/Work and evidence fragment may be useful to multiple projects.

Conceptually:

```text
Research Profile
       ↓
Shared Literature / Evidence Context
       ├── Project 1 interpretation
       └── Project 2 interpretation
```

Project-specific objects include candidate gaps, RQs, contribution candidates, R-stage reasoning, assessments, and Human Decisions.

This prevents unnecessary duplication while preserving scientific context.

## 18. Advice Priorities

A HUMAN may configure prioritization preferences such as relative emphasis on:

- gap evidence strength;
- novelty potential;
- counter-evidence risk;
- theoretical significance;
- methodological feasibility;
- RQ–Theory–Method alignment;
- practical/policy significance;
- review priority.

These weights affect attention/ranking, not scientific truth.

Example:

```text
Research priorities
Theoretical contribution       HIGH
Counter-evidence sensitivity   HIGH
Method feasibility             MEDIUM
Practical significance         MEDIUM
```

The UI should avoid implying that these preferences make one candidate objectively superior.

## 19. Research Policies / Preferences

Profiles or Projects may later contain configurable policies/preferences such as:

- preferred publication periods;
- languages;
- evidence-access preferences;
- source inclusion preferences;
- search expansion aggressiveness;
- review sensitivity;
- disciplinary terminology.

J1 treats these as HUMAN-visible configuration, not hardcoded core behavior.

## 20. Source Configuration Boundary

Research Profile may express which scholarly sources should be used or prioritized, but source credentials and technical adapter configuration are operational concerns.

The HUMAN research UX should say, for example:

```text
Sources
OpenAlex              Enabled
Crossref              Enabled
Semantic Scholar      Enabled / degraded
Specialized Source    Optional add-in
```

It should not expose secrets or require routine engineering recovery approval.

## 21. Profile Selector and Project Selector

The Cockpit maintains persistent context:

```text
PROFILE
[ Management / Organization Studies ▼ ]

PROJECT
[ Human Capability and Organizational Resilience ▼ ]
```

Changing Profile changes the knowledge context.

Changing Project changes scientific intent, R0–R16 state, project-specific opportunities, assessments, and Human Decisions.

## 22. Profile A Example

```text
PROFILE A
Computer / Information Systems

Interests
- IT Governance
- e-Government / Digital Government
- Enterprise Architecture

Watchlists
- IT governance mechanisms
- digital-government transformation
- enterprise-architecture capability

Seed literature
[configured works]

Theory/framework watch
[HUMAN-configured / AI-suggested]

Method watch
[HUMAN-configured / AI-suggested]

PROJECT
Cross-agency Digital Government Governance

Intent
Investigate governance and architecture capabilities under disruption.

Provisional focus
governance capability
cross-agency coordination
institutional/technology disruption

R0
DEVELOPING
```

## 23. Profile B Example

```text
PROFILE B
Management / Organization Studies

Interests
- Organizational Resilience
- Human Behaviour
- Human Capability

Watchlists
- resilience capability
- adaptive behaviour
- human capability measurement

Seed literature
[configured works]

Theory/framework watch
[HUMAN-configured / AI-suggested]

Method watch
[HUMAN-configured / AI-suggested]

PROJECT
Human Capability and Organizational Resilience

Intent
Investigate how human capabilities enable resilient responses under disruption.

Provisional focus
human capability
adaptive behaviour
organizational resilience

R0
DEVELOPING
```

The structure is identical; only configuration and evidence differ.

## 24. Generality Diagnostic

At every configuration capability, ask:

1. Does Profile A work without core modification?
2. Does Profile B work without core modification?
3. Is a domain assumption leaking into the core?
4. Can the difference be expressed as generic research objects or configuration?
5. Is the capability genuinely specialized?

Classification follows ADR-001:

`PROFILE_CONFIG | CORE_GENERALIZATION | ADD_IN_CANDIDATE | UNRESOLVED_GENERALITY`

A Generality Exception does not globally stop the project.

## 25. Examples of What Must Not Happen

Avoid core logic such as:

```text
if domain == "enterprise_architecture": ...
if domain == "management": ...
```

Avoid separate core implementations such as:

```text
ManagementGapEngine
ITGovernanceGapEngine
ManagementR0toR16
ComputingR0toR16
```

Prefer:

```text
Generic Gap / Theory / Method / Construct / Relationship objects
+
Research Profile configuration
+
Optional specialized add-ins where genuinely necessary
```

## 26. Add-in Visibility

If a Profile uses an optional specialized capability, the HUMAN should be able to see it without confusing it with the core.

Example:

```text
OPTIONAL CAPABILITIES
Specialized Domain Ontology       Enabled
Specialized Source Connector      Enabled
Specialized Analysis Tool         Not installed
```

Add-ins must preserve evidence traceability, HUMAN authority, local failure semantics, and R0–R16 non-gating behavior.

## 27. Profile Versioning and Knowledge Evolution

Profile changes can alter future discovery and therefore need temporal context.

Example:

```text
Sep 01 — Profile v2
Watchlists: organizational resilience, human capability

Sep 08 — Profile v3
Added: adaptive behaviour
Added synonym: organisational resilience

Effect:
New discovery coverage expanded.
```

Historical assessments should retain which Profile version shaped their discovery context.

## 28. Project Versioning

Project intent also evolves.

Example:

```text
Project Intent v1
Human capability and resilience

Project Intent v2
Human capability → adaptive behaviour → organizational resilience

Reason
R6/R8 evidence suggests mechanism clarification is needed.
```

This evolution should connect to R0–R16 and Human Decisions rather than silently replacing the old intent.

## 29. Coverage Context

The Profile/Project screen should show compact coverage context after discovery begins:

```text
Current coverage
Configured sources: 3
Healthy: 2
Degraded: 1
Project corpus: 312 works
Full text: 48% of project corpus
Last watchlist update: [...]
```

The configuration page should link to Coverage & Health for detail.

## 30. Telegram Configuration Boundary

A Profile or Project may configure whether it participates in Telegram Research Radar and which types of scientific change are relevant.

Examples:

```text
Telegram Radar
Daily digest             ON
High-value changes       ON
Coverage degradation     ON when scientifically material
Raw crawler logs         OFF
```

Telegram remains a radar, not the canonical configuration or approval surface.

## 31. Low-Fidelity Layout

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ RESEARCH PROFILE                                                           │
│ [Management / Organization Studies ▼]                                      │
├───────────────────────────────┬─────────────────────────────────────────────┤
│ PROFILE CONTEXT               │ PROJECTS                                    │
│                               │                                             │
│ Domain description            │ ● Human Capability & Resilience             │
│ [...]                         │   R0 DEVELOPING                              │
│                               │                                             │
│ Interests                     │ ○ Leadership Under Disruption               │
│ Resilience                    │   R0 NOT STARTED                            │
│ Human Behaviour               │                                             │
│ Human Capability              │ [+ Create Project]                          │
│                               │                                             │
│ Watchlists                    │ SELECTED PROJECT                            │
│ [...]                         │ Intent [...]                                │
│                               │ Provisional RQs [...]                       │
│ Seeds                         │ Focus constructs [...]                      │
│ [...]                         │                                             │
│                               │ [Open Research Journey]                     │
│ AI Suggestions [Review]       │ [Open Cockpit]                              │
└───────────────────────────────┴─────────────────────────────────────────────┘
```

## 32. Minimal Onboarding Experience

Version 0 should aim for:

`Install → Create Profile → Add Seed Papers → Configure Watchlist → Create Project → Start`

Optional information may be added later.

The HUMAN should not need to fully define theory, method, contribution, or final RQ before obtaining value from the system.

## 33. J1 Acceptance Criteria

Research Profile / Project Configuration v0 is acceptable when a HUMAN can answer:

1. What knowledge domain/context is this Profile observing?
2. What specific scientific intent belongs to this Project?
3. What is shared across Projects and what remains Project-specific?
4. What terminology/watchlists/seeds guide discovery?
5. Can AI suggest profile content while HUMAN controls acceptance?
6. Are synonyms distinguished from construct equivalence?
7. Can Profile configuration evolve with history preserved?
8. Can Project intent evolve with history preserved?
9. Can advice priorities influence attention without becoming truth thresholds?
10. Can source/add-in configuration be visible without exposing operational secrets?
11. Can Profile A and Profile B use the exact same configuration structure?
12. Can a future domain be onboarded primarily through configuration/data?
13. If not, is the difference classified through ADR-001 rather than creating an ad-hoc domain core?

## 34. J1 Boundary

This specification intentionally does not yet define:

- PostgreSQL schema;
- ontology implementation;
- profile file format;
- project file format;
- API endpoints;
- embedding strategy;
- query-generation algorithm;
- source adapter implementation;
- scoring formula;
- add-in interface;
- authentication/permissions;
- multi-user collaboration semantics.

Those belong to J2 and later stages and must be derived from the accepted HUMAN-facing configuration experience.

## 35. Pinned UX Principle Candidate

> **A research domain should enter GFPROJCLAW as a configurable knowledge context, and a research project should enter as HUMAN scientific intent. Neither should require a new research-intelligence core.**
