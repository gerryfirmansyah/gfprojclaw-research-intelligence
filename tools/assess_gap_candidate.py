#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone

import sys
sys.path.insert(0, "/opt/gfprojclaw-research-intelligence/prototype/api")
from db import db

ASSESSMENT_TYPE = "GAP_CANDIDATE_EVIDENCE_CONTEXT_V1"
MODEL_OR_AGENT = "gfprojclaw-bootstrap-assessor"
MODEL_VERSION = "v1"

DIMENSIONS = {
    "GAP_EVIDENCE_STRENGTH": (
        "PRELIMINARY_SINGLE_CLAIM",
        "Only one persisted abstract-derived claim currently supports this candidate gap."
    ),
    "COUNTER_EVIDENCE_RISK": (
        "UNKNOWN_COUNTER_SEARCH_NOT_RUN",
        "No counter-search has been run in the linked CoverageContext."
    ),
}
DIMENSIONS.update({
    "EVIDENCE_COVERAGE_CONTEXT": (
        "LIMITED_SINGLE_ABSTRACT_SLICE",
        "Coverage is limited to the current persisted bootstrap slice and abstract-only evidence."
    ),
    "REVIEW_PRIORITY": (
        "HIGH_HUMAN_REVIEW_RECOMMENDED",
        "The gap and its supporting relationship remain machine-suggested and require HUMAN review."
    ),
})


def load_basis(conn, project_id, gap_id):
    return conn.execute("""
        SELECT gc.id AS gap_id, gc.project_id, gc.current_evolution_state,
               gc.scope_jsonb, roi.canonical_label,
               cc.id AS coverage_context_id, cc.counter_search_state,
               cc.access_summary_jsonb
        FROM gap_candidate gc
        JOIN research_object_identity roi ON roi.id = gc.id AND roi.project_id = gc.project_id
        LEFT JOIN LATERAL (
            SELECT * FROM coverage_context c
            WHERE c.project_id = gc.project_id ORDER BY c.observed_at DESC LIMIT 1
        ) cc ON TRUE
        WHERE gc.project_id = %s AND gc.id = %s AND roi.lifecycle_state = 'ACTIVE'
    """, (project_id, gap_id)).fetchone()

def upsert_assessment(conn, basis):
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
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (
        basis["project_id"], basis["gap_id"], basis["coverage_context_id"],
        ASSESSMENT_TYPE, MODEL_OR_AGENT, MODEL_VERSION,
        "Machine assessment of current evidence context only; not a scientific verdict.",
        datetime.now(timezone.utc),
    )).fetchone()
    return row["id"], True

def ensure_dimensions(conn, assessment_id):
    for dimension_type, (value_text, explanation) in DIMENSIONS.items():
        conn.execute("""
            INSERT INTO assessment_dimension (
                assessment_id, dimension_type, value_text, explanation
            ) VALUES (%s,%s,%s,%s)
            ON CONFLICT (assessment_id, dimension_type) DO NOTHING
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
        preview = {
            "gap_id": str(basis["gap_id"]),
            "coverage_context_id": str(basis["coverage_context_id"]) if basis["coverage_context_id"] else None,
            "assessment_type": ASSESSMENT_TYPE,
            "dimensions": DIMENSIONS,
        }
        if not args.apply:
            print(preview)
            conn.rollback()
            return
        assessment_id, created = upsert_assessment(conn, basis)
        ensure_dimensions(conn, assessment_id)
        print({
            **preview,
            "assessment_id": str(assessment_id),
            "created": created,
        })


if __name__ == "__main__":
    main()
