const API_BASE = "https://api.116.212.72.79.nip.io";
const projectSelect = document.getElementById("admin-project-select");
let contextRows=[];
const esc = v => String(v ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));

function applyTheme(theme) { document.documentElement.dataset.theme = theme; const b=document.getElementById("theme-toggle"); b.textContent=theme==="dark"?"☀️ Light":"🌙 Dark"; }
applyTheme(localStorage.getItem("gfprojclaw-theme") || "light");
document.getElementById("theme-toggle").onclick=()=>{const t=document.documentElement.dataset.theme==="dark"?"light":"dark"; localStorage.setItem("gfprojclaw-theme",t); applyTheme(t);};

function renderConfig(){
  const c=contextRows.find(x=>x.project_id===projectSelect.value)||{}, box=document.getElementById("admin-config"); if(!box)return;
  box.innerHTML=`<div class="detail-grid"><div class="card"><h3>Research Profile · v${esc(c.profile_version||"—")}</h3><label>Profile name<input id="ac-profile-name" value="${esc(c.profile_name||"")}"></label><label>Summary<textarea id="ac-profile-summary">${esc(c.profile_summary||"")}</textarea></label></div><div class="card"><h3>Project · v${esc(c.project_version||"—")}</h3><label>Project name<input id="ac-project-name" value="${esc(c.project_name||"")}"></label><label>Research intent<textarea id="ac-intent">${esc(c.research_intent||"")}</textarea></label><label>Provisional RQ<textarea id="ac-rq">${esc(c.provisional_rq_text||"")}</textarea></label></div></div><label>Admin / HUMAN actor<input id="ac-actor" placeholder="required"></label><label>Reason for configuration change<textarea id="ac-reason" placeholder="required; recorded with this administrative action"></textarea></label><details><summary>Advanced JSON configuration</summary><div class="detail-grid"><label>Profile JSON<textarea id="ac-pjson">${esc(JSON.stringify(c.profile_configuration_jsonb||{},null,2))}</textarea></label><label>Project JSON<textarea id="ac-qjson">${esc(JSON.stringify(c.project_configuration_jsonb||{},null,2))}</textarea></label></div></details><div class="callout warning">Saving creates a new canonical version. Review the preview first. Administrative configuration does not make a scientific decision.</div><button class="text-button" id="ac-preview">Preview changes</button><div id="ac-preview-box"></div>`;
  document.getElementById('ac-preview').onclick=previewConfig;
}
function previewConfig(){
 const c=contextRows.find(x=>x.project_id===projectSelect.value)||{}, actor=document.getElementById('ac-actor').value.trim(), reason=document.getElementById('ac-reason').value.trim(), out=document.getElementById('ac-preview-box');
 if(!actor||!reason){out.innerHTML='<div class="callout warning">Admin/HUMAN actor and reason are required.</div>';return;} try{JSON.parse(document.getElementById('ac-pjson').value||'{}');JSON.parse(document.getElementById('ac-qjson').value||'{}')}catch(e){out.innerHTML=`<div class="callout warning">Invalid JSON: ${esc(e.message)}</div>`;return;}
 const changes=[['Profile name',c.profile_name,document.getElementById('ac-profile-name').value],['Profile summary',c.profile_summary,document.getElementById('ac-profile-summary').value],['Project name',c.project_name,document.getElementById('ac-project-name').value],['Research intent',c.research_intent,document.getElementById('ac-intent').value],['Provisional RQ',c.provisional_rq_text,document.getElementById('ac-rq').value]].filter(x=>String(x[1]||'')!==String(x[2]||''));
 out.innerHTML=`<h3>Preview</h3>${changes.length?changes.map(x=>`<p><strong>${esc(x[0])}</strong><br>Current: ${esc(x[1]||'NOT_AVAILABLE')}<br>Proposed: ${esc(x[2]||'NOT_AVAILABLE')}</p>`).join(''):'<p>No structured-field changes detected.</p>'}<p><strong>Reason:</strong> ${esc(reason)}</p><button class="text-button" id="ac-save">Confirm & create new versions</button>`;document.getElementById('ac-save').onclick=saveConfig;
}

async function loadOperationalHealth(){
 const box=document.getElementById("admin-ops-health"); if(!box)return;
 try{const r=await fetch(`${API_BASE}/api/admin/operational-health`,{cache:"no-store"});if(!r.ok)throw new Error(`HTTP ${r.status}`);const h=await r.json(), sv=h.services||{}, badge=(label,u)=>`<div class="health-row"><div><strong>${esc(label)}</strong><small>${esc(u.LoadState||"unknown")} · ${esc(u.UnitFileState||"not-enabled")}</small></div><span class="state ${u.ActiveState==="active"?"green":u.LoadState==="not-found"?"gray":"yellow"}">${esc(u.ActiveState||"UNKNOWN")}</span></div>`;box.innerHTML=`<div class="detail-grid"><div class="card"><h3>Services & Schedulers</h3>${badge("Cockpit API",sv.api||{})}${badge("Telegram daily radar",sv.telegram_timer||{})}${badge("PostgreSQL backup",sv.backup_timer||{})}${badge("Continuous Pilot",sv.continuous_pilot_timer||{})}${badge("Legacy G6–G9 (historical)",sv.legacy_g6_g9||{})}</div><div class="card"><h3>Backup & Storage</h3><p><strong>Latest backup</strong><br>${esc(h.backup?.latest_name||"NOT_AVAILABLE")} · ${h.backup?.latest_bytes?Math.round(h.backup.latest_bytes/1024)+" KB":"NOT_AVAILABLE"}</p><p><strong>Backup count</strong><br>${esc(h.backup?.count??"NOT_AVAILABLE")}</p><p><strong>Disk</strong><br>${esc(h.storage?.used_percent??"NOT_AVAILABLE")}% used · ${h.storage?.free_bytes?Math.round(h.storage.free_bytes/1073741824)+" GB free":"NOT_AVAILABLE"}</p></div></div><div class="callout">Operational projection is read-only and reports scientific_decision=false. A disabled/not-found Continuous Pilot is not treated as a scientific failure.</div>`;}catch(e){box.innerHTML=`<div class="callout warning">Production health unavailable: ${esc(e.message)}</div>`;}
}

async function loadAdmin() {
  if (!projectSelect.value) return;
  renderConfig();
  loadOperationalHealth();
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
fetch(`${API_BASE}/api/context`,{cache:"no-store"}).then(r=>r.json()).then(rows=>{contextRows=rows; projectSelect.innerHTML=rows.map(x=>`<option value="${esc(x.project_id)}">${esc(x.profile_name)} / ${esc(x.project_name)}</option>`).join(""); projectSelect.onchange=loadAdmin; loadAdmin();}).catch(e=>{projectSelect.innerHTML="<option>Context unavailable</option>";});

// Presentation language is local UI preference; operational/canonical payloads are not translated.
document.querySelectorAll("[data-language-select]").forEach(el=>el.addEventListener("change",event=>window.GF_I18N?.setLanguage(event.target.value)));
window.GF_I18N?.apply();

async function saveConfig(){
 const c=contextRows.find(x=>x.project_id===projectSelect.value)||{}, out=document.getElementById('ac-preview-box');
 const actor=document.getElementById('ac-actor').value.trim(), reason=document.getElementById('ac-reason').value.trim();
 if(!actor||!reason){out.innerHTML='<div class="callout warning">Actor dan alasan perubahan wajib diisi.</div>';return;}
 let pc,qc; try{pc=JSON.parse(document.getElementById('ac-pjson').value||'{}');qc=JSON.parse(document.getElementById('ac-qjson').value||'{}');}catch(e){out.innerHTML=`<div class="callout warning">JSON tidak valid: ${esc(e.message)}</div>`;return;}
 const payload={profile_id:c.profile_id,project_id:c.project_id,actor,reason,profile:{name:document.getElementById('ac-profile-name').value.trim(),summary:document.getElementById('ac-profile-summary').value.trim(),configuration:pc},project:{name:document.getElementById('ac-project-name').value.trim(),research_intent:document.getElementById('ac-intent').value.trim(),provisional_rq_text:document.getElementById('ac-rq').value.trim(),configuration:qc}};
 if(!payload.profile.name||!payload.project.name||!payload.project.research_intent){out.innerHTML='<div class="callout warning">Nama profil, nama proyek, dan research intent tidak boleh kosong.</div>';return;}
 try{const r=await fetch(`${API_BASE}/api/admin/profile-project-configuration`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const x=await r.json();if(!r.ok)throw new Error(x.error||`HTTP ${r.status}`);if(x.scientific_decision!==false||x.atomic!==true)throw new Error('Administrative boundary response invalid');out.innerHTML=`<div class="callout">Versi canonical baru tersimpan secara atomic: Profile v${esc(x.profile_version)}, Project v${esc(x.project_version)}. Muat ulang untuk membaca state terbaru.</div>`;}catch(e){out.innerHTML=`<div class="callout warning">Tidak tersimpan: ${esc(e.message)}</div>`;}
}
