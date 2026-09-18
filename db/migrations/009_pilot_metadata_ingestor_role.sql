BEGIN;
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='gfproj_pilot_metadata_ingestor') THEN
    CREATE ROLE gfproj_pilot_metadata_ingestor NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS;
  END IF;
END $$;
ALTER ROLE gfproj_pilot_metadata_ingestor NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS;
GRANT USAGE ON SCHEMA public TO gfproj_pilot_metadata_ingestor;
GRANT SELECT ON literature_source,research_project,research_project_version TO gfproj_pilot_metadata_ingestor;
GRANT SELECT,INSERT ON source_record,project_work_relevance TO gfproj_pilot_metadata_ingestor;
GRANT UPDATE (normalization_state, provenance_hash) ON source_record TO gfproj_pilot_metadata_ingestor;
GRANT UPDATE (last_seen_at) ON project_work_relevance TO gfproj_pilot_metadata_ingestor;
GRANT SELECT,INSERT ON work,work_identifier,work_source_record TO gfproj_pilot_metadata_ingestor;
REVOKE DELETE ON source_record,project_work_relevance,work,work_identifier,work_source_record FROM gfproj_pilot_metadata_ingestor;
REVOKE ALL ON evidence_fragment,claim,evidence_relationship,gap_candidate,assessment,assessment_dimension,change_event,human_decision,investigation_direction FROM gfproj_pilot_metadata_ingestor;
GRANT gfproj_pilot_metadata_ingestor TO gfproj_pilot_executor;
COMMIT;
