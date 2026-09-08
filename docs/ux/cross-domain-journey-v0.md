# Cross-Domain Journey v0

Status: **J1 ACTIVE — Generality Measurement Baseline**

## Purpose

GFPROJCLAW must be developed and evaluated against two Research Profiles simultaneously. Generality is therefore measured continuously at every J-stage and R-stage rather than tested only after implementation.

## Reference Profile A — Computer / Information Systems

Primary research areas:

- IT Governance
- e-Government / Digital Government
- Enterprise Architecture

## Reference Profile B — Management / Organization Studies

Primary research areas:

- Resilient Organization / Organizational Resilience
- Human Behaviour
- Human Capability

## Cross-Domain Rule

Both profiles must use the same Research Intelligence Core, Research Cockpit, R0-R16 journey model, evidence model, change model, advice model and HUMAN decision model.

Adding or switching a research domain must be a configuration/data operation, not a source-code development project.

Domain-specific vocabulary, concepts, constructs, theories, frameworks, methods, watchlists, seed literature and priorities belong to Research Profiles and Research Projects, not to hardcoded core logic.

## Dual-Profile Development Rule

Every relevant J0-J16 development stage must be reviewed using both Profile A and Profile B.

For each stage we ask:

1. Does the capability work for Profile A?
2. Does the same capability work for Profile B?
3. Is any domain-specific assumption embedded in the core?
4. Can differences be represented through profile/project configuration or generic research objects?
5. Does the HUMAN receive equivalent evidence traceability and scientific authority in both profiles?

A capability is not considered generally validated merely because it works for one reference profile.

## R0-R16 Generality Rule

The same R0-R16 research journey applies to both profiles:

R0 Research Intent
R1 Research Landscape
R2 Evidence Mapping
R3 Problem Formulation
R4 Gap Formation
R5 Gap Falsification
R6 Theory Positioning
R7 Research Question
R8 Conceptualization
R9 Method Intelligence
R10 Research Design
R11 Contribution Formation
R12 Novelty Challenge
R13 Evidence & Argument Audit
R14 Adversarial Review
R15 Scholarly Positioning
R16 Research Readiness

The stages may emphasize different research objects by domain, but the core journey must not fork into separate domain-specific implementations.

## Example Domain Differences Without Core Forking

Profile A may emphasize governance mechanisms, architecture frameworks, maturity models, institutional arrangements and technology/public-sector contexts.

Profile B may emphasize constructs, behavioural mechanisms, mediators/moderators, capabilities, levels of analysis and organizational contexts.

These differences must be represented using generic research objects such as:

`Concept`, `Construct`, `Definition`, `Theory`, `Model`, `Framework`, `Mechanism`, `Relationship`, `Mediator`, `Moderator`, `LevelOfAnalysis`, `Method`, `Operationalization`, `Measurement`, `Claim`, `Evidence`, `GapCandidate`, `ExistingSolution`, `CounterEvidence`, `ContributionCandidate`, `Assessment`, `ChangeEvent`, and `HumanDecision`.

This list is conceptual during J1; the formal Research Object Model belongs to J2.

## Generality Scorecard for Each J-Stage

Each J-stage should record a small cross-domain validation matrix:

| Check | Profile A | Profile B | Core Change Required? |
|---|---|---|---|
| HUMAN question supported | TBD | TBD | Expected: No |
| Generic objects sufficient | TBD | TBD | Expected: No |
| Evidence trace works | TBD | TBD | Expected: No |
| R0-R16 mapping works | TBD | TBD | Expected: No |
| Domain vocabulary configurable | TBD | TBD | Expected: No |

Any `Yes` under **Core Change Required?** triggers a generality review before the stage is pinned.

## Generality Scorecard for Each R-Stage

For each R-stage, both profiles should eventually demonstrate:

`STATUS → WHY → EVIDENCE → LEARN → RISK → SUGGESTED ACTION → HUMAN DECISION → CHANGE HISTORY`

The content may differ by domain; the reasoning and traceability structure must remain general.

## Anti-Hardcoding Test

The following patterns are architectural warning signs:

- `if domain == "it_governance"`
- `if domain == "management"`
- separate core Gap engines for each discipline
- separate R0-R16 implementations by discipline
- domain-specific database schema required merely to onboard a new discipline
- domain-specific Dashboard navigation required merely to switch profiles

Domain adapters are acceptable only where an external source or genuinely domain-specific data format requires them; scientific reasoning objects should remain generic wherever possible.

## Version 0 Cross-Domain Acceptance Criterion

Version 0 should demonstrate that a HUMAN can create/select both reference profiles, observe literature/evidence intelligence through the same Research Cockpit, inspect R0-R16 through the same journey model, trace advice to evidence, and make HUMAN research judgments without source-code changes between Profile A and Profile B.

## Development Principle

> **Generality is not a final test. It is a continuously measured property of the journey.**

Every future design decision should therefore answer both:

- How does this help HUMAN research in Profile A?
- How does the same mechanism help HUMAN research in Profile B?

If the answers require two different core systems, the design should be reconsidered before implementation.
