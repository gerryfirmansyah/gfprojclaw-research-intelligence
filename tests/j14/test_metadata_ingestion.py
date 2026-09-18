import json,os,subprocess,sys
from pathlib import Path
import psycopg
ROOT=Path(__file__).resolve().parents[2]; TOOL=ROOT/"tools"/"ingest_discovery_metadata.py"; DSN=os.environ["GFPROJ_PILOT_DSN"]
PROJECT="a2000000-0000-0000-0000-000000000001"; VERSION="a3000000-0000-0000-0000-000000000001"
def run(tmp_path,envelope,retrieved="2026-09-18T08:00:00Z",ok=True):
 p=tmp_path/"e.json";p.write_text(json.dumps(envelope));r=subprocess.run([sys.executable,str(TOOL),"--envelope",str(p),"--retrieved-at",retrieved,"--apply"],env=os.environ.copy(),text=True,capture_output=True)
 assert (r.returncode==0)==ok,(r.stdout,r.stderr);return r
def env(records,version=VERSION):return {"source_key":"openalex","project_id":PROJECT,"project_version_id":version,"records":records}
def rec(oid="https://openalex.org/WJ14TEST1",doi="https://doi.org/10.5555/j14.test.1",title="J14 synthetic metadata fixture"):return {"openalex_id":oid,"doi":doi,"title":title,"publication_date":"2026-01-02","publication_year":2026,"type":"article","has_abstract":False,"payload_hash":"fixture-hash"}
def count(sql):
 with psycopg.connect(DSN) as c:return c.execute(sql).fetchone()[0]
def test_idempotent_and_scientific_boundary(tmp_path):
 x=env([rec()]);run(tmp_path,x);run(tmp_path,x)
 assert count("SELECT count(*) FROM work_identifier WHERE identifier_value IN ('WJ14TEST1','10.5555/j14.test.1')")==2
 assert count("SELECT count(*) FROM project_work_relevance WHERE project_id='"+PROJECT+"' AND origin='openalex_pilot_ingest'")==1
 assert count("SELECT count(*) FROM human_decision")==0
 assert count("SELECT count(*) FROM claim")==0
 assert count("SELECT count(*) FROM evidence_fragment")==0
def test_stale_version_fails_closed(tmp_path):
 r=run(tmp_path,env([rec("https://openalex.org/WJ14TEST2","10.5555/j14.test.2")],"00000000-0000-0000-0000-000000000099"),ok=False);assert "stale project version" in r.stderr
def test_identifier_collision_fails_locally(tmp_path):
 run(tmp_path,env([rec("https://openalex.org/WJ14COLA","10.5555/j14.cola")]),"2026-09-18T08:01:00Z")
 run(tmp_path,env([rec("https://openalex.org/WJ14COLB","10.5555/j14.colb")]),"2026-09-18T08:02:00Z")
 r=run(tmp_path,env([rec("https://openalex.org/WJ14COLA","10.5555/j14.colb","collision")]),"2026-09-18T08:03:00Z",False);assert "identifier collision" in r.stderr
