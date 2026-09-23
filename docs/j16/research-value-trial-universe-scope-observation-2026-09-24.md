# Research Value Trial — Universe Scope Observation 2026-09-24

Status: **TRIAL / NON-CANONICAL / COUNT-ONLY**. No records from this observation are promoted to Project Corpus or Evidence.

## Question

Can explicit research boundaries reveal a useful scope ladder before GFPROJCLAW retrieves and characterizes a corpus?

HUMAN-selected time window: **2022–2026**.

## Provider observations

| Query option | OpenAlex reported count | Crossref reported count |
|---|---:|---:|
| AI digital government | 296,878 | 1,191,351 |
| artificial intelligence public administration | 288,456 | 1,348,982 |
| AI governance public sector | 158,511 | 1,222,351 |
| algorithmic decision making public administration | 201,536 | 1,128,747 |
| explainable AI public administration | 193,424 | 1,112,843 |
| artificial intelligence digital government public administration | 103,599 | 2,051,828 |
| "digital government" "artificial intelligence" | 10,996 | 1,436,420 |
| "digital government" AI | 10,260 | 1,191,351 |
| "public administration" "artificial intelligence" | 46,365 | 1,348,982 |
| "public sector" "AI governance" | 5,789 | 1,222,351 |
| "public administration" "algorithmic decision making" | 2,667 | 1,128,747 |

These are **provider-reported matches under each provider's query semantics**, not counts of scientifically relevant literature. They MUST NOT be added together.

## What the trial reveals

1. The 2022–2026 time boundary alone does not make the broad free-text query operationally small.
2. OpenAlex phrase-sensitive query options create materially smaller bounded universes: 10,996; 10,260; 5,789; and 2,667 in the examples above.
3. Crossref `query.bibliographic` remains extremely broad and does not narrow in the same way. Crossref counts therefore cannot be treated as parity measurements of the OpenAlex query scopes.
4. Provider query semantics are part of the observed universe. A displayed query string alone is insufficient provenance.
5. The 5,789- and 2,667-work OpenAlex scopes are plausible **whole-metadata-retrieval trial candidates**. This is an operational statement only, not a recommendation that either scope is scientifically preferable.

## Year distribution — OpenAlex

### "public sector" "AI governance"
- 2022: 202
- 2023: 383
- 2024: 750
- 2025: 1,908
- 2026: 2,546
- 2022–2026 total: 5,789

### "public administration" "algorithmic decision making"
- 2022: 193
- 2023: 295
- 2024: 367
- 2025: 796
- 2026: 1,016
- 2022–2026 total: 2,667

The increase toward 2025–2026 is an observation of provider-reported matches. It is not by itself evidence of scientific importance, quality, novelty, or a research gap.

## Draft researcher-facing advice pattern

Instead of saying **"this is the correct scope"**, GFPROJCLAW should say:

> This option currently maps to N provider-reported works for 2022–2026 under the stated provider/query semantics. At this size, whole-metadata retrieval is / is not yet selected for the trial. You may inspect this scope, narrow it further, broaden it, or compare another branch. The system has not determined scientific relevance.

The HUMAN should be able to see how the universe changes when moving between query/scope options before deciding where deeper exploration should begin.

## Next trial boundary

Do not characterize the earlier top-198 retrieval as the Research Universe. Before MAP/WHY, choose a HUMAN-inspected bounded scope and perform whole-bounded progressive metadata retrieval, preserving pagination and exact members.
