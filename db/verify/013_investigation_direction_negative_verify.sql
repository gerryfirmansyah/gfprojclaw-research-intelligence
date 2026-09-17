\set ON_ERROR_STOP on
BEGIN;

DO $$
DECLARE
    v_profile uuid := '3b000000-0000-4000-8000-000000000001';
    v_project uuid := '3b100000-0000-4000-8000-000000000001';
BEGIN
    BEGIN
        INSERT INTO research_object_identity
            (object_type, profile_id, project_id, canonical_label, lifecycle_state, origin)
        VALUES ('UNSUPPORTED_OBJECT', v_profile, v_project, 'Must fail', 'ACTIVE', 'J13_VERIFY');
        RAISE EXCEPTION 'unsupported object_type was accepted';
    EXCEPTION WHEN check_violation THEN NULL;
    END;

    BEGIN
        INSERT INTO research_object_identity
            (object_type, canonical_label, lifecycle_state, origin)
        VALUES ('INVESTIGATION_DIRECTION', 'Must fail', 'ACTIVE', 'J13_VERIFY');
        RAISE EXCEPTION 'projectless investigation direction was accepted';
    EXCEPTION WHEN check_violation THEN NULL;
    END;
END $$;

ROLLBACK;

-- Compatibility and child-state checks run in a fresh rollback-only transaction.
BEGIN;
DO $$
DECLARE
    v_profile uuid := '3b000000-0000-4000-8000-000000000001';
    v_project uuid := '3b100000-0000-4000-8000-000000000001';
    v_id uuid := gen_random_uuid();
BEGIN
    INSERT INTO research_object_identity
        (id, object_type, profile_id, project_id, canonical_label, lifecycle_state, origin)
    VALUES (v_id, 'GAP_CANDIDATE', v_profile, v_project, 'Compatibility gap', 'ACTIVE', 'J13_VERIFY');
    INSERT INTO gap_candidate
        (id, project_id, gap_type, statement, current_evolution_state)
    VALUES (v_id, v_project, 'SYNTHESIS_GAP', 'Compatibility only.', 'CANDIDATE');

    BEGIN
        INSERT INTO investigation_direction
            (id, project_id, statement, current_state)
        VALUES (v_id, v_project, 'Wrong identity type must fail.', 'CANDIDATE');
        RAISE EXCEPTION 'GAP_CANDIDATE identity was accepted as investigation direction';
    EXCEPTION WHEN foreign_key_violation THEN NULL;
    END;

    BEGIN
        INSERT INTO investigation_direction
            (id, project_id, statement, current_state)
        VALUES (v_id, v_project, 'Must fail.', 'INVALID_STATE');
        RAISE EXCEPTION 'invalid investigation state was accepted';
    EXCEPTION WHEN check_violation THEN NULL;
    END;
END $$;
ROLLBACK;
