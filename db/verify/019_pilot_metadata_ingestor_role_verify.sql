BEGIN;
DO $$ BEGIN
  IF NOT has_table_privilege('gfproj_pilot_metadata_ingestor','research_project_version','SELECT') THEN RAISE EXCEPTION 'metadata role cannot read ProjectVersion'; END IF;
  IF has_table_privilege('gfproj_pilot_metadata_ingestor','research_project_version','INSERT') THEN RAISE EXCEPTION 'metadata role must not version projects'; END IF;
  IF NOT has_table_privilege('gfproj_pilot_metadata_ingestor','source_record','INSERT') THEN RAISE EXCEPTION 'metadata role cannot insert SourceRecord'; END IF;
  IF NOT has_table_privilege('gfproj_pilot_metadata_ingestor','work','INSERT') THEN RAISE EXCEPTION 'metadata role cannot insert Work'; END IF;
  IF has_table_privilege('gfproj_pilot_metadata_ingestor','work','UPDATE') THEN RAISE EXCEPTION 'metadata role must not update Work'; END IF;
  IF NOT has_table_privilege('gfproj_pilot_metadata_ingestor','project_work_relevance','UPDATE') THEN RAISE EXCEPTION 'metadata role cannot maintain candidate association'; END IF;
  IF has_table_privilege('gfproj_pilot_metadata_ingestor','human_decision','INSERT') OR has_table_privilege('gfproj_pilot_metadata_ingestor','claim','INSERT') OR has_table_privilege('gfproj_pilot_metadata_ingestor','evidence_fragment','INSERT') OR has_table_privilege('gfproj_pilot_metadata_ingestor','gap_candidate','INSERT') OR has_table_privilege('gfproj_pilot_metadata_ingestor','investigation_direction','INSERT') THEN RAISE EXCEPTION 'metadata role crossed scientific authority boundary'; END IF;
  IF has_table_privilege('gfproj_pilot_metadata_ingestor','source_record','DELETE') OR has_table_privilege('gfproj_pilot_metadata_ingestor','work','DELETE') THEN RAISE EXCEPTION 'metadata role must not delete canonical metadata'; END IF;
  IF NOT pg_has_role('gfproj_pilot_executor','gfproj_pilot_metadata_ingestor','MEMBER') THEN RAISE EXCEPTION 'executor is not member of metadata capability'; END IF;
END $$;
ROLLBACK;
