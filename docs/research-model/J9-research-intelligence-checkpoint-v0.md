# J9 Research Intelligence — Exit Checkpoint v0

Status: implementation checkpoint; final deployment/commit verification pending.

## Scope

J9 turns persisted `GapCandidate` evidence into research-opportunity context for HUMAN scientific review. Prioritization is advisory only: it does not establish novelty, significance, feasibility, acceptance, or scientific truth.

## Implemented vertical slice

- Opportunity engine uses canonical `GapCandidate`, `EvidenceRelationship`, `Assessment`, `AssessmentDimension`, and `CoverageContext` objects.
- Four advisory dimensions are persisted: `REVIEW_PRIORITY`, `NOVELTY_POTENTIAL`, `THEORETICAL_SIGNIFICANCE`, and `METHODOLOGICAL_FEASIBILITY`.
- Assessment persistence is idempotent for the same project/gap/coverage/type/model/version context.
- API exposes research opportunities with evidence counts, coverage context, advisory assessment, and latest HUMAN decision context.
- Evidence trace remains canonical: `EvidenceRelationship → Claim → EvidenceFragment → Work → WorkSourceRecord → SourceRecord`.
- Research Opportunities UI renders advisory dimensions, coverage limitations, and canonical evidence trace.

## Authority boundaries

J9 does not automatically create `HumanDecision`, does not automatically mutate `GapCandidate` state, and does not convert advisory ranking into a final verdict. HUMAN scientific judgment remains authoritative.

## Validation evidence

- Production-backed opportunity assessment dry-run passed on the persisted Project A gap.
- Persistence apply created/reused `RESEARCH_OPPORTUNITY_INTELLIGENCE_V1` with exactly four advisory dimensions.
- Idempotency rerun reused the same Assessment rather than duplicating it.
- Boundary verification confirmed the target gap remains `CANDIDATE`; the existing HUMAN decision is not linked to the J9 assessment.
- SQL verifier `db/verify/011_research_opportunity_intelligence_verify.sql` passed (`BEGIN`, `DO`, `ROLLBACK`) after adding canonical SourceRecord trace validation.
- Local API validation returned the persisted opportunity, assessment, coverage limitation, and evidence trace through SourceRecord.
- `node --check prototype/app.js` passed after wiring `loadProjectOpportunities()`.
- `git diff --check` passed after the J9 UI/API edits.

## Remaining exit work

Before declaring J9 complete: rerun final static/runtime checks where tool policy permits, review the complete diff/status, commit and push the J9 slice, verify deployment/workflow and live Research Opportunities behavior, then update this checkpoint to final PASS.

## Exit criterion

J9 exits only when evidence-backed research opportunities are inspectable end-to-end while prioritization remains explicitly advisory, coverage limitations remain visible, provenance remains traceable to canonical source records, and HUMAN scientific authority is preserved.
