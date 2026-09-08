# Evidence Explorer v0

Status: **J1 ACTIVE — Low-Fidelity UX Specification**

## 1. Purpose

Evidence Explorer is the scientific traceability workspace of GFPROJCLAW.

Its primary purpose is to let a HUMAN move from a research-level statement, assessment, gap, theory, method option, or contribution candidate down to the literature record that supports or challenges it.

The core trace is:

`Source → Paper/Work → Passage or Record → Extracted Claim → Evidence Relationship → Synthesis/Research Object → Assessment → HUMAN Judgment`

The central principle is:

> **No Evidence → No Evidence-Backed Claim.**

Evidence Explorer does not decide whether a scientific interpretation is true. It makes the evidence, provenance, limitations, disagreements, and access level visible so the HUMAN can judge them.

## 2. Cross-Domain Requirement

The same Evidence Explorer must support both reference profiles.

### Profile A — Computer / Information Systems

- IT Governance
- e-Government / Digital Government
- Enterprise Architecture

### Profile B — Management / Organization Studies

- Resilient Organization / Organizational Resilience
- Human Behaviour
- Human Capability

The evidence model must not fork by domain. Domain differences should be represented through Research Profiles, Research Projects, generic research objects, or ADR-001 extension mechanisms.

## 3. Primary HUMAN Questions

Evidence Explorer should help answer:

- Where did this claim come from?
- What exactly does the source say?
- Is the evidence full text, abstract only, or metadata only?
- Does the paper support, challenge, extend, replicate, contradict, or address the research object?
- Is the extracted claim stronger than the source actually supports?
- Are multiple papers saying the same thing?
- Is there contradictory evidence?
- What context, sample, method, theory, or limitation qualifies the evidence?
- Which synthesis, gap, theory option, method option, contribution candidate, assessment, or R-stage uses this evidence?
- Has the interpretation changed over time?
- What still requires HUMAN review?

## 4. Evidence Explorer Screen Structure

```text
EVIDENCE EXPLORER
Profile: [ ... ]   Project: [ ... ]

Search: [ paper / DOI / author / claim / concept / theory / gap / method ]
Filters: [Access] [Relationship] [Claim Status] [Year] [Source] [R-Stage]

LEFT: Evidence Results
CENTER: Evidence Detail
RIGHT: Research Context / Trace
```

The low-fidelity design may use panels, drawers, or drill-down pages. The important requirement is continuous navigability from research interpretation to source evidence and back.

## 5. Evidence Result Row

Each result should expose enough context to judge whether it deserves inspection:

```text
CLM-142
Claim: [concise extracted claim]
Paper: [title, year]
Relationship: CHALLENGES GAP-014
Access: FULL_TEXT
Claim Status: HUMAN_REVIEWED / MACHINE_EXTRACTED / CONTESTED
Used By: R4, R5, R12
```

The result list should not imply that machine-extracted claims are equivalent to HUMAN-reviewed interpretations.

## 6. Paper / Work Layer

A paper/work view should expose at minimum:

- stable work identifier;
- title;
- authors;
- publication year/date where available;
- DOI and other source identifiers where available;
- venue/journal/conference where available;
- source records from which metadata/content was obtained;
- access level;
- discovered-by search/run/watchlist;
- profile/project relevance;
- extraction status;
- linked claims;
- linked evidence relationships;
- linked research objects;
- provenance/history.

Multiple source records may refer to the same normalized work. Source identity and work identity should therefore be conceptually distinct in J2.

## 7. Access Level — Mandatory Scientific Context

Every paper/claim/evidence view must visibly distinguish:

`FULL_TEXT | ABSTRACT_ONLY | METADATA_ONLY`

### FULL_TEXT

The system has accessible full-text material sufficient to retain passage-level provenance for the relevant extraction.

### ABSTRACT_ONLY

The evidence is based on an abstract or equivalent summary record. Claims must not be presented as though the full paper was inspected.

### METADATA_ONLY

The system knows that the work exists and may use bibliographic metadata for discovery, deduplication, search expansion, or coverage analysis.

Metadata alone must **not** be presented as passage-level scientific evidence.

This distinction must remain visible when evidence propagates into Gap, Theory, Method, Contribution, Advice, Today, or R0–R16 screens.

## 8. Passage / Record Layer

For evidence-backed claims, the HUMAN should be able to inspect the relevant passage or source record.

The view should show:

```text
Evidence Fragment: EVF-0092
Paper: [work]
Location: [section/page/paragraph or source-record location if available]
Access: FULL_TEXT
Extraction Version: [...]

Relevant passage:
[bounded source text or representation permitted by source/access policy]

Extracted claim:
[claim]

Relationship:
SUPPORTS / CHALLENGES / EXTENDS / REPLICATES / CONTRADICTS / ADDRESSES
```

Exact storage/rendering constraints will be decided later according to source rights and implementation requirements. J1 requires provenance and inspectability, not unrestricted reproduction of source text.

## 9. Claim Layer

A Claim is a proposition extracted or recorded from evidence. It is not automatically a scientific truth.

A claim view should expose:

- claim text;
- claim type where useful;
- source paper/work;
- supporting passage/record;
- access level;
- extraction method/version;
- confidence/quality observations if used;
- context/scope;
- linked concepts/constructs;
- theory/model/framework links where relevant;
- method/design links where relevant;
- evidence relationships;
- conflicting claims;
- HUMAN review state;
- history.

Potential claim review states can remain conceptually separate from evidence relationships, for example:

`MACHINE_EXTRACTED | NEEDS_REVIEW | HUMAN_REVIEWED | CONTESTED | QUARANTINED`

The exact enum belongs to J2 or later.

## 10. Evidence Relationships

Evidence should be connected to research objects using explicit semantic relationships rather than a generic “related” link wherever possible.

Initial conceptual relationships include:

`SUPPORTS | CHALLENGES | EXTENDS | REPLICATES | CONTRADICTS | ADDRESSES`

Examples:

```text
CLM-142 CHALLENGES GAP-014
CLM-151 SUPPORTS GAP-014
CLM-166 ADDRESSES GAP-014
CLM-180 EXTENDS THEORY-006
CLM-193 CHALLENGES METHOD-012
```

The relationship itself should be inspectable: who/what created it, why, which evidence supports that interpretation, whether a HUMAN reviewed it, and whether it changed.

## 11. Contradictory Evidence

Evidence Explorer must make disagreement visible.

It must never silently replace an older claim merely because a newer paper disagrees.

A contested view may show:

```text
Research Object: GAP-014

SUPPORTS        7 claims / 5 papers
CHALLENGES      3 claims / 3 papers
ADDRESSES       2 claims / 2 papers
CONTRADICTS     1 claim  / 1 paper

Current synthesis: CONTESTED
Human state: NEED MORE EVIDENCE
```

Counts are navigation aids, not scientific votes. Ten weak papers do not automatically outweigh one strong study.

## 12. Context Before Aggregation

The system should preserve context that may explain apparent contradiction, including where extractable:

- population/sample;
- organizational/public-sector context;
- geography;
- time period;
- unit/level of analysis;
- research design;
- operationalization/measurement;
- theory/framework;
- boundary conditions;
- limitations.

This supports the HUMAN in distinguishing genuine contradiction from contextual or methodological differences.

## 13. Claim–Evidence Audit

Evidence Explorer should support later Claim–Evidence Audit capability by making visible whether:

- the cited passage actually supports the extracted claim;
- the claim overgeneralizes beyond the source;
- causal language exceeds the research design;
- an abstract-only source is being treated as full-text evidence;
- a synthesis ignores known counter-evidence;
- a claim relies excessively on one paper or one scholarly school;
- evidence is stale relative to newer contradictory literature.

The system may flag these as attention items, not scientific verdicts.

## 14. Research Context / Backlinks

Every evidence item should show where it is being used.

Possible backlinks include:

- What We Know synthesis;
- Candidate Gap;
- Existing Solution;
- Limitation;
- Counter-Evidence;
- Theory/Mechanism option;
- Method option;
- Candidate Contribution;
- Assessment/advice dimension;
- ChangeEvent;
- R0–R16 stage;
- HUMAN Decision.

This creates bidirectional navigation:

`Research Reasoning → Evidence`

and

`Evidence → Research Reasoning`.

## 15. Relationship to Today / What Changed?

A Today card such as:

```text
GAP-014 weakened
Reason: new prior solution discovered
Affected: R4 R5 R11 R12
```

must support navigation:

`Today Change → ChangeEvent → Existing Solution / Claim → Evidence Fragment → Paper/Source`

The HUMAN should never have to trust an unexplained change label.

## 16. Relationship to Research Journey R0–R16

An R-stage status must be explainable through evidence.

Example:

```text
R5 Gap Falsification — NEEDS ATTENTION
Why?
Two newly discovered studies may already address part of GAP-014.

[Inspect Evidence]
```

Navigation:

`R5 → WHY → Claims → Evidence Relationships → Passage/Record → Papers`

The same mechanism applies across both reference profiles.

## 17. Relationship to Gap–Solution Workspace

Every section of the Gap–Solution Workspace should be evidence-addressable.

Examples:

```text
WHAT WE KNOW → supporting/challenging claims
WHAT WE DON'T KNOW → evidence coverage + unresolved synthesis
EXISTING SOLUTIONS → claims/papers that address the gap
LIMITATIONS → limitation claims/passages
COUNTER-EVIDENCE → challenging/contradictory evidence
THEORY OPTIONS → evidence linking theories/mechanisms
METHOD OPTIONS → evidence about research designs/measurements
NOVELTY CHALLENGE → nearest prior solutions and overlap evidence
```

## 18. HUMAN Review Actions

From Evidence Explorer, a HUMAN may eventually be able to:

- confirm interpretation;
- modify extracted claim;
- mark needs more context;
- flag unsupported extraction;
- mark evidence as relevant/not relevant to project;
- record disagreement with machine relationship;
- request/find more evidence;
- quarantine an item from evidence-backed synthesis while preserving audit history.

Exact controls belong to later UX/implementation refinement.

Human review does not stop future crawling or unrelated extraction.

## 19. Local Quarantine

If a passage, citation, source record, extraction, or relationship cannot be verified, the affected item may be quarantined locally.

Example:

```text
CLM-204 — QUARANTINED
Reason: passage provenance could not be verified
Affected synthesis: GAP-021 coverage reduced
Unrelated claims: continue normally
```

Quarantine means the item cannot currently be promoted as evidence-backed knowledge. It does not mean the entire paper, source, run, profile, or project must stop unless the failure genuinely affects that scope.

## 20. Temporal Evidence and Versioning

Evidence interpretation may change.

The system should retain history such as:

```text
v1  CLM-142 → SUPPORTS GAP-014
v2  HUMAN review narrows claim scope
v3  New context extraction → relationship changed to CHALLENGES
```

Old assessments are not overwritten. The HUMAN can inspect why an interpretation changed.

## 21. Profile A Example

Illustrative trace only:

```text
Research Object:
GAP-014 — Governance capability under digital-government disruption

Synthesis:
Current evidence suggests the proposed gap may be context-dependent.

CHALLENGING CLAIM:
CLM-142 — A prior governance/EA capability study appears to address part of the proposed mechanism.

Evidence:
EVF-0092
Access: FULL_TEXT
Paper: [Profile A literature]
Context: digital government / public organization
Method: [extracted method context]

Relationship:
CLM-142 CHALLENGES GAP-014

Affected Journey:
R4 Gap Formation
R5 Gap Falsification
R11 Contribution Formation
R12 Novelty Challenge

Human:
NEED MORE EVIDENCE
```

## 22. Profile B Example

Illustrative trace only:

```text
Research Object:
GAP-014 — Human capability mechanisms in organizational resilience

Synthesis:
Current evidence suggests that the proposed mechanism may overlap with an established behavioural explanation.

CHALLENGING CLAIM:
CLM-142 — A prior organizational study appears to explain part of the resilience mechanism through an existing construct.

Evidence:
EVF-0092
Access: ABSTRACT_ONLY
Paper: [Profile B literature]
Context: organization / workforce
Level of analysis: [if extractable]
Method: [if extractable]

Relationship:
CLM-142 CHALLENGES GAP-014

Affected Journey:
R4 Gap Formation
R5 Gap Falsification
R6 Theory Positioning
R8 Conceptualization
R12 Novelty Challenge

Human:
NEED MORE EVIDENCE
```

The structure is identical. Domain vocabulary and scientific content differ through the profile/project and evidence itself.

## 23. Cross-Domain Generality Matrix

| Capability | Profile A | Profile B | Expected Resolution |
|---|---|---|---|
| Work identity | IS/government/EA papers | management/OB papers | Core generic |
| Passage provenance | source text/record | source text/record | Core generic |
| Claim | governance/architecture claim | behavioural/capability claim | Core generic |
| Construct/context | governance/institutional | human/organizational | Generic objects + profile content |
| Evidence relationship | supports/challenges/etc. | supports/challenges/etc. | Core generic |
| Method context | IS/public-sector methods | management/organization methods | Generic method objects |
| Level of analysis | system/org/institution etc. | individual/team/org etc. | Generic object |
| Specialized source | possible computing-specific source | possible management-specific source | Add-in/source adapter if needed |

Differences follow ADR-001 classifications and do not globally stop development.

## 24. Low-Fidelity Detail Layout

```text
┌────────────────────────────────────────────────────────────────────┐
│ EVIDENCE EXPLORER                                                  │
│ Profile [A/B]  Project [...]  Search [...]                         │
├────────────────┬─────────────────────────────┬─────────────────────┤
│ RESULTS        │ EVIDENCE DETAIL             │ RESEARCH CONTEXT    │
│                │                             │                     │
│ CLM-142        │ Paper / Work                │ Used by GAP-014     │
│ CHALLENGES     │ Access: FULL_TEXT           │ R4 R5 R12           │
│ GAP-014        │                             │                     │
│                │ Relevant Passage / Record   │ Current synthesis   │
│ CLM-151        │ [...]                       │ CONTESTED           │
│ SUPPORTS       │                             │                     │
│ GAP-014        │ Extracted Claim             │ Human state         │
│                │ [...]                       │ NEED MORE EVIDENCE  │
│ CLM-166        │                             │                     │
│ ADDRESSES      │ Relationship                │ Change history      │
│ GAP-014        │ CHALLENGES GAP-014          │ [...]               │
│                │                             │                     │
│                │ [Review] [History]          │ [Open GAP-014]      │
└────────────────┴─────────────────────────────┴─────────────────────┘
```

## 25. Evidence Quality Without False Precision

J1 does not require a universal evidence-quality score.

Where useful, the system should expose decomposed observations such as:

- access completeness;
- provenance completeness;
- extraction review state;
- methodological context availability;
- replication/corroboration;
- contradiction;
- recency;
- source/coverage limitations.

A later scoring mechanism may use some of these as advice dimensions, but Evidence Explorer should preserve the underlying observations so the HUMAN can inspect them.

## 26. J1 Acceptance Criteria

Evidence Explorer v0 is acceptable when a HUMAN can answer:

1. Which paper/source supports this research statement?
2. What passage or record was used?
3. What claim was extracted?
4. What evidence relationship was inferred?
5. Is the evidence full text, abstract only, or metadata only?
6. What context qualifies the claim?
7. What evidence challenges or contradicts it?
8. Which gap/theory/method/contribution/R-stage uses it?
9. Why did an assessment change?
10. Has a HUMAN reviewed the interpretation?
11. Is any item quarantined, and why?
12. What coverage limitations remain?
13. Can Profile A and Profile B use exactly the same evidence reasoning structure?

## 27. J1 Boundary

This specification intentionally does not yet define:

- PostgreSQL tables;
- vector database choice;
- embedding model;
- document parser implementation;
- extraction prompt design;
- source-specific copyright/storage policy implementation;
- API endpoints;
- class hierarchy;
- evidence scoring formula;
- plugin/add-in contract.

These belong to J2 and later architecture/implementation stages and should be derived from the accepted HUMAN evidence experience.

## 28. Pinned UX Principle Candidate

> **Every important scientific status, change, advice item, gap, theory option, method option, and contribution candidate must be able to answer: “What evidence leads us here, what challenges it, how complete is our access, and what still requires HUMAN judgment?”**
