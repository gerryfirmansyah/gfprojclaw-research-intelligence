const API_BASE = "https://api.116.212.72.79.nip.io";
const projectSelect = document.getElementById("admin-project-select");
const esc = v => String(v ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));

function applyTheme(theme) { document.documentElement.dataset.theme = theme; const b=document.getElementById("theme-toggle"); b.textContent=theme==="dark"?"☀️ Light":"🌙 Dark"; }
applyTheme(localStorage.getItem("gfprojclaw-theme") || "light");
document.getElementById("theme-toggle").onclick=()=>{const t=document.documentElement.dataset.theme==="dark"?"light":"dark"; localStorage.setItem("gfprojclaw-theme",t); applyTheme(t);};

async function loadAdmin() {
  if (!projectSelect.value) return;
  const p=encodeURIComponent(projectSelect.value);
  const pilot=document.getElementById("admin-pilot"), sources=document.getElementById("admin-sources");
  try {
    const r=await fetch(`${API_BASE}/api/projects/${p}/pilot-health`,{cache:"no-store"}); const rows=r.ok?await r.json():[];
    pilot.innerHTML=rows.length?rows.map(x=>`<div class="change-row"><div class="change-main"><strong>${esc(x.status)} · ${esc(x.trigger_type)}</strong><small>Run ${esc(x.pilot_run_id)}</small><p>Started: ${esc(x.started_at)}<br>Finished: ${esc(x.finished_at||"RUNNING")}<br>Stage attempts: ${esc(x.stage_attempts)} · Failed attempts: ${esc(x.failed_stage_attempts)}</p><p>Stage history: ${esc((x.stage_history||[]).join(" → ")||"none")}</p></div></div>`).join(""):"<p>No Continuous Pilot run recorded.</p>";
  } catch(e) { pilot.innerHTML=`<p>Operational run data unavailable: ${esc(e.message)}</p>`; }
  try {
    const r=await fetch(`${API_BASE}/api/projects/${p}/coverage`,{cache:"no-store"}); const c=r.ok?await r.json():{};
    sources.innerHTML=(c.sources||[]).length?(c.sources||[]).map(x=>`<div class="health-row"><div><strong>${esc(x.source_key)}</strong><small>${esc(x.access_limitations||"No access limitation recorded")}</small></div><span class="state yellow">${esc(x.health_state)}</span></div>`).join(""):"<p>No persisted source observations.</p>";
  } catch(e) { sources.innerHTML=`<p>Source health unavailable: ${esc(e.message)}</p>`; }
}
fetch(`${API_BASE}/api/context`,{cache:"no-store"}).then(r=>r.json()).then(rows=>{projectSelect.innerHTML=rows.map(x=>`<option value="${esc(x.project_id)}">${esc(x.profile_name)} / ${esc(x.project_name)}</option>`).join(""); projectSelect.onchange=loadAdmin; loadAdmin();}).catch(e=>{projectSelect.innerHTML="<option>Context unavailable</option>";});

// Presentation language is local UI preference; operational/canonical payloads are not translated.
document.querySelectorAll("[data-language-select]").forEach(el=>el.addEventListener("change",event=>window.GF_I18N?.setLanguage(event.target.value)));
window.GF_I18N?.apply();
