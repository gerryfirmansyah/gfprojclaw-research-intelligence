# J14 Continuous Pilot Gap Audit v0

## Finding
J14 is not ready for overall HUMAN PASS. Two independent gaps remain: production execution identity/scheduling, and real source execution inside the continuous worker.

## Demonstrated
- Canonical pilot run/stage persistence, idempotent RUNNING resume, bounded retry delay, local-failure semantics, and persisted failure/recovery observability.
- Cockpit pilot-health projection and canonical Daily Radar traceability.
- HUMAN-accepted Telegram format, live delivery, project/domain separation, and recovery semantics.
- Scientific guardrail evidence: automatic scientific decisions remain zero; pilot authority excludes HumanDecision writes at the tested DB role boundary.
- Disabled scheduler and peer-auth templates plus deterministic activation/rollback runbook.

## Gap A — production identity/scheduler
`gfproj-pilot` is not provisioned. Therefore Unix peer/map authentication to `gfproj_pilot_executor`, effective `gfproj_pilot_worker`, and an installed canonical timer cannot yet be validated end-to-end. This remains an infrastructure prerequisite; do not bypass it.

## Gap B — continuous worker source execution
`tools/run_continuous_pilot.py` currently models OpenAlex/Crossref stage outcomes and retry behavior with simulation. It does not itself perform real OpenAlex/Crossref discovery/retrieval. Existing OpenAlex import tooling consumes a supplied artifact and currently uses the Cockpit runtime DB credential path, so it must not simply be called by the scheduled worker as-is.

This means the contract flow `Scheduled Pilot Run -> source-local discovery/retrieval -> canonical Work/SourceRecord/...` has not yet been proven as one continuous least-privilege production worker path.

## Required closure before overall J14 HUMAN PASS
1. Add bounded real source adapters with explicit timeout/retry and source-local failure behavior. Start with metadata discovery/retrieval only; do not create scientific verdicts.
2. Persist retrieved provenance through a worker-authorized canonical ingestion boundary that does not reuse `gfproj_app`/Cockpit authority and does not grant broad scientific writes.
3. Demonstrate idempotent real-source MANUAL execution for both Profile A and Profile B with traceable canonical records.
4. Demonstrate source degradation remains local and Radar/Cockpit accurately expose it.
5. Obtain HUMAN acceptance of the real-source continuous path.
6. Separately satisfy the authorized `gfproj-pilot` OS identity and peer/map end-to-end prerequisite, then trial the production service identity.
7. Only then install/test the canonical timer and obtain HUMAN acceptance before enablement.

## Non-goals
Do not auto-assert gap, novelty, significance, causality, relevance acceptance, or HUMAN decisions. Do not repurpose the legacy Telegram scheduler. Do not erase failed operational history.
