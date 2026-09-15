#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
import sys

sys.path.insert(0, "/opt/gfprojclaw-research-intelligence/prototype/api")
from db import db

ASSESSMENT_TYPE = "ADVICE_CRITIC_V1"
MODEL_OR_AGENT = "gfprojclaw-advice-critic"
MODEL_VERSION = "v1"


def load_basis(conn, project_id, gap_id):
    return conn.execute("""
        SELECT gc.id AS gap_id, gc.project_id, roi.canonical_label,
               cc.id AS coverage_context_id, cc.counter_search_state, cc.limitations,
               count(er.id) FILTER (WHERE er.semantic_type = 'SUPPORTS') AS support_count,
               count(er.id) FILTER (WHERE er.semantic_type IN ('CHALLENGES','CONTRADICTS')) AS challenge_count,
               count(DISTINCT c.id) AS linked_claim_count
        FROM gap_candidate gc
        JOIN research_object_identity roi ON roi.id = gc.id AND roi.project_id = gc.project_id
        LEFT JOIN evidence_relationship er ON er.target_research_object_id = gc.id
        LEFT JOIN claim c ON c.id = er.claim_id
        LEFT JOIN LATERAL (
            SELECT * FROM coverage_context x WHERE x.project_id = gc.project_id
            ORDER BY x.observed_at DESC LIMIT 1
        ) cc ON TRUE
        WHERE gc.project_id = %s AND gc.id = %s AND roi.lifecycle_state = 'ACTIVE'
        GROUP BY gc.id, roi.canonical_label, cc.id, cc.counter_search_state, cc.limitations
    """, (project_id, gap_id)).fetchone()


def dimensions_for(basis):
    support = int(basis["support_count"] or 0)
    challenge = int(basis["challenge_count"] or 0)
    counter = basis["counter_search_state"] or "NOT_RECORDED"
    if support and challenge:
        balance = "MIXED_SUPPORT_AND_CHALLENGE"
    elif support:
        balance = "SUPPORT_ONLY"
    elif challenge:
        balance = "CHALLENGE_ONLY"
    else:
        balance = "NO_LINKED_EVIDENCE"
    action = "RUN_COUNTER_SEARCH_AND_HUMAN_REVIEW" if counter in ("NOT_RUN", "NOT_RECORDED") else "HUMAN_REVIEW_EVIDENCE_BALANCE"
    return {
        "COUNTER_EVIDENCE_RISK": (balance, f"Persisted relationships: {support} supporting, {challenge} challenging/contradicting; this is observed evidence balance, not a truth probability."),
        "EVIDENCE_COVERAGE_CONTEXT": (counter, basis["limitations"] or "No explicit coverage limitation text is recorded; counter-search state is contextual, not proof of absence."),
        "REVIEW_PRIORITY": (action, "Advice & Critic recommendation only; falsification work should precede stronger claims and HUMAN scientific judgment remains authoritative."),
    }

def find_or_create(conn, basis):
    existing = conn.execute("""
        SELECT id FROM assessment
        WHERE project_id = %s AND target_research_object_id = %s
          AND coverage_context_id IS NOT DISTINCT FROM %s
          AND assessment_type = %s AND model_or_agent = %s AND model_version = %s
        ORDER BY assessed_at DESC LIMIT 1
    """, (basis["project_id"], basis["gap_id"], basis["coverage_context_id"],
          ASSESSMENT_TYPE, MODEL_OR_AGENT, MODEL_VERSION)).fetchone()
    if existing:
        return existing["id"], False
    row = conn.execute("""
        INSERT INTO assessment (
            project_id, target_research_object_id, coverage_context_id,
            assessment_type, model_or_agent, model_version,
            explanation_summary, assessed_at
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (basis["project_id"], basis["gap_id"], basis["coverage_context_id"],
          ASSESSMENT_TYPE, MODEL_OR_AGENT, MODEL_VERSION,
          "Advice & Critic surfaces weaknesses and falsification work; it is not a scientific verdict and HUMAN authority remains explicit.",
          datetime.now(timezone.utc))).fetchone()
    return row["id"], True


def ensure_dimensions(conn, assessment_id, dimensions):
    for dimension_type, (value_text, explanation) in dimensions.items():
        conn.execute("""INSERT INTO assessment_dimension
            (assessment_id, dimension_type, value_text, explanation)
            VALUES (%s,%s,%s,%s) ON CONFLICT (assessment_id, dimension_type) DO NOTHING
        """, (assessment_id, dimension_type, value_text, explanation))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--gap-id", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    with db() as conn:
        basis = load_basis(conn, args.project_id, args.gap_id)
        if not basis:
            raise SystemExit("Active GapCandidate not found in project")
        dimensions = dimensions_for(basis)
        preview = {
            "gap_id": str(basis["gap_id"]),
            "coverage_context_id": str(basis["coverage_context_id"]) if basis["coverage_context_id"] else None,
            "assessment_type": ASSESSMENT_TYPE,
            "support_count": int(basis["support_count"] or 0),
            "challenge_count": int(basis["challenge_count"] or 0),
            "linked_claim_count": int(basis["linked_claim_count"] or 0),
            "dimensions": dimensions,
        }
        if not args.apply:
            print(preview)
            conn.rollback()
            return
        assessment_id, created = find_or_create(conn, basis)
        ensure_dimensions(conn, assessment_id, dimensions)
        print({**preview, "assessment_id": str(assessment_id), "created": created})


if __name__ == "__main__":
    main()
