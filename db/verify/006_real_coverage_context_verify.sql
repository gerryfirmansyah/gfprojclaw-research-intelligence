\pset pager off

SELECT cc.id AS coverage_context_id,
       p.name AS project_name,
       cc.observed_at,
       cc.access_summary_jsonb,
       cc.extraction_summary_jsonb,
       cc.counter_search_state,
       cc.limitations,
       ls.source_key,
       css.health_state,
       css.observed_record_count,
       css.access_limitations
FROM coverage_context cc
JOIN research_project p ON p.id = cc.project_id
LEFT JOIN coverage_source_state css ON css.coverage_context_id = cc.id
LEFT JOIN literature_source ls ON ls.id = css.literature_source_id
WHERE cc.project_id = '3a100000-0000-4000-8000-000000000001'
ORDER BY cc.observed_at DESC
LIMIT 10;
