BEGIN;

CREATE TABLE continuous_pilot_run (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    trigger_type text NOT NULL CHECK (trigger_type IN ('MANUAL','SCHEDULED','RETRY')),
    project_id uuid NULL REFERENCES research_project(id) ON DELETE RESTRICT,
    started_at timestamptz NOT NULL,
    finished_at timestamptz NULL,
    status text NOT NULL CHECK (status IN ('RUNNING','COMPLETED','PARTIAL','FAILED')),
    machine_actions_jsonb jsonb NOT NULL DEFAULT '[]'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT continuous_pilot_run_time_ck CHECK (finished_at IS NULL OR finished_at >= started_at)
);

CREATE INDEX continuous_pilot_run_started_idx ON continuous_pilot_run(started_at DESC);

CREATE TABLE continuous_pilot_stage_run (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    pilot_run_id uuid NOT NULL REFERENCES continuous_pilot_run(id) ON DELETE RESTRICT,
    stage_key text NOT NULL CHECK (btrim(stage_key) <> ''),
    source_key text NULL,
    attempt integer NOT NULL DEFAULT 1 CHECK (attempt >= 1),
    status text NOT NULL CHECK (status IN ('RUNNING','COMPLETED','FAILED','SKIPPED')),
    started_at timestamptz NOT NULL,
    finished_at timestamptz NULL,
    error_class text NULL,
    error_summary text NULL,
    metrics_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT continuous_pilot_stage_time_ck CHECK (finished_at IS NULL OR finished_at >= started_at),
    CONSTRAINT continuous_pilot_stage_attempt_uk UNIQUE (pilot_run_id, stage_key, source_key, attempt)
);

CREATE INDEX continuous_pilot_stage_run_idx ON continuous_pilot_stage_run(pilot_run_id, started_at);

REVOKE INSERT, UPDATE, DELETE ON continuous_pilot_run, continuous_pilot_stage_run FROM gfproj_app;
GRANT SELECT ON continuous_pilot_run, continuous_pilot_stage_run TO gfproj_app;

COMMIT;
