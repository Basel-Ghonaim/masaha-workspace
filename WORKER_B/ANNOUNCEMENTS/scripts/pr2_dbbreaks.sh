#!/usr/bin/env bash
# B3–B5: each drops one rule of data_report_rules on masaha_b_test only, runs db/dataReports.api.test.ts (red),
# restores the rule with the migration's own statement, and runs it again (green).
cd /c/dev/masaha/app-b || exit 9
PSQL=(docker exec -i masaha-postgres-1 psql -U masaha -d masaha_b_test -v ON_ERROR_STOP=1 -q)
run() {
  npm exec -w @masaha/api -- vitest run --project api src/db/dataReports.api.test.ts 2>&1 \
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
brk B3 'DROP INDEX "data_reports_open_key";' \
  'CREATE UNIQUE INDEX "data_reports_open_key" ON "data_reports"("user_id", "space_id", "field") WHERE ("status" = '"'"'OPEN'"'"');'
brk B4 'ALTER TABLE "data_reports" DROP CONSTRAINT "data_reports_decision_check";' \
  'ALTER TABLE "data_reports" ADD CONSTRAINT "data_reports_decision_check" CHECK (("status" = '"'"'OPEN'"'"') = ("resolved_at" IS NULL) AND ("resolved_at" IS NULL) = ("resolved_by_id" IS NULL) AND ("resolved_at" IS NULL) = ("resolved_as" IS NULL) AND ("status" <> '"'"'OPEN'"'"' OR "resolution_note" IS NULL) AND ("resolution_note" IS NULL OR btrim("resolution_note") <> '"''"'));'
brk B5 'ALTER TABLE "data_reports" DROP CONSTRAINT "data_reports_dismissal_note_check";' \
  'ALTER TABLE "data_reports" ADD CONSTRAINT "data_reports_dismissal_note_check" CHECK ("status" <> '"'"'DISMISSED'"'"' OR "resolution_note" IS NOT NULL);'
echo "== the rules now:"
echo "SELECT conname FROM pg_constraint WHERE conrelid = 'data_reports'::regclass AND contype = 'c' ORDER BY 1; SELECT indexdef FROM pg_indexes WHERE indexname = 'data_reports_open_key';" | "${PSQL[@]}" -t
