# Human Review v0

Status: **J1 ACTIVE — Low-Fidelity UX Specification**

## 1. Purpose

Human Review is the scientific judgment workspace of GFPROJCLAW.

All upstream intelligence — literature discovery, evidence extraction, gap analysis, existing-solution search, theory and method intelligence, advice assessments, falsification, adversarial review, and knowledge evolution — ultimately supports HUMAN reasoning rather than replacing it.

The governing principle is:

> **AI provides evidence, alternatives, challenges, explanations, and advice. HUMAN retains scientific authority.**

Human Review is therefore not an approval gate for system operation. It is a structured place for the researcher to inspect scientifically meaningful attention items and record reasoned judgments in their evidence context.

## 2. What Human Review Is Not

Human Review must not become:

- a global research gate;
- a queue that crawling must wait for;
- an engineering-recovery authorization system;
- a PASS/FAIL workflow;
- a mechanism where AI scores determine HUMAN choices;
- an automatic paper/topic acceptance process;
- a publication or Q1-readiness approval mechanism;
- a requirement to review every machine extraction before unrelated research continues.

Scientific review and operational continuity are separate concerns.

## 3. Cross-Domain Requirement

The same Human Review experience must support both reference profiles:

- **Profile A — Computer / Information Systems:** IT Governance, e-Government / Digital Government, Enterprise Architecture.
- **Profile B — Management / Organization Studies:** Resilient Organization / Organizational Resilience, Human Behaviour, Human Capability.

The review mechanics are generic. Domain vocabulary and scientific substance come from the Research Profile, Research Project, research objects, and evidence.

Any genuinely specialized review capability follows ADR-001 and does not globally stop development.

## 4. Primary HUMAN Questions

The workspace should help answer:

- What currently needs my scientific attention?
- Why does it need attention?
- What changed?
- What evidence supports the current interpretation?
- What evidence challenges it?
- What alternatives exist?
- What is uncertain or coverage-limited?
- Which R0–R16 stages are affected?
- What did I decide previously?
- Has new evidence materially changed the context of that decision?
- What should I inspect before making a judgment?
- Can I record my reasoning without freezing future discovery?

## 5. Review Queue Philosophy

The queue contains **scientific attention items**, not generic AI errors or raw system incidents.

Examples include:

- candidate gap weakened by new evidence;
- candidate gap possibly closed by existing solutions;
- novelty overlap discovered;
- competing theory or mechanism identified;
- construct definition contested;
- level-of-analysis mismatch;
- methodological alternative discovered;
- claim–evidence mismatch suspected;
- synthesis has material counter-evidence;
- previous HUMAN decision may deserve reconsideration after a ChangeEvent;
- R-stage reasoning state requires HUMAN interpretation.

Operational issues belong primarily in Coverage & Health unless they materially alter scientific coverage or confidence context.

## 6. Queue Layout

```text
HUMAN REVIEW
Profile: [ ... ]   Project: [ ... ]

Filters: [Attention Type] [R-Stage] [Research Object] [Changed] [Decision State]
Sort: [Research Significance] [Recent Change] [Counter Risk] [Oldest]

ATTENTION ITEM                                  WHY                         R-STAGE       HUMAN STATE
─────────────────────────────────────────────────────────────────────────────────────────────────
GAP-014 — Existing solution overlap             Novelty may be narrower     R5 R11 R12    NEED REVIEW
THEORY-006 — Competing explanation              New contradictory evidence R6 R14        NEED REVIEW
CLM-204 — Evidence provenance uncertain         Claim may be unsupported    R2 R13        NEED REVIEW
METHOD-012 — Alternative design discovered      Better alignment possible  R9 R10        NOT REVIEWED
```

Ranking prioritizes attention; it does not determine scientific truth.

## 7. Attention Item Contract

Every review item should answer:

```text
WHAT NEEDS ATTENTION?
[research object / decision / claim]

WHY NOW?
[meaningful change or unresolved scientific issue]

WHAT CHANGED?
[previous → current]

SUPPORTING EVIDENCE
[evidence-linked claims]

CHALLENGING / COUNTER-EVIDENCE
[evidence-linked claims]

ALTERNATIVES
[theory / method / formulation / solution alternatives]

COVERAGE & UNCERTAINTY
[access/source/search limitations]

AFFECTED R-STAGES
[R...]

PREVIOUS HUMAN JUDGMENT
[if any]

SUGGESTED HUMAN ACTIONS
[non-binding]
```

No important review item should exist as an unexplained alert.

## 8. HUMAN Decision Vocabulary

For v0, the primary HUMAN actions are:

`REVIEW | MODIFY | ACCEPT DIRECTION | REJECT CANDIDATE | NEED MORE EVIDENCE`

These labels describe researcher's current judgment, not universal scientific truth.

### REVIEW

The HUMAN has inspected the item but may not yet commit to a substantive direction.

### MODIFY

The HUMAN chooses to revise a gap, claim, RQ, conceptualization, theory positioning, method direction, contribution, or other research object.

### ACCEPT DIRECTION

The HUMAN judges that the current direction is sufficiently defensible to continue developing, given the current evidence context.

This does **not** mean “scientifically proven,” “novelty confirmed,” or “publication ready.”

### REJECT CANDIDATE

The HUMAN decides not to pursue the candidate in its current role/formulation.

The object and its history remain preserved.

### NEED MORE EVIDENCE

The HUMAN explicitly records that the current evidence is insufficient for a stronger judgment.

This may inform future search prioritization but must not globally block unrelated crawling.

## 9. Decision Record

A HUMAN judgment should preserve its scientific context.

Conceptually:

```text
Human Decision: HD-0031
Researcher: [actor]
Time: [...]
Decision: ACCEPT DIRECTION

Object:
GAP-014

Rationale:
The narrower gap remains plausible after considering the newly discovered prior solution.

Evidence State:
[version/reference to evidence context]

Known Counter-Evidence:
[references]

Coverage Context:
Full text incomplete; one source degraded.

Affected R-Stages:
R4 R5 R11 R12
```

J2 will determine exact data structures.

## 10. Rationale Is First-Class

The system should encourage a HUMAN to record **why** a decision was made.

A decision without rationale may still be stored, but the UX should make clear that rationale improves future understanding, reproducibility, and learning.

The rationale is a HUMAN interpretation and should be distinguishable from machine-generated summaries.

## 11. Evidence Snapshot / Evidence Context

A decision must be interpretable relative to what evidence was available when it was made.

If a HUMAN selects `ACCEPT DIRECTION` on September 4 and new literature appears on September 8, the September 4 judgment must remain historically understandable.

Therefore Human Review conceptually links decisions to:

- relevant research objects;
- evidence/claim state;
- known counter-evidence;
- assessment version;
- coverage context;
- R-stage context;
- time/version.

This supports the principle that historical assessments and decisions are not overwritten.

## 12. New Evidence Does Not Auto-Reverse HUMAN Decisions

Example:

```text
Sep 04
HUMAN: ACCEPT DIRECTION
GAP-014

Sep 08
NEW EVIDENCE:
Existing Solution SOL-008 overlaps with the proposed contribution.

SYSTEM:
Previous HUMAN decision may warrant review.

CURRENT HUMAN DECISION:
Still ACCEPT DIRECTION until HUMAN changes it.
```

The system may recommend review but may not silently convert the decision to REJECT or MODIFY.

## 13. Review Detail — Three-Panel Model

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ HUMAN REVIEW                                                               │
│ Profile [A/B]  Project [...]                                                │
├──────────────────┬──────────────────────────────────┬───────────────────────┤
│ REVIEW QUEUE     │ SCIENTIFIC CONTEXT               │ HUMAN JUDGMENT        │
│                  │                                  │                       │
│ GAP-014 ●        │ WHY NOW                          │ Previous decision     │
│ THEORY-006       │ Existing solution found          │ ACCEPT DIRECTION      │
│ CLM-204          │                                  │ Sep 04                │
│ METHOD-012       │ WHAT CHANGED                     │                       │
│                  │ Novelty 81 → 52                  │ Current judgment      │
│                  │                                  │ [Review ▼]            │
│                  │ SUPPORTING EVIDENCE              │                       │
│                  │ [3 papers]                       │ Rationale             │
│                  │                                  │ [..................]  │
│                  │ COUNTER-EVIDENCE                 │                       │
│                  │ [2 papers]                       │ [Record Judgment]     │
│                  │                                  │                       │
│                  │ ALTERNATIVES                     │                       │
│                  │ [Open Gap Workspace]             │                       │
│                  │ [Open Evidence]                  │                       │
└──────────────────┴──────────────────────────────────┴───────────────────────┘
```

## 14. Review Should Support Inspection, Not Force Immediate Choice

A HUMAN may need to navigate away from the review item to inspect:

- Evidence Explorer;
- Gap–Solution Workspace;
- Knowledge Evolution;
- relevant R-stage;
- paper/work detail;
- competing theory;
- method alternatives;
- previous decisions.

The review context should remain recoverable when the HUMAN returns.

The UX should not force a premature binary answer merely to clear a queue.

## 15. Review and R0–R16

Human Review is integrated with the living research journey.

Examples:

```text
R4 Gap Formation
Status: NEEDS ATTENTION
Reason: prior solution discovered
→ Open Human Review
```

```text
R6 Theory Positioning
Status: EVIDENCE GROWING
Reason: competing theoretical explanation discovered
→ Review alternatives
```

```text
R13 Evidence & Argument Audit
Status: NEEDS ATTENTION
Reason: claim appears stronger than supporting passage
→ Review claim/evidence
```

R-stage status and HUMAN Decision remain distinct.

## 16. Review and Today / What Changed?

Today identifies changes requiring attention.

Navigation:

`Today → ChangeEvent → Human Review → Evidence / Workspace → HUMAN Judgment`

Example Today card:

```text
NOVELTY CHALLENGE
GAP-014
Existing solution discovered.
R12 may need attention.

[Review]
```

The HUMAN should arrive in review with the change context already visible.

## 17. Review and Evidence Explorer

Every evidence-related review must support traceability to:

`Paper/Work → Passage/Record → Claim → Evidence Relationship`

Examples:

- unsupported claim;
- ambiguous passage;
- abstract-only evidence being overinterpreted;
- contradictory studies;
- context mismatch;
- extraction needing HUMAN correction.

Human Review should not duplicate Evidence Explorer. It should deep-link to the evidence while preserving the decision context.

## 18. Review and Knowledge Evolution

Human Review should show relevant historical context:

```text
Previous Assessment
GAP-014: STRENGTHENING

ChangeEvent
SOL-008 discovered

Current Assessment
GAP-014: CONTESTED

Previous HUMAN Decision
ACCEPT DIRECTION

Question for HUMAN
Does the narrower formulation remain defensible?
```

This makes review an evidence-aware reasoning activity rather than an isolated approval click.

## 19. Review and Gap–Solution Workspace

For gap/novelty review, the HUMAN should be able to inspect the full reasoning canvas:

`What We Know → What We Don't Know → Why It Matters → Gap → Existing Solutions → Limitations → Alternatives/Counter-Evidence → Theory → Method → Possible Contribution → Novelty Challenge`

Human Review records the judgment after or during that investigation.

## 20. Scientific Attention vs Engineering Attention

A strict separation is required.

### Scientific attention

Examples:

- Is this gap still defensible?
- Does this paper actually challenge the mechanism?
- Is this construct distinct?
- Which theory is more appropriate?
- Does the method align with the RQ?
- Is the contribution meaningful?

These belong in Human Review.

### Engineering/operational attention

Examples:

- worker crashed;
- API rate-limited;
- retry exhausted;
- source temporarily unavailable;
- parser failed.

These belong in operational observability/Coverage & Health, except where their consequence materially changes scientific coverage context.

Engineering recovery must not require scientific authorization.

## 21. Non-Blocking Review Principle

> **Unreviewed scientific attention does not stop future literature discovery, evidence ingestion, or unrelated analysis.**

Examples:

- GAP-014 can await HUMAN review while new papers continue to be discovered;
- THEORY-006 can remain contested while method intelligence continues;
- one quarantined claim does not stop healthy claims;
- R12 may need attention while R9 continues to evolve.

This directly implements the project's no-global-lock principle.

## 22. Review Prioritization

The system may rank review items using explainable advice dimensions such as:

- magnitude of assessment change;
- strength of new counter-evidence;
- novelty threat;
- theoretical significance;
- number/importance of affected R-stages;
- relevance to active RQs/watchlists;
- coverage quality;
- age of unresolved item;
- relationship to previous HUMAN decisions.

Prioritization answers **what may deserve attention first**, not **what the HUMAN must decide**.

No score threshold may automatically force ACCEPT/REJECT.

## 23. Suggested Human Actions

The system may suggest next actions such as:

- inspect nearest prior solution;
- compare competing theories;
- narrow gap scope;
- inspect full-text evidence;
- search for additional counter-evidence;
- verify construct definition;
- examine level-of-analysis mismatch;
- compare alternative methods;
- revisit contribution statement.

Suggestions must explain why they are relevant.

They are non-binding.

## 24. Learning Layer

Human Review is also part of the Research Living Lab.

Each review item may explain why the issue matters scientifically.

Example:

```text
WHY THIS MATTERS
A gap should survive reasonable attempts to find prior solutions.
Discovering overlap does not automatically destroy the research opportunity;
it may indicate that the gap needs a narrower mechanism, context, or boundary condition.
```

For a theory review:

```text
WHY THIS MATTERS
Competing explanations help distinguish whether the proposed contribution extends theory,
merely changes terminology, or requires a different mechanism.
```

The learning layer should teach reasoning principles, not prescribe a rigid research recipe.

## 25. Profile A Example

```text
REVIEW ITEM
GAP-014 — Governance capability under digital-government disruption

WHY NOW
An enterprise-architecture capability study appears to address part of the proposed mechanism.

CURRENT MACHINE ASSESSMENT
Gap: CONTESTED
Novelty Potential: decreased

SUPPORTING EVIDENCE
Studies indicating unresolved cross-agency governance limitations.

CHALLENGING EVIDENCE
SOL-008 / CLM-142 suggests an existing capability mechanism.

ALTERNATIVE INTERPRETATION
The opportunity may concern cross-agency institutional boundary conditions rather than governance capability generally.

AFFECTED
R4 R5 R6 R7 R11 R12

HUMAN OPTIONS
REVIEW / MODIFY / ACCEPT DIRECTION / REJECT CANDIDATE / NEED MORE EVIDENCE
```

## 26. Profile B Example

```text
REVIEW ITEM
GAP-014 — Human capability mechanisms in organizational resilience

WHY NOW
An organizational-behaviour study appears to explain part of the proposed mechanism using an established construct.

CURRENT MACHINE ASSESSMENT
Gap: CONTESTED
Novelty Potential: decreased

SUPPORTING EVIDENCE
Studies indicating unresolved links between capability and adaptive behaviour.

CHALLENGING EVIDENCE
SOL-009 / CLM-142 suggests an overlapping behavioural mechanism.

ALTERNATIVE INTERPRETATION
The opportunity may concern level-of-analysis or boundary conditions rather than human capability generally.

AFFECTED
R4 R5 R6 R8 R11 R12

HUMAN OPTIONS
REVIEW / MODIFY / ACCEPT DIRECTION / REJECT CANDIDATE / NEED MORE EVIDENCE
```

The review mechanics remain identical across profiles.

## 27. Cross-Domain Generality Matrix

| Review Capability | Profile A | Profile B | Expected Resolution |
|---|---|---|---|
| Gap review | governance/EA gap | resilience/capability gap | Core generic |
| Evidence review | IS/public-sector evidence | management/organization evidence | Core generic |
| Theory review | governance/institutional lenses | behavioural/capability lenses | Core generic + profile content |
| Construct review | governance/EA constructs | human/organizational constructs | Generic objects |
| Method review | IS/public-sector methods | management/organization methods | Generic method objects |
| Decision history | same mechanism | same mechanism | Core generic |
| Learning layer | same reasoning principles | same reasoning principles | Core generic + profile examples |
| Specialized review | if genuinely needed | if genuinely needed | ADR-001 extension/add-in |

A mismatch is a Generality Exception, not a project stop condition.

## 28. Decision Change / Supersession

A later HUMAN judgment may supersede an earlier judgment, but the earlier decision remains visible.

Example:

```text
HD-0031 — Sep 04
ACCEPT DIRECTION

HD-0042 — Sep 10
MODIFY
Supersedes HD-0031
Reason: new evidence shows strong overlap with prior solution.
```

This preserves the evolution of HUMAN reasoning.

The system should not rewrite HD-0031 as though the HUMAN had always chosen MODIFY.

## 29. Feedback Loop Without Truth Learning

HUMAN decisions may improve future prioritization or personalization.

For example, the system may learn that the researcher wants more attention on theoretical contribution or particular methodological risks.

However:

> **HUMAN feedback improves relevance and prioritization; it does not become an objective scientific truth label.**

A rejected candidate is not universally false. It may simply be unsuitable for the current project or evidence state.

## 30. Review Completion Is Not Knowledge Completion

A reviewed item can become active again after new evidence.

Example:

```text
Sep 04 — HUMAN REVIEWED
Sep 08 — new contradictory evidence
Sep 08 — NEEDS ATTENTION
```

This is normal knowledge evolution, not workflow failure.

## 31. Review Queue Hygiene

To avoid overwhelming the HUMAN, the system should prefer meaningful scientific attention over volume.

It should avoid creating separate review items for every minor extraction when those items can be grouped into one scientifically coherent question.

Example:

Prefer:

```text
GAP-014 — Three new studies materially challenge the current novelty interpretation.
```

rather than three nearly identical alerts unless separate review is scientifically necessary.

## 32. Coverage Context Is Mandatory

A HUMAN judgment should see relevant coverage limitations.

Example:

```text
COVERAGE CONTEXT
OpenAlex: HEALTHY
Crossref: HEALTHY
Semantic Scholar: DEGRADED
Full text: 48%
Abstract: 87%
Metadata: 100%

Interpretation:
Prior-solution search may be incomplete.
Absence of discovered evidence is not evidence of absence.
```

Coverage limitations should inform judgment without becoming automatic scientific verdicts.

## 33. J1 Acceptance Criteria

Human Review v0 is acceptable when a HUMAN can answer:

1. What needs my scientific attention?
2. Why now?
3. What changed?
4. What evidence supports the current interpretation?
5. What evidence challenges it?
6. What alternatives should I inspect?
7. What coverage/uncertainty limits apply?
8. Which R0–R16 stages are affected?
9. What did I decide previously?
10. What evidence context existed when I made that decision?
11. Can I record a new judgment and rationale without erasing history?
12. Can new evidence request review without automatically reversing my decision?
13. Can research crawling and unrelated analysis continue while review is pending?
14. Can Profile A and Profile B use the same review architecture?

## 34. J1 Boundary

This specification intentionally does not yet define:

- database schema for HumanDecision;
- authentication/role model;
- multi-researcher conflict resolution;
- electronic signatures;
- approval workflow engine;
- notification implementation;
- queue algorithms;
- scoring formulas;
- API endpoints;
- add-in contracts.

These belong to J2 and later stages and should be derived from the accepted HUMAN research experience.

## 35. Pinned UX Principle Candidate

> **Human Review is where evidence-aware scientific judgment is recorded, not where the system asks permission to continue operating. New evidence may request renewed attention, but only the HUMAN changes the HUMAN scientific decision.**
