#!/usr/bin/env python3
import argparse, subprocess, sys
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-id', required=True)
    ap.add_argument('--window-date', help='Asia/Jakarta YYYY-MM-DD; defaults to current WIB date')
    ap.add_argument('--limit', type=int, default=3)
    ap.add_argument('--timeout', type=float, default=15)
    ap.add_argument('--max-attempts', type=int, default=2)
    ap.add_argument('--retry-delay-seconds', type=float, default=5)
    a = ap.parse_args()
    window = a.window_date or datetime.now(ZoneInfo('Asia/Jakarta')).date().isoformat()
    try:
        datetime.strptime(window, '%Y-%m-%d')
    except ValueError:
        raise SystemExit('--window-date must be YYYY-MM-DD')
    key = f'j14-scheduled:{a.project_id}:{window}'
    cmd = [sys.executable, str(ROOT/'tools'/'run_continuous_pilot.py'),
           '--project-id', a.project_id, '--trigger-type', 'SCHEDULED',
           '--idempotency-key', key, '--limit', str(a.limit),
           '--timeout', str(a.timeout), '--max-attempts', str(a.max_attempts),
           '--retry-delay-seconds', str(a.retry_delay_seconds)]
    raise SystemExit(subprocess.run(cmd).returncode)

if __name__ == '__main__':
    main()
