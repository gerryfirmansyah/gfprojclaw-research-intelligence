# HUMAN–Machine Discovery Benchmark Contract v0

Status: DESIGN CONTRACT — verification instrument; no scientific decision authority.

## Purpose
GFPROJCLAW MUST make machine discovery empirically comparable with a HUMAN-performed search. The benchmark measures reproducibility, coverage differences, and retrieval discrepancies. It does not establish which side is scientifically correct and does not treat either HUMAN or machine as global Research Universe ground truth.

## Comparison unit
A comparison is valid only within an explicit scope:
- project/profile and research interest;
- provider/source and UI/API channel;
- exact query expression;
- search timestamp or declared comparison window;
- filters, sort, pagination/page size, result cap, and other material parameters;
- provider-reported total when available;
- records actually captured/retrieved;
- identifier basis used for reconciliation.

If material search conditions differ, label the result NON_PARITY_COMPARISON rather than treating it as an exact replication test.

## HUMAN observation
Record source/provider and channel, exact query, searched_at, filters/parameters, provider_reported_total, human_captured_count, captured identifiers/export where available, screenshot/export evidence where available, and limitations. A manually observed provider count without member identifiers can support count comparison but cannot establish member-level overlap.

## Machine observation
Record source/provider and API/channel, exact canonical HUMAN-approved query, query fingerprint, project/project-version, requested limit/page strategy, provider_reported_total when exposed, retrieved_count, unique/reconciled count when available, observation time, errors/truncation/degradation, and exact retrieved member identifiers.

A bounded retrieval such as limit=10 MUST be displayed as retrieved_count=10, never as Research Universe=10 or provider_reported_total=10.
## Comparison outputs
Where member identifiers exist on both sides, expose human_count, machine_count, overlap_count (HUMAN intersection Machine), human_only_count, machine_only_count, and exact member lists for all sets. Where only provider-reported counts exist, expose count deltas but mark overlap NOT_AVAILABLE. Every aggregate MUST drill down to exact members when canonical member data exists.

## Interpretation
Differences are audit targets, not automatic errors. Possible explanations include query translation, API versus web behavior, indexing time, provider updates, filters, pagination, ranking, export limits, access/licensing, identifier normalization, or crawler defects. GFPROJCLAW may surface these as hypotheses/options but MUST NOT silently decide the cause.

The benchmark MUST NOT automatically declare HUMAN wrong, declare machine superior, call either result exhaustive, establish relevance/eligibility/gap/novelty/significance/evidence, promote discovered Works into Project Corpus/Evidence, or write a HUMAN scientific decision.

## Benchmark modes
1. QUERY_PARITY — same provider and materially equivalent query/filters; tests retrieval reproducibility.
2. COVERAGE_COMPARISON — different providers/channels; examines overlap and source blind spots.
3. SCREENING_COMPARISON — compares machine advisory screening with explicit HUMAN screening; scientific inclusion/exclusion remains HUMAN authority.

## Researcher-facing presentation
The primary UI should answer:
1. Apa yang dicari HUMAN dan mesin?
2. Apakah kondisi pencariannya benar-benar comparable?
3. Provider melaporkan berapa hasil?
4. HUMAN menangkap berapa; mesin mengambil berapa?
5. Apa yang ditemukan keduanya, HUMAN-only, dan machine-only?
6. Paper persis apa yang membentuk setiap angka?
7. Apa keterbatasan/perbedaan kondisi pencarian?
8. Apa yang perlu HUMAN periksa berikutnya?

Raw UUID/JSON belongs in collapsed canonical provenance, not as the primary explanation.
## First controlled trial
Start with one project, one HUMAN-approved query, and one source (OpenAlex). Record a HUMAN OpenAlex web search and a machine OpenAlex API search as separate observations. Do not claim parity until query/filters/time/channel differences are documented. Compare provider-reported totals and captured members separately.

The current machine preview of 10 OpenAlex records is a bounded retrieval sample. Until provider total is captured, it MUST remain retrieved_count=10; provider_reported_total=NOT_AVAILABLE, not a Research Universe size.

## Acceptance gates
1. Contract regression protects parity semantics and HUMAN authority.
2. Machine fetch envelope exposes provider total independently from retrieved count where provider supplies it.
3. HUMAN observation can be recorded without converting it into a scientific decision.
4. Comparison projection exposes parity state, counts, overlap, HUMAN-only, machine-only, limitations, and exact members.
5. Controlled OpenAlex HUMAN-vs-machine trial is visually inspected by HUMAN.
6. Only after acceptance may the pattern be generalized to additional sources.
