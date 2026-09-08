# J3 ResearchProject Contract Acceptance v0

## Status

**ACCEPTED / PASS**

The J3 ResearchProject contract has been checked against the canonical PostgreSQL production schema and is sufficient for v0 without a DDL change.

## Production schema evidence

`research_project` provides:

- stable UUID identity;
- mandatory `profile_id` parentage;
- HUMAN-readable `name`;
- lifecycle status `ACTIVE | PAUSED | ARCHIVED`;
- `current_version_id` pointer constrained to the same Project;
- creation metadata.

`research_project_version` provides:

- append-oriented positive `version_no`;
- HUMAN `research_intent`;
- optional, revisable `provisional_rq_text`;
- generic `project_configuration_jsonb`;
- same-Project `supersedes_version_id` lineage;
- creation metadata.

Production foreign keys also confirm that ResearchProject is already the contextual anchor for downstream canonical objects including `assessment`, `change_event`, `coverage_context`, `gap_candidate`, `human_decision`, `project_work_relevance`, and `research_object_identity`.

## Contract conclusions

1. Profile and Project remain distinct: Profile is reusable/versioned research context; Project is a specific HUMAN research effort under one Profile.
2. Project identity is stable while meaning evolves through append-oriented Project versions.
3. Provisional RQ is optional and revisable; it is not a gate.
4. Project configuration remains domain-agnostic and may vary by configuration values rather than core code branches.
5. No schema field or Project status encodes automated scientific acceptance or global workflow locking.
6. The existing schema is sufficient to anchor R0–R16, project-scoped opportunities, assessments, change events, coverage snapshots, and HUMAN decisions.
7. No DDL change is required for the v0 Project contract.

## Bootstrap direction

The next implementation step is a deliberately minimal Project bootstrap proving:

`ResearchProfile → ResearchProject → ResearchProjectVersion → Research Cockpit context`

The bootstrap must:

- use the same transaction mechanics for Profile A and Profile B;
- create one initial HUMAN research Project under each reference Profile;
- keep `provisional_rq_text` nullable/revisable;
- use one generic project-configuration shape across both domains;
- create no synthetic Work, Claim, EvidenceFragment, GapCandidate, Assessment, ChangeEvent, or HumanDecision merely for UI population;
- be tested outside production before deployment.

The initial Project names and research intents should represent actual HUMAN research efforts rather than fabricated scientific conclusions.

## Generality check

- Works for Profile A: **YES**
- Works for Profile B: **YES**
- Domain-specific core branch required: **NO**
- Difference representation: **Research Profile / Project configuration**
- Generality exception: **NONE identified at this stage**

## Result

**J3 ResearchProject Contract — ACCEPTED / PASS**

J3 remains active until the minimal A/B Project bootstrap/read path is implemented and verified. This acceptance does not claim scientific validity for any future Project content and does not authorize synthetic evidence insertion.
