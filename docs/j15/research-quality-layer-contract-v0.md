# J15 Research Quality Layer Contract v0

## Purpose
J15 exposes inspectable research-quality observations without converting them into automatic scientific verdicts. Quality is decomposed, contextual, source-traceable, and HUMAN-reviewable.

## Quality dimensions v0
- access completeness
- provenance completeness
- extraction review state
- methodological context availability
- corroboration / replication context
- contradiction / counter-evidence context
- recency context
- source and coverage limitations

These dimensions are observations or advisory context, not a universal evidence-quality score.

## Canonical flow
Canonical evidence/source state -> decomposed quality observations -> advisory quality assessment -> Cockpit/Radar review surface -> HUMAN judgment -> explicit HumanDecision/history where applicable.

## Invariants
1. No universal quality score is required for J15 v0.
2. No threshold may automatically ACCEPT/REJECT evidence, gaps, directions, claims, novelty, significance, causality, or relevance.
3. Every quality observation must be traceable to canonical evidence/source/project state or be explicitly marked NOT_AVAILABLE/NOT_RUN.
4. Access level (FULL_TEXT, ABSTRACT_ONLY, METADATA_ONLY) must remain visible and must not be silently upgraded.
5. Missing methodological context is not evidence of poor methodology; it is missing context.
6. Contradiction/counter-evidence is contextual evidence, not an automatic invalidation.
7. Quality advice must preserve underlying observations so a HUMAN can inspect why attention is suggested.
8. Failures remain local; one unavailable quality dimension must not globally lock unrelated research objects/projects.
9. Machine processing must not create HumanDecision or claim final scientific authority.
10. Historical observations remain auditable; later observations may supersede operational assessments without erasing prior history.

## Minimum HUMAN-trialable slice
For one canonical research object in Profile A and one investigation direction in Profile B, the Cockpit must show source/evidence traceability plus the available quality dimensions, explicit unknown/not-run states, limitations, and an explainable review suggestion. The HUMAN must be able to inspect the underlying source before making any judgment.

## Acceptance evidence
J15 v0 is ready for HUMAN acceptance only when:
1. Profile A and Profile B both project quality observations from real canonical data.
2. At least one ABSTRACT_ONLY or METADATA_ONLY limitation remains explicit end-to-end.
3. Missing context is represented without fabricating a negative quality judgment.
4. Advice/review prioritization is explainable and cannot auto-decide.
5. HumanDecision write authority remains HUMAN-only.
6. Quality history is reproducible from canonical state and retains prior observations.
7. A HUMAN completes the end-to-end Cockpit trial for both profiles.

## Non-goals
J15 v0 does not prove that a gap exists, that a contribution is novel/significant, that a causal mechanism is true, or that a discovered work is scientifically relevant. It does not replace domain-specific critical appraisal instruments or HUMAN methodological review.
