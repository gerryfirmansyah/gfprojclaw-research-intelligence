from pathlib import Path
import importlib.util
from datetime import datetime
from zoneinfo import ZoneInfo
path=Path('tools/send_attention_radar.py'); spec=importlib.util.spec_from_file_location('radar',path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.context=lambda:[{'project_id':'p','profile_name':'A','project_name':'P','research_intent':'R'}]
m.get=lambda pid:{'new_papers':[],'new_claims':[],'new_contradictory_evidence':[],'advice_critic_changes':[],'attention_claims':[],'coverage':{'counter_search_state':'NOT_RUN'}}
s=m.build(datetime(2026,9,21,8,0,tzinfo=ZoneInfo('Asia/Jakarta')))
assert 'Radar dibuat: 21 Sep 2026 · 08:00 WIB' in s
assert 'Jendela observasi: 20 Sep 2026 · 08:00 — 21 Sep 2026 · 08:00 WIB (24 jam)' in s
print('ATTENTION_RADAR_TIMESTAMP_PASS')
