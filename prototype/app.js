const data = {
  A: {
    projects: ["Cross-agency Digital Government Governance", "Enterprise Architecture Capability Study"],
    changes: [
      ["GAP-014", "New paper challenges the broad governance-capability formulation", "CONTESTED", "red"],
      ["SOL-008", "Existing enterprise-architecture solution overlaps GAP-021", "POSSIBLY CLOSED", "yellow"],
      ["METHOD-012", "Longitudinal mixed-method alternative identified", "NEW ALTERNATIVE", "blue"],
      ["COVERAGE", "Semantic Scholar degraded; prior-solution search may be incomplete", "DEGRADED", "yellow"]
    ],
    opportunities: [
      ["GAP-014", "Cross-agency governance capability under disruption", 82, "Strong", "CONTESTED"],
      ["GAP-009", "Resilience and IT-governance integration", 78, "Moderate", "STRENGTHENING"],
      ["GAP-021", "Adaptive enterprise-architecture capability", 65, "Weak", "POSSIBLY CLOSED"],
      ["GAP-017", "Human factors in e-government transformation", 61, "Moderate", "REVIEW"]
    ],
    papers: [
      ["Digital government resilience: a systematic review", 2026, "Gov. Info. Q.", "92%"],
      ["AI governance in the public sector", 2026, "Public Mgmt. Rev.", "87%"],
      ["Enterprise architecture capability under disruption", 2025, "IS Frontiers", "84%"],
      ["Institutional complexity in digital government", 2025, "Gov. Info. Q.", "79%"]
    ]
  },
  B: {
    projects: ["Human Capability & Organizational Resilience", "Leadership Under Disruption"],
    changes: [
      ["GAP-014", "Behavioural construct overlaps the proposed human-capability mechanism", "CONTESTED", "red"],
      ["THEORY-006", "Competing explanation gains support", "NEEDS REVIEW", "yellow"],
      ["CLM-204", "Level-of-analysis mismatch detected", "CHALLENGED", "red"],
      ["METHOD-012", "Multilevel longitudinal design identified", "NEW ALTERNATIVE", "blue"]
    ],
    opportunities: [
      ["GAP-014", "Human capability mechanism in organizational resilience", 81, "Strong", "CONTESTED"],
      ["GAP-009", "Adaptive behaviour as mechanism", 76, "Moderate", "STRENGTHENING"],
      ["GAP-021", "Capability transfer across levels of analysis", 69, "Moderate", "REVIEW"],
      ["GAP-017", "Resilience measurement boundary conditions", 64, "Weak", "CANDIDATE"]
    ],
    papers: [
      ["Human capability and adaptive resilience", 2026, "J. Org. Change", "94%"],
      ["Behavioural mechanisms of organizational resilience", 2026, "Org. Studies", "89%"],
      ["Multilevel resilience capability development", 2025, "J. Management", "83%"],
      ["Measurement ambiguity in resilience research", 2025, "Acad. Mgmt. Rev.", "78%"]
    ]
  }
};

const journeyStages = [
  ["R0", "Research Intent", "HUMAN REVIEWED", "green"],
  ["R1", "Research Landscape", "MATURE", "green"],
  ["R2", "Evidence Mapping", "EVIDENCE GROWING", "blue"],
  ["R3", "Problem Formulation", "DEVELOPING", "blue"],
  ["R4", "Gap Formation", "NEEDS ATTENTION", "red"],
  ["R5", "Gap Falsification", "EVIDENCE GROWING", "blue"],
  ["R6", "Theory Positioning", "NEEDS ATTENTION", "red"],
  ["R7", "Research Question", "DEVELOPING", "blue"],
  ["R8", "Conceptualization", "DEVELOPING", "blue"],
  ["R9", "Method Intelligence", "EVIDENCE GROWING", "blue"],
  ["R10", "Research Design", "NOT STARTED", "gray"],
  ["R11", "Contribution Formation", "DEVELOPING", "blue"],
  ["R12", "Novelty Challenge", "NEEDS ATTENTION", "red"],
  ["R13", "Evidence & Argument Audit", "NOT STARTED", "gray"],
  ["R14", "Adversarial Review", "NOT STARTED", "gray"],
  ["R15", "Scholarly Positioning", "DEVELOPING", "blue"],
  ["R16", "Research Readiness", "DEVELOPING", "blue"]
];

const health = [
  ["OpenAlex", "HEALTHY", "green", "78% of configured discovery executed"],
  ["Semantic Scholar", "DEGRADED", "yellow", "Citation expansion limited"],
  ["Crossref", "HEALTHY", "green", "Metadata discovery current"],
  ["Full-text extraction", "HEALTHY", "green", "48% of current project corpus"]
];

const evolution = [
  ["GAP-014", "STRENGTHENING → CONTESTED", "2h ago"],
  ["GAP-009", "Evidence increased", "6h ago"],
  ["METHOD-012", "New alternative", "1d ago"],
  ["CLM-142", "Contradiction found", "1d ago"]
];

const telegram = [
  ["09:12", "3 new papers materially affect GAP-014"],
  ["07:45", "GAP-021 may already have a prior solution"],
  ["Yesterday", "Competing theory deserves review"],
  ["Yesterday", "Coverage degraded for one discovery source"]
];

const profileSelect = document.getElementById("profile-select");
const projectSelect = document.getElementById("project-select");
const PROTOTYPE_VERSION = "0.11.0";
const API_BASE = window.location.hostname.endsWith("github.io") ? "https://api.116.212.72.79.nip.io" : "";

function selectedDummyData() {
  const idx = Math.max(0, profileSelect.selectedIndex);
  return Object.values(data)[idx] || Object.values(data)[0];
}

function selectedProjectLabel() {
  return projectSelect.selectedOptions[0]?.textContent || "Selected project";
}

function stateClass(label) {
  if (/CONTESTED|CHALLENGED|NEEDS ATTENTION/i.test(label)) return "red";
  if (/STRENGTH|MATURE|HUMAN REVIEWED|HEALTHY/i.test(label)) return "green";
  if (/POSSIBLY|DEGRADED|REVIEW/i.test(label)) return "yellow";
  if (/NOT STARTED/i.test(label)) return "gray";
  return "blue";
}

function renderProjects() {
  projectSelect.innerHTML = data[profileSelect.value].projects.map(x => `<option>${x}</option>`).join("");
}

function renderDashboard() {
  const d = selectedDummyData();
  document.getElementById("change-list").innerHTML = d.changes.map(([id, text, state, cls]) => `
    <div class="change-row"><div class="change-main"><strong>${id} — ${text}</strong><small>Evidence-aware dummy ChangeEvent</small></div><span class="state ${cls}">${state}</span></div>`).join("");

  document.getElementById("journey-mini").innerHTML = journeyStages.slice(0, 7).map(([r, name, status, cls]) => `
    <div class="journey-row"><span class="r-code">${r}</span><div><strong>${name}</strong><small>Evidence-linked stage status</small></div><span class="state ${cls}">${status}</span></div>`).join("") + `<button class="text-button" data-open="journey">Show R7–R16</button>`;

  document.getElementById("opportunity-table").innerHTML = `
    <table class="table"><thead><tr><th>ID</th><th>Candidate</th><th>Gap evidence</th><th>Coverage</th><th>Evolution</th></tr></thead><tbody>
    ${d.opportunities.map(([id, title, score, evidence, status]) => `<tr><td><strong>${id}</strong></td><td>${title}</td><td><span class="score">${score}</span></td><td>${evidence}</td><td><span class="state ${stateClass(status)}">${status}</span></td></tr>`).join("")}
    </tbody></table>`;

  renderLatestPapers();
  document.querySelectorAll(".metric-card").forEach(el => el.classList.add("dummy-surface"));
  ["change-list","journey-mini","opportunity-table","evolution-mini","telegram-mini"].forEach(id => document.getElementById(id)?.closest(".panel")?.classList.add("dummy-surface"));
  document.getElementById("paper-list")?.closest(".panel")?.classList.add("real-surface");
  document.getElementById("health-mini")?.closest(".panel")?.classList.add("real-surface");
  loadProjectCoverageSummary();
  document.getElementById("evolution-mini").innerHTML = evolution.map(([id,change,when]) => `<div class="evolution-row"><div><strong>${id}</strong><small>${change}</small></div><small>${when}</small></div>`).join("");
  document.getElementById("telegram-mini").innerHTML = telegram.map(([time,text]) => `<div class="telegram-row"><time>${time}</time><strong>${text}</strong></div>`).join("");
  bindOpenButtons();
}

async function renderLatestPapers() {
  const box = document.getElementById("paper-list");
  const projectId = projectSelect.value;
  if (!box || !projectId) return;
  box.innerHTML = `<div class="paper-row"><div><strong>Loading real project works…</strong></div></div>`;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectId)}/papers`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const papers = await response.json();
    box.innerHTML = papers.length ? papers.map(p => {
      const year = p.publication_year || "Year unknown";
      const venue = p.venue_name || "Venue unknown";
      const status = p.human_review_state || p.relevance_state || "UNREVIEWED";
      return `<div class="paper-row"><div><strong>${p.title}</strong><small>${year} · ${venue} · ${p.current_access_level} · ${p.source_key || "source unknown"}</small></div><span class="state ${stateClass(status)}">${status}</span></div>`;
    }).join("") : `<div class="paper-row"><div><strong>No real works stored for this project yet.</strong><small>Latest Papers is reading PostgreSQL, not dummy scientific evidence.</small></div></div>`;
  } catch (error) {
    console.error(error);
    box.innerHTML = `<div class="paper-row"><div><strong>Real paper data unavailable</strong><small>${error.message}</small></div></div>`;
  }
}

function commonHeader(title, subtitle, mode = "dummy") {
  const label = mode === "real" ? "REAL DATA · PostgreSQL / API" : "DUMMY DATA · illustrative";
  return `<div class="detail-header"><div><h1>${title}</h1><p>${subtitle}</p></div><div class="coverage-pill ${mode === "real" ? "real-surface" : "dummy-surface"}">${label}</div></div>`;
}

function renderJourney() {
  return commonHeader("Research Journey R0–R16", "A living research-lab view, not a progress gate.") + `
    <div class="detail-grid"><div class="stack"><div class="card"><h3>All stages</h3>${journeyStages.map(([r,n,s,c]) => `<div class="journey-row"><span class="r-code">${r}</span><div><strong>${n}</strong><small>Status is reversible</small></div><span class="state ${c}">${s}</span></div>`).join("")}</div></div>
    <div class="stack"><div class="card"><h3>R6 — Theory Positioning</h3><div class="callout warning">NEEDS ATTENTION because a competing explanation now covers part of the same mechanism.</div><p><strong>What we found</strong></p><ul><li>23 mapped papers</li><li>5 candidate theoretical lenses</li><li>4 challenging evidence links</li><li>2 competing explanations</li></ul><p><strong>Learn</strong></p><p>Theory should be evaluated for explanatory fit and contribution, not popularity alone.</p></div><div class="card"><h3>Evidence trace</h3><div class="trace">R6 WHY → CLM-142 → CHALLENGES THEORY-006 → EVF-0092 → Paper → Source</div></div></div>
    <div class="stack"><div class="card"><h3>Suggested HUMAN actions</h3><div class="decision-bar"><button class="primary">Compare theories</button><button>Inspect mechanisms</button><button>Counter-evidence</button><button>Need more evidence</button></div></div><div class="card"><h3>Recent stage impacts</h3><p>CE-0048 affects R4, R5, R6, R11 and R12. These are attention signals, not forced transitions.</p></div></div></div>`;
}

function renderOpportunities() {
  return commonHeader("Research Opportunities", "Evidence-backed advisory prioritization for HUMAN scientific review.", "real") + `
  <div class="callout warning">Prioritization is advisory context only. It does not establish novelty, significance, feasibility, acceptance, or a scientific verdict.</div>
  <div class="card real-surface"><h3>Research Opportunities <span class="data-badge real">REAL DATA</span></h3><div id="real-gap-list">Loading persisted opportunity intelligence…</div></div>
  <div class="detail-grid" style="margin-top:14px"><div class="card real-surface"><h3>Candidate Detail</h3><div id="real-gap-detail">Select a persisted opportunity.</div></div><div class="card real-surface"><h3>Evidence & Coverage</h3><div id="real-gap-relationship">No evidence context loaded yet.</div></div><div class="card real-surface"><h3>Advisory Dimensions</h3><div id="real-gap-assessment">Select a persisted opportunity.</div></div><div class="card real-surface"><h3>Advice & Critic</h3><div id="real-gap-critic">Select a persisted opportunity.</div></div><div class="card real-surface"><h3>HUMAN Authority</h3><div id="real-gap-decision">Select a persisted opportunity.</div></div></div>`;
}

async function loadProjectOpportunities() {
  const list = document.getElementById("real-gap-list");
  const detail = document.getElementById("real-gap-detail");
  const relation = document.getElementById("real-gap-relationship");
  const decision = document.getElementById("real-gap-decision");
  if (!list || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/opportunities`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Opportunities HTTP ${response.status}`);
    const rows = await response.json();
    if (!rows.length) { list.innerHTML = "<p>No persisted research opportunities for this project yet.</p>"; detail.innerHTML = "<p>Nothing to inspect yet.</p>"; relation.innerHTML = "<p>No canonical evidence trace persisted.</p>"; decision.innerHTML = "<p>No research opportunity available for HUMAN review.</p>"; return; }
    list.innerHTML = rows.map((r,i) => `<div class="change-row" data-gap-index="${i}"><div class="change-main"><strong>${escapeHtml(r.canonical_label)}</strong><small>${escapeHtml(r.gap_type)} · ${escapeHtml(r.current_evolution_state)}</small></div><span class="state ${stateClass(r.current_evolution_state)}">${escapeHtml(r.current_evolution_state)}</span></div>`).join("");
    const show = async r => {
      detail.innerHTML = `<p><strong>Statement:</strong> ${escapeHtml(r.statement)}</p><p><strong>Type:</strong> ${escapeHtml(r.gap_type)}</p><p><strong>State:</strong> ${escapeHtml(r.current_evolution_state)}</p>`;
      const trace = Array.isArray(r.evidence_trace) ? r.evidence_trace : [];
      relation.innerHTML = `<p><strong>Persisted evidence links:</strong> ${escapeHtml(r.support_count)} supporting · ${escapeHtml(r.challenge_count)} challenging · ${escapeHtml(r.linked_claim_count)} linked claim(s)</p><p><strong>Counter-search:</strong> ${escapeHtml(r.counter_search_state || "NOT_RECORDED")}</p><p><strong>Coverage limitation:</strong> ${escapeHtml(r.coverage_limitations || "Not recorded")}</p>${trace.length ? trace.map(t => { const links = (Array.isArray(t.work_identifiers) ? t.work_identifiers : []).map(i => i.type === "DOI" ? `<a href="${escapeHtml(`https://doi.org/${i.value}`)}" target="_blank" rel="noopener noreferrer">DOI</a>` : i.type === "OPENALEX" ? `<a href="${escapeHtml(`https://openalex.org/${i.value}`)}" target="_blank" rel="noopener noreferrer">OpenAlex</a>` : "").filter(Boolean).join(" · "); return `<div class="trace"><strong>${escapeHtml(t.semantic_type)}</strong> · ${escapeHtml(t.work_title)}${links ? ` · ${links}` : ""}<br><small>SourceRecord: ${escapeHtml(t.source_identifier || t.source_record_id)} · Claim: ${escapeHtml(t.claim_text)}</small></div>`; }).join("") : `<p>No canonical evidence trace persisted.</p>`}`;
      const dimensions = Array.isArray(r.dimensions) ? r.dimensions : [];
      document.getElementById("real-gap-assessment").innerHTML = dimensions.length ? dimensions.map(d => `<p><strong>${escapeHtml(d.dimension_type)}:</strong> ${escapeHtml(d.value_text ?? d.value_numeric ?? "UNKNOWN")}</p><small>${escapeHtml(d.explanation || "")}</small>`).join("") : `<p>No persisted J9 assessment dimensions.</p>`;
      await renderGapCritic(r);
      renderGapDecision(r);
    };
    document.querySelectorAll("[data-gap-index]").forEach(el => el.onclick = () => show(rows[Number(el.dataset.gapIndex)]));
    show(rows[0]);
  } catch (error) { console.error(error); list.innerHTML = `<p>Research Opportunities API unavailable: ${escapeHtml(error.message)}</p>`; }
}

async function renderGapCritic(gap) {
  const box = document.getElementById("real-gap-critic");
  if (!box || !projectSelect.value) return;
  box.innerHTML = `<p>Loading persisted Advice & Critic…</p>`;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/advice-critic`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Advice & Critic HTTP ${response.status}`);
    const rows = await response.json();
    const critic = rows.find(r => r.gap_id === gap.gap_id);
    if (!critic) { box.innerHTML = `<p>No persisted J10 Advice & Critic assessment for this candidate.</p>`; return; }
    gap.assessment_id = critic.assessment_id || null;
    const dimensions = Array.isArray(critic.dimensions) ? critic.dimensions : [];
    const byType = type => dimensions.find(d => d.dimension_type === type);
    const risk = byType("COUNTER_EVIDENCE_RISK");
    const coverage = byType("EVIDENCE_COVERAGE_CONTEXT");
    const priority = byType("REVIEW_PRIORITY");
    box.innerHTML = `<p><strong>Critic — what challenges this opportunity?</strong></p><p>${escapeHtml(risk?.explanation || "No persisted counter-evidence assessment is available.")}</p><p><strong>What remains unknown?</strong></p><p>Counter-search: ${escapeHtml(critic.counter_search_state || "NOT_RECORDED")} · ${escapeHtml(coverage?.explanation || critic.coverage_limitations || "Coverage limitations are not recorded.")}</p><p><strong>Recommended next HUMAN action</strong></p><p>${escapeHtml(priority?.value_text || "HUMAN_REVIEW_REQUIRED")}</p><small>${escapeHtml(priority?.explanation || "Machine advice only; HUMAN scientific judgment remains authoritative.")}</small><div class="callout warning">Advice & Critic supports falsification and review; it does not establish novelty, truth, acceptance, or a scientific verdict.</div>`;
  } catch (error) {
    console.error(error);
    box.innerHTML = `<p>Advice & Critic unavailable: ${escapeHtml(error.message)}</p>`;
  }
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}

function renderEvidence() {
  return commonHeader("Evidence Explorer", "Real EvidenceFragment and Claim records for the selected Project.", "real") + `
  <div class="detail-grid"><div class="card"><h3>Evidence Results</h3><div id="real-evidence-list">Loading canonical evidence…</div></div>
  <div class="card"><h3>Evidence Detail</h3><div id="real-evidence-detail">Select a persisted claim.</div></div>
  <div class="card"><h3>Canonical boundary</h3><div class="trace">Project → Work → EvidenceFragment → Claim</div><p>Only persisted EvidenceRelationships are shown or implied; no additional relationship is inferred.</p></div></div>`;
}

async function loadProjectEvidence() {
  const list = document.getElementById("real-evidence-list");
  const detail = document.getElementById("real-evidence-detail");
  if (!list || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/evidence`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Evidence HTTP ${response.status}`);
    const rows = await response.json();
    if (!rows.length) {
      list.innerHTML = "<p>No persisted EvidenceFragment / Claim records for this project yet.</p>";
      detail.innerHTML = "<p>Nothing to review yet.</p>";
      return;
    }
    list.innerHTML = rows.map((r, i) => `<div class="change-row" data-evidence-index="${i}"><div class="change-main"><strong>${escapeHtml(r.claim_text)}</strong><small>${escapeHtml(r.work_title)} · ${escapeHtml(r.access_level)}</small></div><span class="state ${stateClass(r.review_state)}">${escapeHtml(r.review_state)}</span></div>`).join("");
    const show = r => { detail.innerHTML = `<p><strong>Paper:</strong> ${escapeHtml(r.work_title)}</p><p><strong>Fragment:</strong> ${escapeHtml(r.fragment_type)} · ${escapeHtml(r.access_level)}</p><p><strong>Evidence preview:</strong> ${escapeHtml(r.fragment_preview)}…</p><p><strong>Claim:</strong> ${escapeHtml(r.claim_text)}</p><p><strong>Extraction:</strong> ${escapeHtml(r.extraction_origin)} · ${escapeHtml(r.extraction_version)}</p><div class="callout warning">${escapeHtml(r.review_state)} — HUMAN validation required before scientific acceptance.</div>`; };
    document.querySelectorAll("[data-evidence-index]").forEach(el => el.onclick = () => show(rows[Number(el.dataset.evidenceIndex)]));
    show(rows[0]);
  } catch (error) {
    console.error(error);
    list.innerHTML = `<p>Evidence API unavailable: ${escapeHtml(error.message)}</p>`;
  }
}

function renderEvolution() {
  return commonHeader("Knowledge Evolution", "Persisted ChangeEvents explain what changed and why without rewriting HUMAN decisions.", "real") + `
  <div class="detail-grid"><div class="card real-surface"><h3>ChangeEvent Timeline <span class="data-badge real">REAL DATA</span></h3><div id="real-change-list">Loading canonical ChangeEvents…</div></div>
  <div class="card real-surface"><h3>Reasoning Delta</h3><div id="real-change-detail">Select a persisted ChangeEvent.</div></div>
  <div class="card real-surface"><h3>Scientific Authority Boundary</h3><div class="callout warning">ChangeEvents record historical knowledge evolution. They do not automatically mutate GapCandidate state or HumanDecision.</div></div></div>`;
}

async function loadProjectChanges() {
  const list = document.getElementById("real-change-list");
  const detail = document.getElementById("real-change-detail");
  if (!list || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/changes`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Changes HTTP ${response.status}`);
    const rows = await response.json();
    if (!rows.length) { list.innerHTML = "<p>No persisted ChangeEvents for this project yet.</p>"; detail.innerHTML = "<p>Nothing has been recorded yet.</p>"; return; }
    list.innerHTML = rows.map((r,i) => `<div class="change-row" data-change-index="${i}"><div class="change-main"><strong>${escapeHtml(r.change_type)}</strong><small>${escapeHtml(r.canonical_label)} · ${escapeHtml(r.observed_at)}</small></div></div>`).join("");
    const show = r => { detail.innerHTML = `<p><strong>Why:</strong> ${escapeHtml(r.reasoning_delta)}</p><p><strong>Previous:</strong> ${escapeHtml(JSON.stringify(r.previous_state_jsonb ?? null))}</p><p><strong>Current:</strong> ${escapeHtml(JSON.stringify(r.current_state_jsonb ?? null))}</p><div class="callout warning">Historical observation only; no HUMAN decision was changed automatically.</div>`; };
    document.querySelectorAll("[data-change-index]").forEach(el => el.onclick = () => show(rows[Number(el.dataset.changeIndex)]));
    show(rows[0]);
  } catch (error) { console.error(error); list.innerHTML = `<p>ChangeEvent API unavailable: ${escapeHtml(error.message)}</p>`; }
}

function renderReview() {
  return commonHeader("Human Review", "Canonical claims needing HUMAN scientific review for the selected Project.", "real") + `
  <div class="detail-grid"><div class="card real-surface"><h3>Review Queue <span class="data-badge real">REAL DATA</span></h3><div id="real-review-list">Loading canonical review queue…</div></div>
  <div class="card real-surface"><h3>Review Context</h3><div id="real-review-detail">Select a persisted claim.</div></div>
  <div class="card"><h3>Decision boundary</h3><p>This queue supports inspection of canonical claims. A HumanDecision is written only through an explicit HUMAN action in a workflow that provides decision controls.</p><div class="callout warning">NEEDS_REVIEW is an attention state, not scientific acceptance or rejection.</div></div></div>`;
}

async function loadHumanReview() {
  const list = document.getElementById("real-review-list");
  const detail = document.getElementById("real-review-detail");
  if (!list || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/evidence`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Review HTTP ${response.status}`);
    const rows = (await response.json()).filter(r => r.review_state === "NEEDS_REVIEW" || r.review_state === "CONTESTED");
    if (!rows.length) { list.innerHTML = "<p>No persisted claims currently need review.</p>"; detail.innerHTML = "<p>Nothing to review yet.</p>"; return; }
    list.innerHTML = rows.map((r,i) => `<div class="change-row" data-review-index="${i}"><div class="change-main"><strong>${escapeHtml(r.claim_text)}</strong><small>${escapeHtml(r.work_title)} · ${escapeHtml(r.access_level)}</small></div><span class="state ${stateClass(r.review_state)}">${escapeHtml(r.review_state)}</span></div>`).join("");
    const show = r => { detail.innerHTML = `<p><strong>Paper:</strong> ${escapeHtml(r.work_title)}</p><p><strong>Evidence basis:</strong> ${escapeHtml(r.fragment_type)} · ${escapeHtml(r.access_level)}</p><p><strong>Claim:</strong> ${escapeHtml(r.claim_text)}</p><p><strong>Extraction origin:</strong> ${escapeHtml(r.extraction_origin)}</p><div class="callout warning">HUMAN review required. Persisted machine-suggested relationships are not HUMAN decisions or accepted scientific conclusions.</div>`; };
    document.querySelectorAll("[data-review-index]").forEach(el => el.onclick = () => show(rows[Number(el.dataset.reviewIndex)]));
    show(rows[0]);
  } catch (error) { console.error(error); list.innerHTML = `<p>Review API unavailable: ${escapeHtml(error.message)}</p>`; }
}

function renderCoverage() {
  return commonHeader("Coverage & Health", "Observed coverage state from the latest persisted CoverageContext.", "real") + `
  <div id="real-coverage-detail" class="detail-grid"><div class="card real-surface"><h3>Loading coverage…</h3></div></div>`;
}

async function loadProjectCoverage(targetId = "real-coverage-detail") {
  const box = document.getElementById(targetId);
  if (!box || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/coverage`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Coverage HTTP ${response.status}`);
    const c = await response.json();
    if (!c.coverage_context_id) { box.innerHTML = `<div class="card real-surface"><p>No persisted CoverageContext for this project yet.</p></div>`; return; }
    const access = c.access_summary_jsonb || {};
    const extraction = c.extraction_summary_jsonb || {};
    const sources = c.sources || [];
    box.innerHTML = `<div class="card real-surface"><h3>Source observations <span class="data-badge real">REAL DATA</span></h3>${sources.length ? sources.map(src => `<div class="health-row"><div><strong>${escapeHtml(src.source_key)}</strong><small>${escapeHtml(src.access_limitations || "No access limitation recorded")}</small></div><span class="state yellow">${escapeHtml(src.health_state)}</span></div>`).join("") : `<p>No source observations persisted.</p>`}</div><div class="card real-surface"><h3>Persisted corpus coverage</h3><ul><li>FULL_TEXT — ${access.FULL_TEXT || 0}</li><li>ABSTRACT_ONLY — ${access.ABSTRACT_ONLY || 0}</li><li>METADATA_ONLY — ${access.METADATA_ONLY || 0}</li><li>Claims — ${extraction.claims || 0}</li><li>Quarantined claims — ${extraction.quarantined || 0}</li></ul><p><strong>Counter-search:</strong> ${escapeHtml(c.counter_search_state)}</p></div><div class="card real-surface"><h3>Boundary</h3><p><strong>Observed:</strong> ${escapeHtml(c.observed_at)}</p><div class="callout warning">${escapeHtml(c.limitations || "No limitations recorded.")}</div></div>`;
  } catch (error) { box.innerHTML = `<div class="card"><p>Coverage API unavailable: ${escapeHtml(error.message)}</p></div>`; }
}

async function loadProjectCoverageSummary() {
  const box = document.getElementById("health-mini");
  if (!box) return;
  box.innerHTML = `<div class="health-row"><div><strong>Loading real coverage…</strong></div></div>`;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/coverage`, { cache: "no-store" });
    const c = response.ok ? await response.json() : {};
    box.innerHTML = c.coverage_context_id ? (c.sources || []).map(src => `<div class="health-row"><div><strong>${escapeHtml(src.source_key)}</strong><small>${escapeHtml(src.observed_record_count)} observed record(s)</small></div><span class="state yellow">${escapeHtml(src.health_state)}</span></div>`).join("") + `<div class="callout">Counter-search: ${escapeHtml(c.counter_search_state)}</div>` : `<p>No persisted coverage snapshot yet.</p>`;
  } catch (error) { box.innerHTML = `<p>Coverage unavailable.</p>`; }
}

function renderProfiles() {
  const isA = profileSelect.selectedIndex === 0;
  return commonHeader("Research Profile / Project Configuration", "Domain context is configuration; scientific intent belongs to a Project.") + `
  <div class="detail-grid"><div class="card"><h3>${isA ? "Profile A — Computer / Information Systems" : "Profile B — Management / Organization Studies"}</h3><p><strong>Core interests</strong></p><ul>${(isA ? ["IT Governance","e-Government / Digital Government","Enterprise Architecture"] : ["Organizational Resilience","Human Behaviour","Human Capability"]).map(x=>`<li>${x}</li>`).join("")}</ul><p><strong>Seed literature:</strong> 12 works</p><p><strong>Watchlists:</strong> 4 active</p></div>
  <div class="card"><h3>Selected Project</h3><p><strong>${selectedProjectLabel()}</strong></p><p>Research intent is provisional and feeds R0 rather than pre-completing the research journey.</p><div class="callout">AI suggestions: 3 concepts · 2 theory candidates · 2 method candidates. HUMAN Accept / Modify / Reject.</div></div>
  <div class="card"><h3>Generality Check</h3><ul><li>Same core objects</li><li>Same R0–R16 journey</li><li>Same Evidence Explorer</li><li>Same ChangeEvent logic</li><li>Same Human Review</li></ul><p><strong>No domain-specific core branch required.</strong></p></div></div>`;
}

function renderTelegram() {
  return commonHeader("Telegram Research Radar", "Read-only projection of canonical ChangeEvent. Telegram never becomes scientific state.") + `
  <div id="radar-live" class="card"><p>Loading canonical Radar projection…</p></div>
  <div class="card"><h3>Radar Rules</h3><ul><li>No raw crawler logs</li><li>No automatic scientific decisions</li><li>No canonical state in Telegram</li><li>Delivery failure stays local</li><li>Inspect full context in Dashboard</li></ul></div>`;
}

async function loadProjectRadar() {
  const box = document.getElementById("radar-live");
  if (!box) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/radar`, { cache: "no-store" });
    const rows = response.ok ? await response.json() : [];
    box.innerHTML = rows.length ? rows.map(r => `<div class="change-row"><div class="change-main"><strong>${escapeHtml(r.change_type)}</strong><small>${escapeHtml(r.profile_name)} / ${escapeHtml(r.project_name)}</small><p><strong>WHAT CHANGED</strong><br>${escapeHtml(r.canonical_label)}</p><p><strong>WHY IT MATTERS</strong><br>${escapeHtml(r.reasoning_delta)}</p><p><strong>COVERAGE</strong><br>Counter-search: ${escapeHtml(r.counter_search_state || "UNKNOWN")} · ${escapeHtml(r.coverage_limitations || "No limitation recorded")}</p><p><strong>HUMAN CONTEXT</strong><br>Latest decision: ${escapeHtml(r.latest_human_decision || "NONE")}. This Radar item does not change it.</p></div></div>`).join("") : `<p>No canonical ChangeEvent is currently available for Radar projection.</p>`;
  } catch (error) {
    box.innerHTML = `<p>Radar projection unavailable. Canonical research processing is unaffected.</p>`;
  }
}

const renderers = { journey:renderJourney, opportunities:renderOpportunities, evidence:renderEvidence, evolution:renderEvolution, review:renderReview, coverage:renderCoverage, profiles:renderProfiles, telegram:renderTelegram };

function showView(name) {
  document.querySelectorAll(".view").forEach(v => v.classList.remove("active-view"));
  document.querySelectorAll(".nav-item").forEach(v => v.classList.toggle("active", v.dataset.view === name));
  const view = document.getElementById(`view-${name}`);
  if (name !== "today" && renderers[name]) view.innerHTML = renderers[name]();
  view.classList.add("active-view");
  if (name === "evidence") loadProjectEvidence();
  if (name === "review") loadHumanReview();
  if (name === "opportunities") loadProjectOpportunities();
  if (name === "coverage") loadProjectCoverage();
  if (name === "evolution") loadProjectChanges();
  if (name === "telegram") loadProjectRadar();
}

function bindOpenButtons() {
  document.querySelectorAll("[data-open]").forEach(b => b.onclick = () => showView(b.dataset.open));
}

document.getElementById("main-nav").addEventListener("click", e => {
  const button = e.target.closest("[data-view]");
  if (button) showView(button.dataset.view);
});
document.querySelectorAll(".nav-list.small [data-view]").forEach(b => b.addEventListener("click", () => showView(b.dataset.view)));

projectSelect.addEventListener("change", () => { renderLatestPapers(); const active = document.querySelector(".active-view")?.id.replace("view-",""); if (active && active !== "today") showView(active); });
document.getElementById("global-search").addEventListener("keydown", e => { if (e.key === "Enter") showView("evidence"); });

fetch(`${API_BASE}/api/context`, { cache: "no-store" }).then(r => { if (!r.ok) throw new Error(`Context HTTP ${r.status}`); return r.json(); }).then(rows => {
  const profiles = [...new Map(rows.map(r => [r.profile_id, r])).values()];
  profileSelect.innerHTML = profiles.map(r => `<option value="${r.profile_id}">${r.profile_name}</option>`).join("");
  const bindProjects = () => {
    const projects = rows.filter(r => r.profile_id === profileSelect.value);
    projectSelect.innerHTML = projects.map(r => `<option value="${r.project_id}">${r.project_name}</option>`).join("");
    renderLatestPapers();
  };
  profileSelect.onchange = () => { bindProjects(); };
  bindProjects();
  renderDashboard();
  const version = document.getElementById("prototype-version");
  if (version) version.textContent = `Prototype v${PROTOTYPE_VERSION} · live`;
}).catch(error => {
  console.error(error);
  projectSelect.innerHTML = `<option>Context unavailable</option>`;
  const version = document.getElementById("prototype-version");
  if (version) version.textContent = `Prototype v${PROTOTYPE_VERSION} · API error`;
});


async function renderGapDecision(row) {
  const box = document.getElementById("real-gap-decision");
  if (!box) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/decisions`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Decisions HTTP ${response.status}`);
    const all = await response.json();
    const history = all.filter(d => d.primary_research_object_id === row.gap_id);
    const latest = history[0];
    box.innerHTML = latest ? `<p><strong>Latest HUMAN decision:</strong> ${escapeHtml(latest.decision_type)}</p><p>${escapeHtml(latest.rationale)}</p><small>${escapeHtml(latest.actor)} · ${escapeHtml(latest.decided_at)}</small><h4>Change history</h4>${history.map((d, i) => `<div class="trace"><strong>${i === 0 ? "CURRENT · " : "PRIOR · "}${escapeHtml(d.decision_type)}</strong><br>${escapeHtml(d.rationale)}<br><small>${escapeHtml(d.actor)} · ${escapeHtml(d.decided_at)} · Assessment: ${escapeHtml(d.assessment_id || "none")} · Supersedes: ${escapeHtml(d.supersedes_decision_id || "none")}</small></div>`).join("")}` : `<p>No HumanDecision persisted for this candidate.</p>`;
    box.innerHTML += `<div class="human-review-form" style="margin-top:12px"><label>HUMAN reviewer<br><input id="human-review-actor" type="text" placeholder="Researcher name"></label><br><label>Researcher rationale / note<br><textarea id="human-review-rationale" rows="4" placeholder="Why are you taking this action based on the evidence and critic above?"></textarea></label></div><div class="decision-bar" style="margin-top:10px"><button data-decision="REVIEW">Review</button><button data-decision="MODIFY">Modify</button><button data-decision="ACCEPT_DIRECTION">Accept direction</button><button data-decision="REJECT_CANDIDATE">Reject candidate</button><button data-decision="NEED_MORE_EVIDENCE">Need more evidence</button></div><div class="callout warning" style="margin-top:10px">Accept direction means proceed with the current research direction based on current evidence; it does not establish that the gap is true or novel. Only an explicit HUMAN action writes a decision. New decisions supersede history; they do not rewrite it.</div>`;
    box.querySelectorAll("[data-decision]").forEach(btn => btn.onclick = () => submitHumanDecision(row, btn.dataset.decision));
  } catch (error) { box.innerHTML = `<p>Decision API unavailable: ${escapeHtml(error.message)}</p>`; }
}

async function submitHumanDecision(row, decisionType) {
  const actor = document.getElementById("human-review-actor")?.value?.trim();
  const rationale = document.getElementById("human-review-rationale")?.value?.trim();
  if (!actor || !rationale) {
    window.alert("HUMAN reviewer and rationale are required before recording a decision.");
    return;
  }
  const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/decisions`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ object_id: row.gap_id, assessment_id: row.assessment_id || null, decision_type: decisionType, rationale, actor })
  });
  const payload = await response.json();
  if (!response.ok) { window.alert(payload.error || `Decision HTTP ${response.status}`); return; }
  await renderGapDecision(row);
}

async function renderGapAssessment(gap) {
  const box = document.getElementById("real-gap-assessment");
  if (!box) return;
  box.innerHTML = "<p>Loading machine assessment…</p>";
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/assessments`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Assessments HTTP ${response.status}`);
    const rows = (await response.json()).filter(a => a.target_research_object_id === gap.gap_id);
    if (!rows.length) { box.innerHTML = "<p>No persisted Assessment for this GapCandidate yet.</p>"; return; }
    const a = rows[0];
    const dims = (a.dimensions || []).map(d => `<li><strong>${escapeHtml(d.dimension_type)}</strong>: ${escapeHtml(d.value_text ?? d.value_numeric)}<br><small>${escapeHtml(d.explanation || "")}</small></li>`).join("");
    box.innerHTML = `<p><strong>${escapeHtml(a.assessment_type)}</strong></p><p>${escapeHtml(a.explanation_summary || "")}</p><ul>${dims}</ul><div class="callout warning">Machine dimensions are contextual advice, not probabilities or scientific acceptance.</div>`;
  } catch (error) {
    console.error(error);
    box.innerHTML = `<p>Assessment API unavailable: ${escapeHtml(error.message)}</p>`;
  }
}
