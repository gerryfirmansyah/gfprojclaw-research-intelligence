from pathlib import Path
h=Path("prototype/research-workspace.html").read_text()
c=Path("prototype/styles.css").read_text()
assert 'id="discovery-benchmark" class="panel explorer-start-panel workspace-hidden-legacy"' in h
assert 'id="start" class="panel explorer-start-panel workspace-hidden-legacy"' in h
assert '.research-workspace #discovery-benchmark' in c
assert '.research-workspace #start {display:none!important}' in c
assert 'id="discovery-benchmark" class="panel explorer-start-panel">' not in h
assert 'id="start" class="panel explorer-start-panel">' not in h
print("WORKSPACE_LEGACY_ENTRY_REMOVED_PASS")
