-- GFPROJCLAW — Migration 001: Canonical Vertical Slice
-- J2 SQL Draft v0
-- Created: 2026-09-08
-- PostgreSQL: 16.x target family
-- Policy: forward-only versioned migration; ordinary transaction rollback on DDL failure.
-- Scientific principle: constraints protect provenance and identity, not scientific verdicts.

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE research_profile (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL CHECK (btrim(name) <> ''),
    status text NOT NULL CHECK (status IN ('ACTIVE','INACTIVE','ARCHIVED')),
    current_version_id uuid NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by text NULL
);

CREATE TABLE research_profile_version (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id uuid NOT NULL REFERENCES research_profile(id) ON DELETE RESTRICT,
    version_no integer NOT NULL CHECK (version_no > 0),
    summary text NULL,
    configuration_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    supersedes_version_id uuid NULL REFERENCES research_profile_version(id) ON DELETE RESTRICT,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by text NULL,
    CONSTRAINT research_profile_version_no_uk UNIQUE (profile_id, version_no),
    CONSTRAINT research_profile_version_profile_id_id_uk UNIQUE (profile_id, id),
    CONSTRAINT research_profile_version_no_self_supersede_ck CHECK (supersedes_version_id IS NULL OR supersedes_version_id <> id)
);

ALTER TABLE research_profile
    ADD CONSTRAINT research_profile_current_version_fk
    FOREIGN KEY (id, current_version_id)
    REFERENCES research_profile_version(profile_id, id)
    ON DELETE RESTRICT;

CREATE INDEX research_profile_version_profile_version_idx
    ON research_profile_version(profile_id, version_no DESC);

CREATE TABLE research_project (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id uuid NOT NULL REFERENCES research_profile(id) ON DELETE RESTRICT,
    name text NOT NULL CHECK (btrim(name) <> ''),
    status text NOT NULL CHECK (status IN ('ACTIVE','PAUSED','ARCHIVED')),
    current_version_id uuid NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by text NULL
);

CREATE INDEX research_project_profile_status_idx
    ON research_project(profile_id, status);

CREATE TABLE research_project_version (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES research_project(id) ON DELETE RESTRICT,
    version_no integer NOT NULL CHECK (version_no > 0),
    research_intent text NULL,
    provisional_rq_text text NULL,
    project_configuration_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    supersedes_version_id uuid NULL REFERENCES research_project_version(id) ON DELETE RESTRICT,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by text NULL,
    CONSTRAINT research_project_version_no_uk UNIQUE (project_id, version_no),
    CONSTRAINT research_project_version_project_id_id_uk UNIQUE (project_id, id),
    CONSTRAINT research_project_version_no_self_supersede_ck CHECK (supersedes_version_id IS NULL OR supersedes_version_id <> id)
);

ALTER TABLE research_project
    ADD CONSTRAINT research_project_current_version_fk
    FOREIGN KEY (id, current_version_id)
    REFERENCES research_project_version(project_id, id)
    ON DELETE RESTRICT;

CREATE INDEX research_project_version_project_version_idx
    ON research_project_version(project_id, version_no DESC);

CREATE TABLE literature_source (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_key text NOT NULL UNIQUE CHECK (btrim(source_key) <> ''),
    name text NOT NULL CHECK (btrim(name) <> ''),
    source_type text NOT NULL CHECK (btrim(source_type) <> ''),
    active boolean NOT NULL DEFAULT true,
    configuration_reference text NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE source_record (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    literature_source_id uuid NOT NULL REFERENCES literature_source(id) ON DELETE RESTRICT,
    source_record_identifier text NOT NULL CHECK (btrim(source_record_identifier) <> ''),
    retrieved_at timestamptz NOT NULL,
    raw_metadata_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    content_access_state text NOT NULL CHECK (content_access_state IN ('FULL_TEXT','ABSTRACT_ONLY','METADATA_ONLY')),
    normalization_state text NOT NULL CHECK (normalization_state IN ('UNRESOLVED','MATCHED','NEW_WORK','AMBIGUOUS','QUARANTINED')),
    provenance_hash text NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT source_record_retrieval_uk UNIQUE (literature_source_id, source_record_identifier, retrieved_at)
);

CREATE INDEX source_record_source_identifier_idx
    ON source_record(literature_source_id, source_record_identifier);
CREATE INDEX source_record_retrieved_idx
    ON source_record(retrieved_at DESC);

CREATE TABLE work (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title text NOT NULL CHECK (btrim(title) <> ''),
    publication_date date NULL,
    publication_year smallint NULL CHECK (publication_year IS NULL OR publication_year BETWEEN 1000 AND 3000),
    venue text NULL,
    work_type text NULL,
    current_access_level text NOT NULL CHECK (current_access_level IN ('FULL_TEXT','ABSTRACT_ONLY','METADATA_ONLY')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX work_publication_year_idx
    ON work(publication_year DESC);

CREATE TABLE work_identifier (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    work_id uuid NOT NULL REFERENCES work(id) ON DELETE RESTRICT,
    identifier_type text NOT NULL CHECK (identifier_type IN ('DOI','OPENALEX','SEMANTIC_SCHOLAR','PMID','ISBN','OTHER')),
    identifier_value text NOT NULL CHECK (btrim(identifier_value) <> ''),
    is_primary boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT work_identifier_global_uk UNIQUE (identifier_type, identifier_value),
    CONSTRAINT work_identifier_work_uk UNIQUE (work_id, identifier_type, identifier_value)
);

CREATE INDEX work_identifier_work_idx
    ON work_identifier(work_id);

CREATE TABLE work_source_record (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    work_id uuid NOT NULL REFERENCES work(id) ON DELETE RESTRICT,
    source_record_id uuid NOT NULL REFERENCES source_record(id) ON DELETE RESTRICT,
    match_method text NOT NULL CHECK (btrim(match_method) <> ''),
    match_state text NOT NULL CHECK (match_state IN ('MATCHED','PROVISIONAL','HUMAN_REVIEWED')),
    matched_at timestamptz NOT NULL,
    CONSTRAINT work_source_record_source_uk UNIQUE (source_record_id),
    CONSTRAINT work_source_record_pair_uk UNIQUE (work_id, source_record_id)
);

CREATE INDEX work_source_record_work_idx
    ON work_source_record(work_id);

CREATE TABLE project_work_relevance (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES research_project(id) ON DELETE RESTRICT,
    work_id uuid NOT NULL REFERENCES work(id) ON DELETE RESTRICT,
    relevance_state text NOT NULL CHECK (relevance_state IN ('CANDIDATE','RELEVANT','LOW_RELEVANCE','EXCLUDED','NEEDS_REVIEW')),
    relevance_advice numeric(5,2) NULL CHECK (relevance_advice IS NULL OR relevance_advice BETWEEN 0 AND 100),
    rationale text NULL,
    origin text NOT NULL CHECK (btrim(origin) <> ''),
    human_review_state text NULL,
    first_seen_at timestamptz NOT NULL,
    last_seen_at timestamptz NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT project_work_relevance_pair_uk UNIQUE (project_id, work_id),
    CONSTRAINT project_work_relevance_time_ck CHECK (last_seen_at >= first_seen_at)
);

CREATE INDEX project_work_relevance_project_state_idx
    ON project_work_relevance(project_id, relevance_state);
CREATE INDEX project_work_relevance_project_seen_idx
    ON project_work_relevance(project_id, last_seen_at DESC);

CREATE TABLE evidence_fragment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    work_id uuid NOT NULL REFERENCES work(id) ON DELETE RESTRICT,
    source_record_id uuid NULL REFERENCES source_record(id) ON DELETE RESTRICT,
    access_level text NOT NULL CHECK (access_level IN ('FULL_TEXT','ABSTRACT_ONLY')),
    fragment_type text NOT NULL CHECK (fragment_type IN ('PASSAGE','ABSTRACT_SEGMENT','STRUCTURED_RECORD_EXCERPT')),
    locator_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    text_or_reference text NOT NULL CHECK (btrim(text_or_reference) <> ''),
    content_hash text NULL,
    extraction_version text NULL,
    quarantine_state text NOT NULL DEFAULT 'ACTIVE' CHECK (quarantine_state IN ('ACTIVE','QUARANTINED')),
    quarantine_reason text NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT evidence_fragment_quarantine_ck CHECK (
        (quarantine_state = 'ACTIVE' AND quarantine_reason IS NULL)
        OR
        (quarantine_state = 'QUARANTINED' AND quarantine_reason IS NOT NULL AND btrim(quarantine_reason) <> '')
    )
);

CREATE INDEX evidence_fragment_work_idx
    ON evidence_fragment(work_id);
CREATE INDEX evidence_fragment_source_record_idx
    ON evidence_fragment(source_record_id) WHERE source_record_id IS NOT NULL;
CREATE INDEX evidence_fragment_content_hash_idx
    ON evidence_fragment(content_hash) WHERE content_hash IS NOT NULL;

CREATE TABLE claim (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_fragment_id uuid NOT NULL REFERENCES evidence_fragment(id) ON DELETE RESTRICT,
    claim_text text NOT NULL CHECK (btrim(claim_text) <> ''),
    claim_type text NULL,
    scope_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    extraction_origin text NOT NULL CHECK (btrim(extraction_origin) <> ''),
    review_state text NOT NULL CHECK (review_state IN ('MACHINE_EXTRACTED','NEEDS_REVIEW','HUMAN_REVIEWED','CONTESTED','QUARANTINED')),
    supersedes_claim_id uuid NULL REFERENCES claim(id) ON DELETE RESTRICT,
    quarantine_state text NOT NULL DEFAULT 'ACTIVE' CHECK (quarantine_state IN ('ACTIVE','QUARANTINED')),
    quarantine_reason text NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT claim_no_self_supersede_ck CHECK (supersedes_claim_id IS NULL OR supersedes_claim_id <> id),
    CONSTRAINT claim_quarantine_ck CHECK (
        (quarantine_state = 'ACTIVE' AND quarantine_reason IS NULL AND review_state <> 'QUARANTINED')
        OR
        (quarantine_state = 'QUARANTINED' AND quarantine_reason IS NOT NULL AND btrim(quarantine_reason) <> '' AND review_state = 'QUARANTINED')
    )
);

CREATE INDEX claim_fragment_idx
    ON claim(evidence_fragment_id);
CREATE INDEX claim_review_state_idx
    ON claim(review_state);

CREATE TABLE research_object_identity (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    object_type text NOT NULL CHECK (object_type IN ('GAP_CANDIDATE')),
    profile_id uuid NULL REFERENCES research_profile(id) ON DELETE RESTRICT,
    project_id uuid NULL REFERENCES research_project(id) ON DELETE RESTRICT,
    canonical_label text NOT NULL CHECK (btrim(canonical_label) <> ''),
    lifecycle_state text NOT NULL CHECK (lifecycle_state IN ('ACTIVE','INACTIVE','SUPERSEDED','QUARANTINED')),
    origin text NOT NULL CHECK (btrim(origin) <> ''),
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by text NULL,
    CONSTRAINT research_object_identity_project_scope_ck CHECK (object_type <> 'GAP_CANDIDATE' OR project_id IS NOT NULL),
    CONSTRAINT research_object_identity_id_project_uk UNIQUE (id, project_id)
);

CREATE INDEX research_object_identity_project_type_state_idx
    ON research_object_identity(project_id, object_type, lifecycle_state);

CREATE TABLE gap_candidate (
    id uuid PRIMARY KEY,
    project_id uuid NOT NULL,
    gap_type text NOT NULL CHECK (gap_type IN ('EXPLICIT_GAP','EMPIRICAL_GAP','THEORETICAL_GAP','SYNTHESIS_GAP')),
    statement text NOT NULL CHECK (btrim(statement) <> ''),
    scope_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    current_evolution_state text NOT NULL CHECK (current_evolution_state IN ('CANDIDATE','STRENGTHENING','WEAKENING','CONTESTED','POSSIBLY_CLOSED','REOPENED')),
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT gap_candidate_identity_project_fk
        FOREIGN KEY (id, project_id)
        REFERENCES research_object_identity(id, project_id)
        ON DELETE RESTRICT,
    CONSTRAINT gap_candidate_project_fk
        FOREIGN KEY (project_id)
        REFERENCES research_project(id)
        ON DELETE RESTRICT
);

CREATE INDEX gap_candidate_project_state_idx
    ON gap_candidate(project_id, current_evolution_state);
CREATE INDEX gap_candidate_project_type_idx
    ON gap_candidate(project_id, gap_type);

CREATE TABLE evidence_relationship (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id uuid NOT NULL REFERENCES claim(id) ON DELETE RESTRICT,
    target_research_object_id uuid NOT NULL REFERENCES research_object_identity(id) ON DELETE RESTRICT,
    semantic_type text NOT NULL CHECK (semantic_type IN ('SUPPORTS','CHALLENGES','EXTENDS','REPLICATES','CONTRADICTS','ADDRESSES')),
    rationale text NULL,
    origin text NOT NULL CHECK (btrim(origin) <> ''),
    review_state text NOT NULL CHECK (review_state IN ('MACHINE_SUGGESTED','NEEDS_REVIEW','HUMAN_REVIEWED','CONTESTED','QUARANTINED')),
    supersedes_relationship_id uuid NULL REFERENCES evidence_relationship(id) ON DELETE RESTRICT,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT evidence_relationship_no_self_supersede_ck CHECK (supersedes_relationship_id IS NULL OR supersedes_relationship_id <> id)
);

CREATE INDEX evidence_relationship_target_semantic_idx
    ON evidence_relationship(target_research_object_id, semantic_type);
CREATE INDEX evidence_relationship_claim_idx
    ON evidence_relationship(claim_id);
CREATE INDEX evidence_relationship_review_state_idx
    ON evidence_relationship(review_state);

CREATE TABLE coverage_context (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES research_project(id) ON DELETE RESTRICT,
    profile_version_id uuid NOT NULL REFERENCES research_profile_version(id) ON DELETE RESTRICT,
    project_version_id uuid NULL REFERENCES research_project_version(id) ON DELETE RESTRICT,
    observed_at timestamptz NOT NULL,
    query_context_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    temporal_window_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    access_summary_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    extraction_summary_jsonb jsonb NOT NULL DEFAULT '{}'::jsonb,
    counter_search_state text NOT NULL CHECK (counter_search_state IN ('NOT_RUN','PARTIAL','RUN','DEGRADED')),
    limitations text NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX coverage_context_project_observed_idx
    ON coverage_context(project_id, observed_at DESC);
CREATE INDEX coverage_context_profile_version_idx
    ON coverage_context(profile_version_id);

CREATE TABLE coverage_source_state (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    coverage_context_id uuid NOT NULL REFERENCES coverage_context(id) ON DELETE RESTRICT,
    literature_source_id uuid NOT NULL REFERENCES literature_source(id) ON DELETE RESTRICT,
    health_state text NOT NULL CHECK (health_state IN ('HEALTHY','DEGRADED','BACKOFF','DISABLED','ATTENTION')),
    attempted_record_count integer NULL CHECK (attempted_record_count IS NULL OR attempted_record_count >= 0),
    observed_record_count integer NULL CHECK (observed_record_count IS NULL OR observed_record_count >= 0),
    access_limitations text NULL,
    degradation_reason text NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT coverage_source_state_pair_uk UNIQUE (coverage_context_id, literature_source_id)
);

CREATE INDEX coverage_source_state_source_created_idx
    ON coverage_source_state(literature_source_id, created_at DESC);

CREATE TABLE assessment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES research_project(id) ON DELETE RESTRICT,
    target_research_object_id uuid NOT NULL,
    coverage_context_id uuid NULL REFERENCES coverage_context(id) ON DELETE RESTRICT,
    assessment_type text NOT NULL CHECK (btrim(assessment_type) <> ''),
    model_or_agent text NULL,
    model_version text NULL,
    explanation_summary text NULL,
    assessed_at timestamptz NOT NULL,
    supersedes_assessment_id uuid NULL REFERENCES assessment(id) ON DELETE RESTRICT,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT assessment_no_self_supersede_ck CHECK (supersedes_assessment_id IS NULL OR supersedes_assessment_id <> id),
    CONSTRAINT assessment_target_project_fk
        FOREIGN KEY (target_research_object_id, project_id)
        REFERENCES research_object_identity(id, project_id)
        ON DELETE RESTRICT
);

CREATE INDEX assessment_target_assessed_idx
    ON assessment(target_research_object_id, assessed_at DESC);
CREATE INDEX assessment_project_assessed_idx
    ON assessment(project_id, assessed_at DESC);

CREATE TABLE assessment_dimension (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id uuid NOT NULL REFERENCES assessment(id) ON DELETE RESTRICT,
    dimension_type text NOT NULL CHECK (dimension_type IN (
        'GAP_EVIDENCE_STRENGTH',
        'COUNTER_EVIDENCE_RISK',
        'EVIDENCE_COVERAGE_CONTEXT',
        'REVIEW_PRIORITY',
        'NOVELTY_POTENTIAL',
        'THEORETICAL_SIGNIFICANCE',
        'METHODOLOGICAL_FEASIBILITY'
    )),
    value_numeric numeric(6,2) NULL,
    value_text text NULL,
    explanation text NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT assessment_dimension_type_uk UNIQUE (assessment_id, dimension_type),
    CONSTRAINT assessment_dimension_value_ck CHECK (value_numeric IS NOT NULL OR value_text IS NOT NULL)
);

CREATE INDEX assessment_dimension_assessment_idx
    ON assessment_dimension(assessment_id);

CREATE TABLE change_event (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES research_project(id) ON DELETE RESTRICT,
    primary_research_object_id uuid NOT NULL,
    coverage_context_id uuid NULL REFERENCES coverage_context(id) ON DELETE RESTRICT,
    change_type text NOT NULL CHECK (change_type IN (
        'EVIDENCE_ADDED',
        'EVIDENCE_CHALLENGED',
        'EVIDENCE_CONTRADICTED',
        'GAP_STRENGTHENED',
        'GAP_WEAKENED',
        'GAP_CONTESTED',
        'GAP_POSSIBLY_CLOSED',
        'GAP_REOPENED',
        'ASSESSMENT_CHANGED',
        'COVERAGE_CHANGED'
    )),
    observed_at timestamptz NOT NULL,
    previous_state_jsonb jsonb NULL,
    current_state_jsonb jsonb NULL,
    reasoning_delta text NOT NULL CHECK (btrim(reasoning_delta) <> ''),
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT change_event_object_project_fk
        FOREIGN KEY (primary_research_object_id, project_id)
        REFERENCES research_object_identity(id, project_id)
        ON DELETE RESTRICT
);

CREATE INDEX change_event_project_observed_idx
    ON change_event(project_id, observed_at DESC);
CREATE INDEX change_event_object_observed_idx
    ON change_event(primary_research_object_id, observed_at DESC);
CREATE INDEX change_event_type_observed_idx
    ON change_event(change_type, observed_at DESC);

CREATE TABLE human_decision (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES research_project(id) ON DELETE RESTRICT,
    primary_research_object_id uuid NOT NULL,
    assessment_id uuid NULL REFERENCES assessment(id) ON DELETE RESTRICT,
    coverage_context_id uuid NULL REFERENCES coverage_context(id) ON DELETE RESTRICT,
    decision_type text NOT NULL CHECK (decision_type IN ('REVIEW','MODIFY','ACCEPT_DIRECTION','REJECT_CANDIDATE','NEED_MORE_EVIDENCE')),
    rationale text NOT NULL CHECK (btrim(rationale) <> ''),
    actor text NOT NULL CHECK (btrim(actor) <> ''),
    decided_at timestamptz NOT NULL,
    supersedes_decision_id uuid NULL REFERENCES human_decision(id) ON DELETE RESTRICT,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT human_decision_no_self_supersede_ck CHECK (supersedes_decision_id IS NULL OR supersedes_decision_id <> id),
    CONSTRAINT human_decision_object_project_fk
        FOREIGN KEY (primary_research_object_id, project_id)
        REFERENCES research_object_identity(id, project_id)
        ON DELETE RESTRICT
);

CREATE INDEX human_decision_object_decided_idx
    ON human_decision(primary_research_object_id, decided_at DESC);
CREATE INDEX human_decision_project_decided_idx
    ON human_decision(project_id, decided_at DESC);

COMMIT;
