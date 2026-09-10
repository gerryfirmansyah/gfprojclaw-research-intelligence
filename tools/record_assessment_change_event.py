#!/usr/bin/env python3
import argparse
import sys
import uuid

from psycopg.types.json import Jsonb

sys.path.insert(0, "/opt/gfprojclaw-research-intelligence/prototype/api")
from db import db

EVENT_NAMESPACE = uuid.UUID("b01b5c5a-7c53-4f7d-9b50-0f9154c539e1")
CHANGE_TYPE = "ASSESSMENT_CHANGED"


def load_assessment(conn, project_id, assessment_id):
    return conn.execute("""
        SELECT a.id AS assessment_id, a.project_id,
               a.target_research_object_id AS object_id,
               a.coverage_context_id, a.assessment_type,
               a.model_or_agent, a.model_version,
               a.explanation_summary, a.assessed_at,
               a.supersedes_assessment_id,
               gc.current_evolution_state
        FROM assessment a
        JOIN gap_candidate gc ON gc.id = a.target_research_object_id
        WHERE a.project_id = %s AND a.id = %s
    """, (project_id, assessment_id)).fetchone()


def build_state(row):
    return {
        "assessment_id": str(row["assessment_id"]),
        "assessment_type": row["assessment_type"],
        "model_or_agent": row["model_or_agent"],
        "model_version": row["model_version"],
        "gap_evolution_state": row["current_evolution_state"],
    }


def event_id_for(row):
    return uuid.uuid5(
        EVENT_NAMESPACE,
        f"assessment:{row['project_id']}:{row['assessment_id']}:{CHANGE_TYPE}",
    )


def load_previous_state(conn, row):
    if not row["supersedes_assessment_id"]:
        return None
    previous = conn.execute("""
        SELECT id AS assessment_id, assessment_type,
               model_or_agent, model_version
        FROM assessment WHERE id = %s AND project_id = %s
    """, (row["supersedes_assessment_id"], row["project_id"])).fetchone()
    return build_state({**row, **previous}) if previous else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--assessment-id", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    with db() as conn:
        row = load_assessment(conn, args.project_id, args.assessment_id)
        if not row:
            raise SystemExit("Assessment for GapCandidate not found in project")

        event_id = event_id_for(row)
        previous_state = load_previous_state(conn, row)
        current_state = build_state(row)
        reasoning = (
            "Initial machine assessment context recorded; no scientific state transition implied."
            if previous_state is None else
            "Machine assessment context changed; no scientific state transition implied."
        )
        preview = {
            "event_id": str(event_id),
            "change_type": CHANGE_TYPE,
            "object_id": str(row["object_id"]),
            "coverage_context_id": str(row["coverage_context_id"]) if row["coverage_context_id"] else None,
            "previous_state": previous_state,
            "current_state": current_state,
            "reasoning_delta": reasoning,
        }
        if not args.apply:
            print(preview)
            conn.rollback()
            return

        existing = conn.execute(
            "SELECT id FROM change_event WHERE id = %s", (event_id,)
        ).fetchone()
        created = False
        if not existing:
            conn.execute("""
                INSERT INTO change_event (
                    id, project_id, primary_research_object_id,
                    coverage_context_id, change_type, observed_at,
                    previous_state_jsonb, current_state_jsonb, reasoning_delta
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                event_id, row["project_id"], row["object_id"],
                row["coverage_context_id"], CHANGE_TYPE, row["assessed_at"],
                Jsonb(previous_state) if previous_state is not None else None,
                Jsonb(current_state), reasoning,
            ))
            created = True

        print({**preview, "created": created})


if __name__ == "__main__":
    main()
