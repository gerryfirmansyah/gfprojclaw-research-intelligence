# J3 Reference Profile Configurations v0

Status: **J3 ACTIVE — Reference Configuration Baseline**

## 1. Purpose

This artifact instantiates the accepted `research-profile-v0` contract for two deliberately different research contexts while preserving one generic configuration structure.

The purpose is not to prove that two profiles are scientifically complete. The purpose is to test whether the same Research Intelligence Core can represent and operate on both contexts without domain-specific source-code branches.

Governing principle:

> **Generality is measured by running different domains through the same profile contract, evidence model, temporal model, and HUMAN authority model.**

## 2. Shared Structural Contract

Both Profile A and Profile B use exactly these top-level keys:

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

Differences between the profiles appear only in values and object instances.

No core code may branch on names such as `enterprise architecture`, `IT governance`, `organizational resilience`, or `human capability`.

## 3. Profile A — Computer / Information Systems

Reference profile name:

`Computer / Information Systems Research Intelligence`

### 3.1 Configuration

```json
{
  "schema_version": "research-profile-v0",
  "context": {
    "domain": "Computer / Information Systems",
    "disciplines": [
      "Information Systems",
      "Information Technology Governance",
      "Digital Government",
      "Enterprise Architecture"
    ],
    "description": "Reusable research context for studying governance, digital-government transformation, enterprise architecture, and related information-systems phenomena.",
    "language_preferences": ["en", "id"]
  },
  "terminology": {
    "preferred_terms": [
      "IT governance",
      "information technology governance",
      "e-government",
      "digital government",
      "enterprise architecture"
    ],
    "synonyms": {
      "IT governance": ["information technology governance", "ITG"],
      "e-government": ["electronic government", "e-gov"],
      "digital government": ["digital public administration", "digital governance"],
      "enterprise architecture": ["EA", "enterprise architecture management"]
    },
    "related_terms": [
      "digital transformation",
      "public-sector information systems",
      "IT alignment",
      "technology governance",
      "enterprise transformation",
      "architecture governance"
    ],
    "excluded_or_ambiguous_terms": []
  },
  "concepts": [
    {
      "key": "it-governance",
      "label": "IT Governance",
      "aliases": ["Information Technology Governance", "ITG"],
      "description": "Governance of information-technology decision rights, accountability, alignment, control, and value-related mechanisms.",
      "priority": "HIGH"
    },
    {
      "key": "digital-government",
      "label": "Digital Government",
      "aliases": ["e-Government", "Electronic Government"],
      "description": "Use and governance of digital technologies in government, public administration, and public-service transformation.",
      "priority": "HIGH"
    },
    {
      "key": "enterprise-architecture",
      "label": "Enterprise Architecture",
      "aliases": ["EA", "Enterprise Architecture Management"],
      "description": "Architectural principles, structures, models, and governance used to align organizational capabilities, processes, information, and technology.",
      "priority": "HIGH"
    }
  ],
  "watchlists": [
    {
      "key": "watch-it-governance",
      "label": "IT Governance developments",
      "target_type": "CONCEPT",
      "terms": ["IT governance", "information technology governance", "ITG"],
      "priority": "HIGH",
      "enabled": true
    },
    {
      "key": "watch-digital-government",
      "label": "Digital Government developments",
      "target_type": "CONCEPT",
      "terms": ["digital government", "e-government", "electronic government"],
      "priority": "HIGH",
      "enabled": true
    },
    {
      "key": "watch-enterprise-architecture",
      "label": "Enterprise Architecture developments",
      "target_type": "CONCEPT",
      "terms": ["enterprise architecture", "enterprise architecture management", "architecture governance"],
      "priority": "HIGH",
      "enabled": true
    }
  ],
  "seed_works": [],
  "theory_interests": [],
  "method_interests": [
    {
      "key": "method-case-study",
      "label": "Case Study",
      "aliases": ["case research"],
      "priority": "NORMAL"
    },
    {
      "key": "method-survey",
      "label": "Survey Research",
      "aliases": ["questionnaire survey"],
      "priority": "NORMAL"
    },
    {
      "key": "method-design-science",
      "label": "Design Science Research",
      "aliases": ["DSR", "design science"],
      "priority": "NORMAL"
    }
  ],
  "source_preferences": {
    "preferred_providers": [],
    "disabled_providers": [],
    "access_priority": ["FULL_TEXT", "ABSTRACT_ONLY", "METADATA_ONLY"],
    "notes": "Provider configuration remains external to scientific truth and must not contain credentials."
  },
  "advice_preferences": {
    "dimensions": {
      "gap_evidence_strength": 1.0,
      "novelty_potential": 1.0,
      "counter_evidence_risk": 1.0,
      "evidence_coverage": 1.0,
      "theoretical_significance": 1.0,
      "methodological_feasibility": 1.0,
      "rq_theory_method_alignment": 1.0,
      "practical_policy_significance": 1.0,
      "review_priority": 1.0
    },
    "scientific_acceptance_threshold": null
  },
  "discovery_preferences": {
    "languages": ["en", "id"],
    "publication_types": [],
    "time_horizon": "OPEN",
    "keyword_expansion": true,
    "exploratory_breadth": "BALANCED"
  },
  "notes": {
    "reference_profile": true,
    "scientific_status": "Configuration context only; not evidence and not a scientific conclusion."
  }
}
```

## 4. Profile B — Management / Organization Studies

Reference profile name:

`Management / Organization Studies Research Intelligence`

### 4.1 Configuration

```json
{
  "schema_version": "research-profile-v0",
  "context": {
    "domain": "Management / Organization Studies",
    "disciplines": [
      "Organization Studies",
      "Management",
      "Organizational Behaviour",
      "Human Resource and Capability Studies"
    ],
    "description": "Reusable research context for studying organizational resilience, human behaviour, human capability, and related management and organization phenomena.",
    "language_preferences": ["en", "id"]
  },
  "terminology": {
    "preferred_terms": [
      "organizational resilience",
      "resilient organization",
      "human behaviour",
      "human behavior",
      "human capability"
    ],
    "synonyms": {
      "organizational resilience": ["organisational resilience", "resilient organization", "resilient organisation"],
      "human behaviour": ["human behavior", "individual behaviour", "individual behavior"],
      "human capability": ["human capabilities", "employee capability", "workforce capability"]
    },
    "related_terms": [
      "adaptive capacity",
      "organizational adaptation",
      "employee resilience",
      "organizational behaviour",
      "dynamic capabilities",
      "human capital",
      "workforce capability"
    ],
    "excluded_or_ambiguous_terms": []
  },
  "concepts": [
    {
      "key": "organizational-resilience",
      "label": "Organizational Resilience",
      "aliases": ["Organisational Resilience", "Resilient Organization"],
      "description": "Organizational capacity or processes related to anticipating, absorbing, adapting to, responding to, and learning from disruption or adversity.",
      "priority": "HIGH"
    },
    {
      "key": "human-behaviour",
      "label": "Human Behaviour",
      "aliases": ["Human Behavior", "Individual Behaviour"],
      "description": "Human actions, responses, decisions, and behavioural mechanisms relevant to organizational contexts.",
      "priority": "HIGH"
    },
    {
      "key": "human-capability",
      "label": "Human Capability",
      "aliases": ["Human Capabilities", "Workforce Capability"],
      "description": "Individual or collective abilities, competencies, capacities, and related organizationally relevant human resources.",
      "priority": "HIGH"
    }
  ],
  "watchlists": [
    {
      "key": "watch-organizational-resilience",
      "label": "Organizational Resilience developments",
      "target_type": "CONCEPT",
      "terms": ["organizational resilience", "organisational resilience", "resilient organization", "resilient organisation"],
      "priority": "HIGH",
      "enabled": true
    },
    {
      "key": "watch-human-behaviour",
      "label": "Human Behaviour developments",
      "target_type": "CONCEPT",
      "terms": ["human behaviour", "human behavior", "organizational behaviour", "organizational behavior"],
      "priority": "HIGH",
      "enabled": true
    },
    {
      "key": "watch-human-capability",
      "label": "Human Capability developments",
      "target_type": "CONCEPT",
      "terms": ["human capability", "human capabilities", "workforce capability", "employee capability"],
      "priority": "HIGH",
      "enabled": true
    }
  ],
  "seed_works": [],
  "theory_interests": [],
  "method_interests": [
    {
      "key": "method-case-study",
      "label": "Case Study",
      "aliases": ["case research"],
      "priority": "NORMAL"
    },
    {
      "key": "method-survey",
      "label": "Survey Research",
      "aliases": ["questionnaire survey"],
      "priority": "NORMAL"
    },
    {
      "key": "method-qualitative-interview",
      "label": "Qualitative Interview",
      "aliases": ["semi-structured interview", "in-depth interview"],
      "priority": "NORMAL"
    }
  ],
  "source_preferences": {
    "preferred_providers": [],
    "disabled_providers": [],
    "access_priority": ["FULL_TEXT", "ABSTRACT_ONLY", "METADATA_ONLY"],
    "notes": "Provider configuration remains external to scientific truth and must not contain credentials."
  },
  "advice_preferences": {
    "dimensions": {
      "gap_evidence_strength": 1.0,
      "novelty_potential": 1.0,
      "counter_evidence_risk": 1.0,
      "evidence_coverage": 1.0,
      "theoretical_significance": 1.0,
      "methodological_feasibility": 1.0,
      "rq_theory_method_alignment": 1.0,
      "practical_policy_significance": 1.0,
      "review_priority": 1.0
    },
    "scientific_acceptance_threshold": null
  },
  "discovery_preferences": {
    "languages": ["en", "id"],
    "publication_types": [],
    "time_horizon": "OPEN",
    "keyword_expansion": true,
    "exploratory_breadth": "BALANCED"
  },
  "notes": {
    "reference_profile": true,
    "scientific_status": "Configuration context only; not evidence and not a scientific conclusion."
  }
}
```

## 5. Cross-Domain Generality Review

The two reference configurations intentionally differ in vocabulary, constructs, related terminology, watch targets, and method interests while preserving the same structural contract.

Current classification:

- Different domain names and disciplines → `PROFILE_CONFIG`.
- Different terminology and synonyms → `PROFILE_CONFIG`.
- Different concept instances → `PROFILE_CONFIG`.
- Different watchlists → `PROFILE_CONFIG`.
- Different method interests → `PROFILE_CONFIG`.
- Same advice-dimension structure → generic core capability.
- Same source-preference structure → generic core capability.
- Same versioning and HUMAN-authority rules → generic core capability.

No `CORE_GENERALIZATION`, `ADD_IN_CANDIDATE`, or `UNRESOLVED_GENERALITY` item is required merely to represent these two v0 reference configurations.

This conclusion applies only to representation at J3 v0. Later execution may reveal new generality exceptions; those are tracked rather than treated as project stops.

## 6. Scientific Integrity Rules for Reference Configurations

1. Configuration vocabulary is not scientific evidence.
2. Seed works, when later added, are discovery anchors and not privileged truth.
3. Watchlists prioritize attention and do not exclude unrelated valid evidence.
4. Theory and method interests guide recognition and comparison but do not predetermine scientific appropriateness.
5. Advice weights affect emphasis only and never create an automated acceptance verdict.
6. Domain descriptions and concept descriptions are HUMAN-provided context; evidence-backed claims must still follow the canonical evidence path.
7. Absence of a term from these profiles does not imply scientific irrelevance.
8. Contradictory and counter-evidence must remain discoverable regardless of profile preference.

## 7. Persistence Mapping

For each reference profile:

```text
research_profile
  id                 = stable opaque UUID
  name               = reference profile name
  status             = ACTIVE
  current_version_id = version v1 after version insert

research_profile_version
  id                  = stable opaque UUID
  profile_id          = parent profile UUID
  version_no          = 1
  summary             = initial J3 reference configuration
  configuration_jsonb = exact profile configuration
  supersedes_version_id = NULL
```

The initial bootstrap must therefore use a bounded transaction sequence that satisfies the circular current-version relationship:

```text
1. INSERT research_profile with current_version_id = NULL
2. INSERT research_profile_version v1
3. UPDATE research_profile.current_version_id = v1
4. COMMIT
```

Profile A and Profile B must use the same transaction mechanics.

## 8. Bootstrap Design Rules

The implementation bootstrap following this artifact must:

1. use deterministic UUIDs so verification is reproducible;
2. create only Profile A/B identities and their v1 configuration records;
3. not create ResearchProjects yet;
4. not create scientific Claims, EvidenceFragments, GapCandidates, Assessments, or HumanDecisions;
5. not label reference configuration as evidence;
6. not contain source credentials or secrets;
7. fail locally on duplicate identity or integrity violation rather than silently mutating existing records;
8. use one bounded database transaction;
9. be testable first outside production;
10. be production-reviewable before execution.

The bootstrap is reference/domain configuration data, not a schema migration.

## 9. Acceptance Criteria

This artifact is accepted when:

1. Profile A and Profile B conform to the same `research-profile-v0` top-level structure.
2. Domain differences are represented entirely as configuration values at this stage.
3. No scientific conclusion is embedded in the configuration.
4. No acceptance score threshold is configured.
5. The persistence mapping fits the existing canonical `research_profile` and `research_profile_version` schema without DDL changes.
6. Versioning remains append-oriented and traceable.
7. The next bootstrap can insert the two profiles deterministically without inserting synthetic scientific evidence.

## 10. Not Building Yet

This artifact does not yet implement:

- ResearchProject bootstrap;
- seed-work ingestion;
- source-provider credentials;
- discovery execution;
- literature crawling;
- canonical Concept/Theory/Method objects;
- Project-specific R0–R16 state;
- gap or novelty inference;
- advice computation;
- HUMAN review workflow;
- Dashboard integration;
- Telegram alerts.

These remain subsequent vertical-slice steps.

## 11. Next Artifact

The next implementation artifact should be a deterministic SQL bootstrap plus a verifier for Profile A/B using the same generic persistence mechanics:

```text
J3 Contract
  → J3 Reference Profile Configurations
  → Deterministic Profile A/B Bootstrap SQL
  → Bootstrap Verification
  → Disposable/isolated test
  → Production review
  → Production bootstrap
  → Real ResearchProject integration
```
