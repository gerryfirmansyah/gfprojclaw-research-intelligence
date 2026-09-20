-- J15 ChangeEvent canonical Assessment/evidence traceability.
-- Versioned migration candidate; production application requires separate HUMAN/deployment approval.
BEGIN;

ALTER TABLE assessment
  ADD CONSTRAINT assessment_transition_reference_uk
  UNIQUE (id, supersedes_assessment_id, project_id, target_research_object_id);

ALTER TABLE change_event
  ADD COLUMN previous_assessment_id uuid NULL,
  ADD COLUMN current_assessment_id uuid NULL,
  ADD COLUMN current_supersedes_assessment_id uuid NULL,
  ADD CONSTRAINT change_event_id_object_uk UNIQUE (id, primary_research_object_id),
  ADD CONSTRAINT change_event_previous_assessment_fk
    FOREIGN KEY (previous_assessment_id, project_id, primary_research_object_id)
    REFERENCES assessment(id, project_id, target_research_object_id) ON DELETE RESTRICT,
  ADD CONSTRAINT change_event_current_assessment_fk
    FOREIGN KEY (current_assessment_id, project_id, primary_research_object_id)
    REFERENCES assessment(id, project_id, target_research_object_id) ON DELETE RESTRICT,
  ADD CONSTRAINT change_event_current_transition_fk
    FOREIGN KEY (current_assessment_id, current_supersedes_assessment_id, project_id, primary_research_object_id)
    REFERENCES assessment(id, supersedes_assessment_id, project_id, target_research_object_id)
    MATCH SIMPLE ON DELETE RESTRICT,
  ADD CONSTRAINT change_event_assessment_required_ck
    CHECK (change_type <> 'ASSESSMENT_CHANGED' OR current_assessment_id IS NOT NULL),
  ADD CONSTRAINT change_event_assessment_transition_ck
    CHECK (
      (previous_assessment_id IS NULL AND current_supersedes_assessment_id IS NULL)
      OR previous_assessment_id = current_supersedes_assessment_id
    );

ALTER TABLE evidence_relationship
  ADD CONSTRAINT evidence_relationship_id_target_uk
  UNIQUE (id, target_research_object_id);

CREATE TABLE change_event_evidence (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  change_event_id uuid NOT NULL,
  evidence_relationship_id uuid NOT NULL,
  target_research_object_id uuid NOT NULL,
  role text NOT NULL CHECK (role IN ('TRIGGER','CONTEXT')),
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT change_event_evidence_event_object_fk
    FOREIGN KEY (change_event_id, target_research_object_id)
    REFERENCES change_event(id, primary_research_object_id) ON DELETE RESTRICT,
  CONSTRAINT change_event_evidence_relationship_object_fk
    FOREIGN KEY (evidence_relationship_id, target_research_object_id)
    REFERENCES evidence_relationship(id, target_research_object_id) ON DELETE RESTRICT,
  CONSTRAINT change_event_evidence_member_uk
    UNIQUE (change_event_id, evidence_relationship_id, role)
);

CREATE INDEX change_event_evidence_event_idx ON change_event_evidence(change_event_id);
CREATE INDEX change_event_evidence_relationship_idx ON change_event_evidence(evidence_relationship_id);

-- Deterministic backfill: current production ASSESSMENT_CHANGED rows only.
UPDATE change_event ce
SET current_assessment_id = a.id,
    current_supersedes_assessment_id = a.supersedes_assessment_id,
    previous_assessment_id = a.supersedes_assessment_id
FROM assessment a
WHERE ce.change_type = 'ASSESSMENT_CHANGED'
  AND ce.current_assessment_id IS NULL
  AND ce.current_state_jsonb ? 'assessment_id'
  AND (ce.current_state_jsonb->>'assessment_id') ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
  AND a.id = (ce.current_state_jsonb->>'assessment_id')::uuid
  AND a.project_id = ce.project_id
  AND a.target_research_object_id = ce.primary_research_object_id;

-- No historical change_event_evidence backfill: exact trigger membership is not persisted.

COMMIT;
