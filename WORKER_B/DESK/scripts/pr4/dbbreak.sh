#!/bin/bash
# Usage: dbbreak.sh <break sql> <restore sql> <test file...>; runs on masaha_b_test only.
S=/c/dev/masaha/workspace/WORKER_B/DESK/scripts/pr4
U=$(grep -E '^DATABASE_URL=' /c/dev/masaha/app-b/apps/api/.env | sed -E 's#.*://([^:]*):.*#\1#')
psql() { docker exec -i masaha-postgres-1 psql -v ON_ERROR_STOP=1 -U "$U" -d masaha_b_test -q; }
brk=$1; rst=$2; shift 2
psql < "$brk" || { echo "BREAK NOT MADE"; exit 2; }
cd /c/dev/masaha/app-b/apps/api
echo "== broken:"; npx vitest run --project api "$@" 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | grep -E "Tests  |Test Files|AssertionError|Error:|×" | head -12
psql < "$rst" || { echo "RESTORE FAILED"; exit 3; }
echo "== restored:"; npx vitest run --project api "$@" 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | grep -E "Tests  |Test Files|×" | head -6
docker exec masaha-postgres-1 psql -U "$U" -d masaha_b_test -tAc "SELECT prosrc LIKE '%payments_visit_written_off%' FROM pg_proc WHERE proname = 'payments_guard_insert'; SELECT count(*) FROM pg_constraint WHERE conname = 'visits_write_off_check'"
