# GFPROJCLAW Research Cockpit v0

Status: **J1 Low-Fidelity UX Baseline**  
Version: **0**  
Canonical repository: `gerryfirmansyah/gfprojclaw-research-intelligence`  

## 1. Purpose

This document is the living UX specification for the GFPROJCLAW Research Cockpit. It translates the pinned architecture constitution into the HUMAN-facing research workspace.

The cockpit is designed to help HUMAN researchers understand:

- what changed in the research landscape;
- where their research currently stands across R0-R16;
- why the system assigns a research status;
- what evidence supports or challenges that status;
- what research opportunities, alternatives and risks are emerging;
- what needs HUMAN judgment;
- what the HUMAN may learn or review next.

The cockpit must never convert research maturity into a scientific gate. AI provides evidence-backed candidates, advice and critique; HUMAN retains scientific authority.

## 2. Pinned UX Principles

1. **Dashboard = place to work and think.**
2. **Telegram = research radar, not canonical research state.**
3. **PostgreSQL = canonical knowledge/evidence store.**
4. **What Changed? is more important than raw document counts.**
5. **R0-R16 is iterative, not a waterfall or gate chain.**
6. **No global SYSTEM FAILED state for local source/job failures.**
7. **Advice scores prioritize attention; they are not truth probabilities or publication probabilities.**
8. **Scientific claims must remain traceable to evidence.**
9. **Absence of discovered evidence is not evidence of absence.**
10. **The same cockpit must work across Research Profiles without domain-specific UX hardcoding.**

## 3. Global Context Header

The Research Profile is the context for the entire cockpit.

```text
GFPROJCLAW — RESEARCH COCKPIT

Research Profile
[ Resilient Organization & Human Capability ▼ ]

Research Project
[ Organizational Resilience Study ▼ ]

Watchlist: Organizational Resilience | Human Capability | Dynamic Capabilities
Coverage: 2015–2026
Last intelligence update: Today 06:20
Sources: 2 Healthy · 1 Degraded
Human attention: 14 items
```

Switching to another profile such as `IT Governance / e-Government / Enterprise Architecture` must not require a different cockpit design.

## 4. Screen Hierarchy

The Version 0 cockpit uses six primary research areas:

1. **Today / What Changed?**
2. **Research Journey R0-R16**
3. **Research Opportunities**
4. **Evidence Explorer**
5. **Knowledge Evolution**
6. **Human Review**

Secondary areas:

- Research Profiles / Watchlists
- Coverage & System Health
- Research Policy / Settings

## 5. Screen 1 — Today / What Changed?

### Purpose

Show meaningful changes in the research landscape since the HUMAN last reviewed the profile/project.

### Human questions

- What changed?
- Why does it matter?
- Which R-stage, gap, theory, method or contribution may be affected?
- What requires my attention now?

### Minimum information

```text
┌─────────────────────────────────────────────────────────────┐
│ WHAT CHANGED?                              Last 24 hours     │
├─────────────────────────────────────────────────────────────┤
│ + 18 new relevant papers                                   │
│ +  7 new evidence-backed claims                            │
│ ↑  GAP-014 strengthened                                    │
│ ↓  GAP-021 weakened by 2 recent studies                    │
│ !  GAP-008 possibly addressed by existing solution         │
│ +  1 competing theoretical explanation discovered          │
│ +  2 alternative methods discovered                        │
│ !  R6 Theory Positioning requires attention                │
└─────────────────────────────────────────────────────────────┘
```

### Meaningful change card

```text
GAP-014
Human capability as mechanism of organizational resilience

STRENGTHENING
Previous advice: 72
Current advice: 81

WHY DID IT CHANGE?
+ 3 new supporting studies
+ 1 new boundary-condition finding
- 1 counter-evidence paper

[Why?] [Evidence] [Counter Evidence] [Review]
```

The numeric value is an explainable advice/ranking score, not a probability that the claim is true.

## 6. Screen 2 — Research Journey R0-R16

### Purpose

Provide a living research-lab view of the project’s scientific maturity, evidence and attention needs.

### Research Journey

```text
R0  Research Intent             HUMAN REVIEWED       ✓
R1  Research Landscape          MATURE               ●
R2  Evidence Mapping            EVIDENCE GROWING      ●
R3  Problem Formulation         DEVELOPING            ◐
R4  Gap Formation               NEEDS ATTENTION       !
R5  Gap Falsification           EVIDENCE GROWING      ●
R6  Theory Positioning          NEEDS ATTENTION       !
R7  Research Question           DEVELOPING            ◐
R8  Conceptualization           DEVELOPING            ◐
R9  Method Intelligence         EVIDENCE GROWING      ●
R10 Research Design             NOT STARTED           ○
R11 Contribution Formation      DEVELOPING            ◐
R12 Novelty Challenge           NEEDS ATTENTION       !
R13 Evidence & Argument Audit   NOT STARTED           ○
R14 Adversarial Review          NOT STARTED           ○
R15 Scholarly Positioning       DEVELOPING            ◐
R16 Research Readiness          DEVELOPING            ◐
```

### Allowed status vocabulary

- NOT STARTED
- DEVELOPING
- EVIDENCE GROWING
- NEEDS ATTENTION
- HUMAN REVIEWED
- MATURE

Statuses are informational and reversible as knowledge evolves.

### Non-gating rule

There is no rule such as `R5 must PASS before R6 unlocks`.

New evidence may affect multiple stages simultaneously:

```text
New evidence may affect:
R4  Gap Formation
R6  Theory Positioning
R11 Contribution Formation
R12 Novelty Challenge
```

## 7. R-Stage Detail — Living Lab Pattern

Every R-stage detail view must expose the same information pattern:

**STATUS → WHY → EVIDENCE → LEARN → RISK → SUGGESTED ACTION → HUMAN DECISION → CHANGE HISTORY**

Example:

```text
R6 — THEORY POSITIONING

STATUS
NEEDS ATTENTION

WHY?
Current candidate gap is supported by several studies,
but its theoretical explanation is not yet well differentiated.

WHAT WE FOUND
5 relevant theoretical lenses
23 mapped papers
8 use Theory A
6 use Theory B
4 use Theory C
5 other / mixed

EVIDENCE
Supporting evidence       12
Challenging evidence       4
Boundary conditions        3
Competing explanations     2

LEARN — WHY DOES THIS MATTER?
A theory should not be selected merely because it is frequently
used. HUMAN should examine whether its mechanism explains the
research problem and whether the study can meaningfully extend,
challenge, integrate or bound existing theory.

RISKS
! Current argument may be primarily contextual.
! Competing Theory B explains part of the same phenomenon.
! Boundary condition found in 3 studies.

SUGGESTED HUMAN ACTIONS
[Compare Theories]
[Inspect Mechanisms]
[Review Counter-Evidence]
[Request More Evidence]

HUMAN JUDGMENT
[Accept Current Direction]
[Modify]
[Need More Evidence]
[Record Researcher Note]
```

## 8. R0-R16 Research Stages

| R | Stage | Core HUMAN question |
|---|---|---|
| R0 | Research Intent | What phenomenon or scientific problem do I want to understand? |
| R1 | Research Landscape | What is already known and where is the conversation moving? |
| R2 | Evidence Mapping | What evidence exists, how accessible is it, and where does it conflict? |
| R3 | Problem Formulation | What is the substantive scientific problem? |
| R4 | Gap Formation | What is not sufficiently known, explained, tested or synthesized? |
| R5 | Gap Falsification | Does the gap survive deliberate attempts to disprove it? |
| R6 | Theory Positioning | Which theory best explains the problem and where are its limits? |
| R7 | Research Question | Does the RQ logically follow from problem, evidence and gap? |
| R8 | Conceptualization | What constructs, mechanisms and relationships should be examined? |
| R9 | Method Intelligence | How have comparable studies investigated this problem? |
| R10 | Research Design | What defensible design can answer the RQ? |
| R11 | Contribution Formation | If the study succeeds, what changes in understanding, method, policy or practice? |
| R12 | Novelty Challenge | Is the proposed contribution meaningfully distinct from existing solutions? |
| R13 | Evidence & Argument Audit | Does every important claim have appropriate evidence? |
| R14 | Adversarial Review | What are the strongest reasons a critical reviewer could reject the argument? |
| R15 | Scholarly Positioning | Which scholarly conversation does the research contribute to and how? |
| R16 | Research Readiness | What is strong, uncertain or still requires HUMAN attention? |

## 9. Screen 3 — Research Opportunities

### Purpose

Surface candidate research opportunities without collapsing scientific judgment into one opaque score.

```text
RESEARCH OPPORTUNITIES

                 Evidence  Novelty  Counter   Theory   Method
                 Strength  Potential Risk     Value    Feasib.
──────────────────────────────────────────────────────────────
GAP-014              81       74       38        86       71
GAP-021              62       41       77        68       84
GAP-033              73       88       52        79       61
```

Dimensions may include:

- Gap Evidence Strength
- Novelty Potential
- Counter-Evidence Risk
- Evidence Coverage
- Theoretical Significance
- Methodological Feasibility
- RQ-Theory-Method Alignment
- Practical / Policy Significance
- Review Priority

No score automatically accepts or rejects a scientific candidate.

## 10. Candidate / Gap-Solution Workspace

### Purpose

Provide the primary HUMAN workspace for examining a candidate gap or research opportunity.

```text
GAP-014
Human capability → Organizational resilience

[CANDIDATE GAP] [STRENGTHENING]

WHAT WE KNOW
Evidence-backed synthesis...

WHAT WE DON'T KNOW
Candidate insufficiency...

WHY IT MATTERS
Potential theoretical/practical significance...

EXISTING SOLUTIONS
Solution A
Solution B
Solution C

LIMITATIONS OF EXISTING SOLUTIONS
...

ALTERNATIVE EXPLANATIONS
Theory B...
Mechanism C...

COUNTER-EVIDENCE
Paper 1
Paper 2

POSSIBLE CONTRIBUTION
Candidate theory extension...
Possible boundary condition...

METHOD OPTIONS
Longitudinal...
SEM...
Case study...
Mixed method...

HUMAN
[Review] [Modify] [Need More Evidence]
```

Existing solutions must be presented before novelty claims are promoted.

## 11. Screen 4 — Evidence Explorer

### Purpose

Allow every important scientific claim to be traced back to the available source evidence.

```text
CLAIM-204
Human capability positively influences adaptive resilience.

Evidence status: CONTESTED

SUPPORTS
Paper A — 2024
Paper B — 2025
Paper C — 2026

CHALLENGES
Paper D — 2025
Paper E — 2026

EXTENDS
Paper F — 2026

[Open Paper A]
        ↓
[Relevant Passage / Record]
        ↓
[Extracted Claim]
        ↓
[Evidence Relationship]
        ↓
[Current Synthesis]
```

Required evidence-access disclosure:

- FULL TEXT
- ABSTRACT ONLY
- METADATA ONLY

Pinned traceability chain:

`Source → Passage/Record → Extracted Claim → Evidence → Synthesis → Candidate Gap → Human Judgment`

No Evidence → No Evidence-Backed Claim.

## 12. Screen 5 — Knowledge Evolution

### Purpose

Show how research understanding changes over time rather than simply accumulating documents.

```text
GAP-014 — KNOWLEDGE EVOLUTION

Jan 2026    CANDIDATE
            Evidence: 7 papers

Mar 2026    STRENGTHENING
            +4 supporting papers

May 2026    CONTESTED
            2 counter-evidence studies discovered

Jul 2026    STRENGTHENING
            boundary condition identified

Sep 2026    Current
            Gap Evidence Advice: 81
            Novelty Potential: 74
```

Each change must allow HUMAN to inspect:

`What changed → New evidence → Previous assessment → New assessment → Why`

Historical assessments are versioned and never silently overwritten.

## 13. Screen 6 — Human Review

### Purpose

Collect scientific-attention items requiring HUMAN judgment, not engineering error logs.

```text
HUMAN REVIEW

HIGH ATTENTION
─────────────────────────────────────
R12 Novelty Challenge
New 2026 paper overlaps candidate contribution

R6 Theory Positioning
Competing theoretical explanation discovered

GAP-021
3 counter-evidence papers found

NORMAL
─────────────────────────────────────
2 new method alternatives
1 construct-definition disagreement
4 synthesis updates
```

HUMAN actions may include:

- REVIEW
- MODIFY
- ACCEPT DIRECTION
- REJECT CANDIDATE
- NEED MORE EVIDENCE
- RECORD RESEARCHER NOTE

The system must preserve the evidence context and researcher rationale available when a decision was made.

## 14. Coverage & System Health

### Purpose

Expose operational limitations and evidence coverage without making infrastructure the center of the research experience.

```text
RESEARCH COVERAGE

OpenAlex             HEALTHY
Crossref             HEALTHY
Semantic Scholar     DEGRADED

Full-text coverage       48%
Abstract coverage        87%
Metadata coverage        100%

IMPORTANT
Semantic Scholar coverage has been degraded for 6 hours.
Current research assessments remain available, but discovery
coverage may be incomplete.
```

Local source degradation must never become a global research lock.

Epistemic warning:

**Absence of discovered evidence ≠ evidence of absence.**

## 15. Research Profile UX

Research Profile configuration provides domain context without changing the core engine.

Minimum profile context:

- domain / discipline;
- topics and subtopics;
- watchlists;
- seed papers / DOI / seminal literature;
- Research Questions when available;
- concepts / constructs;
- preferred theories / models / frameworks;
- preferred or excluded methods when relevant;
- source preferences;
- scoring/advice priorities;
- research policy;
- Telegram/reporting preferences.

Pinned reference profiles:

### Profile A — Computing / Information Systems

- IT Governance
- e-Government / Digital Government
- Enterprise Architecture

### Profile B — Management / Organization Studies

- Management
- Resilient Organization / Organizational Resilience
- Human Capability
- Organizational Capability

Cross-domain acceptance rule: both profiles must use the same Research Cockpit and Research Intelligence Core without domain-specific source-code modifications.

## 16. Telegram Research Radar

Telegram is not the canonical workspace. It alerts HUMAN when attention is useful.

```text
GFPROJCLAW — DAILY RESEARCH INTELLIGENCE

Profile:
Resilient Organization & Human Capability

Since yesterday:
18 new relevant papers
7 new evidence-backed claims

Research changes:
↑ GAP-014 strengthened
↓ GAP-021 weakened
! GAP-008 may have an existing solution
! Competing theory found for R6
+ 2 method alternatives

Human attention:
R6  Theory Positioning
R12 Novelty Challenge

Coverage:
Semantic Scholar DEGRADED
Other sources healthy

Open Research Cockpit →
```

Do not send routine raw crawler logs, retry noise or HTTP failures to the researcher unless operational degradation materially affects research coverage.

## 17. J1 Acceptance Criteria

J1 is considered complete when the low-fidelity UX can clearly answer:

1. What changed?
2. Where is my research across R0-R16?
3. Why is the research status assigned?
4. What evidence supports or challenges it?
5. What opportunities, alternatives and risks are emerging?
6. What requires HUMAN judgment?
7. What can the HUMAN learn or review next without surrendering scientific authority to AI?

Architecture acceptance criterion:

> The entire UX must continue to work when the active Research Profile changes between the pinned Computing/IS and Management/Organization Studies reference profiles, without domain-specific UX or core-code branches.

## 18. Version 0 Boundary

This is a low-fidelity living specification. J1 must not prematurely define implementation details belonging to J2+ such as database schema, APIs, queues, source adapters or agent orchestration.

Version 0 should prove research usefulness before operational complexity.

## 19. Next J1 Work

Before moving to J2, this document should be refined with:

- final screen/navigation hierarchy;
- minimum information required per screen;
- HUMAN actions and transitions;
- relationship between Research Profile, Research Project and R0-R16;
- priority classification for Version 0 versus later UX;
- Telegram-to-Dashboard navigation behavior;
- explicit UX handling of uncertainty, limited coverage and contradictory evidence.

---

**Pinned development context:** `Version 0 — J0 PINNED / J1 ACTIVE`  
**Document role:** Living UX specification.  
**Scientific authority:** HUMAN.
