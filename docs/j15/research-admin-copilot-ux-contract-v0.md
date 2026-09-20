# J15 Research Copilot / Admin Copilot UX Contract v0

Date: 2026-09-20
Status: HUMAN UX DIRECTION PINNED — implementation checkpoint

## 1. Application boundary

GFPROJCLAW remains one application with one canonical scientific backend, but exposes two clearly separated workspaces/pages: Research Copilot and Admin Copilot. Backend complexity must not leak into the Research Copilot.

## 2. Research Copilot

Research Copilot is for research meaning, evidence, uncertainty, explanation, and HUMAN scientific decisions. Its primary navigation may contain Today, Research Journey, Research Objects / Opportunities, Literature / Evidence Explorer, Research Quality, Advice & Critic, Human Review, and Knowledge Evolution.

Operational implementation details such as scheduler state, worker internals, raw API health, retry queues, database operations, quarantine internals, and service logs must not be mixed into researcher pages. Operational degradation may be summarized only in research-relevant language, without hiding scientific limitations.

## 3. Admin Copilot

Admin Copilot is for system operation, observability, configuration, and administration. It may contain Continuous Pilot, source/provider configuration, source runs, failures/retry, quarantine, API/services, activity/audit, user/access management, and UI preference defaults.

Access to Admin Copilot is permission-aware. A researcher who lacks administrative responsibility should not need to understand backend processes to use Research Copilot.

## 4. No orphan aggregate

Every scientifically meaningful count or aggregate exposed to a researcher must provide a path to its canonical members. Examples include persisted papers, HUMAN decisions, ChangeEvents, radar items, mapped papers, theoretical lenses, and evidence relationship counts. A count must not be a dead statistic.

## 5. Scientific visual hierarchy

Paper title, bibliographic metadata, EvidenceFragment/source text, machine Claim, EvidenceRelationship/rationale, explanation, and HUMAN verification state must be visually distinguishable. Paper titles use one consistent semantic component. Bold typography is reserved for hierarchy and labels; explanatory prose, evidence text, metadata, and rationale normally use regular/medium weight.

Illustrative/DUMMY data must be visually unmistakable from REAL canonical data and must not look like persisted scientific state.

## 6. Design tokens and preferences

Colors, typography, spacing, surfaces, and status presentation should be driven by semantic CSS design tokens rather than hard-coded component styling. Preference precedence should support system default -> administrator-configured default -> permitted user preference.

Customization must preserve accessibility and scientific semantics. A user preference must not make UNKNOWN, warning, HUMAN review, machine suggestion, or other scientifically meaningful states indistinguishable.

## 7. Language

Research Copilot and Admin Copilot should support an Indonesian / English UI toggle through an i18n presentation layer. Navigation, labels, warnings, helper text, and UI explanation templates may be localized. Canonical paper titles, source evidence, Claims, persisted rationale, and scientific records remain in their source/canonical language unless a separately labeled translated view is implemented.

## 8. Preserved scientific boundaries

Research Copilot must continue to distinguish project literature from canonical ResearchObject evidence, ABSTRACT_ONLY from full text, UNKNOWN/NOT_AVAILABLE/NOT_RUN from negative scientific judgments, machine suggestions from HUMAN decisions, and historical ChangeEvent membership absence from evidence absence.

## 9. J15 acceptance boundary

This contract records HUMAN UX direction. It does not declare J15 HUMAN PASS. Implementation must be re-trialed by HUMAN for Profile A and Profile B before acceptance.
