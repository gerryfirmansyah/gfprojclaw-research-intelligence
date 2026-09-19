# J14 Continuous Pilot Gap Audit v0

## Finding
J14 is not ready for overall HUMAN PASS. Production identity, bounded real-source execution, retry observability, and deterministic scheduled-window idempotency are now demonstrated. The remaining acceptance boundary is HUMAN review before timer installation or enablement.

## Demonstrated
- Canonical pilot run/stage persistence, idempotent RUNNING resume, bounded retry delay, local-failure semantics, and persisted failure/recovery observability.
- Cockpit pilot-health projection and canonical Daily Radar traceability.
- HUMAN-accepted Telegram format, live delivery, project/domain separation, and recovery semantics.
- Scientific guardrail evidence: automatic scientific decisions remain zero; pilot authority excludes HumanDecision writes at the tested DB role boundary.
- Disabled scheduler and peer-auth templates plus deterministic activation/rollback runbook.

## Gap A — production identity/scheduler
`gfproj-pilot` is provisioned and peer/map authentication to `gfproj_pilot_executor` is verified. The canonical timer remains uninstalled and disabled pending HUMAN acceptance.

## Gap B — continuous worker source execution
`tools/run_continuous_pilot.py` now executes bounded OpenAlex/Crossref discovery through the dedicated executor and metadata-ingestor boundary. MANUAL Profile A/B execution, persisted retry observability, and deterministic Profile A SCHEDULED wrapper execution plus replay have been demonstrated. Controlled simulation requires explicit opt-in.

## Required closure before overall J14 HUMAN PASS
1. Complete final regression and diff review of the adapters, ingestion path, worker, scheduled wrapper, and templates.
2. Capture the current production proof and keep service/timer installation disabled.
3. Obtain explicit HUMAN acceptance of the real-source continuous path.
4. Only after that acceptance, install/test the canonical service/timer and obtain separate HUMAN acceptance before timer enablement.

## Non-goals
Do not auto-assert gap, novelty, significance, causality, relevance acceptance, or HUMAN decisions. Do not repurpose the legacy Telegram scheduler. Do not erase failed operational history.
