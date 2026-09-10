import argparse
import hashlib
import json
import sys

from psycopg.types.json import Jsonb

sys.path.insert(0, "/opt/gfprojclaw-research-intelligence/prototype/api")
from db import db

EXTRACTION_VERSION = "openalex-abstract-v1"
CLAIM_ORIGIN = "machine_assisted_bootstrap_v1"
def reconstruct_abstract(index):
    words = []
    for word, positions in (index or {}).items():
        for pos in positions:
            words.append((pos, word))
    return " ".join(word for _, word in sorted(words))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--openalex-id", required=True)
    parser.add_argument("--claim-text", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    with db() as conn:
        row = conn.execute("""
            SELECT w.id AS work_id, sr.id AS source_record_id,
                   sr.raw_metadata_jsonb
            FROM work_identifier wi
            JOIN work w ON w.id = wi.work_id
            JOIN work_source_record wsr ON wsr.work_id = w.id
            JOIN source_record sr ON sr.id = wsr.source_record_id
            WHERE wi.identifier_type = 'OPENALEX'
              AND wi.identifier_value = %s
            ORDER BY sr.retrieved_at DESC
            LIMIT 1
        """, (args.openalex_id,)).fetchone()
        if not row:
            raise SystemExit("OpenAlex work/source record not found")

        abstract = reconstruct_abstract(
            row["raw_metadata_jsonb"].get("abstract_inverted_index")
        )
        if not abstract:
            raise SystemExit("No abstract available")
        content_hash = hashlib.sha256(abstract.encode()).hexdigest()
        fragment = conn.execute("""
            SELECT id FROM evidence_fragment
            WHERE work_id = %s AND source_record_id = %s
              AND fragment_type = 'ABSTRACT_SEGMENT'
              AND content_hash = %s
            LIMIT 1
        """, (row["work_id"], row["source_record_id"], content_hash)).fetchone()

        result = {
            "work_id": str(row["work_id"]),
            "source_record_id": str(row["source_record_id"]),
            "content_hash": content_hash,
            "abstract_chars": len(abstract),
        }
        if not args.apply:
            result["mode"] = "dry-run"
            print(json.dumps(result, indent=2))
            return
        if fragment:
            fragment_id = fragment["id"]
        else:
            fragment_id = conn.execute("""
                INSERT INTO evidence_fragment (
                    work_id, source_record_id, access_level, fragment_type,
                    locator_jsonb, text_or_reference, content_hash,
                    extraction_version
                ) VALUES (%s, %s, 'ABSTRACT_ONLY', 'ABSTRACT_SEGMENT',
                          %s, %s, %s, %s)
                RETURNING id
            """, (
                row["work_id"], row["source_record_id"],
                Jsonb({"source": "openalex", "field": "abstract_inverted_index"}),
                abstract, content_hash, EXTRACTION_VERSION,
            )).fetchone()["id"]
        claim = conn.execute("""
            SELECT id FROM claim
            WHERE evidence_fragment_id = %s
              AND claim_text = %s
              AND extraction_origin = %s
            LIMIT 1
        """, (fragment_id, args.claim_text, CLAIM_ORIGIN)).fetchone()
        if claim:
            claim_id = claim["id"]
        else:
            claim_id = conn.execute("""
                INSERT INTO claim (
                    evidence_fragment_id, claim_text, claim_type,
                    scope_jsonb, extraction_origin, review_state
                ) VALUES (%s, %s, 'FINDING', %s, %s, 'NEEDS_REVIEW')
                RETURNING id
            """, (
                fragment_id, args.claim_text,
                Jsonb({"basis": "abstract", "human_validation_required": True}),
                CLAIM_ORIGIN,
            )).fetchone()["id"]
        result.update({
            "mode": "apply",
            "evidence_fragment_id": str(fragment_id),
            "claim_id": str(claim_id),
            "review_state": "NEEDS_REVIEW",
        })
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
