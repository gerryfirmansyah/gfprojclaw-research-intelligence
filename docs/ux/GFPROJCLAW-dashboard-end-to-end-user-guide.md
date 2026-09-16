# GFPROJCLAW Research Cockpit — End-to-End User Guide

**Review draft — 16 September 2026**

GFPROJCLAW should be used as a **research cockpit**, not as a conventional progress dashboard. Its purpose is to help a researcher see what changed, inspect the evidence behind a research signal, understand uncertainty and coverage limitations, receive machine-generated advice and criticism, and then make an explicit scientific decision as a HUMAN researcher.

> **STATUS → WHY → EVIDENCE → LEARN → RISK → SUGGESTED ACTION → HUMAN DECISION → CHANGE HISTORY**

Core authority rule: GFPROJCLAW may discover, connect, prioritize, critique, and explain evidence. It does **not** establish scientific truth, novelty, acceptance, or a final research verdict. HUMAN scientific judgment remains authoritative.

## 1. What to look at first every day

First confirm the **Profile** and **Project** selectors. Profile provides the broader domain context; Project is the concrete research context whose evidence, claims, opportunities, assessments, and decisions are being inspected.

Then open **Today**. Its primary question is not “how much of the research is complete?” but **“what changed since the previous research session, why does it matter, and where is HUMAN attention useful?”** Prioritize Recent Important Changes such as newly challenging evidence, a prior solution that may overlap a gap, a competing theory, coverage degradation, or materially new evidence.

Prototype caution: parts of Today are still illustrative/dummy surfaces. Treat panels explicitly marked **REAL DATA · PostgreSQL / API** as canonical for current HUMAN trials. Do not interpret illustrative counts or example opportunities as persisted scientific state.

## 2. Coverage before confidence

After Today, inspect **Coverage & Health** before trusting an opportunity or machine recommendation. Coverage answers a critical epistemic question: **how much of the relevant evidence universe has actually been observed?**

In the current real project slice, the cockpit shows one ABSTRACT_ONLY work, one Claim, no FULL_TEXT work, and `Counter-search: NOT_RUN`. The persisted boundary states that discovery breadth and counter-search are not yet complete.

Therefore, **0 challenging evidence does not mean no challenging evidence exists**. It may mean challenging evidence has not yet been searched for or persisted. Coverage context determines how strongly a current assessment may reasonably be used.

## 3. Research Opportunities — the main reasoning workspace

Research Opportunities presents evidence-backed candidates for HUMAN scientific review. A `CANDIDATE` is not a validated research gap. The current real candidate is **empirical and explanatory specificity in AI public governance**, represented as a `SYNTHESIS_GAP` in `CANDIDATE` state.

Read an opportunity in this order:

1. **Candidate Detail** — understand statement, type, and current state. Treat tentative wording such as “suggests” and “may remain underdeveloped” literally.
2. **Evidence & Coverage** — inspect supporting/challenging relationships, linked claims, counter-search state, and coverage limitations.
3. **Source provenance** — follow the evidence chain to the paper and original source. For important decisions, open OpenAlex, DOI, or the publisher rather than relying only on an AI summary.
4. **Advisory Dimensions** — inspect what is known and unknown about novelty, methodological feasibility, theoretical significance, and review priority. `UNKNOWN` is preferable to a fabricated confidence score.
5. **Advice & Critic** — read what challenges the opportunity, what remains unknown, and the recommended next HUMAN action.
6. **HUMAN Authority** — only after the preceding checks should the researcher record a scientific action and rationale.

Canonical provenance chain:

**Opportunity → EvidenceRelationship → Claim → EvidenceFragment → Work/Paper → Source**

A paper is not itself a research gap. A paper contains or supports evidence; evidence can support a Claim; persisted relationships can support or challenge an Opportunity. Separating these objects makes the research reasoning auditable.

## 4. Evidence Explorer — ask “what is the basis?”

Evidence Explorer is used when a researcher wants to inspect the basis of a claim or opportunity. The canonical chain is:

**Project → Work → EvidenceFragment → Claim**

The current example identifies an `ABSTRACT_SEGMENT` with `ABSTRACT_ONLY` access and a machine-assisted extraction origin. Access level matters. A claim derived from an abstract should not automatically be treated as equivalent to a full-text scientific review.

`NEEDS_REVIEW` is an attention state requiring HUMAN validation; it is not scientific acceptance or rejection.

## 5. Advice & Critic — machine reasoning, not scientific authority

Advice & Critic should be read after the evidence and coverage context are understood. Its job is to expose weaknesses, unknowns, and useful next actions.

For the current candidate, the system observes one supporting and zero challenging relationships but explicitly states that this is an **observed evidence balance, not a truth probability**. Because counter-search is `NOT_RUN` and discovery breadth is incomplete, the recommended action `RUN_COUNTER_SEARCH_AND_HUMAN_REVIEW` is consistent with the current limitations.

The recommendation is advice. The researcher remains responsible for deciding what to do.

## 6. HUMAN Authority and decision discipline

HUMAN Authority is the boundary where machine reasoning ends and explicit scientific judgment begins. A decision should never be treated like a “like” button. It should record **who decided, what was decided, why, when, and against which evidence/assessment context**.

- `ACCEPT_DIRECTION` — proceed with the current research direction based on current evidence. This does **not** establish that the gap is true or novel.
- `MODIFY` — retain useful parts of the direction but change its formulation, boundary, mechanism, theory, or other framing.
- `NEED_MORE_EVIDENCE` — defer a stronger directional decision and seek additional evidence, counter-evidence, or coverage.
- `REJECT_CANDIDATE` — explicitly decide not to continue the candidate in its current form.
- `REVIEW` — record that HUMAN scientific review remains required.

Example rationale for the current evidence state:

> Current evidence is based on one abstract-derived claim and counter-search has not been performed. I need competing evidence and prior-solution coverage before deciding whether to pursue this direction.

## 7. Change History — never rewrite research reasoning

A later HUMAN decision should supersede an earlier decision rather than erase it. A defensible history might evolve:

**REVIEW → NEED_MORE_EVIDENCE → MODIFY → ACCEPT_DIRECTION**

The current decision should remain visible together with prior decisions, assessment lineage, and supersedes lineage. This preserves the intellectual history of the project: the researcher can reconstruct not only what was decided, but how the decision changed as evidence changed.

## 8. Human Review — the scientific attention queue

Human Review is the inbox for canonical claims and other research objects that require HUMAN scientific attention. Inspect the paper, evidence basis, claim, and extraction origin before making a scientific judgment in a workflow that provides decision controls.

Prototype note: the screenshots reviewed still show the older “read-only for now” wording. The J11 working tree has already been revised so that this boundary describes the review queue accurately without implying that no persisted decision workflow exists.

## 9. Knowledge Evolution — what changed and why?

Knowledge Evolution records persisted `ChangeEvent`s. It explains historical changes in assessments and evidence context without silently rewriting HUMAN decisions. Use it to compare previous and current reasoning state and understand why a candidate or stage now deserves attention.

A ChangeEvent is historical/evolution context, not a global scientific gate. New evidence may change an assessment or attention signal while the HUMAN decision remains unchanged until the researcher explicitly acts.

## 10. Research Journey R0–R16 — a living map, not a waterfall

The R0–R16 Research Journey is a living research-lab map. It must not be interpreted as a linear completion percentage or waterfall gate. Later evidence can legitimately send the researcher back to an earlier stage — for example from Novelty Challenge back to Gap Formation, Theory Positioning, or Method Intelligence.

Use the Journey to answer: **which part of the research reasoning is affected by the latest evidence or decision, what was learned, what evidence trace explains the impact, and what HUMAN action may be useful next?**

## 11. Profiles & Projects and Telegram Radar

**Profiles & Projects** controls research scope. Profile represents a broader domain/research context; Project represents a concrete research agenda. The current configuration page shown in the prototype is still illustrative, while the project selector itself is backed by canonical context data.

**Telegram Research Radar** is a compressed, non-canonical attention channel. It should notify the researcher that something deserves inspection and deep-link back to the cockpit. It should not store canonical scientific state or make scientific decisions.

Correct flow:

**Telegram alert → Cockpit → Evidence → Context → HUMAN judgment**

## 12. Recommended daily activity

1. **Confirm context** — verify Profile and Project.
2. **Triage Today** — read Recent Important Changes before browsing opportunities.
3. **Check Coverage & Health** — ask whether current evidence coverage is sufficient to act.
4. **Clear Human Review** — inspect canonical claims requiring HUMAN attention.
5. **Inspect changed Opportunities** — read candidate, evidence, coverage, advisory dimensions, critic, unknowns, and suggested action.
6. **Trace important evidence** — use Evidence Explorer and, when necessary, open DOI/publisher/original sources.
7. **Record an explicit HUMAN decision** — choose the action you actually intend and write a rationale.
8. **Inspect Knowledge Evolution** — understand what changed and ensure no machine event silently changed HUMAN authority.
9. **Revisit R0–R16** — see which research stages are affected; move backward or forward as evidence requires.
10. **Perform deep work** — run literature discovery, counter-search, theory comparison, method exploration, writing, or experiments based on the evidence state.

## 13. Current end-to-end example

Current real flow:

**Coverage shows one abstract-only work and Counter-search NOT_RUN** → Opportunities presents a tentative AI public-governance synthesis-gap candidate → Evidence & Coverage links one supporting Claim to the systematic literature review → researcher verifies OpenAlex/DOI/publisher provenance → Advisory Dimensions remain UNKNOWN where evidence is incomplete → Advice & Critic recommends counter-search and HUMAN review → HUMAN records a decision and rationale → later evidence produces ChangeEvents → Knowledge Evolution explains the delta → relevant R0–R16 stages receive attention → Today surfaces the important change in the next research session.

GFPROJCLAW is therefore a **continuous research reasoning loop**, not a pipeline that simply ends.

## 14. Three questions to remember

**1. WHAT CHANGED?** — Today / Knowledge Evolution.

**2. CAN I TRUST THE CURRENT EVIDENCE COVERAGE ENOUGH TO ACT?** — Coverage & Health / Evidence Explorer.

**3. WHAT REQUIRES MY SCIENTIFIC JUDGMENT TODAY?** — Human Review / Opportunities.

Only after these are answered should the researcher ask: **What should I do next?** — Research Journey + Advice & Critic.

## 15. Interpretations to avoid

- `CANDIDATE` does not mean a valid or novel gap has been established.
- `SUPPORTS` does not mean a claim is scientifically true.
- `0 CHALLENGES` does not mean counter-evidence does not exist.
- `ACCEPT_DIRECTION` does not establish novelty or truth.
- `NEEDS_ATTENTION` does not mean the research is wrong.
- `R16` does not mean R0–R15 are permanently finalized.

## 16. J11 HUMAN acceptance target

J11 should not receive FINAL PASS from syntax or backend tests alone. The HUMAN-trialable chain is:

**Opportunity → Evidence → Critic → Unknowns → Suggested Action → reviewer + rationale → explicit HUMAN decision → persisted HumanDecision → assessment lineage → Change History**

The researcher should perform a meaningful decision rather than a fake production test. Only after this chain is visible, understandable, and auditable in the cockpit should J11 be considered ready for final acceptance.

## 17. Reflection questions

- Does Today immediately tell me what deserves attention, or does it still look like a generic metrics dashboard?
- Can I distinguish canonical REAL DATA from illustrative prototype data without ambiguity?
- Before acting on an opportunity, can I understand coverage limitations and counter-search state?
- Can I trace every important machine recommendation back to claims, evidence fragments, papers, and original sources?
- Is the difference between machine advice and HUMAN scientific authority unmistakable?
- Does the decision history preserve how my reasoning changed rather than only showing the latest answer?
- Does R0–R16 help me think iteratively rather than pressure me into a linear completion model?
- What information would I need every morning for GFPROJCLAW to become a genuine daily research cockpit?
