-- J3 reference Project bootstrap verification v0
-- Safe read-only production verification; creates no scientific objects.

SELECT
    rp.name AS profile,
    p.name AS project,
    p.status,
    v.version_no,
    v.research_intent,
    v.provisional_rq_text,
    v.project_configuration_jsonb->>'schema_version' AS schema_version,
    (p.current_version_id = v.id) AS current_ok
FROM research_profile rp
JOIN research_project p ON p.profile_id = rp.id
JOIN research_project_version v ON v.id = p.current_version_id
WHERE p.created_by = 'j3-reference-project-bootstrap-v0'
ORDER BY rp.name;
