from __future__ import annotations
import copy,json,sys,uuid
sys.path.insert(0,'prototype/api')
from db import db
ACTOR='gerry firmansyah'
CONFIGS={
'3a100000-0000-4000-8000-000000000001':{
 'semantic_groups':{
  'ai':['artificial intelligence','AI','algorithmic systems','automated decision making'],
  'public_governance_context':['digital government','e-government','public administration','public sector','government'],
  'governance_explanation':['governance','accountability','decision making','implementation','institutional','organizational']},
 'expression':'("artificial intelligence" OR "algorithmic systems" OR "automated decision making") AND ("digital government" OR "e-government" OR "public administration" OR "public sector" OR government) AND (governance OR accountability OR "decision making" OR implementation OR institutional OR organizational)'},
'3b100000-0000-4000-8000-000000000001':{
 'semantic_groups':{
  'resilience':['organizational resilience','organisational resilience','resilient organization','resilient organisation'],
  'human':['human capability','human capabilities','employee capability','workforce capability','human capital','employee resilience'],
  'mechanism_level':['mechanism','cross-level','multilevel','adaptive capacity','adaptation','behavior','behaviour']},
 'expression':'("organizational resilience" OR "organisational resilience" OR "resilient organization" OR "resilient organisation") AND ("human capability" OR "human capabilities" OR "employee capability" OR "workforce capability" OR "human capital" OR "employee resilience") AND (mechanism OR "cross-level" OR multilevel OR "adaptive capacity" OR adaptation OR behavior OR behaviour)'}}
with db() as conn:
 with conn.cursor() as cur:
  out=[]
  for pid,approved in CONFIGS.items():
   cur.execute('SELECT p.current_version_id,v.version_no,v.research_intent,v.provisional_rq_text,v.project_configuration_jsonb FROM research_project p JOIN research_project_version v ON v.id=p.current_version_id WHERE p.id=%s AND p.status=\'ACTIVE\' FOR UPDATE OF p',(pid,)); row=cur.fetchone()
   if not row: raise SystemExit(f'active project not found: {pid}')
   cfg=copy.deepcopy(row['project_configuration_jsonb']); existing=cfg.get('discovery_overrides') or {}
   if existing: raise SystemExit(f'fail closed: discovery_overrides already populated for {pid}')
   cfg['discovery_overrides']={'human_approved_query_v1':approved,'approval':{'actor':ACTOR,'decision':'ACCEPT_AS_PROPOSED','artifact':'docs/j14/discovery-query-candidates-v0.md','scientific_evidence':False}}
   vid=str(uuid.uuid4()); n=row['version_no']+1
   cur.execute('INSERT INTO research_project_version(id,project_id,version_no,research_intent,provisional_rq_text,project_configuration_jsonb,supersedes_version_id,created_by) VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s,%s)',(vid,pid,n,row['research_intent'],row['provisional_rq_text'],json.dumps(cfg),row['current_version_id'],ACTOR))
   cur.execute('UPDATE research_project SET current_version_id=%s WHERE id=%s',(vid,pid)); out.append({'project_id':pid,'version_no':n,'version_id':vid,'supersedes':str(row['current_version_id'])})
  print(json.dumps(out,indent=2))
