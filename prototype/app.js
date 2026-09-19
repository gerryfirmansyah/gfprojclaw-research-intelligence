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
const PROTOTYPE_VERSION = "0.12.5";
const API_BASE = window.location.hostname.endsWith("github.io") ? "https://api.116.212.72.79.nip.io" : "";
const themeToggle = document.getElementById("theme-toggle");

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  const dark = theme === "dark";
  if (themeToggle) {
    themeToggle.textContent = dark ? "☀️ Light" : "🌙 Dark";
    themeToggle.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    themeToggle.setAttribute("aria-pressed", String(dark));
  }
}

const savedTheme = localStorage.getItem("gfprojclaw-theme");
applyTheme(savedTheme === "dark" ? "dark" : "light");
themeToggle?.addEventListener("click", () => {
  const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  localStorage.setItem("gfprojclaw-theme", next);
  applyTheme(next);
});

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
  document.getElementById("change-list").innerHTML = `<div class="change-row"><div class="change-main"><strong>Loading canonical ChangeEvents…</strong><small>Persisted project state</small></div></div>`;
  loadTodayChanges();

  document.getElementById("journey-mini").innerHTML = journeyStages.slice(0, 7).map(([r, name]) => `
    <div class="journey-row"><span class="r-code">${r}</span><div><strong>${name}</strong><small>Workflow guide only · no canonical stage status persisted</small></div><span class="state gray">GUIDE</span></div>`).join("") + `<button class="text-button" data-open="journey">Show R7–R16 guide</button>`;

  document.getElementById("opportunity-table").innerHTML = `<p>Loading canonical research opportunities…</p>`;
  loadTodayOpportunities();

  renderLatestPapers();
  document.querySelectorAll(".metric-card").forEach(el => { el.classList.remove("dummy-surface"); el.classList.add("real-surface"); });
  ["journey-mini"].forEach(id => { const panel = document.getElementById(id)?.closest(".panel"); panel?.classList.remove("dummy-surface"); panel?.classList.add("guide-surface"); });
  ["change-list","opportunity-table","paper-list","evolution-mini","telegram-mini"].forEach(id => document.getElementById(id)?.closest(".panel")?.classList.add("real-surface"));
  document.getElementById("health-mini")?.closest(".panel")?.classList.add("real-surface");
  loadProjectCoverageSummary();
  loadTodayMetrics();
  loadTodayEvolution();
  loadTodayRadar();
  bindOpenButtons();
}

async function loadTodayMetrics() {
  const projectId = projectSelect.value;
  if (!projectId) return;
  const endpoints = ["papers", "decisions", "changes", "coverage", "radar"];
  try {
    const [papers, decisions, changes, coverage, radar] = await Promise.all(endpoints.map(async name => {
      const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectId)}/${name}`, { cache: "no-store" });
      if (!response.ok) throw new Error(`${name} HTTP ${response.status}`);
      return response.json();
    }));
    const setMetric = (id, value, detail) => { const el = document.getElementById(id); if (el) { el.querySelector("strong").textContent = value; el.querySelector("small").textContent = detail; el.classList.remove("dummy-surface"); el.classList.add("real-surface"); } };
    setMetric("metric-papers", papers.length, "Persisted works in selected project");
    setMetric("metric-decisions", decisions.length, "Explicit persisted HUMAN decisions");
    setMetric("metric-changes", changes.length, "Persisted canonical ChangeEvents");
    setMetric("metric-coverage", coverage.coverage_context_id ? 1 : 0, coverage.counter_search_state ? `Counter-search: ${coverage.counter_search_state}` : "No CoverageContext persisted");
    setMetric("metric-radar", radar.length, "Read-only projections from ChangeEvent");
    const pill = document.getElementById("today-coverage-pill");
    if (pill) pill.textContent = coverage.coverage_context_id ? `Coverage persisted · counter-search ${coverage.counter_search_state || "UNKNOWN"}` : "No persisted CoverageContext";
  } catch (error) {
    document.querySelectorAll(".metric-card").forEach(el => { el.querySelector("strong").textContent = "—"; el.querySelector("small").textContent = `Canonical metric unavailable: ${error.message}`; });
  }
}

async function loadTodayRadar() {
  const box = document.getElementById("telegram-mini");
  if (!box || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/radar`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const rows = await response.json();
    box.innerHTML = rows.length ? rows.slice(0, 4).map(r => `<div class="telegram-row"><time>${escapeHtml(r.observed_at || "")}</time><strong>${escapeHtml(r.change_type)} — ${escapeHtml(r.canonical_label)}</strong></div>`).join("") : `<p>No canonical Radar item yet.</p>`;
  } catch (error) { box.innerHTML = `<p>Radar projection unavailable: ${escapeHtml(error.message)}</p>`; }
}

async function loadTodayEvolution() {
  const box = document.getElementById("evolution-mini");
  if (!box || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/changes`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const rows = await response.json();
    box.innerHTML = rows.length ? rows.slice(0, 4).map(r => `<div class="evolution-row"><div><strong>${escapeHtml(r.canonical_label || r.primary_research_object_id)}</strong><small>${escapeHtml(r.change_type)} · ${escapeHtml(r.reasoning_delta || "No reasoning delta recorded")}</small></div><small>${escapeHtml(r.observed_at || "")}</small></div>`).join("") : `<p>No persisted evolution event yet.</p>`;
  } catch (error) { box.innerHTML = `<p>Canonical evolution unavailable: ${escapeHtml(error.message)}</p>`; }
}

async function loadTodayOpportunities() {
  const box = document.getElementById("opportunity-table");
  if (!box || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/opportunities`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const rows = await response.json();
    box.innerHTML = rows.length ? `<table class="table"><thead><tr><th>Candidate</th><th>Evidence</th><th>Counter-search</th><th>State</th></tr></thead><tbody>${rows.slice(0, 5).map(r => `<tr><td><strong>${escapeHtml(r.canonical_label || r.gap_id)}</strong><br><small>${escapeHtml(r.statement || "No statement recorded")}</small></td><td>${escapeHtml(r.support_count)} support · ${escapeHtml(r.challenge_count)} challenge</td><td>${escapeHtml(r.counter_search_state || "NOT_RECORDED")}</td><td><span class="state ${stateClass(r.current_evolution_state || "CANDIDATE")}">${escapeHtml(r.current_evolution_state || "CANDIDATE")}</span></td></tr>`).join("")}</tbody></table>` : `<p>No canonical research opportunity persisted for this project yet.</p>`;
  } catch (error) {
    box.innerHTML = `<p>Canonical opportunities unavailable: ${escapeHtml(error.message)}</p>`;
  }
}

async function loadTodayChanges() {
  const box = document.getElementById("change-list");
  if (!box || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/changes`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const rows = await response.json();
    box.innerHTML = rows.length ? rows.slice(0, 5).map(r => `<div class="change-row"><div class="change-main"><strong>${escapeHtml(r.change_type)} — ${escapeHtml(r.canonical_label || r.primary_research_object_id)}</strong><small>${escapeHtml(r.reasoning_delta || "No reasoning delta recorded")} · ${escapeHtml(r.observed_at || "time unknown")}</small></div><span class="state blue">CANONICAL</span></div>`).join("") : `<p>No persisted ChangeEvent for this project yet.</p>`;
  } catch (error) {
    box.innerHTML = `<p>Canonical ChangeEvents unavailable: ${escapeHtml(error.message)}</p>`;
  }
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
  <div class="detail-grid" style="margin-top:14px"><div class="card real-surface"><h3>Research Object Detail</h3><div id="real-gap-detail">Select a persisted opportunity.</div></div><div class="card real-surface"><h3>Evidence & Coverage</h3><div id="real-gap-relationship">No evidence context loaded yet.</div></div><div class="card real-surface"><h3>Advisory Dimensions</h3><div id="real-gap-assessment">Select a persisted opportunity.</div></div><div class="card real-surface"><h3>Advice & Critic</h3><div id="real-gap-critic">Select a persisted opportunity.</div></div><div class="card real-surface"><h3>Research Quality <span class="data-badge real">REAL DATA</span></h3><div id="real-gap-quality">Select a persisted research object.</div></div><div class="card real-surface"><h3>Evidence Verification <span class="data-badge real">REAL DATA</span></h3><div id="real-gap-verification">Select a persisted research object.</div></div><div class="card real-surface"><h3>HUMAN Authority</h3><div id="real-gap-decision">Select a persisted opportunity.</div></div></div>`;
}

async function loadProjectOpportunities() {
  const list = document.getElementById("real-gap-list"), detail = document.getElementById("real-gap-detail");
  const relation = document.getElementById("real-gap-relationship"), decision = document.getElementById("real-gap-decision");
  if (!list || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/research-objects`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Research Objects HTTP ${response.status}`);
    const rows = await response.json();
    if (!rows.length) { list.innerHTML = "<p>No active canonical research objects for this project yet.</p>"; detail.innerHTML = "<p>Nothing to inspect yet.</p>"; relation.innerHTML = "<p>No canonical evidence relationship is implied.</p>"; decision.innerHTML = "<p>No research object available for HUMAN review.</p>"; return; }
    list.innerHTML = rows.map((r,i) => `<div class="change-row" data-object-index="${i}"><div class="change-main"><strong>${escapeHtml(r.canonical_label)}</strong><small>${escapeHtml(r.object_type)} · ${escapeHtml(r.object_state)}</small></div><span class="state ${stateClass(r.object_state)}">${escapeHtml(r.object_state)}</span></div>`).join("");
    const show = async r => {
      const isGap = r.object_type === "GAP_CANDIDATE";
      detail.innerHTML = `<p><strong>Statement:</strong> ${escapeHtml(r.statement)}</p><p><strong>Object type:</strong> ${escapeHtml(r.object_type)}</p>${isGap ? `<p><strong>Gap type:</strong> ${escapeHtml(r.gap_type)}</p>` : ""}<p><strong>State:</strong> ${escapeHtml(r.object_state)}</p><p><strong>Scientific status:</strong> ${escapeHtml(r.scope_jsonb?.scientific_status || (isGap ? "GAP_CANDIDATE_REQUIRES_HUMAN_VALIDATION" : "NOT_RECORDED"))}</p>`;
      relation.innerHTML = isGap ? `<p>Loading persisted gap evidence relationships…</p>` : `<p><strong>Evidence relationship status:</strong> none implied by this projection.</p><p>Review canonical EvidenceFragment and Claim records in Evidence Explorer. An Investigation Direction is not evidence of a gap, novelty, or causal mechanism.</p><div class="callout warning">EvidenceRelationships must be explicitly persisted and reviewed; this screen does not infer SUPPORTS or CHALLENGES.</div>`;
      document.getElementById("real-gap-assessment").innerHTML = isGap ? `<p>Loading persisted assessment…</p>` : `<p>No assessment is required to display this HUMAN-selected investigation direction.</p>`;
      document.getElementById("real-gap-critic").innerHTML = isGap ? `<p>Loading persisted Advice & Critic…</p>` : `<p>Advice & Critic has not been generalized for Investigation Direction. Continue evidence screening without treating this absence as a global lock.</p>`;
      if (isGap) { const legacy = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/opportunities`, {cache:"no-store"}); const oldRows = legacy.ok ? await legacy.json() : []; const old = oldRows.find(x => x.gap_id === r.research_object_id); if (old) { Object.assign(r, old); const trace = Array.isArray(old.evidence_trace) ? old.evidence_trace : []; relation.innerHTML = `<p><strong>Persisted evidence links:</strong> ${escapeHtml(old.support_count)} supporting · ${escapeHtml(old.challenge_count)} challenging · ${escapeHtml(old.linked_claim_count)} linked claim(s)</p><p><strong>Counter-search:</strong> ${escapeHtml(old.counter_search_state || "NOT_RECORDED")}</p><p><strong>Coverage limitation:</strong> ${escapeHtml(old.coverage_limitations || "Not recorded")}</p>${trace.length ? trace.map(t => { const links = (Array.isArray(t.work_identifiers) ? t.work_identifiers : []).map(i => i.type === "DOI" ? `<a class="source-link source-link-doi" href="${escapeHtml(`https://doi.org/${i.value}`)}" target="_blank" rel="noopener noreferrer" title="Open DOI source">DOI ↗</a>` : i.type === "OPENALEX" ? `<a class="source-link source-link-openalex" href="${escapeHtml(`https://openalex.org/${i.value}`)}" target="_blank" rel="noopener noreferrer" title="Open in OpenAlex">OpenAlex ↗</a>` : "").filter(Boolean).join(" · "); const access = t.access_level || "NOT_RECORDED"; const accessNote = access === "ABSTRACT_ONLY" ? " — limited evidence access" : access === "METADATA_ONLY" ? " — metadata only; no text evidence" : ""; return `<div class="trace"><strong>${escapeHtml(t.semantic_type)}</strong> · ${escapeHtml(t.work_title)} <span class="access-badge ${access === "FULL_TEXT" ? "full" : "limited"}">${escapeHtml(access)}${escapeHtml(accessNote)}</span>${links ? ` · ${links}` : ""}<br><small>SourceRecord: ${escapeHtml(t.source_identifier || t.source_record_id)} · EvidenceFragment: ${escapeHtml(t.evidence_fragment_id)} · Claim: ${escapeHtml(t.claim_text)}</small></div>`; }).join("") : `<p>No canonical evidence trace persisted.</p>`}`; await renderGapCritic(r); await renderGapAssessment(r); } }
      await renderResearchQuality(r);
      await renderEvidenceVerification(r);
      await renderGapDecision(r);
    };
    document.querySelectorAll("[data-object-index]").forEach(el => el.onclick = () => show(rows[Number(el.dataset.objectIndex)]));
    await show(rows[0]);
  } catch (error) { console.error(error); list.innerHTML = `<p>Research Objects API unavailable: ${escapeHtml(error.message)}</p>`; }
}

async function renderGapCritic(gap) {
  const box = document.getElementById("real-gap-critic");
  if (!box || !projectSelect.value) return;
  box.innerHTML = "<p>Loading persisted Advice & Critic…</p>";
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/advice-critic`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Advice & Critic HTTP ${response.status}`);
    const rows = await response.json();
    const critic = rows.find(r => r.gap_id === gap.gap_id);
    if (!critic) { box.innerHTML = "<p>No persisted J10 Advice & Critic assessment for this candidate.</p>"; return; }
    gap.assessment_id = critic.assessment_id || null;
    const dimensions = Array.isArray(critic.dimensions) ? critic.dimensions : [];
    const evidence = Array.isArray(critic.evidence_basis) ? critic.evidence_basis : [];
    const dimensionCards = dimensions.map(d => `<div class="trace"><strong>${escapeHtml(d.dimension_type)} — ${escapeHtml(d.value_text || "NOT_RECORDED")}</strong><p>${escapeHtml(d.explanation || "Explanation unavailable from current canonical assessment.")}</p></div>`).join("");
    const evidenceCards = evidence.length ? evidence.map(e => `<div class="trace"><strong>${escapeHtml(e.semantic_type)} · ${escapeHtml(e.work_title || "Work unavailable")}</strong><p><strong>Claim under review:</strong> ${escapeHtml(e.claim_text || "Claim unavailable")}</p><p><strong>Why linked:</strong> ${escapeHtml(e.relationship_rationale || "Relationship rationale unavailable.")}</p><small>Evidence access: ${escapeHtml(e.access_level || "NOT_RECORDED")} · Claim: ${escapeHtml(e.claim_review_state || "NOT_RECORDED")} · Relationship: ${escapeHtml(e.relationship_review_state || "NOT_RECORDED")}</small></div>`).join("") : "<p>No explicit canonical evidence relationship is available as a basis for this Advice & Critic assessment.</p>";
    box.innerHTML = `<p><strong>Advice & Critic assessment</strong></p><p>${escapeHtml(critic.explanation_summary || "Explanation summary unavailable from current canonical assessment.")}</p><div class="trace"><strong>Assessment target</strong><p>${escapeHtml(critic.canonical_label || critic.statement || "Research Object unavailable")} · ${escapeHtml(critic.gap_type || "TYPE_NOT_RECORDED")}</p><p>This assessment applies to the Research Object and its currently linked canonical evidence set; it is not an assessment of an individual paper.</p><small>Evidence scope: ${escapeHtml(critic.linked_claim_count ?? 0)} linked Claim(s) · ${escapeHtml(critic.support_count ?? 0)} SUPPORTS · ${escapeHtml(critic.challenge_count ?? 0)} CHALLENGES/CONTRADICTS</small></div><p><strong>Reviewable machine reasoning</strong></p>${dimensionCards}<p><strong>Canonical evidence basis</strong></p>${evidenceCards}<p><strong>Coverage / unresolved limitation</strong></p><p>Counter-search: ${escapeHtml(critic.counter_search_state || "NOT_RECORDED")}. ${escapeHtml(critic.coverage_limitations || "No additional coverage limitation is recorded.")}</p><div class="callout warning">Verify the explanation against Evidence Verification and the external source before accepting any stronger scientific claim. Advice & Critic does not establish novelty, truth, acceptance, or a scientific verdict.</div>`;
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

async function loadHumanReviewBadge() {
  const badge = document.getElementById("human-review-badge"); if (!badge) return;
  try { const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/evidence`, {cache:"no-store"}); if (!response.ok) throw new Error(`HTTP ${response.status}`); const rows = await response.json(); badge.textContent = rows.filter(r => r.review_state === "NEEDS_REVIEW" || r.review_state === "CONTESTED").length; }
  catch (error) { badge.textContent = "?"; }
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
  return commonHeader("Telegram Research Radar", "Read-only projection of canonical ChangeEvent. Telegram never becomes scientific state.", "real") + `
  <div id="pilot-health-live" class="card"><p>Loading Continuous Pilot health…</p></div>
  <div id="radar-live" class="card"><p>Loading canonical Radar projection…</p></div>
  <div class="card"><h3>Radar Rules</h3><ul><li>No raw crawler logs</li><li>No automatic scientific decisions</li><li>No canonical state in Telegram</li><li>Delivery failure stays local</li><li>Inspect full context in Dashboard</li></ul></div>`;
}

async function loadPilotHealth() {
  const box = document.getElementById("pilot-health-live"); if (!box) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/pilot-health`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`); const rows = await response.json();
    box.innerHTML = `<h3>Continuous Pilot Health</h3><p class="muted">Operational health only — never a scientific judgment.</p>` + (rows.length ? rows.map(r => `<div class="change-row"><div class="change-main"><strong>${escapeHtml(r.status)} · ${escapeHtml(r.trigger_type)}</strong><small>Run ${escapeHtml(r.pilot_run_id)}</small><p>Started: ${escapeHtml(r.started_at)}<br>Finished: ${escapeHtml(r.finished_at || "RUNNING")}<br>Stage attempts: ${escapeHtml(r.stage_attempts)} · Failed attempts: ${escapeHtml(r.failed_stage_attempts)}</p><p>Stage history: ${escapeHtml((r.stage_history || []).join(" → ") || "none")}</p><p>Machine actions: ${escapeHtml(JSON.stringify(r.machine_actions_jsonb || []))}</p></div></div>`).join("") : `<p>No Continuous Pilot run recorded yet.</p>`);
  } catch (error) { box.innerHTML = `<h3>Continuous Pilot Health</h3><p>Operational health unavailable; canonical scientific state is unaffected.</p>`; }
}

async function loadProjectRadar() {
  const box = document.getElementById("radar-live");
  if (!box) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/radar`, { cache: "no-store" });
    const rows = response.ok ? await response.json() : [];
    box.innerHTML = rows.length ? rows.map(r => `<div class="change-row"><div class="change-main"><strong>${escapeHtml(r.change_type)}</strong><small>${escapeHtml(r.profile_name)} / ${escapeHtml(r.project_name)}</small><p><strong>WHAT CHANGED</strong><br>${escapeHtml(r.canonical_label)}</p><p><strong>WHY IT MATTERS</strong><br>${escapeHtml(r.reasoning_delta)}</p><p><strong>COVERAGE</strong><br>Counter-search: ${escapeHtml(r.counter_search_state || "UNKNOWN")} · ${escapeHtml(r.coverage_limitations || "No limitation recorded")}</p><p><strong>HUMAN CONTEXT</strong><br>Latest decision: ${escapeHtml(r.latest_human_decision || "NONE")}. This Radar item does not change it.</p><button class="text-button" onclick="showView('opportunities')">Investigate evidence & source</button></div></div>`).join("") : `<p>No canonical ChangeEvent is currently available for Radar projection.</p>`;
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
  if (name === "telegram") { loadPilotHealth(); loadProjectRadar(); }
}

function bindOpenButtons() {
  document.querySelectorAll("[data-open]").forEach(b => b.onclick = () => showView(b.dataset.open));
}

document.getElementById("main-nav").addEventListener("click", e => {
  const button = e.target.closest("[data-view]");
  if (button) showView(button.dataset.view);
});
document.querySelectorAll(".nav-list.small [data-view]").forEach(b => b.addEventListener("click", () => showView(b.dataset.view)));

projectSelect.addEventListener("change", () => { loadHumanReviewBadge(); const active = document.querySelector(".active-view")?.id.replace("view-",""); if (!active || active === "today") renderDashboard(); else showView(active); });
document.getElementById("global-search").addEventListener("keydown", e => { if (e.key === "Enter") showView("evidence"); });

fetch(`${API_BASE}/api/context`, { cache: "no-store" }).then(r => { if (!r.ok) throw new Error(`Context HTTP ${r.status}`); return r.json(); }).then(rows => {
  const profiles = [...new Map(rows.map(r => [r.profile_id, r])).values()];
  profileSelect.innerHTML = profiles.map(r => `<option value="${r.profile_id}">${r.profile_name}</option>`).join("");
  const bindProjects = () => {
    const projects = rows.filter(r => r.profile_id === profileSelect.value);
    projectSelect.innerHTML = projects.map(r => `<option value="${r.project_id}">${r.project_name}</option>`).join("");
    renderLatestPapers();
  };
  profileSelect.onchange = () => { bindProjects(); loadHumanReviewBadge(); const active = document.querySelector(".active-view")?.id.replace("view-",""); if (!active || active === "today") renderDashboard(); else showView(active); };
  bindProjects();
  renderDashboard();
loadHumanReviewBadge();
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
    const history = all.filter(d => d.primary_research_object_id === (row.research_object_id || row.gap_id));
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
    body: JSON.stringify({ object_id: row.research_object_id || row.gap_id, assessment_id: row.assessment_id || null, decision_type: decisionType, rationale, actor })
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

async function renderResearchQuality(row) {
  const box = document.getElementById("real-gap-quality");
  if (!box || !projectSelect.value || !row?.research_object_id) return;
  box.innerHTML = "<p>Loading canonical quality observations…</p>";
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/quality?object_id=${encodeURIComponent(row.research_object_id)}`, {cache:"no-store"});
    if (!response.ok) throw new Error(`Quality HTTP ${response.status}`);
    const q = await response.json();
    const observations = Array.isArray(q.observations) ? q.observations : [];
    const limitations = Array.isArray(q.limitations) ? q.limitations : [];
    const suggestions = Array.isArray(q.review_suggestions) ? q.review_suggestions : [];
    const fmt = value => value == null ? "—" : (typeof value === "string" ? value : JSON.stringify(value));
    box.innerHTML = `
      <div class="callout warning">Quality observations are decomposed advisory context, not a universal score or scientific verdict.</div>
      ${observations.map(o => `<div class="trace"><strong>${escapeHtml(o.dimension)}</strong> · <span class="state ${stateClass(o.state)}">${escapeHtml(o.state)}</span><br><small>${escapeHtml(fmt(o.value))}</small><br><small>Basis: ${escapeHtml(o.basis || "Not recorded")}</small></div>`).join("")}
      <p><strong>Limitations</strong></p>${limitations.length ? `<ul>${limitations.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>` : "<p>No additional limitation recorded by this projection.</p>"}
      <p><strong>Suggested HUMAN review actions</strong></p>${suggestions.length ? suggestions.map(x => `<div class="trace"><strong>${escapeHtml(x.action)}</strong><br><small>Because: ${escapeHtml((x.because || []).join("; "))}</small></div>`).join("") : "<p>No quality-triggered review suggestion.</p>"}
      <div class="callout warning">scientific_decision=${escapeHtml(String(q.scientific_decision))}. HUMAN scientific authority remains explicit.</div>`;
  } catch (error) {
    box.innerHTML = `<p>Research Quality unavailable: ${escapeHtml(error.message)}</p>`;
  }
}

async function renderEvidenceVerification(row) {
  const box=document.getElementById("real-gap-verification");
  if(!box || !projectSelect.value || !row?.research_object_id) return;
  box.innerHTML="<p>Loading inspectable canonical evidence…</p>";
  try {
    const response=await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/evidence-verification?object_id=${encodeURIComponent(row.research_object_id)}`,{cache:"no-store"});
    if(!response.ok) throw new Error(`Evidence verification HTTP ${response.status}`);
    const rows=await response.json();
    box.innerHTML=`<div class="callout warning">Read what is actually stored before judging a Claim or relationship. PROJECT_LITERATURE_ONLY is candidate context, not evidence for this research object. ABSTRACT_ONLY is not full text.</div>`+
      rows.map((x,i)=>{
        const links=[x.doi_url ? `<a class="source-link source-link-doi" href="${escapeHtml(x.doi_url)}" target="_blank" rel="noopener noreferrer">DOI ↗</a>`:"",x.openalex_url ? `<a class="source-link source-link-openalex" href="${escapeHtml(x.openalex_url)}" target="_blank" rel="noopener noreferrer">OpenAlex ↗</a>`:""].filter(Boolean).join(" · ");
        const text=x.evidence_text ? `<details ${i===0 ? "open":""}><summary>Read stored ${escapeHtml(x.fragment_type || "evidence fragment")} (${escapeHtml(x.access_level || "UNKNOWN")})</summary><p class="evidence-readable">${escapeHtml(x.evidence_text)}</p></details>` : `<p><em>No canonical EvidenceFragment text is stored for this work.</em></p>`;
        const claim=x.claim_id ? `<p><strong>Extracted Claim:</strong> ${escapeHtml(x.claim_text)}<br><small>Claim review: ${escapeHtml(x.claim_review_state)} · extraction: ${escapeHtml(x.extraction_origin)}</small></p>` : "<p><strong>Extracted Claim:</strong> none stored.</p>";
        const rel=x.relationship_id ? `<p><strong>Object relationship:</strong> ${escapeHtml(x.semantic_type)} · ${escapeHtml(x.relationship_review_state)}</p>` : "<p><strong>Object relationship:</strong> none asserted.</p>";
        return `<div class="trace"><strong>${escapeHtml(x.title)}</strong><br><small>${escapeHtml(x.publication_year || "Year unavailable")} · ${escapeHtml(x.object_evidence_status)} · ${escapeHtml(x.access_level || x.current_access_level || "METADATA_ONLY")}</small>${links ? `<p>${links}</p>`:""}${text}${claim}${rel}</div>`;
      }).join("")+
      `<div class="callout warning">External DOI/OpenAlex links are for HUMAN source inspection. This screen does not claim access to publisher full text unless canonical access_level is FULL_TEXT.</div>`;
  } catch(error) {
    box.innerHTML=`<p>Evidence Verification unavailable: ${escapeHtml(error.message)}</p>`;
  }
}
