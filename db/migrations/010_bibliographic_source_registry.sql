BEGIN;
INSERT INTO literature_source (source_key,name,source_type,active,configuration_reference) VALUES ('openalex','OpenAlex','BIBLIOGRAPHIC_API',true,'provider:openalex'), ('crossref','Crossref','BIBLIOGRAPHIC_API',true,'provider:crossref') ON CONFLICT (source_key) DO NOTHING;
COMMIT;
