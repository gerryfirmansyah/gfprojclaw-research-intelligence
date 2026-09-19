# J15 Quality API Checkpoint v0

## Runtime proof
The read-only quality projection is exposed at:
`GET /api/projects/{project_id}/quality?object_id={research_object_id}`.

Local Cockpit API and the public API endpoint were exercised against production canonical data.

### Profile A
Target: `edb00111-cf5b-5089-8464-c5f9135a0802`.

Observed:
- GAP_CANDIDATE / CANDIDATE.
- latest HUMAN decision: ACCEPT_DIRECTION.
- linked evidence access remains ABSTRACT_ONLY.
- Claim review remains NEEDS_REVIEW.
- EvidenceRelationship review remains MACHINE_SUGGESTED.
- methodological context is NOT_AVAILABLE.
- counter-search remains NOT_RUN.
- coverage limitation remains explicit.
- review suggestions explain their triggering observations.
- `scientific_decision=false`.

### Profile B
Target: `3b200000-0000-4000-8000-000000000013`.

Observed:
- INVESTIGATION_DIRECTION / INVESTIGATING.
- latest HUMAN decision: ACCEPT_DIRECTION.
- no canonical EvidenceRelationship is asserted for this direction.
- evidence references are therefore empty.
- project literature is not silently promoted to object evidence.
- review suggestion is ESTABLISH_EXPLICIT_EVIDENCE_LINKAGE.
- `scientific_decision=false`.

## Guardrail
This endpoint performs SELECT/projection only. It does not create Assessment, Claim, EvidenceRelationship, GapCandidate, InvestigationDirection, ChangeEvent, or HumanDecision records. Existing HUMAN decisions are context only.

## Remaining J15 acceptance work
The quality observations are API-visible but are not yet a HUMAN-trialable Cockpit surface. J15 overall HUMAN PASS therefore remains pending UI integration, end-to-end HUMAN trial for both profiles, and a decision on whether persistent quality-history dimensions require a narrow reviewed migration.
