# Profile / Project HUMAN Configuration v0

Status: IMPLEMENTATION PASS — pre-J16 prerequisite

Profile and Project configuration is now projected from canonical PostgreSQL state rather than the former illustrative Profile A/B cards. HUMAN may edit an active Profile or Project through explicit save controls. Every save creates a new immutable version row, links `supersedes_version_id`, advances `current_version_id`, records the HUMAN actor, and returns `scientific_decision=false`.

Profile configuration exposes name, summary, and configuration JSON. Project configuration exposes name, provisional research intent, provisional RQ, and project configuration JSON. These fields configure research context; they do not establish gap, novelty, theory, method, significance, causal mechanism, relevance, or scientific acceptance/rejection.

Profile A and B remain useful cross-domain regression fixtures, but the UI no longer represents their old illustrative content as production scientific state. A no-semantic-change Profile A write was executed solely to verify version persistence: version 1 -> 2, actor `J16_CONFIGURATION_REGRESSION`, with `scientific_decision=false`.

Regression evidence: `PROFILE_PROJECT_CONFIGURATION_PASS`, `J15_CHANGE_EVENT_MEMBER_PROJECTION_PASS`, `DAILY_ATTENTION_PROJECTION_PASS`; Cockpit API active after restart.
