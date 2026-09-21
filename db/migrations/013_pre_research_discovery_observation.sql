BEGIN;

-- Phase 0 canonical exploration container. This migration defines structure only;
-- it does not create exploration sessions, scientific records, or HUMAN decisions.
CREATE TABLE research_exploration_session (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES research_project(id) ON DELETE RESTRICT,
    profile_version_id uuid NOT NULL REFERENCES research_profile_version(id) ON DELETE RESTRICT,
    project_version_id uuid NULL REFERENCES research_project_version(id) ON DELETE RESTRICT,
    research_interest text NOT NULL CHECK (btrim(research_interest) <> ''),
    status text NOT NULL CHECK (status IN ('EXPLORING','READY_FOR_HUMAN_DECISION','TRANSITIONED','PAUSED')),
    started_at timestamptz NOT NULL,
    closed_at timestamptz NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT research_exploration_session_time_ck CHECK (closed_at IS NULL OR closed_at >= started_at)
);

CREATE INDEX research_exploration_session_project_started_idx
    ON research_exploration_session(project_id, started_at DESC);

CREATE TABLE research_scope_node (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    exploration_session_id uuid NOT NULL REFERENCES research_exploration_session(id) ON DELETE RESTRICT,
    scope_level text NOT NULL CHECK (scope_level IN ('L0','L1','L2','L3','L4')),
    label text NOT NULL CHECK (btrim(label) <> ''),
    scope_description text NULL,
    parent_scope_node_id uuid NULL REFERENCES research_scope_node(id) ON DELETE RESTRICT,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT research_scope_node_session_label_uk UNIQUE (exploration_session_id, scope_level, label)
);

CREATE INDEX research_scope_node_session_level_idx
    ON research_scope_node(exploration_session_id, scope_level);

CREATE TABLE discovery_query_family (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    exploration_session_id uuid NOT NULL REFERENCES research_exploration_session(id) ON DELETE RESTRICT,
    scope_node_id uuid NULL REFERENCES research_scope_node(id) ON DELETE RESTRICT,
    family_key text NOT NULL CHECK (btrim(family_key) <> ''),
    label text NOT NULL CHECK (btrim(label) <> ''),
    rationale text NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT discovery_query_family_session_key_uk UNIQUE (exploration_session_id, family_key)
);

CREATE TABLE discovery_query (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    query_family_id uuid NOT NULL REFERENCES discovery_query_family(id) ON DELETE RESTRICT,
    query_text text NOT NULL CHECK (btrim(query_text) <> ''),
    query_parameters_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX discovery_query_family_idx ON discovery_query(query_family_id);

CREATE TABLE discovery_observation (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    exploration_session_id uuid NOT NULL REFERENCES research_exploration_session(id) ON DELETE RESTRICT,
    scope_node_id uuid NULL REFERENCES research_scope_node(id) ON DELETE RESTRICT,
    discovery_query_id uuid NOT NULL REFERENCES discovery_query(id) ON DELETE RESTRICT,
    literature_source_id uuid NOT NULL REFERENCES literature_source(id) ON DELETE RESTRICT,
    pilot_run_id uuid NULL REFERENCES continuous_pilot_run(id) ON DELETE RESTRICT,
    pilot_stage_run_id uuid NULL REFERENCES continuous_pilot_stage_run(id) ON DELETE RESTRICT,
    source_record_id uuid NOT NULL REFERENCES source_record(id) ON DELETE RESTRICT,
    observed_at timestamptz NOT NULL,
    observation_state text NOT NULL CHECK (observation_state IN ('OBSERVED','RETRIEVED','DEGRADED','PARTIAL')),
    position_or_rank integer NULL CHECK (position_or_rank IS NULL OR position_or_rank >= 1),
    observation_metadata_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
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
