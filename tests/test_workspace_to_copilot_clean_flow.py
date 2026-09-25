from pathlib import Path
w=Path('prototype/research-workspace.js').read_text()
a=Path('prototype/app.js').read_text()
h=Path('prototype/research-workspace.html').read_text()
i=Path('prototype/index.html').read_text()
checks={
'01_old_checkpoint_removed':'9 · HUMAN checkpoint' not in w,
'02_old_next_move_removed':'10 · Next research move' not in w,
'03_old_roadmap_removed':'10 langkah penelitian mendalam' not in w,
'04_decision_gate':'Keputusan HUMAN' in w,
'05_focused_stage':'FOCUSED INVESTIGATION' in w,
'06_human_direction':'HUMAN Research Direction' in w,
'07_focused_handoff':'focused=o?.focused_investigation' in a,
'08_no_repeat_assessment':'assessment tidak diulang' in a,
'09_copilot_next_question':'Research Copilot · Next Verification Question' in a,
'10_back_to_workspace':'Kembali ke Research Workspace' in i and 'Focused Investigation → 6 HUMAN Direction → 7 Copilot' in h,
}
for k,v in checks.items():
    assert v,k
    print(k,'PASS')
