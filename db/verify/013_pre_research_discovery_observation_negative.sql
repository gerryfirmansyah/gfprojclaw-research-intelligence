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

INSERT INTO research_exploration_session
(id, project_id, profile_version_id, research_interest, status, started_at)
VALUES
 ('73000000-0000-4000-8000-000000000001','72000000-0000-4000-8000-000000000001','71000000-0000-4000-8000-000000000011','A','EXPLORING',now()),
 ('73000000-0000-4000-8000-000000000002','72000000-0000-4000-8000-000000000002','71000000-0000-4000-8000-000000000011','B','EXPLORING',now());

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

DO $$ BEGIN
  BEGIN
    INSERT INTO discovery_observation
      (exploration_session_id, scope_node_id, discovery_query_id, literature_source_id, source_record_id, observed_at, observation_state)
    VALUES
      ('73000000-0000-4000-8000-000000000001','74000000-0000-4000-8000-000000000001','76000000-0000-4000-8000-000000000002',
       '00000000-0000-0000-0000-000000000000','00000000-0000-0000-0000-000000000000',now(),'OBSERVED');
    RAISE EXCEPTION 'cross-session observation query was accepted';
  EXCEPTION WHEN foreign_key_violation THEN NULL; END;
END $$;

ROLLBACK;
SELECT 'PRE_RESEARCH_DISCOVERY_NEGATIVE_PASS' AS result;
