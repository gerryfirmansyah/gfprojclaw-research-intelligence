# J15 Current State Checkpoint v0

Date: 2026-09-20
Status: J15 IN PROGRESS — HUMAN TRIAL
Code baseline: 968cc9f — Clarify J15 advice critic assessment scope

## 1. Purpose

This document pins the current J15 state before any further information-architecture,
canonical-model, schema, API, or frontend change.

It is a checkpoint, not a J15 HUMAN PASS declaration.

## 2. Completed J15 capabilities

J15 currently includes:

- Research Quality projection with no universal quality score.
- HUMAN Evidence Verification from canonical stored evidence.
- Explainable Advice & Critic using persisted Assessment explanations.
- Explicit Advice & Critic assessment target and evidence scope.
- HUMAN scientific authority remains explicit.
- Machine projections do not establish scientific truth or automatically create HUMAN decisions.

## 3. HUMAN trial findings

### 3.1 Explanation requirement

Every machine-generated scientific Claim, Advice, Critic, Assessment, or recommendation
exposed for HUMAN review must provide a verifiable explanation.

Where canonical explanation is unavailable, the UI must not fabricate one.

### 3.2 No orphan aggregate

Every scientifically meaningful aggregate must be traceable to its canonical members.

Examples:

- 7 new papers -> HUMAN can inspect the seven Works.
- 18 SUPPORTS -> HUMAN can inspect the 18 EvidenceRelationships and their evidence chain.
- 2 CONTRADICTS -> HUMAN can inspect the relevant Work, Claim, EvidenceFragment,
  EvidenceRelationship, and rationale.
- 5 NEEDS_REVIEW -> HUMAN can open the five canonical review items.
- Advice & Critic changed -> HUMAN can inspect the Research Object, Assessment,
  evidence change, and reasoning delta.

### 3.3 Research and Operations perspectives

GFPROJCLAW remains one Cockpit with two explicit perspectives:

RESEARCH
- Research Home / Daily Brief
- Research Objects
- Literature
- Evidence Explorer
- Research Quality
- Advice & Critic
- Human Review
- Knowledge Evolution

OPERATIONS
- System Overview
- Continuous Pilot
- Source Runs
- Failures / Retry
- Quarantine
- API / Services
- Activity / Audit

Menu/perspective is the primary distinction. Color or badges are secondary cues only.

## 4. Daily Brief versus Knowledge Evolution

Research Home / Daily Brief answers:

"What needs HUMAN attention now?"

Knowledge Evolution answers:

"How has knowledge about this Research Object changed over time?"

They must not be duplicate views.

Daily discovery activity and scientific knowledge evolution are distinct:

1. Newly discovered literature
   - Work discovered by the system.
   - It is not automatically evidence for a Research Object.

2. New linked evidence
   - Work -> EvidenceFragment -> Claim -> EvidenceRelationship -> Research Object
     exists canonically.

3. New scientific-context change
   - New evidence or reassessment produces a meaningful reasoning change.

A newly discovered Work must never be silently classified as SUPPORTS,
CONTRADICTS, or another scientific relationship without a canonical
EvidenceRelationship.

## 5. Canonical-data audit completed so far

Current production can trace the current evidence set through:

Research Object
-> EvidenceRelationship
-> Claim
-> EvidenceFragment
-> Work
-> source identifiers

Current ChangeEvent provides:

- primary Research Object
- change type
- previous state snapshot
- current state snapshot
- reasoning delta
- coverage context

However, the current production schema does not provide an implemented
ChangeEvent -> exact trigger-member linkage.

Therefore historical member attribution must not be reconstructed by simply joining
a historical ChangeEvent to the Research Object's current evidence set.

That could falsely attribute evidence that exists now to a past event.

## 6. Existing architecture intent discovered during audit

J2 architecture already specifies:

- one primary Research Object per ChangeEvent;
- many trigger references per ChangeEvent;
- do not force one paper = one ChangeEvent;
- ChangeEvent represents meaningful reasoning change, not every crawler action.

J2 persistence design also proposed:

change_event_evidence
- id
- change_event_id
- claim_id nullable
- evidence_relationship_id nullable
- research_object_id nullable
- role

Its stated purpose is to capture what caused a change without embedding an opaque
list in JSON.

This concept has NOT yet been authorized for a new production migration during
the current J15 HUMAN trial.

## 7. Open architecture question

Before implementing anything, determine the smallest canonical design required for:

"What changed -> how many -> exactly which records -> why -> HUMAN verification"

while preserving the distinction between:

- discovery activity such as newly discovered Works; and
- meaningful scientific ChangeEvents caused by evidence/reassessment.

In particular, do not force raw Work discovery into ChangeEvent merely to populate
Daily Brief.

## 8. Current stop boundary

At this checkpoint:

- no new schema migration is authorized;
- no change_event_evidence implementation has been authorized;
- no Research Home / Daily Brief implementation has been authorized;
- no J15 HUMAN PASS has been declared;
- continuous-pilot production timer remains outside this checkpoint and is not
  authorized by J15 work.

Next work resumes from the canonical-data/design audit, not from implementation.


## 9. 2026-09-20 public acceptance preflight

Public HTTPS contract checks now pass against the deployed API for both canonical trial profiles. Profile A exposes `ABSTRACT_ONLY` linked evidence, explicit `NOT_AVAILABLE` methodological context, `scientific_decision=false`, a canonical `SUPPORTS` relationship, `NOT_RUN` counter-search, and persisted Advice & Critic explanations. Profile B exposes all Research Quality observations as `NOT_AVAILABLE`, no canonical evidence references, six verification items explicitly marked `PROJECT_LITERATURE_ONLY` with no EvidenceRelationship, and no generalized Advice & Critic assessment.

The deployed GitHub Pages `app.js` also contains the expected HUMAN-facing markers for Research Quality, Evidence Verification, `PROJECT_LITERATURE_ONLY`, unavailable-explanation handling, historical `UNKNOWN/NOT_RECORDED` ChangeEvent membership, and Assessment transition display.

These are machine-verifiable deployment preflight checks, not a substitute for the acceptance criterion requiring a HUMAN to complete the end-to-end Cockpit trial for both profiles. J15 therefore remains IN PROGRESS / HUMAN TRIAL.
