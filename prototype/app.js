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
  document.getElementById("health-mini").innerHTML = health.map(([source,status,cls,detail]) => `<div class="health-row"><div><strong>${source}</strong><small>${detail}</small></div><span class="state ${cls}">${status}</span></div>`).join("");
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
    const response = await fetch(`/api/projects/${encodeURIComponent(projectId)}/papers`);
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

function commonHeader(title, subtitle) {
  return `<div class="detail-header"><div><h1>${title}</h1><p>${subtitle}</p></div><div class="coverage-pill">Dummy data · HUMAN scientific authority</div></div>`;
}

function renderJourney() {
  return commonHeader("Research Journey R0–R16", "A living research-lab view, not a progress gate.") + `
    <div class="detail-grid"><div class="stack"><div class="card"><h3>All stages</h3>${journeyStages.map(([r,n,s,c]) => `<div class="journey-row"><span class="r-code">${r}</span><div><strong>${n}</strong><small>Status is reversible</small></div><span class="state ${c}">${s}</span></div>`).join("")}</div></div>
    <div class="stack"><div class="card"><h3>R6 — Theory Positioning</h3><div class="callout warning">NEEDS ATTENTION because a competing explanation now covers part of the same mechanism.</div><p><strong>What we found</strong></p><ul><li>23 mapped papers</li><li>5 candidate theoretical lenses</li><li>4 challenging evidence links</li><li>2 competing explanations</li></ul><p><strong>Learn</strong></p><p>Theory should be evaluated for explanatory fit and contribution, not popularity alone.</p></div><div class="card"><h3>Evidence trace</h3><div class="trace">R6 WHY → CLM-142 → CHALLENGES THEORY-006 → EVF-0092 → Paper → Source</div></div></div>
    <div class="stack"><div class="card"><h3>Suggested HUMAN actions</h3><div class="decision-bar"><button class="primary">Compare theories</button><button>Inspect mechanisms</button><button>Counter-evidence</button><button>Need more evidence</button></div></div><div class="card"><h3>Recent stage impacts</h3><p>CE-0048 affects R4, R5, R6, R11 and R12. These are attention signals, not forced transitions.</p></div></div></div>`;
}

function renderOpportunities() {
  const d = selectedDummyData();
  return commonHeader("Research Opportunities", "Investigate candidate opportunities only after known evidence and existing solutions are visible.") + `
  <div class="card"><table class="table"><thead><tr><th>ID</th><th>Candidate</th><th>Gap evidence</th><th>Novelty</th><th>Counter risk</th><th>Theory value</th><th>Method feasibility</th><th>State</th></tr></thead><tbody>${d.opportunities.map(([id,title,score,,status],i)=>`<tr><td><strong>${id}</strong></td><td>${title}</td><td>${score}</td><td>${[52,78,44,61][i]}</td><td>${[68,31,74,46][i]}</td><td>${[82,71,69,58][i]}</td><td>${[73,80,66,75][i]}</td><td><span class="state ${stateClass(status)}">${status}</span></td></tr>`).join("")}</tbody></table></div>
  <div class="detail-grid" style="margin-top:14px"><div class="card"><h3>What We Know</h3><p>Current evidence suggests the candidate mechanism matters in several contexts, but findings are not uniform.</p><div class="callout">Traceable synthesis: 7 supports · 3 challenges · 2 addresses</div></div><div class="card"><h3>Existing Solutions — before Novelty</h3><ul><li>SOL-003 — adjacent framework</li><li>SOL-008 — partial mechanism overlap</li><li>SOL-011 — related boundary-condition solution</li></ul><p><strong>Residual question:</strong> Is the unresolved issue a mechanism, boundary condition, or terminology overlap?</p></div><div class="card"><h3>HUMAN Judgment</h3><div class="decision-bar"><button>Review</button><button>Modify</button><button class="primary">Accept direction</button><button>Reject candidate</button><button>Need more evidence</button></div></div></div>`;
}

function renderEvidence() {
  return commonHeader("Evidence Explorer", "Trace research interpretation back to Paper/Work, Passage/Record, Claim and Evidence Relationship.") + `
  <div class="detail-grid"><div class="card"><h3>Evidence Results</h3><div class="change-row"><div class="change-main"><strong>CLM-142</strong><small>CHALLENGES GAP-014 · FULL_TEXT</small></div><span class="state red">CONTESTED</span></div><div class="change-row"><div class="change-main"><strong>CLM-151</strong><small>SUPPORTS GAP-014 · ABSTRACT_ONLY</small></div><span class="state green">REVIEWED</span></div><div class="change-row"><div class="change-main"><strong>CLM-166</strong><small>ADDRESSES GAP-014 · FULL_TEXT</small></div><span class="state blue">EXTRACTED</span></div></div>
  <div class="card"><h3>Evidence Detail — CLM-142</h3><p><strong>Paper:</strong> Example study of governance/capability under disruption</p><p><strong>Access:</strong> FULL_TEXT</p><p><strong>Relevant passage:</strong> [bounded dummy passage displayed here]</p><p><strong>Extracted claim:</strong> An established mechanism explains part of the phenomenon currently attributed to GAP-014.</p><div class="callout warning">Audit flag: claim scope should remain bounded to the studied context.</div></div>
  <div class="card"><h3>Research Context / Backlinks</h3><div class="trace">Source<br>↓<br>Paper/Work<br>↓<br>EVF-0092<br>↓<br>CLM-142<br>↓<br>CHALLENGES GAP-014<br>↓<br>R4 · R5 · R12<br>↓<br>Human Decision HD-0031</div></div></div>`;
}

function renderEvolution() {
  return commonHeader("Knowledge Evolution", "Track how understanding changed, which evidence caused it, and what needs renewed HUMAN attention.") + `
  <div class="detail-grid"><div class="card"><h3>GAP-014 Timeline</h3><div class="timeline"><div class="timeline-item"><time>Sep 01</time><strong>CANDIDATE</strong><p>Initial synthesis identified mechanism uncertainty.</p></div><div class="timeline-item"><time>Sep 04</time><strong>STRENGTHENING</strong><p>Two supporting claims were added.</p></div><div class="timeline-item"><time>Sep 06</time><strong>CONTESTED</strong><p>SOL-008 discovered.</p></div><div class="timeline-item"><time>Sep 08</time><strong>CONTESTED — formulation narrowed</strong><p>Boundary condition found; HUMAN review requested.</p></div></div></div>
  <div class="card"><h3>Reasoning Delta</h3><p><strong>Before</strong><br>The broad gap looked plausible.</p><p><strong>New information</strong><br>A prior solution overlaps part of the proposed mechanism.</p><p><strong>After</strong><br>The gap may remain defensible only under a narrower boundary condition.</p><p><strong>Uncertainty</strong><br>Full-text and adjacent-domain coverage remain incomplete.</p></div>
  <div class="card"><h3>Human Context</h3><p>Previous decision: <strong>ACCEPT DIRECTION</strong> on Sep 04.</p><div class="callout warning">New evidence may affect the previous decision. The decision has not been changed automatically.</div><div class="decision-bar" style="margin-top:10px"><button class="primary">Open Human Review</button></div></div></div>`;
}

function renderReview() {
  return commonHeader("Human Review", "Scientific attention and reasoned HUMAN judgment — never an operational gate.") + `
  <div class="detail-grid"><div class="card"><h3>Review Queue</h3><div class="change-row"><div class="change-main"><strong>GAP-014 — Existing solution overlap</strong><small>R5 · R11 · R12</small></div><span class="state red">NEED REVIEW</span></div><div class="change-row"><div class="change-main"><strong>THEORY-006 — Competing explanation</strong><small>R6 · R14</small></div><span class="state yellow">NEED REVIEW</span></div><div class="change-row"><div class="change-main"><strong>CLM-204 — Provenance uncertain</strong><small>R2 · R13</small></div><span class="state red">NEED REVIEW</span></div></div>
  <div class="card"><h3>Why Now?</h3><p>GAP-014 changed from STRENGTHENING to CONTESTED after SOL-008 was discovered.</p><h3>Supporting Evidence</h3><p>3 papers / 7 evidence relationships.</p><h3>Counter-Evidence</h3><p>2 papers directly challenge the broad formulation.</p><h3>Coverage</h3><p>Prior-solution search remains LIMITED because one discovery source is degraded.</p></div>
  <div class="card"><h3>HUMAN Judgment</h3><p>Previous: <strong>ACCEPT DIRECTION</strong></p><label>Rationale<textarea style="width:100%;min-height:110px;margin-top:6px;border:1px solid #dfe6f1;border-radius:8px;padding:9px">The narrower formulation appears defensible, but more counter-search is needed.</textarea></label><div class="decision-bar" style="margin-top:10px"><button>Review</button><button>Modify</button><button class="primary">Accept direction</button><button>Reject</button><button>Need more evidence</button></div></div></div>`;
}

function renderCoverage() {
  return commonHeader("Coverage & Health", "Distinguish what the system could observe from what the science actually means.") + `
  <div class="detail-grid"><div class="card"><h3>Source Health</h3>${health.map(([s,status,cls,detail])=>`<div class="health-row"><div><strong>${s}</strong><small>${detail}</small></div><span class="state ${cls}">${status}</span></div>`).join("")}</div>
  <div class="card"><h3>Evidence Access Coverage</h3><p><strong>Project corpus denominator:</strong> 312 normalized works</p><ul><li>FULL_TEXT — 150 (48.1%)</li><li>ABSTRACT_ONLY — 121 (38.8%)</li><li>METADATA_ONLY — 41 (13.1%)</li></ul><div class="callout warning">Absence of discovered evidence is not evidence of absence.</div></div>
  <div class="card"><h3>Scientific Impact</h3><p><strong>Prior-solution search:</strong> LIMITED</p><p><strong>Gap falsification:</strong> LIMITED</p><p><strong>Existing stored evidence:</strong> PRESERVED</p><p><strong>Healthy crawling:</strong> CONTINUING</p><div class="callout">Semantic Scholar degradation does not automatically strengthen GAP-014.</div></div></div>`;
}

function renderProfiles() {
  const isA = profileSelect.selectedIndex === 0;
  return commonHeader("Research Profile / Project Configuration", "Domain context is configuration; scientific intent belongs to a Project.") + `
  <div class="detail-grid"><div class="card"><h3>${isA ? "Profile A — Computer / Information Systems" : "Profile B — Management / Organization Studies"}</h3><p><strong>Core interests</strong></p><ul>${(isA ? ["IT Governance","e-Government / Digital Government","Enterprise Architecture"] : ["Organizational Resilience","Human Behaviour","Human Capability"]).map(x=>`<li>${x}</li>`).join("")}</ul><p><strong>Seed literature:</strong> 12 works</p><p><strong>Watchlists:</strong> 4 active</p></div>
  <div class="card"><h3>Selected Project</h3><p><strong>${selectedProjectLabel()}</strong></p><p>Research intent is provisional and feeds R0 rather than pre-completing the research journey.</p><div class="callout">AI suggestions: 3 concepts · 2 theory candidates · 2 method candidates. HUMAN Accept / Modify / Reject.</div></div>
  <div class="card"><h3>Generality Check</h3><ul><li>Same core objects</li><li>Same R0–R16 journey</li><li>Same Evidence Explorer</li><li>Same ChangeEvent logic</li><li>Same Human Review</li></ul><p><strong>No domain-specific core branch required.</strong></p></div></div>`;
}

function renderTelegram() {
  return commonHeader("Telegram Research Radar", "A compressed, non-canonical attention channel that points back to the cockpit.") + `
  <div class="detail-grid"><div class="card"><h3>Daily Research Radar</h3><p><strong>${selectedProjectLabel()}</strong></p><ul><li>14 new relevant works</li><li>5 new evidence-backed claims</li><li>GAP-014 became CONTESTED</li><li>1 competing theory deserves review</li><li>R5 and R12 need HUMAN attention</li></ul><div class="callout warning">Coverage: 2 sources healthy · 1 degraded.</div></div>
  <div class="card"><h3>High-value alert</h3><p><strong>EXISTING SOLUTION DISCOVERED</strong></p><p>SOL-008 may address part of GAP-014. The contribution may need a narrower boundary condition.</p><p>Evidence: 1 new full-text paper · 2 linked claims.</p><button class="text-button">Open Gap–Solution Workspace</button></div>
  <div class="card"><h3>Radar Rules</h3><ul><li>No raw crawler logs</li><li>No automatic scientific decisions</li><li>No canonical state in Telegram</li><li>Delivery failure stays local</li><li>Deep-link back to Dashboard</li></ul></div></div>`;
}

const renderers = { journey:renderJourney, opportunities:renderOpportunities, evidence:renderEvidence, evolution:renderEvolution, review:renderReview, coverage:renderCoverage, profiles:renderProfiles, telegram:renderTelegram };

function showView(name) {
  document.querySelectorAll(".view").forEach(v => v.classList.remove("active-view"));
  document.querySelectorAll(".nav-item").forEach(v => v.classList.toggle("active", v.dataset.view === name));
  const view = document.getElementById(`view-${name}`);
  if (name !== "today" && renderers[name]) view.innerHTML = renderers[name]();
  view.classList.add("active-view");
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

fetch("/api/context").then(r => r.json()).then(rows => {
  const profiles = [...new Map(rows.map(r => [r.profile_id, r])).values()];
  profileSelect.innerHTML = profiles.map(r => `<option value="${r.profile_id}">${r.profile_name}</option>`).join("");
  const bindProjects = () => {
    const projects = rows.filter(r => r.profile_id === profileSelect.value);
    projectSelect.innerHTML = projects.map(r => `<option value="${r.project_id}">${r.project_name}</option>`).join("");
    renderLatestPapers();
  };
  profileSelect.onchange = () => { bindProjects(); };
  bindProjects();
}).catch(console.error);
