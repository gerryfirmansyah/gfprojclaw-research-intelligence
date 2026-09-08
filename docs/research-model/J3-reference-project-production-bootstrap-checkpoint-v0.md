# J3 Reference Project Production Bootstrap Checkpoint v0

Status: **ACCEPTED / PASS**

The deterministic A/B reference Project bootstrap at `db/fixtures/003_reference_projects.sql` was deployed successfully to production.

Observed deployment result: `BEGIN`, `INSERT 0 2`, `INSERT 0 2`, `UPDATE 2`, `COMMIT`.

Production verification confirmed exactly one ACTIVE version-1 Project beneath each reference Profile, both with `current_version_id` correctly pointing to version 1, `schema_version = research-project-v0`, and nullable `provisional_rq_text`.

Both domains use the same persistence mechanics and generic Project configuration shape. No synthetic Work, Claim, EvidenceFragment, GapCandidate, Assessment, ChangeEvent, or HumanDecision was created.

The read-only production verifier is `db/verify/003_reference_projects_verify.sql`.

Result: **ResearchProfile → ResearchProject → ResearchProjectVersion production bootstrap/read path PASS.**
