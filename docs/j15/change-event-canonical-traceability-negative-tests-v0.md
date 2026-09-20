# J15 ChangeEvent Canonical Traceability — Negative Integrity Tests v0

Date: 2026-09-20
Status: pre-migration executable test design
Contract: docs/j15/change-event-canonical-traceability-contract-v0.md

## Purpose

Define failure cases before DDL implementation so the migration is judged by canonical integrity, not merely by successful creation.

All tests must run transactionally and roll back. They must not mutate production scientific state.

## Test A — Cross-object EvidenceRelationship attachment must fail

Given ChangeEvent E targets ResearchObject A and EvidenceRelationship R targets ResearchObject B, inserting a change_event_evidence row pairing E with R must fail at database constraint level.

Expected protection: composite same-object foreign keys.

## Test B — Same-object EvidenceRelationship attachment may pass

Given ChangeEvent E and EvidenceRelationship R both target ResearchObject A, and role is valid, the association is structurally eligible.

This is a persistence-integrity test only. It does not assert that R scientifically caused E.

## Test C — Invalid evidence role must fail

A role outside the explicit J15 vocabulary must fail.

Initial allowed roles: TRIGGER, CONTEXT.

## Test D — Cross-project current Assessment must fail

Given a ChangeEvent in Project A, assigning current_assessment_id from Project B must fail even if UUIDs are otherwise valid.

Expected protection: composite Assessment reference using event project_id and primary_research_object_id lineage.

## Test E — Cross-object Assessment in same Project must fail

Given a ChangeEvent targeting ResearchObject A, assigning an Assessment targeting ResearchObject B must fail.

This guards object lineage independently of project lineage.

## Test F — Initial ASSESSMENT_CHANGED without current Assessment must fail

For change_type = ASSESSMENT_CHANGED, current_assessment_id must be non-null.

previous_assessment_id may be null only when the current Assessment has no supersedes_assessment_id.

## Test G — Invalid before/after Assessment lineage must fail

If both previous_assessment_id and current_assessment_id are present, current Assessment must canonically supersede previous Assessment for the same project/object lineage.

A pair of unrelated Assessments must not be accepted merely because both target the same ResearchObject.

## Test H — Evidence trigger must not silently become literature discovery

A Work or source record without a canonical EvidenceRelationship must not be insertable into change_event_evidence because the association has no work_id/source_record_id shortcut.

Expected result: no schema path exists for bypassing EvidenceRelationship -> Claim -> EvidenceFragment -> Work.

## Test I — Cross-object trigger remains invalid across projects

An EvidenceRelationship targeting a ResearchObject in another Project must fail through the same-object composite key. No separate application-only project check is sufficient.

## Test J — Historical event must not acquire inferred current evidence

Migration/backfill verification must assert that existing ChangeEvents receive no change_event_evidence rows unless exact historical trigger membership is independently persisted and verifiable.

For the current production ASSESSMENT_CHANGED event, expected evidence-trigger backfill count is zero.

## Test K — Assessment backfill must be deterministic

Backfill current_assessment_id only when current_state_jsonb.assessment_id:
- parses as UUID;
- resolves to exactly one canonical Assessment;
- matches event project_id;
- matches event primary_research_object_id.

Any nonconforming row must stop or be reported for HUMAN review; it must not be guessed.
