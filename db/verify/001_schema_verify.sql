-- GFPROJCLAW — Migration 001 production-safe schema/integrity verification
-- J2 SQL Draft v1 — Pre-Test Corrections
-- Safe on production after migration; requires no synthetic fixture rows.

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
        SELECT 1 FROM information_schema.tables i
        WHERE i.table_schema = current_schema()
          AND i.table_name = t.table_name
          AND i.table_type = 'BASE TABLE'
    );
    IF missing_count <> 0 THEN
        RAISE EXCEPTION 'Migration 001 verification failed: % canonical tables are missing', missing_count;
    END IF;
END $$;

DO $$
DECLARE bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM research_profile p
    JOIN research_profile_version v ON v.id = p.current_version_id
    WHERE v.profile_id <> p.id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Current Profile version ownership invariant failed'; END IF;

    SELECT count(*) INTO bad_count
    FROM research_project p
    JOIN research_project_version v ON v.id = p.current_version_id
    WHERE v.project_id <> p.id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Current Project version ownership invariant failed'; END IF;
END $$;

DO $$
DECLARE bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM research_profile_version v
    JOIN research_profile_version s ON s.id = v.supersedes_version_id
    WHERE s.profile_id <> v.profile_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Profile-version supersession crossed Profile lineage'; END IF;

    SELECT count(*) INTO bad_count
    FROM research_project_version v
    JOIN research_project_version s ON s.id = v.supersedes_version_id
    WHERE s.project_id <> v.project_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Project-version supersession crossed Project lineage'; END IF;
END $$;

DO $$
DECLARE bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM research_object_identity r
    JOIN research_project p ON p.id = r.project_id
    WHERE r.project_id IS NOT NULL
      AND r.profile_id IS DISTINCT FROM p.profile_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'ResearchObject Profile/Project lineage invariant failed'; END IF;

    SELECT count(*) INTO bad_count
    FROM gap_candidate g
    JOIN research_object_identity r ON r.id = g.id
    WHERE r.object_type <> 'GAP_CANDIDATE'
       OR r.project_id IS DISTINCT FROM g.project_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'GapCandidate typed identity invariant failed'; END IF;
END $$;

DO $$
DECLARE bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM evidence_fragment f
    LEFT JOIN work w ON w.id = f.work_id
    WHERE w.id IS NULL;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'EvidenceFragment to Work provenance invariant failed'; END IF;

    SELECT count(*) INTO bad_count
    FROM claim c
    LEFT JOIN evidence_fragment f ON f.id = c.evidence_fragment_id
    WHERE f.id IS NULL;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Atomic Claim provenance invariant failed'; END IF;

    SELECT count(*) INTO bad_count
    FROM evidence_fragment f
    JOIN source_record s ON s.id = f.source_record_id
    WHERE s.content_access_state = 'METADATA_ONLY';
    IF bad_count <> 0 THEN RAISE EXCEPTION 'METADATA_ONLY SourceRecord produced an EvidenceFragment'; END IF;

    SELECT count(*) INTO bad_count
    FROM evidence_fragment f
    LEFT JOIN work_source_record wsr
      ON wsr.work_id = f.work_id
     AND wsr.source_record_id = f.source_record_id
    WHERE f.source_record_id IS NOT NULL
      AND wsr.id IS NULL;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'EvidenceFragment SourceRecord/Work normalization lineage failed'; END IF;
END $$;

DO $$
DECLARE bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM coverage_context c
    JOIN research_project p ON p.id = c.project_id
    JOIN research_profile_version pv ON pv.id = c.profile_version_id
    WHERE pv.profile_id <> p.profile_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'CoverageContext Profile lineage invariant failed'; END IF;

    SELECT count(*) INTO bad_count
    FROM coverage_context c
    JOIN research_project_version jv ON jv.id = c.project_version_id
    WHERE c.project_version_id IS NOT NULL
      AND jv.project_id <> c.project_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'CoverageContext Project-version lineage invariant failed'; END IF;
END $$;

DO $$
DECLARE bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM assessment a
    JOIN research_object_identity r ON r.id = a.target_research_object_id
    WHERE r.project_id IS DISTINCT FROM a.project_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Assessment target/project invariant failed'; END IF;

    SELECT count(*) INTO bad_count
    FROM assessment a
    JOIN coverage_context c ON c.id = a.coverage_context_id
    WHERE c.project_id <> a.project_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Assessment CoverageContext crossed Project'; END IF;

    SELECT count(*) INTO bad_count
    FROM change_event e
    JOIN research_object_identity r ON r.id = e.primary_research_object_id
    WHERE r.project_id IS DISTINCT FROM e.project_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'ChangeEvent target/project invariant failed'; END IF;

    SELECT count(*) INTO bad_count
    FROM change_event e
    JOIN coverage_context c ON c.id = e.coverage_context_id
    WHERE c.project_id <> e.project_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'ChangeEvent CoverageContext crossed Project'; END IF;

    SELECT count(*) INTO bad_count
    FROM human_decision h
    JOIN research_object_identity r ON r.id = h.primary_research_object_id
    WHERE r.project_id IS DISTINCT FROM h.project_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'HumanDecision target/project invariant failed'; END IF;

    SELECT count(*) INTO bad_count
    FROM human_decision h
    JOIN coverage_context c ON c.id = h.coverage_context_id
    WHERE c.project_id <> h.project_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'HumanDecision CoverageContext crossed Project'; END IF;

    SELECT count(*) INTO bad_count
    FROM human_decision h
    JOIN assessment a ON a.id = h.assessment_id
    WHERE a.project_id <> h.project_id
       OR a.target_research_object_id <> h.primary_research_object_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'HumanDecision Assessment lineage invariant failed'; END IF;
END $$;

DO $$
DECLARE bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM assessment a
    JOIN assessment s ON s.id = a.supersedes_assessment_id
    WHERE s.project_id <> a.project_id
       OR s.target_research_object_id <> a.target_research_object_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Assessment supersession crossed lineage'; END IF;

    SELECT count(*) INTO bad_count
    FROM human_decision h
    JOIN human_decision s ON s.id = h.supersedes_decision_id
    WHERE s.project_id <> h.project_id
       OR s.primary_research_object_id <> h.primary_research_object_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'HumanDecision supersession crossed lineage'; END IF;

    SELECT count(*) INTO bad_count
    FROM claim c
    JOIN claim s ON s.id = c.supersedes_claim_id
    WHERE s.evidence_fragment_id <> c.evidence_fragment_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Claim supersession crossed EvidenceFragment lineage'; END IF;

    SELECT count(*) INTO bad_count
    FROM evidence_relationship e
    JOIN evidence_relationship s ON s.id = e.supersedes_relationship_id
    WHERE s.claim_id <> e.claim_id
       OR s.target_research_object_id <> e.target_research_object_id;
    IF bad_count <> 0 THEN RAISE EXCEPTION 'EvidenceRelationship supersession crossed lineage'; END IF;
END $$;

DO $$
DECLARE bad_count integer;
BEGIN
    SELECT count(*) INTO bad_count
    FROM claim c
    JOIN evidence_fragment f ON f.id = c.evidence_fragment_id
    WHERE c.quarantine_state = 'ACTIVE'
      AND f.quarantine_state = 'QUARANTINED';
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Active Claim depends on quarantined EvidenceFragment'; END IF;

    SELECT count(*) INTO bad_count
    FROM evidence_relationship er
    JOIN claim c ON c.id = er.claim_id
    WHERE er.review_state <> 'QUARANTINED'
      AND c.quarantine_state = 'QUARANTINED';
    IF bad_count <> 0 THEN RAISE EXCEPTION 'Non-quarantined EvidenceRelationship depends on quarantined Claim'; END IF;
END $$;

SELECT 'J2 Migration 001 production-safe schema verification passed' AS verification_result;
