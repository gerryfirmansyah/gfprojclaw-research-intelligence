# Research Scope & Coverage Alert Contract v0

Status: DESIGN CONTRACT — no scientific decision authority.

## Purpose
GFPROJCLAW is a research companion and continuous observation system, not an autonomous research-production machine. Research Alerts help a HUMAN notice when the current exploration may be too narrow, incomplete, stale, contradictory, or otherwise worth revisiting.

Core rule: **Automate observation continuously. Support reasoning interactively. Preserve scientific decisions for HUMAN.**

## Alert reasoning pattern
Every scientifically meaningful alert MUST expose:
1. **Observation** — what canonical machine-readable state changed or is currently visible.
2. **Explanation** — why the condition is being surfaced.
3. **Uncertainty** — what is UNKNOWN, NOT_AVAILABLE, NOT_RECORDED, or NOT_RUN.
4. **Options** — reversible exploration actions, not commands or scientific conclusions.
5. **HUMAN decision** — any scope/relevance/scientific interpretation remains explicit HUMAN authority.
6. **Re-observation** — after a HUMAN-approved exploration change, compare the new state with prior state.

## Scope Ladder
A project MAY define an inspectable exploration ladder:
- L0 — exact research question / most specific formulation
- L1 — immediate topic
- L2 — parent research domain
- L3 — adjacent domains / terminology
- L4 — broad disciplinary landscape

The ladder is an exploration aid, not a quality score. GFPROJCLAW MUST NOT automatically decide which level is scientifically correct.

## Initial alert families
- `SCOPE_COVERAGE_ATTENTION` — current corpus is small or sharply contracts across a Scope Ladder boundary, but cause is not established.
- `DISCOVERY_COVERAGE_INCOMPLETE` — source/query/time/access coverage is insufficient for a broad interpretation.
- `TERMINOLOGY_EXPANSION_OPTION` — alternate terms or adjacent concepts could materially change discovery breadth.
- `COUNTER_SEARCH_NOT_RUN` — a claim/gap/assessment is being considered without recorded counter-search.
- `SOURCE_BLIND_SPOT` — relevant source families are unsearched, inaccessible, degraded, or source-unique records indicate incomplete overlap.
- `EVIDENCE_THIN` — project/evidence/HUMAN-reviewed layers are too sparse to support a strong interpretation; this is not a rejection of the research direction.
- `LANDSCAPE_CHANGE` — newly observed literature may change the context of an existing research direction or assessment.
- `CONTRADICTION_ATTENTION` — newly observed evidence may challenge an existing claim/assessment and requires HUMAN inspection.

## Minimum evidence for a scope alert
A low paper count alone MUST NOT produce the conclusion `scope too narrow` or `research gap proven`.

Before a scope-related alert can offer a stronger interpretation, the UI SHOULD expose, where available:
- exact query/query family and Scope Ladder level;
- source(s) searched and source health/access limitations;
- observation/search time and temporal window;
- returned/observed source-record counts;
- deduplicated unique-work count;
- screening state/counts and reasons;
- Project Corpus, Evidence Corpus, and HUMAN-reviewed Evidence counts;
- terminology expansions attempted;
- adjacent-domain searches attempted;
- counter-search state;
- inaccessible/unsearched sources and other limitations.

Missing prerequisites MUST weaken the message and be displayed explicitly. Example: `Research Universe: UNKNOWN; counter-search: NOT_RUN; therefore the system cannot determine whether a small Project Corpus reflects a narrow scope, restrictive terminology, source coverage, access limitations, or a genuinely sparse literature.`

## HUMAN-facing alert shape
Each alert SHOULD answer:
- Apa yang saya lihat?
- Mengapa sistem menunjukkan ini?
- Apa dasar canonical/provenance-nya?
- Apa yang belum diketahui/dijalankan?
- Apa beberapa opsi eksplorasi yang dapat dipilih HUMAN?
- Apa yang perlu HUMAN periksa sebelum mengubah arah penelitian?

Raw IDs/JSON may be available for audit but MUST NOT substitute for this explanation.

## Automation boundary
Machine MAY automatically: discover/crawl permitted sources, preserve provenance, deduplicate conservatively, cluster, calculate descriptive coverage, detect changes, identify terminology candidates, surface possible contradictions, and prepare Advice/Critic.

Machine MUST NOT automatically: declare scope scientifically correct/incorrect, establish a research gap or novelty, establish relevance/causality/significance, accept/reject evidence scientifically, change the research question, promote a Work into scientific evidence without the canonical relationship/review path, or write a HUMAN scientific decision.

## Canonical fit with current schema
The existing model already provides useful foundations: `literature_source`, `source_record`, `work_source_record`, `project_work_relevance`, `coverage_context`, `coverage_source_state`, `continuous_pilot_run`, and `continuous_pilot_stage_run`.

However, current schema does not yet provide a first-class reproducible discovery observation linking an exact query/query-family/Scope Ladder level to each returned source record and run. `coverage_context.query_context_jsonb` can describe context and `continuous_pilot_stage_run.metrics_jsonb` can describe execution, but neither alone establishes record-level discovery provenance. Implementation MUST extend the canonical model rather than invent a parallel corpus model.

## UI destinations
Research Alert should eventually surface in:
- Today / What Needs My Attention;
- Research Coverage / corpus funnel and Scope Ladder;
- Telegram Radar as a concise alert with timestamp and observation window;
- Advice & Critic where relevant;
- HUMAN Review when a scientific decision is actually requested.

Every aggregate alert MUST drill down to its exact members/provenance where available.

## Initial production state
Until reproducible external discovery is implemented, the current small Project Corpus MUST be described conservatively. For the present Profile A state, Research Universe is UNKNOWN and counter-search is NOT_RUN; therefore no `scope too narrow` conclusion is permitted.

## Acceptance gates
1. Contract regression protects HUMAN authority and UNKNOWN/NOT_RUN semantics.
2. Canonical discovery provenance is modeled and migration-reviewed before production mutation.
3. Read-only projections expose source/query/run/Scope Ladder coverage and corpus funnel.
4. Alerts are explanation-first and member-traceable.
5. Telegram/dashboard use the same canonical alert projection.
6. Real-source controlled trial demonstrates broadening/narrowing without automatic scientific decisions.
7. HUMAN visually verifies usefulness and wording before production acceptance.
