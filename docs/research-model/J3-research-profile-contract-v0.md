# J3 Research Profile Contract v0

Status: **J3 ACTIVE — Contract Baseline**

## 1. Purpose

J3 defines the minimum contract for a configurable, versioned Research Profile that can drive the same Research Intelligence Core across different research domains without domain-specific source-code modifications.

The governing principle is:

> **Domain knowledge belongs in versioned Research Profiles; the core provides generic research-intelligence behavior.**

J3 is not a taxonomy project and is not a hardcoded domain adapter. It establishes the contract that lets a HUMAN configure research context, vocabulary, attention targets, discovery preferences, theory/method interests, and prioritization preferences while preserving traceability and temporal history.

## 2. Human-Facing Questions J3 Must Enable

A valid Research Profile must help the system answer:

- Which research domain and thematic context is active?
- Which concepts, constructs, theories, models, methods, and terms should receive attention?
- Which literature should discovery prioritize without excluding unexpected evidence?
- Which recurring topics or relationships should be watched for change?
- Which source and access preferences affect coverage?
- Which advice dimensions should receive more or less attention for this profile?
- Which profile version was active when evidence, coverage, or an assessment was produced?
- Can a second domain use the same core without software changes?

## 3. Scope Boundary

### ResearchProfile owns reusable research context

Examples:

- domain and discipline context;
- terminology and search vocabulary;
- concepts/constructs of interest;
- seed works or identifiers;
- watchlists;
- theory/model/framework interests;
- method/measurement interests;
- source preferences;
- prioritization/advice preferences;
- configurable policies that do not constitute scientific verdicts.

### ResearchProject owns project-specific scientific work

Examples:

- specific research intent;
- provisional research questions;
- project-specific gap candidates;
- project-specific theory positioning;
- contribution candidates;
- R0–R16 stage state;
- assessments;
- HUMAN decisions.

Key rule:

> **A Profile guides discovery and interpretation context; it does not contain one project's scientific conclusions.**

## 4. Persistence Contract

The existing canonical persistence shape is retained.

### `research_profile`

Stores stable identity and lifecycle only:

- `id`;
- `name`;
- `status`;
- `current_version_id`;
- creation metadata.

### `research_profile_version`

Stores immutable/versioned profile content:

- `id`;
- `profile_id`;
- `version_no`;
- `summary`;
- `configuration_jsonb`;
- `supersedes_version_id`;
- creation metadata.

The v0 contract intentionally uses bounded JSONB for flexible profile configuration. It does not introduce one table per domain concept.

## 5. Minimum `configuration_jsonb` Contract

The following top-level structure is the J3 v0 baseline:

```json
{
  "schema_version": "research-profile-v0",
  "context": {},
  "terminology": {},
  "concepts": [],
  "watchlists": [],
  "seed_works": [],
  "theory_interests": [],
  "method_interests": [],
  "source_preferences": {},
  "advice_preferences": {},
  "discovery_preferences": {},
  "notes": {}
}
```

The structure is generic. Domain vocabulary appears only in values and object instances.

## 6. Field Semantics

### `schema_version`

Identifies the profile configuration contract used by the stored version.

It is not the same as `research_profile_version.version_no`.

### `context`

Describes reusable domain context.

Recommended v0 fields:

```json
{
  "domain": "...",
  "disciplines": ["..."],
  "description": "...",
  "language_preferences": ["en"]
}
```

No core behavior may branch on literal domain names.

### `terminology`

Provides configurable vocabulary used for discovery and interpretation support.

Recommended structure:

```json
{
  "preferred_terms": [],
  "synonyms": {},
  "related_terms": [],
  "excluded_or_ambiguous_terms": []
}
```

These terms guide retrieval and analysis; they are not evidence that a concept is scientifically valid.

### `concepts`

Contains profile-level concepts or constructs of recurring interest.

A concept entry may contain:

```json
{
  "key": "stable-profile-local-key",
  "label": "...",
  "aliases": [],
  "description": "...",
  "priority": "NORMAL"
}
```

Profile-local concept configuration does not replace canonical scientific objects extracted from literature.

### `watchlists`

Represents recurring research-attention targets.

A watchlist entry may target:

- topic/concept;
- theory/framework;
- method/measurement;
- relationship;
- author or venue when useful;
- other generic research object categories supported later.

Recommended structure:

```json
{
  "key": "...",
  "label": "...",
  "target_type": "CONCEPT",
  "terms": [],
  "priority": "NORMAL",
  "enabled": true
}
```

Watchlists prioritize attention. They must not act as global gates that exclude unrelated valid evidence.

### `seed_works`

Contains HUMAN-supplied starting literature references.

Preferred identifiers include DOI and other stable identifiers when available.

Seed works are discovery anchors, not privileged truth and not automatically accepted evidence.

### `theory_interests`

Contains theories, models, or frameworks the HUMAN wants the system to recognize and watch.

Entries are profile context only. Extracted claims about theories still require evidence provenance.

### `method_interests`

Contains recurring methods, operationalizations, measurements, research designs, or analytical approaches of interest.

The field may guide method intelligence but must not predetermine which method is scientifically appropriate for a project.

### `source_preferences`

Expresses source-level discovery preferences such as preferred providers, disabled providers, access priorities, or source-specific configuration references.

Key rule:

> **Source preference influences coverage strategy, not scientific truth.**

Credentials and secrets must never be stored in profile JSON.

### `advice_preferences`

Contains HUMAN-configurable weighting or attention preferences for advisory dimensions.

Examples may include:

- Gap Evidence Strength;
- Novelty Potential;
- Counter-Evidence Risk;
- Evidence Coverage;
- Theoretical Significance;
- Methodological Feasibility;
- RQ–Theory–Method Alignment;
- Practical/Policy Significance;
- Review Priority.

These settings change ranking or emphasis only.

Key rule:

> **No advice preference or score threshold may become an automated scientific acceptance verdict.**

### `discovery_preferences`

Contains configurable discovery hints such as time horizon, publication types, languages, keyword expansion preferences, and exploratory breadth.

These preferences are soft workflow controls. Failure to satisfy one preference must not create a global research lock.

### `notes`

Reserved for bounded HUMAN-readable annotations and profile metadata that do not justify adding a new canonical field in v0.

## 7. Versioning Contract

Profile configuration is append-oriented.

For an initial profile:

```text
ResearchProfile
  → ResearchProfileVersion v1
  → current_version_id = v1
```

For a later change:

```text
ResearchProfileVersion v1
  ← supersedes — v2
ResearchProfile.current_version_id = v2
```

Rules:

1. Existing historical versions are not overwritten for normal scientific/profile evolution.
2. `supersedes_version_id` must refer to a version of the same Profile.
3. A change to profile context creates a new version when it may affect discovery, coverage, interpretation, prioritization, or reproducibility.
4. Coverage and later temporal objects may retain the exact profile version that was active at the time.
5. Version history must remain inspectable by the HUMAN.

## 8. Reference Profiles for Continuous Generality Testing

J3 uses two simultaneous reference profiles.

### Profile A — Computer / Information Systems

Initial thematic context:

- IT Governance;
- e-Government / Digital Government;
- Enterprise Architecture.

### Profile B — Management / Organization Studies

Initial thematic context:

- Resilient Organization / Organizational Resilience;
- Human Behaviour;
- Human Capability.

These are reference configurations, not core domain modules.

Acceptance criterion:

> **Both profiles must run through the same canonical schema and Research Intelligence Core without domain-specific source-code modifications.**

## 9. Generality Exception Contract

When Profile A and Profile B require materially different behavior, J3 does not stop the project.

The difference is classified as one of:

- `PROFILE_CONFIG` — representable as profile/project configuration;
- `CORE_GENERALIZATION` — generic core abstraction should be extended;
- `ADD_IN_CANDIDATE` — specialized optional capability is justified;
- `UNRESOLVED_GENERALITY` — tracked architectural debt, non-blocking.

Governing principle:

> **Perbedaan kebutuhan domain tidak menghentikan project. Ia menjadi sinyal untuk menentukan apakah core perlu digeneralisasi, konfigurasi diperluas, atau capability domain-specific dipisahkan sebagai add-in/plugin.**

Any future add-in must preserve evidence traceability, HUMAN authority, history, local-failure semantics, and non-gating research behavior.

## 10. Scientific Integrity Rules

1. Profile terms are retrieval/attention context, not evidence.
2. Seed works are anchors, not accepted truth.
3. Profile theory interests do not imply theoretical validity.
4. Profile method interests do not imply methodological suitability.
5. Absence from a watchlist does not imply irrelevance.
6. Source preferences must be reflected in CoverageContext when they affect evidence coverage.
7. Machine-generated suggestions for profile content remain proposals until accepted or modified by the HUMAN.
8. Scientific claims still follow:

```text
Source → Passage/Record → Claim → Evidence → Synthesis/Research Object → HUMAN Judgment
```

## 11. Operational Rules

1. A malformed Profile version may be rejected or quarantined locally without stopping unrelated profiles or projects.
2. A disabled or failing source degrades coverage rather than globally blocking research.
3. Profile updates are independent of crawler recovery or engineering authorization.
4. Daily processing uses the current profile version for new work while preserving historical context for previous work.
5. Secrets, API keys, passwords, and connection credentials never belong in `configuration_jsonb`.

## 12. V0 Validation Requirements

Before J3 is accepted, the implementation must demonstrate:

1. Profile A can be represented by this contract.
2. Profile B can be represented by this contract.
3. Both use the same persistence shape.
4. No core code contains domain-specific branches for A or B.
5. Each profile has a deterministic initial version.
6. `current_version_id` correctly points to that version.
7. Version supersession can be demonstrated without overwriting history.
8. Profile configuration can be retrieved by the runtime role.
9. No synthetic profile fixture is silently treated as scientific evidence.
10. Any A/B mismatch is classified through the Generality Exception contract rather than used as a project-stopping gate.

## 13. Not Building Yet

J3 v0 does not yet build:

- full ontology management;
- domain-specific agents;
- autonomous scientific profile generation;
- profile-derived scientific acceptance thresholds;
- one database table per domain concept;
- source credentials management inside the profile;
- full Watchlist canonical persistence model;
- full theory/method object persistence beyond the J2 vertical slice;
- final UI forms for every profile field.

Those capabilities may be added only when they enable a clear HUMAN research decision, dashboard experience, Telegram signal, evidence trace, integrity requirement, or justified generality extension.

## 14. J3 Exit Direction

The next implementation artifact after this contract should be a deterministic, reviewable bootstrap/configuration for Profile A and Profile B using the same generic structure.

Expected progression:

```text
J3 Contract
  → Profile A/B Reference Configurations
  → Validation against same schema
  → Safe bootstrap path
  → HUMAN-visible Profile selector / Project binding
```

No production profile data should be inserted until the reference configurations and validation contract have been reviewed.

## 15. Acceptance Statement

J3 v0 is acceptable when a Research Profile can be treated as a reusable, versioned configuration of research context rather than as domain-specific application code.

The architectural target remains:

> **General Research Intelligence Engine + configurable Research Domain Profile.**
