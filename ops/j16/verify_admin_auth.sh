#!/usr/bin/env bash
set -euo pipefail
base="${1:-https://api.116.212.72.79.nip.io}"
public_code="$(curl -sS -o /dev/null -w '%{http_code}' "$base/api/context")"
admin_code="$(curl -sS -o /dev/null -w '%{http_code}' "$base/api/admin/operational-health")"
[[ "$public_code" == 200 ]] || { echo "PUBLIC_CONTEXT_FAIL:$public_code"; exit 1; }
[[ "$admin_code" == 401 ]] || { echo "ADMIN_UNAUTH_FAIL:$admin_code"; exit 1; }
echo 'ADMIN_AUTH_BOUNDARY_PASS public=200 admin_unauth=401'
