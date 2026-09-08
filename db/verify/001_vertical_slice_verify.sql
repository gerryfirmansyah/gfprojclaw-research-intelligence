-- GFPROJCLAW — Migration 001 verification
-- J2 SQL Draft v0
-- Run after 001_canonical_vertical_slice.sql and 001_vertical_slice_reference.sql.
-- Fails locally with an exception when a canonical invariant is violated.

DO $$
DECLARE
    expected_tables text[] := ARRAY[
        'research_profile','research_profile_version','research_project','research_project_version',
        'literature_source','source_record','work','work_identifier','work_source_record',
        'project_work_relevance','evidence_fragment','claim','research_object_identity','gap_candidate',
        'evidence_relationship','coverage_context','coverage_source_state','assessment',
        'assessment_dimension','change_event','human_decision'
    ];
    missing_count integer;
BEGIN
    SELECT count(*) INTO missing_count
    FROM unnest(expected_tables) AS t(table_name)
    WHERE NOT EXISTS (
        SELECT 1
        FROM information_schema.tables i
        WHERE i.table_schema = current_schema()
          AND i.table_name = t.table_name
          AND i.table_type = 'BASE TABLE'
    );

    IF missing_count <> 0 THEN
        RAISE EXCEPTION 'Migration 001 verification failed: % canonical tables are missing', missing_count;
    END IF;
END $$;

DO $$
DECLARE
    bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM research_profile p
    JOIN research_profile_version v ON v.id = p.current_version_id
    WHERE v.profile_id <> p.id;
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'Current Profile version ownership invariant failed';
    END IF;

    SELECT count(*) INTO bad_count
    FROM research_project p
    JOIN research_project_version v ON v.id = p.current_version_id
    WHERE v.project_id <> p.id;
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'Current Project version ownership invariant failed';
    END IF;
END $$;

DO $$
DECLARE
    bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM gap_candidate g
    JOIN research_object_identity r ON r.id = g.id
    WHERE r.object_type <> 'GAP_CANDIDATE'
       OR r.project_id IS DISTINCT FROM g.project_id;
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'GapCandidate typed identity invariant failed';
    END IF;
END $$;

DO $$
DECLARE
    bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM claim c
    LEFT JOIN evidence_fragment f ON f.id = c.evidence_fragment_id
    WHERE f.id IS NULL;
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'Atomic Claim provenance invariant failed';
    END IF;

    SELECT count(*) INTO bad_count
    FROM evidence_fragment f
    LEFT JOIN work w ON w.id = f.work_id
    WHERE w.id IS NULL;
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'EvidenceFragment to Work provenance invariant failed';
    END IF;

    SELECT count(*) INTO bad_count
    FROM evidence_fragment f
    JOIN source_record s ON s.id = f.source_record_id
    WHERE s.content_access_state = 'METADATA_ONLY';
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'METADATA_ONLY record produced an EvidenceFragment';
    END IF;
END $$;

DO $$
DECLARE
    bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM assessment a
    JOIN research_object_identity r ON r.id = a.target_research_object_id
    WHERE r.project_id IS DISTINCT FROM a.project_id;
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'Assessment target/project invariant failed';
    END IF;

    SELECT count(*) INTO bad_count
    FROM change_event c
    JOIN research_object_identity r ON r.id = c.primary_research_object_id
    WHERE r.project_id IS DISTINCT FROM c.project_id;
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'ChangeEvent target/project invariant failed';
    END IF;

    SELECT count(*) INTO bad_count
    FROM human_decision h
    JOIN research_object_identity r ON r.id = h.primary_research_object_id
    WHERE r.project_id IS DISTINCT FROM h.project_id;
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'HumanDecision target/project invariant failed';
    END IF;
END $$;

DO $$
DECLARE
    bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM coverage_context c
    JOIN research_project p ON p.id = c.project_id
    JOIN research_profile_version pv ON pv.id = c.profile_version_id
    WHERE pv.profile_id <> p.profile_id;
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'CoverageContext Profile lineage invariant failed';
    END IF;

    SELECT count(*) INTO bad_count
    FROM coverage_context c
    JOIN research_project_version jv ON jv.id = c.project_version_id
    WHERE c.project_version_id IS NOT NULL
      AND jv.project_id <> c.project_id;
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'CoverageContext Project version lineage invariant failed';
    END IF;
END $$;

DO $$
DECLARE
    gap_a uuid := 'a4000000-0000-0000-0000-000000000001';
    gap_b uuid := 'b4000000-0000-0000-0000-000000000001';
    support_count integer;
    challenge_count integer;
    work_count integer;
BEGIN
    SELECT count(*) FILTER (WHERE semantic_type = 'SUPPORTS'),
           count(*) FILTER (WHERE semantic_type IN ('CHALLENGES','CONTRADICTS'))
      INTO support_count, challenge_count
    FROM evidence_relationship
    WHERE target_research_object_id = gap_a;

    IF support_count < 1 OR challenge_count < 1 THEN
        RAISE EXCEPTION 'Profile A fixture does not contain both support and challenge evidence';
    END IF;

    SELECT count(DISTINCT f.work_id) INTO work_count
    FROM evidence_relationship er
    JOIN claim c ON c.id = er.claim_id
    JOIN evidence_fragment f ON f.id = c.evidence_fragment_id
    WHERE er.target_research_object_id = gap_a;

    IF work_count < 2 THEN
        RAISE EXCEPTION 'Profile A evidence trace does not reach at least two Works';
    END IF;

    SELECT count(*) FILTER (WHERE semantic_type = 'SUPPORTS'),
           count(*) FILTER (WHERE semantic_type IN ('CHALLENGES','CONTRADICTS'))
      INTO support_count, challenge_count
    FROM evidence_relationship
    WHERE target_research_object_id = gap_b;

    IF support_count < 1 OR challenge_count < 1 THEN
        RAISE EXCEPTION 'Profile B fixture does not contain both support and challenge evidence';
    END IF;

    SELECT count(DISTINCT f.work_id) INTO work_count
    FROM evidence_relationship er
    JOIN claim c ON c.id = er.claim_id
    JOIN evidence_fragment f ON f.id = c.evidence_fragment_id
    WHERE er.target_research_object_id = gap_b;

    IF work_count < 2 THEN
        RAISE EXCEPTION 'Profile B evidence trace does not reach at least two Works';
    END IF;
END $$;

DO $$
DECLARE
    bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM claim c
    JOIN evidence_fragment f ON f.id = c.evidence_fragment_id
    WHERE c.quarantine_state = 'ACTIVE'
      AND f.quarantine_state = 'QUARANTINED';
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'Active Claim depends on a quarantined EvidenceFragment';
    END IF;

    SELECT count(*) INTO bad_count
    FROM evidence_relationship er
    JOIN claim c ON c.id = er.claim_id
    WHERE er.review_state <> 'QUARANTINED'
      AND c.quarantine_state = 'QUARANTINED';
    IF bad_count <> 0 THEN
        RAISE EXCEPTION 'Non-quarantined EvidenceRelationship depends on a quarantined Claim';
    END IF;
END $$;

DO $$
DECLARE
    a_profile_count integer;
    b_profile_count integer;
    a_project_count integer;
    b_project_count integer;
BEGIN
    SELECT count(*) INTO a_profile_count
    FROM research_profile
    WHERE id = 'a0000000-0000-0000-0000-000000000001';
    SELECT count(*) INTO b_profile_count
    FROM research_profile
    WHERE id = 'b0000000-0000-0000-0000-000000000001';
    SELECT count(*) INTO a_project_count
    FROM research_project
    WHERE id = 'a2000000-0000-0000-0000-000000000001';
    SELECT count(*) INTO b_project_count
    FROM research_project
    WHERE id = 'b2000000-0000-0000-0000-000000000001';

    IF a_profile_count <> 1 OR b_profile_count <> 1 OR a_project_count <> 1 OR b_project_count <> 1 THEN
        RAISE EXCEPTION 'Cross-domain fixture identities are incomplete';
    END IF;
END $$;

-- Inspectable end-to-end evidence trace for both reference Profiles.
SELECT
    p.name AS profile,
    pr.name AS project,
    roi.canonical_label AS research_object,
    g.gap_type,
    g.current_evolution_state,
    er.semantic_type,
    c.claim_text,
    f.fragment_type,
    w.title AS work_title,
    ls.name AS literature_source,
    sr.source_record_identifier
FROM gap_candidate g
JOIN research_object_identity roi ON roi.id = g.id
JOIN research_project pr ON pr.id = g.project_id
JOIN research_profile p ON p.id = pr.profile_id
JOIN evidence_relationship er ON er.target_research_object_id = g.id
JOIN claim c ON c.id = er.claim_id
JOIN evidence_fragment f ON f.id = c.evidence_fragment_id
JOIN work w ON w.id = f.work_id
LEFT JOIN source_record sr ON sr.id = f.source_record_id
LEFT JOIN literature_source ls ON ls.id = sr.literature_source_id
ORDER BY p.name, roi.canonical_label, er.semantic_type, w.title;

-- HUMAN authority remains separate from machine advice.
SELECT
    p.name AS profile,
    pr.name AS project,
    roi.canonical_label AS research_object,
    a.assessment_type,
    a.explanation_summary AS machine_advice,
    h.decision_type AS human_decision,
    h.rationale AS human_rationale,
    h.actor,
    h.decided_at
FROM human_decision h
JOIN research_project pr ON pr.id = h.project_id
JOIN research_profile p ON p.id = pr.profile_id
JOIN research_object_identity roi ON roi.id = h.primary_research_object_id
LEFT JOIN assessment a ON a.id = h.assessment_id
ORDER BY p.name, h.decided_at;

-- Coverage is context, never a scientific verdict or global gate.
SELECT
    p.name AS profile,
    pr.name AS project,
    cc.observed_at,
    cc.counter_search_state,
    ls.name AS source,
    css.health_state,
    css.attempted_record_count,
    css.observed_record_count,
    css.degradation_reason,
    cc.limitations
FROM coverage_context cc
JOIN research_project pr ON pr.id = cc.project_id
JOIN research_profile p ON p.id = pr.profile_id
JOIN coverage_source_state css ON css.coverage_context_id = cc.id
JOIN literature_source ls ON ls.id = css.literature_source_id
ORDER BY p.name, ls.name;

SELECT 'J2 Migration 001 vertical slice verification passed' AS verification_result;
