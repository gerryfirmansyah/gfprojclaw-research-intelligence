# J15 Explainable Advice & Critic v0

HUMAN trial feedback identified that machine status/value labels alone are not sufficient for scientific review. Every displayed Advice & Critic dimension must expose its persisted explanation, and the assessment must expose the canonical evidence basis that the HUMAN can cross-check in Evidence Verification.

## Reviewable projection
Advice & Critic now projects the persisted assessment explanation summary; every persisted dimension value plus its assessment_dimension explanation; explicit evidence basis including Work, Claim text, EvidenceRelationship semantic type and rationale, access level, Claim review state, and relationship review state; CoverageContext counter-search state and limitation; and an explicit instruction to verify the reasoning against Evidence Verification/source before stronger scientific acceptance.

## Profile A runtime proof
The current canonical ADVICE_CRITIC_V1 has three explained dimensions: COUNTER_EVIDENCE_RISK, EVIDENCE_COVERAGE_CONTEXT, and REVIEW_PRIORITY. Its evidence basis contains one SUPPORTS relationship whose Claim is NEEDS_REVIEW, relationship is MACHINE_SUGGESTED, and evidence access is ABSTRACT_ONLY. Counter-search remains NOT_RUN.

## Guardrails
The UI does not generate scientific reasoning that is absent from canonical state. Missing explanation/rationale is labeled unavailable. Explanation is review material, not proof of novelty, truth, relevance, causality, acceptance, or a scientific verdict.

## Acceptance gap
J15 remains pending HUMAN browser re-trial of the explainable Advice & Critic presentation and verification against the stored abstract/source.
