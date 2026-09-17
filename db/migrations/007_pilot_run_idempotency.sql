BEGIN;
ALTER TABLE continuous_pilot_run
  ADD COLUMN IF NOT EXISTS idempotency_key text;
CREATE UNIQUE INDEX IF NOT EXISTS uq_continuous_pilot_run_idempotency_key
  ON continuous_pilot_run (idempotency_key)
  WHERE idempotency_key IS NOT NULL;
COMMIT;
