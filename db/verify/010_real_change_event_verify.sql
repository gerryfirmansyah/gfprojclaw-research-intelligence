-- Read-only verifier for the first real J8 ChangeEvent slice.
SELECT
    ce.id AS change_event_id,
    ce.project_id,
    ce.primary_research_object_id,
    roi.canonical_label,
    ce.coverage_context_id,
    ce.change_type,
    ce.observed_at,
    ce.previous_state_jsonb,
    ce.current_state_jsonb,
    ce.reasoning_delta
FROM change_event ce
JOIN research_object_identity roi
  ON roi.id = ce.primary_research_object_id
 AND roi.project_id = ce.project_id
WHERE ce.id = '10d5b1f3-5248-5bba-9400-d3dd1b2de146'::uuid;
