import argparse
import uuid

from psycopg.types.json import Jsonb

import sys
sys.path.insert(0, "/opt/gfprojclaw-research-intelligence/prototype/api")
from db import db

ORIGIN = "machine_assisted_gap_bootstrap_v1"
NAMESPACE = uuid.UUID("5c92cb4b-48e2-4ab5-9a65-74c9c9ec82e7")
LABEL = "Candidate: empirical and explanatory specificity in AI public governance"
STATEMENT = (
    "Current synthesized evidence suggests that empirical and explanatory research "
    "focused on specific forms of AI in public governance may remain underdeveloped."
)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-id", required=True)
    ap.add_argument("--claim-id", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    gap_id = uuid.uuid5(NAMESPACE, f"gap:{args.project_id}:{LABEL}")
    rel_id = uuid.uuid5(NAMESPACE, f"rel:{args.claim_id}:{gap_id}:SUPPORTS")

    with db() as conn:
        claim = conn.execute("""
            SELECT c.id, ef.work_id, p.profile_id
            FROM claim c
            JOIN evidence_fragment ef ON ef.id = c.evidence_fragment_id
            JOIN project_work_relevance pwr ON pwr.work_id = ef.work_id
            JOIN research_project p ON p.id = pwr.project_id
            WHERE c.id = %s AND p.id = %s AND p.status = 'ACTIVE'
        """, (args.claim_id, args.project_id)).fetchone()
        if not claim:
            raise SystemExit("Claim is not linked to the active target project")

        payload = {
            "gap_id": str(gap_id),
            "relationship_id": str(rel_id),
            "label": LABEL,
            "statement": STATEMENT,
            "gap_type": "SYNTHESIS_GAP",
            "relationship": "SUPPORTS",
            "relationship_review_state": "MACHINE_SUGGESTED",
        }
        if not args.apply:
            print(payload)
            conn.rollback()
            return

        scope = {
            "basis_claim_id": args.claim_id,
            "basis_work_id": str(claim["work_id"]),
            "evidence_scope": "single_abstract_claim",
            "human_validation_required": True,
        }
        conn.execute("""
            INSERT INTO research_object_identity
                (id, object_type, profile_id, project_id, canonical_label,
                 lifecycle_state, origin, created_by)
            VALUES (%s, 'GAP_CANDIDATE', %s, %s, %s, 'ACTIVE', %s, 'gfprojclaw-machine-assist')
            ON CONFLICT (id) DO NOTHING
        """, (gap_id, claim["profile_id"], args.project_id, LABEL, ORIGIN))

        conn.execute("""
            INSERT INTO gap_candidate
                (id, project_id, gap_type, statement, scope_jsonb, current_evolution_state)
            VALUES (%s, %s, 'SYNTHESIS_GAP', %s, %s, 'CANDIDATE')
            ON CONFLICT (id) DO NOTHING
        """, (gap_id, args.project_id, STATEMENT, Jsonb(scope)))
        conn.execute("""
            INSERT INTO evidence_relationship
                (id, claim_id, target_research_object_id, semantic_type,
                 rationale, origin, review_state)
            VALUES (%s, %s, %s, 'SUPPORTS', %s, %s, 'MACHINE_SUGGESTED')
            ON CONFLICT (id) DO NOTHING
        """, (
            rel_id, args.claim_id, gap_id,
            "Single abstract-derived claim is consistent with this tentative synthesis gap; HUMAN review required.",
            ORIGIN,
        ))
        conn.commit()
        print(payload)


if __name__ == "__main__":
    main()
