# Progressive Retrieval Contract v0

Research Explorer MUST distinguish provider-reported results from records actually retrieved.

## Invariant
Retrieval limit is an operational batch boundary, never a scientific boundary of the Research Universe.

## Required funnel
Provider reported → Retrieved → Deduplicated → Screened → Likely relevant / Uncertain / Likely out-of-scope → HUMAN reviewed → Project Corpus.

Every scientifically meaningful aggregate MUST expose its exact member set when canonical members exist. A provider-reported total without retrieved members is coverage metadata, not a corpus.

## Progressive retrieval
Retrieval proceeds in bounded pages/batches. Each run records source/provider, exact query, query fingerprint, retrieval time, provider-reported total when available, requested count, retrieved count, pagination/cursor state, errors/truncation, and member identifiers.

A batch of 10, 100, or any other size MUST NOT be labeled Research Universe. Unretrieved remainder remains explicit as NOT_RETRIEVED or coverage remaining; it is not classified as irrelevant.

Machine screening is advisory. LIKELY_RELEVANT, UNCERTAIN, and LIKELY_OUT_OF_SCOPE require inspectable reasons and do not promote records into Project Corpus or Evidence. HUMAN scientific judgment remains authoritative.

Stopping progressive retrieval requires an explicit operational or HUMAN-reviewed rationale. The system MUST NOT silently equate a retrieval cap, ranking cutoff, or apparent topic saturation with exhaustive scientific coverage.

scientific_decision=false
