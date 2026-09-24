from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]; j=(r/'prototype/explorer.js').read_text(); api=(r/'prototype/api/server.py').read_text(); x=json.load(open(r/'data/research_value_trial/smart-city-urban-abstracts.json'))
assert len(x['papers'])==19 and all(p.get('abstract') for p in x['papers'])
for s in ['renderUrbanAdvanced','Opportunity A','Opportunity B','Opportunity C','Opportunity D','HUMAN verification required','smart-city-urban-abstracts']: assert s in j
assert 'smart-city-urban-abstracts' in api
print('SMART_CITY_URBAN_ADVANCED_PASS')
