#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--project-id',action='append',required=True); ap.add_argument('--hours',type=int,default=24); ap.add_argument('--send',action='store_true'); a=ap.parse_args()
    renderer=Path(__file__).with_name('render_telegram_daily_digest.py')
    messages=[subprocess.check_output([sys.executable,str(renderer),'--project-id',project_id,'--hours',str(a.hours)],text=True).strip() for project_id in a.project_id]
    if not a.send:
        print('\n\n'.join(messages)); print('\n[DRY RUN: Telegram delivery not attempted]'); return
    token=os.environ.get('TELEGRAM_BOT_TOKEN'); chat=os.environ.get('TELEGRAM_CHAT_ID')
    if not token or not chat: raise SystemExit('Telegram credentials unavailable')
    for msg in messages:
        data=urllib.parse.urlencode({'chat_id':chat,'text':msg,'disable_web_page_preview':'true'}).encode()
        req=urllib.request.Request(f'https://api.telegram.org/bot{token}/sendMessage',data=data,method='POST')
        with urllib.request.urlopen(req,timeout=15) as r:
            if r.status != 200: raise SystemExit(f'Telegram delivery failed: HTTP {r.status}')
    print('Telegram digest delivered')
if __name__=='__main__': main()
