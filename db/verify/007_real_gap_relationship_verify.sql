SELECT
    p.name AS project_name,
    roi.id AS gap_id,
    roi.canonical_label,
    gc.gap_type,
    gc.statement,
    gc.current_evolution_state,
    er.id AS relationship_id,
    er.semantic_type,
    er.review_state AS relationship_review_state,
    c.id AS claim_id,
    c.review_state AS claim_review_state,
    w.title AS work_title
FROM research_project p
JOIN gap_candidate gc ON gc.project_id = p.id
JOIN research_object_identity roi ON roi.id = gc.id
JOIN evidence_relationship er ON er.target_research_object_id = gc.id
JOIN claim c ON c.id = er.claim_id
JOIN evidence_fragment ef ON ef.id = c.evidence_fragment_id
JOIN work w ON w.id = ef.work_id
WHERE p.id = '3a100000-0000-4000-8000-000000000001'
  AND gc.id = 'edb00111-cf5b-5089-8464-c5f9135a0802';
