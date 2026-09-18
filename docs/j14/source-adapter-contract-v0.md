# J14 Bounded Source Adapter Contract v0

## Purpose
Define real metadata discovery/retrieval for the continuous pilot without granting scientific authority or reusing Cockpit credentials.

## Input
A source adapter receives an ACTIVE project id plus an explicit discovery query derived from the current canonical ResearchProjectVersion configuration. Query derivation must be reproducible and persisted in operational provenance. If no reviewed discovery query exists, fail closed; never invent scientific scope from a project name.

## Output envelope
Each adapter returns source_key, request/query fingerprint, requested_at, completed_at, HTTP/result status, bounded record count, provider identifiers, raw metadata payload references/hashes, access/provenance metadata, and error class/summary when applicable. Adapter output is metadata/provenance only and contains no relevance acceptance, gap, novelty, significance, causality, or HUMAN decision.

## Network boundary
- Explicit connect/read timeout; no unbounded request.
- Bounded result/page count per run.
- Bounded retry count and delay/backoff.
- Provider 429/5xx/network failures remain source-local and are recorded as operational failure.
- User-Agent/contact configuration is explicit where provider policy expects it.
- Redirects/response sizes must remain bounded; malformed payloads fail locally.

## OpenAlex adapter
Use the public Works API for metadata discovery. Persist OpenAlex work id, DOI when supplied, title/publication metadata, access metadata, retrieval timestamp, and a deterministic payload hash. Abstract availability may establish ABSTRACT_ONLY provenance; it must not be treated as full text.

## Crossref adapter
Use the public Works API for bibliographic metadata discovery. Persist DOI/provider identifiers, title/publication metadata, retrieval timestamp, and deterministic payload hash. Crossref metadata does not by itself establish full-text access or scientific relevance.

## Canonical ingestion boundary
The adapter itself performs no database write. A separate worker-authorized ingestion boundary validates the envelope, deduplicates identifiers, and persists only explicitly granted canonical metadata/provenance. It must not reuse `gfproj_app`, and must not gain HumanDecision write authority or broad scientific-object write authority.

## Idempotency
A repeated provider record with the same canonical identifier and payload hash must not create duplicate Work identity. Retrieval events may remain separately traceable through SourceRecord provenance when the canonical model requires it.

## Acceptance
Before production scheduling: fixture tests, bounded live retrieval trial, malformed/rate-limit failure trial, idempotent ingestion trial, project A/B trial, canonical Radar/Cockpit traceability, scientific_decisions_made_automatically=0, and explicit HUMAN acceptance.
