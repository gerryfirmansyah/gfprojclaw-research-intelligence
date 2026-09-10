from db import db


def list_context():
    with db() as conn:
        rows = conn.execute("""
            SELECT rp.id AS profile_id, rp.name AS profile_name,
                   rpv.version_no AS profile_version,
                   p.id AS project_id, p.name AS project_name,
                   pv.version_no AS project_version,
                   pv.research_intent, pv.provisional_rq_text
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


def create_human_decision(project_id, object_id, decision_type, rationale, actor):
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
                project_id, primary_research_object_id, coverage_context_id,
                decision_type, rationale, actor, decided_at, supersedes_decision_id
            ) VALUES (%s, %s, %s, %s, %s, %s, now(), %s)
            RETURNING id AS decision_id, project_id, primary_research_object_id,
                      decision_type, rationale, actor, decided_at,
                      supersedes_decision_id, coverage_context_id
        """, (
            project_id, object_id,
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


def list_project_changes(project_id, object_id=None, limit=50):
    with db() as conn:
        rows = conn.execute("""
            SELECT ce.id AS change_event_id,
                   ce.primary_research_object_id,
                   roi.canonical_label,
                   ce.coverage_context_id,
                   ce.change_type, ce.observed_at,
                   ce.previous_state_jsonb,
                   ce.current_state_jsonb,
                   ce.reasoning_delta
            FROM change_event ce
            JOIN research_object_identity roi
              ON roi.id = ce.primary_research_object_id
            WHERE ce.project_id = %s
              AND (%s::uuid IS NULL OR ce.primary_research_object_id = %s::uuid)
            ORDER BY ce.observed_at DESC, ce.created_at DESC
            LIMIT %s
        """, (project_id, object_id, object_id, limit)).fetchall()
    return rows
