#!/usr/bin/env python3
import argparse,json,time,urllib.parse,urllib.request

def abstract_text(index):
    if not index:return None
    out=[]
    for word,positions in index.items():
        for pos in positions:out.append((pos,word))
    return ' '.join(w for _,w in sorted(out))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ids',required=True,help='comma separated OpenAlex IDs');ap.add_argument('--output',required=True);ap.add_argument('--delay',type=float,default=.1);a=ap.parse_args()
    rows=[]
    for oid in [x.strip() for x in a.ids.split(',') if x.strip()]:
        wid=oid.rsplit('/',1)[-1]
        req=urllib.request.Request('https://api.openalex.org/works/'+urllib.parse.quote(wid),headers={'User-Agent':'GFPROJCLAW-HUMAN-Verification/0.1'})
        try:
            with urllib.request.urlopen(req,timeout=20) as r:x=json.loads(r.read())
            txt=abstract_text(x.get('abstract_inverted_index'))
            rows.append({'openalex_id':x.get('id'),'title':x.get('title'),'doi':x.get('doi'),'abstract':txt,'abstract_state':'AVAILABLE' if txt else 'NOT_AVAILABLE_FROM_OPENALEX','source_url':x.get('id'),'scientific_decision':False})
        except Exception as e: rows.append({'openalex_id':oid,'abstract':None,'abstract_state':'FETCH_FAILED','error':str(e),'scientific_decision':False})
        time.sleep(a.delay)
    out={'mode':'TRIAL_PROGRESSIVE_ABSTRACT_VERIFICATION','papers':rows,'canonical_write':False,'scientific_decision':False}
    json.dump(out,open(a.output,'w'),ensure_ascii=False,indent=2);print(json.dumps({'requested':len(rows),'available':sum(bool(x.get('abstract')) for x in rows)}))
if __name__=='__main__':main()
