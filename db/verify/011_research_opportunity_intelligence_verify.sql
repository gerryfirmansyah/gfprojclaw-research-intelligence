\set ON_ERROR_STOP on
BEGIN;

DO $$
DECLARE
  p uuid := '3a100000-0000-4000-8000-000000000001';
  g uuid := 'edb00111-cf5b-5089-8464-c5f9135a0802';
  a uuid := 'e6478267-0d03-4de7-a25a-50ad2318b29a';
  n integer;
BEGIN
  IF (SELECT current_evolution_state FROM gap_candidate WHERE project_id=p AND id=g) <> 'CANDIDATE' THEN
    RAISE EXCEPTION 'J9 mutated GapCandidate state';
  END IF;

  SELECT count(*) INTO n FROM assessment
   WHERE id=a AND project_id=p AND target_research_object_id=g
     AND assessment_type='RESEARCH_OPPORTUNITY_INTELLIGENCE_V1';
  IF n <> 1 THEN RAISE EXCEPTION 'Expected one J9 opportunity assessment'; END IF;

  SELECT count(*) INTO n FROM assessment_dimension WHERE assessment_id=a;
  IF n <> 4 THEN RAISE EXCEPTION 'Expected four J9 dimensions, got %', n; END IF;

  SELECT count(*) INTO n FROM assessment_dimension
   WHERE assessment_id=a AND dimension_type='REVIEW_PRIORITY'
     AND value_text='HIGH_HUMAN_REVIEW_RECOMMENDED';
  IF n <> 1 THEN RAISE EXCEPTION 'Review priority must remain advisory'; END IF;

  SELECT count(*) INTO n FROM assessment_dimension
   WHERE assessment_id=a
     AND dimension_type IN ('NOVELTY_POTENTIAL','THEORETICAL_SIGNIFICANCE','METHODOLOGICAL_FEASIBILITY')
     AND value_text LIKE 'UNKNOWN%';
  IF n <> 3 THEN RAISE EXCEPTION 'Insufficient-evidence dimensions must remain UNKNOWN'; END IF;

  SELECT count(*) INTO n FROM assessment x JOIN coverage_context cc ON cc.id=x.coverage_context_id
   WHERE x.id=a AND cc.project_id=p;
  IF n <> 1 THEN RAISE EXCEPTION 'J9 assessment lacks project CoverageContext'; END IF;

  SELECT count(*) INTO n FROM evidence_relationship er JOIN claim c ON c.id=er.claim_id
   JOIN evidence_fragment ef ON ef.id=c.evidence_fragment_id
   JOIN work w ON w.id=ef.work_id
   JOIN work_source_record wsr ON wsr.work_id=w.id
   JOIN source_record sr ON sr.id=wsr.source_record_id
   WHERE er.target_research_object_id=g
     AND btrim(sr.source_record_identifier) <> '';
  IF n < 1 THEN RAISE EXCEPTION 'J9 opportunity lacks canonical evidence trace through SourceRecord'; END IF;

  SELECT count(*) INTO n FROM human_decision WHERE assessment_id=a;
  IF n <> 0 THEN RAISE EXCEPTION 'J9 assessment must not auto-create HumanDecision'; END IF;
END $$;

ROLLBACK;
