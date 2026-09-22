from db import db


def list_context():
    with db() as conn:
        rows = conn.execute("""
            SELECT rp.id AS profile_id, rp.name AS profile_name,
                   rpv.version_no AS profile_version,
                   p.id AS project_id, p.name AS project_name,
                   pv.version_no AS project_version,
                   pv.research_intent, pv.provisional_rq_text,
                   rpv.summary AS profile_summary, rpv.configuration_jsonb AS profile_configuration_jsonb,
                   pv.project_configuration_jsonb
            FROM research_profile rp
            JOIN research_profile_version rpv ON rpv.id = rp.current_version_id
            JOIN research_project p ON p.profile_id = rp.id AND p.status = 'ACTIVE'
            JOIN research_project_version pv ON pv.id = p.current_version_id
            WHERE rp.status = 'ACTIVE'
            ORDER BY rp.name, p.name
        """).fetchall()
    return rows


def list_project_papers(project_id, limit=20):
    with db() as conn:
        rows = conn.execute("""
            SELECT w.id AS work_id, w.title, w.publication_year,
                   w.publication_date, w.venue AS venue_name, w.work_type,
                   w.current_access_level, pwr.relevance_state,
                   pwr.relevance_advice, pwr.human_review_state,
                   pwr.first_seen_at, pwr.last_seen_at,
                   ids.identifiers, src.source_key
            FROM research_project p
            JOIN project_work_relevance pwr ON pwr.project_id = p.id
            JOIN work w ON w.id = pwr.work_id
            LEFT JOIN LATERAL (
                SELECT jsonb_object_agg(identifier_type, identifier_value) AS identifiers
                FROM work_identifier wi
                WHERE wi.work_id = w.id
            ) ids ON TRUE
            LEFT JOIN LATERAL (
                SELECT ls.source_key
                FROM work_source_record wsr
                JOIN source_record sr ON sr.id = wsr.source_record_id
                JOIN literature_source ls ON ls.id = sr.literature_source_id
                WHERE wsr.work_id = w.id
                ORDER BY sr.retrieved_at DESC
                LIMIT 1
            ) src ON TRUE
            WHERE p.id = %s AND p.status = 'ACTIVE'
            ORDER BY pwr.last_seen_at DESC, w.publication_date DESC NULLS LAST,
                     w.publication_year DESC NULLS LAST, w.title
            LIMIT %s
        """, (project_id, limit)).fetchall()
    return rows


def list_project_evidence(project_id, limit=50):
    with db() as conn:
        rows = conn.execute("""
            SELECT c.id AS claim_id, c.claim_text, c.claim_type,
                   c.review_state, c.extraction_origin, c.scope_jsonb,
                   ef.id AS evidence_fragment_id, ef.fragment_type,
                   ef.access_level, ef.locator_jsonb,
                   left(ef.text_or_reference, 280) AS fragment_preview,
                   ef.extraction_version, ef.quarantine_state,
                   w.id AS work_id, w.title AS work_title,
                   w.publication_year, w.venue
            FROM research_project p
            JOIN project_work_relevance pwr ON pwr.project_id = p.id
            JOIN work w ON w.id = pwr.work_id
            JOIN evidence_fragment ef ON ef.work_id = w.id
            JOIN claim c ON c.evidence_fragment_id = ef.id
            WHERE p.id = %s AND p.status = 'ACTIVE'
            ORDER BY c.created_at DESC
            LIMIT %s
        """, (project_id, limit)).fetchall()
    return rows


def get_project_coverage(project_id):
    with db() as conn:
        row = conn.execute("""
            SELECT cc.id AS coverage_context_id, cc.observed_at,
                   cc.access_summary_jsonb, cc.extraction_summary_jsonb,
                   cc.counter_search_state, cc.limitations,
                   COALESCE(src.sources, '[]'::jsonb) AS sources
            FROM coverage_context cc
            LEFT JOIN LATERAL (
                SELECT jsonb_agg(jsonb_build_object(
                    'source_key', ls.source_key,
                    'health_state', css.health_state,
                    'observed_record_count', css.observed_record_count,
                    'attempted_record_count', css.attempted_record_count,
                    'access_limitations', css.access_limitations,
                    'degradation_reason', css.degradation_reason
                ) ORDER BY ls.source_key) AS sources
                FROM coverage_source_state css
                JOIN literature_source ls ON ls.id = css.literature_source_id
                WHERE css.coverage_context_id = cc.id
            ) src ON TRUE
            WHERE cc.project_id = %s
            ORDER BY cc.observed_at DESC
            LIMIT 1
        """, (project_id,)).fetchone()
    return row


def get_project_corpus_layers(project_id):
    """Read-only, scope-explicit corpus projection. No scientific judgment."""
    with db() as conn:
        row = conn.execute("""
            SELECT
              (SELECT count(*) FROM project_work_relevance pwr WHERE pwr.project_id=%s) AS project_corpus,
              (SELECT count(DISTINCT ef.work_id) FROM project_work_relevance pwr JOIN evidence_fragment ef ON ef.work_id=pwr.work_id WHERE pwr.project_id=%s) AS evidence_corpus,
              (SELECT count(DISTINCT c.evidence_fragment_id) FROM project_work_relevance pwr JOIN evidence_fragment ef ON ef.work_id=pwr.work_id JOIN claim c ON c.evidence_fragment_id=ef.id WHERE pwr.project_id=%s AND c.review_state NOT IN ('NEEDS_REVIEW','MACHINE_SUGGESTED')) AS human_reviewed_evidence
        """, (project_id, project_id, project_id)).fetchone()
    coverage = get_project_coverage(project_id) or {}
    sources = coverage.get('sources') or []
    observed = sum((x.get('observed_record_count') or 0) for x in sources)
    return {
      'research_universe': {'state':'UNKNOWN','count':None,'reason':'Global literature universe is not asserted by current source/query coverage.'},
      'discovery_corpus': {'state':'OBSERVED_SOURCE_RECORDS' if sources else 'NOT_AVAILABLE','count':observed if sources else None,'note':'Source-record observations may overlap; this is not a unique-work count.'},
      'deduplicated_corpus': {'state':'NOT_AVAILABLE','count':None},
      'screening_corpus': {'state':'NOT_AVAILABLE','count':None},
      'project_corpus': {'state':'AVAILABLE','count':row['project_corpus']},
      'evidence_corpus': {'state':'AVAILABLE','count':row['evidence_corpus']},
      'human_reviewed_evidence': {'state':'AVAILABLE','count':row['human_reviewed_evidence']},
      'coverage_context_id': coverage.get('coverage_context_id'), 'observed_at': coverage.get('observed_at'),
      'counter_search_state': coverage.get('counter_search_state','NOT_AVAILABLE'), 'limitations': coverage.get('limitations'),
      'sources': sources, 'scientific_decision': False
    }

def list_project_research_objects(project_id, limit=50):
    with db() as conn:
        rows = conn.execute("""
            SELECT roi.id AS research_object_id, roi.object_type, roi.canonical_label,
                   roi.lifecycle_state, roi.origin, roi.created_at,
                   COALESCE(gc.statement, idr.statement) AS statement,
                   COALESCE(gc.scope_jsonb, idr.scope_jsonb, '{}'::jsonb) AS scope_jsonb,
                   gc.gap_type,
                   CASE WHEN roi.object_type = 'GAP_CANDIDATE' THEN gc.current_evolution_state
                        WHEN roi.object_type = 'INVESTIGATION_DIRECTION' THEN idr.current_state END AS object_state,
                   hd.decision_type AS latest_human_decision,
                   hd.decided_at AS latest_human_decision_at
            FROM research_object_identity roi
            LEFT JOIN gap_candidate gc ON gc.id = roi.id AND gc.project_id = roi.project_id
            LEFT JOIN investigation_direction idr ON idr.id = roi.id AND idr.project_id = roi.project_id
            LEFT JOIN LATERAL (
                SELECT x.decision_type, x.decided_at FROM human_decision x
                WHERE x.project_id = roi.project_id AND x.primary_research_object_id = roi.id
                ORDER BY x.decided_at DESC, x.created_at DESC LIMIT 1
            ) hd ON TRUE
            WHERE roi.project_id = %s AND roi.lifecycle_state = 'ACTIVE'
            ORDER BY roi.created_at DESC LIMIT %s
        """, (project_id, limit)).fetchall()
    return rows

def list_project_gaps(project_id, limit=50):
    with db() as conn:
        rows = conn.execute("""
            SELECT gc.id AS gap_id, roi.canonical_label, gc.gap_type,
                   gc.statement, gc.scope_jsonb, gc.current_evolution_state,
                   er.id AS relationship_id, er.semantic_type,
                   er.rationale AS relationship_rationale,
                   er.review_state AS relationship_review_state,
                   c.id AS claim_id, c.claim_text, c.review_state AS claim_review_state,
                   w.id AS work_id, w.title AS work_title
            FROM gap_candidate gc
            JOIN research_object_identity roi ON roi.id = gc.id
            LEFT JOIN evidence_relationship er ON er.target_research_object_id = gc.id
            LEFT JOIN claim c ON c.id = er.claim_id
            LEFT JOIN evidence_fragment ef ON ef.id = c.evidence_fragment_id
            LEFT JOIN work w ON w.id = ef.work_id
            WHERE gc.project_id = %s AND roi.lifecycle_state = 'ACTIVE'
            ORDER BY gc.created_at DESC, er.created_at DESC NULLS LAST
            LIMIT %s
        """, (project_id, limit)).fetchall()
    return rows


ALLOWED_DECISIONS = {"REVIEW", "MODIFY", "ACCEPT_DIRECTION", "REJECT_CANDIDATE", "NEED_MORE_EVIDENCE"}


def list_project_decisions(project_id, object_id=None, limit=50):
    with db() as conn:
        rows = conn.execute("""
            SELECT hd.id AS decision_id, hd.primary_research_object_id,
                   roi.canonical_label, hd.decision_type, hd.rationale,
                   hd.actor, hd.decided_at, hd.supersedes_decision_id,
                   hd.coverage_context_id, hd.assessment_id
            FROM human_decision hd
            JOIN research_object_identity roi ON roi.id = hd.primary_research_object_id
            WHERE hd.project_id = %s
              AND (%s::uuid IS NULL OR hd.primary_research_object_id = %s::uuid)
            ORDER BY hd.decided_at DESC, hd.created_at DESC
            LIMIT %s
        """, (project_id, object_id, object_id, limit)).fetchall()
    return rows


def create_human_decision(project_id, object_id, decision_type, rationale, actor, assessment_id=None):
    if decision_type not in ALLOWED_DECISIONS:
        raise ValueError("Unsupported decision_type")
    if not str(rationale or "").strip() or not str(actor or "").strip():
        raise ValueError("rationale and actor are required")
    with db() as conn:
        target = conn.execute("""
            SELECT roi.id FROM research_object_identity roi
            JOIN research_project p ON p.id = roi.project_id
            WHERE roi.id = %s AND roi.project_id = %s
              AND roi.lifecycle_state = 'ACTIVE' AND p.status = 'ACTIVE'
        """, (object_id, project_id)).fetchone()
        if not target:
            raise ValueError("Active research object not found in project")
        if assessment_id:
            assessment = conn.execute("""
                SELECT id FROM assessment
                WHERE id = %s AND project_id = %s
                  AND target_research_object_id = %s
            """, (assessment_id, project_id, object_id)).fetchone()
            if not assessment:
                raise ValueError("Assessment not found for this research object in project")
        coverage = conn.execute("""
            SELECT id FROM coverage_context WHERE project_id = %s
            ORDER BY observed_at DESC LIMIT 1
        """, (project_id,)).fetchone()
        previous = conn.execute("""
            SELECT id FROM human_decision
            WHERE project_id = %s AND primary_research_object_id = %s
            ORDER BY decided_at DESC, created_at DESC LIMIT 1
        """, (project_id, object_id)).fetchone()
        row = conn.execute("""
            INSERT INTO human_decision (
                project_id, primary_research_object_id, assessment_id, coverage_context_id,
                decision_type, rationale, actor, decided_at, supersedes_decision_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, now(), %s)
            RETURNING id AS decision_id, project_id, primary_research_object_id,
                      decision_type, rationale, actor, decided_at,
                      supersedes_decision_id, coverage_context_id, assessment_id
        """, (
            project_id, object_id, assessment_id,
            coverage["id"] if coverage else None,
            decision_type, rationale.strip(), actor.strip(),
            previous["id"] if previous else None,
        )).fetchone()
    return row


def list_project_assessments(project_id, object_id=None, limit=50):
    with db() as conn:
        rows = conn.execute("""
            SELECT a.id AS assessment_id, a.target_research_object_id,
                   roi.canonical_label, a.coverage_context_id,
                   a.assessment_type, a.model_or_agent, a.model_version,
                   a.explanation_summary, a.assessed_at,
                   a.supersedes_assessment_id,
                   COALESCE(d.dimensions, '[]'::jsonb) AS dimensions
            FROM assessment a
            JOIN research_object_identity roi ON roi.id = a.target_research_object_id
            LEFT JOIN LATERAL (
                SELECT jsonb_agg(jsonb_build_object(
                    'dimension_type', ad.dimension_type,
                    'value_numeric', ad.value_numeric,
                    'value_text', ad.value_text,
                    'explanation', ad.explanation
                ) ORDER BY ad.dimension_type) AS dimensions
                FROM assessment_dimension ad WHERE ad.assessment_id = a.id
            ) d ON TRUE
            WHERE a.project_id = %s
              AND (%s::uuid IS NULL OR a.target_research_object_id = %s::uuid)
            ORDER BY a.assessed_at DESC, a.created_at DESC
            LIMIT %s
        """, (project_id, object_id, object_id, limit)).fetchall()
    return rows


def _list_project_changes(conn, project_id, object_id=None, limit=50):
    rows = conn.execute("""
            SELECT ce.id AS change_event_id,
                   ce.primary_research_object_id,
                   roi.canonical_label,
                   ce.coverage_context_id,
                   ce.previous_assessment_id,
                   ce.current_assessment_id,
                   ce.current_supersedes_assessment_id,
                   ce.change_type, ce.observed_at,
                   ce.previous_state_jsonb,
                   ce.current_state_jsonb,
                   ce.reasoning_delta,
                   COALESCE(cem.evidence_members, '[]'::jsonb) AS evidence_members
            FROM change_event ce
            JOIN research_object_identity roi
              ON roi.id = ce.primary_research_object_id
            LEFT JOIN LATERAL (
                SELECT jsonb_agg(jsonb_build_object(
                    'change_event_evidence_id', x.id,
                    'role', x.role,
                    'evidence_relationship_id', er.id,
                    'semantic_type', er.semantic_type,
                    'claim_id', c.id,
                    'claim_text', c.claim_text,
                    'evidence_fragment_id', ef.id,
                    'access_level', ef.access_level,
                    'work_id', w.id,
                    'work_title', w.title
                ) ORDER BY x.created_at, x.id) AS evidence_members
                FROM change_event_evidence x
                JOIN evidence_relationship er ON er.id = x.evidence_relationship_id
                  AND er.target_research_object_id = x.target_research_object_id
                JOIN claim c ON c.id = er.claim_id
                JOIN evidence_fragment ef ON ef.id = c.evidence_fragment_id
                JOIN work w ON w.id = ef.work_id
                WHERE x.change_event_id = ce.id
            ) cem ON TRUE
            WHERE ce.project_id = %s
              AND (%s::uuid IS NULL OR ce.primary_research_object_id = %s::uuid)
            ORDER BY ce.observed_at DESC, ce.created_at DESC
            LIMIT %s
        """, (project_id, object_id, object_id, limit)).fetchall()
    return rows


def list_project_changes(project_id, object_id=None, limit=50):
    with db() as conn:
        return _list_project_changes(conn, project_id, object_id, limit)


def list_project_opportunities(project_id, limit=50):
    with db() as conn:
        rows = conn.execute("""
            SELECT gc.id AS gap_id, roi.canonical_label, gc.gap_type,
                   gc.statement, gc.current_evolution_state,
                   COALESCE(ev.support_count, 0) AS support_count,
                   COALESCE(ev.challenge_count, 0) AS challenge_count,
                   COALESCE(ev.linked_claim_count, 0) AS linked_claim_count,
                   COALESCE(et.evidence_trace, '[]'::jsonb) AS evidence_trace,
                   cc.id AS coverage_context_id, cc.observed_at AS coverage_observed_at,
                   cc.counter_search_state, cc.limitations AS coverage_limitations,
                   a.id AS assessment_id, a.assessment_type, a.explanation_summary,
                   COALESCE(ad.dimensions, '[]'::jsonb) AS dimensions,
                   hd.decision_type AS latest_human_decision,
                   hd.decided_at AS latest_human_decision_at
            FROM gap_candidate gc
            JOIN research_object_identity roi ON roi.id = gc.id AND roi.project_id = gc.project_id
            LEFT JOIN LATERAL (
                SELECT count(*) FILTER (WHERE er.semantic_type='SUPPORTS') AS support_count,
                       count(*) FILTER (WHERE er.semantic_type='CHALLENGES') AS challenge_count,
                       count(DISTINCT er.claim_id) AS linked_claim_count
                FROM evidence_relationship er WHERE er.target_research_object_id = gc.id
            ) ev ON TRUE
            LEFT JOIN LATERAL (
                SELECT jsonb_agg(jsonb_build_object(
                    'relationship_id', er.id, 'semantic_type', er.semantic_type,
                    'claim_id', c.id, 'claim_text', c.claim_text,
                    'evidence_fragment_id', ef.id, 'access_level', ef.access_level,
                    'work_id', w.id, 'work_title', w.title,
                    'source_record_id', sr.id, 'source_identifier', sr.source_record_identifier,
                    'work_identifiers', COALESCE((SELECT jsonb_agg(jsonb_build_object('type', wi.identifier_type, 'value', wi.identifier_value, 'is_primary', wi.is_primary) ORDER BY wi.is_primary DESC, wi.identifier_type) FROM work_identifier wi WHERE wi.work_id = w.id), '[]'::jsonb)
                ) ORDER BY er.created_at) AS evidence_trace
                FROM evidence_relationship er
                JOIN claim c ON c.id = er.claim_id
                JOIN evidence_fragment ef ON ef.id = c.evidence_fragment_id
                JOIN work w ON w.id = ef.work_id
                LEFT JOIN work_source_record wsr ON wsr.work_id = w.id
                LEFT JOIN source_record sr ON sr.id = wsr.source_record_id
                WHERE er.target_research_object_id = gc.id
            ) et ON TRUE
            LEFT JOIN LATERAL (
                SELECT * FROM coverage_context x WHERE x.project_id = gc.project_id
                ORDER BY x.observed_at DESC LIMIT 1
            ) cc ON TRUE
            LEFT JOIN LATERAL (
                SELECT x.* FROM assessment x
                WHERE x.project_id = gc.project_id
                  AND x.target_research_object_id = gc.id
                  AND x.assessment_type = 'RESEARCH_OPPORTUNITY_INTELLIGENCE_V1'
                ORDER BY x.assessed_at DESC, x.created_at DESC LIMIT 1
            ) a ON TRUE
            LEFT JOIN LATERAL (
                SELECT jsonb_agg(jsonb_build_object(
                    'dimension_type', d.dimension_type,
                    'value_numeric', d.value_numeric,
                    'value_text', d.value_text,
                    'explanation', d.explanation
                ) ORDER BY d.dimension_type) AS dimensions
                FROM assessment_dimension d WHERE d.assessment_id = a.id
            ) ad ON TRUE
            LEFT JOIN LATERAL (
                SELECT x.decision_type, x.decided_at FROM human_decision x
                WHERE x.project_id = gc.project_id
                  AND x.primary_research_object_id = gc.id
                ORDER BY x.decided_at DESC, x.created_at DESC LIMIT 1
            ) hd ON TRUE
            WHERE gc.project_id = %s AND roi.lifecycle_state = 'ACTIVE'
            ORDER BY
              CASE
                WHEN EXISTS (
                  SELECT 1 FROM assessment_dimension d
                  WHERE d.assessment_id = a.id
                    AND d.dimension_type = 'REVIEW_PRIORITY'
                    AND d.value_text = 'HIGH_HUMAN_REVIEW_RECOMMENDED'
                ) THEN 0 ELSE 1
              END,
              gc.created_at DESC
            LIMIT %s
        """, (project_id, limit)).fetchall()
    return rows


def list_project_advice_critic(project_id, limit=50):
    with db() as conn:
        rows = conn.execute("""
            SELECT gc.id AS gap_id, roi.canonical_label, gc.gap_type,
                   gc.statement, gc.current_evolution_state,
                   COALESCE(ev.support_count, 0) AS support_count,
                   COALESCE(ev.challenge_count, 0) AS challenge_count,
                   COALESCE(ev.linked_claim_count, 0) AS linked_claim_count,
                   cc.id AS coverage_context_id, cc.counter_search_state,
                   cc.limitations AS coverage_limitations,
                   a.id AS assessment_id, a.explanation_summary,
                   COALESCE(ad.dimensions, '[]'::jsonb) AS dimensions,
                   COALESCE(ev.evidence_basis, '[]'::jsonb) AS evidence_basis,
                   hd.decision_type AS latest_human_decision
            FROM gap_candidate gc
            JOIN research_object_identity roi ON roi.id=gc.id AND roi.project_id=gc.project_id
            LEFT JOIN LATERAL (
                SELECT count(*) FILTER (WHERE semantic_type='SUPPORTS') support_count,
                       count(*) FILTER (WHERE semantic_type IN ('CHALLENGES','CONTRADICTS')) challenge_count,
                       count(DISTINCT er.claim_id) linked_claim_count,
                       jsonb_agg(jsonb_build_object(
                         'semantic_type',er.semantic_type,'relationship_review_state',er.review_state,
                         'relationship_rationale',er.rationale,'claim_text',c.claim_text,
                         'claim_review_state',c.review_state,'access_level',ef.access_level,
                         'work_title',w.title,'evidence_fragment_id',ef.id
                       ) ORDER BY er.created_at DESC) FILTER (WHERE er.id IS NOT NULL) evidence_basis
                FROM evidence_relationship er
                LEFT JOIN claim c ON c.id=er.claim_id
                LEFT JOIN evidence_fragment ef ON ef.id=c.evidence_fragment_id
                LEFT JOIN work w ON w.id=ef.work_id
                WHERE er.target_research_object_id=gc.id
            ) ev ON TRUE
            LEFT JOIN LATERAL (
                SELECT * FROM coverage_context x WHERE x.project_id=gc.project_id
                ORDER BY x.observed_at DESC LIMIT 1
            ) cc ON TRUE
            LEFT JOIN LATERAL (
                SELECT x.* FROM assessment x
                WHERE x.project_id=gc.project_id
                  AND x.target_research_object_id=gc.id
                  AND x.assessment_type='ADVICE_CRITIC_V1'
                ORDER BY x.assessed_at DESC, x.created_at DESC LIMIT 1
            ) a ON TRUE
            LEFT JOIN LATERAL (
                SELECT jsonb_agg(jsonb_build_object(
                    'dimension_type', d.dimension_type,
                    'value_text', d.value_text,
                    'explanation', d.explanation
                ) ORDER BY d.dimension_type) dimensions
                FROM assessment_dimension d WHERE d.assessment_id=a.id
            ) ad ON TRUE
            LEFT JOIN LATERAL (
                SELECT x.decision_type FROM human_decision x
                WHERE x.project_id=gc.project_id
                  AND x.primary_research_object_id=gc.id
                ORDER BY x.decided_at DESC, x.created_at DESC LIMIT 1
            ) hd ON TRUE
            WHERE gc.project_id=%s AND roi.lifecycle_state='ACTIVE'
              AND a.id IS NOT NULL
            ORDER BY a.assessed_at DESC LIMIT %s
        """, (project_id, limit)).fetchall()
    return rows


def list_project_radar(project_id, limit=20):
    """Read-only Telegram Radar projection from canonical ChangeEvent state."""
    with db() as conn:
        rows = conn.execute("""
            SELECT ce.id AS change_event_id, ce.change_type, ce.observed_at,
                   ce.primary_research_object_id, roi.canonical_label,
                   ce.reasoning_delta, ce.previous_state_jsonb, ce.current_state_jsonb,
                   ce.coverage_context_id, cc.counter_search_state,
                   cc.limitations AS coverage_limitations,
                   p.name AS project_name, rp.name AS profile_name,
                   hd.decision_type AS latest_human_decision
            FROM change_event ce
            JOIN research_object_identity roi ON roi.id = ce.primary_research_object_id
            JOIN research_project p ON p.id = ce.project_id
            JOIN research_profile rp ON rp.id = p.profile_id
            LEFT JOIN coverage_context cc ON cc.id = ce.coverage_context_id
            LEFT JOIN LATERAL (
                SELECT x.decision_type FROM human_decision x
                WHERE x.project_id = ce.project_id
                  AND x.primary_research_object_id = ce.primary_research_object_id
                ORDER BY x.decided_at DESC, x.created_at DESC LIMIT 1
            ) hd ON TRUE
            WHERE ce.project_id = %s
            ORDER BY ce.observed_at DESC, ce.created_at DESC LIMIT %s
        """, (project_id, limit)).fetchall()
    return rows


def list_project_pilot_health(project_id, limit=20):
    """Read-only J14 operational health; never a scientific decision surface."""
    with db() as conn:
        rows = conn.execute("""
            SELECT r.id AS pilot_run_id, r.trigger_type, r.started_at, r.finished_at,
                   r.status, r.machine_actions_jsonb, r.idempotency_key,
                   COALESCE(count(s.id),0) AS stage_attempts,
                   COALESCE(count(s.id) FILTER (WHERE s.status='FAILED'),0) AS failed_stage_attempts, ARRAY_REMOVE(ARRAY_AGG(s.source_key || ':' || s.attempt::text || ':' || s.status ORDER BY s.source_key,s.attempt),NULL) AS stage_history
            FROM continuous_pilot_run r
            LEFT JOIN continuous_pilot_stage_run s ON s.pilot_run_id=r.id
            WHERE r.project_id=%s
            GROUP BY r.id ORDER BY r.started_at DESC LIMIT %s
        """, (project_id, limit)).fetchall()
    return rows

def get_project_quality(project_id, object_id=None):
    with db() as conn:
        obj = conn.execute("""
            SELECT roi.id AS research_object_id, roi.object_type, roi.canonical_label,
                   roi.lifecycle_state,
                   CASE WHEN roi.object_type='GAP_CANDIDATE' THEN gc.current_evolution_state
                        WHEN roi.object_type='INVESTIGATION_DIRECTION' THEN idr.current_state END AS object_state,
                   hd.decision_type AS latest_human_decision, hd.decided_at AS latest_human_decision_at
            FROM research_object_identity roi
            LEFT JOIN gap_candidate gc ON gc.id=roi.id AND gc.project_id=roi.project_id
            LEFT JOIN investigation_direction idr ON idr.id=roi.id AND idr.project_id=roi.project_id
            LEFT JOIN LATERAL (
                SELECT decision_type,decided_at FROM human_decision
                WHERE project_id=roi.project_id AND primary_research_object_id=roi.id
                ORDER BY decided_at DESC,created_at DESC LIMIT 1
            ) hd ON TRUE
            WHERE roi.project_id=%s AND roi.lifecycle_state='ACTIVE'
              AND (%s::uuid IS NULL OR roi.id=%s::uuid)
            ORDER BY roi.created_at DESC LIMIT 1
        """,(project_id,object_id,object_id)).fetchone()
        if not obj:
            return None
        evidence = conn.execute("""
            SELECT er.semantic_type,er.review_state AS relationship_review_state,
                   c.id AS claim_id,c.review_state AS claim_review_state,c.extraction_origin,c.scope_jsonb,
                   ef.id AS evidence_fragment_id,ef.access_level,ef.source_record_id,
                   w.id AS work_id,w.title,w.publication_year,w.publication_date,
                   ls.source_key,sr.source_record_identifier,sr.retrieved_at
            FROM evidence_relationship er
            JOIN claim c ON c.id=er.claim_id
            JOIN evidence_fragment ef ON ef.id=c.evidence_fragment_id
            JOIN work w ON w.id=ef.work_id
            LEFT JOIN source_record sr ON sr.id=ef.source_record_id
            LEFT JOIN literature_source ls ON ls.id=sr.literature_source_id
            WHERE er.target_research_object_id=%s
            ORDER BY er.created_at DESC
        """,(obj['research_object_id'],)).fetchall()
        cov = conn.execute("""
            SELECT cc.observed_at,cc.counter_search_state,cc.limitations,
                   cc.access_summary_jsonb,cc.extraction_summary_jsonb,
                   COALESCE(src.sources,'[]'::jsonb) AS sources
            FROM coverage_context cc
            LEFT JOIN LATERAL (
                SELECT jsonb_agg(jsonb_build_object(
                    'source_key',ls.source_key,'health_state',css.health_state,
                    'access_limitations',css.access_limitations,'degradation_reason',css.degradation_reason
                ) ORDER BY ls.source_key) AS sources
                FROM coverage_source_state css JOIN literature_source ls ON ls.id=css.literature_source_id
                WHERE css.coverage_context_id=cc.id
            ) src ON TRUE
            WHERE cc.project_id=%s ORDER BY cc.observed_at DESC LIMIT 1
        """,(project_id,)).fetchone()
    ev=[dict(x) for x in evidence]
    access=sorted({x['access_level'] for x in ev if x.get('access_level')})
    rel_states=sorted({x['relationship_review_state'] for x in ev if x.get('relationship_review_state')})
    claim_states=sorted({x['claim_review_state'] for x in ev if x.get('claim_review_state')})
    traceable=sum(1 for x in ev if x.get('claim_id') and x.get('evidence_fragment_id') and x.get('work_id'))
    methodological=any(bool((x.get('scope_jsonb') or {}).get(k)) for x in ev for k in ('method','methodology','design'))
    semantics={}
    for x in ev: semantics[x['semantic_type']]=semantics.get(x['semantic_type'],0)+1
    observations=[
      {'dimension':'ACCESS_COMPLETENESS','state':'AVAILABLE' if access else 'NOT_AVAILABLE','value':access or None,'basis':'linked canonical evidence access levels'},
      {'dimension':'PROVENANCE_COMPLETENESS','state':'AVAILABLE' if ev else 'NOT_AVAILABLE','value':{'traceable_relationships':traceable,'linked_relationships':len(ev)} if ev else None,'basis':'Claim -> EvidenceFragment -> Work traceability'},
      {'dimension':'EXTRACTION_REVIEW_STATE','state':'AVAILABLE' if ev else 'NOT_AVAILABLE','value':{'claim_states':claim_states,'relationship_states':rel_states} if ev else None,'basis':'canonical review states'},
      {'dimension':'METHODOLOGICAL_CONTEXT_AVAILABILITY','state':'AVAILABLE' if methodological else 'NOT_AVAILABLE','value':None,'basis':'explicit method/methodology/design keys in canonical claim scope'},
      {'dimension':'CORROBORATION_CONTEXT','state':'AVAILABLE' if ev else 'NOT_AVAILABLE','value':{'SUPPORTS':semantics.get('SUPPORTS',0),'EXTENDS':semantics.get('EXTENDS',0),'REPLICATES':semantics.get('REPLICATES',0)} if ev else None,'basis':'canonical evidence relationships only'},
      {'dimension':'CONTRADICTION_CONTEXT','state':'AVAILABLE' if ev else ('NOT_RUN' if cov and cov['counter_search_state']=='NOT_RUN' else 'NOT_AVAILABLE'),'value':{'CHALLENGES':semantics.get('CHALLENGES',0),'CONTRADICTS':semantics.get('CONTRADICTS',0),'counter_search_state':cov['counter_search_state'] if cov else 'NOT_AVAILABLE'},'basis':'canonical relationships and coverage counter-search state'},
      {'dimension':'RECENCY_CONTEXT','state':'AVAILABLE' if ev else 'NOT_AVAILABLE','value':[{'work_id':str(x['work_id']),'publication_year':x['publication_year'],'publication_date':x['publication_date'],'retrieved_at':x['retrieved_at']} for x in ev] if ev else None,'basis':'publication/retrieval dates; no quality penalty inferred'},
      {'dimension':'SOURCE_COVERAGE_LIMITATIONS','state':'AVAILABLE' if cov else 'NOT_AVAILABLE','value':{'limitations':cov['limitations'],'sources':cov['sources']} if cov else None,'basis':'latest canonical CoverageContext'}
    ]
    suggestions=[]
    if 'ABSTRACT_ONLY' in access: suggestions.append({'action':'INSPECT_FULL_TEXT','because':['ACCESS_COMPLETENESS=ABSTRACT_ONLY']})
    if any(x in ('NEEDS_REVIEW','MACHINE_SUGGESTED') for x in claim_states+rel_states): suggestions.append({'action':'HUMAN_REVIEW_EXTRACTION_RELATIONSHIP','because':['canonical review state requires/indicates review']})
    if cov and cov['counter_search_state']=='NOT_RUN': suggestions.append({'action':'CONSIDER_COUNTER_SEARCH','because':['counter_search_state=NOT_RUN']})
    if ev and not methodological: suggestions.append({'action':'INSPECT_METHODOLOGICAL_CONTEXT','because':['linked evidence exists but METHODOLOGICAL_CONTEXT_AVAILABILITY=NOT_AVAILABLE']})
    if not ev: suggestions.append({'action':'ESTABLISH_EXPLICIT_EVIDENCE_LINKAGE','because':['no canonical EvidenceRelationship is asserted for this research object']})
    return {'object':dict(obj),'observations':observations,'limitations':([cov['limitations']] if cov and cov['limitations'] else []) + ([] if ev else ['No canonical EvidenceRelationship is asserted for this research object; project literature is not projected as object evidence.']),'review_suggestions':suggestions,'evidence_references':ev,'scientific_decision':False}

def list_project_evidence_verification(project_id, object_id=None):
    with db() as conn:
        rows = conn.execute("""
            SELECT w.id AS work_id,w.title,w.publication_year,w.current_access_level,
                   pwr.relevance_state,pwr.human_review_state,
                   ef.id AS evidence_fragment_id,ef.fragment_type,ef.access_level,
                   ef.text_or_reference AS evidence_text,ef.source_record_id,
                   sr.source_record_identifier,ls.source_key,
                   c.id AS claim_id,c.claim_text,c.review_state AS claim_review_state,c.extraction_origin,
                   er.id AS relationship_id,er.semantic_type,er.review_state AS relationship_review_state,
                   ids.identifiers
            FROM project_work_relevance pwr
            JOIN work w ON w.id=pwr.work_id
            LEFT JOIN evidence_fragment ef ON ef.work_id=w.id AND ef.quarantine_state='ACTIVE'
            LEFT JOIN source_record sr ON sr.id=ef.source_record_id
            LEFT JOIN literature_source ls ON ls.id=sr.literature_source_id
            LEFT JOIN claim c ON c.evidence_fragment_id=ef.id AND c.quarantine_state='ACTIVE'
            LEFT JOIN evidence_relationship er ON er.claim_id=c.id
                 AND (%s::uuid IS NULL OR er.target_research_object_id=%s::uuid)
            LEFT JOIN LATERAL (
                SELECT jsonb_object_agg(identifier_type,identifier_value) identifiers
                FROM work_identifier wi WHERE wi.work_id=w.id
            ) ids ON TRUE
            WHERE pwr.project_id=%s
            ORDER BY (er.id IS NOT NULL) DESC,(ef.id IS NOT NULL) DESC,w.publication_year DESC NULLS LAST,w.title
        """,(object_id,object_id,project_id)).fetchall()
    out=[]
    for row in rows:
        x=dict(row); ids=x.pop('identifiers') or {}
        x['identifiers']=ids
        x['doi_url']=f"https://doi.org/{ids['DOI']}" if ids.get('DOI') else None
        x['openalex_url']=f"https://openalex.org/{ids['OPENALEX']}" if ids.get('OPENALEX') else None
        x['object_evidence_status']='EXPLICIT_RELATIONSHIP' if x.get('relationship_id') else 'PROJECT_LITERATURE_ONLY'
        x['full_text_available']=x.get('access_level')=='FULL_TEXT'
        out.append(x)
    return out


def get_project_daily_attention(project_id, hours=24):
    """Read-only attention projection: explicit time window + exact members."""
    hours = max(1, min(int(hours), 168))
    with db() as conn:
        papers = conn.execute("""
            SELECT w.id AS work_id,w.title,pwr.first_seen_at,w.current_access_level
            FROM project_work_relevance pwr JOIN work w ON w.id=pwr.work_id
            WHERE pwr.project_id=%s AND pwr.first_seen_at >= now()-(%s * interval '1 hour')
            ORDER BY pwr.first_seen_at DESC
        """,(project_id,hours)).fetchall()
        claims = conn.execute("""
            SELECT c.id AS claim_id,c.claim_text,c.review_state,c.created_at,
                   ef.id AS evidence_fragment_id,ef.access_level,w.id AS work_id,w.title AS work_title
            FROM project_work_relevance pwr JOIN work w ON w.id=pwr.work_id
            JOIN evidence_fragment ef ON ef.work_id=w.id JOIN claim c ON c.evidence_fragment_id=ef.id
            WHERE pwr.project_id=%s AND c.created_at >= now()-(%s * interval '1 hour')
            ORDER BY c.created_at DESC
        """,(project_id,hours)).fetchall()
        contradictory = conn.execute("""
            SELECT er.id AS relationship_id,er.semantic_type,er.review_state,er.created_at,
                   er.target_research_object_id,c.id AS claim_id,c.claim_text,
                   ef.id AS evidence_fragment_id,w.id AS work_id,w.title AS work_title
            FROM evidence_relationship er JOIN claim c ON c.id=er.claim_id
            JOIN evidence_fragment ef ON ef.id=c.evidence_fragment_id JOIN work w ON w.id=ef.work_id
            JOIN project_work_relevance pwr ON pwr.work_id=w.id AND pwr.project_id=%s
            WHERE er.semantic_type IN ('CHALLENGES','CONTRADICTS')
              AND er.created_at >= now()-(%s * interval '1 hour')
            ORDER BY er.created_at DESC
        """,(project_id,hours)).fetchall()
        assessments = conn.execute("""
            SELECT a.id AS assessment_id,a.target_research_object_id,roi.canonical_label,
                   a.assessed_at,a.explanation_summary
            FROM assessment a JOIN research_object_identity roi ON roi.id=a.target_research_object_id
            WHERE a.project_id=%s AND a.assessment_type='ADVICE_CRITIC_V1'
              AND a.assessed_at >= now()-(%s * interval '1 hour')
            ORDER BY a.assessed_at DESC
        """,(project_id,hours)).fetchall()
        attention = conn.execute("""
            SELECT c.id AS claim_id,c.claim_text,c.review_state,ef.id AS evidence_fragment_id,
                   ef.access_level,w.id AS work_id,w.title AS work_title
            FROM project_work_relevance pwr JOIN work w ON w.id=pwr.work_id
            JOIN evidence_fragment ef ON ef.work_id=w.id JOIN claim c ON c.evidence_fragment_id=ef.id
            WHERE pwr.project_id=%s AND c.review_state IN ('NEEDS_REVIEW','CONTESTED')
            ORDER BY c.created_at DESC
        """,(project_id,)).fetchall()
        coverage=get_project_coverage(project_id)
    return {'window_hours':hours,'new_papers':papers,'new_claims':claims,
            'new_contradictory_evidence':contradictory,'advice_critic_changes':assessments,
            'attention_claims':attention,'coverage':coverage or {},'scientific_decision':False}


def update_research_profile(profile_id, name, summary, configuration, actor):
    if not str(name or '').strip() or not str(actor or '').strip(): raise ValueError('name and actor are required')
    configuration = configuration if isinstance(configuration, dict) else {}
    with db() as conn:
        row=conn.execute("SELECT current_version_id FROM research_profile WHERE id=%s AND status='ACTIVE' FOR UPDATE",(profile_id,)).fetchone()
        if not row: raise ValueError('Active research profile not found')
        old=row['current_version_id']
        v=conn.execute("SELECT COALESCE(max(version_no),0)+1 n FROM research_profile_version WHERE profile_id=%s",(profile_id,)).fetchone()['n']
        new=conn.execute("""INSERT INTO research_profile_version(profile_id,version_no,summary,configuration_jsonb,supersedes_version_id,created_by) VALUES(%s,%s,%s,%s::jsonb,%s,%s) RETURNING id,version_no""",(profile_id,v,summary,__import__('json').dumps(configuration),old,actor)).fetchone()
        conn.execute("UPDATE research_profile SET name=%s,current_version_id=%s WHERE id=%s",(name.strip(),new['id'],profile_id)); conn.commit()
    return {'profile_id':profile_id,'profile_version':new['version_no'],'scientific_decision':False}


def update_research_project(project_id, name, research_intent, provisional_rq_text, configuration, actor):
    if not str(name or '').strip() or not str(actor or '').strip(): raise ValueError('name and actor are required')
    configuration = configuration if isinstance(configuration, dict) else {}
    with db() as conn:
        row=conn.execute("SELECT current_version_id FROM research_project WHERE id=%s AND status='ACTIVE' FOR UPDATE",(project_id,)).fetchone()
        if not row: raise ValueError('Active research project not found')
        old=row['current_version_id']; v=conn.execute("SELECT COALESCE(max(version_no),0)+1 n FROM research_project_version WHERE project_id=%s",(project_id,)).fetchone()['n']
        new=conn.execute("""INSERT INTO research_project_version(project_id,version_no,research_intent,provisional_rq_text,project_configuration_jsonb,supersedes_version_id,created_by) VALUES(%s,%s,%s,%s,%s::jsonb,%s,%s) RETURNING id,version_no""",(project_id,v,research_intent,provisional_rq_text,__import__('json').dumps(configuration),old,actor)).fetchone()
        conn.execute("UPDATE research_project SET name=%s,current_version_id=%s WHERE id=%s",(name.strip(),new['id'],project_id)); conn.commit()
    return {'project_id':project_id,'project_version':new['version_no'],'scientific_decision':False}


def update_profile_project_configuration(profile_id, project_id, profile, project, actor, reason):
    import json
    if not all(str(x or '').strip() for x in (profile_id,project_id,actor,reason)): raise ValueError('profile_id, project_id, actor, and reason are required')
    if not str(profile.get('name') or '').strip() or not str(project.get('name') or '').strip() or not str(project.get('research_intent') or '').strip(): raise ValueError('profile name, project name, and research intent are required')
    pc=profile.get('configuration') if isinstance(profile.get('configuration'),dict) else {}; qc=project.get('configuration') if isinstance(project.get('configuration'),dict) else {}
    audit_actor=f"{actor.strip()} | reason: {reason.strip()}"
    with db() as conn:
        pr=conn.execute("SELECT current_version_id FROM research_profile WHERE id=%s AND status='ACTIVE' FOR UPDATE",(profile_id,)).fetchone(); pj=conn.execute("SELECT current_version_id FROM research_project WHERE id=%s AND research_profile_id=%s AND status='ACTIVE' FOR UPDATE",(project_id,profile_id)).fetchone()
        if not pr or not pj: raise ValueError('Active linked profile/project not found')
        pv=conn.execute("SELECT COALESCE(max(version_no),0)+1 n FROM research_profile_version WHERE profile_id=%s",(profile_id,)).fetchone()['n']; qv=conn.execute("SELECT COALESCE(max(version_no),0)+1 n FROM research_project_version WHERE project_id=%s",(project_id,)).fetchone()['n']
        pn=conn.execute("INSERT INTO research_profile_version(profile_id,version_no,summary,configuration_jsonb,supersedes_version_id,created_by) VALUES(%s,%s,%s,%s::jsonb,%s,%s) RETURNING id",(profile_id,pv,profile.get('summary'),json.dumps(pc),pr['current_version_id'],audit_actor)).fetchone()['id']
        qn=conn.execute("INSERT INTO research_project_version(project_id,version_no,research_intent,provisional_rq_text,project_configuration_jsonb,supersedes_version_id,created_by) VALUES(%s,%s,%s,%s,%s::jsonb,%s,%s) RETURNING id",(project_id,qv,project.get('research_intent'),project.get('provisional_rq_text'),json.dumps(qc),pj['current_version_id'],audit_actor)).fetchone()['id']
        conn.execute("UPDATE research_profile SET name=%s,current_version_id=%s WHERE id=%s",(profile['name'].strip(),pn,profile_id)); conn.execute("UPDATE research_project SET name=%s,current_version_id=%s WHERE id=%s",(project['name'].strip(),qn,project_id)); conn.commit()
    return {'profile_id':profile_id,'profile_version':pv,'project_id':project_id,'project_version':qv,'scientific_decision':False,'atomic':True}



def get_project_seed_universe(project_id):
    """Read-only seed-to-universe projection. Project Works are seeds, never the asserted universe."""
    papers = list_project_papers(project_id, limit=100)
    seeds=[]
    for p in papers:
        ids=p.get('identifiers') or {}
        seeds.append({'work_id':p.get('work_id'),'title':p.get('title'),'publication_year':p.get('publication_year'),
          'venue_name':p.get('venue_name'),'access_level':p.get('current_access_level'),'source_key':p.get('source_key'),
          'identifiers':ids,'seed_role':'PROJECT_CORPUS_SEED'})
    exploration=get_project_exploration(project_id)
    sessions=exploration.get('sessions') or []
    observations=[]
    query_families=[]
    for session in sessions:
        observations.extend(session.get('observations') or [])
        query_families.extend(session.get('query_families') or [])
    source_keys=sorted({o.get('source_key') for o in observations if o.get('source_key')})
    # These are transparent lexical candidates derived only from seed titles; they are not HUMAN-approved scope.
    stop={'the','of','a','an','and','in','on','to','toward','towards','for','with','use','meets'}
    terms={}
    import re
    for seed in seeds:
        for token in re.findall(r"[A-Za-z][A-Za-z-]{2,}", seed.get('title') or ''):
            key=token.lower()
            if key in stop: continue
            terms.setdefault(key,{'term':token,'seed_work_ids':[]})
            if seed['work_id'] not in terms[key]['seed_work_ids']: terms[key]['seed_work_ids'].append(seed['work_id'])
    terminology=sorted(terms.values(),key=lambda x:(-len(x['seed_work_ids']),x['term'].lower()))
    for x in terminology: x['seed_count']=len(x['seed_work_ids']); x['candidate_state']='MACHINE_DERIVED_NOT_HUMAN_APPROVED'
    # Phrase candidates are contiguous title phrases only: inspectable observations, not semantic truth.
    phrase_patterns=[
      ('artificial intelligence','Artificial Intelligence'),('explainable artificial intelligence','Explainable Artificial Intelligence'),
      ('public administration','Public Administration'),('public governance','Public Governance'),
      ('algorithmic decision-making','Algorithmic Decision-Making'),('systematic literature review','Systematic Literature Review'),
      ('research agenda','Research Agenda'),('responsible ai','Responsible AI')
    ]
    phrase_candidates=[]
    for phrase,label in phrase_patterns:
        members=[seed['work_id'] for seed in seeds if phrase in (seed.get('title') or '').lower()]
        if members: phrase_candidates.append({'phrase':label,'seed_work_ids':members,'seed_count':len(members),
          'candidate_state':'MACHINE_DERIVED_NOT_HUMAN_APPROVED','derivation':'EXACT_PHRASE_IN_SEED_TITLE'})
    query_family_candidates=[{'label':x['phrase'],'seed_work_ids':x['seed_work_ids'],
      'candidate_query':'\"'+x['phrase']+'\"','candidate_state':'OPTION_NOT_HUMAN_APPROVED',
      'why_shown':'Exact phrase observed in one or more seed titles; offered as a discovery option, not as the correct research scope.'}
      for x in phrase_candidates]
    return {
      'stage':'RESEARCH_EXPLORER','projection':'SEED_TO_UNIVERSE','project_id':project_id,
      'seed_state':'AVAILABLE' if seeds else 'NOT_AVAILABLE','seed_count':len(seeds),'seeds':seeds,
      'observed_universe_state':'OBSERVED' if observations else 'NOT_RUN',
      'observed_record_count':len(observations) if observations else 0,
      'source_keys':source_keys,'query_family_count':len(query_families),
      'terminology_candidates':terminology,
      'terminology_method':'LEXICAL_FROM_SEED_TITLES_V1',
      'terminology_limitation':'Title tokens and exact seed-title phrases only; not semantic validation, scope selection, relevance judgment, or HUMAN approval.',
      'phrase_candidates':phrase_candidates,'query_family_candidates':query_family_candidates,
      'query_family_state':'OPTIONS_NOT_HUMAN_APPROVED' if query_family_candidates else 'NOT_AVAILABLE',
      'explanation':('Project Corpus Works are available as exploration seeds. They do not define the Research Universe. '
        'Canonical seed-triggered discovery has not been run, so the observed Research Universe remains NOT_RUN.' if seeds and not observations else
        'Seed Works and canonical discovery observations are available for HUMAN inspection.' if observations else
        'No Project Corpus seed Works are available; no Research Universe is asserted.'),
      'next_observation_needed': (['derive inspectable terminology/query-family candidates from seeds','run provenance-preserving multi-source discovery','show source/query coverage and blind spots','run counter-search'] if seeds and not observations else []),
      'scientific_decision':False,
      'constraints':{'seeds_are_universe':False,'discovery_is_evidence':False,'gap_proven':False,'novelty_proven':False}
    }

def get_project_exploration(project_id):
    """Read-only Research Explorer projection. Empty canonical state remains explicit."""
    with db() as conn:
        sessions = conn.execute("""
            SELECT s.id AS exploration_session_id, s.research_interest, s.status,
                   s.started_at, s.closed_at, s.profile_id, s.profile_version_id,
                   s.project_version_id,
                   COALESCE(nodes.nodes, '[]'::jsonb) AS scope_nodes,
                   COALESCE(families.families, '[]'::jsonb) AS query_families,
                   COALESCE(obs.observations, '[]'::jsonb) AS observations
            FROM research_exploration_session s
            LEFT JOIN LATERAL (
              SELECT jsonb_agg(jsonb_build_object('id',n.id,'scope_level',n.scope_level,
                'label',n.label,'scope_description',n.scope_description,
                'parent_scope_node_id',n.parent_scope_node_id) ORDER BY n.scope_level DESC,n.label) nodes
              FROM research_scope_node n WHERE n.exploration_session_id=s.id
            ) nodes ON TRUE
            LEFT JOIN LATERAL (
              SELECT jsonb_agg(jsonb_build_object('id',f.id,'family_key',f.family_key,
                'label',f.label,'rationale',f.rationale,'scope_node_id',f.scope_node_id,
                'queries',COALESCE(q.queries,'[]'::jsonb)) ORDER BY f.family_key) families
              FROM discovery_query_family f
              LEFT JOIN LATERAL (
                SELECT jsonb_agg(jsonb_build_object('id',dq.id,'query_text',dq.query_text,
                  'query_parameters',dq.query_parameters_jsonb) ORDER BY dq.id) queries
                FROM discovery_query dq WHERE dq.query_family_id=f.id AND dq.exploration_session_id=s.id
              ) q ON TRUE WHERE f.exploration_session_id=s.id
            ) families ON TRUE
            LEFT JOIN LATERAL (
              SELECT jsonb_agg(jsonb_build_object('id',o.id,'scope_node_id',o.scope_node_id,
                'discovery_query_id',o.discovery_query_id,'source_key',ls.source_key,
                'source_record_id',o.source_record_id,'observed_at',o.observed_at,
                'observation_state',o.observation_state,'position_or_rank',o.position_or_rank,
                'pilot_run_id',o.pilot_run_id,'pilot_stage_run_id',o.pilot_stage_run_id,
                'metadata',o.observation_metadata_jsonb) ORDER BY o.observed_at DESC) observations
              FROM discovery_observation o JOIN literature_source ls ON ls.id=o.literature_source_id
              WHERE o.exploration_session_id=s.id AND o.project_id=s.project_id
            ) obs ON TRUE
            WHERE s.project_id=%s ORDER BY s.started_at DESC
        """, (project_id,)).fetchall()
    return {
      'stage':'RESEARCH_EXPLORER',
      'project_id':project_id,
      'state':'AVAILABLE' if sessions else 'NOT_RECORDED',
      'explanation': ('Canonical Research Explorer sessions are available for HUMAN inspection.' if sessions else
        'No canonical Research Explorer session has been recorded for this project. This does not mean exploration did not occur or that coverage is complete.'),
      'sessions':sessions,
      'scientific_decision':False
    }
