# J3 Research Project Contract v0

Status: **J3 ACTIVE — Research Project Contract Baseline**

## 1. Purpose

This contract defines `ResearchProject` as the HUMAN-specific research context that operates under a reusable `ResearchProfile`.

A Profile describes reusable domain context, terminology, watchlists, seed anchors, theory/method interests, source preferences, discovery preferences, and advice preferences. A Project represents one concrete HUMAN research effort conducted within that context.

Governing hierarchy:

```text
RESEARCH PROFILE → RESEARCH PROJECT → RESEARCH COCKPIT
```

A Profile may support many Projects. R0–R16 state, project-specific gaps, research questions, theory positioning, method choices, assessments, change events, and HUMAN decisions belong to the Project context rather than to the reusable Profile.

## 2. Governing Principle

> **Profile defines reusable research context; Project defines one HUMAN research effort. Project state may evolve independently without mutating the reusable Profile.**

The Project must not collapse HUMAN scientific judgment into machine state, and no Project field may act as a global scientific gate.

## 3. Canonical Persistence Mapping

The existing canonical schema is sufficient for v0.

### `research_project`

```text
id                 stable opaque UUID
profile_id         parent ResearchProfile UUID
name               HUMAN-readable project name
status             ACTIVE | PAUSED | ARCHIVED
current_version_id current ResearchProjectVersion after version insert
created_at         system timestamp
created_by         actor/source identifier
```

### `research_project_version`

```text
id                          stable opaque UUID
project_id                  parent ResearchProject UUID
version_no                  positive append-oriented version number
research_intent             HUMAN research intent at this version
provisional_rq_text          optional evolving research question text
project_configuration_jsonb project-specific configuration/context
supersedes_version_id       previous version of the same Project or NULL
created_at                  system timestamp
created_by                  actor/source identifier
```

No DDL change is required for the v0 Project contract.

## 4. Identity and Versioning

Project identity is stable across time; Project meaning evolves through append-oriented `research_project_version` records.

Initial creation sequence:

```text
1. INSERT research_project with current_version_id = NULL
2. INSERT research_project_version v1
3. UPDATE research_project.current_version_id = v1
4. COMMIT
```

Later changes create v2, v3, and so on. Historical versions are retained and `supersedes_version_id` must remain within the same Project.

Create a new Project version when a change may materially affect research intent, provisional research question, project-scoped discovery emphasis, project-scoped interpretation, project-scoped prioritization, reproducibility, or downstream R0–R16 reasoning.

Routine operational events such as a transient source failure do not require a Project version.

## 5. Profile–Project Boundary

The boundary is intentionally strict.

### Belongs to Profile

Reusable context across multiple projects, including:

- domain and disciplines;
- terminology and synonyms;
- reusable concepts/watchlists;
- seed-work discovery anchors;
- theory/method interests;
- source preferences;
- discovery preferences;
- advice preference defaults.

### Belongs to Project

Context specific to one HUMAN research effort, including:

- research intent;
- provisional research question;
- project-specific scope and exclusions;
- project-specific focus or emphasis;
- project-specific R0–R16 state;
- project-specific gap candidates;
- project-specific theory positioning;
- project-specific method reasoning;
- project-specific assessments and change events;
- project-specific HUMAN decisions.

A Project may refine Profile defaults, but must not silently rewrite the Profile.

## 6. Minimum `project_configuration_jsonb` Shape

The v0 Project configuration uses one generic shape for all domains:

```json
{
  "schema_version": "research-project-v0",
  "scope": {},
  "focus": {},
  "discovery_overrides": {},
  "advice_overrides": {},
  "notes": {}
}
```

### `scope`

Project-specific boundaries such as population/context, organizational or societal setting, geography, level of analysis, time scope, and explicit exclusions. Fields remain optional and domain-neutral.

### `focus`

Project-specific terms, concepts, phenomena, relationships, or themes that deserve additional attention. These guide prioritization and must not create a hard filter that hides otherwise relevant counter-evidence.

### `discovery_overrides`

Optional soft overrides to Profile discovery preferences. Missing values inherit Profile context. Overrides must not create a global lock.

### `advice_overrides`

Optional HUMAN-selected project-level emphasis. Scores remain advice/ranking only and never become scientific acceptance thresholds.

### `notes`

Bounded HUMAN project annotations and metadata. Not scientific evidence.

## 7. Research Intent

`research_intent` is HUMAN-authored or HUMAN-approved project context describing what the researcher is trying to understand, explain, compare, design, evaluate, or challenge.

It is not an evidence-backed conclusion and it does not need to be phrased as a final research question.

At R0 it is expected to be provisional and revisable.

## 8. Provisional Research Question

`provisional_rq_text` is optional and explicitly provisional.

It may be NULL during early landscape/evidence work. The system must not force a research question before the HUMAN is ready.

When it changes materially, a new Project version preserves the history rather than overwriting the prior question.

## 9. R0–R16 Relationship

The Project is the anchor for the HUMAN Research Living Lab.

R0–R16 statuses are not stored as a single PASS/FAIL chain and are not Project gates. Each stage remains reversible and evidence-aware.

The Project provides the context under which later capabilities will represent:

```text
STATUS → WHY → EVIDENCE → LEARN → RISK → SUGGESTED ACTION → HUMAN DECISION → CHANGE HISTORY
```

No stage status prevents literature discovery or unrelated healthy processing.

## 10. Scientific Integrity Rules

1. Project intent and configuration are context, not scientific evidence.
2. A provisional RQ is not a validated finding.
3. Project focus may prioritize discovery but must not suppress contradictory or counter-evidence.
4. Project-level advice preferences may change ranking/emphasis only.
5. No score or configuration threshold may automatically accept a gap, novelty claim, theory, method, or contribution.
6. Scientific claims still require the canonical traceability path from Work and EvidenceFragment through Claim and EvidenceRelationship.
7. HUMAN decisions remain historical and separate from Assessment.
8. Project version history must remain inspectable for reproducibility.
9. Source or worker failure is local operational degradation, not Project failure.
10. A paused or archived Project must not redefine the scientific status of its historical evidence.

## 11. Cross-Domain Generality Requirement

The same Project contract must work beneath both reference Profiles:

- Profile A — Computer / Information Systems;
- Profile B — Management / Organization Studies.

No core code may branch on project domain names, domain terminology, theories, methods, or watchlist values.

If later execution reveals different Project behavior across domains, classify it as one of:

- `PROFILE_CONFIG`
- `CORE_GENERALIZATION`
- `ADD_IN_CANDIDATE`
- `UNRESOLVED_GENERALITY`

A generality exception is architectural learning, not a project stop.

## 12. Bootstrap Direction

The first Project bootstrap following this contract should be deliberately minimal.

For v0, create one real initial Project under each reference Profile using the same transaction mechanics and same generic JSON structure. The initial Projects should exist to prove the Profile → Project → Cockpit path, not to assert scientific conclusions.

Bootstrap must not create synthetic scientific evidence merely to populate the UI.

Project bootstrap data must be reviewed and tested outside production before deployment.

## 13. Acceptance Criteria

This contract is accepted when:

1. Project is clearly separated from reusable Profile context.
2. Existing `research_project` and `research_project_version` schema can persist the v0 contract without DDL changes.
3. Project history is append-oriented and traceable.
4. Provisional RQ remains optional and revisable.
5. Project configuration remains generic across Profile A/B.
6. No Project field creates a global gate or automated scientific verdict.
7. Project can become the anchor for R0–R16, project-specific research opportunities, assessments, change events, and HUMAN decisions.
8. The next implementation step can bootstrap minimal A/B Projects without inserting synthetic evidence.

## 14. Not Building Yet

This contract does not yet implement:

- R0–R16 persistence tables or UI state;
- literature ingestion;
- source credentials;
- ProjectWorkRelevance population;
- canonical evidence extraction;
- gap inference;
- theory/method canonical objects;
- assessment computation;
- HUMAN review UI;
- Telegram signals;
- publication positioning or J15 quality capabilities.

Those capabilities must attach to the Project incrementally while preserving evidence traceability and HUMAN authority.
