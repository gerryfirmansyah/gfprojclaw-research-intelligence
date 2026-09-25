from pathlib import Path
A=Path("prototype/app.js").read_text(); C=Path("prototype/styles.css").read_text(); H=Path("prototype/index.html").read_text()
checks=[
("01 active session reader",'function activeSession()' in A),
("02 focused state reader",'function activeFocused()' in A),
("03 session header",'function sessionHeader' in A),
("04 one-frame evidence",'function sessionEvidenceRows' in A and 'table-frame active-session-table' in A),
("05 opportunity active renderer",'function renderActiveOpportunities' in A),
("06 evidence active renderer",'function renderActiveEvidence' in A),
("07 evolution active renderer",'function renderActiveEvolution' in A),
("08 human review active renderer",'function renderActiveReview' in A),
("09 coverage active renderer",'function renderActiveCoverage' in A),
("10 profile active renderer",'function renderActiveProfiles' in A),
("11 radar active renderer",'function renderActiveTelegram' in A),
("12 active renderer routing",'const activeRenderers=' in A),
("13 stale loaders gated",'if (!sessionMode) {' in A),
("14 dashboard session gate",'const sf=activeFocused();' in A and 'bindOpenButtons(); return;' in A),
("15 dashboard no stale change",'State lama tidak dirender pada sesi ini.' in A),
("16 dashboard no stale radar",'0 item sesi aktif — belum ada canonical ChangeEvent.' in A),
("17 old profile selector suppressed",'Active Research Session' in A and 'profileSelect.disabled=true' in A),
("18 old project selector suppressed",'Focused Investigation / IO aktif' in A and 'projectSelect.disabled=true' in A),
("19 noncanonical boundary explicit",'NON-CANONICAL sampai HUMAN membuat explicit scientific write/decision.' in A),
("20 readable active-session surface",'.active-session-strip' in C and 'font-size:19px' in C and 'Prototype v0.19.0' in H),
]
for name,ok in checks:
    assert ok,name
    print(name,"PASS")
print("ACTIVE_SESSION_20_STAGE_PASS")
