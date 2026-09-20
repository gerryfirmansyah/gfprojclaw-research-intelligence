# Daily Researcher Journey Acceptance v0

Status: PRE-J16 ACCEPTANCE PREREQUISITE

## Principle
The researcher experience is attention-driven, not system-status-driven. Telegram is a non-canonical radar; GFPROJCLAW Dashboard remains the inspection/review workspace and canonical state remains in PostgreSQL.

## Daily journey
1. Open GFPROJCLAW / receive Telegram Research Radar.
2. **What Changed?** Show changes from a defined observation window, including newly persisted works/claims, contradictory evidence, and Advice & Critic/ChangeEvent changes when canonically available.
3. **What Needs My Attention?** Surface exact NEEDS_REVIEW and CONTESTED members plus incomplete counter-search context.
4. **Why?** Open the affected Research Object and explanation/reasoning delta.
5. **Inspect Evidence.** Trace Claim -> EvidenceFragment -> Paper/source. ABSTRACT_ONLY remains explicit.
6. **Read Advice & Critic.** Explain weaknesses, falsification work, limitations, and uncertainty; never present a machine scientific verdict.
7. **HUMAN Review.** HUMAN explicitly decides/contests/requests further investigation through authorized review controls.
8. **Continue Research.** Subsequent discovery may use the new canonical state only through already-authorized processing boundaries.

## Traceability rule
Every displayed aggregate must be traceable to its exact canonical members. Counts must not be invented or inferred from unrelated operational logs. A zero/unknown/not-run state is shown honestly.

## Telegram boundary
Telegram sends attention summaries only. It must not expose crawler/service internals as the researcher-facing daily message, must not become canonical state, and delivery failure remains local. A Telegram message should direct HUMAN to GFPROJCLAW for evidence inspection and decisions.

## Pre-J16 PASS evidence
- canonical Dashboard projections for What Changed and attention items are reachable;
- Claim -> EvidenceFragment -> Paper trace is reachable;
- Advice & Critic is explainable and source/coverage limitations remain visible;
- HUMAN Review is explicit and HUMAN-only;
- Telegram can successfully deliver an attention-driven message without becoming canonical state;
- Telegram delivery configuration protects secrets;
- daily delivery scheduling is deterministic and observable;
- continuous-pilot activation remains independent and unauthorized by this acceptance.

## 2026-09-20 executable pre-J16 evidence
- `daily-attention?hours=24` now projects an explicit 24-hour window with exact members for new papers, new Claims, contradictory relationships, and Advice & Critic assessments; outstanding NEEDS_REVIEW/CONTESTED remains independent of the change window.
- Profile A observed: 1 new paper, 0 new Claim, 0 new contradictory relationship, 0 Advice & Critic change, 1 outstanding NEEDS_REVIEW, counter-search `NOT_RUN`.
- Profile B observed: 1 new paper, 0 new Claim, 0 new contradictory relationship, 0 Advice & Critic change, 4 outstanding NEEDS_REVIEW, coverage/counter-search unavailable.
- Projection explicitly returns `scientific_decision=false`.
- Attention-driven Telegram message successfully delivered as message id `323`.
- Daily Telegram timer is enabled/active for 08:00 WIB with `Persistent=true`; no-change days still send a completed-radar heartbeat while outstanding attention remains visible.
- Continuous-pilot timer remains `not-found` / `inactive` and is not authorized by this acceptance.
- Regression: `J15_CHANGE_EVENT_MEMBER_PROJECTION_PASS`, `DAILY_ATTENTION_PROJECTION_PASS`, JS syntax PASS, `git diff --check` PASS.

Status: IMPLEMENTATION PASS — HUMAN message visibility may be visually confirmed in Telegram; no scientific acceptance is implied by delivery.
