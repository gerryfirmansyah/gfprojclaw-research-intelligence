-- Read-only verifier for explicit HUMAN decision persistence.
SELECT
    hd.id AS decision_id,
    hd.project_id,
    roi.canonical_label,
    hd.decision_type,
    hd.rationale,
    hd.actor,
    hd.decided_at,
    hd.supersedes_decision_id,
    hd.coverage_context_id,
    hd.assessment_id
FROM human_decision hd
JOIN research_object_identity roi
  ON roi.id = hd.primary_research_object_id
 AND roi.project_id = hd.project_id
WHERE hd.project_id = '3a100000-0000-4000-8000-000000000001'
ORDER BY hd.decided_at DESC, hd.created_at DESC;
