-- GFPROJCLAW — Migration 001 deterministic reference fixture
-- J2 SQL Draft v0
-- Synthetic data only. Not scientific evidence. Not for production interpretation.
-- Purpose: prove the same canonical schema and evidence trace for Profile A and Profile B.

BEGIN;

INSERT INTO research_profile (id, name, status, created_by)
VALUES
('a0000000-0000-0000-0000-000000000001', 'Computer / Information Systems', 'ACTIVE', 'fixture'),
('b0000000-0000-0000-0000-000000000001', 'Management / Organization Studies', 'ACTIVE', 'fixture');

INSERT INTO research_profile_version (
    id, profile_id, version_no, summary, configuration_jsonb, created_by
)
VALUES
(
 'a1000000-0000-0000-0000-000000000001',
 'a0000000-0000-0000-0000-000000000001',
 1,
 'Synthetic reference profile for Computer / Information Systems.',
 '{"watch_terms":["IT governance","digital government","enterprise architecture"],"fixture":true}'::jsonb,
 'fixture'
),
(
 'b1000000-0000-0000-0000-000000000001',
 'b0000000-0000-0000-0000-000000000001',
 1,
 'Synthetic reference profile for Management / Organization Studies.',
 '{"watch_terms":["organizational resilience","human behaviour","human capability"],"fixture":true}'::jsonb,
 'fixture'
);

UPDATE research_profile
SET current_version_id = 'a1000000-0000-0000-0000-000000000001'
WHERE id = 'a0000000-0000-0000-0000-000000000001';

UPDATE research_profile
SET current_version_id = 'b1000000-0000-0000-0000-000000000001'
WHERE id = 'b0000000-0000-0000-0000-000000000001';

INSERT INTO research_project (id, profile_id, name, status, created_by)
VALUES
(
 'a2000000-0000-0000-0000-000000000001',
 'a0000000-0000-0000-0000-000000000001',
 'Synthetic Digital Governance Study',
 'ACTIVE',
 'fixture'
),
(
 'b2000000-0000-0000-0000-000000000001',
 'b0000000-0000-0000-0000-000000000001',
 'Synthetic Organizational Resilience Study',
 'ACTIVE',
 'fixture'
);

INSERT INTO research_project_version (
    id, project_id, version_no, research_intent, provisional_rq_text, project_configuration_jsonb, created_by
)
VALUES
(
 'a3000000-0000-0000-0000-000000000001',
 'a2000000-0000-0000-0000-000000000001',
 1,
 'Fixture intent: investigate a possible digital-governance coordination gap without asserting that the gap is true.',
 'How might cross-unit governance coordination differ across digital public-service contexts?',
 '{"fixture":true,"priority":"evidence_trace"}'::jsonb,
 'fixture'
),
(
 'b3000000-0000-0000-0000-000000000001',
 'b2000000-0000-0000-0000-000000000001',
 1,
 'Fixture intent: investigate a possible organizational-resilience capability gap without asserting that the gap is true.',
 'How might human capability shape resilience responses across organizational contexts?',
 '{"fixture":true,"priority":"evidence_trace"}'::jsonb,
 'fixture'
);

UPDATE research_project
SET current_version_id = 'a3000000-0000-0000-0000-000000000001'
WHERE id = 'a2000000-0000-0000-0000-000000000001';

UPDATE research_project
SET current_version_id = 'b3000000-0000-0000-0000-000000000001'
WHERE id = 'b2000000-0000-0000-0000-000000000001';

INSERT INTO literature_source (id, source_key, name, source_type, active, configuration_reference)
VALUES
('c0000000-0000-0000-0000-000000000001', 'fixture_openalex', 'Fixture OpenAlex-like Source', 'BIBLIOGRAPHIC_API', true, 'fixture://openalex'),
('c0000000-0000-0000-0000-000000000002', 'fixture_s2', 'Fixture Semantic-Scholar-like Source', 'BIBLIOGRAPHIC_API', true, 'fixture://s2');

INSERT INTO source_record (
    id, literature_source_id, source_record_identifier, retrieved_at,
    raw_metadata_jsonb, content_access_state, normalization_state, provenance_hash
)
VALUES
(
 'd0000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000001', 'FIX-A-SUPPORT',
 '2026-09-08T08:00:00+07:00',
 '{"fixture":true,"title":"Synthetic IS Support Work"}'::jsonb,
 'ABSTRACT_ONLY', 'MATCHED', 'fixture-hash-a-support'
),
(
 'd0000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000002', 'FIX-A-CHALLENGE',
 '2026-09-08T08:05:00+07:00',
 '{"fixture":true,"title":"Synthetic IS Challenge Work"}'::jsonb,
 'ABSTRACT_ONLY', 'MATCHED', 'fixture-hash-a-challenge'
),
(
 'd0000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000001', 'FIX-B-SUPPORT',
 '2026-09-08T08:10:00+07:00',
 '{"fixture":true,"title":"Synthetic Management Support Work"}'::jsonb,
 'ABSTRACT_ONLY', 'MATCHED', 'fixture-hash-b-support'
),
(
 'd0000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000002', 'FIX-B-CHALLENGE',
 '2026-09-08T08:15:00+07:00',
 '{"fixture":true,"title":"Synthetic Management Challenge Work"}'::jsonb,
 'ABSTRACT_ONLY', 'MATCHED', 'fixture-hash-b-challenge'
);

INSERT INTO work (
    id, title, publication_date, publication_year, venue, work_type, current_access_level
)
VALUES
('e0000000-0000-0000-0000-000000000001', 'Synthetic Fixture: Coordination Limitations in Digital Governance', '2025-05-01', 2025, 'Fixture Journal A', 'ARTICLE', 'ABSTRACT_ONLY'),
('e0000000-0000-0000-0000-000000000002', 'Synthetic Fixture: Coordination Practices Already Addressing Digital Governance', '2026-01-15', 2026, 'Fixture Journal A', 'ARTICLE', 'ABSTRACT_ONLY'),
('e0000000-0000-0000-0000-000000000003', 'Synthetic Fixture: Human Capability Limitations in Organizational Resilience', '2025-06-01', 2025, 'Fixture Journal B', 'ARTICLE', 'ABSTRACT_ONLY'),
('e0000000-0000-0000-0000-000000000004', 'Synthetic Fixture: Established Capability Practices in Organizational Resilience', '2026-02-01', 2026, 'Fixture Journal B', 'ARTICLE', 'ABSTRACT_ONLY');

INSERT INTO work_identifier (id, work_id, identifier_type, identifier_value, is_primary)
VALUES
('e1000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000001', 'OTHER', 'fixture:a:support', true),
('e1000000-0000-0000-0000-000000000002', 'e0000000-0000-0000-0000-000000000002', 'OTHER', 'fixture:a:challenge', true),
('e1000000-0000-0000-0000-000000000003', 'e0000000-0000-0000-0000-000000000003', 'OTHER', 'fixture:b:support', true),
('e1000000-0000-0000-0000-000000000004', 'e0000000-0000-0000-0000-000000000004', 'OTHER', 'fixture:b:challenge', true);

INSERT INTO work_source_record (id, work_id, source_record_id, match_method, match_state, matched_at)
VALUES
('f0000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000001', 'd0000000-0000-0000-0000-000000000001', 'fixture_identifier', 'MATCHED', '2026-09-08T08:20:00+07:00'),
('f0000000-0000-0000-0000-000000000002', 'e0000000-0000-0000-0000-000000000002', 'd0000000-0000-0000-0000-000000000002', 'fixture_identifier', 'MATCHED', '2026-09-08T08:21:00+07:00'),
('f0000000-0000-0000-0000-000000000003', 'e0000000-0000-0000-0000-000000000003', 'd0000000-0000-0000-0000-000000000003', 'fixture_identifier', 'MATCHED', '2026-09-08T08:22:00+07:00'),
('f0000000-0000-0000-0000-000000000004', 'e0000000-0000-0000-0000-000000000004', 'd0000000-0000-0000-0000-000000000004', 'fixture_identifier', 'MATCHED', '2026-09-08T08:23:00+07:00');

INSERT INTO project_work_relevance (
    id, project_id, work_id, relevance_state, relevance_advice, rationale, origin,
    first_seen_at, last_seen_at
)
VALUES
('f1000000-0000-0000-0000-000000000001', 'a2000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000001', 'RELEVANT', 84.00, 'Synthetic support-side evidence candidate.', 'fixture', '2026-09-08T08:20:00+07:00', '2026-09-08T08:20:00+07:00'),
('f1000000-0000-0000-0000-000000000002', 'a2000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000002', 'RELEVANT', 87.00, 'Synthetic challenge-side evidence candidate.', 'fixture', '2026-09-08T08:21:00+07:00', '2026-09-08T08:21:00+07:00'),
('f1000000-0000-0000-0000-000000000003', 'b2000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000003', 'RELEVANT', 83.00, 'Synthetic support-side evidence candidate.', 'fixture', '2026-09-08T08:22:00+07:00', '2026-09-08T08:22:00+07:00'),
('f1000000-0000-0000-0000-000000000004', 'b2000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000004', 'RELEVANT', 86.00, 'Synthetic challenge-side evidence candidate.', 'fixture', '2026-09-08T08:23:00+07:00', '2026-09-08T08:23:00+07:00');

INSERT INTO evidence_fragment (
    id, work_id, source_record_id, access_level, fragment_type, locator_jsonb,
    text_or_reference, content_hash, extraction_version
)
VALUES
('01000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000001', 'd0000000-0000-0000-0000-000000000001', 'ABSTRACT_ONLY', 'ABSTRACT_SEGMENT', '{"segment":1,"fixture":true}'::jsonb, 'Synthetic fixture passage: coordination remains inconsistent across units in the observed digital-governance setting.', 'fragment-a-support', 'fixture-v1'),
('01000000-0000-0000-0000-000000000002', 'e0000000-0000-0000-0000-000000000002', 'd0000000-0000-0000-0000-000000000002', 'ABSTRACT_ONLY', 'ABSTRACT_SEGMENT', '{"segment":1,"fixture":true}'::jsonb, 'Synthetic fixture passage: established coordination practices substantially address the previously reported governance limitation.', 'fragment-a-challenge', 'fixture-v1'),
('01000000-0000-0000-0000-000000000003', 'e0000000-0000-0000-0000-000000000003', 'd0000000-0000-0000-0000-000000000003', 'ABSTRACT_ONLY', 'ABSTRACT_SEGMENT', '{"segment":1,"fixture":true}'::jsonb, 'Synthetic fixture passage: resilience responses vary with uneven human capability development.', 'fragment-b-support', 'fixture-v1'),
('01000000-0000-0000-0000-000000000004', 'e0000000-0000-0000-0000-000000000004', 'd0000000-0000-0000-0000-000000000004', 'ABSTRACT_ONLY', 'ABSTRACT_SEGMENT', '{"segment":1,"fixture":true}'::jsonb, 'Synthetic fixture passage: established capability routines reduce the proposed resilience limitation in comparable settings.', 'fragment-b-challenge', 'fixture-v1');

INSERT INTO claim (
    id, evidence_fragment_id, claim_text, claim_type, scope_jsonb,
    extraction_origin, review_state
)
VALUES
('02000000-0000-0000-0000-000000000001', '01000000-0000-0000-0000-000000000001', 'Coordination inconsistency remains observable in the synthetic digital-governance setting.', 'FINDING', '{"fixture":true}'::jsonb, 'fixture_extractor', 'NEEDS_REVIEW'),
('02000000-0000-0000-0000-000000000002', '01000000-0000-0000-0000-000000000002', 'Established coordination practices may substantially address the proposed digital-governance limitation.', 'FINDING', '{"fixture":true}'::jsonb, 'fixture_extractor', 'NEEDS_REVIEW'),
('02000000-0000-0000-0000-000000000003', '01000000-0000-0000-0000-000000000003', 'Uneven human capability is associated with variation in synthetic organizational-resilience responses.', 'FINDING', '{"fixture":true}'::jsonb, 'fixture_extractor', 'NEEDS_REVIEW'),
('02000000-0000-0000-0000-000000000004', '01000000-0000-0000-0000-000000000004', 'Established capability routines may reduce the proposed resilience limitation in comparable settings.', 'FINDING', '{"fixture":true}'::jsonb, 'fixture_extractor', 'NEEDS_REVIEW');

INSERT INTO research_object_identity (
    id, object_type, profile_id, project_id, canonical_label, lifecycle_state, origin, created_by
)
VALUES
('a4000000-0000-0000-0000-000000000001', 'GAP_CANDIDATE', 'a0000000-0000-0000-0000-000000000001', 'a2000000-0000-0000-0000-000000000001', 'Synthetic GAP-A: cross-unit digital-governance coordination', 'ACTIVE', 'fixture', 'fixture'),
('b4000000-0000-0000-0000-000000000001', 'GAP_CANDIDATE', 'b0000000-0000-0000-0000-000000000001', 'b2000000-0000-0000-0000-000000000001', 'Synthetic GAP-B: human capability in organizational resilience', 'ACTIVE', 'fixture', 'fixture');

INSERT INTO gap_candidate (
    id, project_id, gap_type, statement, scope_jsonb, current_evolution_state
)
VALUES
('a4000000-0000-0000-0000-000000000001', 'a2000000-0000-0000-0000-000000000001', 'THEORETICAL_GAP', 'Synthetic candidate: existing explanations may insufficiently account for cross-unit coordination variation in digital governance.', '{"fixture":true}'::jsonb, 'CONTESTED'),
('b4000000-0000-0000-0000-000000000001', 'b2000000-0000-0000-0000-000000000001', 'EMPIRICAL_GAP', 'Synthetic candidate: evidence may insufficiently explain how human capability shapes resilience responses across contexts.', '{"fixture":true}'::jsonb, 'CONTESTED');

INSERT INTO evidence_relationship (
    id, claim_id, target_research_object_id, semantic_type, rationale, origin, review_state
)
VALUES
('03000000-0000-0000-0000-000000000001', '02000000-0000-0000-0000-000000000001', 'a4000000-0000-0000-0000-000000000001', 'SUPPORTS', 'Synthetic claim is consistent with the candidate limitation.', 'fixture', 'NEEDS_REVIEW'),
('03000000-0000-0000-0000-000000000002', '02000000-0000-0000-0000-000000000002', 'a4000000-0000-0000-0000-000000000001', 'CHALLENGES', 'Synthetic claim indicates an existing practice may already address the candidate limitation.', 'fixture', 'NEEDS_REVIEW'),
('03000000-0000-0000-0000-000000000003', '02000000-0000-0000-0000-000000000003', 'b4000000-0000-0000-0000-000000000001', 'SUPPORTS', 'Synthetic claim is consistent with the candidate limitation.', 'fixture', 'NEEDS_REVIEW'),
('03000000-0000-0000-0000-000000000004', '02000000-0000-0000-0000-000000000004', 'b4000000-0000-0000-0000-000000000001', 'CHALLENGES', 'Synthetic claim indicates established capability practices may reduce the candidate limitation.', 'fixture', 'NEEDS_REVIEW');

INSERT INTO coverage_context (
    id, project_id, profile_version_id, project_version_id, observed_at,
    query_context_jsonb, temporal_window_jsonb, access_summary_jsonb,
    extraction_summary_jsonb, counter_search_state, limitations
)
VALUES
(
 '04000000-0000-0000-0000-000000000001',
 'a2000000-0000-0000-0000-000000000001',
 'a1000000-0000-0000-0000-000000000001',
 'a3000000-0000-0000-0000-000000000001',
 '2026-09-08T09:00:00+07:00',
 '{"fixture":true,"query_family":"digital_governance"}'::jsonb,
 '{"from":"2025-01-01","to":"2026-09-08"}'::jsonb,
 '{"abstract_only":2,"full_text":0}'::jsonb,
 '{"claims":2,"quarantined":0}'::jsonb,
 'PARTIAL',
 'Synthetic fixture coverage; one source marked degraded. Absence of additional evidence is not evidence of absence.'
),
(
 '04000000-0000-0000-0000-000000000002',
 'b2000000-0000-0000-0000-000000000001',
 'b1000000-0000-0000-0000-000000000001',
 'b3000000-0000-0000-0000-000000000001',
 '2026-09-08T09:05:00+07:00',
 '{"fixture":true,"query_family":"organizational_resilience"}'::jsonb,
 '{"from":"2025-01-01","to":"2026-09-08"}'::jsonb,
 '{"abstract_only":2,"full_text":0}'::jsonb,
 '{"claims":2,"quarantined":0}'::jsonb,
 'PARTIAL',
 'Synthetic fixture coverage; one source marked degraded. Absence of additional evidence is not evidence of absence.'
);

INSERT INTO coverage_source_state (
    id, coverage_context_id, literature_source_id, health_state,
    attempted_record_count, observed_record_count, access_limitations, degradation_reason
)
VALUES
('04100000-0000-0000-0000-000000000001', '04000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000001', 'HEALTHY', 1, 1, 'ABSTRACT_ONLY fixture access', NULL),
('04100000-0000-0000-0000-000000000002', '04000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000002', 'DEGRADED', 1, 1, 'ABSTRACT_ONLY fixture access', 'Synthetic degradation for coverage-context testing.'),
('04100000-0000-0000-0000-000000000003', '04000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000001', 'HEALTHY', 1, 1, 'ABSTRACT_ONLY fixture access', NULL),
('04100000-0000-0000-0000-000000000004', '04000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000002', 'DEGRADED', 1, 1, 'ABSTRACT_ONLY fixture access', 'Synthetic degradation for coverage-context testing.');

INSERT INTO assessment (
    id, project_id, target_research_object_id, coverage_context_id,
    assessment_type, model_or_agent, model_version, explanation_summary, assessed_at
)
VALUES
('05000000-0000-0000-0000-000000000001', 'a2000000-0000-0000-0000-000000000001', 'a4000000-0000-0000-0000-000000000001', '04000000-0000-0000-0000-000000000001', 'GAP_REVIEW_ADVICE', 'fixture_agent', 'v1', 'Synthetic advice: support and challenge evidence coexist; human review remains required.', '2026-09-08T09:10:00+07:00'),
('05000000-0000-0000-0000-000000000002', 'b2000000-0000-0000-0000-000000000001', 'b4000000-0000-0000-0000-000000000001', '04000000-0000-0000-0000-000000000002', 'GAP_REVIEW_ADVICE', 'fixture_agent', 'v1', 'Synthetic advice: support and challenge evidence coexist; human review remains required.', '2026-09-08T09:15:00+07:00');

INSERT INTO assessment_dimension (
    id, assessment_id, dimension_type, value_numeric, value_text, explanation
)
VALUES
('05100000-0000-0000-0000-000000000001', '05000000-0000-0000-0000-000000000001', 'GAP_EVIDENCE_STRENGTH', 62.00, NULL, 'Synthetic attention score, not probability.'),
('05100000-0000-0000-0000-000000000002', '05000000-0000-0000-0000-000000000001', 'COUNTER_EVIDENCE_RISK', 58.00, NULL, 'Challenge evidence is present.'),
('05100000-0000-0000-0000-000000000003', '05000000-0000-0000-0000-000000000001', 'EVIDENCE_COVERAGE_CONTEXT', NULL, 'PARTIAL', 'Fixture source degradation limits observable coverage.'),
('05100000-0000-0000-0000-000000000004', '05000000-0000-0000-0000-000000000001', 'REVIEW_PRIORITY', 78.00, NULL, 'Contested evidence merits human attention.'),
('05100000-0000-0000-0000-000000000005', '05000000-0000-0000-0000-000000000002', 'GAP_EVIDENCE_STRENGTH', 61.00, NULL, 'Synthetic attention score, not probability.'),
('05100000-0000-0000-0000-000000000006', '05000000-0000-0000-0000-000000000002', 'COUNTER_EVIDENCE_RISK', 60.00, NULL, 'Challenge evidence is present.'),
('05100000-0000-0000-0000-000000000007', '05000000-0000-0000-0000-000000000002', 'EVIDENCE_COVERAGE_CONTEXT', NULL, 'PARTIAL', 'Fixture source degradation limits observable coverage.'),
('05100000-0000-0000-0000-000000000008', '05000000-0000-0000-0000-000000000002', 'REVIEW_PRIORITY', 80.00, NULL, 'Contested evidence merits human attention.');

INSERT INTO change_event (
    id, project_id, primary_research_object_id, coverage_context_id,
    change_type, observed_at, previous_state_jsonb, current_state_jsonb, reasoning_delta
)
VALUES
('06000000-0000-0000-0000-000000000001', 'a2000000-0000-0000-0000-000000000001', 'a4000000-0000-0000-0000-000000000001', '04000000-0000-0000-0000-000000000001', 'GAP_CONTESTED', '2026-09-08T09:20:00+07:00', '{"state":"CANDIDATE"}'::jsonb, '{"state":"CONTESTED"}'::jsonb, 'Synthetic support and challenge claims now coexist; this is an attention signal, not a verdict.'),
('06000000-0000-0000-0000-000000000002', 'b2000000-0000-0000-0000-000000000001', 'b4000000-0000-0000-0000-000000000001', '04000000-0000-0000-0000-000000000002', 'GAP_CONTESTED', '2026-09-08T09:25:00+07:00', '{"state":"CANDIDATE"}'::jsonb, '{"state":"CONTESTED"}'::jsonb, 'Synthetic support and challenge claims now coexist; this is an attention signal, not a verdict.');

INSERT INTO human_decision (
    id, project_id, primary_research_object_id, assessment_id, coverage_context_id,
    decision_type, rationale, actor, decided_at
)
VALUES
('07000000-0000-0000-0000-000000000001', 'a2000000-0000-0000-0000-000000000001', 'a4000000-0000-0000-0000-000000000001', '05000000-0000-0000-0000-000000000001', '04000000-0000-0000-0000-000000000001', 'NEED_MORE_EVIDENCE', 'Fixture human decision: contested evidence and partial coverage require more evidence before direction is accepted.', 'fixture_human', '2026-09-08T09:30:00+07:00'),
('07000000-0000-0000-0000-000000000002', 'b2000000-0000-0000-0000-000000000001', 'b4000000-0000-0000-0000-000000000001', '05000000-0000-0000-0000-000000000002', '04000000-0000-0000-0000-000000000002', 'NEED_MORE_EVIDENCE', 'Fixture human decision: contested evidence and partial coverage require more evidence before direction is accepted.', 'fixture_human', '2026-09-08T09:35:00+07:00');

COMMIT;
