from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.types.json import Jsonb

ENV_FILE = "/opt/gfprojclaw/config/runtime.env"
SOURCE_KEY = "openalex"


def dsn() -> str:
    load_dotenv(ENV_FILE)
    return " ".join(f"{k}={os.environ[v]}" for k, v in [
        ("host", "GFPROJ_DB_HOST"), ("port", "GFPROJ_DB_PORT"),
        ("dbname", "GFPROJ_DB_NAME"), ("user", "GFPROJ_DB_USER"),
        ("password", "GFPROJ_DB_PASSWORD"),
    ])

def normalize_openalex(value: str) -> str:
    return value.rsplit("/", 1)[-1].strip()


def normalize_doi(value: str) -> str:
    value = value.strip().lower()
    for prefix in ("https:" + "//doi.org/", "http:" + "//doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix):]
    return value


def load_record(path: Path, openalex_id: str) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    target = normalize_openalex(openalex_id)
    for row in payload.get("results", []):
        if normalize_openalex(row.get("id", "")) == target:
            return row
    raise ValueError(f"OpenAlex record not found: {target}")


def record_hash(record: dict) -> str:
    canonical = json.dumps(record, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def access_state(record: dict) -> str:
    return "ABSTRACT_ONLY" if record.get("abstract_inverted_index") else "METADATA_ONLY"


def venue(record: dict) -> str | None:
    return (record.get("primary_location") or {}).get("source", {}).get("display_name")


def validate_record(record: dict) -> None:
    if not record.get("id"):
        raise ValueError("OpenAlex record missing id")
    if not (record.get("title") or "").strip():
        raise ValueError("OpenAlex record missing title")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--artifact", type=Path, required=True)
    p.add_argument("--openalex-id", required=True)
    p.add_argument("--project-id", required=True)
    p.add_argument("--retrieved-at", required=True)
    p.add_argument("--apply", action="store_true")
    return p.parse_args()


def ensure_active_project(conn, project_id: str) -> None:
    row = conn.execute(
        "SELECT status FROM research_project WHERE id = %s", (project_id,)
    ).fetchone()
    if not row:
        raise ValueError(f"Project not found: {project_id}")
    if row[0] != "ACTIVE":
        raise ValueError(f"Project is not ACTIVE: {project_id} ({row[0]})")


def ensure_source(conn) -> str:
    row = conn.execute(
        "SELECT id FROM literature_source WHERE source_key = %s", (SOURCE_KEY,)
    ).fetchone()
    if row:
        return str(row[0])
    return str(conn.execute(
        """INSERT INTO literature_source
           (source_key, name, source_type, active, configuration_reference)
           VALUES (%s, %s, %s, true, %s) RETURNING id""",
        (SOURCE_KEY, "OpenAlex", "BIBLIOGRAPHIC_API", "provider:openalex"),
    ).fetchone()[0])


def ensure_source_record(conn, source_id: str, record: dict,
                         retrieved_at: str) -> str:
    openalex_id = normalize_openalex(record["id"])
    row = conn.execute(
        """SELECT id FROM source_record
           WHERE literature_source_id = %s
             AND source_record_identifier = %s
             AND retrieved_at = %s""",
        (source_id, openalex_id, retrieved_at),
    ).fetchone()
    if row:
        return str(row[0])
    return str(conn.execute(
        """INSERT INTO source_record
           (literature_source_id, source_record_identifier, retrieved_at,
            raw_metadata_jsonb, content_access_state, normalization_state,
            provenance_hash)
           VALUES (%s, %s, %s, %s, %s, 'UNRESOLVED', %s)
           RETURNING id""",
        (source_id, openalex_id, retrieved_at, Jsonb(record),
         access_state(record), record_hash(record)),
    ).fetchone()[0])


def find_work_by_identifier(conn, identifier_type: str,
                            identifier_value: str | None) -> str | None:
    if not identifier_value:
        return None
    row = conn.execute(
        """SELECT work_id FROM work_identifier
           WHERE identifier_type = %s AND identifier_value = %s""",
        (identifier_type, identifier_value),
    ).fetchone()
    return str(row[0]) if row else None


def resolve_work(conn, record: dict) -> str:
    openalex_id = normalize_openalex(record["id"])
    doi = normalize_doi(record["doi"]) if record.get("doi") else None
    by_openalex = find_work_by_identifier(conn, "OPENALEX", openalex_id)
    by_doi = find_work_by_identifier(conn, "DOI", doi)
    if by_openalex and by_doi and by_openalex != by_doi:
        raise ValueError("Identifier collision: OpenAlex and DOI resolve to different works")
    existing = by_openalex or by_doi
    if existing:
        return existing
    return str(conn.execute(
        """INSERT INTO work
           (title, publication_date, publication_year, venue, work_type,
            current_access_level)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
        (record["title"].strip(), record.get("publication_date"),
         record.get("publication_year"), venue(record), record.get("type"),
         access_state(record)),
    ).fetchone()[0])


def ensure_identifier(conn, work_id: str, identifier_type: str,
                      identifier_value: str | None, is_primary: bool) -> None:
    if not identifier_value:
        return
    owner = find_work_by_identifier(conn, identifier_type, identifier_value)
    if owner and owner != work_id:
        raise ValueError(f"Identifier already belongs to another work: {identifier_type}")
    conn.execute(
        """INSERT INTO work_identifier
           (work_id, identifier_type, identifier_value, is_primary)
           VALUES (%s, %s, %s, %s)
           ON CONFLICT (identifier_type, identifier_value) DO NOTHING""",
        (work_id, identifier_type, identifier_value, is_primary),
    )


def ensure_work_link(conn, work_id: str, source_record_id: str,
                     matched_at: str) -> None:
    row = conn.execute(
        "SELECT work_id FROM work_source_record WHERE source_record_id = %s",
        (source_record_id,),
    ).fetchone()
    if row and str(row[0]) != work_id:
        raise ValueError("SourceRecord already linked to another Work")
    conn.execute(
        """INSERT INTO work_source_record
           (work_id, source_record_id, match_method, match_state, matched_at)
           VALUES (%s, %s, %s, 'MATCHED', %s)
           ON CONFLICT (source_record_id) DO NOTHING""",
        (work_id, source_record_id, "openalex_identifier_resolution", matched_at),
    )


def ensure_project_relevance(conn, project_id: str, work_id: str,
                             seen_at: str) -> None:
    conn.execute(
        """INSERT INTO project_work_relevance
           (project_id, work_id, relevance_state, relevance_advice, rationale,
            origin, human_review_state, first_seen_at, last_seen_at)
           VALUES (%s, %s, 'CANDIDATE', NULL, %s, %s, NULL, %s, %s)
           ON CONFLICT (project_id, work_id) DO UPDATE
           SET last_seen_at = GREATEST(project_work_relevance.last_seen_at,
                                      EXCLUDED.last_seen_at)""",
        (project_id, work_id,
         "Discovered from OpenAlex; awaiting HUMAN relevance review.",
         "openalex_import", seen_at, seen_at),
    )


def persist(record: dict, project_id: str, retrieved_at: str) -> dict:
    with psycopg.connect(dsn()) as conn:
        ensure_active_project(conn, project_id)
        source_id = ensure_source(conn)
        source_record_id = ensure_source_record(conn, source_id, record, retrieved_at)
        work_id = resolve_work(conn, record)
        openalex_id = normalize_openalex(record["id"])
        doi = normalize_doi(record["doi"]) if record.get("doi") else None
        ensure_identifier(conn, work_id, "OPENALEX", openalex_id, True)
        ensure_identifier(conn, work_id, "DOI", doi, False)
        ensure_work_link(conn, work_id, source_record_id, retrieved_at)
        conn.execute("UPDATE source_record SET normalization_state = 'MATCHED' WHERE id = %s",
                     (source_record_id,))
        ensure_project_relevance(conn, project_id, work_id, retrieved_at)
        return {"source_id": source_id, "source_record_id": source_record_id,
                "work_id": work_id}


def preview(record: dict, args) -> dict:
    return {
        "openalex_id": normalize_openalex(record["id"]),
        "doi": normalize_doi(record["doi"]) if record.get("doi") else None,
        "title": record.get("title"),
        "publication_date": record.get("publication_date"),
        "type": record.get("type"),
        "venue": venue(record),
        "access_state": access_state(record),
        "provenance_hash": record_hash(record),
        "project_id": args.project_id,
        "retrieved_at": args.retrieved_at,
        "mode": "APPLY" if args.apply else "DRY_RUN",
    }


def main():
    args = parse_args()
    record = load_record(args.artifact, args.openalex_id)
    validate_record(record)
    result = preview(record, args)
    if args.apply:
        result.update(persist(record, args.project_id, args.retrieved_at))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
