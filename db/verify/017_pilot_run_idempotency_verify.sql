BEGIN;
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema='public' AND table_name='continuous_pilot_run' AND column_name='idempotency_key'
  ) THEN RAISE EXCEPTION 'idempotency_key missing'; END IF;
  IF NOT EXISTS (
    SELECT 1 FROM pg_indexes
    WHERE schemaname='public' AND tablename='continuous_pilot_run'
      AND indexname='uq_continuous_pilot_run_idempotency_key'
  ) THEN RAISE EXCEPTION 'idempotency unique index missing'; END IF;
END $$;
ROLLBACK;
