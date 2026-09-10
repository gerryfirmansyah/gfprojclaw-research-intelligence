-- Read-only verification for first real EvidenceFragment / Claim path.
SELECT
    p.name AS project_name,
    w.title AS work_title,
    ef.id AS evidence_fragment_id,
    ef.fragment_type,
    ef.access_level,
    ef.extraction_version,
    ef.quarantine_state,
    c.id AS claim_id,
    c.claim_type,
    c.review_state,
    c.extraction_origin,
    c.claim_text
FROM research_project p
JOIN project_work_relevance pwr ON pwr.project_id = p.id
JOIN work w ON w.id = pwr.work_id
JOIN evidence_fragment ef ON ef.work_id = w.id
JOIN claim c ON c.evidence_fragment_id = ef.id
JOIN work_identifier wi ON wi.work_id = w.id
WHERE p.id = '3a100000-0000-4000-8000-000000000001'
  AND wi.identifier_type = 'OPENALEX'
  AND wi.identifier_value = 'W3139363371';
