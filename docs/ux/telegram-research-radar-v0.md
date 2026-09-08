# Telegram Research Radar v0

Status: **J1 ACTIVE — Low-Fidelity UX Specification**

## 1. Purpose

Telegram Research Radar is the lightweight attention channel of GFPROJCLAW.

The Dashboard is where the HUMAN works, inspects evidence, reasons, compares alternatives, and records scientific judgment. Telegram is where the system surfaces a small number of meaningful research changes that may deserve attention.

The governing principle is:

> **Dashboard = place to work and think. Telegram = radar. PostgreSQL = canonical evidence and knowledge store.**

Telegram must reduce the need to repeatedly open the Dashboard merely to ask whether anything scientifically meaningful has changed.

## 2. What Telegram Is Not

Telegram must not become:

- the canonical research database;
- the primary evidence-inspection interface;
- the place where full scientific reasoning is performed;
- a replacement for Human Review;
- an approval gate;
- a raw crawler log stream;
- an engineering console;
- a score spam channel;
- a publication/Q1 probability notifier;
- a mechanism that converts AI advice into scientific decisions.

Important messages should point the HUMAN back to the Research Cockpit for inspection and judgment.

## 3. Cross-Domain Requirement

The same Radar mechanism must support both reference profiles:

- **Profile A — Computer / Information Systems**
- **Profile B — Management / Organization Studies**

Message structure, scientific-change semantics, coverage disclosure, and HUMAN authority remain generic. Domain terminology comes from Profile/Project content.

## 4. Primary HUMAN Questions

A useful Radar message should quickly answer:

- What changed?
- Why might it matter?
- Which Profile/Project is affected?
- Which research object changed?
- Is the change strengthening, weakening, contesting, or otherwise altering current reasoning?
- What evidence caused it?
- Which R0–R16 stages may need attention?
- Is coverage limited?
- Do I need to inspect or review something now?
- Where do I go in the Dashboard for the full reasoning trace?

## 5. Signal Hierarchy

Telegram should prioritize **meaningful scientific changes**, not volume.

High-value signal classes include:

- candidate gap materially strengthens or weakens;
- candidate gap becomes contested, possibly closed, or reopened;
- important existing solution is discovered;
- novelty interpretation changes materially;
- meaningful counter-evidence appears;
- competing theory/mechanism becomes relevant;
- important method alternative is discovered;
- construct/definition/measurement becomes contested;
- R-stage requires renewed HUMAN attention;
- previous HUMAN decision may deserve review because evidence changed;
- coverage degradation materially limits an active scientific question.

Routine paper discovery belongs mainly in digest form unless unusually relevant.

## 6. Message Contract

A high-value Radar message should normally contain:

```text
[CHANGE TYPE]
Profile / Project

WHAT CHANGED
[object and transition]

WHY IT MATTERS
[brief evidence-aware explanation]

EVIDENCE
[new/changed evidence summary]

AFFECTED
[R-stages / research objects]

COVERAGE
[only when relevant]

ACTION
[Open Dashboard / Review]
```

Messages should remain concise enough for Telegram. Full detail lives in the Dashboard.

## 7. Example — Gap Weakening

```text
GFPROJCLAW Research Radar

GAP WEAKENING
Management / Organization Studies
Human Capability & Organizational Resilience

GAP-014: STRENGTHENING → CONTESTED

Why:
A newly discovered study appears to explain part of the proposed mechanism using an established behavioural construct.

Impact:
Novelty Potential 81 → 52
R5, R6, R11, R12 need attention.

Coverage:
Full-text coverage remains incomplete.

Open Research Cockpit → GAP-014
```

The numeric delta is advice context, not probability or verdict.

## 8. Example — Existing Solution Threat

```text
GFPROJCLAW Research Radar

EXISTING SOLUTION DISCOVERED
Computer / Information Systems
Cross-agency Digital Government Governance

SOL-008 may address part of GAP-014.

Why it matters:
The current contribution may need a narrower boundary condition rather than a broad governance-capability claim.

Evidence:
1 new full-text paper; 2 linked claims.

Affected:
R4, R5, R11, R12

Open Gap–Solution Workspace
```

## 9. Example — Counter-Evidence

```text
GFPROJCLAW Research Radar

COUNTER-EVIDENCE
Organizational Resilience Project

Three new claims challenge the current synthesis for GAP-021.

Current state:
STRENGTHENING → CONTESTED

Why:
Findings differ across level of analysis and measurement approach.

Suggested HUMAN attention:
Compare contexts before revising the gap.

Open Evidence Explorer
```

## 10. Example — Coverage Degradation

Telegram should alert on operational degradation only when scientific coverage is materially affected.

```text
GFPROJCLAW Research Radar

COVERAGE DEGRADED
Profile A — Computer / Information Systems

Semantic Scholar remains unavailable.
Prior-solution and citation-expansion coverage for GAP-014 is currently limited.

Healthy work continues through OpenAlex and Crossref.
Existing evidence remains preserved.

Open Coverage & Health
```

Do not send:

```text
HTTP 429
retry 1
retry 2
worker timeout
```

unless the HUMAN explicitly configures an engineering channel outside the Research Radar concept.

## 11. Daily Digest

The daily digest should answer:

> **What meaningfully changed since the previous digest?**

Illustrative structure:

```text
GFPROJCLAW — Daily Research Radar
8 Sep
Profile: Management / Organization Studies
Project: Human Capability & Organizational Resilience

TODAY
• 14 new relevant works discovered
• 5 new evidence-backed claims
• GAP-014 became CONTESTED
• 1 existing solution affects novelty interpretation
• 1 competing theory deserves review
• R5 and R12 need HUMAN attention

COVERAGE
2 sources healthy; 1 degraded
Full text: 48% of current project corpus

HUMAN REVIEW
2 meaningful items waiting

Open Today / What Changed?
```

Counts summarize activity; scientifically meaningful changes receive explanatory emphasis.

## 12. Weekly Digest

A weekly digest may emphasize knowledge evolution rather than daily activity.

Example:

```text
GFPROJCLAW — Weekly Research Evolution

This week:
• GAP-014: CANDIDATE → STRENGTHENING → CONTESTED
• Novelty Potential: 81 → 52 after prior solution discovery
• Theory option T-006 gained new supporting evidence
• Method option M-012 emerged from 4 recent studies
• 2 HUMAN decisions recorded
• 1 previous decision now deserves renewed review

Coverage:
Full-text access improved from 42% → 48% of project corpus.

Open Knowledge Evolution
```

## 13. High-Value Immediate Alerts

Not every change should wait for a digest.

Potential immediate alerts include:

- a strongly relevant prior solution threatens an active candidate contribution;
- a gap becomes `POSSIBLY_CLOSED`;
- significant counter-evidence materially changes an active assessment;
- new evidence directly challenges a recent HUMAN decision;
- severe coverage degradation materially affects a high-priority active project.

The implementation threshold is deferred beyond J1, but the UX principle is that immediate alerts are exceptional and meaningful.

## 14. Avoiding Alert Fatigue

Radar quality depends on restraint.

The system should prefer:

```text
GAP-014 — 4 new studies materially changed the current interpretation.
```

rather than four separate near-identical alerts.

Routine discovery should normally aggregate into digests.

Repeated operational failures should be summarized by scientific impact, not emitted request by request.

## 15. Message Prioritization

Radar may use explainable attention dimensions such as:

- active Project relevance;
- magnitude of reasoning change;
- counter-evidence significance;
- novelty threat;
- theoretical significance;
- affected R-stages;
- relationship to previous HUMAN decisions;
- evidence access/coverage quality;
- recency.

These dimensions decide notification priority, not scientific truth.

## 16. Telegram and Today / What Changed?

Telegram is a compressed projection of Today.

Conceptually:

`ChangeEvent → Today / What Changed? → Radar Selection → Telegram`

Telegram should not create a separate scientific state.

The canonical ChangeEvent and reasoning remain in the platform.

A Telegram message should deep-link, where technically possible, to the corresponding Dashboard context.

## 17. Telegram and Evidence Explorer

Messages may summarize evidence, but should not pretend that the summary is the evidence itself.

Example:

```text
Evidence:
2 new full-text studies challenge the current mechanism.

[Open Evidence Explorer]
```

The HUMAN should inspect paper, passage/record, claim, and evidence relationship in the Dashboard when needed.

## 18. Telegram and Knowledge Evolution

Temporal messages should describe meaningful transitions:

```text
GAP-014
STRENGTHENING → CONTESTED
```

or

```text
Novelty Potential
81 → 52
```

with a short explanation of the Reasoning Delta.

Historical detail remains in Knowledge Evolution.

## 19. Telegram and Human Review

Radar may notify the HUMAN that scientific attention is warranted.

Example:

```text
HUMAN REVIEW
A previous ACCEPT DIRECTION decision for GAP-014 may deserve review after new prior-solution evidence.

The decision has NOT been changed automatically.

Open Human Review
```

Telegram must never imply that an AI review request itself changed the HUMAN decision.

## 20. Telegram and Coverage & Health

Coverage alerts should answer:

- what degraded;
- what scientific search/assessment may be affected;
- what continues normally;
- whether existing evidence remains valid;
- where to inspect details.

This preserves the local-failure/no-global-lock model.

## 21. Profile / Project Routing

Every scientific Radar message should identify its relevant context when ambiguity is possible:

```text
Profile: Management / Organization Studies
Project: Human Capability & Organizational Resilience
```

A Profile-level message may be sent when the change affects multiple Projects.

Example:

```text
PROFILE INTELLIGENCE
A new organizational-resilience review may affect 3 active projects.
```

The Dashboard resolves project-specific implications.

## 22. Multiple Projects

When several Projects have changes, a digest may group them:

```text
PROFILE: Management / Organization Studies

Human Capability & Resilience
• GAP-014 became CONTESTED
• R12 needs attention

Leadership Under Disruption
• 3 new high-relevance papers
• no major assessment changes
```

This avoids mixing scientific contexts.

## 23. User Configuration

At Profile or Project level, the HUMAN may configure Radar preferences such as:

```text
Daily digest                    ON
Weekly evolution digest         ON
High-value scientific alerts    ON
Coverage-impact alerts          ON
Routine new-paper alerts        DIGEST ONLY
Raw crawler logs                OFF
```

The HUMAN may also choose which Profiles/Projects participate in Telegram Radar.

Exact scheduling and delivery configuration belong to later implementation stages.

## 24. Telegram Commands — V0 Boundary

V0 should remain conservative about commands.

Potential safe navigation/status interactions later may include:

```text
/today
/review
/coverage
```

However, Telegram should **not** become the primary place to execute irreversible or scientifically consequential judgments.

In particular, v0 should not require decisions such as `ACCEPT DIRECTION` or `REJECT CANDIDATE` to be made from Telegram.

The Dashboard preserves the richer evidence context required for scientific judgment.

## 25. No Canonical State in Telegram

Telegram delivery failures, deleted messages, chat history loss, or message edits must not affect canonical research state.

Canonical state remains in PostgreSQL/platform storage.

Conceptually:

`Canonical ChangeEvent → Notification Projection → Telegram Message`

not:

`Telegram Message → Canonical Scientific Truth`

## 26. Delivery Failure Is Local

If Telegram delivery fails:

- research crawling continues;
- evidence extraction continues;
- Knowledge Evolution continues;
- Human Review state remains available in Dashboard;
- the notification may retry independently;
- unrelated notification channels/work continue.

Telegram failure is never a global research lock.

## 27. Evidence and Privacy Discipline

Radar messages should expose only the minimum evidence context needed for attention.

Long passages, sensitive credentials, raw source payloads, internal secrets, and unnecessary operational details should not be sent through Telegram.

Full evidence inspection remains in the controlled Dashboard/Evidence Explorer.

## 28. Profile A Example

```text
GFPROJCLAW Research Radar

THEORY / GAP CHANGE
Profile A — Computer / Information Systems
Project: Cross-agency Digital Government Governance

GAP-014 remains CONTESTED.
A newly discovered enterprise-architecture capability study strengthens an alternative mechanism.

Affected:
R5 Gap Falsification
R6 Theory Positioning
R11 Contribution Formation
R12 Novelty Challenge

Coverage:
Prior-solution search currently LIMITED.

Open Research Cockpit
```

## 29. Profile B Example

```text
GFPROJCLAW Research Radar

THEORY / GAP CHANGE
Profile B — Management / Organization Studies
Project: Human Capability & Organizational Resilience

GAP-014 remains CONTESTED.
A newly discovered organizational-behaviour study strengthens an alternative mechanism.

Affected:
R5 Gap Falsification
R6 Theory Positioning
R11 Contribution Formation
R12 Novelty Challenge

Coverage:
Competing-mechanism search currently LIMITED.

Open Research Cockpit
```

The Radar structure is identical; scientific content differs through Profile/Project context.

## 30. Cross-Domain Generality Matrix

| Radar Capability | Profile A | Profile B | Expected Resolution |
|---|---|---|---|
| Daily digest | same structure | same structure | Core generic |
| Gap change alert | governance/EA content | resilience/capability content | Generic research objects |
| Theory alert | IS/governance theories | management/behaviour theories | Profile content |
| Method alert | IS/public-sector methods | management/org methods | Generic method object |
| R-stage impact | R0–R16 | R0–R16 | Core generic |
| Coverage alert | same semantics | same semantics | Core generic |
| Deep-link target | same cockpit structure | same cockpit structure | Core generic |
| Specialized channel | if genuinely required | if genuinely required | ADR-001 add-in/integration |

A mismatch is a Generality Exception, not a global stop condition.

## 31. Notification Lifecycle

Conceptually:

```text
Evidence / Coverage Change
        ↓
Change Detection
        ↓
ChangeEvent
        ↓
Scientific Significance / Attention Prioritization
        ├── Dashboard Today
        ├── Human Review when needed
        └── Telegram Radar when notification-worthy
```

Telegram does not independently infer scientific state.

## 32. Anti-Patterns

Avoid messages such as:

```text
Novelty confirmed: 91%
```

```text
Your research is Q1 ready.
```

```text
No prior research exists.
```

```text
GAP-014 rejected automatically.
```

```text
Pipeline failed because one source returned 429.
```

Prefer bounded, evidence-aware language:

```text
No closely matching prior solution was discovered in the current search coverage.
```

```text
GAP-014 is currently CONTESTED after new counter-evidence.
```

```text
One source is degraded; healthy discovery continues with reduced coverage.
```

## 33. J1 Acceptance Criteria

Telegram Research Radar v0 is acceptable when a HUMAN can answer from a message:

1. What meaningfully changed?
2. Which Profile/Project is affected?
3. Why might the change matter?
4. What evidence or coverage change caused it?
5. Which R0–R16 stages may need attention?
6. Is coverage limited?
7. Does the message distinguish AI assessment from HUMAN judgment?
8. Can the HUMAN navigate to the Dashboard for full evidence and reasoning?
9. Are routine paper discoveries aggregated rather than spammed?
10. Are raw engineering logs excluded from the Research Radar?
11. Does Telegram failure leave canonical research processing unaffected?
12. Does Telegram avoid becoming the scientific approval interface?
13. Can Profile A and Profile B use the same Radar architecture?

## 34. J1 Boundary

This specification intentionally does not yet define:

- Telegram Bot API implementation;
- bot tokens/secrets;
- webhook vs polling architecture;
- notification database tables;
- retry/backoff formulas;
- exact alert thresholds;
- exact digest schedule;
- deep-link URL implementation;
- message-template code;
- multi-user Telegram routing;
- authentication/linking flow;
- add-in contracts.

These belong to later architecture and implementation stages and must serve the accepted research-attention experience.

## 35. Pinned UX Principle Candidate

> **Telegram tells the researcher that something worth inspecting has changed; the Dashboard explains why, the evidence shows what supports or challenges it, and the HUMAN decides what it means scientifically.**
