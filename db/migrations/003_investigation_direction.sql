BEGIN;

ALTER TABLE research_object_identity
    DROP CONSTRAINT research_object_identity_object_type_check;

ALTER TABLE research_object_identity
    ADD CONSTRAINT research_object_identity_object_type_check
    CHECK (object_type IN ('GAP_CANDIDATE','INVESTIGATION_DIRECTION'));

ALTER TABLE research_object_identity
    DROP CONSTRAINT research_object_identity_project_scope_ck;

ALTER TABLE research_object_identity
    ADD CONSTRAINT research_object_identity_project_scope_ck
    CHECK (object_type NOT IN ('GAP_CANDIDATE','INVESTIGATION_DIRECTION') OR project_id IS NOT NULL);

ALTER TABLE research_object_identity ADD CONSTRAINT research_object_identity_id_project_type_uk UNIQUE (id, project_id, object_type);

CREATE TABLE investigation_direction (
    id uuid PRIMARY KEY,
    project_id uuid NOT NULL,
    object_type text NOT NULL DEFAULT 'INVESTIGATION_DIRECTION' CHECK (object_type = 'INVESTIGATION_DIRECTION'),
    statement text NOT NULL CHECK (btrim(statement) <> ''),
    scope_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    current_state text NOT NULL CHECK (current_state IN ('CANDIDATE','INVESTIGATING','PAUSED','SUPERSEDED')),
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT investigation_direction_identity_project_fk
        FOREIGN KEY (id, project_id, object_type)
        REFERENCES research_object_identity(id, project_id, object_type)
        ON DELETE RESTRICT,
    CONSTRAINT investigation_direction_project_fk
        FOREIGN KEY (project_id) REFERENCES research_project(id) ON DELETE RESTRICT
);

CREATE INDEX investigation_direction_project_state_idx ON investigation_direction(project_id, current_state);

GRANT SELECT, INSERT, UPDATE ON investigation_direction TO gfproj_app;

COMMIT;
