-- J15 bounded runtime privileges for ChangeEvent traceability.
-- Production application requires separate HUMAN/deployment approval.
BEGIN;

GRANT SELECT, INSERT ON change_event_evidence TO gfproj_app;
REVOKE UPDATE, DELETE ON change_event_evidence FROM gfproj_app;

-- change_event remains append-oriented. Existing SELECT/INSERT grant is sufficient
-- for the writer to populate canonical Assessment references at INSERT time.

COMMIT;
