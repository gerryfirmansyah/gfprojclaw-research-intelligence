DO $$
DECLARE r record;
BEGIN
 SELECT rolcanlogin,rolsuper,rolcreatedb,rolcreaterole,rolinherit,rolreplication,rolbypassrls INTO r FROM pg_roles WHERE rolname='gfproj_pilot_executor';
 IF NOT FOUND OR NOT r.rolcanlogin OR r.rolsuper OR r.rolcreatedb OR r.rolcreaterole OR r.rolinherit OR r.rolreplication OR r.rolbypassrls THEN RAISE EXCEPTION 'executor attributes invalid'; END IF;
 IF NOT pg_has_role('gfproj_pilot_executor','gfproj_pilot_worker','MEMBER') THEN RAISE EXCEPTION 'worker membership missing'; END IF;
 IF has_table_privilege('gfproj_pilot_executor','human_decision','INSERT') OR has_table_privilege('gfproj_pilot_executor','human_decision','UPDATE') THEN RAISE EXCEPTION 'executor has HumanDecision write authority'; END IF;
END $$;
