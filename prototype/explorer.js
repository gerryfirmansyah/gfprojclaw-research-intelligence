const API_BASE=location.hostname.endsWith("github.io")?"https://api.116.212.72.79.nip.io":"";
const esc=x=>String(x??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const project=document.getElementById("explorer-project"),state=document.getElementById("seed-universe-state"),summary=document.getElementById("seed-universe-summary"),papers=document.getElementById("seed-paper-list"),queries=document.getElementById("seed-query-options");
const roleLabel=x=>({"CORE_PHENOMENON":"Fenomena inti","PUBLIC_SECTOR_CONTEXT":"Konteks sektor publik","DECISION_APPLICATION":"Keputusan / aplikasi","RESPONSIBILITY_EXPLAINABILITY":"Responsibility / explainability","LANDSCAPE_REVIEW":"Pemetaan landscape"})[x]||"Istilah dari seed";
async function loadSeedUniverse(){
 if(!project.value)return;state.textContent="LOADING";
 try{const r=await fetch(`${API_BASE}/api/projects/${encodeURIComponent(project.value)}/seed-universe`,{cache:"no-store"});if(!r.ok)throw new Error(`HTTP ${r.status}`);const x=await r.json();
 state.textContent=x.observed_universe_state||"UNKNOWN";state.className=`state ${x.observed_universe_state==="OBSERVED"?"green":"gray"}`;
 summary.innerHTML=`<strong>${esc(x.seed_count)} seed paper</strong> · Research Universe: <strong>${esc(x.observed_universe_state)}</strong><br>${esc(x.explanation)}<br><small>Scientific decision: false · Seed ≠ Universe · Discovery ≠ Evidence</small>`;
 papers.innerHTML=(x.seeds||[]).map((p,i)=>`<article class="explorer-seed"><strong>${i+1}. ${esc(p.title)}</strong><p>${esc(p.publication_year||"NOT_RECORDED")} · ${esc(p.venue_name||"NOT_RECORDED")} · ${esc(p.access_level||"NOT_RECORDED")}</p><details><summary>Canonical detail</summary><small>Work: ${esc(p.work_id)} · source: ${esc(p.source_key||"NOT_RECORDED")}</small></details></article>`).join("")||'<div class="callout">Seed paper NOT_AVAILABLE.</div>';
 const groups={};(x.query_family_candidates||[]).forEach(q=>(groups[q.family_role]??=[]).push(q));
 queries.innerHTML=Object.entries(groups).map(([role,items])=>`<section class="query-family"><h4>${esc(roleLabel(role))}</h4><p class="explorer-muted">Opsi untuk memperluas pencarian; bukan scope yang ditetapkan mesin.</p>${items.map(q=>`<article class="explorer-query"><div><strong>${esc(q.label)}</strong><code>${esc(q.candidate_query)}</code><span class="state gray">NOT APPROVED</span></div><p><strong>Mengapa ditampilkan?</strong> ${esc(q.why_shown)}</p><p><strong>Paper pemicu:</strong> ${q.seed_titles.map(esc).join(" · ")}</p><p><strong>Yang perlu HUMAN periksa:</strong> ${esc(q.human_check)}</p><details><summary>Canonical provenance</summary><small>Work ID: ${q.seed_work_ids.map(esc).join(" · ")}</small></details></article>`).join("")}</section>`).join("")||'<div class="callout">Query option NOT_AVAILABLE.</div>';
 }catch(e){state.textContent="NOT_AVAILABLE";summary.textContent=`Seed projection tidak tersedia: ${e.message}`;papers.innerHTML="";queries.innerHTML="";}
}
fetch(`${API_BASE}/api/context`,{cache:"no-store"}).then(r=>{if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.json()}).then(rows=>{project.innerHTML=rows.map(x=>`<option value="${esc(x.project_id)}">${esc(x.profile_name)} / ${esc(x.project_name)}</option>`).join("");project.onchange=loadSeedUniverse;loadSeedUniverse();}).catch(e=>{project.innerHTML='<option>Context unavailable</option>';summary.textContent=`Context tidak tersedia: ${e.message}`;});
const benchResult=document.getElementById("bench-result"),benchPreview=document.getElementById("bench-preview");
if(benchPreview)benchPreview.onclick=()=>{
 const total=document.getElementById("bench-total").value,captured=document.getElementById("bench-captured").value,query=document.getElementById("bench-query").value.trim(),time=document.getElementById("bench-time").value,params=document.getElementById("bench-params").value.trim();
 const members=document.getElementById("bench-members").value.split(/\n+/).map(x=>x.trim()).filter(Boolean);
 if(!query||!time){benchResult.innerHTML="<strong>INCOMPLETE</strong> · Exact query dan waktu pencarian diperlukan sebelum benchmark dapat dibandingkan.";return;}
 const parity=params?"PARITY_REQUIRES_REVIEW":"NON_PARITY_COMPARISON";
 benchResult.innerHTML="<strong>HUMAN observation draft</strong><br>Provider reported: <strong>"+esc(total||"NOT_AVAILABLE")+"</strong> · HUMAN captured: <strong>"+esc(captured||"NOT_AVAILABLE")+"</strong> · Member identifiers: <strong>"+members.length+"</strong><br>Comparison readiness: <strong>"+parity+"</strong><br>Overlap / HUMAN-only / Machine-only: <strong>NOT_AVAILABLE</strong> sampai machine observation dan member reconciliation tersedia.<br><small>Local preview only · no canonical write · scientific decision: false</small>";
};

const initialQuery=document.getElementById("initial-human-query"),initialPreview=document.getElementById("initial-query-preview"),initialResult=document.getElementById("initial-query-result");
if(initialPreview)initialPreview.onclick=()=>{
 const q=initialQuery.value.trim();
 if(!q){initialResult.innerHTML="<strong>INCOMPLETE</strong> · Query awal HUMAN diperlukan.";return;}
 initialResult.innerHTML="<strong>Baseline preview:</strong> "+esc(q)+"<br><small>Origin: HUMAN_PROVIDED · approval state: LOCAL_PREVIEW · canonical write: false · scientific decision: false · historical J14 query unchanged</small>";
};
