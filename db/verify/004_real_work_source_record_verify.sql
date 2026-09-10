-- Verify first real OpenAlex Work/SourceRecord path.
-- Read-only; returns one row when the expected candidate is present.
SELECT
    rp.name AS project_name,
    w.id AS work_id,
    w.title,
    w.current_access_level,
    sr.source_record_identifier,
    sr.normalization_state,
    sr.provenance_hash,
    pwr.relevance_state,
    pwr.relevance_advice,
    pwr.human_review_state
FROM research_project rp
JOIN project_work_relevance pwr ON pwr.project_id = rp.id
JOIN work w ON w.id = pwr.work_id
JOIN work_source_record wsr ON wsr.work_id = w.id
JOIN source_record sr ON sr.id = wsr.source_record_id
JOIN literature_source ls ON ls.id = sr.literature_source_id
JOIN work_identifier wi ON wi.work_id = w.id
WHERE rp.id = '3a100000-0000-4000-8000-000000000001'
  AND ls.source_key = 'openalex'
  AND wi.identifier_type = 'OPENALEX'
  AND wi.identifier_value = 'W3139363371';
