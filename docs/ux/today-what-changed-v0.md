# Today / What Changed? v0

Status: **J1 ACTIVE — Cross-Domain Screen Specification**

## 1. Purpose

`Today / What Changed?` is the primary Research Cockpit screen for detecting meaningful change in a continuously evolving research landscape.

It must answer a HUMAN researcher's first question:

> **What changed since I last looked, why does it matter, and where should I inspect next?**

The screen must not become a document-count dashboard or infrastructure monitor.

## 2. Core UX Principle

The screen prioritizes **research-significant change**, not raw activity.

Examples of significant change:

- a candidate gap becomes better supported;
- a candidate gap becomes weaker;
- a previously claimed novelty may already have an existing solution;
- counter-evidence appears;
- a competing theory or mechanism appears;
- a new method or operationalization becomes relevant;
- a construct definition becomes contested;
- a new boundary condition appears;
- evidence coverage materially changes;
- one or more R0-R16 stages need renewed HUMAN attention.

## 3. Global Context

Every screen instance is scoped by:

```text
Research Profile
Research Project
Watchlists / Research Questions
Time window
Evidence coverage context
```

Example:

```text
PROFILE
Management / Organization Studies

PROJECT
Organizational Resilience & Human Capability

WINDOW
Since last review · 24h

COVERAGE
2 Healthy sources · 1 Degraded
```

## 4. Minimum Screen Layout

```text
┌──────────────────────────────────────────────────────────────┐
│ TODAY / WHAT CHANGED?                                       │
│ Profile: [ ... ]   Project: [ ... ]   Since: [ Last review ]│
├──────────────────────────────────────────────────────────────┤
│ RESEARCH CHANGES                                             │
│ ↑ GAP strengthened                                           │
│ ↓ GAP weakened                                               │
│ ! Possible prior solution / overlap                          │
│ ! Counter-evidence discovered                                │
│ + Competing theory / mechanism                               │
│ + Method / measurement alternative                           │
├──────────────────────────────────────────────────────────────┤
│ AFFECTED JOURNEY                                             │
│ R4 Gap Formation                                             │
│ R6 Theory Positioning                                        │
│ R9 Method Intelligence                                       │
│ R12 Novelty Challenge                                        │
├──────────────────────────────────────────────────────────────┤
│ HUMAN ATTENTION                                              │
│ 3 high attention · 5 normal                                 │
├──────────────────────────────────────────────────────────────┤
│ COVERAGE CONTEXT                                             │
│ Discovery may be incomplete due to one degraded source       │
└──────────────────────────────────────────────────────────────┘
```

## 5. Change Card Contract

Every meaningful change card must contain:

```text
CHANGE TYPE
Research object
Current state
Previous state when available
Why it changed
Evidence added / removed / contradicted
Affected R-stage(s)
Confidence / coverage context
HUMAN actions
```

Minimum HUMAN actions:

```text
[Why?]
[Evidence]
[Counter Evidence]
[Open Candidate]
[Review]
```

## 6. Example A — Computer / Information Systems

### Context

```text
Profile A
Computer / Information Systems

Watchlists
IT Governance
E-Government / Digital Government
Enterprise Architecture
```

### Example change card

```text
CHANGE
GAP-A014 — IT governance mechanisms in cross-agency digital government

STATE
STRENGTHENING

Advice
Previous: 68
Current: 77

WHY DID IT CHANGE?
+ 4 studies report coordination limitations across agencies
+ 2 studies identify governance-role ambiguity
- 1 recent study reports an effective federated mechanism

AFFECTED JOURNEY
R2 Evidence Mapping
R4 Gap Formation
R5 Gap Falsification
R6 Theory Positioning
R11 Contribution Formation
R12 Novelty Challenge

COVERAGE
3 full-text studies
3 abstract-only studies
1 metadata-only study

[Why?] [Evidence] [Counter Evidence] [Open Candidate] [Review]
```

### Example theory change

```text
CHANGE
Competing theoretical explanation discovered

OBJECT
Institutional explanation for inter-agency governance adoption

CURRENT INTERPRETATION
Current project emphasizes governance capability.
New literature suggests institutional pressure may explain part of the same phenomenon.

AFFECTS
R6 Theory Positioning
R7 Research Question
R8 Conceptualization
R11 Contribution Formation

HUMAN ATTENTION
Compare mechanism coverage before selecting theoretical direction.
```

### Example method change

```text
CHANGE
New methodological alternative

OBJECT
Enterprise Architecture capability assessment

FOUND
A longitudinal mixed-method design used to observe capability development over time.

AFFECTS
R9 Method Intelligence
R10 Research Design

SYSTEM ROLE
Surface the alternative and evidence.

HUMAN ROLE
Judge methodological fit to the research question and context.
```

## 7. Example B — Management / Organization Studies

### Context

```text
Profile B
Management / Organization Studies

Watchlists
Resilient Organization
Human Behaviour
Human Capability
```

### Example change card

```text
CHANGE
GAP-B014 — Human capability as a mechanism of organizational resilience

STATE
STRENGTHENING

Advice
Previous: 72
Current: 81

WHY DID IT CHANGE?
+ 3 studies support capability-related mechanisms
+ 1 study identifies a boundary condition
- 1 study attributes resilience primarily to structural redundancy

AFFECTED JOURNEY
R2 Evidence Mapping
R4 Gap Formation
R5 Gap Falsification
R6 Theory Positioning
R8 Conceptualization
R11 Contribution Formation
R12 Novelty Challenge

COVERAGE
4 full-text studies
1 abstract-only study

[Why?] [Evidence] [Counter Evidence] [Open Candidate] [Review]
```

### Example construct change

```text
CHANGE
Construct definition disagreement

OBJECT
Human Capability

FOUND
Three recent studies operationalize capability differently:
- individual-level adaptive capability
- team-level behavioural capability
- organization-level capability bundle

AFFECTS
R2 Evidence Mapping
R6 Theory Positioning
R8 Conceptualization
R9 Method Intelligence

RISK
Level-of-analysis mismatch may create theoretical and measurement ambiguity.
```

### Example behavioural mechanism change

```text
CHANGE
Alternative mechanism discovered

OBJECT
Relationship between human capability and organizational resilience

CURRENT MODEL
Human capability → resilience

NEW POSSIBILITY
Human capability → adaptive behaviour → resilience

AFFECTS
R6 Theory Positioning
R8 Conceptualization
R11 Contribution Formation

SYSTEM ROLE
Surface candidate mechanism with evidence links.

HUMAN ROLE
Judge whether mediation is theoretically defensible and research-worthy.
```

## 8. Cross-Domain Generality Test

The examples above deliberately use different scientific vocabulary, but the screen contract remains identical.

The same generic change structure must support:

| Generic change concept | Profile A example | Profile B example |
|---|---|---|
| Gap change | governance coordination gap | human capability mechanism gap |
| Theory change | institutional explanation | behavioural / capability explanation |
| Construct/concept issue | governance capability definition | human capability definition |
| Method change | EA longitudinal assessment | resilience mixed-method design |
| Boundary condition | agency structure | organizational context |
| Existing solution | federated governance model | known resilience intervention |
| Counter-evidence | effective governance mechanism | structural redundancy explanation |

No screen component should depend on the literal domain name.

## 9. Ranking Without Scientific Verdict

`Today` may prioritize items by an explainable review-priority function, but must not label them as scientifically true/false.

Potential dimensions:

```text
Magnitude of assessment change
Evidence strength change
Counter-evidence risk
Number of affected R-stages
Novelty threat
Theory significance
Method relevance
Coverage quality
Researcher watchlist relevance
```

Example:

```text
HIGH ATTENTION
GAP-B014: new counter-evidence affects R4, R6 and R12

NORMAL
2 additional papers support already mature synthesis
```

The prioritization determines **what HUMAN should inspect first**, not what HUMAN must believe.

## 10. Coverage and Uncertainty Contract

Each important change must be interpretable in light of evidence availability.

Example:

```text
EVIDENCE COVERAGE
FULL TEXT      42%
ABSTRACT       88%
METADATA      100%

SOURCE STATUS
OpenAlex             HEALTHY
Crossref             HEALTHY
Semantic Scholar     DEGRADED

INTERPRETATION
This change is supported by available evidence, but literature discovery may be incomplete.
```

Pinned principle:

> **Absence of discovered evidence is not evidence of absence.**

## 11. Relationship to R0-R16

A ChangeEvent may affect one or many research stages.

Example generic mapping:

```text
New paper
   ↓
New Claim / Evidence
   ↓
ChangeEvent
   ├── R2 Evidence Mapping
   ├── R4 Gap Formation
   ├── R6 Theory Positioning
   ├── R9 Method Intelligence
   └── R12 Novelty Challenge
```

The system must never treat this as a forced stage transition.

It is an **attention signal**, not a workflow gate.

## 12. HUMAN Review Flow

From any change card, HUMAN should be able to move through:

```text
What Changed?
      ↓
Why?
      ↓
Evidence
      ↓
Supporting / Challenging / Extending records
      ↓
Affected research object
      ↓
Affected R-stage
      ↓
HUMAN judgment
```

HUMAN decisions may include:

```text
Accept Current Direction
Modify
Reject Candidate
Need More Evidence
Record Researcher Note
```

## 13. Anti-Patterns

`Today / What Changed?` must not become:

- a raw feed of all newly crawled papers;
- a crawler log screen;
- a global PASS/FAIL dashboard;
- an AI-generated scientific verdict page;
- a single-score ranking of research ideas;
- a source-health page disguised as research intelligence;
- a domain-specific dashboard requiring separate implementation for Profile A and B.

## 14. Version 0 Acceptance Test

The screen passes J1 v0 when a HUMAN can use the same interaction model for both Profile A and Profile B to answer:

1. What scientifically meaningful thing changed?
2. Why did it change?
3. What evidence caused the change?
4. What evidence challenges it?
5. Which R-stage(s) may need renewed attention?
6. What uncertainty or coverage limitations apply?
7. What should I inspect next?
8. Can I trace the intelligence back to evidence without AI making the final scientific decision?

## 15. Design Consequence for J2

This J1 screen implies the need for generic relationships among concepts such as:

```text
ResearchProfile
ResearchProject
ResearchObject
Evidence
Assessment
ChangeEvent
RStageImpact
HumanDecision
CoverageContext
```

These are **J1-derived conceptual requirements only**. Their formal definition, cardinality, schema and implementation belong to J2 Research Object Model.

---

**Development checkpoint:** `Version 0 — J0 PINNED / J1 ACTIVE`  
**Cross-domain rule:** Profile A and Profile B are developed and measured simultaneously.  
**Scientific authority:** HUMAN.
