-- GFPROJCLAW — Migration 001 fixture verification
-- J2 SQL Draft v1 — Pre-Test Corrections
-- TEST ONLY. Requires db/fixtures/001_vertical_slice_reference.sql.
-- Never run this verifier as a reason to load synthetic fixtures into production.

DO $$
DECLARE bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM research_profile
    WHERE id IN (
        'a0000000-0000-0000-0000-000000000001',
        'b0000000-0000-0000-0000-000000000001'
    ) AND current_version_id IS NULL;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Fixture Profile current-version pointer missing'; END IF;

    SELECT count(*) INTO bad_count
    FROM research_project
    WHERE id IN (
        'a2000000-0000-0000-0000-000000000001',
        'b2000000-0000-0000-0000-000000000001'
    ) AND current_version_id IS NULL;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Fixture Project current-version pointer missing'; END IF;
END $$;

DO $$
DECLARE
    gap_id uuid;
    support_count integer;
    challenge_count integer;
    work_count integer;
BEGIN
    FOREACH gap_id IN ARRAY ARRAY[
        'a4000000-0000-0000-0000-000000000001'::uuid,
        'b4000000-0000-0000-0000-000000000001'::uuid
    ]
    LOOP
        SELECT count(*) FILTER (WHERE semantic_type = 'SUPPORTS'),
               count(*) FILTER (WHERE semantic_type IN ('CHALLENGES','CONTRADICTS'))
          INTO support_count, challenge_count
        FROM evidence_relationship
        WHERE target_research_object_id = gap_id;

        IF support_count < 1 OR challenge_count < 1 THEN
            RAISE EXCEPTION 'Fixture Gap % lacks both support and challenge evidence', gap_id;
        END IF;

        SELECT count(DISTINCT f.work_id) INTO work_count
        FROM evidence_relationship er
        JOIN claim c ON c.id = er.claim_id
        JOIN evidence_fragment f ON f.id = c.evidence_fragment_id
        JOIN work_source_record wsr
          ON wsr.work_id = f.work_id
         AND wsr.source_record_id = f.source_record_id
        JOIN source_record sr ON sr.id = wsr.source_record_id
        JOIN literature_source ls ON ls.id = sr.literature_source_id
        WHERE er.target_research_object_id = gap_id;

        IF work_count < 2 THEN
            RAISE EXCEPTION 'Fixture Gap % evidence trace does not reach at least two Works', gap_id;
        END IF;
    END LOOP;
END $$;

DO $$
DECLARE bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM human_decision h
    JOIN assessment a ON a.id = h.assessment_id
    WHERE h.project_id IN (
        'a2000000-0000-0000-0000-000000000001',
        'b2000000-0000-0000-0000-000000000001'
    )
      AND (a.project_id <> h.project_id OR a.target_research_object_id <> h.primary_research_object_id);
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Fixture HumanDecision/Assessment lineage failed'; END IF;

    SELECT count(*) INTO bad_count
    FROM research_project p
    WHERE p.id IN (
        'a2000000-0000-0000-0000-000000000001',
        'b2000000-0000-0000-0000-000000000001'
    )
      AND NOT EXISTS (SELECT 1 FROM human_decision h WHERE h.project_id = p.id)
      AND NOT EXISTS (SELECT 1 FROM assessment a WHERE a.project_id = p.id);
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Fixture lacks separate Assessment/HumanDecision rows'; END IF;
END $$;

DO $$
DECLARE bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM research_project p
    WHERE p.id IN (
        'a2000000-0000-0000-0000-000000000001',
        'b2000000-0000-0000-0000-000000000001'
    )
      AND NOT EXISTS (
        SELECT 1
        FROM coverage_context cc
        JOIN coverage_source_state css ON css.coverage_context_id = cc.id
        WHERE cc.project_id = p.id AND css.health_state = 'DEGRADED'
      );
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Fixture Project lacks degraded-source coverage context'; END IF;
END $$;

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
JOIN work_source_record wsr ON wsr.work_id = f.work_id AND wsr.source_record_id = f.source_record_id
JOIN source_record sr ON sr.id = wsr.source_record_id
JOIN literature_source ls ON ls.id = sr.literature_source_id
WHERE p.id IN (
    'a0000000-0000-0000-0000-000000000001',
    'b0000000-0000-0000-0000-000000000001'
)
ORDER BY p.name, roi.canonical_label, er.semantic_type, w.title;

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
WHERE p.id IN (
    'a0000000-0000-0000-0000-000000000001',
    'b0000000-0000-0000-0000-000000000001'
)
ORDER BY p.name, h.decided_at;

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
WHERE p.id IN (
    'a0000000-0000-0000-0000-000000000001',
    'b0000000-0000-0000-0000-000000000001'
)
ORDER BY p.name, ls.name;

SELECT 'J2 Migration 001 fixture verification passed' AS verification_result;
