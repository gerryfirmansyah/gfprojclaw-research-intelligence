# Research Universe / Living SLR Contract v0

Status: DESIGN CONTRACT — accepted direction, implementation pending.

## Purpose
GFPROJCLAW is a Research Intelligence Platform that helps HUMAN researchers map a broad research universe, progressively narrow it, inspect evidence, and choose research directions. It provides options and traceability; it is not the sole authority and does not manufacture scientific certainty.

Core principle: **maximize research visibility, not manufactured research certainty.**

## Corpus layers
The UI and API MUST distinguish these layers; a count in one layer MUST NOT be presented as the size of another.

1. **Research Universe** — external records visible through searched sources/query families. This is source- and query-bounded, never assumed globally complete.
2. **Discovery Corpus** — records actually returned/observed by GFPROJCLAW discovery runs, retaining source/query/run provenance.
3. **Deduplicated Corpus** — canonical Works after identifier/metadata reconciliation. Raw source records remain traceable.
4. **Screening Corpus** — unique Works with machine relevance state/reason and/or HUMAN screening state. Machine screening is advisory.
5. **Project Corpus** — Works explicitly associated with a ResearchProject. This is what the current persisted-paper count represents.
6. **Evidence Corpus** — Works with inspectable EvidenceFragment/Claim and explicit EvidenceRelationship where relationship to a ResearchObject is asserted.
7. **HUMAN-reviewed Evidence** — evidence/claims/relationships with explicit HUMAN review/decision records.

A Work filtered from a narrower layer SHOULD remain available in broader layers with its state/reason; filtering must not silently erase research visibility.

## Living-SLR boundary
GFPROJCLAW MAY provide SLR-like research intelligence: reproducible search history, source coverage, deduplication, screening funnel, inclusion/exclusion reasoning, corpus characteristics, clusters, methods, theories, contexts, contradiction, and evidence traceability.

GFPROJCLAW MUST NOT call a corpus a completed SLR, systematic review, PRISMA-compliant review, or exhaustive literature set unless a declared protocol and its required HUMAN acceptance gates have actually been completed. A PRISMA-like funnel may be used only when explicitly labelled as provenance/workflow visualization rather than compliance.

## Coverage semantics
Every scientifically meaningful corpus count MUST answer, directly or by drill-down: count of what layer; which project/profile/intent; which sources; which query/query family and time window; when searched; records observed/attempted/retrieved; deduplication basis; NOT_RUN/NOT_AVAILABLE/degraded/inaccessible scope; machine screening and why; and what HUMAN actually reviewed.

Absence from a discovered/project corpus is never evidence of absence from the research universe.

## Source plurality and external benchmarks
Sources are complementary, not ground truth. OpenAlex, Crossref, ScienceDirect, Semantic Scholar, Scopus, Web of Science, arXiv, PubMed, DOAJ, institutional repositories, or future sources may have different scope/access. GFPROJCLAW SHOULD expose overlap, source-unique records, blind spots, degradation, and access limitations.

ScienceDirect is the first planned external benchmark for the Digital Government & AI trial. A ScienceDirect result count is a source/query-bounded benchmark, not the size of the global literature universe and not a scientific relevance judgment.

## Screening states
Machine states SHOULD distinguish at minimum: UNKNOWN/NOT_SCREENED, CANDIDATE, RELATED, LOW_RELEVANCE, OUT_OF_CURRENT_SCOPE. Reasons and model/rule provenance must be inspectable. HUMAN inclusion/exclusion/review remains explicit and separate; machine screening must never masquerade as HUMAN eligibility judgment.

## Provenance chain
Target inspectable path: Research Universe observation -> DiscoveryRun/SourceRecord -> canonical Work -> Project relevance/screening -> EvidenceFragment -> Claim -> EvidenceRelationship -> ResearchObject -> Assessment/Advice/Critic -> HUMAN Decision.

Not every record must reach every layer. Missing links must be visible rather than inferred.

## HUMAN interface acceptance
Primary corpus surfaces MUST show both count and scope. Replace ambiguous labels such as `Paper Tersimpan: 3` with language equivalent to `Project corpus: 3 persisted Works` plus coverage/completeness context. HUMAN must be able to drill from aggregates to exact members and source/query provenance.

## Initial implementation slice
1. Add explicit corpus-layer projection/count semantics without mutating scientific state.
2. Expose discovery/source/query provenance and completeness limitations on Research Coverage.
3. Add external benchmark model/projection; ScienceDirect first where lawful/technically available.
4. Show overlap/source-unique/undiscovered-to-project counts without automatically promoting Works into Project Corpus.
5. Run the Digital Government & AI trial and record HUMAN usefulness observations.
