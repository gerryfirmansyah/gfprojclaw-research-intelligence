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
