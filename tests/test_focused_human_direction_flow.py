from pathlib import Path
js=Path("prototype/research-workspace.js").read_text()
css=Path("prototype/styles.css").read_text()
required=["focused-note","HUMAN Research Direction","Lanjutkan investigasi ini → Research Copilot","Revisi arah investigasi","Evidence belum cukup","gfprojclaw-focused-investigation","focused_investigation","human_direction:\'CONTINUE_INVESTIGATION\'"]
for x in required:
    assert x in js, x
assert ".research-workspace #opportunity-analysis{border:0" in css
assert ".research-workspace .focused-investigation{width:calc(100vw - 96px)" in css
print("FOCUSED_HUMAN_DIRECTION_FLOW_PASS")
