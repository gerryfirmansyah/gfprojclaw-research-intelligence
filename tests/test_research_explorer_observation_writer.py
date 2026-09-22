from pathlib import Path
import subprocess,sys
p=Path("tools/ingest_research_explorer_observation.py"); s=p.read_text()
for x in ["research_exploration_session","discovery_query_family","discovery_query","source_record","discovery_observation","project_work_relevance","evidence_fragment","human_decision","scientific_decision", "apply disabled"]:
 assert x in s,x
assert "INSERT INTO project_work_relevance" not in s
assert "INSERT INTO evidence_fragment" not in s
assert "INSERT INTO human_decision" not in s
for env in [Path("/tmp/profile-a-openalex-preview.json"),Path("/tmp/profile-a-crossref-preview.json")]:
 if env.exists():
  r=subprocess.run([sys.executable,str(p),"--envelope",str(env),"--research-interest","Understand AI use in public services"],capture_output=True,text=True)
  assert r.returncode==0,r.stderr
  assert '"mode": "DRY_RUN"' in r.stdout
print("RESEARCH_EXPLORER_OBSERVATION_WRITER_PASS")
