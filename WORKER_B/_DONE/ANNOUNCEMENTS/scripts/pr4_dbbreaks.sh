#!/usr/bin/env bash
# B5–B6: each drops one rule of closure_extension_key on masaha_b_test only, runs db/closureExtensions.api.test.ts
# (red), restores the rule with the migration's own statement, and runs it again (green).
cd /c/dev/masaha/app-b || exit 9
PSQL=(docker exec -i masaha-postgres-1 psql -U masaha -d masaha_b_test -v ON_ERROR_STOP=1 -q)
run() {
  npm exec -w @masaha/api -- vitest run --project api src/db/closureExtensions.api.test.ts 2>&1 \
    | sed 's/\x1b\[[0-9;]*m//g' | grep -E '^\s+×|Tests\s+[0-9]|AssertionError|promise resolved' | head -8
}
brk() {
  local id=$1 drop=$2 restore=$3
  echo "== $id: $drop"
  echo "$drop" | "${PSQL[@]}" || { echo "!!! $id drop failed"; return; }
  run
  echo "$restore" | "${PSQL[@]}" || { echo "!!! $id RESTORE FAILED"; return; }
  echo "   restored; run again:"
  run
}
brk B5 'DROP TRIGGER "announcements_guard_extended" ON "announcements";' \
  'CREATE TRIGGER "announcements_guard_extended" BEFORE UPDATE OF "type", "starts_at", "ends_at", "deleted_at" ON "announcements" FOR EACH ROW WHEN (OLD."type" = '"'"'CLOSURE'"'"') EXECUTE FUNCTION "announcements_guard_extended"();'
brk B6 'DROP INDEX "closure_extensions_request_id_key";' \
  'CREATE UNIQUE INDEX "closure_extensions_request_id_key" ON "closure_extensions"("request_id");'
echo "== the rules now:"
echo "SELECT tgname FROM pg_trigger WHERE tgname = 'announcements_guard_extended'; SELECT indexdef FROM pg_indexes WHERE indexname = 'closure_extensions_request_id_key';" | "${PSQL[@]}" -t
