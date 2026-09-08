# Research Opportunities / Gap–Solution Workspace v0

Status: **J1 ACTIVE — Low-Fidelity UX Specification**

## 1. Purpose

The Research Opportunities / Gap–Solution Workspace is where GFPROJCLAW helps a HUMAN investigate whether an observed research insufficiency may become a defensible research opportunity.

It is not a novelty generator, automatic topic selector, publication predictor, or scientific approval engine.

Its job is to organize the reasoning chain:

`Evidence → Candidate Gap → Existing Solutions → Limitations → Alternatives → Counter-Evidence → Theory → Method → Possible Contribution → HUMAN Judgment`

A core UX rule is:

> **Existing Solutions must be examined before Novelty.**

This reduces false novelty caused by discovering a limitation while failing to discover work that already addresses it.

## 2. Cross-Domain Requirement

The same workspace must support both reference profiles without changing core UX or scientific reasoning logic.

### Profile A — Computer / Information Systems

Reference areas:
- IT Governance
- e-Government / Digital Government
- Enterprise Architecture

Illustrative project question:

> How do governance and enterprise-architecture capabilities influence the resilience of digital-government transformation under institutional and technological disruption?

### Profile B — Management / Organization Studies

Reference areas:
- Resilient Organization / Organizational Resilience
- Human Behaviour
- Human Capability

Illustrative project question:

> How do human and organizational capabilities enable resilient organizational responses under disruption, and through which behavioural mechanisms?

These examples are validation fixtures, not hardcoded topics.

## 3. Two-Level Workspace

The feature has two related screens:

1. **Research Opportunity Board** — compare and prioritize candidate opportunities.
2. **Gap–Solution Workspace** — investigate one candidate deeply.

The board supports attention allocation. The workspace supports scientific reasoning.

Neither makes the final scientific decision.

---

# 4. Research Opportunity Board

## 4.1 Primary HUMAN Questions

The board should help answer:

- What candidate research opportunities currently exist?
- Which ones changed recently?
- Which have stronger evidence for the gap?
- Which may already have solutions?
- Where is counter-evidence strongest?
- Which candidates may have theoretical significance?
- Which appear methodologically investigable?
- Which require HUMAN attention now?

## 4.2 Board Layout

```text
RESEARCH OPPORTUNITIES
Profile: [ ... ]   Project: [ ... ]

Filters: [Status] [Gap Type] [R-Stage] [Changed] [Human Review]

Candidate       Evolution       Gap Evidence   Novelty   Counter Risk   Theory Value   Method Feasibility   Attention
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
GAP-014         STRENGTHENING       81            63          48             76                70             REVIEW
GAP-021         CONTESTED           67            51          79             72                61             HIGH
GAP-028         POSSIBLY_CLOSED     42            23          88             35                74             REVIEW
```

Numbers are advice dimensions for prioritizing attention. They are not probabilities, truth scores, publication probabilities, or automatic acceptance thresholds.

## 4.3 Required Dimensions

At minimum, candidates can expose separate advice dimensions:

- **Gap Evidence Strength** — how strongly current evidence supports the claimed insufficiency.
- **Novelty Potential** — whether the proposed contribution appears distinguishable from discovered prior work.
- **Counter-Evidence Risk** — strength/relevance of evidence challenging the gap or proposed interpretation.
- **Theoretical Significance** — potential relevance to theory, mechanism, boundary conditions, constructs, relationships, or framework development.
- **Methodological Feasibility** — whether literature indicates plausible ways to investigate the question.
- **Evidence Coverage Context** — whether the assessment is based on broad or limited discovery/full-text coverage.

No single composite score is required in v0.

## 4.4 Evolution State

Machine-generated candidate evolution may use:

`CANDIDATE | STRENGTHENING | WEAKENING | CONTESTED | POSSIBLY_CLOSED | REOPENED`

This state describes current evidence dynamics, not HUMAN acceptance.

HUMAN decisions remain separate.

---

# 5. Candidate / Gap–Solution Workspace

## 5.1 Header

```text
GAP-014 — [Candidate Gap Statement]

Evolution: STRENGTHENING
Human State: NEED MORE EVIDENCE
Affected Journey: R4 R5 R6 R7 R11 R12
Last Meaningful Change: [date/event]
Coverage: [context]

[Evidence] [Counter-Evidence] [History] [Human Review]
```

The header must immediately distinguish machine assessment from HUMAN judgment.

## 5.2 Scientific Reasoning Canvas

The main screen follows this order:

```text
1. WHAT WE KNOW
        ↓
2. WHAT WE DON'T KNOW
        ↓
3. WHY IT MATTERS
        ↓
4. CANDIDATE GAP
        ↓
5. EXISTING SOLUTIONS
        ↓
6. LIMITATIONS OF EXISTING SOLUTIONS
        ↓
7. ALTERNATIVE EXPLANATIONS / COUNTER-EVIDENCE
        ↓
8. THEORY / MECHANISM OPTIONS
        ↓
9. METHOD OPTIONS
        ↓
10. POSSIBLE CONTRIBUTION
        ↓
11. NOVELTY CHALLENGE
        ↓
12. HUMAN JUDGMENT
```

The sequence is explanatory rather than a blocking workflow. HUMAN users may navigate directly to any section.

---

# 6. What We Know

Summarize established or recurring findings relevant to the candidate.

Every evidence-backed statement must be traceable through:

`Synthesis → Claim → Evidence Relationship → Passage/Record → Paper → Source`

The screen should expose supporting, challenging, extending, replicating and contradictory evidence where available.

### Profile A example

Current literature may indicate that governance mechanisms, institutional arrangements or enterprise-architecture capabilities are associated with digital-transformation outcomes under particular contexts.

### Profile B example

Current literature may indicate that adaptive capabilities, behavioural responses, leadership or organizational resources contribute to resilience under particular disruption contexts.

The system must not treat these illustrative statements as established facts without actual evidence in the active corpus.

---

# 7. What We Don't Know

This section records candidate insufficiencies rather than definitive claims of absence.

Possible forms include:

- inconsistent findings;
- under-tested relationships;
- unclear mechanisms;
- missing boundary conditions;
- limited contexts or populations;
- construct ambiguity;
- methodological limitations;
- fragmented literature;
- missing integration between scholarly conversations.

The UI should explicitly remind the HUMAN:

> **Absence of discovered evidence is not evidence of absence.**

Coverage context must therefore be visible.

---

# 8. Why It Matters

Apply the project's “So What?” reasoning:

- What do we currently know?
- What remains uncertain?
- Why does resolving that uncertainty matter?
- If investigated successfully, what might change in theory, explanation, method, policy or practice?

This section is especially important for preventing a technically detectable literature gap from automatically becoming a worthwhile research problem.

---

# 9. Candidate Gap

Gap type may include:

`EXPLICIT_GAP | EMPIRICAL_GAP | THEORETICAL_GAP | SYNTHESIS_GAP`

The candidate should include:

- concise gap statement;
- evidence basis;
- scope/context;
- assumptions;
- affected constructs/concepts/theories;
- evidence coverage;
- counter-search status;
- current evolution state;
- affected R-stages.

GFPROJCLAW labels it **Candidate Gap** until HUMAN scientific judgment establishes how it should be used in the research project.

---

# 10. Existing Solutions — Before Novelty

This is a mandatory reasoning section whenever novelty is being considered.

The system actively searches for prior work that may already address the candidate gap through:

- theories;
- models/frameworks;
- empirical studies;
- methods;
- constructs/measures;
- interventions;
- mechanisms;
- alternative research traditions;
- adjacent-domain solutions.

### Profile A example

A proposed governance–resilience relationship may already be partly addressed through digital-government capability models, IT governance mechanisms, enterprise-architecture capability literature, institutional theory, or adjacent digital-resilience research.

### Profile B example

A proposed human-capability–resilience relationship may already be partly addressed through dynamic capabilities, organizational resilience, psychological/behavioural mechanisms, human-capital perspectives or adjacent organizational-behaviour research.

These examples demonstrate the same generic operation: **find prior solutions before claiming novelty**.

---

# 11. Limitations of Existing Solutions

For each discovered solution, the workspace should ask:

- What does it actually address?
- What evidence supports it?
- In which context was it tested?
- What assumptions does it make?
- What limitations were reported?
- Which aspects of the candidate gap remain unresolved?
- Is the limitation substantive or merely contextual replication?

The HUMAN should be able to compare solutions side by side.

---

# 12. Alternative Explanations and Counter-Evidence

The workspace must actively attempt to weaken the candidate.

Potential challenges include:

- prior study already resolves the claimed gap;
- competing theory explains the phenomenon better;
- relationship is context-specific;
- construct overlaps with an established construct;
- causal interpretation exceeds evidence;
- observed inconsistency comes from measurement differences;
- claimed novelty is terminology rather than contribution;
- adjacent literature contains an overlooked solution.

This section connects directly to R5 Gap Falsification, R12 Novelty Challenge and R14 Adversarial Review.

Counter-evidence is retained, not overwritten.

---

# 13. Theory / Mechanism Options

The system may surface theory-related possibilities, but does not select the theory for the HUMAN.

It should distinguish possibilities such as:

- theory application;
- theory extension;
- theory integration;
- competing explanation;
- mechanism clarification;
- boundary-condition discovery;
- construct refinement;
- relationship refinement.

### Profile A

Potential theoretical lenses may arise from governance, institutional, capability, socio-technical or architecture-related literature.

### Profile B

Potential lenses may arise from organizational resilience, capability, behavioural, resource, leadership or organizational-theory literature.

The categories are generic; profile vocabulary and discovered theories supply domain content.

---

# 14. Method Options

Method intelligence should answer:

- How have comparable questions been investigated?
- What research designs were used?
- What samples/contexts were studied?
- How were constructs operationalized?
- What instruments/measures were used?
- What analysis techniques were used?
- What validation strategies were used?
- What methodological limitations recur?
- What alternative methods exist?

The system recommends options with evidence and limitations rather than prescribing one method.

---

# 15. Possible Contribution

Possible contribution is downstream of gap and existing-solution analysis.

The workspace may organize contribution candidates into:

- theoretical;
- empirical;
- methodological;
- synthesis/integration;
- practical/policy.

It should distinguish stronger contribution possibilities such as mechanism clarification, boundary conditions, theory integration or construct refinement from weak claims such as “this context has not been studied.”

The system outputs **Candidate Contribution**, not a declaration of novelty.

---

# 16. Novelty Challenge

Before a HUMAN treats a contribution as novel, GFPROJCLAW should expose:

- nearest prior solutions;
- conceptual overlap;
- terminology overlap;
- adjacent-domain work;
- counter-evidence;
- evidence coverage limitations;
- alternative interpretation;
- what appears genuinely different;
- what remains uncertain.

Novelty Potential is an advice dimension only.

The screen should never display statements such as:

`Novelty confirmed`

or

`Q1-ready`.

---

# 17. HUMAN Judgment

Available HUMAN actions may include:

`REVIEW | MODIFY | ACCEPT DIRECTION | REJECT CANDIDATE | NEED MORE EVIDENCE`

A decision stores:

- decision;
- rationale;
- evidence state at decision time;
- affected research objects;
- affected R-stages;
- timestamp/version.

A HUMAN decision does not freeze knowledge. New literature may reopen or weaken a previously reviewed candidate.

---

# 18. Relationship to R0–R16

A single candidate may affect multiple R-stages simultaneously.

Typical links include:

- R2 Evidence Mapping
- R3 Problem Formulation
- R4 Gap Formation
- R5 Gap Falsification
- R6 Theory Positioning
- R7 Research Question
- R8 Conceptualization
- R9 Method Intelligence
- R11 Contribution Formation
- R12 Novelty Challenge
- R13 Evidence & Argument Audit
- R14 Adversarial Review
- R15 Scholarly Positioning
- R16 Research Readiness

No stage must PASS before another can be inspected.

---

# 19. Change Intelligence

The workspace is temporal.

Example:

```text
2026-09-01  GAP-014  CANDIDATE
2026-09-04  +2 supporting claims       → STRENGTHENING
2026-09-06  existing solution found    → CONTESTED
2026-09-08  boundary condition found   → REFINED / assessment updated
```

The implementation should use the project-approved evolution vocabulary rather than inventing an automatic scientific verdict. Historical assessments remain accessible.

A change view should explain:

`Previous Assessment → New Evidence → Reasoning Change → Current Assessment → Affected R-Stages`

---

# 20. Evidence Traceability

Every important assertion or score explanation should support navigation to evidence.

Example:

```text
Novelty Potential: 63
  ↓ Why?
Three nearby solutions discovered; one overlaps strongly.
  ↓
Existing Solution SOL-008
  ↓
Claim CLM-142
  ↓
Passage / Abstract Record
  ↓
Paper
  ↓
Source + Access Level
```

Access level must remain visible:

`FULL_TEXT | ABSTRACT_ONLY | METADATA_ONLY`

Metadata-only discovery must not be presented as passage-level evidence.

---

# 21. Coverage Context

The workspace must disclose limitations such as:

- sources searched;
- source degradation;
- search freshness;
- full-text coverage;
- abstract coverage;
- metadata-only records;
- known query/profile limitations.

This prevents the system from converting incomplete discovery into false certainty.

---

# 22. Profile A / Profile B Generality Matrix

| Capability | Profile A | Profile B | Expected Resolution |
|---|---|---|---|
| Candidate gap | ITGov/eGov/EA problem | resilience/behaviour/capability problem | Core generic |
| Existing solution | governance/framework/capability solution | theory/mechanism/capability solution | Core generic |
| Construct analysis | governance/architecture constructs | behavioural/capability constructs | Core generic |
| Theory analysis | IS/governance/institutional lenses | management/OB/capability lenses | Profile content |
| Method intelligence | IS/public-sector designs | management/organization designs | Core generic + profile content |
| Counter-evidence | competing framework/explanation | competing theory/mechanism | Core generic |
| Contribution | theory/empirical/method/policy | theory/empirical/method/practice | Core generic |
| Specialized future need | domain source/notation/tool | domain instrument/analysis/tool | Add-in candidate if genuinely specialized |

Any mismatch is handled according to ADR-001:

`PROFILE_CONFIG | CORE_GENERALIZATION | ADD_IN_CANDIDATE | UNRESOLVED_GENERALITY`

It does not globally stop the project.

---

# 23. Low-Fidelity Candidate Detail Example — Profile A

```text
GAP-014 — Governance capability under digital-government disruption
Evolution: CONTESTED
Human: NEED MORE EVIDENCE
Affected: R4 R5 R6 R11 R12

WHAT WE KNOW
[Evidence-backed synthesis]

WHAT WE DON'T KNOW
[Mechanism / boundary uncertainty]

WHY IT MATTERS
[Scientific + public-sector significance]

EXISTING SOLUTIONS
SOL-003  Governance mechanism approach
SOL-008  EA capability approach
SOL-011  Adjacent digital-resilience approach

LIMITATIONS
[Context / mechanism / measurement limitations]

COUNTER-EVIDENCE
[Prior work challenging claimed gap]

THEORY OPTIONS
[Evidence-linked candidate lenses]

METHOD OPTIONS
[Comparable designs + limitations]

POSSIBLE CONTRIBUTION
[Candidate only]

NOVELTY CHALLENGE
Nearest overlap: SOL-008
Coverage limitation: full text incomplete

HUMAN DECISION
[Review] [Modify] [Accept Direction] [Reject] [Need More Evidence]
```

# 24. Low-Fidelity Candidate Detail Example — Profile B

```text
GAP-014 — Human capability mechanisms in organizational resilience
Evolution: CONTESTED
Human: NEED MORE EVIDENCE
Affected: R4 R5 R6 R8 R11 R12

WHAT WE KNOW
[Evidence-backed synthesis]

WHAT WE DON'T KNOW
[Behavioural mechanism / boundary uncertainty]

WHY IT MATTERS
[Scientific + organizational significance]

EXISTING SOLUTIONS
SOL-004  Dynamic-capability explanation
SOL-009  Behavioural mechanism approach
SOL-013  Organizational-resilience framework

LIMITATIONS
[Construct / level-of-analysis / context limitations]

COUNTER-EVIDENCE
[Prior work challenging claimed gap]

THEORY OPTIONS
[Evidence-linked candidate lenses]

METHOD OPTIONS
[Comparable designs + measures + limitations]

POSSIBLE CONTRIBUTION
[Candidate only]

NOVELTY CHALLENGE
Nearest overlap: SOL-009
Coverage limitation: some evidence abstract-only

HUMAN DECISION
[Review] [Modify] [Accept Direction] [Reject] [Need More Evidence]
```

The two screens intentionally share the same structure.

---

# 25. J1 Acceptance Criteria for This Workspace

The low-fidelity design is acceptable when a HUMAN can answer:

1. What is the candidate gap?
2. What evidence supports it?
3. What evidence challenges it?
4. What prior solutions already exist?
5. What limitations remain after considering those solutions?
6. Why might the unresolved issue matter?
7. What theory/mechanism alternatives exist?
8. How have comparable questions been investigated?
9. What contribution might be possible without declaring novelty prematurely?
10. Why did the candidate assessment change over time?
11. Which R0–R16 stages are affected?
12. What requires HUMAN judgment?
13. What is the evidence/coverage limitation?
14. Can the exact same reasoning structure support Profile A and Profile B?

## 26. J1 Boundary

This document specifies HUMAN-facing information architecture and reasoning behavior.

It intentionally does **not** yet define:

- PostgreSQL schema;
- class hierarchy;
- API endpoints;
- agent implementation;
- scoring formula;
- plugin/add-in interface;
- extraction prompts;
- queue topology.

Those must be derived later from the accepted J1 experience, especially during J2 Research Object Model and subsequent architecture stages.

## 27. Pinned UX Principle Candidate

> **A research opportunity becomes interesting only after the system shows what is known, what remains uncertain, what solutions already exist, what challenges the interpretation, why the unresolved issue matters, and what still requires HUMAN scientific judgment.**
