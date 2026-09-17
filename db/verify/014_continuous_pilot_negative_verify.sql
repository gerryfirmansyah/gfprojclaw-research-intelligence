BEGIN;
DO $$
BEGIN
  BEGIN
    INSERT INTO continuous_pilot_run (trigger_type, started_at, finished_at, status) VALUES ('SCHEDULED', now(), now() - interval '1 minute', 'COMPLETED');
    RAISE EXCEPTION 'expected invalid time failure';
  EXCEPTION WHEN check_violation THEN NULL;
  END;
  BEGIN
    INSERT INTO continuous_pilot_run (trigger_type, started_at, status) VALUES ('AUTO_SCIENTIFIC_DECISION', now(), 'RUNNING');
    RAISE EXCEPTION 'expected invalid trigger failure';
  EXCEPTION WHEN check_violation THEN NULL;
  END;
END $$;
ROLLBACK;
