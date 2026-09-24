# Research Value Trial — HUMAN Acceptance Protocol v0

Status: **HUMAN GATE / ENGINE FREEZE EXCEPT ACCEPTANCE-BLOCKING DEFECTS**.

## Purpose

The engine has enough executable evidence for the current trial. From this checkpoint, do not optimize architecture, ranking, clustering, retrieval, or visual polish merely because improvement is possible. First learn whether a HUMAN researcher accepts the research experience.

## Acceptance session

Use the existing bounded trial: AI + digital government + public services; OpenAlex; 2022–2026. Do not silently change the query or source during the acceptance session.

The HUMAN performs this journey:

1. Read coverage and limitations.
2. Inspect at least one expected observed area.
3. Inspect at least one surprising or unclear observed area.
4. Read WHY for each selected area.
5. Inspect exact member papers for each selected area.
6. Open at least three source/DOI links in total.
7. State what was learned from the landscape.
8. State what remains uncertain or misleading.
9. Choose a next-scope reflection: NARROW, BROADEN, BRANCH, KEEP_SCOPE, RECONSIDER_QUERY, or INSPECT_MORE.
10. Complete the four acceptance checks and provide a written rationale.

## Four acceptance checks

The HUMAN, not the engine, evaluates whether:

- the landscape improved understanding of the research space;
- WHY improved understanding of why an area or paper was surfaced;
- WHY can be traced to exact papers and source/DOI;
- coverage and blind spots are understandable enough to prevent false confidence.

## Verdicts

**ACCEPT** — all four checks are satisfied and the HUMAN says the experience materially helps the research task.

**PARTIAL** — useful value is visible, but one or more acceptance-blocking frictions prevent routine research use.

**REJECT / REWORK** — the experience does not materially improve understanding or next-step choice compared with provider search alone, or creates unacceptable false confidence.

The system MUST NOT assign the verdict automatically.

## What happens after the HUMAN verdict

If ACCEPT: freeze the accepted behavior contract, then refactor/harden the engine behind that contract. Preserve the accepted journey and provenance invariants with regression tests.

If PARTIAL: convert only HUMAN-observed acceptance blockers into prioritized fixes; rerun the same acceptance protocol after remediation.

If REJECT / REWORK: do not polish the engine. Revisit the research experience hypothesis, especially landscape usefulness, WHY quality, inspection depth, or coverage framing.

## Evidence to record

Record selected areas, inspected paper identifiers, links opened, HUMAN learning notes, uncertainties, chosen scope reflection, the four check results, rationale, and final HUMAN verdict. Keep machine observations distinct from HUMAN statements.
