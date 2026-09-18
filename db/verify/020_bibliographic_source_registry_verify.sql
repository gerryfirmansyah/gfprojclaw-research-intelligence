BEGIN;
DO $$ BEGIN
 IF (SELECT count(*) FROM literature_source WHERE source_key IN ('openalex','crossref') AND active AND source_type='BIBLIOGRAPHIC_API' AND ((source_key='openalex' AND configuration_reference='provider:openalex') OR (source_key='crossref' AND configuration_reference='provider:crossref'))) <> 2 THEN RAISE EXCEPTION 'canonical bibliographic source registry invalid'; END IF;
 IF has_table_privilege('gfproj_pilot_metadata_ingestor','literature_source','INSERT') OR has_table_privilege('gfproj_pilot_metadata_ingestor','literature_source','UPDATE') OR has_table_privilege('gfproj_pilot_metadata_ingestor','literature_source','DELETE') THEN RAISE EXCEPTION 'metadata role can mutate source registry'; END IF;
 IF NOT has_table_privilege('gfproj_pilot_metadata_ingestor','literature_source','SELECT') THEN RAISE EXCEPTION 'metadata role cannot read source registry'; END IF;
END $$;
ROLLBACK;
