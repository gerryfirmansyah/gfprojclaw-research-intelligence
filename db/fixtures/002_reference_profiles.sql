-- J3 reference profile bootstrap v0
-- Reference configuration data only. This is not scientific evidence.
-- Deterministic, bounded, non-idempotent by design: duplicate execution must fail locally.

BEGIN;

INSERT INTO research_profile (id, name, status, current_version_id, created_by)
VALUES
  ('3a000000-0000-4000-8000-000000000001', 'Computer / Information Systems Research Intelligence', 'ACTIVE', NULL, 'j3-reference-bootstrap-v0'),
  ('3b000000-0000-4000-8000-000000000001', 'Management / Organization Studies Research Intelligence', 'ACTIVE', NULL, 'j3-reference-bootstrap-v0');

INSERT INTO research_profile_version (
  id, profile_id, version_no, summary, configuration_jsonb, supersedes_version_id, created_by
)
VALUES
(
  '3a000000-0000-4000-8000-000000000011',
  '3a000000-0000-4000-8000-000000000001',
  1,
  'Initial J3 reference configuration for Computer / Information Systems',
  $json$
  {
    "schema_version": "research-profile-v0",
    "context": {
      "domain": "Computer / Information Systems",
      "disciplines": ["Information Systems", "Information Technology Governance", "Digital Government", "Enterprise Architecture"],
      "description": "Reusable research context for studying governance, digital-government transformation, enterprise architecture, and related information-systems phenomena.",
      "language_preferences": ["en", "id"]
    },
    "terminology": {
      "preferred_terms": ["IT governance", "information technology governance", "e-government", "digital government", "enterprise architecture"],
      "synonyms": {
        "IT governance": ["information technology governance", "ITG"],
        "e-government": ["electronic government", "e-gov"],
        "digital government": ["digital public administration", "digital governance"],
        "enterprise architecture": ["EA", "enterprise architecture management"]
      },
      "related_terms": ["digital transformation", "public-sector information systems", "IT alignment", "technology governance", "enterprise transformation", "architecture governance"],
      "excluded_or_ambiguous_terms": []
    },
    "concepts": [
      {"key":"it-governance","label":"IT Governance","aliases":["Information Technology Governance","ITG"],"description":"Governance of information-technology decision rights, accountability, alignment, control, and value-related mechanisms.","priority":"HIGH"},
      {"key":"digital-government","label":"Digital Government","aliases":["e-Government","Electronic Government"],"description":"Use and governance of digital technologies in government, public administration, and public-service transformation.","priority":"HIGH"},
      {"key":"enterprise-architecture","label":"Enterprise Architecture","aliases":["EA","Enterprise Architecture Management"],"description":"Architectural principles, structures, models, and governance used to align organizational capabilities, processes, information, and technology.","priority":"HIGH"}
    ],
    "watchlists": [
      {"key":"watch-it-governance","label":"IT Governance developments","target_type":"CONCEPT","terms":["IT governance","information technology governance","ITG"],"priority":"HIGH","enabled":true},
      {"key":"watch-digital-government","label":"Digital Government developments","target_type":"CONCEPT","terms":["digital government","e-government","electronic government"],"priority":"HIGH","enabled":true},
      {"key":"watch-enterprise-architecture","label":"Enterprise Architecture developments","target_type":"CONCEPT","terms":["enterprise architecture","enterprise architecture management","architecture governance"],"priority":"HIGH","enabled":true}
    ],
    "seed_works": [],
    "theory_interests": [],
    "method_interests": [
      {"key":"method-case-study","label":"Case Study","aliases":["case research"],"priority":"NORMAL"},
      {"key":"method-survey","label":"Survey Research","aliases":["questionnaire survey"],"priority":"NORMAL"},
      {"key":"method-design-science","label":"Design Science Research","aliases":["DSR","design science"],"priority":"NORMAL"}
    ],
    "source_preferences": {"preferred_providers":[],"disabled_providers":[],"access_priority":["FULL_TEXT","ABSTRACT_ONLY","METADATA_ONLY"],"notes":"Provider configuration remains external to scientific truth and must not contain credentials."},
    "advice_preferences": {
      "dimensions": {"gap_evidence_strength":1.0,"novelty_potential":1.0,"counter_evidence_risk":1.0,"evidence_coverage":1.0,"theoretical_significance":1.0,"methodological_feasibility":1.0,"rq_theory_method_alignment":1.0,"practical_policy_significance":1.0,"review_priority":1.0},
      "scientific_acceptance_threshold": null
    },
    "discovery_preferences": {"languages":["en","id"],"publication_types":[],"time_horizon":"OPEN","keyword_expansion":true,"exploratory_breadth":"BALANCED"},
    "notes": {"reference_profile":true,"scientific_status":"Configuration context only; not evidence and not a scientific conclusion."}
  }
  $json$::jsonb,
  NULL,
  'j3-reference-bootstrap-v0'
),
(
  '3b000000-0000-4000-8000-000000000011',
  '3b000000-0000-4000-8000-000000000001',
  1,
  'Initial J3 reference configuration for Management / Organization Studies',
  $json$
  {
    "schema_version": "research-profile-v0",
    "context": {
      "domain": "Management / Organization Studies",
      "disciplines": ["Organization Studies", "Management", "Organizational Behaviour", "Human Resource and Capability Studies"],
      "description": "Reusable research context for studying organizational resilience, human behaviour, human capability, and related management and organization phenomena.",
      "language_preferences": ["en", "id"]
    },
    "terminology": {
      "preferred_terms": ["organizational resilience", "resilient organization", "human behaviour", "human behavior", "human capability"],
      "synonyms": {
        "organizational resilience": ["organisational resilience", "resilient organization", "resilient organisation"],
        "human behaviour": ["human behavior", "individual behaviour", "individual behavior"],
        "human capability": ["human capabilities", "employee capability", "workforce capability"]
      },
      "related_terms": ["adaptive capacity", "organizational adaptation", "employee resilience", "organizational behaviour", "dynamic capabilities", "human capital", "workforce capability"],
      "excluded_or_ambiguous_terms": []
    },
    "concepts": [
      {"key":"organizational-resilience","label":"Organizational Resilience","aliases":["Organisational Resilience","Resilient Organization"],"description":"Organizational capacity or processes related to anticipating, absorbing, adapting to, responding to, and learning from disruption or adversity.","priority":"HIGH"},
      {"key":"human-behaviour","label":"Human Behaviour","aliases":["Human Behavior","Individual Behaviour"],"description":"Human actions, responses, decisions, and behavioural mechanisms relevant to organizational contexts.","priority":"HIGH"},
      {"key":"human-capability","label":"Human Capability","aliases":["Human Capabilities","Workforce Capability"],"description":"Individual or collective abilities, competencies, capacities, and related organizationally relevant human resources.","priority":"HIGH"}
    ],
    "watchlists": [
      {"key":"watch-organizational-resilience","label":"Organizational Resilience developments","target_type":"CONCEPT","terms":["organizational resilience","organisational resilience","resilient organization","resilient organisation"],"priority":"HIGH","enabled":true},
      {"key":"watch-human-behaviour","label":"Human Behaviour developments","target_type":"CONCEPT","terms":["human behaviour","human behavior","organizational behaviour","organizational behavior"],"priority":"HIGH","enabled":true},
      {"key":"watch-human-capability","label":"Human Capability developments","target_type":"CONCEPT","terms":["human capability","human capabilities","workforce capability","employee capability"],"priority":"HIGH","enabled":true}
    ],
    "seed_works": [],
    "theory_interests": [],
    "method_interests": [
      {"key":"method-case-study","label":"Case Study","aliases":["case research"],"priority":"NORMAL"},
      {"key":"method-survey","label":"Survey Research","aliases":["questionnaire survey"],"priority":"NORMAL"},
      {"key":"method-qualitative-interview","label":"Qualitative Interview","aliases":["semi-structured interview","in-depth interview"],"priority":"NORMAL"}
    ],
    "source_preferences": {"preferred_providers":[],"disabled_providers":[],"access_priority":["FULL_TEXT","ABSTRACT_ONLY","METADATA_ONLY"],"notes":"Provider configuration remains external to scientific truth and must not contain credentials."},
    "advice_preferences": {
      "dimensions": {"gap_evidence_strength":1.0,"novelty_potential":1.0,"counter_evidence_risk":1.0,"evidence_coverage":1.0,"theoretical_significance":1.0,"methodological_feasibility":1.0,"rq_theory_method_alignment":1.0,"practical_policy_significance":1.0,"review_priority":1.0},
      "scientific_acceptance_threshold": null
    },
    "discovery_preferences": {"languages":["en","id"],"publication_types":[],"time_horizon":"OPEN","keyword_expansion":true,"exploratory_breadth":"BALANCED"},
    "notes": {"reference_profile":true,"scientific_status":"Configuration context only; not evidence and not a scientific conclusion."}
  }
  $json$::jsonb,
  NULL,
  'j3-reference-bootstrap-v0'
);

UPDATE research_profile
SET current_version_id = CASE id
  WHEN '3a000000-0000-4000-8000-000000000001'::uuid THEN '3a000000-0000-4000-8000-000000000011'::uuid
  WHEN '3b000000-0000-4000-8000-000000000001'::uuid THEN '3b000000-0000-4000-8000-000000000011'::uuid
END
WHERE id IN (
  '3a000000-0000-4000-8000-000000000001'::uuid,
  '3b000000-0000-4000-8000-000000000001'::uuid
);

COMMIT;
