-- Read-only verifier for the first real GapCandidate machine Assessment.
SELECT
    a.id AS assessment_id,
    a.project_id,
    a.target_research_object_id AS gap_id,
    roi.canonical_label,
    a.coverage_context_id,
    a.assessment_type,
    a.model_or_agent,
    a.model_version,
    a.explanation_summary,
    a.assessed_at,
    ad.dimension_type,
    ad.value_numeric,
    ad.value_text,
    ad.explanation
FROM assessment a
JOIN research_object_identity roi ON roi.id = a.target_research_object_id
JOIN assessment_dimension ad ON ad.assessment_id = a.id
WHERE a.project_id = '3a100000-0000-4000-8000-000000000001'
  AND a.target_research_object_id = 'edb00111-cf5b-5089-8464-c5f9135a0802'
ORDER BY ad.dimension_type;
