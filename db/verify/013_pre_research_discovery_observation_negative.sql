-- Negative integrity checks for Phase 0 same-session lineage.
-- All attempted cross-session links must be rejected by PostgreSQL.

BEGIN;

INSERT INTO research_profile (id, name, status)
VALUES ('71000000-0000-4000-8000-000000000001','J16 negative profile','ACTIVE');

INSERT INTO research_profile_version (id, profile_id, version_no, summary)
VALUES ('71000000-0000-4000-8000-000000000011','71000000-0000-4000-8000-000000000001',1,'fixture');

INSERT INTO research_project (id, profile_id, name, status)
VALUES
 ('72000000-0000-4000-8000-000000000001','71000000-0000-4000-8000-000000000001','J16 A','ACTIVE'),
 ('72000000-0000-4000-8000-000000000002','71000000-0000-4000-8000-000000000001','J16 B','ACTIVE');

DO $$ BEGIN
  BEGIN
    INSERT INTO research_exploration_session (project_id, profile_id, profile_version_id, research_interest, status, started_at)
    VALUES ('72000000-0000-4000-8000-000000000001','71000000-0000-4000-8000-000000000001','71000000-0000-4000-8000-000000000099','bad profile version','EXPLORING',now());
    RAISE EXCEPTION 'profile version outside canonical profile was accepted';
  EXCEPTION WHEN foreign_key_violation THEN NULL; END;
END $$;

INSERT INTO research_exploration_session
(id, project_id, profile_id, profile_version_id, research_interest, status, started_at)
VALUES
 ('73000000-0000-4000-8000-000000000001','72000000-0000-4000-8000-000000000001','71000000-0000-4000-8000-000000000001','71000000-0000-4000-8000-000000000011','A','EXPLORING',now()),
 ('73000000-0000-4000-8000-000000000002','72000000-0000-4000-8000-000000000002','71000000-0000-4000-8000-000000000001','71000000-0000-4000-8000-000000000011','B','EXPLORING',now());

INSERT INTO research_scope_node (id, exploration_session_id, scope_level, label)
VALUES
 ('74000000-0000-4000-8000-000000000001','73000000-0000-4000-8000-000000000001','L1','A node'),
 ('74000000-0000-4000-8000-000000000002','73000000-0000-4000-8000-000000000002','L1','B node');

DO $$ BEGIN
  BEGIN
    INSERT INTO research_scope_node (exploration_session_id, scope_level, label, parent_scope_node_id)
    VALUES ('73000000-0000-4000-8000-000000000001','L0','bad parent','74000000-0000-4000-8000-000000000002');
    RAISE EXCEPTION 'cross-session scope parent was accepted';
  EXCEPTION WHEN foreign_key_violation THEN NULL; END;
END $$;

DO $$ BEGIN
  BEGIN
    INSERT INTO discovery_query_family (exploration_session_id, scope_node_id, family_key, label)
    VALUES ('73000000-0000-4000-8000-000000000001','74000000-0000-4000-8000-000000000002','bad','bad');
    RAISE EXCEPTION 'cross-session query family scope was accepted';
  EXCEPTION WHEN foreign_key_violation THEN NULL; END;
END $$;

INSERT INTO discovery_query_family (id, exploration_session_id, scope_node_id, family_key, label)
VALUES
 ('75000000-0000-4000-8000-000000000001','73000000-0000-4000-8000-000000000001','74000000-0000-4000-8000-000000000001','a','A'),
 ('75000000-0000-4000-8000-000000000002','73000000-0000-4000-8000-000000000002','74000000-0000-4000-8000-000000000002','b','B');

DO $$ BEGIN
  BEGIN
    INSERT INTO discovery_query (exploration_session_id, query_family_id, query_text)
    VALUES ('73000000-0000-4000-8000-000000000001','75000000-0000-4000-8000-000000000002','bad');
    RAISE EXCEPTION 'cross-session discovery query was accepted';
  EXCEPTION WHEN foreign_key_violation THEN NULL; END;
END $$;

INSERT INTO discovery_query (id, exploration_session_id, query_family_id, query_text)
VALUES
 ('76000000-0000-4000-8000-000000000001','73000000-0000-4000-8000-000000000001','75000000-0000-4000-8000-000000000001','A'),
 ('76000000-0000-4000-8000-000000000002','73000000-0000-4000-8000-000000000002','75000000-0000-4000-8000-000000000002','B');

INSERT INTO literature_source (id, source_key, name, source_type) VALUES
 ('77000000-0000-4000-8000-000000000001','neg-a','Neg A','API'),
 ('77000000-0000-4000-8000-000000000002','neg-b','Neg B','API');
INSERT INTO source_record (id,literature_source_id,source_record_identifier,retrieved_at,content_access_state,normalization_state) VALUES
 ('78000000-0000-4000-8000-000000000001','77000000-0000-4000-8000-000000000001','a',now(),'METADATA_ONLY','UNRESOLVED');
INSERT INTO continuous_pilot_run (id,trigger_type,project_id,started_at,status) VALUES
 ('79000000-0000-4000-8000-000000000001','MANUAL','72000000-0000-4000-8000-000000000001',now(),'RUNNING'),
 ('79000000-0000-4000-8000-000000000002','MANUAL','72000000-0000-4000-8000-000000000002',now(),'RUNNING');
INSERT INTO continuous_pilot_stage_run (id,pilot_run_id,stage_key,status,started_at) VALUES
 ('7a000000-0000-4000-8000-000000000001','79000000-0000-4000-8000-000000000001','a','RUNNING',now()),
 ('7a000000-0000-4000-8000-000000000002','79000000-0000-4000-8000-000000000002','b','RUNNING',now());

DO $$ BEGIN
  BEGIN
    INSERT INTO discovery_observation (exploration_session_id,scope_node_id,discovery_query_id,literature_source_id,project_id,source_record_id,observed_at,observation_state)
    VALUES ('73000000-0000-4000-8000-000000000001','74000000-0000-4000-8000-000000000001','76000000-0000-4000-8000-000000000001','77000000-0000-4000-8000-000000000002','72000000-0000-4000-8000-000000000001','78000000-0000-4000-8000-000000000001',now(),'OBSERVED');
    RAISE EXCEPTION 'cross-source record was accepted';
  EXCEPTION WHEN foreign_key_violation THEN NULL; END;
END $$;
DO $$ BEGIN
  BEGIN
    INSERT INTO discovery_observation (exploration_session_id,scope_node_id,discovery_query_id,literature_source_id,project_id,pilot_run_id,source_record_id,observed_at,observation_state)
    VALUES ('73000000-0000-4000-8000-000000000001','74000000-0000-4000-8000-000000000001','76000000-0000-4000-8000-000000000001','77000000-0000-4000-8000-000000000001','72000000-0000-4000-8000-000000000001','79000000-0000-4000-8000-000000000002','78000000-0000-4000-8000-000000000001',now(),'OBSERVED');
    RAISE EXCEPTION 'cross-project pilot run was accepted';
  EXCEPTION WHEN foreign_key_violation THEN NULL; END;
END $$;
DO $$ BEGIN
  BEGIN
    INSERT INTO discovery_observation (exploration_session_id,scope_node_id,discovery_query_id,literature_source_id,project_id,pilot_run_id,pilot_stage_run_id,source_record_id,observed_at,observation_state)
    VALUES ('73000000-0000-4000-8000-000000000001','74000000-0000-4000-8000-000000000001','76000000-0000-4000-8000-000000000001','77000000-0000-4000-8000-000000000001','72000000-0000-4000-8000-000000000001','79000000-0000-4000-8000-000000000001','7a000000-0000-4000-8000-000000000002','78000000-0000-4000-8000-000000000001',now(),'OBSERVED');
    RAISE EXCEPTION 'cross-run pilot stage was accepted';
  EXCEPTION WHEN foreign_key_violation THEN NULL; END;
END $$;

ROLLBACK;
SELECT 'PRE_RESEARCH_DISCOVERY_NEGATIVE_PASS' AS result;
