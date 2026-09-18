# J14 Metadata Ingestion Boundary v0

## Purpose
Persist bounded provider discovery metadata without granting the continuous-pilot worker scientific interpretation authority.

## Separate capabilities
`gfproj_pilot_worker` remains operational-run authority only. Introduce a separate NOLOGIN capability role for metadata ingestion and grant it only the minimum canonical privileges required by reviewed ingestion code. The scheduled executor may SET ROLE into this capability only for the bounded ingestion transaction; it must return to the operational worker role for pilot-stage bookkeeping.

## Proposed metadata write surface
Subject to disposable verification before production migration:
- `literature_source`: SELECT only; providers should be pre-provisioned, not created by the worker.
- `source_record`: SELECT, INSERT, UPDATE only for normalization/provenance state required by ingestion.
- `work`: SELECT, INSERT; UPDATE is not required for v0 discovery ingestion.
- `work_identifier`: SELECT, INSERT.
- `work_source_record`: SELECT, INSERT.
- `project_work_relevance`: SELECT, INSERT, UPDATE only to maintain a `CANDIDATE` discovery association and first/last-seen timestamps. No relevance acceptance.
- `research_project`, `research_project_version`: SELECT only, solely to verify ACTIVE project and exact HUMAN-approved current discovery configuration.

## Explicitly forbidden
No INSERT/UPDATE/DELETE on `evidence_fragment`, `claim`, `evidence_relationship`, `gap_candidate`, `assessment`, `assessment_dimension`, `change_event`, `human_decision`, or research-direction objects. No DELETE on metadata tables. No use of `gfproj_app` or database owner credentials.

## Scientific semantics
A discovered Work is only a metadata candidate. Ingestion MUST NOT create an EvidenceFragment or Claim, mark relevance as HUMAN accepted, infer a gap/novelty/significance/causal mechanism, or create a HumanDecision. Provider abstract availability is access provenance only.

## Idempotency and provenance
Canonical Work identity resolves by provider identifier and DOI when available; collisions fail locally. Repeated identical provider payloads do not duplicate Work identity. SourceRecord retains provider identifier, retrieval timestamp, raw metadata, access state, and deterministic payload hash. Project association remains `CANDIDATE` pending HUMAN review.

## Acceptance before production use
1. migration/role SQL reviewed and verified in disposable PostgreSQL;
2. capability has exactly the intended table privileges and forbidden scientific writes fail;
3. fixture ingestion is idempotent;
4. malformed/collision cases fail locally without deleting history;
5. Profile A/B real-source MANUAL trial is traceable from ProjectVersion query to SourceRecord/Work;
6. `scientific_decisions_made_automatically = 0` and HumanDecision count is unchanged;
7. explicit HUMAN acceptance before scheduler activation.
