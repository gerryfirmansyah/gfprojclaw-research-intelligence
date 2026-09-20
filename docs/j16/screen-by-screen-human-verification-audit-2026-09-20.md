# Screen-by-Screen HUMAN Verification Audit — 2026-09-20

Status: STATIC/PROJECTION AUDIT COMPLETE; HUMAN VISUAL RECHECK REQUIRED AFTER REMEDIATIONS.

## Cross-cutting invariant
**No scientifically meaningful machine interpretation may be presented as supported knowledge unless the HUMAN interface provides an inspectable path to the canonical information that supports it.** Database state is machine-readable state; the Research Copilot is the HUMAN scientific verification surface. If a verification path cannot be presented, the UI must expose `UNKNOWN`, `NOT_AVAILABLE`, `NOT_RECORDED`, or `NOT_RUN` rather than silently asserting support.

Every scientifically meaningful aggregate must drill down to exact members. HUMAN-facing explanation should answer: what does this mean, why is it shown, what canonical evidence/state supports it, what is uncertain/unavailable, and what should HUMAN inspect next. Raw IDs/JSON may support audit but must not substitute for explanation.

## Research Copilot checklist
| Screen | Verification path observed | Status | Improvement required |
|---|---|---|---|
| Today — metric cards | All five counts open exact canonical member lists | PASS | None for aggregate traceability |
| Today — Recent Important Changes | Shows event/reason/time; View all reaches ChangeEvent detail | PASS | HUMAN-readable Delta remediation already implemented |
| Today — Research Stage Guide | Explicit GUIDE/non-canonical methodology | PASS | Do not add inferred canonical maturity |
| Today — Top Research Opportunities | Shows support/challenge counts but table rows themselves are not drill-down controls | IMPROVE | Make each candidate open Opportunities detail/evidence path |
| Today — Latest Papers | Shows Work/access/source state but no direct DOI/OpenAlex link in this panel | IMPROVE | Add source links or direct evidence inspection path |
| Today — Research Coverage | Shows access aggregate + limitation and View all | PASS | Coverage full screen should expose source/provider members when canonical source observations exist |
| Today — Knowledge Evolution | Shows ChangeEvent/reason + View all | PASS | None after Delta remediation |
| Today — Telegram Radar | Shows projected events + View all | PASS | Keep read-only boundary explicit |
| Research Journey R0–R16 | Explicit illustrative/non-canonical screen | PASS WITH CAUTION | Mock examples include numeric evidence and action buttons; visually ensure they cannot be mistaken for live state |
| Opportunities — object/detail | Canonical object statement/type/state visible | PASS | Humanize technical state labels where possible |
| Opportunities — Evidence & Coverage | Exact EvidenceRelationship → Claim → EvidenceFragment → Work + source links for GapCandidate | PASS | None |
| Opportunities — Advice & Critic | Explanation, dimensions, evidence basis, limitations visible | PASS | Humanize dimension labels if technical names remain primary |
| Opportunities — machine Assessment | HUMAN-readable purpose/dimensions/check instruction; raw type collapsed | PASS AFTER REMEDIATION | HUMAN visual recheck required |
| Opportunities — Research Quality | HUMAN-readable meaning/current state/importance/check + collapsed raw state | PASS | HUMAN visual recheck pending deployment |
| Opportunities — Evidence Verification | Evidence text/access, Claim, relationship, DOI/OpenAlex shown | PASS | None |
| Opportunities — HUMAN Authority | Decision/rationale/history visible and explicit HUMAN controls | PASS | Preserve reason requirement |
| Evidence Explorer | Claim/Work/fragment/access shown; explicit route to object-aware Verifikasi Bukti for relationship + DOI/OpenAlex | PASS AFTER REMEDIATION | HUMAN visual recheck required |
| Knowledge Evolution | HUMAN-readable change/current state + evidence-trigger membership + collapsed canonical detail | PASS | HUMAN visual recheck pending deployment |
| HUMAN Review | Claim/Work/evidence preview shown; explicit warning + route to Verifikasi Bukti before acceptance | PASS AFTER REMEDIATION | HUMAN visual recheck required |
| Research Coverage | Aggregate counts + exact canonical source observations + limitations rendered | PASS AFTER REMEDIATION | HUMAN visual recheck required |
| Profiles & Projects | Canonical active Profile/Project fields and versions visible | PASS | None |
| Telegram Radar full screen | Change/reason/coverage/HUMAN context + button to evidence | PASS | Button currently routes to Opportunities generally; ideally preserve selected object context |

## Admin Copilot checklist
| Screen | Verification path observed | Status | Improvement required |
|---|---|---|---|
| System Overview | Exact service/timer/storage/backup projection visible | PASS | Operational, not scientific |
| Profile & Project | Current canonical values + Preview Current/Proposed + actor/reason | PASS | None |
| Continuous Pilot | Persisted run IDs, status, attempts, stage history | PASS | Machine actions are not shown here; add collapsed technical actions only if operational debugging requires it |
| Source Runs | Canonical coverage source observations displayed | PASS | Current provider monitoring scope remains limited; UI must not imply continuous monitoring |
| Failures / Retry | Derived from persisted pilot rows | PASS | Keep absence phrased as no persisted item, not no failure ever |
| Quarantine | Explicit NOT_AVAILABLE, no invented records | PASS | Implement only when canonical projection exists |
| API / Services | Exact service states | PASS | Operational only |
| Activity / Audit | Exact activity-log lines | PASS | This is operational activity, not canonical scientific audit |
| Appearance & Language | Local/admin presentation preference; scientific boundary stated | PASS | None |

## Priority remediation queue
1. **HIGH — Research Coverage:** source observations exist in API payload but are not rendered on the full Research Coverage screen.
2. **HIGH — HUMAN Review:** reviewer needs direct evidence/source verification context on the same screen.
3. **HIGH — Evidence Explorer:** add source links and explicit relationship context for end-to-end Claim verification.
4. **MEDIUM — Machine Assessment:** translate assessment/dimension technical vocabulary before raw canonical detail.
5. **MEDIUM — Today Opportunities:** make summary candidates drill directly into exact Opportunity detail.
6. **MEDIUM — Today Latest Papers:** expose external source links/direct verification path.
7. **LOW — Research Journey:** strengthen visual non-canonical boundary around illustrative numeric examples/actions.
8. **LOW — Telegram Radar:** preserve selected object when opening evidence where feasible.

This audit is a code/projection verification, not a HUMAN visual acceptance. Items marked PASS mean an inspectable path exists in the implemented UI logic; final visual comprehensibility remains a HUMAN judgment.
