# J16 Admin Navigation v0

The Admin Copilot sidebar is now functional navigation rather than a visual placeholder. Views are System Overview, Profile & Project, Continuous Pilot, Source Runs, Failures / Retry, Quarantine, API / Services, Activity / Audit, and Appearance & Language.

Existing canonical/operational projections are reused: pilot health, provider coverage, production service/backup/storage health, and the operational activity log. Failure/Retry is derived only from persisted pilot runs. Quarantine explicitly reports `NOT_AVAILABLE` until a canonical quarantine projection exists; no dummy records are invented.

Profile & Project configuration has its own Admin view. Research Copilot remains read-only for this configuration. Admin authentication/authorization remains pending and is required before final J16 production acceptance.
