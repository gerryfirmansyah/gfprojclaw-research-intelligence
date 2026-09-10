import argparse
from datetime import datetime, timezone
import sys

from psycopg.types.json import Jsonb

sys.path.insert(0, "/opt/gfprojclaw-research-intelligence/prototype/api")
from db import db


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    observed_at = datetime.now(timezone.utc)
    with db() as conn:
        project = conn.execute("""
            SELECT p.id, rp.current_version_id AS profile_version_id,
                   p.current_version_id AS project_version_id
            FROM research_project p
            JOIN research_profile rp ON rp.id = p.profile_id
            WHERE p.id = %s AND p.status = 'ACTIVE'
        """, (args.project_id,)).fetchone()
        if not project:
            raise SystemExit("active project not found")

        access = conn.execute("""
            SELECT w.current_access_level, count(*) AS n
            FROM project_work_relevance pwr
            JOIN work w ON w.id = pwr.work_id
            WHERE pwr.project_id = %s
            GROUP BY w.current_access_level
        """, (args.project_id,)).fetchall()
        claim_counts = conn.execute("""
            SELECT count(*) AS claims,
                   count(*) FILTER (WHERE c.quarantine_state = 'QUARANTINED') AS quarantined
            FROM project_work_relevance pwr
            JOIN evidence_fragment ef ON ef.work_id = pwr.work_id
            JOIN claim c ON c.evidence_fragment_id = ef.id
            WHERE pwr.project_id = %s
        """, (args.project_id,)).fetchone()

        source_rows = conn.execute("""
            SELECT ls.id, ls.source_key, count(DISTINCT sr.id) AS observed_records
            FROM project_work_relevance pwr
            JOIN work_source_record wsr ON wsr.work_id = pwr.work_id
            JOIN source_record sr ON sr.id = wsr.source_record_id
            JOIN literature_source ls ON ls.id = sr.literature_source_id
            WHERE pwr.project_id = %s
            GROUP BY ls.id, ls.source_key
        """, (args.project_id,)).fetchall()

        access_summary = {r["current_access_level"]: r["n"] for r in access}
        payload = {
            "observed_at": observed_at.isoformat(),
            "access_summary": access_summary,
            "claims": claim_counts["claims"],
            "quarantined": claim_counts["quarantined"],
            "sources": [dict(r) for r in source_rows],
            "counter_search_state": "NOT_RUN",
        }
        if not args.apply:
            print(payload)
            return
        coverage = conn.execute("""
            INSERT INTO coverage_context (
                project_id, profile_version_id, project_version_id, observed_at,
                query_context_jsonb, temporal_window_jsonb, access_summary_jsonb,
                extraction_summary_jsonb, counter_search_state, limitations
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id
        """, (
            args.project_id, project["profile_version_id"], project["project_version_id"],
            observed_at, Jsonb({"mode":"bootstrap_real_slice"}), Jsonb({}),
            Jsonb(access_summary), Jsonb({"claims": claim_counts["claims"], "quarantined": claim_counts["quarantined"]}),
            "NOT_RUN", "Coverage reflects the current persisted project slice only; discovery breadth and counter-search are not yet complete."
        )).fetchone()

        for source in source_rows:
            conn.execute("""
                INSERT INTO coverage_source_state (
                    coverage_context_id, literature_source_id, health_state,
                    attempted_record_count, observed_record_count, access_limitations, degradation_reason
                ) VALUES (%s,%s,'ATTENTION',NULL,%s,%s,NULL)
            """, (coverage["id"], source["id"], source["observed_records"],
                  "Single bootstrap slice; continuous provider health monitoring is not yet implemented."))

        print({"coverage_context_id": str(coverage["id"]), **payload})


if __name__ == "__main__":
    main()
