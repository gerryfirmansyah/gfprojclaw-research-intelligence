-- GFPROJCLAW — Migration 001 negative integrity tests
-- J2 Disposable PostgreSQL Test Cycle v0
-- Requires Migration 001 + deterministic fixture. Test-only; never production data.
-- This file covers invariants expected to be rejected directly by DDL constraints.
-- Verifier-level negative cases are exercised separately by the workflow.

CREATE OR REPLACE FUNCTION pg_temp.expect_failure(test_name text, statement text)
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
    rejected boolean := false;
BEGIN
    BEGIN
        EXECUTE statement;
    EXCEPTION WHEN others THEN
        rejected := true;
        RAISE NOTICE 'PASS % rejected locally: %', test_name, SQLERRM;
    END;

    IF NOT rejected THEN
        RAISE EXCEPTION 'FAIL %: invalid mutation was accepted', test_name;
    END IF;
END;
$$;

SELECT pg_temp.expect_failure('N01 invalid Profile status',
    $q$UPDATE research_profile SET status='INVALID' WHERE id='a0000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N02 current Profile version crossing Profile lineage',
    $q$UPDATE research_profile SET current_version_id='b1000000-0000-0000-0000-000000000001' WHERE id='a0000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N03 current Project version crossing Project lineage',
    $q$UPDATE research_project SET current_version_id='b3000000-0000-0000-0000-000000000001' WHERE id='a2000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N04 duplicate Work identifier',
    $q$UPDATE work_identifier SET identifier_value='fixture:a:support' WHERE id='e1000000-0000-0000-0000-000000000002'$q$);

SELECT pg_temp.expect_failure('N05 EvidenceFragment cannot be METADATA_ONLY',
    $q$UPDATE evidence_fragment SET access_level='METADATA_ONLY' WHERE id='01000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N07 GapCandidate Project inconsistent with identity',
    $q$UPDATE gap_candidate SET project_id='b2000000-0000-0000-0000-000000000001' WHERE id='a4000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N08 Assessment target/project mismatch',
    $q$UPDATE assessment SET project_id='b2000000-0000-0000-0000-000000000001' WHERE id='05000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N09 ChangeEvent target/project mismatch',
    $q$UPDATE change_event SET project_id='b2000000-0000-0000-0000-000000000001' WHERE id='06000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N10 HumanDecision target/project mismatch',
    $q$UPDATE human_decision SET project_id='b2000000-0000-0000-0000-000000000001' WHERE id='07000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N11 invalid HumanDecision type',
    $q$UPDATE human_decision SET decision_type='AUTO_ACCEPT' WHERE id='07000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N12 quarantined EvidenceFragment requires reason',
    $q$UPDATE evidence_fragment SET quarantine_state='QUARANTINED', quarantine_reason=NULL WHERE id='01000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N16 EvidenceFragment SourceRecord normalized to another Work',
    $q$UPDATE evidence_fragment SET source_record_id='d0000000-0000-0000-0000-000000000002' WHERE id='01000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N17 HumanDecision cites Assessment from another Project/object',
    $q$UPDATE human_decision SET assessment_id='05000000-0000-0000-0000-000000000002' WHERE id='07000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N18 Assessment cites CoverageContext from another Project',
    $q$UPDATE assessment SET coverage_context_id='04000000-0000-0000-0000-000000000002' WHERE id='05000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N19 Profile version supersession crosses Profile lineage',
    $q$UPDATE research_profile_version SET supersedes_version_id='b1000000-0000-0000-0000-000000000001' WHERE id='a1000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N19 Project version supersession crosses Project lineage',
    $q$UPDATE research_project_version SET supersedes_version_id='b3000000-0000-0000-0000-000000000001' WHERE id='a3000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N19 Assessment supersession crosses target lineage',
    $q$UPDATE assessment SET supersedes_assessment_id='05000000-0000-0000-0000-000000000002' WHERE id='05000000-0000-0000-0000-000000000001'$q$);

SELECT pg_temp.expect_failure('N19 HumanDecision supersession crosses target lineage',
    $q$UPDATE human_decision SET supersedes_decision_id='07000000-0000-0000-0000-000000000002' WHERE id='07000000-0000-0000-0000-000000000001'$q$);

SELECT 'J2 Migration 001 hard negative integrity tests passed' AS negative_test_result;
