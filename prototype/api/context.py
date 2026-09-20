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


def list_project_changes(project_id, object_id=None, limit=50):
    with db() as conn:
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
