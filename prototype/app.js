const data = {
  A: {
    projects: ["Cross-agency Digital Government Governance", "Enterprise Architecture Capability Study"],
    changes: [
      ["GAP-014", "New paper menantangs the broad governance-capability formulation", "CONTESTED", "red"],
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
      ["THEORY-006", "Competing explanation gains mendukung", "NEEDS REVIEW", "yellow"],
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
  ["R0", "Research Intent", "DITINJAU HUMAN", "green"],
  ["R1", "Research Landscape", "MATANG", "green"],
  ["R2", "Bukti Mapping", "BUKTI BERTUMBUH", "blue"],
  ["R3", "Problem Formulation", "BERKEMBANG", "blue"],
  ["R4", "Gap Formation", "PERLU PERHATIAN", "red"],
  ["R5", "Gap Falsification", "BUKTI BERTUMBUH", "blue"],
  ["R6", "Theory Positioning", "PERLU PERHATIAN", "red"],
  ["R7", "Research Question", "BERKEMBANG", "blue"],
  ["R8", "Conceptualization", "BERKEMBANG", "blue"],
  ["R9", "Method Intelligence", "BUKTI BERTUMBUH", "blue"],
  ["R10", "Research Design", "BELUM DIMULAI", "gray"],
  ["R11", "Contribution Formation", "BERKEMBANG", "blue"],
  ["R12", "Novelty Challenge", "PERLU PERHATIAN", "red"],
  ["R13", "Bukti & Argument Audit", "BELUM DIMULAI", "gray"],
  ["R14", "Adversarial Review", "BELUM DIMULAI", "gray"],
  ["R15", "Scholarly Positioning", "BERKEMBANG", "blue"],
  ["R16", "Research Readiness", "BERKEMBANG", "blue"]
];

const health = [
  ["OpenAlex", "HEALTHY", "green", "78% of configured discovery executed"],
  ["Semantic Scholar", "DEGRADED", "yellow", "Citation expansion limited"],
  ["Crossref", "HEALTHY", "green", "Metadata discovery current"],
  ["Full-text extraction", "HEALTHY", "green", "48% of current project corpus"]
];

const evolution = [
  ["GAP-014", "STRENGTHENING → CONTESTED", "2h ago"],
  ["GAP-009", "Bukti increased", "6h ago"],
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
const PROTOTYPE_VERSION = "0.17.1";
const API_BASE = window.location.hostname.endsWith("github.io") ? "https://api.116.212.72.79.nip.io" : "";


// Presentation-only Indonesian translations for persisted machine-authored scientific prose.
// Canonical API/DB values remain unchanged and source-origin titles/evidence excerpts stay original.
const presentationId = new Map(Object.entries({
  "Candidate: empirical and explanatory specificity in AI public governance":"Kandidat: kekhususan empiris dan eksplanatori dalam tata kelola publik berbasis AI",
  "Current synthesized evidence suggests that empirical and explanatory research focused on specific forms of AI in public governance may remain underdeveloped.":"Bukti sintesis saat ini menunjukkan bahwa riset empiris dan eksplanatori yang berfokus pada bentuk-bentuk spesifik AI dalam tata kelola publik mungkin masih kurang berkembang.",
  "The reviewed literature is described as largely exploratory, conceptual, qualitative, and practice-driven, motivating more public-sector-focused, empirical, multidisciplinary, and explanatory research on specific forms of AI.":"Literatur yang ditinjau digambarkan sebagian besar bersifat eksploratif, konseptual, kualitatif, dan didorong praktik; hal ini mendorong riset yang lebih berfokus pada sektor publik, empiris, multidisipliner, dan eksplanatori mengenai bentuk-bentuk spesifik AI.",
  "Coverage reflects the current persisted project slice only; discovery breadth and counter-search are not yet complete.":"Cakupan hanya mencerminkan bagian proyek yang saat ini tersimpan; keluasan discovery dan pencarian pembanding belum lengkap.",
  "Research-opportunity prioritization is advisory context only; HUMAN scientific judgment remains authoritative.":"Prioritas peluang riset hanya merupakan konteks saran; penilaian ilmiah HUMAN tetap menjadi otoritas.",
  "Current evidence slice does not support a defensible method-feasibility judgment.":"Bagian bukti saat ini belum mendukung penilaian kelayakan metode yang dapat dipertanggungjawabkan.",
  "Novelty is not established; counter/prior-solution search state is NOT_RUN.":"Kebaruan belum ditetapkan; status pencarian pembanding/solusi terdahulu adalah NOT_RUN.",
  "Advisory attention signal from 1 supporting and 0 challenging persisted relationship(s).":"Sinyal perhatian bersifat saran berdasarkan 1 relasi pendukung dan 0 relasi penantang yang tersimpan.",
  "Current evidence slice does not support a defensible theory-significance judgment.":"Bagian bukti saat ini belum mendukung penilaian signifikansi teori yang dapat dipertanggungjawabkan.",
  "Advice & Critic surfaces weaknesses and falsification work; it is not a scientific verdict and HUMAN authority remains explicit.":"Saran & Kritik menampilkan kelemahan dan pekerjaan falsifikasi; ini bukan keputusan ilmiah dan otoritas HUMAN tetap eksplisit.",
  "Persisted relationships: 1 supporting, 0 challenging/contradicting; this is observed evidence balance, not a truth probability.":"Relasi tersimpan: 1 mendukung, 0 menantang/bertentangan; ini adalah keseimbangan bukti yang diamati, bukan probabilitas kebenaran.",
  "Advice & Critic recommendation only; falsification work should precede stronger claims and HUMAN scientific judgment remains authoritative.":"Ini hanya rekomendasi Saran & Kritik; pekerjaan falsifikasi perlu mendahului Claim yang lebih kuat dan penilaian ilmiah HUMAN tetap menjadi otoritas.",
  "Single abstract-derived claim is consistent with this tentative synthesis gap; HUMAN review required.":"Satu Claim yang diturunkan dari abstrak konsisten dengan gap sintesis tentatif ini; tinjauan HUMAN diperlukan."
}));
const presentId = value => value == null ? value : (presentationId.get(String(value)) || String(value));
const canonicalWithId = value => {
  if (value == null) return "";
  const original=String(value), translated=presentId(original);
  return translated === original ? escapeHtml(original) : `<span class="presentation-translation">${escapeHtml(translated)}</span><details class="canonical-original"><summary>Lihat teks canonical asli</summary><p>${escapeHtml(original)}</p></details>`;
};
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

const WORKSPACE_THEMES = ["light","dark","research-blue","scholar-green","executive-indigo"];
const savedTheme = localStorage.getItem("gfprojclaw-theme");
applyTheme(WORKSPACE_THEMES.includes(savedTheme) ? savedTheme : "light");
themeToggle?.addEventListener("click", () => {
  const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  localStorage.setItem("gfprojclaw-theme", next);
  applyTheme(next);
});
function applyProfileTheme(rows){
  if(localStorage.getItem("gfprojclaw-theme")) return;
  const ctx=rows.find(r=>r.profile_id===profileSelect.value);
  const preferred=ctx?.profile_configuration_jsonb?.workspace_theme;
  if(WORKSPACE_THEMES.includes(preferred)) applyTheme(preferred);
}

function selectedDummyData() {
  const idx = Math.max(0, profileSelect.selectedIndex);
  return Object.values(data)[idx] || Object.values(data)[0];
}

function selectedProjectLabel() {
  return projectSelect.selectedOptions[0]?.textContent || "Proyek terpilih";
}

function stateClass(label) {
  if (/CONTESTED|CHALLENGED|NEEDS ATTENTION|PERLU PERHATIAN/i.test(label)) return "red";
  if (/STRENGTH|MATURE|HUMAN REVIEWED|HEALTHY|MATANG|DITINJAU HUMAN/i.test(label)) return "green";
  if (/POSSIBLY|DEGRADED|REVIEW|TINJAU/i.test(label)) return "yellow";
  if (/NOT STARTED|BELUM DIMULAI/i.test(label)) return "gray";
  return "blue";
}

function renderProjects() {
  projectSelect.innerHTML = data[profileSelect.value].projects.map(x => `<option>${x}</option>`).join("");
}

function renderDashboard() {
  document.getElementById("change-list").innerHTML = `<div class="change-row"><div class="change-main"><strong>Memuat ChangeEvent canonical…</strong><small>Status proyek tersimpan</small></div></div>`;
  loadTodayChanges();

  document.getElementById("journey-mini").innerHTML = journeyStages.slice(0, 7).map(([r, name], index) => `
    <div class="journey-row"><span class="r-code">${r}</span><div><strong>${escapeHtml(window.GF_I18N?.stageName(index) || name)}</strong><small>${escapeHtml(window.GF_I18N?.stageShortDescription?.(index) || window.GF_I18N?.stageDescription?.(index) || "")}</small></div><span class="state gray">GUIDE</span></div>`).join("") + `<button class="text-button" data-open="journey">${escapeHtml(window.GF_I18N?.t("showRemainingStages") || "Show R7–R16 guide")}</button>`;

  document.getElementById("opportunity-table").innerHTML = `<p>Memuat peluang riset canonical…</p>`;
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

let todayMetricMembers = {};

function sourceLinks(identifiers = {}) {
  const links = [];
  if (identifiers.DOI) links.push(`<a class="source-link source-link-doi" href="https://doi.org/${escapeHtml(identifiers.DOI)}" target="_blank" rel="noopener noreferrer">DOI ↗</a>`);
  if (identifiers.OPENALEX) links.push(`<a class="source-link source-link-openalex" href="https://openalex.org/${escapeHtml(identifiers.OPENALEX)}" target="_blank" rel="noopener noreferrer">OpenAlex ↗</a>`);
  return links.join(" · ");
}

function renderMetricMember(kind, item) {
  if (kind === "papers") {
    const links = sourceLinks(item.identifiers || {});
    return `<div class="metric-member"><div class="paper-title">${escapeHtml(item.title || "Karya tanpa judul")}</div><p>${escapeHtml(item.publication_year || "Tahun tidak diketahui")} · ${escapeHtml(item.venue_name || "Venue tidak diketahui")} · ${escapeHtml(item.current_access_level || "ACCESS_NOT_RECORDED")}</p><small>Work: ${escapeHtml(item.work_id)} · Tinjauan: ${escapeHtml(item.human_review_state || item.relevance_state || "NOT_RECORDED")} · Sumber: ${escapeHtml(item.source_key || "NOT_RECORDED")}</small>${links ? `<p>${links}</p>` : ""}</div>`;
  }
  if (kind === "decisions") return `<div class="metric-member"><span class="trace-label">${escapeHtml(item.decision_type || "Keputusan HUMAN")}</span><p>${escapeHtml(item.rationale || "Tidak ada alasan yang direkam")}</p><small>Keputusan: ${escapeHtml(item.decision_id || item.id || "ID_NOT_RECORDED")} · Aktor: ${escapeHtml(item.actor || "NOT_RECORDED")} · ${escapeHtml(item.decided_at || "waktu tidak diketahui")}</small></div>`;
  if (kind === "changes") return `<div class="metric-member"><span class="trace-label">${escapeHtml(item.change_type)}</span><p>${escapeHtml(item.canonical_label || item.primary_research_object_id)}</p><small>ChangeEvent: ${escapeHtml(item.change_event_id || item.id || "ID_NOT_RECORDED")} · ${escapeHtml(item.reasoning_delta || "Tidak ada delta penalaran yang direkam")} · ${escapeHtml(item.observed_at || "waktu tidak diketahui")}</small></div>`;
  if (kind === "coverage") return `<div class="metric-member"><span class="trace-label">CoverageContext</span><p>Pencarian pembanding: ${escapeHtml(item.counter_search_state || "UNKNOWN")}</p><small>Context: ${escapeHtml(item.coverage_context_id)} · ${escapeHtml(item.limitations || "Tidak ada keterbatasan yang direkam")}</small></div>`;
  if (kind === "radar") return `<div class="metric-member"><span class="trace-label">${escapeHtml(item.change_type || "Item Radar")}</span><p>${escapeHtml(item.canonical_label || "Proyeksi canonical")}</p><small>${escapeHtml(item.observed_at || "waktu tidak diketahui")} · proyeksi read-only ChangeEvent</small></div>`;
  return "";
}

let pendingObjectId=null;
async function openObjectVerification(objectId){
  pendingObjectId=objectId||null;
  if(!pendingObjectId && projectSelect.value){
    try{const r=await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/research-objects`,{cache:"no-store"}); if(r.ok){const rows=await r.json(); if(rows.length===1) pendingObjectId=rows[0].research_object_id;}}catch(_){/* verification screen will expose unavailable state */}
  }
  showView("opportunities");
}

function showMetricMembers(kind) {
  const panel=document.getElementById("metric-members"), list=document.getElementById("metric-members-list"), title=document.getElementById("metric-members-title"), summary=document.getElementById("metric-members-summary");
  if (!panel || !list) return;
  const config=todayMetricMembers[kind]; if (!config) return;
  title.textContent=`${config.label} — ${config.items.length} canonical member${config.items.length === 1 ? "" : "s"}`;
  summary.textContent=config.summary;
  list.innerHTML=config.items.length ? config.items.map(item=>renderMetricMember(kind,item)).join("") : `<p>Tidak ada anggota canonical yang tersimpan untuk metrik ini.</p>`;
  panel.hidden=false; panel.scrollIntoView({behavior:"smooth",block:"nearest"});
}

async function loadTodayMetrics() {
  const projectId = projectSelect.value;
  if (!projectId) return;
  const endpoints = ["papers", "decisions", "changes", "coverage", "radar", "corpus-layers"];
  try {
    const [papers, decisions, changes, coverage, radar, corpusLayers] = await Promise.all(endpoints.map(async name => {
      const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectId)}/${name}`, { cache: "no-store" });
      if (!response.ok) throw new Error(`${name} HTTP ${response.status}`);
      return response.json();
    }));
    const id=window.GF_I18N?.current?.() === "id";
    todayMetricMembers={
      papers:{label:window.GF_I18N?.t("persistedPapers") || "Persisted Papers",items:papers,summary:id?"Work tersimpan persis dalam proyek terpilih. Judul paper dan identifier eksternal ditampilkan bila tersedia secara canonical.":"Exact persisted karya in the selected project. Paper titles and external identifiers are shown when canonically available."},
      decisions:{label:window.GF_I18N?.t("humanDecisions") || "HUMAN Decisions",items:decisions,summary:id?"Keputusan HUMAN tersimpan persis yang dikembalikan untuk proyek terpilih.":"Exact explicit persisted Keputusan HUMANs returned for the selected project."},
      changes:{label:window.GF_I18N?.t("knowledgeChanges") || "Knowledge Changes",items:changes,summary:id?"ChangeEvent canonical tersimpan persis untuk proyek terpilih.":"Exact persisted canonical ChangeEvents for the selected project."},
      coverage:{label:window.GF_I18N?.t("coverageContext") || "Coverage Context",items:coverage.coverage_context_id?[coverage]:[],summary:id?"CoverageContext tersimpan yang dihitung oleh kartu ini; konteks ini bukan keputusan ilmiah.":"The persisted CoverageContext represented by this count; it is context, not a scientific verdict."},
      radar:{label:window.GF_I18N?.t("radarItems") || "Radar Items",items:radar,summary:id?"Proyeksi Radar read-only persis yang berasal dari ChangeEvent canonical.":"Exact read-only Radar projections derived from canonical ChangeEvents."}
    };
    const setMetric = (id, value, detail, kind) => { const el = document.getElementById(id); if (el) { el.querySelector("strong").textContent = value; el.querySelector("small").textContent = detail; el.dataset.metricMembers=kind; el.classList.remove("dummy-surface"); el.classList.add("real-surface"); } };
    setMetric("metric-papers", papers.length, `Project Corpus: ${papers.length} persisted Works · Research Universe ${corpusLayers.research_universe?.state || "UNKNOWN"} · Discovery coverage ${corpusLayers.discovery_corpus?.state || "NOT_AVAILABLE"}`, "papers");
    setMetric("metric-decisions", decisions.length, window.GF_I18N?.t("humanDecisionsDetail") || "Explicit persisted Keputusan HUMANs", "decisions");
    setMetric("metric-changes", changes.length, window.GF_I18N?.t("knowledgeChangesDetail") || "Persisted canonical ChangeEvents", "changes");
    setMetric("metric-coverage", coverage.coverage_context_id ? 1 : 0, coverage.counter_search_state ? `Pencarian pembanding: ${coverage.counter_search_state}` : "Tidak ada CoverageContext tersimpan", "coverage");
    setMetric("metric-radar", radar.length, window.GF_I18N?.t("radarDetail") || "Read-only projections from ChangeEvent", "radar");
    const pill = document.getElementById("today-coverage-pill");
    if (pill) pill.textContent = coverage.coverage_context_id ? `Project Corpus ${corpusLayers.project_corpus?.count ?? papers.length} Works · semesta global ${corpusLayers.research_universe?.state || "UNKNOWN"} · pencarian pembanding ${coverage.counter_search_state || "UNKNOWN"}` : `Project Corpus ${papers.length} Works · coverage NOT_AVAILABLE`;
  } catch (error) {
    todayMetricMembers={};
    document.querySelectorAll(".metric-card").forEach(el => { el.querySelector("strong").textContent = "—"; el.querySelector("small").textContent = `Metrik canonical tidak tersedia: ${error.message}`; });
  }
}

async function loadTodayRadar() {
  const box = document.getElementById("telegram-mini");
  if (!box || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/radar`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const rows = await response.json();
    box.innerHTML = rows.length ? rows.slice(0, 4).map(r => `<div class="telegram-row"><time>${escapeHtml(r.observed_at || "")}</time><strong>${escapeHtml(r.change_type)} — ${escapeHtml(r.canonical_label)}</strong></div>`).join("") : `<p>Belum ada Item Radar canonical.</p>`;
  } catch (error) { box.innerHTML = `<p>Proyeksi Radar tidak tersedia: ${escapeHtml(error.message)}</p>`; }
}

async function loadTodayEvolution() {
  const box = document.getElementById("evolution-mini");
  if (!box || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/changes`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const rows = await response.json();
    box.innerHTML = rows.length ? rows.slice(0, 4).map(r => `<div class="evolution-row"><div><strong>${escapeHtml(r.canonical_label || r.primary_research_object_id)}</strong><small>${escapeHtml(r.change_type)} · ${escapeHtml(r.reasoning_delta || "Tidak ada delta penalaran yang direkam")}</small></div><small>${escapeHtml(r.observed_at || "")}</small></div>`).join("") : `<p>Belum ada event evolusi yang tersimpan.</p>`;
  } catch (error) { box.innerHTML = `<p>Evolusi canonical tidak tersedia: ${escapeHtml(error.message)}</p>`; }
}

async function loadTodayOpportunities() {
  const box = document.getElementById("opportunity-table");
  if (!box || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/opportunities`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const rows = await response.json();
    box.innerHTML = rows.length ? `<div class="callout">Ringkasan ini bukan ranking ilmiah. Buka setiap kandidat untuk memeriksa statement, evidence, coverage, asesmen, kritik, kualitas, dan sumber yang mendasarinya.</div><table class="table"><thead><tr><th>Kandidat</th><th>Bukti</th><th>Counter-search</th><th>Status</th><th>Verifikasi</th></tr></thead><tbody>${rows.slice(0, 5).map(r => `<tr><td><strong>${escapeHtml(r.canonical_label || r.gap_id)}</strong><br><small>${escapeHtml(r.statement || "Tidak ada pernyataan yang direkam")}</small></td><td>${escapeHtml(r.support_count)} mendukung · ${escapeHtml(r.challenge_count)} menantang</td><td>${escapeHtml(r.counter_search_state || "NOT_RECORDED")}</td><td><span class="state ${stateClass(r.current_evolution_state || "CANDIDATE")}">${escapeHtml(r.current_evolution_state || "CANDIDATE")}</span></td><td><button class="text-button" data-today-object="${escapeHtml(r.gap_id)}">Periksa dasar →</button></td></tr>`).join("")}</tbody></table>` : `<p>Belum ada peluang riset canonical yang tersimpan untuk proyek ini.</p>`;
    box.querySelectorAll('[data-today-object]').forEach(b=>b.onclick=()=>openObjectVerification(b.dataset.todayObject));
  } catch (error) {
    box.innerHTML = `<p>Peluang canonical tidak tersedia: ${escapeHtml(error.message)}</p>`;
  }
}

async function loadTodayChanges() {
  const box = document.getElementById("change-list");
  if (!box || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/changes`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const rows = await response.json();
    box.innerHTML = rows.length ? rows.slice(0, 5).map(r => `<div class="change-row"><div class="change-main"><strong>${escapeHtml(r.change_type)} — ${escapeHtml(r.canonical_label || r.primary_research_object_id)}</strong><small>${escapeHtml(r.reasoning_delta || "Tidak ada delta penalaran yang direkam")} · ${escapeHtml(r.observed_at || "waktu tidak diketahui")}</small></div><span class="state blue">CANONICAL</span></div>`).join("") : `<p>Belum ada ChangeEvent tersimpan untuk proyek ini.</p>`;
  } catch (error) {
    box.innerHTML = `<p>ChangeEvent canonical tidak tersedia: ${escapeHtml(error.message)}</p>`;
  }
}

async function renderLatestPapers() {
  const box = document.getElementById("paper-list");
  const projectId = projectSelect.value;
  if (!box || !projectId) return;
  box.innerHTML = `<div class="paper-row"><div><strong>Memuat karya nyata proyek…</strong></div></div>`;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectId)}/papers`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const papers = await response.json();
    box.innerHTML = papers.length ? papers.map(p => {
      const year = p.publication_year || "Tahun tidak diketahui";
      const venue = p.venue_name || "Venue tidak diketahui";
      const status = p.human_review_state || p.relevance_state || "UNREVIEWED";
      const links=sourceLinks(p.identifiers||{});
      return `<div class="paper-row"><div><div class="paper-title">${escapeHtml(p.title)}</div><small>${escapeHtml(year)} · ${escapeHtml(venue)} · ${escapeHtml(p.current_access_level)} · ${escapeHtml(p.source_key || "source unknown")}</small>${links?`<p>${links}</p>`:`<small>Identifier eksternal canonical belum tersedia untuk Work ini.</small>`}</div><span class="state ${stateClass(status)}">${escapeHtml(status)}</span></div>`;
    }).join("") : `<div class="paper-row"><div><strong>Belum ada karya nyata yang tersimpan untuk proyek ini.</strong><small>Paper Terbaru membaca PostgreSQL, bukan bukti ilmiah dummy.</small></div></div>`;
  } catch (error) {
    console.error(error);
    box.innerHTML = `<div class="paper-row"><div><strong>Data paper nyata tidak tersedia</strong><small>${error.message}</small></div></div>`;
  }
}

function commonHeader(title, subtitle, mode = "dummy") {
  const label = mode === "real" ? "DATA NYATA · PostgreSQL / API" : "DATA DUMMY · ilustratif";
  return `<div class="detail-header"><div><h1>${title}</h1><p>${subtitle}</p></div><div class="coverage-pill ${mode === "real" ? "real-surface" : "dummy-surface"}">${label}</div></div>`;
}

function renderJourney() {
  const id=window.GF_I18N?.current?.() === "id";
  return commonHeader(id ? "Perjalanan Riset R0–R16" : "Research Journey R0–R16", id ? "Mock-up alur kerja ilustratif saja; belum ada status tahap canonical yang tersimpan." : "Illustrative workflow mock-up only; no canonical stage status is persisted.") + `
    <div class="callout warning dummy-warning">${escapeHtml(window.GF_I18N?.t("illustrativeBoundary") || "ILLUSTRATIVE / NON-CANONICAL demonstration data")}</div><div class="callout">Tahapan penelitian bersifat iteratif; bukti baru dapat membawa HUMAN kembali ke tahap sebelumnya. Deskripsi R0–R16 adalah panduan metodologis, bukan status ilmiah canonical.</div>
    <div class="detail-grid dummy-zone"><div class="stack"><div class="card"><h3>${escapeHtml(window.GF_I18N?.t("allStages") || "All stages")}</h3>${journeyStages.map(([r,n,s,c],index) => `<div class="journey-row"><span class="r-code">${r}</span><div><strong>${escapeHtml(window.GF_I18N?.stageName(index) || n)}</strong><small>${escapeHtml(window.GF_I18N?.stageDescription(index) || "")}</small></div><span class="state ${c}">${s}</span></div>`).join("")}</div></div>
    <div class="stack"><div class="card"><h3>R6 — Penempatan Teori</h3><div class="callout warning">PERLU PERHATIAN karena penjelasan yang bersaing kini mencakup sebagian mekanisme yang sama.</div><p><strong>Yang ditemukan</strong></p><ul><li>23 paper dipetakan</li><li>5 kandidat lensa teoretis</li><li>4 tautan bukti yang menantang</li><li>2 penjelasan yang bersaing</li></ul><p><strong>Panduan pemahaman</strong></p><p>Teori perlu dievaluasi berdasarkan kecocokan penjelasan dan kontribusinya, bukan popularitas semata.</p></div><div class="card"><h3>Jejak bukti</h3><div class="trace">R6 ALASAN → CLM-142 → MENANTANG THEORY-006 → EVF-0092 → Paper → Sumber</div></div></div>
    <div class="stack"><div class="card dummy-surface"><h3>Contoh tindakan HUMAN — ILUSTRATIF</h3><div class="callout warning">Bukan tombol tindakan dan tidak menulis state apa pun. Contoh ini hanya menunjukkan jenis pemeriksaan yang mungkin relevan pada tahap R6.</div><ul><li>Bandingkan teori</li><li>Periksa mekanisme</li><li>Cari bukti pembanding</li><li>Tandai kebutuhan bukti tambahan</li></ul></div><div class="card"><h3>Dampak tahap terkini</h3><p>CE-0048 memengaruhi R4, R5, R6, R11, dan R12. Ini adalah sinyal perhatian, bukan transisi yang dipaksakan.</p></div></div></div>`;
}

function renderOpportunities() {
  return commonHeader("Peluang Riset", "Prioritas berbasis bukti untuk tinjauan ilmiah oleh HUMAN.", "real") + `
  <div class="callout warning">Prioritas hanya merupakan konteks saran. Ini tidak menetapkan kebaruan, signifikansi, kelayakan, penerimaan, atau keputusan ilmiah.</div>
  <div class="card real-surface"><h3>Peluang Riset <span class="data-badge real">DATA NYATA</span></h3><div id="real-gap-list">Memuat informasi peluang riset yang tersimpan…</div></div>
  <div class="detail-grid" style="margin-top:14px"><div class="card real-surface"><h3>Detail Objek Riset</h3><div id="real-gap-detail">Pilih peluang riset yang tersimpan.</div></div><div class="card real-surface"><h3>Bukti & Cakupan</h3><div id="real-gap-relationship">Konteks bukti belum dimuat.</div></div><div class="card real-surface"><h3>Dimensi Saran</h3><div id="real-gap-assessment">Pilih peluang riset yang tersimpan.</div></div><div class="card real-surface"><h3>Saran & Kritik</h3><div id="real-gap-critic">Pilih peluang riset yang tersimpan.</div></div><div class="card real-surface"><h3>Kualitas Riset <span class="data-badge real">DATA NYATA</span></h3><div id="real-gap-quality">Pilih objek riset yang tersimpan.</div></div><div class="card real-surface"><h3>Verifikasi Bukti <span class="data-badge real">DATA NYATA</span></h3><div id="real-gap-verification">Pilih objek riset yang tersimpan.</div></div><div class="card real-surface"><h3>Otoritas HUMAN</h3><div id="real-gap-decision">Pilih peluang riset yang tersimpan.</div></div></div>`;
}

async function loadProjectOpportunities() {
  const list = document.getElementById("real-gap-list"), detail = document.getElementById("real-gap-detail");
  const relation = document.getElementById("real-gap-relationship"), decision = document.getElementById("real-gap-decision");
  if (!list || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/research-objects`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Research Objects HTTP ${response.status}`);
    const rows = await response.json();
    if (!rows.length) { list.innerHTML = "<p>Belum ada objek riset canonical aktif untuk proyek ini.</p>"; detail.innerHTML = "<p>Belum ada yang dapat diperiksa.</p>"; relation.innerHTML = "<p>Tidak ada EvidenceRelationship canonical yang diimplikasikan.</p>"; decision.innerHTML = "<p>Tidak ada objek riset yang tersedia untuk tinjauan HUMAN.</p>"; return; }
    list.innerHTML = rows.map((r,i) => `<div class="change-row" data-object-index="${i}"><div class="change-main"><strong>${escapeHtml(r.canonical_label)}</strong><small>${escapeHtml(r.object_type)} · ${escapeHtml(r.object_state)}</small></div><span class="state ${stateClass(r.object_state)}">${escapeHtml(r.object_state)}</span></div>`).join("");
    const show = async r => {
      const isGap = r.object_type === "GAP_CANDIDATE";
      detail.innerHTML = `<p><strong>Pernyataan:</strong> ${canonicalWithId(r.statement)}</p><p><strong>Tipe objek:</strong> ${escapeHtml(r.object_type)}</p>${isGap ? `<p><strong>Tipe gap:</strong> ${escapeHtml(r.gap_type)}</p>` : ""}<p><strong>Status:</strong> ${escapeHtml(r.object_state)}</p><p><strong>Status ilmiah:</strong> ${escapeHtml(r.scope_jsonb?.scientific_status || (isGap ? "GAP_CANDIDATE_REQUIRES_HUMAN_VALIDATION" : "NOT_RECORDED"))}</p>`;
      relation.innerHTML = isGap ? `<p>Memuat relasi bukti gap yang tersimpan…</p>` : `<p><strong>Status relasi bukti:</strong> tidak ada yang diimplikasikan oleh proyeksi ini.</p><p>Tinjau record EvidenceFragment dan Claim canonical di Penjelajah Bukti. Investigation Direction bukan bukti adanya gap, kebaruan, atau mekanisme kausal.</p><div class="callout warning">EvidenceRelationship harus disimpan dan ditinjau secara eksplisit; layar ini tidak menyimpulkan SUPPORTS atau CHALLENGES.</div>`;
      document.getElementById("real-gap-assessment").innerHTML = isGap ? `<p>Memuat asesmen yang tersimpan…</p>` : `<p>Tidak diperlukan asesmen untuk menampilkan arah investigasi yang dipilih HUMAN ini.</p>`;
      document.getElementById("real-gap-critic").innerHTML = isGap ? `<p>Memuat Saran & Kritik yang tersimpan…</p>` : `<p>Saran & Kritik belum digeneralisasi untuk Investigation Direction. Lanjutkan penyaringan bukti tanpa memperlakukan ketiadaan ini sebagai penguncian global.</p>`;
      if (isGap) { const legacy = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/opportunities`, {cache:"no-store"}); const oldRows = legacy.ok ? await legacy.json() : []; const old = oldRows.find(x => x.gap_id === r.research_object_id); if (old) { Object.assign(r, old); const trace = Array.isArray(old.evidence_trace) ? old.evidence_trace : []; relation.innerHTML = `<p><strong>Tautan bukti tersimpan:</strong> ${escapeHtml(old.support_count)} mendukung · ${escapeHtml(old.challenge_count)} menantang · ${escapeHtml(old.linked_claim_count)} Claim tertaut</p><p><strong>Pencarian pembanding:</strong> ${escapeHtml(old.counter_search_state || "NOT_RECORDED")}</p><p><strong>Keterbatasan cakupan:</strong> ${canonicalWithId(old.coverage_limitations || "Tidak direkam")}</p>${trace.length ? trace.map(t => { const links = (Array.isArray(t.work_identifiers) ? t.work_identifiers : []).map(i => i.type === "DOI" ? `<a class="source-link source-link-doi" href="${escapeHtml(`https://doi.org/${i.value}`)}" target="_blank" rel="noopener noreferrer" title="Buka sumber DOI">DOI ↗</a>` : i.type === "OPENALEX" ? `<a class="source-link source-link-openalex" href="${escapeHtml(`https://openalex.org/${i.value}`)}" target="_blank" rel="noopener noreferrer" title="Buka di OpenAlex">OpenAlex ↗</a>` : "").filter(Boolean).join(" · "); const access = t.access_level || "NOT_RECORDED"; const accessNote = access === "ABSTRACT_ONLY" ? " — akses bukti terbatas" : access === "METADATA_ONLY" ? " — hanya metadata; tidak ada teks bukti" : ""; return `<div class="trace"><span class="trace-label">${escapeHtml(t.semantic_type)}</span><div class="paper-title">${escapeHtml(t.work_title)}</div><span class="access-badge ${access === "FULL_TEXT" ? "full" : "limited"}">${escapeHtml(access)}${escapeHtml(accessNote)}</span>${links ? ` · ${links}` : ""}<br><small>SourceRecord: ${escapeHtml(t.source_identifier || t.source_record_id)} · EvidenceFragment: ${escapeHtml(t.evidence_fragment_id)} · Claim: ${escapeHtml(presentId(t.claim_text))}</small></div>`; }).join("") : `<p>Tidak ada jejak bukti canonical yang tersimpan.</p>`}`; await renderGapCritic(r); await renderGapAssessment(r); } }
      await renderResearchQuality(r);
      await renderEvidenceVerification(r);
      await renderGapDecision(r);
    };
    document.querySelectorAll("[data-object-index]").forEach(el => el.onclick = () => show(rows[Number(el.dataset.objectIndex)]));
    const selected=pendingObjectId ? rows.find(r=>(r.research_object_id||r.gap_id)===pendingObjectId) : null; pendingObjectId=null; await show(selected||rows[0]);
  } catch (error) { console.error(error); list.innerHTML = `<p>API Objek Riset tidak tersedia: ${escapeHtml(error.message)}</p>`; }
}

async function renderGapCritic(gap) {
  const box = document.getElementById("real-gap-critic");
  if (!box || !projectSelect.value) return;
  box.innerHTML = "<p>Memuat Saran & Kritik yang tersimpan…</p>";
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/advice-critic`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Advice & Critic HTTP ${response.status}`);
    const rows = await response.json();
    const critic = rows.find(r => r.gap_id === gap.gap_id);
    if (!critic) { box.innerHTML = "<p>Belum ada Asesmen Saran & Kritik J10 tersimpan untuk kandidat ini.</p>"; return; }
    gap.assessment_id = critic.assessment_id || null;
    const dimensions = Array.isArray(critic.dimensions) ? critic.dimensions : [];
    const evidence = Array.isArray(critic.evidence_basis) ? critic.evidence_basis : [];
    const dimensionCards = dimensions.map(d => `<div class="trace"><strong>${escapeHtml(d.dimension_type)} — ${escapeHtml(d.value_text || "NOT_RECORDED")}</strong><p>${canonicalWithId(d.explanation || "Penjelasan tidak tersedia dari asesmen canonical saat ini.")}</p></div>`).join("");
    const evidenceCards = evidence.length ? evidence.map(e => `<div class="trace"><span class="trace-label">${escapeHtml(e.semantic_type)}</span><div class="paper-title">${escapeHtml(e.work_title || "Work tidak tersedia")}</div><p><span class="trace-label">Claim yang ditinjau:</span> ${canonicalWithId(e.claim_text || "Claim tidak tersedia")}</p><p><span class="trace-label">Alasan ditautkan:</span> ${canonicalWithId(e.relationship_rationale || "Alasan relasi tidak tersedia.")}</p><small>Akses bukti: ${escapeHtml(e.access_level || "NOT_RECORDED")} · Claim: ${escapeHtml(e.claim_review_state || "NOT_RECORDED")} · Relasi: ${escapeHtml(e.relationship_review_state || "NOT_RECORDED")}</small></div>`).join("") : "<p>Tidak ada EvidenceRelationship canonical eksplisit yang tersedia sebagai dasar Asesmen Saran & Kritik ini.</p>";
    box.innerHTML = `<p><strong>Asesmen Saran & Kritik</strong></p><p>${canonicalWithId(critic.explanation_summary || "Ringkasan penjelasan tidak tersedia dari asesmen canonical saat ini.")}</p><div class="trace"><strong>Target asesmen</strong><p>${canonicalWithId(critic.canonical_label || critic.statement || "Objek Riset tidak tersedia")} · ${escapeHtml(critic.gap_type || "TYPE_NOT_RECORDED")}</p><p>Asesmen ini berlaku pada Objek Riset dan kumpulan bukti canonical yang saat ini tertaut; ini bukan asesmen terhadap satu paper.</p><small>Cakupan bukti: ${escapeHtml(critic.linked_claim_count ?? 0)} Claim tertaut · ${escapeHtml(critic.support_count ?? 0)} SUPPORTS · ${escapeHtml(critic.challenge_count ?? 0)} CHALLENGES/CONTRADICTS</small></div><p><strong>Penalaran mesin yang dapat ditinjau</strong></p>${dimensionCards}<p><strong>Dasar bukti canonical</strong></p>${evidenceCards}<p><strong>Cakupan / keterbatasan yang belum terselesaikan</strong></p><p>Pencarian pembanding: ${escapeHtml(critic.counter_search_state || "NOT_RECORDED")}. ${canonicalWithId(critic.coverage_limitations || "Tidak ada keterbatasan cakupan tambahan yang direkam.")}</p><div class="callout warning">Verifikasi penjelasan terhadap Verifikasi Bukti dan sumber eksternal sebelum menerima Claim ilmiah yang lebih kuat. Saran & Kritik tidak menetapkan kebaruan, kebenaran, penerimaan, atau keputusan ilmiah.</div>`;
  } catch (error) {
    console.error(error);
    box.innerHTML = `<p>Saran & Kritik tidak tersedia: ${escapeHtml(error.message)}</p>`;
  }
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}

function renderEvidence() {
  return commonHeader("Penjelajah Bukti", "Record EvidenceFragment dan Claim nyata untuk Proyek yang dipilih.", "real") + `
  <div class="detail-grid evidence-layout"><div class="card evidence-list-card"><h3>Hasil Bukti</h3><div id="real-evidence-list">Memuat bukti canonical…</div></div>
  <div class="card"><h3>Detail Bukti</h3><div id="real-evidence-detail">Pilih Claim yang tersimpan.</div></div>
  <div class="card"><h3>Batas canonical</h3><div class="trace">Project → Work → EvidenceFragment → Claim</div><p>Hanya EvidenceRelationship yang tersimpan yang ditampilkan atau diimplikasikan; tidak ada relasi tambahan yang disimpulkan.</p></div></div>`;
}

async function loadProjectBukti() {
  const list = document.getElementById("real-evidence-list");
  const detail = document.getElementById("real-evidence-detail");
  if (!list || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/evidence`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Bukti HTTP ${response.status}`);
    const rows = await response.json();
    if (!rows.length) {
      list.innerHTML = "<p>Belum ada record EvidenceFragment / Claim tersimpan untuk proyek ini.</p>";
      detail.innerHTML = "<p>Belum ada yang perlu ditinjau.</p>";
      return;
    }
    list.innerHTML = rows.map((r, i) => `<div class="change-row" data-evidence-index="${i}"><div class="change-main"><div>${escapeHtml(presentId(r.claim_text))}</div><small><span class="paper-title">${escapeHtml(r.work_title)}</span> · ${escapeHtml(r.access_level)}</small></div><span class="state ${stateClass(r.review_state)}">${escapeHtml(r.review_state)}</span></div>`).join("");
    const show = r => { detail.innerHTML = `<div class="paper-title">${escapeHtml(r.work_title)}</div><p class="source-language-note">Judul paper dan pratinjau bukti dipertahankan dalam bahasa sumber asli.</p><p><span class="trace-label">Fragmen:</span> ${escapeHtml(r.fragment_type)} · ${escapeHtml(r.access_level)}</p><p><span class="trace-label">Pratinjau bukti asli:</span> ${escapeHtml(r.fragment_preview)}…</p><p><span class="trace-label">Claim — penjelasan Bahasa Indonesia:</span> ${canonicalWithId(r.claim_text)}</p><p><span class="trace-label">Ekstraksi:</span> ${escapeHtml(r.extraction_origin)} · ${escapeHtml(r.extraction_version)}</p><div class="callout">Untuk memeriksa relasi Claim terhadap objek riset dan membuka DOI/OpenAlex, gunakan <strong>Peluang Riset → Verifikasi Bukti</strong>. Layar ini tidak mengasumsikan bahwa Claim memiliki EvidenceRelationship tertentu.</div><button class="text-button" data-open-object-verification>Periksa relasi & sumber pada objek riset →</button><div class="callout warning">${escapeHtml(r.review_state)} — validasi HUMAN diperlukan sebelum penerimaan ilmiah.</div>`; detail.querySelector('[data-open-object-verification]')?.addEventListener('click',()=>openObjectVerification(null)); };
    document.querySelectorAll("[data-evidence-index]").forEach(el => el.onclick = () => show(rows[Number(el.dataset.evidenceIndex)]));
    show(rows[0]);
  } catch (error) {
    console.error(error);
    list.innerHTML = `<p>API Bukti tidak tersedia: ${escapeHtml(error.message)}</p>`;
  }
}

function humanAssessmentState(state){
  if(!state || typeof state!=="object") return "Kondisi asesmen sebelumnya tidak direkam dalam bentuk yang dapat dijelaskan.";
  const gap=state.gap_evolution_state||"NOT_RECORDED", type=state.assessment_type||"NOT_RECORDED", agent=state.model_or_agent||"NOT_RECORDED", version=state.model_version||"NOT_RECORDED";
  if(type==="GAP_CANDIDATE_EVIDENCE_CONTEXT_V1" && gap==="CANDIDATE") return `Sistem telah membuat asesmen awal terhadap kandidat gap riset ini berdasarkan konteks evidence yang tersedia saat asesmen dibuat. Statusnya masih CANDIDATE: gap ini masih kandidat yang perlu diperiksa lebih lanjut oleh HUMAN. Ini bukan bukti bahwa research gap sudah terbukti, bukan keputusan penerimaan ilmiah, dan bukan keputusan HUMAN. Asesmen dibuat oleh ${agent} versi ${version}.`;
  return `Asesmen canonical saat ini bertipe ${type} dengan state ${gap}. Asesmen ini adalah konteks mesin untuk pemeriksaan HUMAN, bukan keputusan ilmiah otomatis.`;
}
function humanAssessmentTransition(r){
  if(!r.previous_assessment_id && r.current_assessment_id) return "Ini adalah asesmen pertama yang tercatat untuk objek riset ini. Tidak ada asesmen sebelumnya yang dapat dibandingkan secara canonical.";
  if(r.previous_assessment_id && r.current_assessment_id) return "Asesmen canonical telah berubah dari asesmen sebelumnya ke asesmen saat ini. Periksa alasan dan evidence pemicu sebelum menafsirkan perubahan tersebut.";
  return "Transisi asesmen tidak tersedia dari state canonical yang direkam.";
}
function technicalAssessmentState(state){return state==null?"null":JSON.stringify(state,null,2);}

function renderEvolution() {
  return commonHeader("Evolusi Pengetahuan", "ChangeEvent tersimpan menjelaskan apa yang berubah dan alasannya tanpa menulis ulang keputusan HUMAN.", "real") + `
  <div class="detail-grid"><div class="card real-surface"><h3>Linimasa ChangeEvent <span class="data-badge real">DATA NYATA</span></h3><div id="real-change-list">Memuat ChangeEvent canonical…</div></div>
  <div class="card real-surface"><h3>Delta Penalaran</h3><div id="real-change-detail">Pilih ChangeEvent yang tersimpan.</div></div>
  <div class="card real-surface"><h3>Batas Otoritas Ilmiah</h3><div class="callout warning">ChangeEvent merekam evolusi pengetahuan historis. ChangeEvent tidak otomatis mengubah status GapCandidate atau HumanDecision.</div></div></div>`;
}

async function loadProjectChanges() {
  const list = document.getElementById("real-change-list");
  const detail = document.getElementById("real-change-detail");
  if (!list || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/changes`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Changes HTTP ${response.status}`);
    const rows = await response.json();
    if (!rows.length) { list.innerHTML = "<p>Belum ada ChangeEvent tersimpan untuk proyek ini.</p>"; detail.innerHTML = "<p>Belum ada yang direkam.</p>"; return; }
    list.innerHTML = rows.map((r,i) => `<div class="change-row" data-change-index="${i}"><div class="change-main"><strong>${escapeHtml(r.change_type)}</strong><small>${escapeHtml(r.canonical_label)} · ${escapeHtml(r.observed_at)}</small></div></div>`).join("");
    const show = r => {
      const members = Array.isArray(r.evidence_members) ? r.evidence_members : [];
      const memberTrace = members.length ? members.map(m => `<div class="trace"><strong>${escapeHtml(m.role)} · ${escapeHtml(m.semantic_type)}</strong> — ${escapeHtml(m.work_title || m.work_id)}<br><small>EvidenceRelationship: ${escapeHtml(m.evidence_relationship_id)} · Claim: ${escapeHtml(m.claim_text || m.claim_id)} · EvidenceFragment: ${escapeHtml(m.evidence_fragment_id)} · ${escapeHtml(m.access_level || "ACCESS_NOT_RECORDED")}</small></div>`).join("") : `<p>Tidak ada keanggotaan pemicu bukti canonical yang direkam untuk ChangeEvent ini. Ini adalah detail pemicu historis UNKNOWN/NOT_RECORDED, bukan bukti bahwa tidak ada bukti yang pernah tersedia.</p>`;
      detail.innerHTML = `<div class="callout"><strong>Apa yang berubah?</strong><br>${escapeHtml(humanAssessmentTransition(r))}</div><p><strong>Mengapa perubahan ini direkam?</strong><br>${escapeHtml(r.reasoning_delta || "Penjelasan tidak tersedia dari state canonical saat ini.")}</p><div class="human-current-state"><h4>Kondisi saat ini — dalam bahasa manusia</h4><p>${escapeHtml(humanAssessmentState(r.current_state_jsonb))}</p><p><strong>Yang perlu HUMAN periksa:</strong><br>Periksa evidence yang mendasari kandidat gap, batas akses sumber, konteks metodologi, dan apakah counter-search telah dilakukan sebelum membuat penilaian tentang gap atau novelty.</p></div><h4>Evidence yang tercatat sebagai pemicu perubahan (${members.length})</h4>${memberTrace}<details class="quality-technical"><summary>Detail teknis / canonical</summary><p><strong>Assessment sebelumnya:</strong> <code>${escapeHtml(r.previous_assessment_id || "INITIAL / NOT_RECORDED")}</code><br><strong>Assessment saat ini:</strong> <code>${escapeHtml(r.current_assessment_id || "NOT_APPLICABLE / NOT_RECORDED")}</code><br><strong>Pendahulu canonical:</strong> <code>${escapeHtml(r.current_supersedes_assessment_id || "NONE / NOT_RECORDED")}</code></p><p><strong>State sebelumnya</strong></p><pre>${escapeHtml(technicalAssessmentState(r.previous_state_jsonb))}</pre><p><strong>State saat ini</strong></p><pre>${escapeHtml(technicalAssessmentState(r.current_state_jsonb))}</pre></details><div class="callout warning">ChangeEvent adalah observasi historis. Tidak ada keputusan HUMAN yang diubah secara otomatis. Evidence pemicu hanya ditampilkan jika keanggotaannya memang disimpan secara eksplisit di change_event_evidence.</div>`;
    };
    document.querySelectorAll("[data-change-index]").forEach(el => el.onclick = () => show(rows[Number(el.dataset.changeIndex)]));
    show(rows[0]);
  } catch (error) { console.error(error); list.innerHTML = `<p>API ChangeEvent tidak tersedia: ${escapeHtml(error.message)}</p>`; }
}

function renderReview() {
  return commonHeader("Tinjauan HUMAN", "Claim canonical yang memerlukan tinjauan ilmiah HUMAN untuk Proyek yang dipilih.", "real") + `
  <div class="detail-grid review-layout"><div class="card real-surface review-list-card"><h3>Antrean Tinjauan <span class="data-badge real">DATA NYATA</span></h3><div id="real-review-list">Memuat antrean tinjauan canonical…</div></div>
  <div class="card real-surface"><h3>Konteks Tinjauan</h3><div id="real-review-detail">Pilih Claim yang tersimpan.</div></div>
  <div class="card"><h3>Batas Keputusan</h3><p>Antrean ini mendukung pemeriksaan Claim canonical. HumanDecision hanya ditulis melalui tindakan HUMAN eksplisit pada alur kerja yang menyediakan kontrol keputusan.</p><div class="callout warning">NEEDS_REVIEW adalah status yang memerlukan perhatian, bukan penerimaan atau penolakan ilmiah.</div></div></div>`;
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
    if (!rows.length) { list.innerHTML = "<p>Saat ini tidak ada Claim tersimpan yang perlu ditinjau.</p>"; detail.innerHTML = "<p>Belum ada yang perlu ditinjau.</p>"; return; }
    list.innerHTML = rows.map((r,i) => `<div class="change-row" data-review-index="${i}"><div class="change-main"><div>${escapeHtml(presentId(r.claim_text))}</div><small>${escapeHtml(r.work_title)} · ${escapeHtml(r.access_level)}</small></div><span class="state ${stateClass(r.review_state)}">${escapeHtml(r.review_state)}</span></div>`).join("");
    const show = r => { detail.innerHTML = `<div class="paper-title">${escapeHtml(r.work_title)}</div><p><span class="trace-label">Dasar bukti:</span> ${escapeHtml(r.fragment_type)} · ${escapeHtml(r.access_level)}</p><p><span class="trace-label">Pratinjau evidence:</span> ${escapeHtml(r.fragment_preview || "NOT_AVAILABLE")}…</p><p><span class="trace-label">Claim:</span> ${escapeHtml(r.claim_text)}</p><p><span class="trace-label">Asal ekstraksi:</span> ${escapeHtml(r.extraction_origin)}</p><div class="callout">Antrean ini menunjukkan Claim yang perlu perhatian. Untuk memeriksa teks evidence yang tersedia, EvidenceRelationship, rationale, dan tautan DOI/OpenAlex terhadap objek riset, buka <strong>Peluang Riset → Verifikasi Bukti</strong>. Jangan menerima Claim hanya dari ringkasan antrean ini.</div><button class="text-button" data-review-verification>Periksa evidence & sumber →</button><div class="callout warning">Tinjauan HUMAN diperlukan. Relasi saran mesin yang tersimpan bukan keputusan HUMAN atau kesimpulan ilmiah yang telah diterima.</div>`; detail.querySelector('[data-review-verification]')?.addEventListener('click',()=>openObjectVerification(null)); };
    document.querySelectorAll("[data-review-index]").forEach(el => el.onclick = () => show(rows[Number(el.dataset.reviewIndex)]));
    show(rows[0]);
  } catch (error) { console.error(error); list.innerHTML = `<p>API Tinjauan tidak tersedia: ${escapeHtml(error.message)}</p>`; }
}

function renderCoverage() {
  return commonHeader("Cakupan Riset", "Batas cakupan ilmiah dari CoverageContext tersimpan terbaru; kesehatan operasional berada di Admin Copilot.", "real") + `
  <div id="real-coverage-detail" class="detail-grid"><div class="card real-surface"><h3>Memuat cakupan…</h3></div></div>`;
}

async function loadProjectCoverage(targetId = "real-coverage-detail") {
  const box = document.getElementById(targetId);
  if (!box || !projectSelect.value) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/coverage`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Coverage HTTP ${response.status}`);
    const c = await response.json();
    const corpusResponse = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/corpus-layers`, { cache: "no-store" });
    const corpus = corpusResponse.ok ? await corpusResponse.json() : {};
    if (!c.coverage_context_id) { box.innerHTML = `<div class="card real-surface"><p>Tidak ada CoverageContext tersimpan for this project yet.</p></div>`; return; }
    const access = c.access_summary_jsonb || {};
    const extraction = c.extraction_summary_jsonb || {};
    const sources = c.sources || [];
    const sourceRows=sources.length?sources.map(x=>`<div class="trace"><strong>${escapeHtml(x.source_key)}</strong><p>Record diamati: ${escapeHtml(x.observed_record_count ?? "NOT_RECORDED")} · dicoba: ${escapeHtml(x.attempted_record_count ?? "NOT_RECORDED")} · status sumber: ${escapeHtml(x.health_state || "NOT_RECORDED")}</p><small>${escapeHtml(x.access_limitations || x.degradation_reason || "Tidak ada keterbatasan sumber tambahan yang direkam")}</small></div>`).join(""):`<p>Source observation canonical tidak tersedia untuk CoverageContext ini.</p>`;
    const layer = (label,key) => { const x=corpus[key]||{}; return `<li><strong>${label}</strong> — ${x.count == null ? escapeHtml(x.state||"NOT_AVAILABLE") : escapeHtml(x.count)}${x.state && x.count != null ? ` · ${escapeHtml(x.state)}` : ""}</li>`; };
    const corpusLayers = `<div class="card real-surface"><h3>Peta lapisan corpus <span class="data-badge real">DATA NYATA</span></h3><ul>${layer("Research Universe","research_universe")}${layer("Discovery Corpus (source-record observations; dapat overlap)","discovery_corpus")}${layer("Deduplicated Corpus","deduplicated_corpus")}${layer("Screening Corpus","screening_corpus")}${layer("Project Corpus","project_corpus")}${layer("Evidence Corpus","evidence_corpus")}${layer("HUMAN-reviewed Evidence","human_reviewed_evidence")}</ul><div class="callout warning">Project Corpus bukan ukuran seluruh literatur. Research Universe hanya dapat dinyatakan sesuai sumber, query, waktu, dan akses yang benar-benar dicari. UNKNOWN/NOT_AVAILABLE berarti sistem belum memiliki dasar canonical untuk menyatakan jumlahnya.</div></div>`;
    box.innerHTML = corpusLayers + `<div class="card real-surface"><h3>Cakupan korpus tersimpan <span class="data-badge real">DATA NYATA</span></h3><ul><li>FULL_TEXT — ${access.FULL_TEXT || 0}</li><li>ABSTRACT_ONLY — ${access.ABSTRACT_ONLY || 0}</li><li>METADATA_ONLY — ${access.METADATA_ONLY || 0}</li><li>Claim — ${extraction.claims || 0}</li></ul><p><strong>Pencarian pembanding:</strong> ${escapeHtml(c.counter_search_state)}</p><p>Angka di atas adalah aggregate CoverageContext. Periksa observasi sumber di bawah untuk memahami cakupan yang benar-benar direkam.</p></div><div class="card real-surface"><h3>Observasi sumber canonical</h3>${sourceRows}</div><div class="card real-surface"><h3>Batas cakupan ilmiah</h3><p><strong>Diamati:</strong> ${escapeHtml(c.observed_at)}</p><div class="callout warning">${escapeHtml(c.limitations || "Tidak ada keterbatasan yang direkam.")}</div><p>Status sumber membantu memeriksa coverage; ini bukan bukti bahwa pencarian telah lengkap secara ilmiah. Run provider/retry dan kesehatan layanan tersedia di Admin Copilot.</p></div>`;
  } catch (error) { box.innerHTML = `<div class="card"><p>API Cakupan tidak tersedia: ${escapeHtml(error.message)}</p></div>`; }
}

async function loadProjectCoverageSummary() {
  const box = document.getElementById("health-mini");
  if (!box) return;
  box.innerHTML = `<div class="health-row"><div><strong>Memuat cakupan nyata…</strong></div></div>`;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/coverage`, { cache: "no-store" });
    const c = response.ok ? await response.json() : {};
    const access = c.access_summary_jsonb || {}; box.innerHTML = c.coverage_context_id ? `<div class="health-row"><div><strong>Akses bukti</strong><small>${access.FULL_TEXT || 0} teks penuh · ${access.ABSTRACT_ONLY || 0} hanya abstrak · ${access.METADATA_ONLY || 0} hanya metadata</small></div></div><div class="callout">Pencarian pembanding: ${escapeHtml(c.counter_search_state)} · ${escapeHtml(c.limitations || "Tidak ada keterbatasan yang direkam")}</div>` : `<p>Belum ada snapshot cakupan tersimpan.</p>`;
  } catch (error) { box.innerHTML = `<p>Cakupan tidak tersedia.</p>`; }
}

function renderProfiles() {
  const ctx=(window.GF_CONTEXT_ROWS||[]).find(r=>r.project_id===projectSelect.value)||{};
  return commonHeader("Profil Riset / Konteks Proyek", "Konteks canonical aktif. Konfigurasi dikelola oleh Admin Copilot dan bersifat read-only di Research Copilot.", "real") + `
  <div class="detail-grid"><div class="card"><h3>Profil Riset · v${escapeHtml(ctx.profile_version||"—")}</h3><p><strong>Nama profil</strong><br>${escapeHtml(ctx.profile_name||"NOT_AVAILABLE")}</p><p><strong>Ringkasan</strong><br>${escapeHtml(ctx.profile_summary||"NOT_AVAILABLE")}</p></div>
  <div class="card"><h3>Proyek · v${escapeHtml(ctx.project_version||"—")}</h3><p><strong>Nama proyek</strong><br>${escapeHtml(ctx.project_name||"NOT_AVAILABLE")}</p><p><strong>Tujuan / research intent</strong><br>${escapeHtml(ctx.research_intent||"NOT_AVAILABLE")}</p><p><strong>RQ sementara</strong><br>${escapeHtml(ctx.provisional_rq_text||"NOT_AVAILABLE")}</p></div>
  <div class="card"><h3>Otoritas Konfigurasi</h3><div class="callout">Profile dan Project hanya dapat dikonfigurasi melalui Admin Copilot. Perubahan dibuat sebagai versi baru; Research Copilot tidak menyediakan kontrol mutasi.</div><p>Keputusan ilmiah tetap memerlukan tindakan HUMAN dan tidak dibuat otomatis oleh konfigurasi administratif.</p></div></div>`;
}

function renderTelegram() {
  return commonHeader("Radar Riset Telegram", "Proyeksi read-only dari ChangeEvent canonical. Telegram tidak pernah menjadi status ilmiah.", "real") + `
  <div id="radar-live" class="card"><p>Memuat proyeksi Radar canonical…</p></div>
  <div class="card"><h3>Aturan Radar</h3><ul><li>Tidak ada log crawler mentah</li><li>Tidak ada keputusan ilmiah otomatis</li><li>Tidak ada status canonical di Telegram</li><li>Kegagalan pengiriman tetap lokal</li><li>Periksa konteks lengkap di Dashboard</li></ul></div>`;
}

async function loadPilotHealth() {
  const box = document.getElementById("pilot-health-live"); if (!box) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/pilot-health`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`); const rows = await response.json();
    box.innerHTML = `<h3>Kesehatan Continuous Pilot</h3><p class="muted">Hanya kesehatan operasional — bukan penilaian ilmiah.</p>` + (rows.length ? rows.map(r => `<div class="change-row"><div class="change-main"><strong>${escapeHtml(r.status)} · ${escapeHtml(r.trigger_type)}</strong><small>Run ${escapeHtml(r.pilot_run_id)}</small><p>Dimulai: ${escapeHtml(r.started_at)}<br>Selesai: ${escapeHtml(r.finished_at || "RUNNING")}<br>Percobaan tahap: ${escapeHtml(r.stage_attempts)} · Percobaan gagal: ${escapeHtml(r.failed_stage_attempts)}</p><p>Riwayat tahap: ${escapeHtml((r.stage_history || []).join(" → ") || "tidak ada")}</p><p>Tindakan mesin: ${escapeHtml(JSON.stringify(r.machine_actions_jsonb || []))}</p></div></div>`).join("") : `<p>Belum ada run Continuous Pilot yang direkam.</p>`);
  } catch (error) { box.innerHTML = `<h3>Kesehatan Continuous Pilot</h3><p>Kesehatan operasional tidak tersedia; status ilmiah canonical tidak terpengaruh.</p>`; }
}

async function loadProjectRadar() {
  const box = document.getElementById("radar-live");
  if (!box) return;
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/radar`, { cache: "no-store" });
    const rows = response.ok ? await response.json() : [];
    box.innerHTML = rows.length ? rows.map(r => `<div class="change-row"><div class="change-main"><strong>${escapeHtml(r.change_type)}</strong><small>${escapeHtml(r.profile_name)} / ${escapeHtml(r.project_name)}</small><p><strong>APA YANG BERUBAH</strong><br>${escapeHtml(r.canonical_label)}</p><p><strong>MENGAPA INI PENTING</strong><br>${escapeHtml(r.reasoning_delta)}</p><p><strong>CAKUPAN</strong><br>Pencarian pembanding: ${escapeHtml(r.counter_search_state || "UNKNOWN")} · ${escapeHtml(r.coverage_limitations || "Tidak ada keterbatasan yang direkam")}</p><p><strong>KONTEKS HUMAN</strong><br>Keputusan terbaru: ${escapeHtml(r.latest_human_decision || "NONE")}. Item Radar ini tidak mengubahnya.</p><button class="text-button" data-radar-object="${escapeHtml(r.primary_research_object_id||"")}">Periksa bukti & sumber</button></div></div>`).join("") : `<p>Saat ini tidak ada ChangeEvent canonical yang tersedia untuk proyeksi Radar.</p>`;
    box.querySelectorAll('[data-radar-object]').forEach(b=>b.onclick=()=>openObjectVerification(b.dataset.radarObject||null));
  } catch (error) {
    box.innerHTML = `<p>Proyeksi Radar tidak tersedia. Pemrosesan riset canonical tidak terpengaruh.</p>`;
  }
}

const renderers = { journey:renderJourney, opportunities:renderOpportunities, evidence:renderEvidence, evolution:renderEvolution, review:renderReview, coverage:renderCoverage, profiles:renderProfiles, telegram:renderTelegram };

function showView(name) {
  document.querySelectorAll(".view").forEach(v => v.classList.remove("active-view"));
  document.querySelectorAll(".nav-item").forEach(v => v.classList.toggle("active", v.dataset.view === name));
  const view = document.getElementById(`view-${name}`);
  if (name !== "today" && renderers[name]) view.innerHTML = renderers[name]();
  view.classList.add("active-view");
  if (name === "evidence") loadProjectBukti();
  if (name === "review") loadHumanReview();
  if (name === "opportunities") loadProjectOpportunities();
  if (name === "coverage") loadProjectCoverage();
  if (name === "evolution") loadProjectChanges();
  if (name === "telegram") loadProjectRadar();
}

function bindOpenButtons() {
  document.querySelectorAll("[data-open]").forEach(b => b.onclick = () => showView(b.dataset.open));
  document.querySelectorAll("[data-metric-open]").forEach(card => {
    const open = () => card.dataset.metricMembers ? showMetricMembers(card.dataset.metricMembers) : showView(card.dataset.metricOpen);
    card.onclick = open;
    card.onkeydown = event => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); open(); } };
  });
  const close=document.getElementById("metric-members-close");
  if (close) close.onclick=()=>{ document.getElementById("metric-members").hidden=true; };
}

document.getElementById("main-nav").addEventListener("click", e => {
  const button = e.target.closest("[data-view]");
  if (button) showView(button.dataset.view);
});
document.querySelectorAll(".nav-list.small [data-view]").forEach(b => b.addEventListener("click", () => showView(b.dataset.view)));

projectSelect.addEventListener("change", () => { loadHumanReviewBadge(); const aktif = document.querySelector(".active-view")?.id.replace("view-",""); if (!active || aktif === "today") renderDashboard(); else showView(active); });
document.getElementById("global-search").addEventListener("keydown", e => { if (e.key === "Enter") showView("evidence"); });

fetch(`${API_BASE}/api/context`, { cache: "no-store" }).then(r => { if (!r.ok) throw new Error(`Context HTTP ${r.status}`); return r.json(); }).then(rows => {
  window.GF_CONTEXT_ROWS=rows;
  const profiles = [...new Map(rows.map(r => [r.profile_id, r])).values()];
  profileSelect.innerHTML = profiles.map(r => `<option value="${r.profile_id}">${r.profile_name}</option>`).join("");
  const bindProjects = () => {
    const projects = rows.filter(r => r.profile_id === profileSelect.value);
    projectSelect.innerHTML = projects.map(r => `<option value="${r.project_id}">${r.project_name}</option>`).join("");
    renderLatestPapers();
    applyProfileTheme(rows);
  };
  profileSelect.onchange = () => { bindProjects(); loadHumanReviewBadge(); const aktif = document.querySelector(".active-view")?.id.replace("view-",""); if (!active || aktif === "today") renderDashboard(); else showView(active); };
  bindProjects();
  renderDashboard();
loadHumanReviewBadge();
  const version = document.getElementById("prototype-version");
  if (version) version.textContent = `Prototype v${PROTOTYPE_VERSION} · live`;
}).catch(error => {
  console.error(error);
  projectSelect.innerHTML = `<option>Konteks tidak tersedia</option>`;
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
    box.innerHTML = latest ? `<p><strong>Keputusan HUMAN terbaru:</strong> ${escapeHtml(latest.decision_type)}</p><p>${escapeHtml(latest.rationale)}</p><small>${escapeHtml(latest.actor)} · ${escapeHtml(latest.decided_at)}</small><h4>Riwayat perubahan</h4>${history.map((d, i) => `<div class="trace"><strong>${i === 0 ? "SAAT INI · " : "SEBELUMNYA · "}${escapeHtml(d.decision_type)}</strong><br>${escapeHtml(d.rationale)}<br><small>${escapeHtml(d.actor)} · ${escapeHtml(d.decided_at)} · Asesmen: ${escapeHtml(d.assessment_id || "tidak ada")} · Menggantikan: ${escapeHtml(d.supersedes_decision_id || "tidak ada")}</small></div>`).join("")}` : `<p>Belum ada HumanDecision tersimpan untuk kandidat ini.</p>`;
    box.innerHTML += `<div class="human-review-form" style="margin-top:12px"><label>Peninjau HUMAN<br><input id="human-review-actor" type="text" placeholder="Nama peneliti"></label><br><label>Alasan / catatan peneliti<br><textarea id="human-review-rationale" rows="4" placeholder="Mengapa Anda mengambil tindakan ini berdasarkan bukti dan kritik di atas?"></textarea></label></div><div class="decision-bar" style="margin-top:10px"><button data-decision="REVIEW">Tinjau</button><button data-decision="MODIFY">Ubah</button><button data-decision="ACCEPT_DIRECTION">Terima arah</button><button data-decision="REJECT_CANDIDATE">Tolak kandidat</button><button data-decision="NEED_MORE_EVIDENCE">Perlu bukti tambahan</button></div><div class="callout warning" style="margin-top:10px">Terima arah berarti melanjutkan arah riset saat ini berdasarkan bukti yang tersedia; ini tidak menetapkan bahwa gap benar atau baru. Hanya tindakan HUMAN eksplisit yang menulis keputusan. Keputusan baru menggantikan keputusan sebelumnya tanpa menulis ulang riwayat.</div>`;
    box.querySelectorAll("[data-decision]").forEach(btn => btn.onclick = () => submitHumanDecision(row, btn.dataset.decision));
  } catch (error) { box.innerHTML = `<p>API Keputusan tidak tersedia: ${escapeHtml(error.message)}</p>`; }
}

async function submitHumanDecision(row, decisionType) {
  const actor = document.getElementById("human-review-actor")?.value?.trim();
  const rationale = document.getElementById("human-review-rationale")?.value?.trim();
  if (!actor || !rationale) {
    window.alert("Peninjau HUMAN dan alasan wajib diisi sebelum merekam keputusan.");
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

const ASSESSMENT_DIMENSION_GUIDE={
  EVIDENCE_SUPPORT_CONTEXT:{title:"Konteks Evidence Pendukung",check:"Periksa EvidenceRelationship dan sumber yang ditampilkan pada Verifikasi Bukti."},
  COUNTER_EVIDENCE_CONTEXT:{title:"Konteks Evidence Penantang",check:"Periksa evidence yang menantang/bertentangan dan status counter-search sebelum menilai gap."},
  COVERAGE_CONTEXT:{title:"Konteks Cakupan",check:"Periksa CoverageContext, sumber yang diamati, dan keterbatasannya."},
  GAP_EVOLUTION_STATE:{title:"Status Kandidat Gap",check:"Baca state sebagai konteks evolusi kandidat, bukan bukti bahwa gap benar atau baru."}
};
function humanAssessmentDimension(d){const g=ASSESSMENT_DIMENSION_GUIDE[d.dimension_type]||{title:String(d.dimension_type||"Dimensi asesmen").replaceAll("_"," "),check:"Periksa penjelasan dan evidence canonical yang mendasari dimensi ini."};return {...g,value:d.value_text??d.value_numeric??"NOT_RECORDED"};}

async function renderGapAssessment(gap) {
  const box = document.getElementById("real-gap-assessment");
  if (!box) return;
  box.innerHTML = "<p>Memuat asesmen mesin…</p>";
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/assessments`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Assessments HTTP ${response.status}`);
    const rows = (await response.json()).filter(a => a.target_research_object_id === gap.gap_id);
    if (!rows.length) { box.innerHTML = "<p>Belum ada Asesmen tersimpan untuk GapCandidate ini.</p>"; return; }
    const a = rows[0];
    const dims = (a.dimensions || []).map(d => {const h=humanAssessmentDimension(d);return `<div class="trace"><strong>${escapeHtml(h.title)}</strong><p><strong>Kondisi:</strong> ${escapeHtml(h.value)}</p><p>${canonicalWithId(d.explanation || "Penjelasan canonical belum tersedia untuk dimensi ini.")}</p><small><strong>Yang perlu HUMAN periksa:</strong> ${escapeHtml(h.check)}</small><details class="quality-technical"><summary>Detail teknis</summary><code>${escapeHtml(d.dimension_type)}</code></details></div>`}).join("");
    box.innerHTML = `<div class="callout"><strong>Apa arti asesmen ini?</strong><br>Ini adalah penilaian mesin terhadap konteks evidence untuk membantu HUMAN memeriksa kandidat gap. Asesmen tidak membuktikan gap, novelty, signifikansi, atau penerimaan ilmiah.</div><p>${canonicalWithId(a.explanation_summary || "Ringkasan penjelasan tidak tersedia dari asesmen canonical saat ini.")}</p>${dims}<details class="quality-technical"><summary>Detail teknis asesmen</summary><p><code>${escapeHtml(a.assessment_type)}</code></p></details><div class="callout warning">Dimensi mesin adalah saran kontekstual. HUMAN perlu memverifikasi penjelasan terhadap Verifikasi Bukti, Coverage, dan sumber sebelum membuat penilaian ilmiah.</div>`;
  } catch (error) {
    console.error(error);
    box.innerHTML = `<p>API Asesmen tidak tersedia: ${escapeHtml(error.message)}</p>`;
  }
}

const QUALITY_HUMAN_GUIDE = {
  ACCESS_COMPLETENESS:{title:"Kelengkapan Akses Bukti",meaning:"Menunjukkan seberapa lengkap isi sumber yang tersedia untuk evidence yang terhubung.",why:"Abstrak dapat membantu screening, tetapi detail metode, batasan, dan hasil sering memerlukan teks penuh.",check:"Periksa level akses setiap sumber. Jika hanya ABSTRACT_ONLY, buka sumber/full text sebelum membuat penilaian yang bergantung pada detail."},
  PROVENANCE_COMPLETENESS:{title:"Keterlacakan Bukti",meaning:"Menunjukkan apakah hubungan evidence dapat ditelusuri dari Claim ke potongan evidence lalu ke paper/sumber asal.",why:"Keterlacakan memungkinkan HUMAN memeriksa apakah pernyataan benar-benar bersumber dari evidence yang ditampilkan.",check:"Ikuti rantai Claim → EvidenceFragment → Work dan baca konteks sumbernya. Keterlacakan tidak berarti Claim otomatis benar."},
  EXTRACTION_REVIEW_STATE:{title:"Status Tinjauan Claim & Hubungan Evidence",meaning:"Menunjukkan apakah hasil ekstraksi Claim dan hubungan evidence masih usulan mesin atau sudah memiliki status review canonical.",why:"Usulan mesin harus diperiksa HUMAN sebelum dipakai sebagai dasar penilaian ilmiah.",check:"Prioritaskan NEEDS_REVIEW dan MACHINE_SUGGESTED; bandingkan teks Claim dengan evidence asal sebelum menyetujui atau menentangnya."},
  METHODOLOGICAL_CONTEXT_AVAILABILITY:{title:"Konteks Metodologi",meaning:"Menunjukkan apakah konteks metode/metodologi/desain eksplisit tersedia dalam scope canonical yang sedang diperiksa.",why:"Tanpa konteks metodologi, sistem tidak memiliki dasar canonical untuk membantu HUMAN menilai bagaimana temuan dihasilkan.",check:"Buka sumber dan periksa bagian metode/desain. NOT_AVAILABLE berarti konteks belum tersedia di state canonical, bukan metodologinya buruk."},
  CORROBORATION_CONTEXT:{title:"Dukungan dari Evidence Lain",meaning:"Merangkum hubungan canonical yang mendukung, memperluas, atau mereplikasi Claim/objek riset.",why:"Beberapa hubungan evidence dapat memberi konteks lebih luas daripada satu sumber saja, tetapi jumlah bukan ukuran kebenaran.",check:"Periksa masing-masing hubungan SUPPORTS, EXTENDS, atau REPLICATES dan nilai relevansinya secara langsung."},
  CONTRADICTION_CONTEXT:{title:"Kontradiksi & Counter-search",meaning:"Menunjukkan evidence canonical yang menantang/bertentangan serta apakah pencarian khusus evidence lawan sudah dilakukan.",why:"Tidak menemukan kontradiksi belum berarti tidak ada kontradiksi, terutama bila counter-search belum dijalankan.",check:"Jika counter-search NOT_RUN, pertimbangkan pencarian evidence yang dapat menantang Claim sebelum menilai gap, novelty, atau kekuatan kesimpulan."},
  RECENCY_CONTEXT:{title:"Konteks Waktu Sumber",meaning:"Menampilkan kapan sumber dipublikasikan dan kapan evidence diperoleh sistem.",why:"Tanggal membantu HUMAN memahami konteks temporal literatur; sumber lama tidak otomatis berkualitas rendah.",check:"Periksa apakah rentang waktu sumber sesuai kebutuhan pertanyaan riset dan apakah literatur yang lebih baru perlu dicari."},
  SOURCE_COVERAGE_LIMITATIONS:{title:"Cakupan Sumber & Keterbatasan",meaning:"Menjelaskan sumber discovery/coverage yang tercatat dan keterbatasan canonical yang diketahui.",why:"Coverage yang terbatas dapat membuat peta literatur belum lengkap tanpa berarti hasil yang ada salah.",check:"Baca keterbatasan dan status sumber sebelum menyimpulkan bahwa pencarian sudah mencakup literatur yang relevan."}
};
function qualityCurrentText(o){
  const v=o?.value, d=o?.dimension;
  if(v==null) return o?.state==="NOT_AVAILABLE" ? "Belum ada konteks canonical yang tersedia untuk dimensi ini." : `Status canonical: ${o?.state||"UNKNOWN"}.`;
  if(d==="PROVENANCE_COMPLETENESS") return `${v.traceable_relationships??0} dari ${v.linked_relationships??0} hubungan evidence dapat ditelusuri lengkap.`;
  if(d==="ACCESS_COMPLETENESS") return `Level akses evidence saat ini: ${(Array.isArray(v)?v:[v]).join(", ")}.`;
  if(d==="EXTRACTION_REVIEW_STATE") return `Status Claim: ${(v.claim_states||[]).join(", ")||"NOT_AVAILABLE"}; status hubungan evidence: ${(v.relationship_states||[]).join(", ")||"NOT_AVAILABLE"}.`;
  if(d==="CORROBORATION_CONTEXT") return `Hubungan tercatat — mendukung: ${v.SUPPORTS??0}, memperluas: ${v.EXTENDS??0}, mereplikasi: ${v.REPLICATES??0}.`;
  if(d==="CONTRADICTION_CONTEXT") return `Menantang: ${v.CHALLENGES??0}; bertentangan: ${v.CONTRADICTS??0}; counter-search: ${v.counter_search_state||"NOT_AVAILABLE"}.`;
  if(d==="RECENCY_CONTEXT" && Array.isArray(v)) return `${v.length} sumber/evidence memiliki konteks tanggal yang dapat diperiksa.`;
  if(d==="SOURCE_COVERAGE_LIMITATIONS") return `Konteks coverage tersedia${v.limitations?`; keterbatasan tercatat: ${v.limitations}`:"."}`;
  return `Status canonical: ${o?.state||"UNKNOWN"}.`;
}
function qualityTechnicalValue(value){return value==null?"—":(typeof value==="string"?value:JSON.stringify(value,null,2));}
async function renderResearchQuality(row) {
  const box = document.getElementById("real-gap-quality");
  if (!box || !projectSelect.value || !row?.research_object_id) return;
  box.innerHTML = "<p>Memuat observasi kualitas canonical…</p>";
  try {
    const response = await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/quality?object_id=${encodeURIComponent(row.research_object_id)}`, {cache:"no-store"});
    if (!response.ok) throw new Error(`Quality HTTP ${response.status}`);
    const q = await response.json(), observations=Array.isArray(q.observations)?q.observations:[], limitations=Array.isArray(q.limitations)?q.limitations:[], suggestions=Array.isArray(q.review_suggestions)?q.review_suggestions:[];
    box.innerHTML = `<div class="callout warning"><strong>Apa yang diperiksa di sini?</strong><br>Bagian ini membantu HUMAN menilai seberapa siap evidence dan konteks sebuah Claim untuk diperiksa. Ini <strong>bukan skor kualitas riset</strong> dan tidak menentukan apakah Claim benar. Fokus pada akses sumber, keterlacakan, status review, metodologi, dukungan/kontradiksi, waktu sumber, dan cakupan pencarian.</div>
      ${observations.map(o=>{const g=QUALITY_HUMAN_GUIDE[o.dimension]||{title:o.dimension,meaning:"Observasi canonical untuk membantu pemeriksaan HUMAN.",why:"Konteks ini tidak menghasilkan keputusan ilmiah.",check:"Periksa evidence dan state canonical terkait."};return `<article class="quality-human-card"><div class="quality-human-head"><h4>${escapeHtml(g.title)}</h4><span class="state ${stateClass(o.state)}">${escapeHtml(o.state)}</span></div><p><strong>Apa artinya?</strong><br>${escapeHtml(g.meaning)}</p><p><strong>Kondisi saat ini</strong><br>${escapeHtml(qualityCurrentText(o))}</p><p><strong>Mengapa penting?</strong><br>${escapeHtml(g.why)}</p><p><strong>Yang perlu HUMAN periksa</strong><br>${escapeHtml(g.check)}</p><details class="quality-technical"><summary>Detail teknis / canonical</summary><p><code>${escapeHtml(o.dimension)}</code></p><pre>${escapeHtml(qualityTechnicalValue(o.value))}</pre><small>Basis canonical: ${escapeHtml(o.basis||"Tidak direkam")}</small></details></article>`}).join("")}
      <div class="quality-summary"><h4>Keterbatasan yang perlu diingat</h4>${limitations.length?`<ul>${limitations.map(x=>`<li>${escapeHtml(x)}</li>`).join("")}</ul>`:"<p>Tidak ada keterbatasan tambahan yang direkam oleh proyeksi ini.</p>"}<h4>Tindakan tinjauan HUMAN yang disarankan</h4>${suggestions.length?suggestions.map(x=>`<div class="trace"><strong>${escapeHtml(x.action)}</strong><br><small>Dipicu oleh state canonical: ${escapeHtml((x.because||[]).join("; "))}</small></div>`).join(""):"<p>Tidak ada saran tinjauan yang dipicu oleh kualitas.</p>"}</div>
      <div class="callout warning">scientific_decision=${escapeHtml(String(q.scientific_decision))}. Observasi dan saran di atas membantu pemeriksaan; keputusan ilmiah tetap milik HUMAN.</div>`;
  } catch (error) { box.innerHTML = `<p>Kualitas Riset tidak tersedia: ${escapeHtml(error.message)}</p>`; }
}

async function renderEvidenceVerification(row) {
  const box=document.getElementById("real-gap-verification");
  if(!box || !projectSelect.value || !row?.research_object_id) return;
  box.innerHTML="<p>Memuat bukti canonical yang dapat diperiksa…</p>";
  try {
    const response=await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectSelect.value)}/evidence-verification?object_id=${encodeURIComponent(row.research_object_id)}`,{cache:"no-store"});
    if(!response.ok) throw new Error(`Bukti verification HTTP ${response.status}`);
    const rows=await response.json();
    box.innerHTML=`<div class="callout warning">Baca apa yang benar-benar tersimpan sebelum menilai Claim atau relasi. PROJECT_LITERATURE_ONLY adalah konteks kandidat, bukan bukti untuk objek riset ini. ABSTRACT_ONLY bukan teks penuh.</div>`+
      rows.map((x,i)=>{
        const links=[x.doi_url ? `<a class="source-link source-link-doi" href="${escapeHtml(x.doi_url)}" target="_blank" rel="noopener noreferrer">DOI ↗</a>`:"",x.openalex_url ? `<a class="source-link source-link-openalex" href="${escapeHtml(x.openalex_url)}" target="_blank" rel="noopener noreferrer">OpenAlex ↗</a>`:""].filter(Boolean).join(" · ");
        const text=x.evidence_text ? `<details ${i===0 ? "open":""}><summary>Baca ${escapeHtml(x.fragment_type || "fragmen bukti")} (${escapeHtml(x.access_level || "UNKNOWN")})</summary><p class="evidence-readable">${escapeHtml(x.evidence_text)}</p></details>` : `<p><em>Tidak ada teks BuktiFragment canonical yang tersimpan untuk karya ini.</em></p>`;
        const claim=x.claim_id ? `<p><strong>Claim hasil ekstraksi:</strong> ${canonicalWithId(x.claim_text)}<br><small>Tinjauan Claim: ${escapeHtml(x.claim_review_state)} · ekstraksi: ${escapeHtml(x.extraction_origin)}</small></p>` : "<p><strong>Claim hasil ekstraksi:</strong> tidak ada yang tersimpan.</p>";
        const rel=x.relationship_id ? `<p><strong>Relasi objek:</strong> ${escapeHtml(x.semantic_type)} · ${escapeHtml(x.relationship_review_state)}</p>` : "<p><strong>Relasi objek:</strong> tidak ada yang dinyatakan.</p>";
        return `<div class="trace"><strong>${escapeHtml(x.title)}</strong><br><small>${escapeHtml(x.publication_year || "Tahun tidak tersedia")} · ${escapeHtml(x.object_evidence_status)} · ${escapeHtml(x.access_level || x.current_access_level || "METADATA_ONLY")}</small>${links ? `<p>${links}</p>`:""}${text}${claim}${rel}</div>`;
      }).join("")+
      `<div class="callout warning">Tautan DOI/OpenAlex eksternal digunakan untuk pemeriksaan sumber oleh HUMAN. Layar ini tidak mengklaim akses ke teks penuh penerbit kecuali access_level canonical adalah FULL_TEXT.</div>`;
  } catch(error) {
    box.innerHTML=`<p>Verifikasi Bukti tidak tersedia: ${escapeHtml(error.message)}</p>`;
  }
}

// Presentation language affects UI chrome only; canonical scientific records remain untouched.
document.querySelectorAll("[data-language-select]").forEach(el => el.addEventListener("change", event => window.GF_I18N?.setLanguage(event.target.value)));
function applyMetricActionLabels() { document.querySelectorAll(".metric-action").forEach(el => el.dataset.memberActionLabel = window.GF_I18N?.t("inspectMembers") || "Inspect members →"); }
window.GF_I18N?.apply();
applyMetricActionLabels();
window.addEventListener("gfprojclaw-language-change", () => {
  applyMetricActionLabels();
  renderToday();
  const aktifJourney=document.getElementById("view-journey"); if (activeJourney?.classList.contains("active-view")) aktifJourney.innerHTML=renderJourney();
  const dark = document.documentElement.dataset.theme === "dark";
  if (themeToggle) themeToggle.textContent = `${dark ? "☀️" : "🌙"} ${window.GF_I18N.t(dark ? "light" : "dark")}`;
});

function renderExplorerHandoff(){
 const box=document.getElementById("explorer-handoff");if(!box)return;
 const params=new URLSearchParams(window.location.search);if(params.get("from")!=="explorer")return;
 let h=null;try{h=JSON.parse(sessionStorage.getItem("gfprojclaw-explorer-handoff")||"null");}catch(_){h=null;}
 box.hidden=false;if(!h){document.getElementById("handoff-summary").textContent="Konteks Explorer tidak ditemukan pada sesi browser ini. Kembali ke Research Explorer dan pilih area lagi.";return;}
 document.getElementById("handoff-title").textContent=`Area terpilih: ${h.area}`;
 document.getElementById("handoff-summary").innerHTML=`<strong>${escapeHtml(h.member_count)} anggota teramati</strong> · ${escapeHtml(h.time_boundary)} · ${escapeHtml(h.verification?.provider||"provider tidak tercatat")}<br><small>Query: ${escapeHtml(h.query)}</small>`;
 document.getElementById("handoff-why").textContent=h.why||"Belum tersedia.";
 document.getElementById("handoff-observed").textContent=`${h.supporting_observation?.observed_title_count||h.member_count} anggota tepat berdasarkan istilah pada judul. Provenance tetap dapat ditelusuri ke Explorer.`;
 document.getElementById("handoff-human").textContent=(h.selected_gap_opportunity?`Gap Opportunity dipilih HUMAN: ${h.selected_gap_opportunity.term}. `:"")+(h.human_learning_note||"Belum ada catatan HUMAN dari Explorer.");
 const gap=document.getElementById("handoff-gap"),verify=document.getElementById("handoff-verification"),start=document.getElementById("handoff-start"),o=h.selected_gap_opportunity;
 if(o){gap.hidden=false;gap.innerHTML=`<strong>Gap Opportunity · ${escapeHtml(o.term)}</strong><br>${escapeHtml(o.observation)}<br><strong>WHY:</strong> ${escapeHtml(o.why)}<br><small>${escapeHtml(o.limitation)}</small>`;verify.hidden=false;verify.innerHTML=`<div class="advice-card"><strong>Hipotesis kerja untuk diuji</strong><p>Apakah pola “${escapeHtml(o.term)}” pada jalur ${escapeHtml((o.path||h.path||[]).join(" → "))} menunjukkan ruang penelitian yang belum cukup dijelaskan?</p></div><div class="advice-card"><strong>Verifikasi berikutnya</strong><p>${escapeHtml(o.verification)}</p></div><div class="advice-card"><strong>Cari supporting evidence</strong><p>Periksa paper yang membentuk sinyal ini; jangan hanya memakai frekuensi istilah judul.</p></div><div class="advice-card"><strong>Cari counter-evidence</strong><p>Cari paper di subset yang dapat membantah bahwa sinyal ini merupakan gap substantif.</p></div>`;}
 if(o?.supporting_papers?.length){const ev=document.getElementById("handoff-evidence");ev.hidden=false;ev.innerHTML=`<strong>Evidence dibawa dari Explorer · ${escapeHtml(o.evidence_level||"ABSTRACT_ONLY")}</strong>${o.supporting_papers.map(p=>`<div class="advanced-paper"><strong>${escapeHtml(p.title||"JUDUL TIDAK TERSEDIA")}</strong><br><small>${p.source_url?`<a href="${escapeHtml(p.source_url)}" target="_blank" rel="noopener">OpenAlex ↗</a>`:""}${p.doi?` · <a href="${escapeHtml(p.doi)}" target="_blank" rel="noopener">DOI ↗</a>`:""}</small><details><summary>Baca abstract evidence</summary><p>${escapeHtml(p.abstract||"Abstract tidak tersedia")}</p></details></div>`).join("")}<p><strong>Counter-evidence protocol:</strong> ${escapeHtml(o.counter_evidence_instruction||"Cari bukti yang menantang opportunity ini.")}</p><small>Evidence ini belum canonical dan tidak menetapkan research gap.</small>`;}
 else if(o){const ev=document.getElementById("handoff-evidence");ev.hidden=false;ev.innerHTML="<strong>Evidence detail belum dibawa.</strong><br>Kembali ke Explorer untuk memilih Advanced Opportunity dengan supporting abstracts.";}
 else {start.disabled=true;start.textContent="Pilih Gap Opportunity di Explorer terlebih dahulu";}
 start.onclick=()=>{if(!o)return;start.textContent="VERIFIKASI DIMULAI · HUMAN REVIEW";start.disabled=true;document.getElementById("handoff-human").textContent=`Opportunity “${o.term}” dipilih untuk diverifikasi. Periksa supporting evidence, counter-evidence, abstrak/metode/konteks sebelum keputusan research gap. Scientific decision tetap milik HUMAN.`;const matrix=document.getElementById("handoff-evidence-matrix"),verdict=document.getElementById("handoff-human-verdict"),papers=o.supporting_papers||[];matrix.hidden=false;matrix.innerHTML=`<strong>Evidence Review Matrix · HUMAN</strong><p>Tandai hasil pembacaan abstract. Status ini adalah catatan review HUMAN, bukan klasifikasi otomatis.</p>${papers.map((p,i)=>`<div class="evidence-review-row" data-i="${i}"><strong>${escapeHtml(p.title||"JUDUL TIDAK TERSEDIA")}</strong><div class="evidence-review-actions"><button type="button" data-status="SUPPORTS">Mendukung</button><button type="button" data-status="CHALLENGES">Menantang</button><button type="button" data-status="UNCLEAR">Belum jelas</button></div><textarea rows="2" placeholder="Catatan HUMAN: mekanisme, konteks, metode, hasil, limitation…"></textarea></div>`).join("")}<button id="summarize-human-review" class="primary-action" type="button">Ringkas review HUMAN</button>`;document.getElementById("summarize-human-review").onclick=()=>{const reviews=[...matrix.querySelectorAll(".evidence-review-row")].map((row,i)=>({openalex_id:papers[i]?.openalex_id,title:papers[i]?.title,status:row.dataset.status||"NOT_REVIEWED",note:row.querySelector("textarea").value.trim()}));const n=x=>reviews.filter(r=>r.status===x).length;verdict.hidden=false;verdict.innerHTML=`<strong>HUMAN Evidence Balance</strong><br>Mendukung: ${n("SUPPORTS")} · Menantang: ${n("CHALLENGES")} · Belum jelas: ${n("UNCLEAR")} · Belum direview: ${n("NOT_REVIEWED")}<p><strong>Keputusan tetap terbuka.</strong> Evidence balance bukan truth probability dan belum membuktikan research gap.</p><button id="save-human-review" class="secondary-action" type="button">Simpan review sementara di sesi</button> <button id="derive-next-question" class="primary-action" type="button">Susun pertanyaan verifikasi berikutnya</button>`;document.getElementById("save-human-review").onclick=()=>{sessionStorage.setItem("gfprojclaw-human-evidence-review",JSON.stringify({opportunity:o.id||o.term,reviews,scientific_decision:false,canonical_write:false}));document.getElementById("save-human-review").textContent="TERSIMPAN DI SESI · NON-CANONICAL";};document.getElementById("derive-next-question").onclick=()=>{const next=document.getElementById("handoff-next-question"),support=n("SUPPORTS"),challenge=n("CHALLENGES"),unclear=n("UNCLEAR")+n("NOT_REVIEWED");next.hidden=false;let focus=challenge?"Jelaskan mengapa evidence yang menantang berbeda: konteks, metode, unit analisis, atau mekanisme?":unclear?"Evidence masih belum cukup: paper/metode/konteks apa yang harus diperiksa agar opportunity dapat diuji lebih kuat?":"Supporting evidence mendominasi review awal: cari secara sengaja studi dengan hasil, mekanisme, atau konteks yang berlawanan sebelum menyimpulkan gap.";next.innerHTML=`<strong>Next Verification Question · HUMAN decides</strong><p>${escapeHtml(focus)}</p><p><strong>Evidence balance saat ini:</strong> ${support} mendukung · ${challenge} menantang · ${unclear} belum pasti.</p><textarea id="human-next-question" rows="3" placeholder="HUMAN dapat mengubah atau mengganti pertanyaan ini sepenuhnya."></textarea><button id="save-next-question" class="secondary-action" type="button">Simpan sebagai arah investigasi sementara</button><small> Sistem hanya menyusun prompt dari review HUMAN; ini bukan research question final, gap, atau keputusan ilmiah.</small>`;document.getElementById("human-next-question").value=focus;document.getElementById("save-next-question").onclick=()=>{const q=document.getElementById("human-next-question").value.trim();sessionStorage.setItem("gfprojclaw-human-next-investigation",JSON.stringify({opportunity:o.id||o.term,question:q,based_on_human_review:true,scientific_decision:false,canonical_write:false}));document.getElementById("save-next-question").textContent="TERSIMPAN · HUMAN INVESTIGATION DRAFT";};};};matrix.querySelectorAll(".evidence-review-actions button").forEach(b=>b.onclick=()=>{const row=b.closest(".evidence-review-row");row.dataset.status=b.dataset.status;row.querySelectorAll("button").forEach(x=>x.classList.toggle("selected",x===b));});};
}
renderExplorerHandoff();
