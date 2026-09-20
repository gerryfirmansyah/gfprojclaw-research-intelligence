#!/usr/bin/env python3
import sys
sys.path.insert(0, '/opt/gfprojclaw-research-intelligence/prototype/api')
from db import db
from context import _list_project_changes

P='3a100000-0000-4000-8000-000000000001'
O='edb00111-cf5b-5089-8464-c5f9135a0802'
E='07000000-0000-0000-0000-000000000010'
R='5396d3f4-a79f-5272-acdb-f049fbf63f59'

with db() as conn:
    conn.execute('BEGIN')
    try:
        conn.execute("INSERT INTO change_event (id,project_id,primary_research_object_id,change_type,observed_at,reasoning_delta) VALUES (%s,%s,%s,'EVIDENCE_ADDED',now(),'Disposable API projection regression test; no scientific transition implied.')", (E,P,O))
        conn.execute("INSERT INTO change_event_evidence (change_event_id,evidence_relationship_id,target_research_object_id,role) VALUES (%s,%s,%s,'TRIGGER')", (E,R,O))
        row=next(r for r in _list_project_changes(conn,P,O) if str(r['change_event_id'])==E)
        assert len(row['evidence_members']) == 1
        member=row['evidence_members'][0]
        assert member['role'] == 'TRIGGER'
        assert member['semantic_type'] == 'SUPPORTS'
        assert member['access_level'] == 'ABSTRACT_ONLY'
        print('J15_CHANGE_EVENT_MEMBER_PROJECTION_PASS')
    finally:
        conn.rollback()
