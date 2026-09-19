# J15 Canonical Quality Projection v0

## Projection rule
The first J15 slice is read-only and deterministic. It derives quality observations from existing canonical state and never writes an Assessment, HumanDecision, Claim, EvidenceRelationship, or scientific verdict.

## Object envelope
For each active research object expose:
- object id/type/label/state and latest HUMAN decision context;
- evidence traceability summary;
- decomposed quality observations;
- limitations and unknown/not-run states;
- explainable review suggestion.

## Dimensions and derivation

### ACCESS_COMPLETENESS
EvidenceFragment.access_level and Work.current_access_level. Preserve FULL_TEXT / ABSTRACT_ONLY / METADATA_ONLY. If no evidence is linked, NOT_AVAILABLE.

### PROVENANCE_COMPLETENESS
Observe whether evidence can be traced through Claim -> EvidenceFragment -> Work and, where available, SourceRecord/LiteratureSource identifiers. Missing links produce PARTIAL or NOT_AVAILABLE, not a scientific penalty.

### EXTRACTION_REVIEW_STATE
Project Claim.review_state and EvidenceRelationship.review_state without converting them to a numeric score. If no claim/relationship exists, NOT_AVAILABLE.

### METHODOLOGICAL_CONTEXT_AVAILABILITY
Only AVAILABLE when explicit canonical methodological context is present in the evidence/claim scope. Otherwise NOT_AVAILABLE. Never infer poor methodology from absence.

### CORROBORATION_CONTEXT
Report linked supporting/extension relationships and distinct works when canonical relationships exist. If none exist, NOT_RUN/NOT_AVAILABLE rather than NO_CORROBORATION.

### CONTRADICTION_CONTEXT
Report canonical CHALLENGES/CONTRADICTS/counter-evidence context when present. Counter-search state NOT_RUN must remain visible.

### RECENCY_CONTEXT
Expose publication year/date and retrieval/coverage observation time as context. Do not label older work low quality merely because it is older.

### SOURCE_COVERAGE_LIMITATIONS
Project CoverageContext limitations, source health/degradation/access limitations, and coverage counter-search state.

## Explainable review suggestion v0
Suggestions are rule-based attention cues, never verdicts. Examples:
- ABSTRACT_ONLY -> inspect full text when the scientific decision depends on details unavailable in the abstract.
- NEEDS_REVIEW/MACHINE_SUGGESTED -> prioritize HUMAN inspection of extraction/relationship.
- counter_search_state=NOT_RUN -> consider counter-search before a novelty/gap judgment.
- methodological context NOT_AVAILABLE -> inspect source/method section before methodological appraisal.
- source DEGRADED -> treat coverage as incomplete until source health recovers.

Every suggestion must name the observations that triggered it.

## Profile A trial target
Gap Candidate `edb00111-cf5b-5089-8464-c5f9135a0802`. Its existing ABSTRACT_ONLY evidence and NOT_RUN counter-search must remain explicit; ACCEPT_DIRECTION is HUMAN direction acceptance, not proof of the gap.

## Profile B trial target
Investigation Direction `3b200000-0000-4000-8000-000000000013`. The projection must show that no EvidenceRelationship is currently asserted for this direction. Existing literature chains may provide project context but must not be presented as evidence for the direction without an explicit canonical relationship.

## API shape candidate
`GET /api/projects/{project_id}/quality?object_id={research_object_id}`

Response should contain `object`, `observations[]`, `limitations[]`, `review_suggestions[]`, `scientific_decision=false`, and source/evidence references sufficient for Cockpit drill-down.
