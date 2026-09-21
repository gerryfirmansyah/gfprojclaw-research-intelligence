DO $$
DECLARE
  missing text;
BEGIN
  SELECT string_agg(x, ', ') INTO missing
  FROM (VALUES
    ('research_exploration_session'),
    ('research_scope_node'),
    ('discovery_query_family'),
    ('discovery_query'),
    ('discovery_observation')
  ) v(x)
  WHERE to_regclass('public.' || x) IS NULL;
  IF missing IS NOT NULL THEN
    RAISE EXCEPTION 'Missing Phase 0 tables: %', missing;
  END IF;
END $$;

DO $$
DECLARE
  t text;
BEGIN
  FOREACH t IN ARRAY ARRAY[
    'research_exploration_session','research_scope_node',
    'discovery_query_family','discovery_query','discovery_observation'
  ] LOOP
    IF NOT has_table_privilege('gfproj_app', t, 'SELECT') THEN
      RAISE EXCEPTION 'gfproj_app lacks SELECT on %', t;
    END IF;
    IF has_table_privilege('gfproj_app', t, 'INSERT')
       OR has_table_privilege('gfproj_app', t, 'UPDATE')
       OR has_table_privilege('gfproj_app', t, 'DELETE') THEN
      RAISE EXCEPTION 'gfproj_app has forbidden write privilege on %', t;
    END IF;
  END LOOP;
END $$;

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM research_exploration_session)
     OR EXISTS (SELECT 1 FROM research_scope_node)
     OR EXISTS (SELECT 1 FROM discovery_query_family)
     OR EXISTS (SELECT 1 FROM discovery_query)
     OR EXISTS (SELECT 1 FROM discovery_observation) THEN
    RAISE EXCEPTION 'Migration 013 must not seed Phase 0 records';
  END IF;
END $$;

SELECT 'PRE_RESEARCH_DISCOVERY_SCHEMA_PASS' AS result;
