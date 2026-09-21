# GFPROJCLAW Two-Stage Researcher Journey v0

Status: DESIGN CONTRACT — product architecture for researcher-facing GFPROJCLAW.

## Researcher journey

GFPROJCLAW has exactly two researcher stages:

1. **Research Explorer** — **Explore → Understand → Decide**.
2. **Research Copilot** — **Research → Review → Observe → Reconsider**.

**Admin Copilot is not a research stage.** It is the operational plane for authorized administration, service/provider health, scheduler and worker operations, backup/recovery, configuration, security, and audit.

## Stage 1 — Research Explorer

Research Explorer begins with an idea, problem, phenomenon, or research interest before a Research Project has been stabilized.

It may help HUMAN inspect the observed Research Universe, domain and adjacent-domain map, terminology, Scope Ladder L4–L0, query families, sources, Discovery Corpus, deduplication, landscape, coverage/blind spots, and counter-search.

Discovery is advisory and provenance-preserving. A discovered Work is not automatically Project Corpus or Evidence. Low counts do not prove narrow scope or a research gap.

The transition boundary is explicit:

**Research Explorer → HUMAN Scope Decision → Create/Transition Research Project → Research Copilot.**

Only HUMAN decides that the current exploration is sufficient for the intended purpose and authorizes the transition.

## Stage 2 — Research Copilot

Research Copilot is the workspace for a formed Research Project. It contains the project-facing journey such as Today, Research Journey, Research Opportunities, Evidence Explorer, Knowledge Evolution, Human Review, Research Coverage, and Living Research Radar.

Research Copilot must retain an inspectable link to the exploration provenance that led to the project: chosen scope, alternatives inspected, queries, sources, coverage limitations, corpus/landscape state, and HUMAN rationale when canonically recorded.

Living Research Radar may surface material new observations and invite HUMAN to reconsider scope. It MUST NOT silently modify project scope or scientific decisions.

## Reconsideration loop

The two stages are connected, not a one-way wizard:

**Research Explorer → Research Copilot → new observation/attention → HUMAN chooses whether to revisit Research Explorer → HUMAN decides whether any project change is warranted.**

Machine observation never substitutes for HUMAN scientific authority.

## Product surfaces

The researcher-facing entry experience SHOULD distinguish:
- **Research Explorer** — explore a research idea and understand the landscape.
- **Research Copilot** — continue an existing Research Project.

Research Explorer SHOULD be a product entry surface before the current project workspace, not merely another sidebar item inside Research Copilot.

## Operational plane

Admin Copilot remains separately accessible to authorized users but is outside the two-stage researcher journey. Administrative state and actions MUST NOT be presented as scientific decisions.

## Canonical implementation mapping

The current Phase 0 / Pre-Research Exploration engineering work, including canonical Discovery Observation, is the data foundation for **Research Explorer**.

Existing Research Copilot remains the project workspace. Migration or UI work MUST preserve the HUMAN-verification invariant and must not automatically promote discovery records into Project Corpus or Evidence Corpus.

## Acceptance implications

1. Research Explorer terminology is used for the researcher-facing Phase 0 product surface.
2. Pre-Research / Phase 0 may remain an internal architecture term.
3. Research Copilot is entered only in the context of a formed Research Project.
4. The transition is HUMAN-authorized and provenance-preserving.
5. Research Copilot can inspect its exploration origin when canonical state exists.
6. Reconsideration returns to Research Explorer without silently changing the project.
7. Admin Copilot is tested and documented as an operational plane, not research Stage 3.
