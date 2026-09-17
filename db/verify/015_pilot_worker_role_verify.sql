BEGIN;
DO $$ BEGIN
  IF NOT has_table_privilege('gfproj_pilot_worker','continuous_pilot_run','INSERT') THEN RAISE EXCEPTION 'worker cannot insert pilot run'; END IF;
  IF NOT has_table_privilege('gfproj_pilot_worker','continuous_pilot_stage_run','UPDATE') THEN RAISE EXCEPTION 'worker cannot update stage'; END IF;
  IF has_table_privilege('gfproj_pilot_worker','human_decision','INSERT') THEN RAISE EXCEPTION 'worker must not insert human decision'; END IF;
  IF has_table_privilege('gfproj_pilot_worker','human_decision','UPDATE') THEN RAISE EXCEPTION 'worker must not update human decision'; END IF;
END $$;
ROLLBACK;
