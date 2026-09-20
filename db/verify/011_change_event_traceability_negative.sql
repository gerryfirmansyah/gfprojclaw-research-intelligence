\set ON_ERROR_STOP on

CREATE OR REPLACE FUNCTION pg_temp.expect_failure(label text, sql_text text)
RETURNS void LANGUAGE plpgsql AS $$
DECLARE failed boolean := false;
BEGIN
  BEGIN
    EXECUTE sql_text;
  EXCEPTION WHEN integrity_constraint_violation THEN
    failed := true;
    RAISE NOTICE 'expected rejection confirmed: %', label;
  END;
  IF NOT failed THEN
    RAISE EXCEPTION 'expected integrity rejection did not occur: %', label;
  END IF;
END $$;

BEGIN;

SELECT pg_temp.expect_failure(
  'ASSESSMENT_CHANGED without current Assessment',
  $$INSERT INTO change_event
    (id,project_id,primary_research_object_id,change_type,observed_at,reasoning_delta)
    SELECT gen_random_uuid(),project_id,primary_research_object_id,
           'ASSESSMENT_CHANGED',now(),'negative test'
    FROM change_event LIMIT 1$$
);

SELECT pg_temp.expect_failure(
  'invalid evidence role',
  $$INSERT INTO change_event_evidence
    (change_event_id,evidence_relationship_id,target_research_object_id,role)
    SELECT ce.id,er.id,ce.primary_research_object_id,'PROVES'
    FROM change_event ce
    JOIN evidence_relationship er
      ON er.target_research_object_id=ce.primary_research_object_id
    LIMIT 1$$
);

SELECT pg_temp.expect_failure(
  'cross-object evidence relationship',
  $$INSERT INTO change_event_evidence
    (change_event_id,evidence_relationship_id,target_research_object_id,role)
    SELECT ce.id,er.id,ce.primary_research_object_id,'TRIGGER'
    FROM change_event ce
    JOIN evidence_relationship er
      ON er.target_research_object_id<>ce.primary_research_object_id
    LIMIT 1$$
);

-- MATCH SIMPLE intentionally permits NULL in the composite FK for an initial Assessment.
-- Prove that it cannot hide a real canonical supersession: create a current Assessment
-- that canonically supersedes another Assessment, then omit that previous Assessment
-- from the ChangeEvent transition. The insert must be rejected.
WITH base AS (
  SELECT * FROM assessment ORDER BY assessed_at LIMIT 1
)
INSERT INTO assessment (
  id, project_id, target_research_object_id, coverage_context_id,
  assessment_type, model_or_agent, model_version, explanation_summary,
  assessed_at, supersedes_assessment_id
)
SELECT '05000000-0000-0000-0000-000000000099'::uuid,
       project_id, target_research_object_id, coverage_context_id,
       assessment_type, model_or_agent, model_version,
       'Negative-test superseding Assessment', assessed_at + interval '1 minute', id
FROM base;

SELECT pg_temp.expect_failure(
  'superseding current Assessment cannot omit canonical previous Assessment',
  $$INSERT INTO change_event (
      id,project_id,primary_research_object_id,change_type,observed_at,reasoning_delta,
      current_assessment_id,current_supersedes_assessment_id,previous_assessment_id
    )
    SELECT gen_random_uuid(),project_id,target_research_object_id,
           'ASSESSMENT_CHANGED',now(),'negative supersession omission test',
           id,NULL,NULL
    FROM assessment
    WHERE id='05000000-0000-0000-0000-000000000099'::uuid$$
);

-- The same superseding Assessment must succeed when the canonical previous Assessment
-- is recorded exactly. This row remains inside the rollback-only negative-test transaction.
INSERT INTO change_event (
  id,project_id,primary_research_object_id,change_type,observed_at,reasoning_delta,
  current_assessment_id,current_supersedes_assessment_id,previous_assessment_id
)
SELECT '06000000-0000-0000-0000-000000000099'::uuid,
       project_id,target_research_object_id,'ASSESSMENT_CHANGED',now(),
       'positive control for exact canonical supersession',
       id,supersedes_assessment_id,supersedes_assessment_id
FROM assessment
WHERE id='05000000-0000-0000-0000-000000000099'::uuid;

SELECT pg_temp.expect_failure(
  'cross-object current Assessment',
  $$UPDATE change_event ce
    SET current_assessment_id=a.id,
        current_supersedes_assessment_id=a.supersedes_assessment_id,
        previous_assessment_id=a.supersedes_assessment_id
    FROM assessment a
    WHERE a.target_research_object_id<>ce.primary_research_object_id$$
);

ROLLBACK;

DO $$
BEGIN
 IF EXISTS (SELECT 1 FROM change_event_evidence) THEN
   RAISE EXCEPTION 'historical evidence trigger backfill must remain empty';
 END IF;
END $$;

SELECT 'J15 change-event traceability negative tests passed' AS result;
