# J16 Replacement Environment Replication Checklist v0

This checklist describes the next executable acceptance exercise; documentation alone is not replication PASS.

1. Provision a disposable/replacement Linux host with PostgreSQL, Python runtime, systemd, Git, and a dedicated `gfproj` account.
2. Clone the repository to `/opt/gfprojclaw-research-intelligence`; create runtime `/opt/gfprojclaw` directories with least-privilege ownership.
3. Supply runtime secrets out-of-band; do not copy credentials into Git or evidence documents.
4. Restore a verified production backup into a non-production PostgreSQL database and apply required runtime configuration.
5. Install Cockpit API and backup unit definitions; keep Continuous Pilot timer uninstalled/inactive unless separately authorized.
6. Start API and verify context, Profile A/B canonical versions, Daily Attention, quality/scientific boundaries, and `scientific_decision=false` operational projections.
7. Verify Telegram only when replacement credentials/destination are explicitly authorized; otherwise test notifier dry-run.
8. Verify backup creation plus disposable restore on the replacement environment.
9. Compare required service identity, file permissions, table/schema invariants, and regression suite with production baseline.
10. Record deviations and obtain HUMAN replication acceptance before calling the replacement equivalent.

Acceptance requires executable evidence from the replacement target. This file is preparation, not evidence that replication has occurred.
