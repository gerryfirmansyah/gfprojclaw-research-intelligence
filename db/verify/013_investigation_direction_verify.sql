\set ON_ERROR_STOP on
BEGIN;

DO $$
DECLARE
    v_profile uuid := '3b000000-0000-4000-8000-000000000001';
    v_project uuid := '3b100000-0000-4000-8000-000000000001';
    v_id uuid := gen_random_uuid();
BEGIN
    INSERT INTO research_object_identity
        (id, object_type, profile_id, project_id, canonical_label, lifecycle_state, origin, created_by)
    VALUES
        (v_id, 'INVESTIGATION_DIRECTION', v_profile, v_project,
         'Verification investigation direction', 'ACTIVE', 'J13_VERIFY', 'verification');

    INSERT INTO investigation_direction
        (id, project_id, statement, scope_jsonb, current_state)
    VALUES
        (v_id, v_project, 'Verification only; not a scientific conclusion.',
         '{"verification":true}'::jsonb, 'CANDIDATE');

    IF NOT EXISTS (SELECT 1 FROM investigation_direction WHERE id = v_id) THEN
        RAISE EXCEPTION 'INVESTIGATION_DIRECTION insert verification failed';
    END IF;
END $$;

ROLLBACK;
