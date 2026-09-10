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
