#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,urllib.parse,urllib.request
API='http://127.0.0.1:8080'; PROJECTS=[('Profile A','3a100000-0000-4000-8000-000000000001'),('Profile B','3b100000-0000-4000-8000-000000000001')]
def get(pid):
    with urllib.request.urlopen(f'{API}/api/projects/{pid}/daily-attention?hours=24',timeout=10) as r:return json.load(r)
def build():
    lines=['GFPROJCLAW — Radar Riset Harian','','WHAT CHANGED? (24 jam)']; states=[]; total_changes=0
    for label,pid in PROJECTS:
        x=get(pid); states.append((label,x)); n=sum(len(x[k]) for k in ('new_papers','new_claims','new_contradictory_evidence','advice_critic_changes')); total_changes+=n
        lines.append(f"{label}: {len(x['new_papers'])} paper baru; {len(x['new_claims'])} Claim baru; {len(x['new_contradictory_evidence'])} bukti menantang/kontradiktif; {len(x['advice_critic_changes'])} perubahan Advice & Critic.")
    if total_changes==0: lines.append('Tidak ada perubahan canonical baru yang terdeteksi dalam 24 jam terakhir.')
    lines += ['','WHAT NEEDS MY ATTENTION?']
    for label,x in states:
        nr=sum(1 for r in x['attention_claims'] if r.get('review_state')=='NEEDS_REVIEW'); co=sum(1 for r in x['attention_claims'] if r.get('review_state')=='CONTESTED')
        lines.append(f'{label}: {nr} NEEDS_REVIEW; {co} CONTESTED.')
        cov=x.get('coverage') or {}; cs=cov.get('counter_search_state')
        lines.append(f"  Counter-search: {cs if cs else 'NOT_AVAILABLE'}.")
    lines += ['','STATUS RADAR','Pemeriksaan harian selesai; projection canonical dapat dibaca.','', 'WHY / INSPECT EVIDENCE','Buka GFPROJCLAW → Research Object → Claim → EvidenceFragment → Paper → Advice & Critic → Tinjauan HUMAN.','Telegram hanya radar read-only; keputusan ilmiah tetap milik HUMAN.','Buka GFPROJCLAW Research Copilot: https://gerryfirmansyah.github.io/gfprojclaw-research-intelligence/prototype/']
    return '\n'.join(lines)
def send(text):
    token=os.environ.get('TELEGRAM_BOT_TOKEN'); chat=os.environ.get('TELEGRAM_CHAT_ID')
    if not token or not chat: raise RuntimeError('Telegram credentials are not configured')
    data=urllib.parse.urlencode({'chat_id':chat,'text':text,'disable_web_page_preview':'true'}).encode(); req=urllib.request.Request(f'https://api.telegram.org/bot{token}/sendMessage',data=data,method='POST')
    with urllib.request.urlopen(req,timeout=30) as r: out=json.load(r)
    if out.get('ok') is not True: raise RuntimeError('Telegram rejected message')
    return out['result']['message_id']
def main():
    p=argparse.ArgumentParser(); p.add_argument('--send',action='store_true'); a=p.parse_args(); text=build()
    print('GFPROJCLAW_ATTENTION_RADAR_SENT',send(text)) if a.send else print(text)
if __name__=='__main__': main()
