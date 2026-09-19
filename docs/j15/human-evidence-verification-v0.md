# J15 HUMAN Evidence Verification v0

HUMAN trial feedback identified a closure gap: quality metadata was visible, but the researcher could not inspect the stored abstract/evidence text that underlies a Claim or relationship.

## Verification loop
Research Object -> Research Quality -> Evidence Verification -> stored EvidenceFragment -> extracted Claim -> explicit object relationship -> DOI/OpenAlex source -> HUMAN judgment.

## Runtime facts
Profile A has one object-linked canonical ABSTRACT_SEGMENT (1641 characters) for the public-governance gap candidate. It remains ABSTRACT_ONLY.

Profile B has four canonical ABSTRACT_SEGMENT records in project literature (917-1260 characters) but no EvidenceRelationship to the Investigation Direction. They therefore remain PROJECT_LITERATURE_ONLY and must not be presented as evidence for that direction.

Some project works have metadata/identifiers but no stored EvidenceFragment text. The UI must say so explicitly.

## UI rules
- Show complete stored EvidenceFragment text when present.
- Show access level next to the fragment.
- Show extracted Claim and its review state when present.
- Show semantic relationship and relationship review state only when explicitly canonical.
- Distinguish EXPLICIT_RELATIONSHIP from PROJECT_LITERATURE_ONLY.
- Provide DOI/OpenAlex links when canonical identifiers exist.
- Never describe ABSTRACT_ONLY as full text.
- Never fabricate text for metadata-only works.
- External source inspection is HUMAN verification context, not automatic scientific acceptance.

## Acceptance gap
J15 remains pending HUMAN browser verification that Profile A permits abstract-vs-Claim/relationship inspection and Profile B permits candidate-literature inspection without implying object evidence.
