# GFPROJCLAW Research Value Trial Map v0

## Product checkpoint — 24 September 2026

GFPROJCLAW is not another literature search engine or crawler. Existing research providers should be reused where they are good at discovery. GFPROJCLAW exists to help a researcher **SEE THE UNIVERSE → UNDERSTAND WHY → VERIFY THE FACTS → HUMAN DECIDES**.

**Draft the research experience first. Prove researcher value end-to-end. Harden only what survives the trial.**

For this trial, do not add engineering infrastructure unless it is required to test researcher value.

## Trial question

Topic: **AI + digital government**

At the end, ask:

> Does GFPROJCLAW help the HUMAN understand this research landscape, its blind spots, and WHY particular literature may matter better than using the underlying search providers alone?

A successful trial does not require a perfect production pipeline. It requires a usable, inspectable research journey.

## What already exists and should be reused

| Research need | Existing GFPROJCLAW asset | Trial use |
|---|---|---|
| Research entry | Research Explorer, seed papers, Initial HUMAN Query | Reuse; make research interest the anchor |
| Discovery | OpenAlex/Crossref fetchers and preview tooling | Reuse providers; do not build a new crawler first |
| Provenance | source records, discovery/query/run concepts | Reuse behind the HUMAN surface |
| Research Universe semantics | living-SLR contract and corpus layers | Reuse definitions |
| Progressive retrieval | batch-boundary invariant and funnel UI | Reuse; batch size is not universe size |
| Coverage safety | scope/coverage alerts and blind-spot semantics | Reuse |
| Scientific safety | HUMAN authority, UNKNOWN/NOT_AVAILABLE/NOT_RUN | Preserve |
| Project research | Research Copilot, Evidence Explorer, Human Review, Radar | Reuse after HUMAN scope/project transition |
| Quality/audit | explanation and canonical provenance invariants | Keep behind researcher-facing explanations |

## Missing vertical slice

### 1. SEE — Observed Research Universe
Draft multi-source observation using existing providers. Show provider-reported totals, actually retrieved records, unique/deduplicated works, overlap where identifiers permit, not-retrieved coverage, and sources not searched.

Every count must answer **N of what scope?** and drill down to members when members exist.

### 2. MAP — Research Landscape
Create an inspectable landscape from the trial corpus: terminology/topic groupings, publication years, venues, review/landscape papers, adjacent areas, and other patterns supported by available metadata/abstracts.

Clusters are machine observations, not scientific truth. HUMAN can inspect exact member papers.

### 3. WHY — Research-context explanation
For a paper, cluster, blind spot, contradiction, or change, explain:
- why it is shown;
- how it may relate to the HUMAN research interest/question;
- what canonical facts or observed records support the explanation;
- uncertainty/limitations;
- what the HUMAN should inspect next.

**Every WHY must be inspectable back to WHAT.**

### 4. VERIFY — HUMAN Paper Inspector
Primary paper view should expose title, authors/year/venue, abstract when available, access/full-text state, reason shown, source/query provenance, cluster membership, and actionable links to DOI/OpenAlex/original source when available.

Raw UUIDs, fingerprints, JSON, and database terminology belong in collapsed technical detail, not the primary research experience.

### 5. COVERAGE — What have we not seen?
Show searched sources, partially observed sources, NOT_SEARCHED sources, retrieval truncation, inaccessible content, query families not run, and other blind spots. Absence from observed data is not evidence of absence from research.

### 6. LEARN / DECIDE — HUMAN learning
Provide a draft surface for HUMAN to record:
- what did I learn from this landscape?
- what surprised me?
- which areas need deeper exploration?
- what remains uncertain?
- should the scope/research question be reconsidered?

Machine may propose options; HUMAN decides scientific relevance, scope, gap, novelty, significance, evidence use, and project transition.

## Draft implementation policy

Temporary or non-canonical trial datasets are allowed if clearly marked **TRIAL / NON-CANONICAL**, with retrieval provenance preserved. They must not silently mutate Project Corpus, Evidence, Claims, HumanDecision, or other production scientific state.

Prefer existing provider capabilities over custom crawling. OpenAlex + Crossref + a HUMAN/provider observation such as ScienceDirect is enough to start the value trial. Additional providers are added only when the trial reveals a meaningful coverage need.

## Do not build yet

Unless the value trial proves they are required, do not prioritize:
- new database migrations;
- new roles/permission architecture;
- scheduler or recovery hardening;
- autonomous continuous crawling;
- production writer hardening;
- sophisticated vector infrastructure;
- large-scale full-text ingestion;
- new abstractions whose only benefit is engineering elegance.

## Trial acceptance

Continue/harden if the HUMAN can credibly say:

> I can see the observed research landscape, I discovered literature or relationships I had not noticed, I understand WHY GFPROJCLAW surfaced them, I can verify the underlying papers/sources, and this changes or sharpens what I inspect next.

Reconsider or stop if the experience remains essentially:

> Search results + dashboard + AI summary that existing tools already provide.

## Build order

**Existing providers → observed universe → landscape → WHY → paper/source verification → coverage/blind spots → HUMAN learning → HUMAN decision.**

Engineering work is admitted only when a step in this vertical journey cannot be tested without it.

## HUMAN research augmentation identity

GFPROJCLAW is a **HUMAN Research Augmentation System**, not a competitor to research search providers. It should reuse existing research information systems where useful and improve the HUMAN's ability to observe, understand, verify, and navigate research choices.

The initial research journey is:

**Research Interest → SEE the bounded universe → Understand scope → Advice + WHY → Explore alternatives → Verify facts → HUMAN defines research direction.**

Scope advice is operational and explanatory, not a scientific verdict. The system may explain that a bounded corpus is still too large for whole-corpus inspection under current trial capabilities, or that a narrower bounded corpus is technically feasible to retrieve in full. It MUST NOT say that the narrower scope is scientifically correct.

### Universe-first retrieval rule

**Reduce the universe by explicit research boundaries, not by hidden retrieval ranking.**

A top-N provider result is a ranked retrieval slice, not a representative Research Universe. If an explicitly bounded universe is technically feasible to retrieve, prefer whole-bounded progressive retrieval before characterizing its landscape. If it is not feasible, expose the limitation and offer HUMAN-inspectable scope/time/query alternatives.

For the first Research Value Trial, the HUMAN-selected contemporary time boundary is **2022–2026**. Literature outside that window is **NOT INCLUDED IN CURRENT EXPLORATION WINDOW**, not irrelevant.
