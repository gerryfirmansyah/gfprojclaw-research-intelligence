BEGIN;
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='gfproj_pilot_worker') THEN
    CREATE ROLE gfproj_pilot_worker NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
  END IF;
END $$;
GRANT USAGE ON SCHEMA public TO gfproj_pilot_worker;
GRANT SELECT, INSERT, UPDATE ON continuous_pilot_run, continuous_pilot_stage_run TO gfproj_pilot_worker;
REVOKE DELETE ON continuous_pilot_run, continuous_pilot_stage_run FROM gfproj_pilot_worker;
REVOKE ALL ON human_decision FROM gfproj_pilot_worker;
COMMIT;
