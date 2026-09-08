# Knowledge Evolution v0

Status: **J1 ACTIVE — Low-Fidelity UX Specification**

## 1. Purpose

Knowledge Evolution is the temporal reasoning workspace of GFPROJCLAW.

Evidence Explorer answers:

> **What evidence leads us here?**

Knowledge Evolution answers:

> **How did our understanding change over time, what caused the change, what was previously believed or assessed, and what now requires HUMAN attention?**

The governing principle is:

> **Track changes in knowledge, not just accumulate documents.**

GFPROJCLAW must preserve scientific history. New evidence may strengthen, weaken, contest, refine, possibly close, or reopen a research interpretation without erasing the previous state.

## 2. Cross-Domain Requirement

The same Knowledge Evolution experience must support both reference profiles:

- **Profile A — Computer / Information Systems:** IT Governance, e-Government / Digital Government, Enterprise Architecture.
- **Profile B — Management / Organization Studies:** Resilient Organization / Organizational Resilience, Human Behaviour, Human Capability.

Temporal reasoning is a core capability. Domain-specific content is supplied by Research Profile, Research Project, evidence and generic research objects.

If a domain requires genuinely specialized temporal analysis, ADR-001 applies; the project is not globally blocked.

## 3. Primary HUMAN Questions

Knowledge Evolution should help the HUMAN answer:

- What changed in my current understanding?
- When did it change?
- Which new or reinterpreted evidence caused it?
- What was the previous assessment?
- What is the current assessment?
- Why did the assessment change?
- Is the change strengthening, weakening, contesting, refining, possibly closing, or reopening an interpretation?
- Which research objects were affected?
- Which R0–R16 stages may need renewed attention?
- Did a previous HUMAN decision exist?
- Does new evidence challenge that previous decision?
- Is the apparent change scientific, coverage-related, or merely operational?
- Can I trace the change all the way back to papers/passages/claims?

## 4. Core Temporal Trace

The minimum reasoning chain is:

`Previous State → ChangeEvent → New/Changed Evidence → Reasoning Delta → Current State → R-Stage Impact → HUMAN Attention/Decision`

Every scientifically meaningful change should be explainable through this chain.

## 5. Screen Structure

```text
KNOWLEDGE EVOLUTION
Profile: [ ... ]   Project: [ ... ]

View: [Timeline] [Object History] [Change Map]
Filters: [Object Type] [Change Type] [R-Stage] [Human Review] [Date]

LEFT: Objects / Changes
CENTER: Temporal Timeline
RIGHT: Why It Changed / Evidence / Human Context
```

The exact visual implementation may change later. J1 requires the reasoning contract and navigation behavior.

## 6. What Can Evolve?

Knowledge Evolution should be able to represent changes to generic research objects including:

- Candidate Gap;
- Existing Solution / Solution Candidate;
- Theory;
- Model / Framework;
- Concept / Construct;
- Definition;
- Relationship;
- Mechanism;
- Mediator / Moderator;
- Boundary Condition;
- Level of Analysis;
- Method;
- Operationalization / Measurement;
- Candidate Contribution;
- Candidate Novelty assessment;
- Evidence synthesis;
- Advice assessment;
- R-stage reasoning state;
- HUMAN Decision context.

J1 does not require every object to have identical state vocabularies. It requires a common temporal/history mechanism.

## 7. Candidate Gap Evolution Vocabulary

For Candidate Gaps, the current machine-generated evolution vocabulary is:

`CANDIDATE | STRENGTHENING | WEAKENING | CONTESTED | POSSIBLY_CLOSED | REOPENED`

These are evidence-dynamics states, not scientific verdicts.

### CANDIDATE

A possible insufficiency has been identified but remains under investigation.

### STRENGTHENING

New evidence or synthesis increases support for treating the insufficiency as a meaningful candidate gap.

### WEAKENING

New evidence reduces support for the current gap formulation.

### CONTESTED

Material supporting and challenging evidence coexist, or alternative interpretations require attention.

### POSSIBLY_CLOSED

Newly discovered work may already address enough of the claimed gap that the current formulation needs substantial reconsideration.

The word **possibly** is mandatory: the machine does not scientifically close a gap.

### REOPENED

A previously weakened or possibly closed gap becomes relevant again because of new evidence, changed context, boundary conditions, contradictory findings, or a refined formulation.

## 8. ChangeEvent

A ChangeEvent is the conceptual record explaining a meaningful transition.

A HUMAN-facing ChangeEvent should expose:

```text
Change: CE-0048
Object: GAP-014
Time: [...]

Previous state: STRENGTHENING
Current state: CONTESTED

WHY?
A newly discovered prior solution overlaps with part of the proposed contribution.

EVIDENCE CHANGE
+ Paper / Claim / Evidence relationship
+ Existing Solution SOL-008

REASONING DELTA
The original gap remains plausible in one boundary condition,
but the broad formulation is no longer well supported.

AFFECTED JOURNEY
R4 R5 R6 R11 R12

COVERAGE
Full text incomplete; one relevant source degraded.

HUMAN CONTEXT
Previous decision: ACCEPT DIRECTION
Current attention: REVIEW
```

The exact database representation belongs to J2.

## 9. Meaningful Change vs Raw Activity

Knowledge Evolution should not become a crawler activity log.

Examples of raw activity that normally do **not** deserve a scientific ChangeEvent by themselves:

- paper downloaded;
- retry occurred;
- worker restarted;
- API returned HTTP 429;
- extraction job completed;
- metadata record refreshed.

These may matter operationally or for provenance, but scientific Knowledge Evolution focuses on changes such as:

- new evidence strengthens a candidate gap;
- prior solution weakens novelty potential;
- construct definition becomes contested;
- competing theory becomes plausible;
- boundary condition changes interpretation;
- new method provides an alternative design;
- evidence contradiction emerges;
- synthesis changes;
- HUMAN decision is revisited because the evidence state changed.

## 10. Scientific Change vs Coverage Change

The system must distinguish changes in scientific interpretation from changes in what the system was able to observe.

Example:

```text
Coverage Change
Semantic Scholar: HEALTHY → DEGRADED
Full-text coverage: 61% → 49%

Interpretation impact:
Novelty search coverage is now less complete.

Scientific state:
GAP-014 remains CONTESTED.
```

A source outage must not automatically become scientific evidence that a gap strengthened or weakened.

## 11. Object Timeline

The HUMAN should be able to open one research object and see its history.

Example:

```text
GAP-014 — Timeline

Sep 01  CANDIDATE
        Initial evidence synthesis identified mechanism uncertainty.

Sep 03  STRENGTHENING
        +2 supporting claims from 2 papers.

Sep 05  STRENGTHENING
        New method limitation supports unresolved empirical issue.

Sep 06  CONTESTED
        Existing Solution SOL-008 discovered.

Sep 08  CONTESTED / REFINED FORMULATION
        Boundary condition suggests broad gap should be narrowed.
        HUMAN review requested.
```

Clicking any event opens its evidence and reasoning delta.

## 12. Assessment Versioning

Advice assessments must be versioned rather than overwritten.

Illustrative example:

```text
GAP-014

Sep 03
Gap Evidence Strength       72
Novelty Potential           81
Counter-Evidence Risk       31

Sep 06
Gap Evidence Strength       74
Novelty Potential           52
Counter-Evidence Risk       68

WHY DID NOVELTY CHANGE?
Existing Solution SOL-008 was discovered and overlaps with the proposed mechanism.
```

The numbers are advice dimensions, not probabilities or scientific truth.

The important capability is explaining the delta.

## 13. Reasoning Delta

A useful Knowledge Evolution event should explain not only that a number or state changed, but **what changed in the reasoning**.

Recommended structure:

```text
BEFORE
What we believed/assessed from available evidence.

NEW INFORMATION
New paper, claim, contradiction, solution, method, theory, coverage change, or HUMAN interpretation.

AFTER
What the current synthesis/assessment now says.

WHY
Explicit explanation of the reasoning difference.

UNCERTAINTY
What remains unresolved or coverage-limited.
```

This is essential for HUMAN learning.

## 14. HUMAN Decision History

HUMAN decisions are historical scientific context and must be preserved.

Example:

```text
Sep 04
HUMAN Decision: ACCEPT DIRECTION
Rationale: Gap appears defensible given current evidence.
Evidence state: EVSET-004

Sep 08
New ChangeEvent: Existing solution discovered
System attention: Previous decision may warrant review

Current HUMAN Decision: unchanged until HUMAN acts
```

The system must never silently revise a HUMAN decision because a machine assessment changed.

Instead it surfaces:

> **New evidence may affect a previous HUMAN decision. Review recommended.**

## 15. R0–R16 Evolution

R-stage status is also temporal and non-linear.

Example:

```text
R12 Novelty Challenge

Sep 03  EVIDENCE GROWING
Sep 04  HUMAN REVIEWED
Sep 08  NEEDS ATTENTION

Reason:
A new prior solution overlaps with the candidate contribution.
```

This is not regression in a software workflow. It is normal scientific learning.

A mature research project may revisit earlier R-stages repeatedly as literature evolves.

## 16. Cross-Stage Impact

One ChangeEvent may affect several R-stages.

Example:

```text
CE-0048 — Existing solution discovered

R4 Gap Formation          → review formulation
R5 Gap Falsification      → new challenge evidence
R6 Theory Positioning     → alternative mechanism found
R11 Contribution          → contribution scope may narrow
R12 Novelty Challenge     → high attention
R16 Research Readiness    → uncertainty increased
```

These are attention impacts, not automatic workflow transitions.

## 17. Knowledge Evolution and Today / What Changed?

Today is the short attention surface. Knowledge Evolution is the historical explanation surface.

Navigation:

`Today Change Card → ChangeEvent → Object Timeline → Reasoning Delta → Evidence → R-stage/HUMAN context`

Today may say:

```text
GAP-014 novelty potential decreased 81 → 52
```

Knowledge Evolution must explain why.

## 18. Knowledge Evolution and Evidence Explorer

Knowledge Evolution never substitutes for evidence provenance.

Every evidence-driven ChangeEvent should support navigation:

`ChangeEvent → Claim/Evidence Relationship → Passage/Record → Paper/Work → Source`

Evidence Explorer provides the evidence detail; Knowledge Evolution provides the temporal reasoning context.

## 19. Knowledge Evolution and Gap–Solution Workspace

The Gap–Solution Workspace shows the current reasoning state.

Knowledge Evolution shows how that state was reached.

Example:

```text
Current Existing Solutions:
SOL-003, SOL-008, SOL-011

[View Evolution]

Sep 01: SOL-003 known
Sep 06: SOL-008 discovered → novelty assessment changed
Sep 07: SOL-011 discovered → boundary condition refined
```

## 20. Knowledge Evolution and Human Review

ChangeEvents can create HUMAN attention items when scientifically meaningful.

Examples:

- previous accepted direction challenged by new evidence;
- gap possibly closed;
- novelty overlap discovered;
- competing theory becomes materially stronger;
- construct definition becomes contested;
- method choice challenged by new methodological evidence.

The review item links to the exact ChangeEvent and evidence.

Human review does not block future crawling or unrelated knowledge evolution.

## 21. Profile A Example

Illustrative only:

```text
Object:
GAP-014 — Governance capability under digital-government disruption

Sep 01 — CANDIDATE
Evidence suggests governance capability matters, but mechanism is unclear.

Sep 04 — STRENGTHENING
Two studies report unresolved coordination/institutional limitations.

Sep 06 — CONTESTED
A prior enterprise-architecture capability model appears to address part of the mechanism.

Sep 08 — CONTESTED / formulation narrowed
New evidence suggests the unresolved issue may concern cross-agency boundary conditions rather than governance capability generally.

Affected:
R4 R5 R6 R7 R11 R12

HUMAN:
Review whether the project should narrow the gap formulation.
```

## 22. Profile B Example

Illustrative only:

```text
Object:
GAP-014 — Human capability mechanisms in organizational resilience

Sep 01 — CANDIDATE
Evidence suggests human capability may matter, but the behavioural mechanism is unclear.

Sep 04 — STRENGTHENING
Two studies indicate unresolved links between capability and adaptive behaviour.

Sep 06 — CONTESTED
An existing organizational-behaviour explanation overlaps with part of the proposed mechanism.

Sep 08 — CONTESTED / formulation narrowed
New evidence suggests the unresolved issue may concern level-of-analysis or contextual boundary conditions rather than human capability generally.

Affected:
R4 R5 R6 R8 R11 R12

HUMAN:
Review whether the mechanism and level of analysis should be reformulated.
```

Both use the same temporal reasoning mechanism.

## 23. Cross-Domain Generality Matrix

| Evolution Capability | Profile A | Profile B | Expected Resolution |
|---|---|---|---|
| Gap evolution | governance/EA gap | resilience/capability gap | Core generic |
| Theory evolution | institutional/governance lens | behavioural/capability lens | Core generic + profile content |
| Construct evolution | governance/EA constructs | human/organizational constructs | Generic research objects |
| Boundary conditions | agency/institution/system | individual/team/org/context | Generic object |
| Method evolution | IS/public-sector alternatives | management/organization alternatives | Generic method object |
| Assessment history | same mechanism | same mechanism | Core generic |
| HUMAN decision history | same mechanism | same mechanism | Core generic |
| Specialized temporal analysis | if genuinely required | if genuinely required | ADR-001 add-in candidate |

A mismatch becomes a Generality Exception, not a global stop condition.

## 24. Low-Fidelity Object History Layout

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ KNOWLEDGE EVOLUTION                                                       │
│ Profile [A/B]  Project [...]  Object [GAP-014 ▼]                          │
├─────────────────────┬─────────────────────────────┬────────────────────────┤
│ TIMELINE            │ CHANGE DETAIL               │ IMPACT / CONTEXT       │
│                     │                             │                        │
│ Sep 08 CONTESTED ●  │ Previous: STRENGTHENING     │ R4  NEEDS ATTENTION    │
│ Sep 06 SOLUTION  ●  │ Current:  CONTESTED         │ R5  NEEDS ATTENTION    │
│ Sep 04 STRENGTH. ●  │                             │ R12 NEEDS ATTENTION    │
│ Sep 01 CANDIDATE ●  │ WHY                         │                        │
│                     │ Existing solution found     │ Human decision         │
│                     │                             │ ACCEPT DIRECTION       │
│                     │ NEW EVIDENCE                │ (Sep 04)               │
│                     │ SOL-008 / CLM-142           │                        │
│                     │ [Open Evidence]             │ [Review Decision]      │
│                     │                             │                        │
│                     │ REASONING DELTA             │ Coverage               │
│                     │ Broad gap now needs         │ Full text: incomplete  │
│                     │ narrower boundary.          │                        │
└─────────────────────┴─────────────────────────────┴────────────────────────┘
```

## 25. Change Map

A later visual mode may show how one event propagates through research reasoning:

```text
New Paper
   ↓
Claim
   ↓
Existing Solution discovered
   ↓
GAP-014 CONTESTED
   ├──→ Novelty Potential ↓
   ├──→ R5 needs attention
   ├──→ R11 contribution scope questioned
   └──→ R12 novelty challenge
            ↓
       HUMAN Review
```

J1 defines the information relationship, not the final graph technology.

## 26. Dead Gap Detection

Knowledge Evolution must support the possibility that continued crawling discovers that a previously interesting gap is no longer defensible in its current form.

The system may surface:

```text
GAP-028 — POSSIBLY_CLOSED
Reason:
Three newly discovered studies directly address the previously claimed absence.

Coverage:
Broad but not exhaustive.

HUMAN action:
Review / Reformulate / Reject Candidate / Need More Evidence
```

The system does not delete the gap. Its history remains scientifically useful: it shows why the project changed direction.

## 27. Reopening Knowledge

A gap, theory interpretation, or contribution can be reopened.

Examples:

- new contradictory evidence;
- new context exposes boundary conditions;
- improved full-text access changes interpretation;
- replication fails;
- construct definition shifts;
- new method reveals prior limitation;
- HUMAN reformulates the research problem.

Knowledge therefore remains living rather than frozen.

## 28. Coverage-Aware Temporal Reasoning

Every important temporal assessment should preserve the coverage context available at that time.

A historical state should not be judged as though later sources were already available.

Example:

```text
Sep 01 assessment
Sources: OpenAlex + Crossref
Full-text coverage: 42%

Sep 08 assessment
Sources: OpenAlex + Crossref + Semantic Scholar
Full-text coverage: 61%
```

This helps explain why an assessment changed and prevents hindsight from erasing the limits of earlier knowledge.

## 29. Reproducibility

A HUMAN should eventually be able to reconstruct a historical assessment from:

- Research Profile version;
- Research Project context;
- search/discovery manifests;
- corpus/evidence state;
- claim/extraction versions;
- assessment version;
- ChangeEvents;
- HUMAN decisions.

J1 requires this traceability concept. Exact export formats belong to later stages.

## 30. Anti-Patterns

Knowledge Evolution must not become:

- a linear progress bar;
- a PASS/FAIL gate history;
- a crawler log viewer;
- a score-only chart without explanations;
- an AI-generated narrative that cannot trace to evidence;
- a system that overwrites contradictory or older assessments;
- a mechanism that automatically reverses HUMAN decisions;
- a global lock when one object becomes contested;
- a publication/Q1 probability tracker.

## 31. J1 Acceptance Criteria

Knowledge Evolution v0 is acceptable when a HUMAN can answer:

1. What changed?
2. What was the previous state?
3. What is the current state?
4. Which evidence or interpretation caused the change?
5. Why did the reasoning change?
6. What uncertainty remains?
7. Which R0–R16 stages are affected?
8. What previous HUMAN decisions exist?
9. Does new evidence suggest those decisions deserve review?
10. Can the HUMAN navigate to the exact evidence?
11. Is scientific change distinguished from coverage/operational change?
12. Are historical assessments preserved rather than overwritten?
13. Can Profile A and Profile B use the same temporal reasoning architecture?

## 32. J1 Boundary

This specification intentionally does not yet define:

- database event tables;
- event-sourcing architecture;
- temporal SQL schema;
- graph database technology;
- scoring formulas;
- change-detection algorithms;
- LLM prompts;
- notification thresholds;
- API endpoints;
- add-in contracts.

These belong to J2 and later stages and must be derived from the accepted HUMAN-facing experience.

## 33. Pinned UX Principle Candidate

> **GFPROJCLAW does not merely remember what the research currently says. It preserves how the understanding changed, which evidence changed it, what uncertainty remained at each point, and what HUMAN judgment was made in that evidence context.**
