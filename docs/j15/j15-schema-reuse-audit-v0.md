# J15 Schema Reuse Audit v0

## Finding
The canonical schema already contains most structural primitives needed for a J15 vertical slice: source access state, Claim/EvidenceRelationship review states, CoverageContext/SourceState, Assessment lineage, ChangeEvent history, and HumanDecision linkage. J15 should reuse these rather than create a parallel quality subsystem.

## Constraint discovered
`assessment_dimension.dimension_type` is a closed CHECK enum containing J9/J10 dimensions only. The J15 decomposed observations (access completeness, provenance completeness, extraction review state, methodological context availability, corroboration, contradiction, recency, source/coverage limitations) cannot be persisted honestly as new assessment dimensions without a reviewed migration or an explicitly different canonical representation.

## Recommended boundary
Start J15 with a read/projection layer that derives inspectable observations from existing canonical fields and marks unavailable context explicitly. Do not force J15 observations into existing J9/J10 dimension labels. After the Profile A/B projection is HUMAN-trialable, decide whether persistent quality-assessment history requires a narrow migration extending the allowed dimension types.

## Existing canonical inputs
- `source_record.content_access_state`
- `claim.review_state` and extraction origin/scope
- `evidence_relationship.review_state`
- `coverage_context.access_summary_jsonb`, `extraction_summary_jsonb`, `counter_search_state`, `limitations`
- `coverage_source_state.health_state`, counts, access limitations, degradation reason
- `assessment` lineage and explanations
- `change_event` history
- explicit `human_decision` authority

## Guardrail
Absence of a canonical field or full text must project as UNKNOWN/NOT_AVAILABLE/NOT_RUN, never as a fabricated negative quality judgment.
