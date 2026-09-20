\set ON_ERROR_STOP on

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema='public' AND table_name='change_event'
      AND column_name='current_assessment_id'
  ) THEN RAISE EXCEPTION 'current_assessment_id missing'; END IF;

  IF to_regclass('public.change_event_evidence') IS NULL THEN
    RAISE EXCEPTION 'change_event_evidence missing';
  END IF;

  IF EXISTS (
    SELECT 1 FROM change_event ce
    JOIN assessment a ON a.id=ce.current_assessment_id
    WHERE a.project_id<>ce.project_id
       OR a.target_research_object_id<>ce.primary_research_object_id
  ) THEN RAISE EXCEPTION 'ChangeEvent/Assessment lineage mismatch'; END IF;

  IF EXISTS (
    SELECT 1 FROM change_event
    WHERE change_type='ASSESSMENT_CHANGED' AND current_assessment_id IS NULL
  ) THEN RAISE EXCEPTION 'ASSESSMENT_CHANGED missing current Assessment'; END IF;

  IF EXISTS (
    SELECT 1 FROM change_event_evidence cee
    JOIN change_event ce ON ce.id=cee.change_event_id
    JOIN evidence_relationship er ON er.id=cee.evidence_relationship_id
    WHERE cee.target_research_object_id<>ce.primary_research_object_id
       OR cee.target_research_object_id<>er.target_research_object_id
  ) THEN RAISE EXCEPTION 'ChangeEvent evidence object lineage mismatch'; END IF;
END $$;

SELECT 'J15 change-event traceability schema verification passed' AS result;
