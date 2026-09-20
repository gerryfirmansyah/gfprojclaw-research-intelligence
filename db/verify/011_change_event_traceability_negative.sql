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
