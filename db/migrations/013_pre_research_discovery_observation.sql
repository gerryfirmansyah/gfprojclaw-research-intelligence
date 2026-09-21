BEGIN;

-- Phase 0 canonical exploration container. This migration defines structure only;
-- it does not create exploration sessions, scientific records, or HUMAN decisions.
CREATE TABLE research_exploration_session (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES research_project(id) ON DELETE RESTRICT,
    profile_id uuid NOT NULL,
    profile_version_id uuid NOT NULL,
    CONSTRAINT research_exploration_session_project_profile_fk
      FOREIGN KEY (project_id, profile_id) REFERENCES research_project(id, profile_id) ON DELETE RESTRICT,
    CONSTRAINT research_exploration_session_profile_version_fk
      FOREIGN KEY (profile_id, profile_version_id) REFERENCES research_profile_version(profile_id, id) ON DELETE RESTRICT,
    project_version_id uuid NULL,
    CONSTRAINT research_exploration_session_project_version_fk
      FOREIGN KEY (project_id, project_version_id) REFERENCES research_project_version(project_id, id) ON DELETE RESTRICT,
    research_interest text NOT NULL CHECK (btrim(research_interest) <> ''),
    status text NOT NULL CHECK (status IN ('EXPLORING','READY_FOR_HUMAN_DECISION','TRANSITIONED','PAUSED')),
    started_at timestamptz NOT NULL,
    closed_at timestamptz NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT research_exploration_session_time_ck CHECK (closed_at IS NULL OR closed_at >= started_at)
);

ALTER TABLE research_exploration_session ADD CONSTRAINT research_exploration_session_id_project_uk UNIQUE (id, project_id);

CREATE INDEX research_exploration_session_project_started_idx
    ON research_exploration_session(project_id, started_at DESC);

CREATE TABLE research_scope_node (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    exploration_session_id uuid NOT NULL REFERENCES research_exploration_session(id) ON DELETE RESTRICT,
    scope_level text NOT NULL CHECK (scope_level IN ('L0','L1','L2','L3','L4')),
    label text NOT NULL CHECK (btrim(label) <> ''),
    scope_description text NULL,
    parent_scope_node_id uuid NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT research_scope_node_session_label_uk UNIQUE (exploration_session_id, scope_level, label),
    CONSTRAINT research_scope_node_session_id_uk UNIQUE (exploration_session_id, id),
    CONSTRAINT research_scope_node_parent_same_session_fk
      FOREIGN KEY (exploration_session_id, parent_scope_node_id)
      REFERENCES research_scope_node(exploration_session_id, id) ON DELETE RESTRICT
);

CREATE INDEX research_scope_node_session_level_idx
    ON research_scope_node(exploration_session_id, scope_level);

CREATE TABLE discovery_query_family (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    exploration_session_id uuid NOT NULL REFERENCES research_exploration_session(id) ON DELETE RESTRICT,
    scope_node_id uuid NULL,
    family_key text NOT NULL CHECK (btrim(family_key) <> ''),
    label text NOT NULL CHECK (btrim(label) <> ''),
    rationale text NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT discovery_query_family_session_key_uk UNIQUE (exploration_session_id, family_key),
    CONSTRAINT discovery_query_family_session_id_uk UNIQUE (exploration_session_id, id),
    CONSTRAINT discovery_query_family_scope_same_session_fk
      FOREIGN KEY (exploration_session_id, scope_node_id)
      REFERENCES research_scope_node(exploration_session_id, id) ON DELETE RESTRICT
);

CREATE TABLE discovery_query (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    exploration_session_id uuid NOT NULL,
    query_family_id uuid NOT NULL,
    query_text text NOT NULL CHECK (btrim(query_text) <> ''),
    query_parameters_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT discovery_query_session_id_uk UNIQUE (exploration_session_id, id),
    CONSTRAINT discovery_query_family_same_session_fk
      FOREIGN KEY (exploration_session_id, query_family_id)
      REFERENCES discovery_query_family(exploration_session_id, id) ON DELETE RESTRICT
);

CREATE INDEX discovery_query_family_idx ON discovery_query(query_family_id);

ALTER TABLE source_record ADD CONSTRAINT source_record_source_id_uk UNIQUE (literature_source_id, id);
ALTER TABLE continuous_pilot_run ADD CONSTRAINT continuous_pilot_run_project_id_uk UNIQUE (project_id, id);
ALTER TABLE continuous_pilot_stage_run ADD CONSTRAINT continuous_pilot_stage_run_run_id_uk UNIQUE (pilot_run_id, id);

CREATE TABLE discovery_observation (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    exploration_session_id uuid NOT NULL REFERENCES research_exploration_session(id) ON DELETE RESTRICT,
    scope_node_id uuid NULL,
    discovery_query_id uuid NOT NULL,
    literature_source_id uuid NOT NULL REFERENCES literature_source(id) ON DELETE RESTRICT,
    project_id uuid NOT NULL,
    pilot_run_id uuid NULL,
    pilot_stage_run_id uuid NULL,
    source_record_id uuid NOT NULL,
    observed_at timestamptz NOT NULL,
    observation_state text NOT NULL CHECK (observation_state IN ('OBSERVED','RETRIEVED','DEGRADED','PARTIAL')),
    position_or_rank integer NULL CHECK (position_or_rank IS NULL OR position_or_rank >= 1),
    observation_metadata_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT discovery_observation_project_session_fk FOREIGN KEY (exploration_session_id, project_id) REFERENCES research_exploration_session(id, project_id) ON DELETE RESTRICT,
    CONSTRAINT discovery_observation_source_same_source_fk FOREIGN KEY (literature_source_id, source_record_id) REFERENCES source_record(literature_source_id, id) ON DELETE RESTRICT,
    CONSTRAINT discovery_observation_pilot_same_project_fk FOREIGN KEY (project_id, pilot_run_id) REFERENCES continuous_pilot_run(project_id, id) ON DELETE RESTRICT,
    CONSTRAINT discovery_observation_stage_same_run_fk FOREIGN KEY (pilot_run_id, pilot_stage_run_id) REFERENCES continuous_pilot_stage_run(pilot_run_id, id) ON DELETE RESTRICT,
    CONSTRAINT discovery_observation_scope_same_session_fk
      FOREIGN KEY (exploration_session_id, scope_node_id)
      REFERENCES research_scope_node(exploration_session_id, id) ON DELETE RESTRICT,
    CONSTRAINT discovery_observation_query_same_session_fk
      FOREIGN KEY (exploration_session_id, discovery_query_id)
      REFERENCES discovery_query(exploration_session_id, id) ON DELETE RESTRICT,
    CONSTRAINT discovery_observation_unique_uk UNIQUE (
        exploration_session_id, discovery_query_id, literature_source_id, source_record_id, observed_at
    )
);

CREATE INDEX discovery_observation_session_observed_idx
    ON discovery_observation(exploration_session_id, observed_at DESC);
CREATE INDEX discovery_observation_source_record_idx
    ON discovery_observation(source_record_id);
CREATE INDEX discovery_observation_query_source_idx
    ON discovery_observation(discovery_query_id, literature_source_id);

-- App/UI is read-only for Phase 0 canonical machine observations.
REVOKE INSERT, UPDATE, DELETE ON research_exploration_session, research_scope_node,
    discovery_query_family, discovery_query, discovery_observation FROM gfproj_app;
GRANT SELECT ON research_exploration_session, research_scope_node,
    discovery_query_family, discovery_query, discovery_observation TO gfproj_app;

COMMIT;
