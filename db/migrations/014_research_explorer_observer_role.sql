BEGIN;
DO $$ BEGIN
 IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='gfproj_explorer_observer') THEN
  CREATE ROLE gfproj_explorer_observer NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS;
 END IF;
END $$;
ALTER ROLE gfproj_explorer_observer NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS;
GRANT USAGE ON SCHEMA public TO gfproj_explorer_observer;
GRANT SELECT ON research_profile,research_profile_version,research_project,research_project_version,literature_source TO gfproj_explorer_observer;
GRANT SELECT,INSERT ON research_exploration_session,discovery_query_family,discovery_query,source_record,discovery_observation TO gfproj_explorer_observer;
REVOKE UPDATE,DELETE ON research_exploration_session,discovery_query_family,discovery_query,discovery_observation FROM gfproj_explorer_observer;
REVOKE UPDATE,DELETE ON source_record FROM gfproj_explorer_observer;
REVOKE ALL ON project_work_relevance,work,work_identifier,work_source_record,evidence_fragment,claim,evidence_relationship,gap_candidate,assessment,assessment_dimension,change_event,human_decision,investigation_direction FROM gfproj_explorer_observer;
GRANT gfproj_explorer_observer TO gfproj_pilot_executor;
COMMIT;
