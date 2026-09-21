from pathlib import Path

contract = Path("docs/j16/pre-research-exploration-journey-contract-v0.md").read_text()
migration = Path("db/migrations/013_pre_research_discovery_observation.sql").read_text()

for token in [
    "Explore → Decide → Research → Observe → Reconsider",
    "A small Project Corpus is an outcome to explain, never a target",
    "HUMAN Scope Decision",
    "Canonical Discovery Observation requirement",
    "UNKNOWN, NOT_AVAILABLE, NOT_RECORDED, and NOT_RUN",
    "Continuous production crawling remains a separate explicit operational gate",
]:
    assert token in contract, token

for table in [
    "research_exploration_session",
    "research_scope_node",
    "discovery_query_family",
    "discovery_query",
    "discovery_observation",
]:
    assert f"CREATE TABLE {table}" in migration, table

for token in [
    "scope_level IN ('L0','L1','L2','L3','L4')",
    "REFERENCES literature_source(id)",
    "REFERENCES source_record(id)",
    "REFERENCES continuous_pilot_run(id)",
    "REFERENCES continuous_pilot_stage_run(id)",
    "REVOKE INSERT, UPDATE, DELETE",
    "GRANT SELECT",
]:
    assert token in migration, token

lower = migration.lower()
# Comments may mention HUMAN decisions; prohibit schema/data operations that create them.
assert "create table human_decision" not in lower
assert "insert into human_decision" not in lower
assert "update human_decision" not in lower
assert "delete from human_decision" not in lower
assert "INSERT INTO" not in migration.upper()
print("PRE_RESEARCH_EXPLORATION_CONTRACT_PASS")
