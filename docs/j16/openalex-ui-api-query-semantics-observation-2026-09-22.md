# OpenAlex UI/API Query Semantics Observation — 2026-09-22

Status: CONTROLLED OBSERVATION — NON_PARITY_COMPARISON; no scientific decision.

## HUMAN observation
From HUMAN-provided screenshot, OpenAlex Web UI visibly showed query text `ai+digital government` and reported 4 works. The screenshot is evidence of the UI observation, but does not establish the exact internal query parsing, API request, filters, or complete identifiers for all four results.

## Machine observation
GFPROJCLAW read-only OpenAlex API preview used the literal query string `ai+digital government` through the OpenAlex Works `search` parameter.
- provider_reported_total: 368329
- requested_count: 10
- retrieved_count: 10
- canonical_write: false
- scientific_decision: false

## Comparison
Status: NON_PARITY_COMPARISON.
The visible HUMAN UI count (4) and API provider-reported total (368329) are not interchangeable. This observation demonstrates a material UI/API query-semantics difference that requires investigation before QUERY_PARITY can be claimed.

The machine's first 10 records are a bounded retrieval sample, not the Research Universe and not 10 relevant papers.

## Next verification
Determine how OpenAlex Web UI encodes/parses the visible `ai+digital government` input and reproduce materially equivalent API semantics. Only then compare exact member sets and compute overlap, HUMAN-only, and machine-only.
