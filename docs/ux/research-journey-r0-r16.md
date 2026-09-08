# Research Journey R0-R16 — Screen Specification v0

Status: **J1 ACTIVE — HUMAN Research Living Lab**  
Purpose: **Center of research learning, maturity visibility, evidence traceability, and HUMAN scientific judgment**

## 1. Core Intent

The Research Journey screen is not a progress bar and not a scientific gate system.

It is a living research-lab interface that helps a HUMAN understand:

- where the research is currently developing;
- which parts have stronger or weaker evidence;
- why a stage has its current status;
- what has changed since the previous assessment;
- what risks or unresolved questions remain;
- what the HUMAN should learn, inspect, compare, challenge, or decide next.

The same journey model must work for both reference profiles:

### Profile A — Computer / Information Systems
- IT Governance
- e-Government / Digital Government
- Enterprise Architecture

### Profile B — Management / Organization Studies
- Resilient Organization / Organizational Resilience
- Human Behaviour
- Human Capability

The content differs by domain; the reasoning structure, evidence traceability, navigation, and HUMAN authority must remain the same.

---

## 2. Pinned Journey Principle

> **R0-R16 is iterative, revisable, evidence-sensitive, and HUMAN-centered. It is not a waterfall and it is not a PASS/FAIL gate chain.**

A HUMAN may inspect any stage at any time.

New evidence may strengthen, weaken, contest, reopen, or redirect one or more stages simultaneously.

Example:

```text
New paper discovered
        ↓
Challenges existing gap claim
        ↓
Affects R4 Gap Formation
Affects R5 Gap Falsification
Affects R11 Contribution Formation
Affects R12 Novelty Challenge
```

No stage is automatically locked because another stage is incomplete.

---

## 3. Screen-Level Human Questions

The Research Journey screen must allow the HUMAN to answer:

1. Where is my research currently strong, developing, uncertain, or needing attention?
2. Why does each R-stage have its current status?
3. What evidence supports or challenges that status?
4. What changed recently?
5. Which stages are connected to the same evidence or research object?
6. What should I learn or inspect next?
7. Which decisions require HUMAN judgment?
8. Has new literature changed an earlier interpretation?

---

## 4. Journey Overview Screen

### 4.1 Global Context

```text
GFPROJCLAW — RESEARCH JOURNEY

Profile:  [ Management / Organization Studies ▼ ]
Project:  [ Organizational Resilience Study ▼ ]

Research Journey: R0-R16
Last assessed: Today 06:20
Recent changes affecting journey: 6
Human attention items: 4
Coverage note: 1 source degraded
```

### 4.2 Journey Matrix

```text
R0   Research Intent               HUMAN REVIEWED        ✓
R1   Research Landscape            MATURE                ●
R2   Evidence Mapping              EVIDENCE GROWING      ●
R3   Problem Formulation           DEVELOPING            ◐
R4   Gap Formation                 NEEDS ATTENTION       !
R5   Gap Falsification             EVIDENCE GROWING      ●
R6   Theory Positioning            NEEDS ATTENTION       !
R7   Research Question             DEVELOPING            ◐
R8   Conceptualization             DEVELOPING            ◐
R9   Method Intelligence           EVIDENCE GROWING      ●
R10  Research Design               NOT STARTED           ○
R11  Contribution Formation        DEVELOPING            ◐
R12  Novelty Challenge             NEEDS ATTENTION       !
R13  Evidence & Argument Audit     NOT STARTED           ○
R14  Adversarial Review            NOT STARTED           ○
R15  Scholarly Positioning         DEVELOPING            ◐
R16  Research Readiness            DEVELOPING            ◐
```

### 4.3 Allowed Status Vocabulary

- NOT STARTED
- DEVELOPING
- EVIDENCE GROWING
- NEEDS ATTENTION
- HUMAN REVIEWED
- MATURE

The interface must not use PASS/FAIL for scientific maturity.

Statuses are reversible and versioned.

---

## 5. Status Is Not a Percentage

The system must not represent R0-R16 as:

```text
Research completion = 72%
```

This creates a false sense of linear completion.

Instead, maturity is multidimensional.

Example:

```text
R6 Theory Positioning
Status: NEEDS ATTENTION

Evidence coverage:       Moderate
Competing explanations:  High
Human review:             Pending
Recent change:            Yes
```

This tells the HUMAN why attention is needed without pretending that scientific maturity can be compressed into one progress value.

---

## 6. Persistent Stage Card Pattern

Every R-stage card uses the same minimum structure:

```text
R6 — THEORY POSITIONING

STATUS
NEEDS ATTENTION

WHY
Competing theoretical explanations remain unresolved.

EVIDENCE SNAPSHOT
23 relevant papers
12 supporting links
4 challenging links
3 boundary-condition findings
2 competing explanations

WHAT CHANGED
+1 competing theory discovered yesterday

HUMAN ATTENTION
Review theory mechanisms and boundary conditions

[Open R6]
```

The wording changes by stage, but the interaction pattern is stable.

---

## 7. R-Stage Detail Pattern

Every stage detail screen must follow:

> **STATUS → WHY → WHAT WE FOUND → EVIDENCE → LEARN → RISK → SUGGESTED ACTION → HUMAN DECISION → CHANGE HISTORY**

### 7.1 Required Sections

```text
R# — STAGE NAME

STATUS
...

WHY
...

WHAT WE FOUND
...

EVIDENCE
...

LEARN — WHY DOES THIS MATTER?
...

RISKS / UNCERTAINTY
...

SUGGESTED HUMAN ACTIONS
...

HUMAN JUDGMENT
...

CHANGE HISTORY
...
```

Every important claim in WHY or WHAT WE FOUND must be navigable to evidence where evidence exists.

---

# 8. R0 — Research Intent

## HUMAN Question

What phenomenon, problem, or purpose is this research trying to understand?

## Profile A Example

```text
Research Intent
Understand how IT governance arrangements influence the success,
accountability, and adaptability of digital-government initiatives.
```

Potential focus objects:

- governance mechanism
- decision rights
- accountability structure
- digital-government outcome
- institutional context

## Profile B Example

```text
Research Intent
Understand how human capability contributes to organizational resilience
under disruption and changing environmental conditions.
```

Potential focus objects:

- human capability
- adaptive behaviour
- organizational resilience
- disruption context
- organizational capability

## Learn

Research intent should describe the phenomenon and scientific purpose before prematurely committing to a particular theory, method, or expected result.

## HUMAN Actions

- clarify phenomenon;
- modify scope;
- record motivation;
- connect project to watchlists;
- HUMAN REVIEW intent.

---

# 9. R1 — Research Landscape

## HUMAN Question

What is already known, and what scholarly conversations exist around the research intent?

## Profile A Example

Possible landscape clusters:

```text
IT governance mechanisms
Digital-government governance
Enterprise architecture governance
Decision rights and accountability
Public-sector digital transformation
Institutional governance perspectives
```

## Profile B Example

Possible landscape clusters:

```text
Organizational resilience
Human capability
Adaptive behaviour
Dynamic capabilities
Resilience mechanisms
Individual-team-organization levels of analysis
```

## Minimum Information

- major literature clusters;
- major theories/frameworks/models;
- dominant methods;
- influential/seminal works;
- recent growth areas;
- contradictory streams;
- coverage period and source limitations.

## Learn

A landscape is more than a list of papers. HUMAN should see the structure of scholarly conversations and where perspectives converge or diverge.

---

# 10. R2 — Evidence Mapping

## HUMAN Question

What evidence exists, how strong is its traceability, and where does it conflict?

## Shared Structure

```text
Evidence Map

SUPPORTS       28
CHALLENGES      7
EXTENDS        11
CONTRADICTS     4
BOUNDARY         6
UNRESOLVED       9
```

## Profile A Example

Evidence may connect governance mechanisms with digital-government performance, alignment, accountability, or architecture outcomes.

## Profile B Example

Evidence may connect human capability with adaptive resilience, recovery, learning, behavioural adaptation, or organizational outcomes.

## Required Disclosure

Every evidence item shows access level:

- FULL TEXT
- ABSTRACT ONLY
- METADATA ONLY

## Learn

Evidence quantity and evidence quality are different. A large number of papers does not automatically make a claim well supported.

---

# 11. R3 — Problem Formulation

## HUMAN Question

What is the substantive scientific problem—not merely a topic or practical complaint?

## Profile A Example

Weak formulation:

```text
Many governments have digital-transformation problems.
```

Stronger candidate formulation:

```text
Existing governance arrangements may not sufficiently explain how
cross-agency decision rights and enterprise-architecture authority
shape adaptive digital-government execution.
```

## Profile B Example

Weak formulation:

```text
Organizations need to become more resilient.
```

Stronger candidate formulation:

```text
Existing resilience research may insufficiently explain how individual
and collective human capabilities translate into adaptive organizational
responses under prolonged disruption.
```

## Learn

A research problem must become scientifically examinable and evidence-grounded, not remain a broad practical concern.

---

# 12. R4 — Gap Formation

## HUMAN Question

What is insufficiently known, explained, tested, integrated, or synthesized?

## Gap Types

- EXPLICIT_GAP
- EMPIRICAL_GAP
- THEORETICAL_GAP
- SYNTHESIS_GAP

## Profile A Example

```text
Candidate Gap
Current IT-governance literature may insufficiently explain how
enterprise-architecture decision rights operate across institutional
boundaries in digital-government ecosystems.
```

## Profile B Example

```text
Candidate Gap
Current organizational-resilience literature may insufficiently explain
the mechanism through which human capability becomes collective adaptive
capacity during prolonged disruption.
```

## Minimum Evidence

The screen must distinguish:

```text
What We Know
What We Don't Know
Existing Explanations
Existing Solutions
Contradictory Evidence
Coverage Limits
```

## Learn

A gap is not simply “few papers exist.” It is a defensible insufficiency in knowledge.

---

# 13. R5 — Gap Falsification

## HUMAN Question

Does the candidate gap survive deliberate attempts to disprove it?

## Shared Falsification Search

```text
Search for:
- prior solutions
- adjacent terminology
- earlier theoretical explanations
- equivalent constructs
- counter-evidence
- overlooked review papers
- newer studies that may close the gap
```

## Profile A Example

A supposed gap in IT-governance decision rights may already be addressed in public-administration, enterprise-architecture, or digital-ecosystem literature under different terminology.

## Profile B Example

A supposed human-capability gap may already be addressed through dynamic capabilities, adaptive capacity, behavioural resilience, or multilevel resilience research.

## Candidate States

- CANDIDATE
- STRENGTHENING
- WEAKENING
- CONTESTED
- POSSIBLY_CLOSED
- REOPENED

## Learn

Falsification protects the HUMAN from building novelty claims on missing terminology rather than missing knowledge.

---

# 14. R6 — Theory Positioning

## HUMAN Question

Which theory, framework, or explanatory mechanism best helps explain the research problem, and what are its boundaries?

## Profile A Example

Possible lenses might include:

```text
IT governance frameworks
Institutional theory
Resource dependence
Agency perspectives
Enterprise architecture governance models
Public-value or digital-government perspectives
```

The system must not choose one automatically.

## Profile B Example

Possible lenses might include:

```text
Dynamic capabilities
Organizational resilience perspectives
Resource-based perspectives
Behavioural theory
Social-cognitive mechanisms
Human-capital perspectives
```

## Minimum Information

For each theoretical candidate:

```text
Theory / Framework
Mechanism
What it explains
What it does not explain
Supporting evidence
Challenging evidence
Boundary conditions
Competing explanations
Potential contribution type
```

## Learn

Theory selection should be based on explanatory fit and potential contribution, not popularity alone.

---

# 15. R7 — Research Question

## HUMAN Question

Does the RQ logically follow from the research problem, evidence, gap, and theory positioning?

## Profile A Example

```text
How do cross-agency IT-governance decision rights and enterprise-
architecture authority influence adaptive digital-government execution?
```

## Profile B Example

```text
How does human capability translate into collective adaptive capacity
that supports organizational resilience during prolonged disruption?
```

## Alignment View

```text
Problem
  ↓
Gap
  ↓
Theory / Mechanism
  ↓
Research Question
```

The system flags misalignment but does not rewrite the RQ as scientific authority.

---

# 16. R8 — Conceptualization

## HUMAN Question

What concepts, constructs, relationships, mechanisms, mediators, moderators, and levels of analysis are involved?

## Profile A Example

```text
Decision Rights
      ↓
Governance Coordination
      ↓
Adaptive Digital Execution

Moderator:
Institutional Complexity
```

## Profile B Example

```text
Human Capability
      ↓
Adaptive Behaviour
      ↓
Organizational Resilience

Possible mediator:
Collective Adaptive Capacity

Possible moderator:
Environmental Turbulence
```

## Learn

Conceptualization makes assumptions explicit and helps prevent vague constructs or hidden causal claims.

---

# 17. R9 — Method Intelligence

## HUMAN Question

How have comparable studies investigated the phenomenon, and what methodological alternatives exist?

## Shared Minimum Information

```text
Research design
Context
Sample / unit of analysis
Operationalization
Measurement instrument
Data collection
Analysis method
Validation
Reported limitations
Alternative approaches
```

## Profile A Example

Possible observed methods:

- case study;
- survey;
- archival/public-sector data;
- process study;
- design science;
- mixed methods.

## Profile B Example

Possible observed methods:

- survey;
- longitudinal study;
- multilevel modelling;
- SEM;
- qualitative case study;
- mixed methods;
- behavioural measurement.

## Learn

Method intelligence describes how the literature has studied the problem; it does not automatically prescribe one method.

---

# 18. R10 — Research Design

## HUMAN Question

What research design can defensibly answer the RQ while respecting the theory, constructs, context, and evidence limitations?

## Alignment Pattern

```text
RQ
 ↓
Required Evidence
 ↓
Unit of Analysis
 ↓
Data
 ↓
Method
 ↓
Validity / Limitations
```

## Cross-Domain Rule

The core screen remains identical; domain configuration determines which design alternatives and methodological concerns are relevant.

---

# 19. R11 — Contribution Formation

## HUMAN Question

If the study succeeds, what changes in knowledge, explanation, method, policy, or practice?

## Contribution Types

- theoretical extension;
- theory integration;
- boundary condition;
- mechanism clarification;
- construct refinement;
- empirical contribution;
- methodological contribution;
- practical/policy contribution.

## Profile A Example

Potential contribution:

```text
Clarify how enterprise-architecture authority functions as an IT-governance
mechanism across inter-organizational digital-government arrangements.
```

## Profile B Example

Potential contribution:

```text
Clarify the mechanism through which human capability becomes collective
adaptive capacity under sustained organizational disruption.
```

## So-What Test

```text
What do we know?
What don't we know?
Why does knowing it matter?
If the study succeeds, what changes?
```

---

# 20. R12 — Novelty Challenge

## HUMAN Question

Is the proposed contribution meaningfully distinct from what already exists?

## Required Order

```text
Existing Solutions
        ↓
Existing Contributions
        ↓
Overlap
        ↓
Differences
        ↓
Counter-Evidence
        ↓
Candidate Novelty
```

Existing solutions must be shown before novelty advice.

## Profile A Example

The system may find a governance model already addressing similar decision-right structures under another digital-government term.

## Profile B Example

The system may find a resilience mechanism already modelled as adaptive capacity rather than human capability.

## Learn

Novelty is not novelty because the terminology differs.

---

# 21. R13 — Evidence & Argument Audit

## HUMAN Question

Do the important claims in the research argument have appropriate and traceable evidence?

## Audit Signals

- citation does not support claim;
- causal overreach;
- stale evidence;
- abstract-only evidence being treated as full-text evidence;
- one-school bias;
- ignored counter-evidence;
- unsupported generalization;
- construct-definition mismatch.

## Shared Trace

```text
Research Claim
      ↓
Citation
      ↓
Source Record / Passage
      ↓
Extracted Claim
      ↓
Evidence Relationship
```

---

# 22. R14 — Adversarial Review

## HUMAN Question

What are the strongest reasons a critical reviewer could reject the argument?

## Critic Tasks

```text
Attack the gap
Attack novelty
Find prior solutions
Find competing theories
Question construct distinctions
Question causal interpretation
Question method fit
Find boundary conditions
Find contradictory evidence
```

## Profile A Example

Reviewer challenge:

```text
Is this really an IT-governance contribution, or merely an application
of established governance principles to a digital-government context?
```

## Profile B Example

Reviewer challenge:

```text
Is human capability distinct from existing adaptive-capacity or dynamic-
capability constructs, or is the proposed contribution construct relabelling?
```

---

# 23. R15 — Scholarly Positioning

## HUMAN Question

Which scholarly conversation is this research contributing to, and what kind of conversation is it entering?

## Profile A Example

Possible conversations:

- IT governance;
- digital government;
- enterprise architecture;
- public-sector digital transformation;
- information-systems governance.

## Profile B Example

Possible conversations:

- organizational resilience;
- human capability;
- organizational behaviour;
- dynamic capabilities;
- crisis/adaptation research.

## Minimum Information

- relevant conversations;
- theoretical lenses;
- contribution types;
- common methods;
- journals/outlets where the conversation appears;
- positioning risks.

This supports scholarly positioning, not publication gaming or acceptance prediction.

---

# 24. R16 — Research Readiness

## HUMAN Question

What is strong, uncertain, contested, incomplete, or awaiting HUMAN judgment across the integrated research argument?

## Example Readiness View

```text
RESEARCH READINESS

Strong / Mature
R1  Research Landscape
R2  Evidence Mapping

Developing
R3  Problem Formulation
R7  Research Question
R8  Conceptualization
R11 Contribution Formation

Needs Attention
R4  Gap Formation
R6  Theory Positioning
R12 Novelty Challenge

Not Yet Assessed
R13 Evidence & Argument Audit
R14 Adversarial Review
```

The screen must never display:

```text
Q1 readiness = 84%
Publication probability = 78%
```

Instead it explains strengths, uncertainties, evidence state, and unresolved HUMAN decisions.

---

# 25. Cross-Stage Relationship View

A research object may affect multiple stages.

Example Profile A:

```text
Enterprise Architecture Decision Rights
        ├── R3 Problem Formulation
        ├── R4 Gap Formation
        ├── R6 Theory Positioning
        ├── R8 Conceptualization
        └── R11 Contribution Formation
```

Example Profile B:

```text
Collective Adaptive Capacity
        ├── R4 Gap Formation
        ├── R6 Theory Positioning
        ├── R8 Conceptualization
        ├── R11 Contribution Formation
        └── R12 Novelty Challenge
```

This prevents R0-R16 from becoming isolated boxes.

---

# 26. Change Sensitivity

Each R-stage must expose recent knowledge changes.

Example:

```text
R12 — NOVELTY CHALLENGE
NEEDS ATTENTION

What changed?
A 2026 paper proposes a construct overlapping the current contribution.

Previous assessment
Novelty Potential: 81

Current assessment
Novelty Potential: 58

Why?
Substantial overlap found in mechanism and operationalization.

[Inspect Paper]
[Compare Constructs]
[Review Existing Solution]
[Record Human Judgment]
```

The previous assessment is retained.

---

# 27. Evidence Traceability From Journey

Every material stage-level statement should support navigation such as:

```text
R6 NEEDS ATTENTION
      ↓
WHY: competing theory discovered
      ↓
Theory B
      ↓
Claim
      ↓
Evidence Link
      ↓
Paper
      ↓
Passage / Record
```

Pinned rule:

> **Every important status must be explainable by navigation.**

---

# 28. Human Decision Model in the Journey

The system suggests attention; the HUMAN decides scientific direction.

Minimum actions:

- ACCEPT CURRENT DIRECTION
- MODIFY
- NEED MORE EVIDENCE
- REJECT CANDIDATE
- RECORD RESEARCHER NOTE

A HUMAN decision records:

```text
Decision
Rationale
Research stage
Affected research object(s)
Evidence state at decision time
Timestamp/version
```

The decision does not freeze future literature discovery.

---

# 29. Learning Layer

The Research Journey is also a learning environment.

Every stage includes a concise **LEARN — WHY DOES THIS MATTER?** panel.

The learning panel must explain the reasoning purpose of the stage, not provide a rigid recipe.

Example:

```text
R5 — GAP FALSIFICATION

LEARN
A candidate gap becomes more defensible when the researcher actively
searches for prior solutions, adjacent terminology, contradictory findings,
and theoretical explanations that could make the proposed gap disappear.
```

This learning layer is shared across profiles while examples can be profile-specific.

---

# 30. Profile A / Profile B Side-by-Side Validation

Each stage should be testable with the same UI pattern.

| Stage | Profile A — Computer / IS | Profile B — Management | Same Core UI? |
|---|---|---|---|
| R0 | ITGov/eGov/EA research intent | Resilience/human capability intent | Yes |
| R1 | governance/EA/digital-government landscape | resilience/behaviour/capability landscape | Yes |
| R2 | governance evidence links | capability/resilience evidence links | Yes |
| R3 | governance problem | resilience/capability problem | Yes |
| R4 | ITGov/EA gap | human capability/resilience gap | Yes |
| R5 | search prior governance solutions | search adjacent capability/resilience solutions | Yes |
| R6 | governance/institutional/EA lenses | dynamic capability/behaviour/resilience lenses | Yes |
| R7 | digital-governance RQ | resilience/human-capability RQ | Yes |
| R8 | governance constructs/mechanisms | behaviour/capability constructs/mechanisms | Yes |
| R9 | IS/public-sector methods | management/behaviour methods | Yes |
| R10 | defensible IS design | defensible management design | Yes |
| R11 | governance/EA contribution | resilience/capability contribution | Yes |
| R12 | prior governance solution overlap | prior construct/mechanism overlap | Yes |
| R13 | claim-evidence audit | claim-evidence audit | Yes |
| R14 | adversarial IS reviewer | adversarial management reviewer | Yes |
| R15 | IS/digital-government conversation | organization/management conversation | Yes |
| R16 | integrated readiness | integrated readiness | Yes |

Any future `No` in the final column requires a generality review.

---

# 31. Minimum Data Visible Per Stage

Without defining the J2 schema yet, every R-stage needs enough information to display:

```text
Stage identity
Current status
Why the status exists
Research objects involved
Evidence supporting/challenging the assessment
Coverage/access limitations
Recent changes
Risks/uncertainties
Suggested HUMAN actions
Human decisions/notes
Assessment history
```

These are UX requirements, not yet database tables.

---

# 32. Navigation Behaviour

From the Journey overview the HUMAN must be able to navigate:

```text
Journey
  ↓
R-stage
  ↓
Research object
  ↓
Evidence / contradiction / alternative
  ↓
Paper / passage
  ↓
Back to stage with context preserved
```

From any candidate gap, theory, method, construct, or contribution workspace, the HUMAN should also see which R-stages it currently affects.

---

# 33. What the Journey Must Not Become

The Research Journey must not become:

- a sequential approval workflow;
- a publication probability calculator;
- a Q1 score;
- a checklist that rewards superficial completion;
- a hidden AI scientific-decision engine;
- a domain-specific workflow requiring separate code for Profile A and B;
- a dashboard of infrastructure failures;
- a place where old assessments are overwritten without history.

---

# 34. J1 Acceptance Criteria for the R0-R16 Screen

The screen is ready to be pinned when a HUMAN can:

1. see all R0-R16 stages without interpreting them as a linear gate;
2. understand the current status and WHY for every active stage;
3. trace meaningful status statements to evidence;
4. see how new literature changed one or more stages;
5. inspect contradictions and alternative explanations;
6. learn why each research stage matters;
7. record HUMAN scientific judgment without blocking continued crawling;
8. navigate from stage → research object → evidence → source;
9. use exactly the same UX for Profile A and Profile B;
10. understand coverage limitations and uncertainty.

Cross-domain acceptance criterion:

> **Profile A and Profile B must complete the same R0-R16 journey through configuration and research content, not through different core implementations.**

---

# 35. J1 Design Outcome

The R0-R16 screen establishes the HUMAN-centered reasoning backbone of GFPROJCLAW:

```text
Research Profile
       ↓
Research Project
       ↓
R0-R16 Living Research Journey
       ↕
Research Objects
       ↕
Evidence
       ↕
Knowledge Change
       ↕
Human Judgment
```

This structure should become one of the primary inputs to J2 Research Object Model, but J1 intentionally stops before defining database schema or implementation classes.

---

**Current project state:** `Version 0 — J0 PINNED / J1 ACTIVE`  
**Document role:** Living UX specification for the HUMAN Research Journey.  
**Scientific authority:** HUMAN.  
**Generality benchmark:** Profile A + Profile B simultaneously.
