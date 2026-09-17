# J14 Continuous Pilot Contract v0

## Purpose
J14 proves continuous research operation without transferring scientific authority from HUMAN to machine.

## Canonical flow
Scheduled Pilot Run -> source-local discovery/retrieval -> canonical Work/SourceRecord/EvidenceFragment/Claim -> advisory processing -> ChangeEvent/Radar -> Telegram summary -> Cockpit drill-down -> HUMAN validation/decision.

## Non-negotiable invariants
- HUMAN is the only scientific decision authority.
- A pilot run MUST NOT create HumanDecision records.
- Source or stage failure is local; it MUST NOT globally lock unrelated projects/sources.
- Every digest number MUST be reproducible from canonical persisted records and an explicit time window.
- Telegram is a projection/delivery surface, never canonical state.
- Access provenance and review state remain visible; ABSTRACT_ONLY is not FULL_TEXT.
- No automatic claim of research gap, novelty, significance, or causality.

## Pilot run envelope
Each run has: run_id, started_at, finished_at, trigger, project/profile scope, status, stage/source outcomes, retry counts, and machine_actions. Status is RUNNING, COMPLETED, PARTIAL, or FAILED. PARTIAL is preferred when one source/stage fails but useful canonical work succeeds elsewhere.

## Daily Research Radar contract
For [window_start, window_end), report canonical counts for newly discovered works, screened/review-state candidates, new evidence fragments/claims, evidence or ChangeEvents affecting research objects, counter-evidence signals when explicitly persisted, local failures, pending HUMAN review, and scientific decisions made automatically.

The final metric MUST be `scientific_decisions_made_automatically = 0`; any non-zero value is a guardrail breach, not a successful digest.

## Traceability
Every aggregate exposes its query basis and drill-down identifiers. A number without canonical traceability MUST be omitted or labelled unavailable; it MUST NOT be guessed from filesystem artifacts or Telegram history.

## Scheduling boundary
Systemd timer may trigger a worker only after dry-run, idempotency, retry/local-failure, observability, and HUMAN trial are demonstrated. Existing legacy Telegram path/timer is not the J14 scheduler and remains untouched during initial implementation.
