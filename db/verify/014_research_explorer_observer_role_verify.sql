DO $$ BEGIN
 IF NOT has_table_privilege('gfproj_explorer_observer','research_exploration_session','INSERT') THEN RAISE EXCEPTION 'observer cannot create exploration session'; END IF;
 IF NOT has_table_privilege('gfproj_explorer_observer','source_record','INSERT') OR NOT has_table_privilege('gfproj_explorer_observer','discovery_observation','INSERT') THEN RAISE EXCEPTION 'observer cannot persist discovery observation'; END IF;
 IF has_table_privilege('gfproj_explorer_observer','project_work_relevance','INSERT') OR has_table_privilege('gfproj_explorer_observer','work','INSERT') OR has_table_privilege('gfproj_explorer_observer','human_decision','INSERT') OR has_table_privilege('gfproj_explorer_observer','evidence_fragment','INSERT') OR has_table_privilege('gfproj_explorer_observer','claim','INSERT') THEN RAISE EXCEPTION 'observer crossed scientific/project corpus authority'; END IF;
 IF has_table_privilege('gfproj_explorer_observer','source_record','UPDATE') OR has_table_privilege('gfproj_explorer_observer','discovery_observation','UPDATE') THEN RAISE EXCEPTION 'observer has mutation authority beyond append'; END IF;
 IF NOT pg_has_role('gfproj_pilot_executor','gfproj_explorer_observer','MEMBER') THEN RAISE EXCEPTION 'executor lacks observer capability'; END IF;
 RAISE NOTICE 'RESEARCH_EXPLORER_OBSERVER_ROLE_PASS';
END $$;
