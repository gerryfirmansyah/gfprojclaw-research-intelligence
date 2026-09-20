# J16 Admin Operational Health v0

Admin Copilot now projects a read-only production-health surface from `/api/admin/operational-health`.

It reports Cockpit API state, Telegram daily-radar timer, PostgreSQL backup timer, intentionally absent Continuous Pilot timer, historical legacy G6–G9 service state, latest local backup/count, and root-filesystem utilization. The projection returns `scientific_decision=false` and does not translate an operational failure into a scientific conclusion.

Production smoke test on 2026-09-20 returned API `active`, backup timer `active`, Continuous Pilot `not-found`, disk usage 18.6%, two local backups, and `scientific_decision=false`.

The legacy G6–G9 unit remains disabled and historically failed. It is displayed for operational visibility only and is not restarted by J16. Authentication/authorization, richer activity/audit projection, source/failure drill-down, and replication readiness remain pending J16 items.
