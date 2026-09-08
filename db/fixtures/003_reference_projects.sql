-- J3 reference project bootstrap v0
-- Real reference configuration data for the Profile -> Project -> Cockpit path.
-- This file creates no scientific evidence, claims, gaps, assessments, or HUMAN decisions.
-- Deliberately non-idempotent: duplicate execution must fail locally.

BEGIN;

INSERT INTO research_project (
    id,
    profile_id,
    name,
    status,
    current_version_id,
    created_by
) VALUES
(
    '3a100000-0000-4000-8000-000000000001',
    '3a000000-0000-4000-8000-000000000001',
    'Computer / Information Systems Research Project',
    'ACTIVE',
    NULL,
    'j3-reference-project-bootstrap-v0'
),
(
    '3b100000-0000-4000-8000-000000000001',
    '3b000000-0000-4000-8000-000000000001',
    'Management / Organization Studies Research Project',
    'ACTIVE',
    NULL,
    'j3-reference-project-bootstrap-v0'
);

INSERT INTO research_project_version (
    id,
    project_id,
    version_no,
    research_intent,
    provisional_rq_text,
    project_configuration_jsonb,
    supersedes_version_id,
    created_by
) VALUES
(
    '3a100000-0000-4000-8000-000000000011',
    '3a100000-0000-4000-8000-000000000001',
    1,
    'Develop a traceable research landscape and identify evidence-backed research opportunities within the configured Computer / Information Systems profile while keeping scientific interpretation and acceptance under HUMAN authority.',
    NULL,
    '{
      "schema_version": "research-project-v0",
      "scope": {},
      "focus": {},
      "discovery_overrides": {},
      "advice_overrides": {},
      "notes": {
        "bootstrap_role": "reference initial project for the Profile -> Project -> Cockpit path",
        "scientific_evidence": false
      }
    }'::jsonb,
    NULL,
    'j3-reference-project-bootstrap-v0'
),
(
    '3b100000-0000-4000-8000-000000000011',
    '3b100000-0000-4000-8000-000000000001',
    1,
    'Develop a traceable research landscape and identify evidence-backed research opportunities within the configured Management / Organization Studies profile while keeping scientific interpretation and acceptance under HUMAN authority.',
    NULL,
    '{
      "schema_version": "research-project-v0",
      "scope": {},
      "focus": {},
      "discovery_overrides": {},
      "advice_overrides": {},
      "notes": {
        "bootstrap_role": "reference initial project for the Profile -> Project -> Cockpit path",
        "scientific_evidence": false
      }
    }'::jsonb,
    NULL,
    'j3-reference-project-bootstrap-v0'
);

UPDATE research_project
SET current_version_id = CASE id
    WHEN '3a100000-0000-4000-8000-000000000001'::uuid THEN '3a100000-0000-4000-8000-000000000011'::uuid
    WHEN '3b100000-0000-4000-8000-000000000001'::uuid THEN '3b100000-0000-4000-8000-000000000011'::uuid
END
WHERE id IN (
    '3a100000-0000-4000-8000-000000000001'::uuid,
    '3b100000-0000-4000-8000-000000000001'::uuid
);

COMMIT;
