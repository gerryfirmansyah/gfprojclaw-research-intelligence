const API_BASE=location.hostname.endsWith("github.io")?"https://api.116.212.72.79.nip.io":"";
const esc=x=>String(x??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const project=document.getElementById("explorer-project"),state=document.getElementById("seed-universe-state"),summary=document.getElementById("seed-universe-summary"),papers=document.getElementById("seed-paper-list"),queries=document.getElementById("seed-query-options");
const roleLabel=x=>({"CORE_PHENOMENON":"Fenomena inti","PUBLIC_SECTOR_CONTEXT":"Konteks sektor publik","DECISION_APPLICATION":"Keputusan / aplikasi","RESPONSIBILITY_EXPLAINABILITY":"Responsibility / explainability","LANDSCAPE_REVIEW":"Pemetaan landscape"})[x]||"Istilah dari seed";
async function loadSeedUniverse(){
 if(!project.value)return;state.textContent="LOADING";
 try{const r=await fetch(`${API_BASE}/api/projects/${encodeURIComponent(project.value)}/seed-universe`,{cache:"no-store"});if(!r.ok)throw new Error(`HTTP ${r.status}`);const x=await r.json();
 renderProgressiveFunnel({sessions:[]});
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

function renderProgressiveFunnel(x){
 const observations=(x.sessions||[]).flatMap(s=>s.observations||[]);
 const retrieved=observations.length;
 const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};
 set("f-provider","NOT_AVAILABLE");
 set("f-retrieved",retrieved);
 set("f-remaining","NOT_AVAILABLE");
 set("f-dedup",retrieved?"NOT_RECORDED":"NOT_RUN");
 set("f-screened",retrieved?"NOT_RECORDED":"NOT_RUN");
 set("f-human",retrieved?"NOT_RECORDED":"NOT_RUN");
 set("f-project","NOT_AVAILABLE");
}

const trialState=document.getElementById("trial-state"),trialCoverage=document.getElementById("trial-coverage"),trialYears=document.getElementById("trial-years"),trialAreas=document.getElementById("trial-areas"),trialAreaDetail=document.getElementById("trial-area-detail"),trialPapers=document.getElementById("trial-papers"),trialBlindspots=document.getElementById("trial-blindspots"),trialDecisions=document.getElementById("trial-decisions"),trialDecisionState=document.getElementById("trial-decision-state");
let trialWhy=null,trialPaperMap=new Map();
function renderTrialPapers(members){
 trialPapers.innerHTML=(members||[]).slice(0,30).map(m=>{const p=trialPaperMap.get(m.openalex_id)||m;return `<article class="explorer-seed"><strong>${esc(p.title||"TITLE NOT_AVAILABLE")}</strong><p>${esc(p.publication_year||"NOT_RECORDED")} · ${esc(p.venue||"VENUE NOT_RECORDED")} · DOI ${esc(p.doi||"NOT_AVAILABLE")}</p><div class="trial-paper-links">${p.source_url?`<a href="${esc(p.source_url)}" target="_blank" rel="noopener">OpenAlex ↗</a>`:""}${p.doi_url?`<a href="${esc(p.doi_url)}" target="_blank" rel="noopener">DOI ↗</a>`:""}</div><small>Abstract: ${esc(p.abstract_state||"NOT_RETRIEVED_IN_THIS_TRIAL")} · Full text: ${esc(p.full_text_state||"NOT_CHECKED")}</small></article>`}).join("")||'<div class="callout">Member paper NOT_AVAILABLE.</div>';
}
function showTrialArea(term){
 const t=(trialWhy?.traces||[]).find(x=>x.area===term);if(!t)return;
 trialAreaDetail.innerHTML=`<strong>WHY ${esc(term)}</strong><br>${esc(t.why_shown)}<br><strong>Supporting observation:</strong> ${esc(t.supporting_observation?.observed_title_count)} exact title-term members.<br><small>Machine observation only · HUMAN must inspect abstract/method/context.</small>`;
 renderTrialPapers(t.members);
}
async function loadResearchValueTrial(){
 if(!trialState)return;
 try{
  const [lr,wr,pr,cr]=await Promise.all(["landscape","why","papers","coverage"].map(x=>fetch(`${API_BASE}/api/trial/research-value/${x}`,{cache:"no-store"})));if([lr,wr,pr,cr].some(r=>!r.ok))throw new Error("trial payload unavailable");
  const [l,w,p,c]=await Promise.all([lr.json(),wr.json(),pr.json(),cr.json()]);trialWhy=w;trialPaperMap=new Map((p.papers||[]).map(x=>[x.openalex_id,x]));
  trialState.textContent="WHOLE BOUNDED";trialState.className="state green";
  const cv=l.coverage||{};trialCoverage.innerHTML=`<strong>${esc(cv.raw_retrieved_count)} / ${esc(cv.provider_reported_total)} raw OpenAlex records retrieved</strong> · ${esc(cv.retrieved_count)} deduplicated members<br><small>Query/time-bounded provider observation · not scientifically relevant count · canonical write: false</small>`;
  trialYears.innerHTML=Object.entries(l.year_landscape||{}).sort().map(([y,n])=>`<article class="trial-metric"><span>${esc(y)}</span><strong>${esc(n)}</strong></article>`).join("");
  trialAreas.innerHTML=(l.observed_areas||[]).map(a=>`<button class="trial-area" type="button" data-term="${esc(a.term)}"><strong>${esc(a.term)}</strong><br><small>${esc(a.observed_count)} title observations</small></button>`).join("");trialAreas.querySelectorAll("button").forEach(b=>b.onclick=()=>showTrialArea(b.dataset.term));
  const cov=c.coverage||{};trialBlindspots.innerHTML=`<strong>Observed:</strong> ${esc((cov.searched_sources||[]).join(", "))}<br><strong>Not searched whole-bounded:</strong> ${esc((cov.not_searched_sources||[]).join(", "))}<br>${esc(c.blind_spot_statement)}<br><small>Abstracts retrieved: ${esc(cov.abstracts_retrieved)} · Full text checked: ${esc(cov.full_text_checked)}</small>`;
  trialDecisions.innerHTML=(c.human_decision_options||[]).map(x=>`<button class="secondary-action" type="button" data-decision="${esc(x)}">${esc(x.replaceAll("_"," "))}</button>`).join("");trialDecisions.querySelectorAll("button").forEach(b=>b.onclick=()=>{trialDecisionState.innerHTML=`<strong>Local HUMAN scope reflection: ${esc(b.dataset.decision)}</strong><br><small>Preview only · no canonical write · not a machine scientific decision.</small>`});
  if(l.observed_areas?.length)showTrialArea(l.observed_areas[0].term);
 }catch(e){trialState.textContent="NOT_AVAILABLE";trialCoverage.textContent=`Trial landscape tidak tersedia: ${e.message}`;}
}
loadResearchValueTrial();
