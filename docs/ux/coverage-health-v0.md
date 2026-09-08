# Coverage & Health v0

Status: **J1 ACTIVE — Low-Fidelity UX Specification**

## 1. Purpose

Coverage & Health tells the HUMAN two different but related things:

1. **Coverage:** how much of the relevant research landscape GFPROJCLAW has actually been able to observe and inspect.
2. **Health:** whether the technical capabilities used to discover, retrieve, extract, and update that evidence are currently operating normally.

The screen exists to prevent operational limitations from becoming false scientific certainty.

The governing epistemic principle is:

> **Absence of discovered evidence is not evidence of absence.**

The governing operational principle is:

> **Source or component degradation reduces observable coverage; it does not automatically invalidate existing evidence and does not stop unrelated healthy research work.**

## 2. What Coverage & Health Is Not

Coverage & Health must not become:

- a scientific PASS/FAIL gate;
- a requirement that every source be healthy before research continues;
- a global network enable/disable control plane;
- an engineering incident approval queue;
- a raw crawler-log dashboard;
- a claim that 100% of the world's literature has been covered;
- a mechanism that converts source availability directly into scientific truth;
- a reason to discard already valid evidence merely because a source later becomes unavailable.

## 3. Cross-Domain Requirement

The same Coverage & Health model must support both reference profiles:

- **Profile A — Computer / Information Systems**
- **Profile B — Management / Organization Studies**

A profile may use different sources, vocabulary, watchlists, publication venues, or search strategies. The core concepts of source health, evidence access, search coverage, freshness, degradation, and scientific impact remain generic.

Source-specific adapters or specialized domain sources may become ADR-001 add-ins without changing the core coverage semantics.

## 4. Primary HUMAN Questions

The screen should help answer:

- Which literature sources are currently available?
- Which are degraded or unavailable?
- What research coverage may be affected?
- How much evidence is FULL_TEXT, ABSTRACT_ONLY, or METADATA_ONLY?
- How fresh is the discovery/search state?
- Which active watchlists/projects may have incomplete coverage?
- Does an operational problem materially affect a current scientific assessment?
- Which scientific conclusions should be interpreted more cautiously because coverage is limited?
- Is the system still processing healthy sources and jobs?
- What needs engineering attention versus HUMAN scientific attention?

## 5. Status Vocabulary

For source/component operational state, v0 uses a simple vocabulary:

`HEALTHY | DEGRADED | BACKOFF | DISABLED | ATTENTION`

### HEALTHY

The capability is operating within expected conditions.

### DEGRADED

The capability is usable but incomplete, unstable, rate-limited, partially failing, or otherwise reducing expected coverage.

### BACKOFF

The system is intentionally waiting before retrying a source or operation, for example after rate limiting or bounded failures.

### DISABLED

The capability/source is intentionally not being used. The reason should be visible.

### ATTENTION

A persistent or material operational issue requires engineering/operator inspection.

These are operational states, not scientific verdicts.

## 6. Top-Level Screen

```text
COVERAGE & HEALTH
Profile: [ ... ]   Project: [ ... ]

Overall Research Coverage Context: DEGRADED
Reason: one discovery source is rate-limited and full-text access is incomplete.

SOURCE HEALTH
OpenAlex              HEALTHY
Crossref              HEALTHY
Semantic Scholar      DEGRADED
[Other configured]    ...

EVIDENCE ACCESS
Full text             48%
Abstract available    87%
Metadata              100% of discovered corpus

FRESHNESS
Last discovery cycle  [...]
Watchlists updated    [...]

SCIENTIFIC IMPACT
Novelty search        Coverage limited
Gap falsification     Coverage limited
Existing evidence     Preserved
Healthy crawling      Continuing
```

Percentages must always have a defined denominator and should never imply coverage of all possible world literature.

## 7. Coverage Dimensions

Coverage is multidimensional. J1 should not collapse it into one opaque score.

Useful dimensions include:

- **Source Coverage** — which configured sources were searched successfully.
- **Query/Watchlist Coverage** — which planned searches/watchlists executed.
- **Temporal Coverage** — publication periods represented/searched.
- **Evidence Access Coverage** — FULL_TEXT / ABSTRACT_ONLY / METADATA_ONLY.
- **Extraction Coverage** — which accessible records have been processed for relevant research objects.
- **Counter-Search Coverage** — how thoroughly attempts were made to challenge gaps/novelty.
- **Project Relevance Coverage** — which active RQs/watchlists received current discovery.
- **Freshness** — how recently relevant searches and evidence were updated.

Not every dimension must be numerically scored.

## 8. Denominator Discipline

Any percentage must state what it measures.

Good:

```text
Full text available: 48% of 312 normalized works currently in this project corpus.
```

Bad:

```text
Literature coverage: 48%
```

The latter falsely suggests that the system knows the total universe of relevant literature.

## 9. Access-Level Coverage

Coverage & Health must align with Evidence Explorer:

`FULL_TEXT | ABSTRACT_ONLY | METADATA_ONLY`

Example:

```text
Project corpus: 312 normalized works

FULL_TEXT       150  (48.1%)
ABSTRACT_ONLY   121  (38.8%)
METADATA_ONLY    41  (13.1%)
```

These percentages describe the discovered project corpus, not all literature that exists.

## 10. Source Health Detail

A source detail view should explain:

```text
Semantic Scholar — DEGRADED

Last successful request: [...]
Current condition: rate limiting / intermittent server errors
Backoff: active
Last healthy period: [...]

Affected:
- discovery completeness
- citation expansion
- prior-solution search coverage

Not affected:
- previously stored evidence
- OpenAlex discovery
- Crossref metadata
- unrelated extraction jobs

Scientific implication:
Novelty and gap-falsification searches may currently be less complete.
```

The HUMAN sees scientific consequence without being flooded with raw HTTP logs.

## 11. Local Failure Principle

Operational failures must be contained at the smallest responsible scope:

`request → paper → job → source → agent/component`

Examples:

- one failed request retries locally;
- one inaccessible paper becomes limited-access or locally failed;
- one extraction failure is quarantined/retried without stopping other papers;
- one source enters DEGRADED/BACKOFF while other sources continue;
- one specialized add-in failure affects only the capability it provides.

No source failure creates a global research lock.

## 12. Partial Daily Success

A daily research cycle may be scientifically useful even when some components are degraded.

Example:

```text
DAILY CYCLE — PARTIAL COVERAGE

OpenAlex              completed
Crossref              completed
Semantic Scholar      degraded
Evidence extraction   91/94 completed
3 papers              locally quarantined/retry pending

Result:
Valid new evidence was ingested.
Knowledge evolution updated where evidence supports it.
Coverage limitation disclosed.
Healthy work continues.
```

`PARTIAL COVERAGE` is preferable to declaring the whole research cycle failed when useful valid work was completed.

## 13. Scientific Impact Mapping

Operational degradation should be translated into bounded scientific consequences.

Example:

```text
SOURCE DEGRADATION
Semantic Scholar → DEGRADED

POSSIBLE COVERAGE IMPACT
Citation expansion ↓
Adjacent-work discovery ↓
Prior-solution discovery ↓

RESEARCH OBJECTS MOST AFFECTED
GAP-014 — novelty challenge
GAP-021 — counter-search
R12 — novelty challenge

WHAT DOES NOT FOLLOW
GAP-014 is not automatically strengthened.
Existing evidence does not become invalid.
HUMAN decisions are not automatically reversed.
```

This distinction is central to the architecture.

## 14. Scientific Coverage Context in Other Screens

Coverage is not confined to the Coverage & Health page.

Important scientific screens should receive compact coverage context.

### Today

```text
Coverage: DEGRADED
One source unavailable; novelty-related changes may be incomplete.
```

### Gap–Solution Workspace

```text
Prior-solution search coverage: LIMITED
Absence of discovered solution is not evidence that no solution exists.
```

### Evidence Explorer

```text
Access: ABSTRACT_ONLY
Do not interpret as full-text passage evidence.
```

### Knowledge Evolution

```text
Assessment changed under improved full-text coverage.
Previous coverage: 42%
Current coverage: 61% of project corpus.
```

### Human Review

```text
Coverage limitation: prior-solution search incomplete.
Consider NEED MORE EVIDENCE.
```

## 15. Coverage-Aware Advice

Advice dimensions may incorporate coverage context, but the system should expose it separately rather than hiding it inside a score.

Example:

```text
Novelty Potential: 74
Evidence Coverage: LIMITED

Why limited?
- one discovery source degraded
- 39% of relevant corpus abstract-only
- adjacent-domain counter-search incomplete
```

A high advice score with weak coverage should look visibly different from a high score with broad evidence access.

## 16. Coverage and Knowledge Evolution

Coverage itself evolves and must be historically interpretable.

Example:

```text
Sep 01
Sources: OpenAlex + Crossref
Full text: 42% of project corpus

Sep 08
Sources: OpenAlex + Crossref + Semantic Scholar
Full text: 61% of project corpus

Scientific consequence:
New prior solutions discovered; novelty assessment changed.
```

Knowledge Evolution should preserve the coverage context that existed at each assessment point.

## 17. Coverage and Human Decisions

A HumanDecision should preserve relevant coverage context.

Example:

```text
HUMAN: ACCEPT DIRECTION
Date: Sep 04

Coverage at decision time:
OpenAlex HEALTHY
Crossref HEALTHY
Semantic Scholar DEGRADED
Full text: 48% of project corpus

Known limitation:
Prior-solution search may be incomplete.
```

Later improvements in coverage may trigger a review suggestion but do not rewrite the historical decision.

## 18. Operational Attention vs Scientific Attention

Coverage & Health is the primary surface for operational attention.

Examples:

```text
Operational:
Semantic Scholar repeatedly rate-limited → ATTENTION
Parser failure for 3 papers → local engineering attention
Extraction worker backlog → operational attention
```

Human Review receives an item only when the scientific consequence matters, for example:

```text
Scientific:
R12 Novelty Challenge — NEEDS ATTENTION
Reason: prior-solution search coverage has been materially incomplete for 5 days.
```

This prevents the researcher from becoming the operator of routine engineering recovery.

## 19. Automatic Engineering Recovery

Routine engineering recovery should be automatic and bounded where safe:

- retry transient request failures;
- apply source-specific backoff;
- resume incremental jobs;
- restart idempotent worker work;
- quarantine repeatedly failing items;
- continue healthy queues.

Escalation occurs when bounded recovery is exhausted or coverage impact becomes material.

Scientific authorization is not required to resume routine technical crawling.

## 20. Source Independence

Each literature source is independently observable and recoverable.

The system should avoid a single global source-success condition such as:

```text
ALL_SOURCES_PASS == true
```

Instead:

```text
OpenAlex           HEALTHY
Crossref           HEALTHY
Semantic Scholar   BACKOFF
Specialized Source DISABLED
```

Research processing continues with explicit coverage disclosure.

## 21. Profile A Example

```text
PROFILE A — Computer / Information Systems
Project: Cross-agency digital-government governance study

SOURCE COVERAGE
OpenAlex              HEALTHY
Crossref              HEALTHY
Semantic Scholar      DEGRADED

PROJECT CORPUS
FULL_TEXT             52%
ABSTRACT_ONLY         36%
METADATA_ONLY         12%

WATCHLIST IMPACT
IT governance         current
Digital government    current
Enterprise architecture citation expansion limited

SCIENTIFIC IMPACT
GAP-014 prior-solution search: LIMITED
R12 novelty challenge: interpret cautiously

HEALTHY WORK
OpenAlex/Crossref crawling and evidence extraction continue.
```

## 22. Profile B Example

```text
PROFILE B — Management / Organization Studies
Project: Human capability and organizational resilience study

SOURCE COVERAGE
OpenAlex              HEALTHY
Crossref              HEALTHY
Semantic Scholar      DEGRADED

PROJECT CORPUS
FULL_TEXT             44%
ABSTRACT_ONLY         43%
METADATA_ONLY         13%

WATCHLIST IMPACT
Organizational resilience   current
Human behaviour             current
Human capability citation expansion limited

SCIENTIFIC IMPACT
GAP-014 competing-mechanism search: LIMITED
R6/R12 interpretation: use coverage caution

HEALTHY WORK
Other source discovery and evidence extraction continue.
```

The operational and epistemic semantics remain identical.

## 23. Cross-Domain Generality Matrix

| Coverage Capability | Profile A | Profile B | Expected Resolution |
|---|---|---|---|
| Source health | same state model | same state model | Core generic |
| Access level | full/abstract/metadata | full/abstract/metadata | Core generic |
| Watchlist coverage | ITGov/eGov/EA | resilience/behaviour/capability | Profile config |
| Corpus denominator | project corpus | project corpus | Core generic |
| Scientific impact | gap/theory/method/etc. | gap/theory/method/etc. | Core generic |
| Specialized source | computing-specific if needed | management-specific if needed | Source adapter/add-in |
| Recovery semantics | local/non-blocking | local/non-blocking | Core generic |

Any mismatch follows ADR-001 and does not globally stop development.

## 24. Low-Fidelity Layout

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ COVERAGE & HEALTH                                                          │
│ Profile [A/B]  Project [...]                                                │
├───────────────────────┬────────────────────────┬────────────────────────────┤
│ SOURCE HEALTH         │ EVIDENCE COVERAGE      │ SCIENTIFIC IMPACT          │
│                       │                        │                            │
│ OpenAlex      HEALTHY │ Full text       48%    │ GAP-014                    │
│ Crossref      HEALTHY │ Abstract        39%    │ prior-solution coverage    │
│ S2          DEGRADED  │ Metadata        13%    │ LIMITED                    │
│                       │                        │                            │
│ [Open source detail]  │ Denominator:           │ R12 NEEDS CAUTION          │
│                       │ 312 project works      │                            │
│                       │                        │ Existing evidence preserved│
├───────────────────────┴────────────────────────┴────────────────────────────┤
│ HEALTHY WORK CONTINUES                                                      │
│ OpenAlex discovery • Crossref metadata • 91 extraction jobs completed      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 25. Telegram Escalation Boundary

Coverage & Health will later feed Telegram Research Radar, but Telegram should receive only meaningful degradation.

Good alert:

```text
Coverage degraded for Profile A:
Semantic Scholar has remained unavailable and prior-solution discovery for GAP-014 is materially affected.
Healthy sources continue.
```

Bad alert stream:

```text
HTTP 429
retry 1
retry 2
worker retry
request timeout
```

Raw engineering noise stays in operational logs/observability.

## 26. No False Completeness

The UI must avoid labels such as:

- `Literature search complete`
- `100% research coverage`
- `No prior solution exists`
- `No contradictory evidence exists`

unless the statement is explicitly bounded to a defined corpus/search execution and phrased accordingly.

Preferred language:

- `No prior solution discovered in the current search coverage.`
- `No contradictory evidence identified in the currently processed corpus.`
- `All configured searches for this cycle completed.`

## 27. Reproducibility Context

Coverage state should eventually be reconstructable from:

- Research Profile version;
- Project/watchlist configuration;
- source configuration;
- search manifests;
- execution timestamps;
- source health history;
- normalized corpus;
- access levels;
- extraction state;
- known degraded/disabled sources.

This enables a HUMAN to understand the limits under which a historical assessment was made.

## 28. J1 Acceptance Criteria

Coverage & Health v0 is acceptable when a HUMAN can answer:

1. Which configured sources are healthy, degraded, in backoff, disabled, or need attention?
2. What part of research coverage is affected?
3. What work continues normally?
4. What proportion of the current project corpus is full text, abstract only, or metadata only?
5. What denominator does every percentage use?
6. How fresh are relevant searches/watchlists?
7. Which gaps/theories/methods/R-stages are most affected by coverage limitations?
8. Is scientific change distinguished from operational degradation?
9. Can a daily cycle remain useful under partial coverage?
10. Can routine engineering recovery happen without scientific authorization?
11. Are historical decisions linked to their coverage context?
12. Does the UI avoid claiming completeness it cannot know?
13. Can Profile A and Profile B use the same coverage/health architecture?

## 29. J1 Boundary

This specification intentionally does not yet define:

- monitoring stack;
- retry counts;
- backoff formulas;
- service supervisor implementation;
- source adapter APIs;
- queue schema;
- incident tables;
- metrics database;
- alert thresholds;
- Telegram implementation;
- add-in contracts.

These belong to later architecture and implementation stages and must serve the accepted HUMAN-facing coverage semantics.

## 30. Pinned UX Principle Candidate

> **GFPROJCLAW must always distinguish “we found no evidence” from “no evidence exists,” and “a source is degraded” from “the scientific interpretation is invalid.” Coverage limitations are disclosed, failures remain local, and healthy research work continues.**
