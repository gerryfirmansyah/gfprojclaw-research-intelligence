# J14 Pilot Worker Execution Contract v0

## Purpose
Define the least-privilege execution boundary for the continuous pilot before any persisted MANUAL run or scheduler activation.

## Required identity boundary
- The operating-system execution identity MUST be dedicated to the pilot or otherwise demonstrably equivalent in privilege isolation.
- PostgreSQL execution MUST resolve to `gfproj_pilot_worker` without reusing Cockpit application authority.
- `gfproj_pilot_worker` MUST remain NOLOGIN, NOSUPERUSER, NOCREATEDB, NOCREATEROLE, and NOINHERIT unless a later reviewed architecture decision explicitly replaces this model.
- No new database password is required by this contract; local peer/map authentication is preferred when safely provisionable.

## Database authority
The worker MAY SELECT/INSERT/UPDATE only the operational pilot run/stage records required for observability. It MUST NOT INSERT, UPDATE, or DELETE `human_decision`. It MUST NOT obtain DDL ownership or broad canonical scientific write authority merely to run the scheduler.

## Fail-closed startup assertions
Before write mode starts, the worker MUST verify its effective database identity and required operational privileges. Startup MUST fail if the effective role is unexpected, HumanDecision write privilege is present, or required operational privilege is absent.

## Scientific authority boundary
A pilot execution may discover, retrieve, deduplicate, record provenance, measure source health, and create explicitly advisory machine outputs only through separately authorized canonical workflows. It MUST NOT automatically establish a research gap, novelty, significance, causal mechanism, or HUMAN decision.

## Scheduling gate
Systemd scheduling and Telegram delivery remain disabled until dry-run, idempotency, bounded retry, local-failure isolation, persisted operational observability, recovery, and a HUMAN-trialable manual run have passed. The legacy Telegram timer/path is not repurposed.
