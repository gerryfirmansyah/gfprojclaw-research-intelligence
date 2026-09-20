# J15 ChangeEvent Canonical Traceability Contract v0

Date: 2026-09-20
Status: HUMAN-approved design direction; contract draft before migration
Baseline checkpoint: 88d0ca7

## 1. Purpose

Activate the already-accepted J2 ChangeEvent traceability design needed by the J15 HUMAN trial.

The requirement is: every scientifically meaningful aggregate or historical change exposed to HUMAN review must be traceable to the canonical members or typed records that caused it.

This contract does not make a scientific decision. HUMAN remains the scientific authority.

## 2. Existing J2 decisions carried forward

A ChangeEvent represents a meaningful reasoning change, not every crawler action.

A ChangeEvent may have many trigger references. One paper must not be forced to equal one ChangeEvent.

For the focal assessment type, a ChangeEvent may connect to:
- 0..1 previous Assessment;
- 0..1 current Assessment.

Where relevant, Assessment transitions use explicit before/after canonical references.

previous_state_jsonb and current_state_jsonb remain historical snapshots/explanations. They do not replace typed canonical records.

## 3. Minimum J15 activation

The existing change_event record remains the historical event envelope.

For Assessment-driven events, add canonical before/after Assessment references to change_event.

For evidence-driven events, activate change_event_evidence as a separate association so an event can have zero or many evidence triggers.

Do not reinterpret project literature as evidence. Evidence traceability requires the canonical EvidenceRelationship -> Claim -> EvidenceFragment -> Work chain.

## 4. Assessment transition constraints

Candidate canonical fields on change_event:
- previous_assessment_id uuid NULL;
- current_assessment_id uuid NULL.

When present, each Assessment reference must belong to the same project_id and primary_research_object_id as the ChangeEvent.

For ASSESSMENT_CHANGED, current_assessment_id is required. previous_assessment_id is optional only for the initial Assessment in a lineage.

When both references are present, current_assessment_id must supersede previous_assessment_id in the Assessment lineage.

The event observed_at should remain aligned with the focal current Assessment assessed_at for the current writer path.

No Assessment reference may be inferred later from whatever Assessment happens to be current.

## 5. Evidence trigger association

Minimum candidate fields for change_event_evidence:
- id uuid primary key;
- change_event_id uuid not null;
- evidence_relationship_id uuid not null;
- role text not null;
- created_at timestamptz not null default now().

For J15 minimum activation, EvidenceRelationship is the canonical atomic evidence trigger. Claim is reached through evidence_relationship.claim_id and must not be redundantly stored on the same association row.

The canonical drill-down is:
ChangeEvent -> change_event_evidence -> EvidenceRelationship -> Claim -> EvidenceFragment -> Work.

One ChangeEvent may have multiple evidence trigger rows. One EvidenceRelationship may participate in multiple ChangeEvents over time.

## 6. Project and object lineage for evidence triggers

The current EvidenceRelationship table has no project_id column. Its target_research_object_id is therefore the authoritative bridge to project lineage.

A change_event_evidence row is valid only when its EvidenceRelationship target_research_object_id equals the ChangeEvent primary_research_object_id.

This also prevents a Claim from another evidence chain being attached merely because its UUID exists.

The migration must enforce this at database level using a composite/reference shape that preserves the existing canonical EvidenceRelationship identity. Application-only validation is insufficient.

## 7. Role semantics

role describes the trigger's role in the ChangeEvent, not scientific truth.

J15 v0 should use a small explicit vocabulary and must not encode probability, significance, novelty proof, or HUMAN acceptance.

Proposed minimum:
- TRIGGER: relationship directly caused the recorded reasoning change;
- CONTEXT: relationship is explicitly preserved as relevant context but is not asserted to be the direct trigger.

Defaulting silently to TRIGGER is not allowed. The writer must state the role.

## 8. Quarantine and review state

change_event_evidence preserves historical trace; it does not promote quarantined evidence into active scientific support.

Consumers must expose the current/preserved EvidenceRelationship and Claim review/quarantine states when HUMAN drills down.

A historical ChangeEvent must not be rewritten merely because a linked Claim or EvidenceRelationship is later reviewed, contested, quarantined, or superseded.

## 9. Event-type requirements

ASSESSMENT_CHANGED:
- requires current_assessment_id;
- previous_assessment_id is nullable only for an initial Assessment;
- does not require change_event_evidence.

EVIDENCE_ADDED, EVIDENCE_CHALLENGED, EVIDENCE_CONTRADICTED:
- require at least one canonical evidence trigger before they may be exposed as member-traceable scientific-context changes;
- each trigger must target the same ResearchObject as the ChangeEvent.

GAP_STRENGTHENED, GAP_WEAKENED, GAP_CONTESTED, GAP_POSSIBLY_CLOSED, GAP_REOPENED:
- may be multi-trigger events;
- their existence is an attention/history signal, not an automatic scientific verdict;
- HUMAN-facing presentation must expose reasoning_delta and relevant trigger members.

COVERAGE_CHANGED:
- continues to use canonical coverage_context_id;
- must not fabricate evidence triggers when the change is coverage-only.

## 10. Discovery is not ChangeEvent evidence

A newly discovered Work is literature discovery until a canonical EvidenceRelationship exists.

Daily Brief may separately show newly discovered Works and allow member drill-down, but those Works must not be counted as SUPPORTS, CHALLENGES, or CONTRADICTS without the canonical evidence chain.

Raw crawler/source activity does not become a scientific ChangeEvent solely to populate an aggregate.

## 11. Temporal integrity and backfill

Do not backfill historical trigger members from the current evidence set.

Historical ChangeEvents may remain without evidence trigger rows when the exact historical trigger cannot be established from persisted canonical records.

The existing production ASSESSMENT_CHANGED event may be backfilled with Assessment references only if its stored assessment IDs and lineage can be deterministically verified against canonical Assessment rows.

UNKNOWN historical trigger detail is preferable to false precision.

## 12. HUMAN-facing traceability acceptance

A scientifically meaningful aggregate is acceptable only if the UI/API can enumerate its canonical members or explicitly state that historical member detail is unavailable.

Examples:
- 2 CONTRADICTS -> enumerate the two EvidenceRelationships and their Claim, EvidenceFragment, Work, rationale, access and review states;
- Assessment changed -> show previous/current Assessment when canonically recorded, plus reasoning_delta;
- 7 new papers -> enumerate the seven discovered Works without calling them evidence unless linked canonically.

No orphan aggregate is the governing J15 UX rule.

## 13. Non-goals

This contract does not:
- create a universal scientific quality score;
- prove gap, novelty, significance, relevance, or causality;
- authorize machine scientific acceptance/rejection;
- activate the continuous-pilot production timer;
- automatically convert project literature into ResearchObject evidence;
- declare J15 HUMAN PASS.

## 14. Migration gate

Before migration implementation:
1. verify the exact PostgreSQL constraint shape for same-object EvidenceRelationship linkage;
2. verify existing production ASSESSMENT_CHANGED data can be deterministically mapped to canonical Assessment;
3. define negative integrity tests for cross-project/cross-object attachment and invalid Assessment transitions;
4. preserve existing API behavior until the traceability projection is explicitly extended.

Only after these checks pass may a migration be proposed for HUMAN review.

## 15. Executable PostgreSQL constraint audit

Audit result: same-object evidence linkage can be enforced without adding project_id to EvidenceRelationship.

The minimum association should carry:
- change_event_id;
- evidence_relationship_id;
- target_research_object_id;
- role.

Required supporting uniqueness:
- change_event(id, primary_research_object_id);
- EvidenceRelationship already has UNIQUE (id, claim_id, target_research_object_id); add the narrower UNIQUE (id, target_research_object_id) only if PostgreSQL requires an exact referenced key for the chosen composite FK.

Required composite FKs:
- (change_event_id, target_research_object_id) -> change_event(id, primary_research_object_id);
- (evidence_relationship_id, target_research_object_id) -> evidence_relationship(id, target_research_object_id).

This makes target_research_object_id a deliberate duplicated lineage key in the association. It is not a second scientific assertion; it exists so PostgreSQL can reject cross-object trigger attachment.

Project lineage then follows from the ChangeEvent's already-enforced (primary_research_object_id, project_id) ResearchObject FK.

Production backfill audit on 2026-09-20:
- ASSESSMENT_CHANGED rows: 1;
- rows missing current_state_jsonb.assessment_id: 0;
- rows whose referenced Assessment disagrees with ChangeEvent project/object lineage: 0;
- the single current Assessment has supersedes_assessment_id = NULL.

Therefore the existing production ASSESSMENT_CHANGED row is deterministically eligible for current_assessment_id backfill, subject to migration review. No evidence-trigger historical backfill is authorized by this finding.

## 16. Before/after Assessment enforcement decision

Repository audit found no persistent database triggers in the canonical migrations. Existing lineage invariants are intentionally expressed with CHECK, UNIQUE, and composite FOREIGN KEY constraints.

J15 should preserve that pattern and avoid introducing a trigger solely for ChangeEvent Assessment lineage.

Executable shape:
- add previous_assessment_id and current_assessment_id to change_event;
- add UNIQUE support on change_event as required for composite references;
- reference each Assessment with (assessment_id, project_id, primary_research_object_id) -> assessment(id, project_id, target_research_object_id);
- for ASSESSMENT_CHANGED require current_assessment_id with a CHECK constraint.

Exact previous/current supersession is enforced declaratively by also carrying current_supersedes_assessment_id on the ChangeEvent transition row, constrained to equal previous_assessment_id when a previous Assessment exists, and by a composite FK:
(current_assessment_id, current_supersedes_assessment_id, project_id, primary_research_object_id)
-> assessment(id, supersedes_assessment_id, project_id, target_research_object_id).

This requires a matching UNIQUE key on Assessment for the referenced column tuple.

For an initial Assessment, both previous_assessment_id and current_supersedes_assessment_id are NULL. PostgreSQL MATCH FULL should be used where the nullable composite transition reference requires all-or-none semantics.

Rationale: keep lineage enforcement visible in DDL, consistent with existing GFPROJCLAW persistence style, rather than hiding scientific-history integrity in procedural trigger code.

Production audit: PostgreSQL 16.15; 3 Assessment rows currently exist and none currently supersedes another. Therefore the transition constraint must be proven with disposable test rows before production migration.

## 17. Disposable PostgreSQL proof result

Executed on 2026-09-20 through the authorized application database connection. All prototype objects were TEMP tables inside rollback-only transactions; production schema and scientific state were not changed.

Results:
- DDL prototype creation: PASS;
- valid Assessment previous -> current supersession transition: PASS;
- valid same-object EvidenceRelationship trigger: PASS;
- cross-object EvidenceRelationship trigger: rejected by ForeignKeyViolation;
- invalid evidence role: rejected by CheckViolation;
- ASSESSMENT_CHANGED without current Assessment: rejected by CheckViolation;
- current Assessment whose canonical supersedes link does not match the recorded transition: rejected by ForeignKeyViolation.

Conclusion: the proposed CHECK + UNIQUE + composite FOREIGN KEY + MATCH FULL approach is executable on the production PostgreSQL version without introducing a persistent trigger.

This proof authorizes drafting a migration proposal for HUMAN review; it does not itself authorize applying that migration.

## 18. Disposable PostgreSQL correction: nullable initial Assessment transition

GitHub Actions PostgreSQL 16 run 35480019858 rejected the first executable Migration 011 candidate while adding `change_event_current_transition_fk`: `MATCH FULL does not allow mixing of null and nonnull key values`. This is the expected initial-Assessment shape: current Assessment/project/object are present while `supersedes_assessment_id` is NULL.

Correction: use `MATCH SIMPLE` for the composite supersession FK. The independent `change_event_current_assessment_fk` continues to enforce current Assessment project/object lineage. For non-initial transitions, all supersession-key columns are non-null, so the composite FK enforces that the current Assessment canonically supersedes the recorded previous Assessment. The transition CHECK continues to require previous/current-supersedes nullness alignment or equality.

This correction replaces the earlier MATCH FULL proposal; the failed disposable run is retained as executable evidence and no production schema was changed.

## 19. Pre-production supersession integrity audit

A pre-production audit after commit `ae3b55f` found that `MATCH SIMPLE` fixes the nullable initial-Assessment deployment case but does not, by itself, prove exact canonical supersession when an event supplies `current_assessment_id` while both transition-side supersession fields are NULL. PostgreSQL skips the composite FK check when any referencing column is NULL.

Therefore production deployment remains blocked until an executable negative test proves rejection of this omission case. A CHECK comparing only the two ChangeEvent-side nullable fields is insufficient because it cannot inspect `assessment.supersedes_assessment_id`.

If the negative test demonstrates the gap, the declarative-only decision in Section 16 must be revisited explicitly. A narrowly scoped integrity trigger is the leading candidate because the invariant crosses a nullable referenced row and cannot be expressed by the current CHECK + MATCH SIMPLE FK combination without losing valid initial-Assessment rows. No production trigger is authorized by this audit alone.

## 20. Narrow exact-supersession trigger candidate

The executable candidate uses one narrowly scoped PostgreSQL constraint trigger on ChangeEvent. It does not derive scientific state, mutate Assessment, or create evidence. For ASSESSMENT_CHANGED only, it reads the already-selected canonical current Assessment on the same project/object lineage and requires both recorded transition-side supersession references to be exactly `IS NOT DISTINCT FROM` the Assessment's canonical `supersedes_assessment_id`.

The existing declarative FKs and CHECKs remain in place. The trigger closes only the nullable cross-row invariant that MATCH SIMPLE cannot express. Disposable verification must prove both sides before production review: omission of a real canonical predecessor is rejected, while an exact previous -> current supersession succeeds. This candidate is not production authorization.

## 21. Historical Assessment UUID guard correction

The first DBA-run disposable suite for the trigger candidate stopped safely before COMMIT because deterministic historical Assessment backfill reported `UPDATE 0`. The seeded canonical Assessment id `05000000-0000-0000-0000-000000000001` is accepted by PostgreSQL `uuid` and by the existing GFPROJCLAW fixture, but the migration's textual guard incorrectly required RFC version nibble 1-5 and variant nibble 8/9/a/b. GFPROJCLAW canonical fixture UUIDs intentionally include zero nibbles, so that guard excluded a valid canonical identifier before the cast/join.

Correction: retain a strict 8-4-4-4-12 hexadecimal textual-shape guard before the PostgreSQL uuid cast, but do not impose RFC version/variant semantics that the canonical schema does not require. Project/object lineage and exact Assessment identity remain enforced by the canonical join and foreign keys. Production remains blocked until the full disposable suite passes with this correction.
