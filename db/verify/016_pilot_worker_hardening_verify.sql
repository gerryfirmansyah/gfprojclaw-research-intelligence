DO $$
DECLARE r record;
BEGIN
  SELECT rolcanlogin, rolsuper, rolcreatedb, rolcreaterole, rolinherit, rolreplication, rolbypassrls INTO r
  FROM pg_roles WHERE rolname='gfproj_pilot_worker';
  IF NOT FOUND OR r.rolcanlogin OR r.rolsuper OR r.rolcreatedb OR r.rolcreaterole OR r.rolinherit OR r.rolreplication OR r.rolbypassrls THEN
    RAISE EXCEPTION 'gfproj_pilot_worker role hardening verification failed';
  END IF;
  IF NOT has_table_privilege('gfproj_pilot_worker','continuous_pilot_run','INSERT')
     OR NOT has_table_privilege('gfproj_pilot_worker','continuous_pilot_stage_run','UPDATE')
     OR has_table_privilege('gfproj_pilot_worker','human_decision','INSERT')
     OR has_table_privilege('gfproj_pilot_worker','human_decision','UPDATE') THEN
    RAISE EXCEPTION 'gfproj_pilot_worker privilege boundary verification failed';
  END IF;
END $$;
