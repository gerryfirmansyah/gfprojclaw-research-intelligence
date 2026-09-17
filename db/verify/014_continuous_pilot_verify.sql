BEGIN;

INSERT INTO continuous_pilot_run (id, trigger_type, project_id, started_at, finished_at, status, machine_actions_jsonb)
VALUES ('14000000-0000-4000-8000-000000000001','MANUAL',NULL,now(),now(),'COMPLETED','["read_only_probe"]'::jsonb);

INSERT INTO continuous_pilot_stage_run (pilot_run_id, stage_key, source_key, attempt, status, started_at, finished_at, metrics_jsonb)
VALUES ('14000000-0000-4000-8000-000000000001','source_probe','OpenAlex',1,'COMPLETED',now(),now(),'{"records":0}'::jsonb);

DO $$
BEGIN
  IF (SELECT count(*) FROM continuous_pilot_run WHERE id='14000000-0000-4000-8000-000000000001') <> 1 THEN RAISE EXCEPTION 'pilot run missing'; END IF;
  IF (SELECT count(*) FROM continuous_pilot_stage_run WHERE pilot_run_id='14000000-0000-4000-8000-000000000001') <> 1 THEN RAISE EXCEPTION 'stage run missing'; END IF;
END $$;

ROLLBACK;
