from pathlib import Path
m=Path("db/migrations/014_research_explorer_observer_role.sql").read_text();v=Path("db/verify/014_research_explorer_observer_role_verify.sql").read_text()
for x in ["gfproj_explorer_observer","research_exploration_session","discovery_query_family","discovery_query","source_record","discovery_observation","REVOKE ALL ON project_work_relevance","human_decision","GRANT gfproj_explorer_observer TO gfproj_pilot_executor"]: assert x in m,x
for x in ["project_work_relevance','INSERT","work','INSERT","human_decision','INSERT","source_record','UPDATE","RESEARCH_EXPLORER_OBSERVER_ROLE_PASS"]: assert x in v,x
print("RESEARCH_EXPLORER_OBSERVER_ROLE_CONTRACT_PASS")
