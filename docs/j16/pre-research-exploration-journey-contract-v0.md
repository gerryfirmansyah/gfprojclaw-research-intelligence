# Research Explorer / Pre-Research Exploration Journey Contract v0

Status: DESIGN CONTRACT — implementation foundation for GFPROJCLAW **Research Explorer** (internal Phase 0 / Pre-Research Exploration).

## Product role
GFPROJCLAW is a HUMAN–machine research companion. It may automate observation, discovery, organization, comparison, monitoring, explanation, alerts, Advice and Critic. It does not autonomously establish scientific meaning or produce HUMAN scientific decisions.

Core journey: **Explore → Decide → Research → Observe → Reconsider**.

## Research Explorer purpose
Research Explorer (internal Phase 0 / Pre-Research Exploration) helps a researcher understand the landscape before stabilizing a scope or research question. It MUST preserve enough provenance to explain how broad discovery, scope refinement, and HUMAN screening later produce the Project Corpus.

A small Project Corpus is an outcome to explain, never a target. A count such as three Works MUST NOT by itself establish that a field is narrow or that a research gap exists.

## Research Explorer stages
1. Research Interest — capture the initial problem, phenomenon, or interest without forcing a final RQ.
2. Domain Mapping — map parent and adjacent domains for HUMAN inspection.
3. Scope Ladder — represent L4 broad discipline, L3 adjacent domains, L2 parent domain, L1 immediate topic, and L0 exact scope.
4. Terminology & Query Families — preserve synonyms, academic terms, related concepts, and reproducible query families.
5. Broad Discovery — observe permitted sources and preserve source/query/run/time/access provenance.
6. Coverage Check — expose searched, inaccessible, degraded, and unsearched source/query/time space.
7. Deduplication & Landscape Mapping — reconcile unique Works while retaining raw source traceability.
8. Scope & Coverage Alerts — surface attention conditions with explanation and uncertainty, not conclusions.
9. Counter-search & Adjacent Exploration — actively inspect literature that could weaken the current interpretation.
10. HUMAN Scope Decision — HUMAN chooses zoom-in/out, terminology/source changes, continue, or defer, with rationale.
11. Re-discovery — compare a HUMAN-approved exploration change against the prior observation.
12. Transition to Research — only after HUMAN considers the current landscape sufficient for the intended purpose.

## Exploration loops
Research Explorer is iterative: **observe → explain → alert → HUMAN discussion → adjust → re-observe**.

After transition to research, Living Research Radar continues discovery. A material change may invite HUMAN to re-screen or revisit Research Explorer; it MUST NOT silently change the chosen research scope.

## Research Exploration Decision Record
The transition from exploration to research SHOULD retain: chosen scope; alternatives inspected; Scope Ladder position; query families; source and coverage state; landscape/corpus state at decision time; known limitations; HUMAN rationale; actor; decision timestamp; and optional superseded prior exploration decision.

This record is scientific governance context. Machine may prepare the context but MUST NOT create a HUMAN decision on the researcher's behalf.

## Corpus transition
The intended trace is:
Research Universe (source/query bounded; possibly UNKNOWN) → Discovery Observations → Deduplicated Corpus → Screening Corpus → HUMAN scope/relevance decisions → Project Corpus → Evidence Corpus → HUMAN-reviewed Evidence.

Pre-research discovery does not automatically promote a Work into Project Corpus or Evidence Corpus.

## Canonical Discovery Observation requirement
Each reproducible discovery observation SHOULD be able to identify: exploration session; Scope Ladder node; query family/query; literature source; discovery run/stage; observed source record; observation/retrieval time; access/retrieval state; and linkage to canonical Work when reconciliation exists.

The implementation MUST extend existing canonical structures rather than create an unrelated parallel corpus. Existing foundations include literature_source, source_record, work_source_record, project_work_relevance, coverage_context, coverage_source_state, continuous_pilot_run, and continuous_pilot_stage_run.

## HUMAN-verification invariant
Every meaningful aggregate must be traceable to exact members. HUMAN-facing explanation should answer what the state means, why it is shown, what canonical state/evidence supports it, what is uncertain/unavailable/not run, and what HUMAN may inspect next.

UNKNOWN, NOT_AVAILABLE, NOT_RECORDED, and NOT_RUN are valid states and MUST NOT be silently converted into negative scientific judgments.

## Acceptance sequence
1. Contract regression passes.
2. Canonical discovery/exploration schema is designed and reviewed.
3. Migration is validated without production scientific data mutation.
4. Read-only exploration projection exposes provenance and Scope Ladder.
5. Controlled real-source discovery validates the trace.
6. Research Alert uses the same canonical projection.
7. HUMAN visually verifies the exploration journey and wording.
8. Continuous production crawling remains a separate explicit operational gate.
